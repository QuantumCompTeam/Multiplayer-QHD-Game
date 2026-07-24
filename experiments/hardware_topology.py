"""Multi-topology EWL hardware batch (items 1, 2, 5, 6, 7).

Companion to experiments/hardware_scaling.py, which stays UNTOUCHED so that its
frozen preregistration (results/hardware-scaling/preregistration.json) and its
cross-day repeats (item 3) remain byte-comparable. That script fixes the GHZ
entangler, the all-Q profile, gamma=pi/2 and the identity wiring; this one
varies all four, which is what the paper's topology, equilibrium, noise and
fairness claims actually need in order to rest on device data.

Five experiment axes, one uniform pub record (see series_meta):

  topology  ghz | ring | star | fully-connected | w      -- item 1
  profile   per-player {D,H,Q}; deviations test equilibrium -- item 2
  fold      cz-fold factor; doubles as a hardware noise axis -- item 5 (+ ZNE)
  wiring    qubit->player permutation on the pinned set     -- item 6
  gamma     entanglement angle                              -- item 7

Modes:
  --report     Transpile report against the REAL coupling map: routed cz count
               and depth per (topology, N). Network read only, no job, no quota.
  --rehearse   Full dress rehearsal of the batch on the reduced device noise
               model, including the complete analysis. No job submitted.
  --hardware   Rehearse (mandatory gate), then submit ONE batch job, persisting
               the job id BEFORE polling.
  --from-job   Recover a submitted batch and analyse it.

Honesty notes carried into every saved result:
- "advantage" = measured profile payoff minus the ANALYTIC noiseless classical
  NE payoff 1/N. Simulation figures use a circuit-relative gap instead; the two
  are NOT comparable and must not share an axis.
- (Q,..,Q) is a restricted-menu pure NE only at N=3. At N>=4 it is a fixed
  cooperative protocol, not an equilibrium claim.
"""

import argparse
import json
import math
import os
import platform
import subprocess
import sys
import warnings
from datetime import datetime, timezone

# NoiseModel.from_dict is deprecated-but-functional in aer 0.14 and is the only
# way to rebuild the reduced device model; silence just that warning category.
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from game.payoffs import expected_payoff
from hardware.chain import best_linear_chain
from hardware.mitigation import (
    confusion_from_counts,
    counts_to_probs,
    mitigate_probs,
    zne_extrapolate,
)
from hardware.topology_hw import GATE_CIRCUITS, build_ewl_circuit, check_isa_on_set

GAMMA = math.pi / 2
FOLDS = (1, 3, 5)
DEFAULT_SHOTS = 4096
DEFAULT_BACKEND = "ibm_fez"
PIN_LEN = 5      # width of the pinned qubit set and of the readout-cal circuits
CZ_BUDGET = 60   # per-pub routed cz ceiling; Task 3's report justifies the value
REPORT_NS = (3, 4, 5)


# ── the uniform series record ─────────────────────────────────────────────────


def series_meta(*, topology, N, fold, gamma, profile, wiring, fil, cz) -> dict:
    """One uniform series record. Every experiment axis is a field here.

    Keeping all five axes in one record shape is the whole design: the plan
    builder, the analysis and the saved artifact all speak the same language,
    so adding an axis never means a new code path.
    """
    if len(wiring) != N:
        raise ValueError(f"wiring has {len(wiring)} entries but N={N}")
    if len(profile) != N:
        raise ValueError(f"profile has {len(profile)} entries but N={N}")
    return {"kind": "series", "topology": str(topology), "N": int(N),
            "fold": int(fold), "gamma": float(gamma), "profile": list(profile),
            "wiring": [int(w) for w in wiring], "fil": [int(q) for q in fil],
            "cz": int(cz)}


def series_key(meta: dict) -> str:
    """Stable identity of a series ACROSS folds (so ZNE has a series to fit)."""
    return (f"{meta['topology']}|N{meta['N']}|g{meta['gamma']:.6f}"
            f"|{''.join(meta['profile'])}|w{'-'.join(map(str, meta['wiring']))}")


# ── payoff estimator (identical to experiments/hardware_scaling.payoff_stats) ──


