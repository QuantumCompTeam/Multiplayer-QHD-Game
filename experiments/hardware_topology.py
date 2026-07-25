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
from qiskit.quantum_info import Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel

from game.payoffs import expected_payoff
from hardware.chain import best_linear_chain
from hardware.mitigation import (
    confusion_from_counts,
    counts_to_probs,
    mitigate_probs,
    zne_extrapolate,
)
from hardware.topology_hw import (
    GATE_CIRCUITS,
    assert_circuit_identity,
    build_ewl_circuit,
    check_isa_on_set,
)

GAMMA = math.pi / 2
FOLDS = (1, 3, 5)
DEFAULT_SHOTS = 4096
DEFAULT_BACKEND = "ibm_fez"
PIN_LEN = 5      # width of the pinned qubit set and of the readout-cal circuits
CZ_BUDGET = 60   # per-pub routed cz ceiling; Task 3's report justifies the value
REPORT_NS = (3, 4, 5)

# The batch cell list, decided from the MEASURED routed cz counts in
# docs/findings/2026-07-25-topology-hardware-feasibility.md -- not from
# pre-routing gate counts, which understate heavy-hex routing cost.
# Excluded there with measured numbers: fully-connected N=5 (67 cz), w N=4
# (107 cz), w N=5 (219 cz), all over CZ_BUDGET. w N=3 (42 cz) is the most
# expensive cell kept and is kept deliberately: every other cell is GHZ-class,
# so without it the topology axis compares one entanglement class.
CELLS = [("ghz", 3), ("ghz", 4), ("ghz", 5),
         ("ring", 3), ("ring", 4), ("ring", 5),
         ("star", 3), ("star", 4), ("star", 5),
         ("fully-connected", 3), ("fully-connected", 4),
         ("w", 3)]

# The three extra axes, all at fold 1. Each is a comparison against a twin that
# already exists in the main batch, so all three must ride in the SAME job: the
# pinned set moves between calibration days, which would make a second-batch
# comparison uncontrolled.
#
# item 2 -- unilateral Hawk deviations at the one cell where the cooperative
# profile is a genuine restricted-menu pure NE (N=3). Falsifiable claim: every
# deviation gap payoff(QQQ) - payoff(H at position k) is >= 0.
DEVIATION_CELL = ("ghz", 3)
DEVIATION_PROFILES = [["H", "Q", "Q"], ["Q", "H", "Q"], ["Q", "Q", "H"]]

# item 6 -- wiring permutations on the cell whose noiseless per-player payoffs
# are already maximally unequal (star N=4 pays mean 1.0, worst player 0.25).
# If the unfairness is topology-locked it stays put in PLAYER space under both
# permutations; if it is device-locked it follows the physical qubits.
WIRING_CELL = ("star", 4)
WIRING_PERMS = [[1, 2, 3, 0], [3, 2, 1, 0]]

# item 7 -- entanglement-angle sweep on the reference cell, swept in the
# DEVIATION GAP rather than in the cooperative payoff. results/gamma-sweep/N3
# shows the cooperative payoff is 1.333333 at every gamma; what gamma moves is
# q_is_nash. Sweeping all-Q pubs would therefore measure a constant. The gap
# payoff_0(Q,Q,Q) - payoff_0(H,Q,Q) is the quantity that varies, so each gamma
# carries both profiles. Noiseless gaps: -0.7031, +0.0469, +0.2599 at
# 0.30/0.40/0.45 pi -- a SIGN CHANGE bracketed between 0.30pi and 0.40pi.
# gamma = 0.5pi is already covered (all-Q from the main batch, HQQ from item 2).
GAMMA_CELL = ("ghz", 3)
GAMMA_SWEEP = (0.30 * math.pi, 0.40 * math.pi, 0.45 * math.pi)
GAMMA_PROFILES = [["Q", "Q", "Q"], ["H", "Q", "Q"]]


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


# ── the noiseless reference for a series ──────────────────────────────────────


