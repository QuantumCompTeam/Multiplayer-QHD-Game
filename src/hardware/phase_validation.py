"""New phase-branch experiment, separate from all historical registrations."""
from __future__ import annotations

import math

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator, Statevector

from circuits.ewl import U
from circuits.gate_level import ghz_gate_circuit
from circuits.n_player import build_ewl_qc
from game.compact_ghz import compact_payoffs
from game.observable_payoffs import counts_summary
from game.phase_branches import counter_strategy, phase_strategy


def experiment_rows(ns=(3,4,5,6,7), *, common_menu=False, pilot=False):
    rows = []
    def add(n, m, kind, player=None, alternative=None):
        profile = [phase_strategy(n,m)]*n
        if player is not None:
            profile[player] = alternative
        rows.append({'id': f'n{n}-{kind}' + (f'-j{player}' if player is not None else ''),
                     'N':n,'branch':m,'kind':kind,'player':player,
                     'strategies':[list(p) for p in profile]})
    for n in ns:
        if not isinstance(n,int) or not 3 <= n <= 7:
            raise ValueError('validated hardware range is N=3..7')
        m = n//2
        add(n,m,'candidate')
        for j in (range(1) if pilot else range(n)):
            add(n,m,'H',j,(math.pi,0.,0.))
            add(n,m,'D',j,(0.,0.,0.))
            if common_menu and m != 1:
                add(n,m,'old_Q',j,phase_strategy(n,1))
        if m != 1:
            add(n,1,'original')
            add(n,1,'original_H',0,(math.pi,0.,0.))
        add(n,m,'unrestricted',0,counter_strategy(n,m))
    return rows


def validated_circuit(row):
    """Dense operator identity AND full ideal output checks, before measurement."""
    n = row['N']
    profile = [tuple(p) for p in row['strategies']]
    j = ghz_gate_circuit(n)
    qc = QuantumCircuit(n)
    qc.compose(j,inplace=True)
    qc.barrier()
    for k,p in enumerate(profile):
        qc.append(UnitaryGate(U(*p)),[k])
    qc.barrier()
    qc.compose(j.inverse(),inplace=True)
    reference = build_ewl_qc(n,profile)
    if not Operator(qc).equiv(Operator(reference)):
        raise ValueError(f"operator identity failed: {row['id']}")
    actual = np.asarray(Statevector(qc).probabilities())
    ideal = np.asarray(Statevector(reference).probabilities())
    if not np.allclose(actual,ideal,atol=1e-10):
        raise ValueError('full output identity failed')
    prediction = compact_payoffs(profile)
    row['ideal_payoff_vector'] = prediction['payoff_vector'].tolist()
    row['ideal_probabilities'] = actual.tolist()
    qc.measure_all()
    return qc


def judge(rows, counts, *, alpha=.05, epsilon=.05, pilot=False):
    """Simultaneous finite-sample Hoeffding bounds on raw deviation gains.

Bounds cover both means in every primary gap, using reward range [0,V].
Calibration/SPAM are part of the measured implemented game, not corrected away.
Shots must be independent within each stationary circuit distribution; drift
is evaluated by separate epochs. Pilot output never certifies all players.
    """
    if len(rows) != len(counts) or not 0 < alpha < 1 or epsilon < 0:
        raise ValueError('invalid counts or confidence configuration')
    summaries = {r['id']:counts_summary(c) for r,c in zip(rows,counts)}
    primary = [r for r in rows if r['kind'] in ['H','D','old_Q']]
    m = len(primary)
    gaps = []
    for row in primary:
        n,j = row['N'],row['player']
        coop = summaries[f'n{n}-candidate']
        dev = summaries[row['id']]
        observed = coop['per_player'][j]-dev['per_player'][j]
        radius = sum(4*math.sqrt(math.log(2*m/alpha)/(2*s['shots'])) for s in [coop,dev])
        gaps.append({'id':row['id'],'N':n,'player':j,'gap':observed,
                     'simultaneous_lower_gap':observed-radius,
                     'simultaneous_upper_normalized_gain':(-observed+radius)/(4/n)})
    complete = all(
        {r['player'] for r in primary if r['N']==n and r['kind']==kind} == set(range(n))
        for n in {r['N'] for r in rows} for kind in ['H','D'])
    passed = bool(gaps) and complete and not pilot and all(
        g['simultaneous_upper_normalized_gain'] <= epsilon for g in gaps)
    return {'scope':'raw implemented restricted-menu game; no SU(2) equilibrium claim',
            'pilot':pilot,'complete_D_H_coverage':complete,'alpha':alpha,'epsilon':epsilon,
            'epsilon_equilibrium_supported':passed,'gaps':gaps,'summaries':summaries}