def _onehot(i: int, N: int) -> np.ndarray:
    v = np.zeros(2**N)
    v[i] = 1.0
    return v


def payoff_stats(probs: np.ndarray, N: int, shots: int) -> dict:
    """Mean profile payoff + multinomial shot-noise sigma of the mean.

    Deliberately the same estimator as the scaling script's, so topology runs
    and scaling runs stay numerically comparable. per_player is kept because
    items 6 and 7 read the per-player FLOOR, not the mean.
    """
    per_player = expected_payoff(probs, N)
    mean = float(np.mean(per_player))
    cbar = np.array([float(np.mean(expected_payoff(_onehot(i, N), N)))
                     for i in range(2**N)])
    var = float(np.sum(probs * cbar**2) - mean**2)
    return {"per_player": [float(x) for x in per_player],
            "mean": mean,
            "sigma": float(np.sqrt(max(var, 0.0) / shots)),
            "p_ground": float(probs[0])}


# ── batch plan ────────────────────────────────────────────────────────────────


def with_measurement(isa: QuantumCircuit, fil: list[int], n_meas: int) -> QuantumCircuit:
    """Append creg 'meas' and measure physical fil[j] -> clbit j."""
    qc = isa.copy()
    creg = ClassicalRegister(n_meas, "meas")
    qc.add_register(creg)
    for j in range(n_meas):
        qc.measure(fil[j], creg[j])
    return qc


def fold_cz(isa: QuantumCircuit, factor: int) -> QuantumCircuit:
    """Local ZNE folding: every cz -> cz^factor (odd factor; cz is self-inverse)."""
    assert factor % 2 == 1
    out = isa.copy_empty_like()
    for ci in isa.data:
        out.append(ci.operation, ci.qubits, ci.clbits)
        if ci.operation.name == "cz":
            for _ in range(factor - 1):
                out.append(ci.operation, ci.qubits, ci.clbits)
    return out


def find_pinned_set(backend) -> list[int]:
    """Best PIN_LEN-qubit linear chain; its qubits are the pinned set.

    A linear chain is still the right pin even for routed topologies: it is the
    lowest-error connected PIN_LEN-subgraph the existing selector can find, and
    pinning the SAME physical qubits across every topology is what makes the
    topology comparison a controlled one rather than a device-quality lottery.
    """
    props = backend.properties()
    edge_err: dict[frozenset, float] = {}
    for a, b in backend.coupling_map.get_edges():
        key = frozenset((a, b))
        if key in edge_err:
            continue
        try:
            edge_err[key] = float(props.gate_error("cz", [a, b]))
        except Exception:  # noqa: BLE001 -- reversed direction
            edge_err[key] = float(props.gate_error("cz", [b, a]))
    nodes = {q for e in edge_err for q in e}
    node_err = {q: float(props.readout_error(q)) for q in nodes}
    chain = best_linear_chain([tuple(e) for e in edge_err], edge_err,
                              node_err, PIN_LEN)
    score_cz = sum(edge_err[frozenset(e)] for e in zip(chain, chain[1:]))
    score_ro = sum(node_err[q] for q in chain)
    print(f"pinned set on {backend.name}: {chain} "
          f"(sum cz err {score_cz:.4f}, sum readout err {score_ro:.4f})")
    return chain