def ideal_probs(topology: str, N: int, gamma: float,
                profile: list[str]) -> np.ndarray:
    """Exact noiseless outcome distribution of one series' logical circuit.

    NOT a single basis state in general. `q_strategy(N)` is derived for the GHZ
    entangler, so only GHZ (plus, coincidentally, ring N=4 and fully-connected
    N=4) concentrates on one outcome; ring N=3/5, star N=3/4/5,
    fully-connected N=3 and W N=3 all spread over 4-16 outcomes noiselessly.
    That spread is the paper's topology claim, not a defect, which is why the
    rehearsal gate below compares against THIS distribution rather than
    assuming the cooperative |0..0>.
    """
    qc = build_ewl_circuit(N, topology, gamma, profile)
    return np.abs(Statevector.from_instruction(qc).data) ** 2


def ideal_payoff_mean(topology: str, N: int, gamma: float,
                      profile: list[str]) -> float:
    """Noiseless mean per-player payoff -- the target ZNE should move toward.

    This equals V/N = 4/N for most cells, but NOT for all: ring N=4 is
    noiselessly deterministic on |1111> (all-Hawk) and pays 1/N, i.e. zero
    advantage on a perfect device. Hardcoding 4/N as the gate's target would
    demand that ZNE move that cell toward a payoff its own circuit never has.
    """
    return float(np.mean(expected_payoff(
        ideal_probs(topology, N, gamma, profile), N)))


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


def validate_pinned_chain(edges, pinned: list[int]) -> None:
    """Raise unless `pinned` is PIN_LEN distinct qubits forming a path IN ORDER.

    The order matters: `pinned[w]` is the physical qubit player-slot w maps to,
    and pinned_calibration reports cz error over zip(pinned, pinned[1:]). A set
    that is connected but listed out of order would silently misdescribe both.
    """
    if len(pinned) != PIN_LEN:
        raise ValueError(f"pinned set has {len(pinned)} qubits but PIN_LEN "
                         f"is {PIN_LEN}")
    if len(set(pinned)) != len(pinned):
        raise ValueError(f"pinned set must be distinct qubits: {pinned}")
    undirected = {frozenset(e) for e in edges}
    for a, b in zip(pinned, pinned[1:]):
        if frozenset((a, b)) not in undirected:
            raise ValueError(f"({a}, {b}) is not an edge of the coupling map; "
                             f"{pinned} is not a connected chain in this order")


def parse_pinned_arg(text: str) -> list[int]:
    """Parse --pinned '20,21,22,23,24'."""
    pinned = [int(x) for x in text.replace(" ", "").split(",") if x]
    if len(pinned) != PIN_LEN:
        raise ValueError(f"--pinned needs exactly PIN_LEN={PIN_LEN} qubits, "
                         f"got {len(pinned)}")
    return pinned


