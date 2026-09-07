"""Prepare and simulate a new phase experiment. Never submits IBM jobs.

Default: offline ideal and depolarizing rehearsal. --backend additionally
authenticates read-only, pins/compiles a chain and rehearses its device model.
Outputs are a draft, not a committed preregistration.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'experiments'))
import numpy as np
from qiskit import QuantumCircuit, qpy, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from circuits.noise import build_noise_model
from hardware.phase_validation import experiment_rows, judge, validated_circuit
from results_io import write_metadata


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--ns',default='3,4,5,6,7')
    p.add_argument('--shots',type=int,default=4096)
    p.add_argument('--pilot',action='store_true')
    p.add_argument('--common-menu',action='store_true')
    p.add_argument('--backend')
    p.add_argument('--chain',help='Explicit comma-separated physical qubits; otherwise select once and record')
    args = p.parse_args()
    if args.output.exists():
        p.error('output exists; use a fresh directory to preserve evidence')
    if args.shots < 2:
        p.error('shots must be >= 2')
    ns = sorted(set(int(n) for n in args.ns.split(',')))
    rows = experiment_rows(ns,common_menu=args.common_menu,pilot=args.pilot)
    circuits = [validated_circuit(row) for row in rows]
    width = max(ns)
    for bit in [0,1]:
        cal = QuantumCircuit(width)
        if bit:
            cal.x(range(width))
        cal.measure_all()
        circuits.append(cal)
    calibration = None
    chain = None
    if args.backend:
        from qiskit_ibm_runtime import QiskitRuntimeService
        from hardware_scaling import find_chain, chain_calibration, reduce_isa, reduce_noise_model
        from qiskit_aer.noise import NoiseModel
        backend = QiskitRuntimeService().backend(args.backend)
        chain = [int(x) for x in args.chain.split(',')] if args.chain else find_chain(backend,width)
        if len(chain) != width or len(set(chain)) != width:
            raise ValueError('chain width must equal max N and contain distinct physical qubits')
        calibration = chain_calibration(backend,chain)
        isa = [transpile(qc,backend=backend,initial_layout=chain[:qc.num_qubits],
                         optimization_level=1,seed_transpiler=907) for qc in circuits]
        noise = NoiseModel.from_backend(backend)
        samples = []
        for index,qc in enumerate(isa):
            n = rows[index]['N'] if index < len(rows) else width
            physical = [None]*n
            for inst in qc.data:
                if inst.operation.name == 'measure':
                    physical[qc.find_bit(inst.clbits[0]).index] = qc.find_bit(inst.qubits[0]).index
            if physical != chain[:n]:
                raise ValueError('routing changed the registered measurement mapping')
            small = reduce_isa(qc,chain[:n])
            ideal = Statevector(small.remove_final_measurements(inplace=False)).probabilities()
            target = rows[index]['ideal_probabilities'] if index < len(rows) else None
            if index >= len(rows):
                target = np.eye(1,2**n,(index-len(rows))*(2**n-1))[0]
            if not np.allclose(ideal,target,atol=1e-9):
                raise ValueError('ISA ideal-output identity failed')
            sim = AerSimulator(method='density_matrix',noise_model=reduce_noise_model(noise,chain[:n]))
            samples.append(sim.run(small,shots=args.shots,seed_simulator=907+index).result().get_counts())
        circuits = isa
        rehearsal_kind = 'device_model'
    else:
        compiled = transpile(circuits,basis_gates=['u','cx'],optimization_level=0,seed_transpiler=907)
        sim = AerSimulator(method='density_matrix',noise_model=build_noise_model(.002))
        result = sim.run(compiled,shots=args.shots,seed_simulator=907).result()
        samples = [result.get_counts(i) for i in range(len(compiled))]
        rehearsal_kind = 'illustrative_depolarizing_p_0.002_not_device_model'
    args.output.mkdir(parents=True)
    with (args.output/'circuits.qpy').open('wb') as handle:
        qpy.dump(circuits,handle)
    manifest = {'status':'DRAFT: not committed or submitted',
                'created_utc':datetime.now(timezone.utc).isoformat(),
                'backend':args.backend,'chain':chain,'shots':args.shots,
                'pilot':args.pilot,'common_menu':args.common_menu,'rows':rows,
                'calibration_circuits':2,'pub_count':len(circuits),
                'alpha':.05,'epsilon':.05,'transpiler_seed':907,
                'optimization_level':1 if args.backend else None,
                'offline_rehearsal_optimization_level':None if args.backend else 0,
                'max_execution_time_seconds':60 if args.pilot else 100,
                'rehearsal_kind':rehearsal_kind,'calibration':calibration,
                'qpy_sha256':hashlib.sha256((args.output/'circuits.qpy').read_bytes()).hexdigest(),
                'code_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
                    ['src/hardware/phase_validation.py','src/game/phase_branches.py',
                     'src/game/observable_payoffs.py','scripts/prepare_phase_hardware.py',
                     'scripts/run_phase_hardware.py']},
                'gate_counts':[dict(qc.count_ops()) for qc in circuits]}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    decision = judge(rows,samples[:len(rows)],pilot=args.pilot)
    (args.output/'rehearsal.json').write_text(json.dumps({'kind':rehearsal_kind,
        'counts':samples,'judgment':decision},indent=2)+'\n',encoding='utf-8')
    write_metadata(args.output,'phase-validation-draft',{'backend':args.backend,'shots':args.shots})
    print(json.dumps({'output':str(args.output),'pubs':len(circuits),'rehearsal':rehearsal_kind,
                      'supports_epsilon_equilibrium':decision['epsilon_equilibrium_supported']}))


if __name__ == '__main__':
    main()