def build_batch(backend, cells, folds=FOLDS, gammas=(GAMMA,),
                profiles=None, wirings=None, pinned=None) -> dict:
    """Build the full batch plan.

    cells:    [(topology, N), ...]                    -- item 1
    folds:    (1, 3, 5, ...)                          -- item 5 + ZNE
    gammas:   (pi/2, ...)                             -- item 7
    profiles: {(topology, N): [profile, ...]}         -- item 2
    wirings:  {(topology, N): [wiring, ...]}          -- item 6
    pinned:   reuse a known pinned set (recovery path); else chosen from calibration

    Deviation and gamma series are cheap only at fold 1; pass per-cell folds by
    calling build_batch twice and concatenating if a cell needs a different set.
    """
    pinned = list(pinned) if pinned is not None else find_pinned_set(backend)
    allowed = set(pinned)
    plan: dict = {"pinned": pinned, "pubs": [], "meta": []}

    for label, prep in (("cal0", False), ("cal1", True)):
        qc = QuantumCircuit(PIN_LEN)
        if prep:
            qc.x(range(PIN_LEN))
        pm = generate_preset_pass_manager(backend=backend, optimization_level=0,
                                          initial_layout=pinned)
        isa = pm.run(qc)
        fil = list(isa.layout.final_index_layout())
        plan["pubs"].append(with_measurement(isa, fil, PIN_LEN))
        plan["meta"].append({"kind": label, "fil": fil})

    profiles = profiles or {}
    wirings = wirings or {}
    for topology, N in cells:
        cell_profiles = profiles.get((topology, N), [["Q"] * N])
        cell_wirings = wirings.get((topology, N), [list(range(N))])
        for gamma in gammas:
            for profile in cell_profiles:
                for wiring in cell_wirings:
                    layout = [pinned[w] for w in wiring]
                    pm = generate_preset_pass_manager(
                        backend=backend, optimization_level=3,
                        initial_layout=layout, seed_transpiler=7)
                    isa_u = pm.run(build_ewl_circuit(N, topology, gamma, profile))
                    fil = list(isa_u.layout.final_index_layout())
                    n_cz = check_isa_on_set(isa_u, allowed, CZ_BUDGET)
                    print(f"  {topology:16s} N={N} g={gamma:.4f} "
                          f"profile={''.join(profile)} wiring={wiring}: "
                          f"cz {n_cz}, depth {isa_u.depth()}")
                    for f in folds:
                        plan["pubs"].append(
                            with_measurement(fold_cz(isa_u, f), fil, N))
                        plan["meta"].append(series_meta(
                            topology=topology, N=N, fold=f, gamma=gamma,
                            profile=profile, wiring=wiring, fil=fil,
                            cz=n_cz * f))
    print(f"batch: {len(plan['pubs'])} pubs")
    return plan


# ── analysis ──────────────────────────────────────────────────────────────────


def analyze_batch(counts_per_pub: list[dict], plan: dict, shots: int) -> dict:
    """counts (one dict per pub, plan order) -> per-series raw/mitigated/ZNE."""
    meta = plan["meta"]
    mats_all = confusion_from_counts(counts_per_pub[0], counts_per_pub[1], PIN_LEN)
    cal_fil = meta[0]["fil"]
    mats_by_phys = {cal_fil[j]: mats_all[j] for j in range(PIN_LEN)}

    grouped: dict[str, list[int]] = {}
    for i, m in enumerate(meta):
        if m["kind"] == "series":
            grouped.setdefault(series_key(m), []).append(i)

    out: dict = {"pinned": plan["pinned"], "shots": shots, "series": {}}
    for key, idxs in grouped.items():
        first = meta[idxs[0]]
        N = first["N"]
        # analytic noiseless all-Hawk payoff (V-C)/N = 1/N at V=4, C=3
        classical = 1.0 / N
        mats = [mats_by_phys[first["fil"][j]] for j in range(N)]
        folds_out: dict[str, dict] = {}
        fold_values, mit_payoffs, mit_sigmas = [], [], []
        for i in sorted(idxs, key=lambda i: meta[i]["fold"]):
            f = meta[i]["fold"]
            p_raw = counts_to_probs(counts_per_pub[i], N)
            p_mit = mitigate_probs(p_raw, mats)
            s_raw = payoff_stats(p_raw, N, shots)
            s_mit = payoff_stats(p_mit, N, shots)
            folds_out[str(f)] = {
                "counts": counts_per_pub[i],
                "cz": meta[i]["cz"],
                "raw": {**s_raw, "advantage": s_raw["mean"] - classical},
                "mitigated": {**s_mit, "advantage": s_mit["mean"] - classical},
            }
            fold_values.append(f)
            mit_payoffs.append(s_mit["mean"])
            mit_sigmas.append(max(s_mit["sigma"], 1e-9))
        entry = {"topology": first["topology"], "N": N, "gamma": first["gamma"],
                 "profile": first["profile"], "wiring": first["wiring"],
                 "fil": first["fil"], "classical_ne_payoff": classical,
                 "ideal_cooperative_payoff": 4.0 / N,
                 "folds": folds_out}
        if len(fold_values) >= 2:
            zne = zne_extrapolate(fold_values, mit_payoffs, mit_sigmas)
            zne["advantage"] = zne["linear"] - classical
            entry["zne"] = zne
        out["series"][key] = entry
    return out