def registered_pinned_set() -> list[int] | None:
    """The pinned set the frozen registration's predictions were computed on.

    None when no registration exists yet (the pre-Task-7 state).
    """
    path = os.path.join(_results_dir(), "preregistration.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return list(json.load(fh)["protocol"]["pinned"])


def resolve_pinned_set(backend, explicit: list[int] | None = None,
                       free: bool = False) -> list[int]:
    """Decide which physical qubits to run on, and say why out loud.

    Precedence: --pinned > the frozen registration > live calibration.

    Defaulting to the REGISTERED set is the fix for what happened to run 1
    (job d9ia1pd0k0jc738jaqgg): ibm_fez recalibrated between registration and
    submission, find_pinned_set re-selected from live calibration, and the
    batch executed on [137,147,146,145,144] while the registered per-cell
    predictions described [20,21,22,23,24]. Those predictions were then
    untestable -- their z-scores conflated device-model error, calibration
    drift and a different qubit set. Holding the qubits fixed also makes the
    Task 9 cross-day repeats controlled, which they otherwise are not.

    `free=True` (--free-pinned) restores live selection deliberately, for a run
    that is not meant to be judged against the registration.
    """
    edges = backend.coupling_map.get_edges()
    if explicit is not None:
        validate_pinned_chain(edges, explicit)
        print(f"pinned set: {explicit} (--pinned, explicit)")
        return explicit

    live = find_pinned_set(backend)
    if free:
        print("pinned set: live calibration (--free-pinned); this run is NOT "
              "comparable to the frozen registration's per-cell predictions.")
        return live

    registered = registered_pinned_set()
    if registered is None:
        print("pinned set: live calibration (no registration exists yet)")
        return live

    validate_pinned_chain(edges, registered)
    if registered == live:
        print(f"pinned set: {registered} (registered; live selection agrees)")
    else:
        print(f"pinned set: {registered} (REGISTERED -- holding it fixed).\n"
              f"  live calibration would have picked {live}. Using the "
              f"registered set so the frozen per-cell predictions stay "
              f"testable; pass --free-pinned to override deliberately.")
    return registered


def build_batch(backend, cells, folds=FOLDS, gammas=(GAMMA,),
                profiles=None, wirings=None, pinned=None,
                include_cal=True) -> dict:
    """Build the full batch plan.

    cells:    [(topology, N), ...]                    -- item 1
    folds:    (1, 3, 5, ...)                          -- item 5 + ZNE
    gammas:   (pi/2, ...)                             -- item 7
    profiles: {(topology, N): [profile, ...]}         -- item 2
    wirings:  {(topology, N): [wiring, ...]}          -- item 6
    pinned:   reuse a known pinned set (recovery path); else chosen from calibration
    include_cal: prepend the two readout-calibration pubs. False when
              concatenating a sub-batch onto one that already carries them.

    Deviation and gamma series are cheap only at fold 1; pass per-cell folds by
    calling build_batch twice and concatenating if a cell needs a different set.
    build_full_batch does exactly that.
    """
    pinned = list(pinned) if pinned is not None else find_pinned_set(backend)
    allowed = set(pinned)
    plan: dict = {"pinned": pinned, "pubs": [], "meta": []}

    for label, prep in (("cal0", False), ("cal1", True)) if include_cal else ():
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
                    logical = build_ewl_circuit(N, topology, gamma, profile)
                    # Gate 1 of 3: the built circuit IS the validated dense
                    # J†(U_1⊗…⊗U_N)J reference. Raises otherwise.
                    assert_circuit_identity(logical, N, topology, gamma, profile)
                    pm = generate_preset_pass_manager(
                        backend=backend, optimization_level=3,
                        initial_layout=layout, seed_transpiler=7)
                    isa_u = pm.run(logical)
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


def build_full_batch(backend, pinned=None, free_pinned=False) -> dict:
    """The submitted batch: the topology ladder plus the three fold-1 axes.

    The topology ladder (CELLS) keeps the full 1/3/5 fold ladder, W N=3
    included, because ZNE needs it. The extra axes get fold 1 only: they ask
    equilibrium, fairness and gamma questions, not extrapolation questions, and
    a fold ladder on each would triple their cost for nothing.

    `pinned=None` resolves through resolve_pinned_set, which defaults to the
    frozen registration's qubits so the batch stays comparable to its own
    predictions. Recovery passes the job's own pinned set explicitly.
    """
    if pinned is None:
        pinned = resolve_pinned_set(backend, free=free_pinned)
    plan = build_batch(backend, CELLS, folds=FOLDS, pinned=pinned)
    pinned = plan["pinned"]

    for label, kwargs in (
        ("item 2 -- unilateral Hawk deviations",
         dict(cells=[DEVIATION_CELL],
              profiles={DEVIATION_CELL: DEVIATION_PROFILES})),
        ("item 6 -- wiring permutations",
         dict(cells=[WIRING_CELL], wirings={WIRING_CELL: WIRING_PERMS})),
        ("item 7 -- gamma sweep of the deviation gap",
         dict(cells=[GAMMA_CELL], gammas=GAMMA_SWEEP,
              profiles={GAMMA_CELL: GAMMA_PROFILES})),
    ):
        print(f"  {label} (fold 1):")
        sub = build_batch(backend, folds=(1,), pinned=pinned,
                          include_cal=False, **kwargs)
        plan["pubs"].extend(sub["pubs"])
        plan["meta"].extend(sub["meta"])

    print(f"full batch: {len(plan['pubs'])} pubs")
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
        # The exact noiseless payoff of THIS cell's own circuit. Distinct from
        # ideal_cooperative_payoff = V/N below, which is what full cooperation
        # would pay: the two differ wherever the all-Q profile does not
        # concentrate on |0..0> (ring N=4 pays 1/N noiselessly, not V/N).
        ideal = ideal_payoff_mean(first["topology"], N, first["gamma"],
                                  first["profile"])
        entry = {"topology": first["topology"], "N": N, "gamma": first["gamma"],
                 "profile": first["profile"], "wiring": first["wiring"],
                 "fil": first["fil"], "classical_ne_payoff": classical,
                 "ideal_payoff": ideal,
                 "ideal_advantage": ideal - classical,
                 "ideal_cooperative_payoff": 4.0 / N,
                 "folds": folds_out}
        if len(fold_values) >= 2:
            zne = zne_extrapolate(fold_values, mit_payoffs, mit_sigmas)
            zne["advantage"] = zne["linear"] - classical
            entry["zne"] = zne
        out["series"][key] = entry
    return out


def print_summary(analysis: dict) -> None:
    print("\n  topology         N  profile  wiring    g/pi  ideal adv   raw adv  "
          "mitig adv   ZNE adv  P(0..0)  worst player")
    for key in sorted(analysis["series"]):
        s = analysis["series"][key]
        f1 = s["folds"].get("1")
        if f1 is None:
            continue
        zne = f"{s['zne']['advantage']:9.4f}" if "zne" in s else "       --"
        worst = min(f1["mitigated"]["per_player"])
        print(f"  {s['topology']:16s} {s['N']}  {''.join(s['profile']):7s} "
              f"{'-'.join(map(str, s['wiring'])):8s} "
              f"{s['gamma'] / math.pi:5.2f} "
              f"{s['ideal_advantage']:10.4f} {f1['raw']['advantage']:9.4f} "
              f"{f1['mitigated']['advantage']:10.4f} "
              f"{zne} {f1['raw']['p_ground']:8.4f} {worst:13.4f}")


# ── transpile feasibility report (no job, no quota) ───────────────────────────


def report(backend, pinned: list[int]) -> None:
    """Routed cz count + depth per (topology, N) on the REAL coupling map.

    Pre-routing gate counts do not price routing on ibm_fez, which is heavy-hex
    (max degree 3, girth 12), so only a measured report can decide the cells.

    What that measurement actually showed, against the expectation: at N<=5 the
    girth argument OVERSTATES the cost. Ring routes to 10/20/28 cz and
    fully-connected to 10/31 at N=3/4 -- the transpiler closes a short cycle
    with a few SWAPs rather than routing a 12-cycle. The real casualty is W
    (42 cz at N=3, 107 and 219 at N=4,5). See
    docs/findings/2026-07-25-topology-hardware-feasibility.md.
    """
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


# ── reduction to the pinned qubits (exact local simulation of the ISA) ────────


def reduce_isa(isa: QuantumCircuit, active: list[int]) -> QuantumCircuit:
    """Rebuild an ISA circuit on len(active) qubits (local j = physical active[j]).

    Ported unchanged from experiments/hardware_scaling.py:342.
    """
    local = {p: j for j, p in enumerate(active)}
    small = QuantumCircuit(len(active))
    for creg in isa.cregs:
        small.add_register(ClassicalRegister(len(creg), creg.name))
    for ci in isa.data:
        phys = [isa.find_bit(q).index for q in ci.qubits]
        if not all(p in local for p in phys):
            print(f"reduce_isa: instruction on non-active qubit {phys}")
            sys.exit(1)
        cl = [isa.find_bit(c).index for c in ci.clbits]
        small.append(ci.operation, [local[p] for p in phys], cl)
    return small


def strip_measures(qc: QuantumCircuit) -> QuantumCircuit:
    """Copy of qc without measure instructions (keeps registers)."""
    out = qc.copy_empty_like()
    for ci in qc.data:
        if ci.operation.name != "measure":
            out.append(ci.operation, ci.qubits, ci.clbits)
    return out


def reduce_noise_model(nm: NoiseModel, active: list[int]) -> NoiseModel:
    """Filter a device NoiseModel to the active qubits, remapped to 0..len-1.

    Ported unchanged from experiments/hardware_scaling.py:367. Uses the NATIVE
    to_dict form (numpy complex arrays): serializable=True encodes Kraus
    matrices as [re, im] pairs that from_dict cannot decode in aer 0.14.
    """
    local = {p: j for j, p in enumerate(active)}
    src = nm.to_dict()
    kept = []
    for err in src["errors"]:
        gqs = err.get("gate_qubits")
        if gqs is None:
            kept.append(err)  # all-qubit default error: applies as-is
            continue
        if all(q in local for tup in gqs for q in tup):
            e2 = dict(err)
            e2["gate_qubits"] = [[local[q] for q in tup] for tup in gqs]
            kept.append(e2)
    return NoiseModel.from_dict({"errors": kept})


# ── dress rehearsal (mandatory pre-submission gate) ───────────────────────────


def _exact_pub_probs(small: QuantumCircuit, qargs: list[int]) -> dict:
    """Exact noiseless outcome distribution of a reduced pub over `qargs`.

    qargs[j] is the local qubit measured into clbit j, and both Qiskit's
    probabilities_dict and get_counts render index 0 as the RIGHTMOST
    character, so the keys line up with the counts the device will return.
    """
    sv = Statevector.from_instruction(strip_measures(small))
    return sv.probabilities_dict(qargs=qargs)


def _tvd(p: dict, q: dict) -> float:
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def rehearse(backend, plan: dict, shots: int, seed: int | None = None) -> dict:
    """Simulate the ENTIRE batch + analysis on the reduced device noise model.

    Mandatory pre-submission gate. Two checks must pass:

      (a) Noiseless dry run, per pub: the reduced, transpiled, FOLDED, measured
          circuit reproduces the logical circuit's exact distribution. This
          replaces the plan's "every pub is single-outcome noiselessly" check,
          which is false for 9 of the 12 cells -- q_strategy(N) is GHZ-derived,
          so only GHZ-class cells concentrate on one basis state (see
          ideal_probs). The distribution check is strictly stronger anyway: it
          validates the layout, the fil->clbit remap AND cz^k = cz for odd k,
          without assuming anything about the topology.

      (b) ZNE moves a strict majority of the all-Q series toward that cell's own
          noiseless payoff. hardware_scaling.py hardcodes >= 2 of 3; here the
          denominator varies with the cell list. A ring or W cell failing to
          improve is expected and is data, not a bug -- a MAJORITY failing means
          the batch is not worth quota.
    """
    print("\n=== dress rehearsal on AerSimulator(device noise model) ===")
    pinned = plan["pinned"]
    nm_small = reduce_noise_model(NoiseModel.from_backend(backend), pinned)
    sim = AerSimulator(method="density_matrix", noise_model=nm_small)

    counts_per_pub = []
    for i, (pub, m) in enumerate(zip(plan["pubs"], plan["meta"])):
        # Reduce onto the whole pinned set, not onto m["fil"]: routing may use a
        # pinned qubit that no virtual qubit ends on, and check_isa_on_set only
        # guarantees the cz gates stayed inside the pinned set.
        small = reduce_isa(pub, pinned)
        qargs = [pinned.index(q) for q in m["fil"]]
        got = _exact_pub_probs(small, qargs)
        if m["kind"] == "series":
            want = {}
            for i, p in enumerate(ideal_probs(m["topology"], m["N"], m["gamma"],
                                              m["profile"])):
                if p > 1e-12:
                    want[format(i, f"0{m['N']}b")] = float(p)
        else:  # cal0 -> |0...0>, cal1 -> |1...1>
            bit = "1" if m["kind"] == "cal1" else "0"
            want = {bit * PIN_LEN: 1.0}
        err = _tvd(got, want)
        if err > 1e-6:
            print(f"noiseless dry run FAILED for {m}: TVD {err:.3e}")
            print(f"  got  {got}")
            print(f"  want {want}")
            sys.exit(1)
        # seed per pub, not per batch: one seed for every pub would correlate
        # their sampling noise and understate the spread.
        kw = {} if seed is None else {"seed_simulator": seed + i}
        counts_per_pub.append(sim.run(small, shots=shots, **kw).result().get_counts())
    print(f"noiseless dry run: {len(plan['pubs'])}/{len(plan['pubs'])} pubs "
          f"reproduce their logical distribution exactly")

    analysis = analyze_batch(counts_per_pub, plan, shots)
    print_summary(analysis)

    coop = [s for s in analysis["series"].values()
            if set(s["profile"]) == {"Q"} and "zne" in s]
    improved = 0
    print("\n  ZNE gate (target = each cell's OWN noiseless payoff):")
    for s in sorted(coop, key=lambda s: (s["topology"], s["N"])):
        ideal = s["ideal_payoff"]
        raw = s["folds"]["1"]["raw"]["mean"]
        zne = s["zne"]["linear"]
        better = abs(zne - ideal) < abs(raw - ideal)
        improved += better
        print(f"    {s['topology']:16s} N={s['N']}: ideal={ideal:.4f} "
              f"|raw-ideal|={abs(raw - ideal):.4f} "
              f"|ZNE-ideal|={abs(zne - ideal):.4f} "
              f"{'improved' if better else 'NOT improved'}")
    ok = improved > len(coop) / 2
    print(f"  rehearsal gate: ZNE improved {improved}/{len(coop)} cooperative "
          f"series -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        sys.exit(1)
    return analysis


# ── persistence ───────────────────────────────────────────────────────────────


def git_provenance() -> dict:
    """Ported unchanged from experiments/hardware_scaling.py:574."""
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                         text=True).strip()
        porcelain = subprocess.check_output(["git", "status", "--porcelain"],
                                            text=True).strip()
        dirty = bool(porcelain)
    except Exception:  # noqa: BLE001
        commit, dirty, porcelain = None, None, ""
    out = {"commit": commit, "dirty": dirty}
    if dirty:
        # G16: "dirty": true alone leaves the code unidentifiable; at least
        # enumerate what was dirty at save time.
        out["dirty_files"] = porcelain.splitlines()
    return out


def environment_provenance() -> dict:
    """Ported unchanged from experiments/hardware_scaling.py:591 (item 16/G16)."""
    env = {
        "python": platform.python_version(),
        "qiskit": __import__("qiskit").__version__,
        "qiskit_aer": __import__("qiskit_aer").__version__,
        "numpy": __import__("numpy").__version__,
        "scipy": __import__("scipy").__version__,
        "platform": platform.platform(),
    }
    try:
        env["qiskit_ibm_runtime"] = __import__("qiskit_ibm_runtime").__version__
    except Exception:  # noqa: BLE001  (absent only on sim-only installs)
        env["qiskit_ibm_runtime"] = None
    return env


def pinned_calibration(backend, pinned: list[int]) -> dict:
    """chain_calibration from hardware_scaling.py:610, over the pinned set.

    The cz_error loop still walks consecutive pairs of `pinned`: the pinned set
    IS a linear chain (find_pinned_set picks one), so those are exactly its
    native edges, and routed topologies use no others -- check_isa_on_set
    enforces that.
    """
    props = backend.properties()
    cal = {
        "backend": backend.name,
        "calibration_last_update": str(props.last_update_date),
        "pinned": pinned,
        "readout_error": {str(q): float(props.readout_error(q)) for q in pinned},
        "t1_us": {str(q): float(props.t1(q)) * 1e6 for q in pinned},
        "t2_us": {str(q): float(props.t2(q)) * 1e6 for q in pinned},
        "cz_error": {},
    }
    for a, b in zip(pinned, pinned[1:]):
        try:
            cal["cz_error"][f"{a}_{b}"] = float(props.gate_error("cz", [a, b]))
        except Exception:  # noqa: BLE001
            cal["cz_error"][f"{a}_{b}"] = float(props.gate_error("cz", [b, a]))
    return cal


def _results_dir() -> str:
    return os.path.join(os.path.dirname(__file__), "..", "results",
                        "hardware-topology")


def _save_pending_job_id(job_id: str, backend_name: str) -> None:
    os.makedirs(_results_dir(), exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()
    with open(os.path.join(_results_dir(), "pending_jobs.txt"), "a",
              encoding="utf-8") as fh:
        fh.write(f"{stamp}\t{backend_name}\t{job_id}\n")


def _submit_cal_path(job_id: str) -> str:
    return os.path.join(_results_dir(), f"pending-{job_id}-calibration.json")


def save_run(analysis: dict, plan: dict, job_info: dict, cal: dict, shots: int,
             cal_submit: dict | None = None) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out_dir = os.path.join(_results_dir(), ts)
    os.makedirs(out_dir, exist_ok=True)
    payload = {
        "experiment": "hardware-topology",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git": git_provenance(),
        "environment": environment_provenance(),
        "job": job_info,
        "shots": shots,
        "note": ("advantage = measured profile payoff minus the ANALYTIC "
                 "noiseless classical NE payoff 1/N. This is the hardware "
                 "convention; simulation figures use the circuit-relative gap "
                 "and the two are NOT comparable. ideal_payoff is this cell's "
                 "own noiseless payoff and is NOT V/N for every topology."),
        "analysis": analysis,
        "pub_meta": plan["meta"],
    }
    with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    with open(os.path.join(out_dir, "calibration.json"), "w",
              encoding="utf-8") as fh:
        json.dump(cal, fh, indent=2)
    if cal_submit is not None:
        # G15: calibration.json above is fetched at analysis time; this one was
        # snapshotted at submission and identifies the calibration the job
        # actually ran under.
        with open(os.path.join(out_dir, "calibration_at_submit.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(cal_submit, fh, indent=2)
    print(f"\nsaved: {os.path.relpath(os.path.join(out_dir, 'result.json'))}")
    return out_dir


def analyze_and_save(counts_per_pub: list[dict], plan: dict, backend,
                     job_info: dict, shots: int) -> None:
    analysis = analyze_batch(counts_per_pub, plan, shots)
    print_summary(analysis)
    cal_submit = None
    sub_path = _submit_cal_path(job_info.get("job_id", ""))
    if job_info.get("job_id") and os.path.exists(sub_path):
        with open(sub_path, encoding="utf-8") as fh:
            cal_submit = json.load(fh)
    save_run(analysis, plan, job_info,
             pinned_calibration(backend, plan["pinned"]), shots,
             cal_submit=cal_submit)


# ── submission and recovery ───────────────────────────────────────────────────


def submit(backend, plan: dict, shots: int) -> str:
    """Submit ONE batch job, persisting the id and calibration BEFORE polling."""
    from qiskit_ibm_runtime import SamplerV2

    cal_submit = pinned_calibration(backend, plan["pinned"])
    print(f"\n=== HARDWARE SUBMISSION: {len(plan['pubs'])} pubs x {shots} shots "
          f"on {backend.name} ===")
    job = SamplerV2(mode=backend).run(plan["pubs"], shots=shots)
    job_id = job.job_id()
    _save_pending_job_id(job_id, backend.name)
    with open(_submit_cal_path(job_id), "w", encoding="utf-8") as fh:
        json.dump(cal_submit, fh, indent=2)
    print(f"submitted job {job_id}; id and submit-time calibration persisted. "
          f"Recover with: --from-job {job_id}")
    return job


def pinned_from_job_pubs(circuits) -> list[int]:
    """Recover the pinned set from the job's OWN cal0 circuit.

    Pub 0 is cal0: transpiled at optimization_level=0 with initial_layout=pinned
    and measured fil[j] -> clbit j, so its measure targets in clbit order ARE
    the pinned set. Reading it from the job rather than from the live backend
    makes recovery immune to the chain selector picking a different set on a
    later calibration day.
    """
    cal0 = circuits[0]
    by_clbit = {cal0.find_bit(ci.clbits[0]).index: cal0.find_bit(ci.qubits[0]).index
                for ci in cal0.data if ci.operation.name == "measure"}
    if sorted(by_clbit) != list(range(PIN_LEN)):
        print(f"cannot read the pinned set from pub 0: measured clbits "
              f"{sorted(by_clbit)}, expected 0..{PIN_LEN - 1}")
        sys.exit(1)
    return [by_clbit[j] for j in range(PIN_LEN)]


def recover(service, backend, job_id: str, shots_hint: int) -> None:
    """Re-analyse a submitted batch, rebuilding the plan on ITS pinned set."""
    job = service.job(job_id)
    print(f"job {job_id} status: {job.status()}")
    if str(job.status()) not in ("DONE", "JobStatus.DONE"):
        print("not finished; re-run later (the job id stays valid).")
        return
    pubs_in = job.inputs["pubs"]
    circuits = [p[0] if isinstance(p, (list, tuple)) else p for p in pubs_in]
    pinned = pinned_from_job_pubs(circuits)
    print(f"recovered pinned set from the job itself: {pinned}")
    plan = build_full_batch(backend, pinned=pinned)
    if len(plan["pubs"]) != len(circuits):
        # Abort rather than guess: a mismatched plan would silently mislabel
        # every series in the saved artifact.
        print(f"ABORT: rebuilt plan has {len(plan['pubs'])} pubs but job "
              f"{job_id} has {len(circuits)}. The cell list changed since "
              f"submission; recover with the code at the submitting commit.")
        sys.exit(1)
    result = job.result()
    counts_per_pub = [r.data.meas.get_counts() for r in result]
    shots = sum(counts_per_pub[0].values()) or shots_hint
    analyze_and_save(counts_per_pub, plan, backend,
                     {"job_id": job_id, "backend": backend.name,
                      "recovered": True}, shots)


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
    ap.add_argument("--report", action="store_true",
                    help="routed cz/depth per cell; network read only, no quota")
    ap.add_argument("--rehearse", action="store_true",
                    help="full dress rehearsal on the device noise model, no job")
    ap.add_argument("--hardware", action="store_true",
                    help="rehearse, then submit the batch (SPENDS QUOTA)")
    ap.add_argument("--from-job", default=None, metavar="JOB_ID",
                    help="recover a submitted batch job and analyse it")
    ap.add_argument("--pinned", default=None, metavar="Q0,Q1,Q2,Q3,Q4",
                    help="run on these physical qubits (overrides everything)")
    ap.add_argument("--free-pinned", action="store_true",
                    help="let live calibration pick the chain instead of "
                         "reusing the registration's; the run is then NOT "
                         "comparable to the frozen per-cell predictions")
    args = ap.parse_args()

    explicit = None
    if args.pinned:
        try:
            explicit = parse_pinned_arg(args.pinned)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            sys.exit(2)
    if explicit is not None and args.free_pinned:
        print("ERROR: --pinned and --free-pinned are mutually exclusive")
        sys.exit(2)

    if not (args.report or args.rehearse or args.hardware or args.from_job):
        print("(no mode selected; use --report / --rehearse / --hardware "
              "/ --from-job)")
        return

    service = load_service()
    backend = service.backend(args.backend)

    if args.report:
        report(backend, resolve_pinned_set(backend, explicit=explicit,
                                           free=args.free_pinned))
        return

    if args.from_job:
        recover(service, backend, args.from_job, args.shots)
        return

    pinned = resolve_pinned_set(backend, explicit=explicit,
                                free=args.free_pinned)
    plan = build_full_batch(backend, pinned=pinned)
    rehearse(backend, plan, args.shots)  # mandatory gate for --hardware too
    if not args.hardware:
        return

    job = submit(backend, plan, args.shots)
    result = job.result()
    counts_per_pub = [r.data.meas.get_counts() for r in result]
    analyze_and_save(counts_per_pub, plan, backend,
                     {"job_id": job.job_id(), "backend": backend.name},
                     args.shots)


if __name__ == "__main__":
    main()
