"""Topology-vs-implementation control study for the noise-robustness ordering.

The Month-4 noise-robustness ordering (README section 9, locked run
results/noise-robustness/2026-07-03T0213Z) compares topologies through their
GATE-LEVEL circuits, which differ in u/cx count and synthesis. Under the
pinned per-gate depolarizing model the orderings could therefore be a
gate-budget artifact ("more gates = more noise") rather than a topology
effect. This script runs the controls:

  census     u/cx counts + depth of the exact production circuit per topology
  control A  gate-count-matched circuits: every topology padded with identity
             pads (cx*cx pairs, u(0,0,0)) up to the max u/cx budget at that N,
             over 5 pad placements (placement is a nuisance parameter)
  control B  realization variance: same entangler unitary, different circuit
             -- transpiler optimization levels {0,2,3} (production is 1),
             edge-order shuffles for the pairwise topologies (commuting RXX
             factors), CX-ladder direction variants for GHZ
  control C  per-2q-gate normalization of the initial advantage decay rate
             (if per-gate rates coincide, the ordering is a gate-count story)
  nulls      wiring-permutation invariance of the MEAN payoff (exact under the
             all-qubit-uniform noise model) and instruction-reorder invariance
             (depth is not a free parameter in a per-gate noise model: two
             circuits with the same per-qubit instruction order are the same
             channel, so matched-count controls subsume matched-depth ones)

Metric = the locked run's own: advantage(p) = mean (Q,..,Q) payoff minus the
noisy classical NE payoff (pure NE of the {D,H}^N tensor evaluated through
the SAME noisy circuit, highest-mean NE), plus q_is_nash from the 2N
unilateral deviations. Restricted evaluation (2^N + 2N + 1 profiles instead
of 3^N) -- identical numbers for these quantities, anchored against the
locked CSV before anything else runs.

All five topologies (ghz, w, ring, star, fully-connected) run at N=3,4,5;
the locked claims cover ghz/w/ring, star/full get their first controlled
noise curves. Simulation only -- zero hardware quota.

Usage (pinned env):
  conda run -n entangled-equilibria python scripts/topology_noise_controls.py
  ... --smoke   # N=3 only, reduced grids, no files written

Writes results/topology-controls/<UTC>/results.json.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpu_limit  # noqa: E402,F401  (caps BLAS threads; MUST precede numpy import)

import numpy as np  # noqa: E402
from qiskit import QuantumCircuit, transpile  # noqa: E402
from qiskit.circuit.library import UnitaryGate  # noqa: E402
from qiskit.quantum_info import Operator  # noqa: E402
from qiskit_aer import AerSimulator  # noqa: E402

from circuits.ewl import DOVE, HAWK, U, q_strategy  # noqa: E402
from circuits.gate_level import pairwise_gate_circuit  # noqa: E402
from circuits.noise import (  # noqa: E402
    _PINNED_BASIS,
    _transpiled_entangler,
    build_ewl_circuit_noisy,
    build_noise_model,
)
from circuits.topology_graphs import topology_graph  # noqa: E402
from config import C, GAMMA, V  # noqa: E402
from experiment.topology_registry import (  # noqa: E402
    canonical,
    resolve,
    resolve_gate_circuit,
)
from game.nash import find_pure_nash  # noqa: E402
from game.payoffs import expected_payoff  # noqa: E402

TOPOS = ("ghz", "w", "ring", "star", "fully-connected")
NS = (3, 4, 5)
P_FULL = tuple(round(0.005 * k, 3) for k in range(11))  # locked run's grid
P_CTRL = (0.01, 0.02, 0.05)
PLACEMENTS = ("pre", "post", "middle", "rand1", "rand2")
SEED = 20260716
NE_TOL = 1e-9  # find_pure_nash tolerance (production value)
LOCKED = os.path.join(os.path.dirname(__file__), "..", "results",
                      "noise-robustness", "2026-07-03T0213Z", "results.csv")

_SIM = AerSimulator(method="density_matrix")


# ── circuit realizations (all verified against the dense entangler) ────────────


def entangler_variants(topology: str, N: int, rng: np.random.Generator) -> dict:
    """Named J realizations in the {u,cx} basis. 'production' is the cached
    Month-4 circuit every locked claim ran on."""
    out = {"production": _transpiled_entangler(canonical(topology), N, GAMMA)[0]}
    raw = resolve_gate_circuit(topology, N, GAMMA)
    for lvl in (0, 2, 3):
        out[f"opt{lvl}"] = transpile(raw, basis_gates=_PINNED_BASIS,
                                     optimization_level=lvl)
    if canonical(topology) in ("ring", "star", "fully-connected"):
        edges = [(int(i), int(j))
                 for i, j in topology_graph(canonical(topology), N).edges()]
        for k in range(4):
            perm = list(edges)
            rng.shuffle(perm)
            qc = pairwise_gate_circuit(perm, N, GAMMA)
            out[f"edges{k}"] = transpile(qc, basis_gates=_PINNED_BASIS,
                                         optimization_level=1)
    if canonical(topology) == "ghz":
        out["ladder-rev"] = transpile(_ghz_ladder_reversed(N),
                                      basis_gates=_PINNED_BASIS,
                                      optimization_level=1)
    return out


def _ghz_ladder_reversed(N: int) -> QuantumCircuit:
    """Same exp(+i*gamma/2 X^(x)N) unitary, parity accumulated onto qubit 0."""
    qc = QuantumCircuit(N)
    qc.h(range(N))
    for q in range(N - 1, 0, -1):
        qc.cx(q, q - 1)
    qc.rz(-GAMMA, 0)
    for q in range(1, N):
        qc.cx(q, q - 1)
    qc.h(range(N))
    return qc


def verify_variant(j_c: QuantumCircuit, topology: str, N: int) -> None:
    dense = resolve(topology, N)(N, GAMMA)
    if not Operator(j_c).equiv(Operator(dense)):
        print(f"VARIANT MISMATCH: {topology} N={N} realization is not J")
        sys.exit(1)


# ── assembly + padding ─────────────────────────────────────────────────────────


def assemble(j_c: QuantumCircuit, N: int, params_list: list) -> QuantumCircuit:
    """J . U-layer . J-dagger translated to {u,cx} -- the production tail."""
    qc = QuantumCircuit(N)
    qc.compose(j_c, inplace=True)
    for q, params in enumerate(params_list):
        qc.append(UnitaryGate(U(*params), label="U"), [q])
    qc.compose(j_c.inverse(), inplace=True)
    return transpile(qc, basis_gates=_PINNED_BASIS, optimization_level=0)


def gate_counts(qc: QuantumCircuit) -> tuple[int, int]:
    ops = qc.count_ops()
    return int(ops.get("u", 0)), int(ops.get("cx", 0))


def pad_instructions(N: int, d_u: int, d_cx_pairs: int) -> list:
    """Identity pads: d_u u(0,0,0) round-robin over qubits, d_cx_pairs cx*cx
    pairs round-robin over (q, q+1 mod N)."""
    pads = []
    for k in range(d_u):
        pads.append(("u", (k % N,)))
    for k in range(d_cx_pairs):
        a = k % N
        pair = (a, (a + 1) % N)
        pads.append(("cx", pair))
        pads.append(("cx", pair))
    return pads


def apply_pads(tqc: QuantumCircuit, pads: list, placement: str,
               rng: np.random.Generator) -> QuantumCircuit:
    """Insert pad instructions at slots determined by `placement`. cx pairs are
    kept adjacent so the inserted block is exactly identity wherever it lands."""
    n_slots = len(tqc.data) + 1
    if placement == "pre":
        slots = [0] * len(pads)
    elif placement == "post":
        slots = [n_slots - 1] * len(pads)
    elif placement == "middle":
        slots = [n_slots // 2] * len(pads)
    else:
        slots = []
        i = 0
        while i < len(pads):
            width = 2 if pads[i][0] == "cx" else 1  # cx pads travel as pairs
            slots.extend([int(rng.integers(0, n_slots))] * width)
            i += width
    out = tqc.copy_empty_like()
    by_slot: dict[int, list] = {}
    for pad, s in zip(pads, slots):
        by_slot.setdefault(s, []).append(pad)
    for idx in range(len(tqc.data) + 1):
        for kind, qubits in by_slot.get(idx, []):
            if kind == "u":
                out.u(0.0, 0.0, 0.0, qubits[0])
            else:
                out.cx(*qubits)
        if idx < len(tqc.data):
            ci = tqc.data[idx]
            out.append(ci.operation, ci.qubits, ci.clbits)
    return out


# ── restricted cell evaluation (anchored against the locked CSV) ───────────────


def profile_set(N: int) -> list[tuple[str, ...]]:
    classical = list(product("DH", repeat=N))
    qprof = tuple("Q" for _ in range(N))
    devs = []
    for player in range(N):
        for alt in "DH":
            d = list(qprof)
            d[player] = alt
            devs.append(tuple(d))
    return classical + [qprof] + devs


def build_cell_circuits(j_c: QuantumCircuit, N: int, pads: list,
                        placement: str, rng: np.random.Generator) -> dict:
    """One translated+padded circuit per profile; reusable across all p."""
    smap = {"D": DOVE, "H": HAWK, "Q": q_strategy(N)}
    circs = {}
    for prof in profile_set(N):
        tqc = assemble(j_c, N, [smap[s] for s in prof])
        if pads:
            tqc = apply_pads(tqc, pads, placement, rng)
        tqc.save_probabilities()
        circs[prof] = tqc
    return circs


def evaluate_cell(circs: dict, N: int, p: float) -> dict:
    """advantage / classical NE / q_is_nash from one batched noisy run."""
    profs = list(circs)
    sim = AerSimulator(method="density_matrix",
                       noise_model=build_noise_model(p)) if p > 0 else _SIM
    result = sim.run(list(circs.values())).result()
    tensor = {}
    for i, prof in enumerate(profs):
        probs = np.asarray(result.data(i)["probabilities"], dtype=np.float64)
        tensor[prof] = expected_payoff(probs / probs.sum(), N, V, C)
    classical = {pr: t for pr, t in tensor.items()
                 if all(s in "DH" for s in pr)}
    ne = find_pure_nash(classical, N, ["D", "H"])
    ne_pay = (max(float(np.mean(tensor[pr])) for pr in ne)
              if ne else float("nan"))
    qprof = tuple("Q" for _ in range(N))
    qvec = tensor[qprof]
    q_is_nash = all(
        tensor[tuple("Q" if j != player else alt for j in range(N))][player]
        <= qvec[player] + NE_TOL
        for player in range(N) for alt in "DH"
    )
    return {"advantage": float(np.mean(qvec)) - ne_pay,
            "q_payoff": float(np.mean(qvec)),
            "q_payoff_vector": [float(x) for x in qvec],
            "classical_ne_payoff": ne_pay,
            "n_classical_ne": len(ne),
            "q_is_nash": bool(q_is_nash)}


# ── anchors + nulls ────────────────────────────────────────────────────────────


def read_locked_csv() -> dict:
    import csv
    rows = {}
    with open(LOCKED, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            key = (r["topology"], int(r["N"]), float(r["noise_p"]))
            rows[key] = {"advantage": float(r["advantage"]),
                         "classical_ne_payoff": float(r["classical_ne_payoff"]),
                         "q_is_nash": r["q_is_nash"] == "True"}
    return rows


def anchor_gate(rng: np.random.Generator, smoke: bool) -> None:
    """My restricted pipeline must reproduce the locked CSV cells exactly."""
    locked = read_locked_csv()
    cells = [("ghz", 3), ("ring", 3), ("w", 3)]
    if not smoke:
        cells += [("ghz", 5), ("ring", 5), ("w", 5)]
    print("=== anchor gate vs locked results.csv ===")
    worst = 0.0
    for topo, N in cells:
        j_c = _transpiled_entangler(canonical(topo), N, GAMMA)[0]
        circs = build_cell_circuits(j_c, N, [], "post", rng)
        for p in (0.02, 0.05):
            mine = evaluate_cell(circs, N, p)
            ref = locked[(canonical(topo), N, p)]
            d = max(abs(mine["advantage"] - ref["advantage"]),
                    abs(mine["classical_ne_payoff"] - ref["classical_ne_payoff"]))
            worst = max(worst, d)
            ok = d < 1e-9 and mine["q_is_nash"] == ref["q_is_nash"]
            print(f"  {topo:>5s} N={N} p={p}: |delta|={d:.2e} "
                  f"nash {mine['q_is_nash']}=={ref['q_is_nash']} "
                  f"{'PASS' if ok else 'FAIL'}")
            if not ok:
                sys.exit(1)
        # production-path cross-check on the Q profile
        probs_prod = build_ewl_circuit_noisy(
            N, [q_strategy(N)] * N, topology=topo, gamma=GAMMA, p=0.02)
        mine_q = evaluate_cell(circs, N, 0.02)["q_payoff"]
        d = abs(float(np.mean(expected_payoff(probs_prod, N, V, C))) - mine_q)
        if d > 1e-12:
            print(f"  {topo} N={N}: runner deviates from production ({d:.2e})")
            sys.exit(1)
    print(f"  all anchors PASS (worst |delta| {worst:.2e})")


def null_checks(rng: np.random.Generator) -> dict:
    """Wiring permutation leaves the MEAN payoff invariant (mapping null);
    reordering commuting disjoint instructions leaves everything invariant
    (depth null). Both exact properties of the per-gate noise model."""
    print("=== null checks (mapping + depth) ===")
    N, p, topo = 5, 0.02, "ring"
    j_c = _transpiled_entangler(canonical(topo), N, GAMMA)[0]
    smap_q = [q_strategy(N)] * N
    base = assemble(j_c, N, smap_q)
    base_s = base.copy()
    base_s.save_probabilities()
    sim = AerSimulator(method="density_matrix", noise_model=build_noise_model(p))
    p0 = np.asarray(sim.run(base_s).result().data(0)["probabilities"])
    m0 = float(np.mean(expected_payoff(p0 / p0.sum(), N, V, C)))

    # mapping null: J on permuted wires (U layer symmetric at (Q,..,Q))
    perm = [1, 2, 3, 4, 0]
    qc = QuantumCircuit(N)
    qc.compose(j_c, qubits=perm, inplace=True)
    for q in range(N):
        qc.append(UnitaryGate(U(*q_strategy(N)), label="U"), [q])
    qc.compose(j_c.inverse(), qubits=perm, inplace=True)
    tqc = transpile(qc, basis_gates=_PINNED_BASIS, optimization_level=0)
    tqc.save_probabilities()
    pp = np.asarray(sim.run(tqc).result().data(0)["probabilities"])
    mp = float(np.mean(expected_payoff(pp / pp.sum(), N, V, C)))
    d_map = abs(mp - m0)

    # depth null: ASAP-repack the instruction list (per-qubit order preserved)
    asap = base.copy_empty_like()
    pending = list(base.data)
    busy_until: dict[int, int] = {}
    order = []
    for ci in pending:
        qs = [base.find_bit(q).index for q in ci.qubits]
        t = max((busy_until.get(q, 0) for q in qs), default=0)
        for q in qs:
            busy_until[q] = t + 1
        order.append((t, len(order), ci))
    for _, _, ci in sorted(order, key=lambda x: (x[0], x[1])):
        asap.append(ci.operation, ci.qubits, ci.clbits)
    asap_s = asap.copy()
    asap_s.save_probabilities()
    pa = np.asarray(sim.run(asap_s).result().data(0)["probabilities"])
    d_depth = float(np.max(np.abs(pa - p0)))
    print(f"  mapping null: |mean payoff delta| = {d_map:.2e} "
          f"(depth {base.depth()} both)")
    print(f"  depth null:   base depth {base.depth()} -> repacked "
          f"{asap.depth()}, max |prob delta| = {d_depth:.2e}")
    if d_map > 1e-9 or d_depth > 1e-9:
        print("  NULL CHECK FAILED -- model assumptions wrong, aborting")
        sys.exit(1)
    return {"mapping_mean_delta": d_map, "depth_prob_delta": d_depth,
            "depth_base": base.depth(), "depth_repacked": asap.depth()}


# ── study ──────────────────────────────────────────────────────────────────────


def main() -> None:
    smoke = "--smoke" in sys.argv
    ns = (3,) if smoke else NS
    p_full = (0.0, 0.02, 0.05) if smoke else P_FULL
    p_ctrl = (0.02,) if smoke else P_CTRL
    placements = ("pre", "post") if smoke else PLACEMENTS
    rng = np.random.default_rng(SEED)

    anchor_gate(rng, smoke)
    nulls = null_checks(rng)

    results: dict = {"census": {}, "baseline": {}, "count_matched": {},
                     "realizations": {}, "nulls": nulls}

    # census + baseline sweep on the production realization
    print("=== census + baseline sweep (production realization) ===")
    circs_cache: dict = {}
    for N in ns:
        for topo in TOPOS:
            j_c = _transpiled_entangler(canonical(topo), N, GAMMA)[0]
            verify_variant(j_c, topo, N)
            circs = build_cell_circuits(j_c, N, [], "post", rng)
            circs_cache[(topo, N)] = circs
            qprof = tuple("Q" for _ in range(N))
            # counts include the U layer -- identical across topologies
            n_u, n_cx = gate_counts(circs[qprof])
            results["census"][f"{topo}|{N}"] = {
                "n_u": n_u, "n_cx": n_cx,
                "depth": circs[qprof].depth() - 1,  # minus save instruction
            }
            sweep = {}
            for p in p_full:
                sweep[str(p)] = evaluate_cell(circs, N, p)
            results["baseline"][f"{topo}|{N}"] = sweep
            a0 = sweep["0.0"]["advantage"]
            a5 = sweep[str(p_full[-1])]["advantage"]
            print(f"  {topo:>15s} N={N}: u={n_u:3d} cx={n_cx:3d} "
                  f"depth={results['census'][f'{topo}|{N}']['depth']:3d}  "
                  f"A(0)={a0:+.4f}  A({p_full[-1]})={a5:+.4f}")

    # control A: count-matched circuits
    print("=== control A: gate-count-matched (pad placements: "
          f"{placements}) ===")
    for N in ns:
        t_u = max(results["census"][f"{t}|{N}"]["n_u"] for t in TOPOS)
        t_cx = max(results["census"][f"{t}|{N}"]["n_cx"] for t in TOPOS)
        results["count_matched"][str(N)] = {"target_u": t_u, "target_cx": t_cx,
                                            "cells": {}}
        for topo in TOPOS:
            c = results["census"][f"{topo}|{N}"]
            d_u, d_cx = t_u - c["n_u"], t_cx - c["n_cx"]
            pairs, resid = divmod(d_cx, 2)  # cx pads are identity PAIRS;
            # an odd deficit leaves the count 1 short (immaterial vs the
            # 2-10x baseline spread) -- recorded per cell as cx_residual.
            for plc in placements:
                if d_u == 0 and d_cx == 0:
                    cell_res = {str(p): results["baseline"][f"{topo}|{N}"][str(p)]
                                for p in p_ctrl}
                else:
                    pads = pad_instructions(N, d_u, pairs)
                    circs = build_cell_circuits(
                        _transpiled_entangler(canonical(topo), N, GAMMA)[0],
                        N, pads, plc, rng)
                    qprof = tuple("Q" for _ in range(N))
                    got_u, got_cx = gate_counts(circs[qprof])
                    assert got_u == t_u and got_cx == t_cx - resid, \
                        f"pad miscount {topo} N={N}: {got_u},{got_cx}"
                    cell_res = {str(p): evaluate_cell(circs, N, p)
                                for p in p_ctrl}
                results["count_matched"][str(N)]["cells"][f"{topo}|{plc}"] = {
                    "cx_residual": resid, **cell_res}
            a = results["count_matched"][str(N)]["cells"][f"{topo}|{placements[0]}"]
            print(f"  {topo:>15s} N={N}: padded to u={t_u} cx={t_cx - resid} "
                  f"A({p_ctrl[-1]})={a[str(p_ctrl[-1])]['advantage']:+.4f} "
                  f"[{placements[0]}]")

    # control B: realization variants
    print("=== control B: realization variants ===")
    for N in ns:
        for topo in TOPOS:
            variants = entangler_variants(topo, N, rng)
            for name, j_c in variants.items():
                if name == "production":
                    continue  # baseline already covers it
                verify_variant(j_c, topo, N)
                circs = build_cell_circuits(j_c, N, [], "post", rng)
                qprof = tuple("Q" for _ in range(N))
                n_u, n_cx = gate_counts(circs[qprof])
                cell_res = {str(p): evaluate_cell(circs, N, p) for p in p_ctrl}
                results["realizations"][f"{topo}|{N}|{name}"] = {
                    "n_u": n_u, "n_cx": n_cx, **cell_res}
            row = " ".join(
                f"{name}:cx={results['realizations'][f'{topo}|{N}|{name}']['n_cx']}"
                for name in variants if name != "production")
            print(f"  {topo:>15s} N={N}: {row}")

    # control C: per-2q-gate normalized initial decay (from baseline sweep)
    print("=== control C: per-cx-normalized decay rates ===")
    results["decay_rates"] = {}
    for N in ns:
        for topo in TOPOS:
            sw = results["baseline"][f"{topo}|{N}"]
            a0 = sw["0.0"]["advantage"]
            if abs(a0) < 1e-6:  # no noiseless advantage -> no decay rate
                results["decay_rates"][f"{topo}|{N}"] = {
                    "lambda": None, "lambda_per_cx": None,
                    "note": "A(0)=0; retention undefined"}
                print(f"  {topo:>15s} N={N}: A(0)=0 -- decay rate undefined")
                continue
            p1 = str(p_full[1])
            lam = (a0 - sw[p1]["advantage"]) / (float(p1) * a0)
            n_cx = results["census"][f"{topo}|{N}"]["n_cx"]
            results["decay_rates"][f"{topo}|{N}"] = {
                "lambda": lam, "lambda_per_cx": lam / n_cx}
            print(f"  {topo:>15s} N={N}: lambda={lam:7.2f}  "
                  f"lambda/cx={lam / n_cx:6.3f}")

    if smoke:
        print("\n--smoke: no files written")
        return

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results",
                           "topology-controls", ts)
    os.makedirs(out_dir, exist_ok=True)
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                         text=True).strip()
    except Exception:  # noqa: BLE001
        commit = None
    payload = {
        "experiment": "topology-noise-controls",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "seed": SEED,
        "game": {"V": V, "C": C, "gamma": "pi/2"},
        "locked_run": "results/noise-robustness/2026-07-03T0213Z",
        "notes": ("metric = locked run's advantage (Q payoff minus noisy "
                  "classical NE payoff, restricted evaluation, anchored); "
                  "depth is not independently variable under per-gate noise "
                  "(see nulls); star/fully-connected have no locked claims "
                  "-- their rows are first controlled curves, not re-tests."),
        **results,
    }
    with open(os.path.join(out_dir, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"\nsaved: {os.path.relpath(os.path.join(out_dir, 'results.json'))}")


if __name__ == "__main__":
    main()