def print_summary(analysis: dict) -> None:
    print("\n  topology         N  profile  wiring   raw adv  mitig adv   ZNE adv  "
          "P(0..0)  worst player")
    for key in sorted(analysis["series"]):
        s = analysis["series"][key]
        f1 = s["folds"].get("1")
        if f1 is None:
            continue
        zne = f"{s['zne']['advantage']:9.4f}" if "zne" in s else "       --"
        worst = min(f1["mitigated"]["per_player"])
        print(f"  {s['topology']:16s} {s['N']}  {''.join(s['profile']):7s} "
              f"{'-'.join(map(str, s['wiring'])):8s} "
              f"{f1['raw']['advantage']:8.4f} {f1['mitigated']['advantage']:10.4f} "
              f"{zne} {f1['raw']['p_ground']:8.4f} {worst:13.4f}")


# ── transpile feasibility report (no job, no quota) ───────────────────────────


def report(backend) -> None:
    """Routed cz count + depth per (topology, N) on the REAL coupling map.

    Pre-routing gate counts badly understate the cost on ibm_fez: it is
    heavy-hex, so max degree is 3 and the girth is 12. There is no native
    triangle (fully-connected needs SWAPs at every N) and no native cycle below
    N=12 (ring needs SWAPs at every N we run); star is native only up to a
    degree-3 hub. Only GHZ is free on this device. This report is the only
    honest source for which cells are worth quota.
    """
    pinned = find_pinned_set(backend)
    print(f"\n{'topology':16s} {'N':>2s} {'cz':>5s} {'depth':>6s}  note")
    for topology in GATE_CIRCUITS:
        for N in REPORT_NS:
            qc = build_ewl_circuit(N, topology, GAMMA)
            pm = generate_preset_pass_manager(
                backend=backend, optimization_level=3,
                initial_layout=pinned[:N], seed_transpiler=7)
            try:
                isa = pm.run(qc)
            except Exception as exc:  # noqa: BLE001
                print(f"{topology:16s} {N:2d} {'--':>5s} {'--':>6s}  "
                      f"TRANSPILE FAILED: {exc}")
                continue
            n_cz = isa.count_ops().get("cz", 0)
            escaped = not set(isa.layout.final_index_layout()) <= set(pinned)
            if escaped:
                note = "LAYOUT ESCAPED the pinned set -- not runnable as pinned"
            elif n_cz > CZ_BUDGET:
                note = f"over cz budget {CZ_BUDGET} -- excluded"
            elif n_cz > 40:
                note = "EXPENSIVE -- justify before submitting"
            else:
                note = "ok"
            print(f"{topology:16s} {N:2d} {n_cz:5d} {isa.depth():6d}  {note}")
    print("\nreference: the committed N=3 GHZ validation ran at 6 cz and kept "
          "95.5% of shots in |000> (results/hardware-n3/2026-07-16T013912Z).")


# ── backend plumbing ──────────────────────────────────────────────────────────


def load_service():
    """Saved-account / env-token QiskitRuntimeService (same logic as Month 5)."""
    from qiskit_ibm_runtime import QiskitRuntimeService

    token = os.environ.get("QISKIT_IBM_TOKEN")
    channel = os.environ.get("QISKIT_IBM_CHANNEL", "ibm_cloud")
    instance = os.environ.get("QISKIT_IBM_INSTANCE")
    try:
        if token:
            kwargs = {"channel": channel, "token": token}
            if instance:
                kwargs["instance"] = instance
            return QiskitRuntimeService(**kwargs)
        return QiskitRuntimeService()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: could not initialise QiskitRuntimeService: {exc}")
        sys.exit(2)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", default=DEFAULT_BACKEND)
    ap.add_argument("--shots", type=int, default=DEFAULT_SHOTS)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    if not args.report:
        print("(no mode selected; use --report. --rehearse/--hardware/--from-job "
              "land in the next task, once the report has chosen the cells.)")
        return

    service = load_service()
    report(service.backend(args.backend))


if __name__ == "__main__":
    main()
