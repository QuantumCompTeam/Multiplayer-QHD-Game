"""N-scaling hardware pipeline (Month 5->6): N=3,4,5 GHZ EWL on one pinned chain.

Design: docs/superpowers/specs/2026-07-16-hardware-scaling-mitigation-design.md

Modes (default = offline gates only):

  (default)      Gates only, no network: per-N circuit-identity assertion vs the
                 dense J†·(U⊗…⊗U)·J reference AND a noiseless Aer dry-run that
                 must reproduce compute_advantage(N) exactly.
  --rehearse     Full dress rehearsal on AerSimulator with the DEVICE noise model
                 (NoiseModel.from_backend, reduced to the pinned chain): builds
                 the exact 11-pub batch, simulates it, runs the complete
                 mitigation + ZNE analysis, and checks ZNE beats raw. Network is
                 needed only to read backend calibration — no job is submitted.
  --report       Transpile report: chosen chain, per-N cz counts per fold, and a
                 QPU-seconds estimate from the previous job's metrics.
  --hardware     Rehearse (mandatory gate), then submit the batch as ONE
                 SamplerV2 job (11 pubs x shots), persist the job id BEFORE
                 polling, then analyze + save.
  --from-job ID  Recover a submitted batch job (plan is reconstructed from the
                 job's own circuits, so recovery is immune to calibration drift)
                 and analyze + save.

Batch layout (one job): pubs = [cal0 |00000>, cal1 |11111>] +
[N in {3,4,5} x cz-fold in {1,3,5}]. All Ns run on prefixes of ONE 5-qubit
linear chain (controlled variable across the scaling curve).

  --ns 3,4,5,6,7 --chain-len 7   Extend the scaling curve (item 4). DEFAULTS
                 REPRODUCE THE REGISTERED BATCH EXACTLY: --ns defaults to 3,4,5
                 and --chain-len to 5, and the default offline-gate output is
                 verified byte-identical to the pre-flag script. Omitting
                 --chain-len alongside --ns raises it to max(ns) automatically.

IMPORTANT for recovery: plan_from_job_circuits rebuilds the pub ORDER from `ns`,
so recovering runs 1-3 requires the default --ns 3,4,5. A job submitted with a
different --ns must be recovered with that same --ns, or the pub count check
fails loudly rather than mislabelling the series. N=3 must always be present:
it is the p_eff fit anchor the frozen preregistration is built on.

Honesty notes carried into every saved result:
- "advantage" = measured (Q,…,Q) cooperative-profile payoff minus the ANALYTIC
  noiseless classical NE payoff (1/3, 1/4, 1/5 at N=3,4,5).
- (Q,…,Q) is a pure NE only at N=3; at N=4,5 a unilateral Hawk deviation beats
  it in the noiseless game (Month-3 finding). The hardware curve measures the
  cooperative profile, not an equilibrium claim at N=4,5.
"""

import argparse
import json
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
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel

from config import GAMMA
from circuits.ewl import U, q_strategy
from circuits.gate_level import ghz_gate_circuit
from circuits.topologies import ghz_entangler
from game.nash import compute_advantage
from game.payoffs import expected_payoff
from hardware.chain import best_linear_chain
from hardware.mitigation import (
    confusion_from_counts,
    counts_to_probs,
    mitigate_probs,
    zne_extrapolate,
)

NS = (3, 4, 5)
FOLDS = (1, 3, 5)
DEFAULT_SHOTS = 4096
CHAIN_LEN = 5
DEFAULT_BACKEND = "ibm_fez"  # same device as the Month-5 N=3 run
PREV_JOB_ID = "d9br6l66hjac73fg3g7g"  # Month-5 N=3 job, used for QPU estimates


# ── circuit construction + offline gates ───────────────────────────────────────


def build_ewl_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit:
    """J · U(q_strategy(N))^⊗N · J† with J = ghz_gate_circuit (CX-ladder form).

    Uses the src gate-level entangler (validated against the dense matrix in
    tests/test_gate_level.py, incl. N=5,6) — NOT the retired N=3-only prototype
    in experiments/hand_built_j.py.
    """
    J = ghz_gate_circuit(N, gamma)
    qc = QuantumCircuit(N)
    qc.compose(J, inplace=True)
    for q in range(N):
        qc.append(UnitaryGate(U(*q_strategy(N)), label="U"), [q])
    qc.compose(J.inverse(), inplace=True)
    return qc


def assert_circuit_identity(qc: QuantumCircuit, N: int) -> None:
    """Gate 1: the built circuit IS the validated Q_N unitary (dense reference)."""
    Uq = U(*q_strategy(N))
    U_layer = Uq
    for _ in range(N - 1):
        U_layer = np.kron(U_layer, Uq)
    J = ghz_entangler(N, GAMMA)
    reference = Operator(J.conj().T @ U_layer @ J)
    if not Operator(qc).equiv(reference):
        print(f"DISCREPANCY: N={N} circuit is NOT the validated Q_{N} unitary.")
        sys.exit(1)
    print(f"  N={N}: circuit-identity assertion PASSED (Operator.equiv).")


def _onehot(i: int, N: int) -> np.ndarray:
    v = np.zeros(2**N)
    v[i] = 1.0
    return v


def payoff_stats(probs: np.ndarray, N: int, shots: int) -> dict:
    """Mean (Q,…,Q)-profile payoff + multinomial shot-noise sigma of the mean."""
    per_player = expected_payoff(probs, N)
    mean = float(np.mean(per_player))
    # coefficient of basis state i in the mean-payoff estimator
    cbar = np.array(
        [float(np.mean(expected_payoff(_onehot(i, N), N))) for i in range(2**N)]
    )
    var = float(np.sum(probs * cbar**2) - mean**2)
    sigma = float(np.sqrt(max(var, 0.0) / shots))
    return {
        "per_player": [float(x) for x in per_player],
        "mean": mean,
        "sigma": sigma,
        "p_ground": float(probs[0]),
    }


def run_noiseless_gates(shots: int, ns=NS) -> dict[int, dict]:
    """Gates 1+2 for every N. Returns per-N references from compute_advantage."""
    print("=== offline gates (no network) ===")
    refs: dict[int, dict] = {}
    sim = AerSimulator()
    for N in ns:
        qc = build_ewl_gate_circuit(N)
        assert_circuit_identity(qc, N)
        ref = compute_advantage(N=N)
        refs[N] = ref
        qm = qc.copy()
        qm.measure_all()
        pm = generate_preset_pass_manager(backend=sim, optimization_level=3)
        counts = sim.run(pm.run(qm), shots=shots).result().get_counts()
        probs = counts_to_probs(counts, N)
        stats = payoff_stats(probs, N, shots)
        adv = stats["mean"] - ref["classical_ne_payoff"]
        ok = abs(adv - ref["advantage"]) < 1e-6
        print(
            f"  N={N}: noiseless dry-run advantage {adv:.6f} "
            f"(ref {ref['advantage']:.6f}, classical NE "
            f"{ref['classical_ne_payoff']:.6f}, q_is_nash={ref['q_is_nash']}) "
            f"{'PASS' if ok else 'FAIL'}"
        )
        if not ok:
            sys.exit(1)
    print("  all gates PASSED.")
    return refs


# ── backend plumbing ───────────────────────────────────────────────────────────


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


def find_chain(backend, chain_len=CHAIN_LEN) -> list[int]:
    """Best 5-qubit linear chain by summed cz + readout calibration error."""
    props = backend.properties()
    edges = list(backend.coupling_map.get_edges())
    edge_err: dict[frozenset, float] = {}
    for a, b in edges:
        key = frozenset((a, b))
        if key in edge_err:
            continue
        try:
            edge_err[key] = float(props.gate_error("cz", [a, b]))
        except Exception:  # noqa: BLE001 -- reversed direction
            edge_err[key] = float(props.gate_error("cz", [b, a]))
    nodes = {q for e in edge_err for q in e}
    node_err = {q: float(props.readout_error(q)) for q in nodes}
    chain = best_linear_chain(
        [tuple(e) for e in edge_err], edge_err, node_err, chain_len
    )
    score_cz = sum(edge_err[frozenset(e)] for e in zip(chain, chain[1:]))
    score_ro = sum(node_err[q] for q in chain)
    print(
        f"pinned chain on {backend.name}: {chain} "
        f"(sum cz err {score_cz:.4f}, sum readout err {score_ro:.4f})"
    )
    return chain


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


def check_isa(isa: QuantumCircuit, chain: list[int], N: int) -> int:
    """Safety: all 2q gates are cz on adjacent chain pairs; count is sane."""
    chain_pairs = {frozenset(p) for p in zip(chain, chain[1:])}
    n_cz = 0
    for ci in isa.data:
        if ci.operation.num_qubits == 2:
            if ci.operation.name != "cz":
                print(f"UNEXPECTED 2q gate {ci.operation.name}")
                sys.exit(1)
            pair = frozenset(isa.find_bit(q).index for q in ci.qubits)
            if pair not in chain_pairs:
                print(f"cz off the pinned chain: {sorted(pair)}")
                sys.exit(1)
            n_cz += 1
    limit = 4 * (N - 1) + 2
    if n_cz > limit:
        print(f"cz count {n_cz} exceeds sanity limit {limit} (routing?)")
        sys.exit(1)
    return n_cz


def build_batch(backend, ns=NS, chain_len=CHAIN_LEN) -> dict:
    """Build the full 11-pub batch plan against a real backend.

    Returns {"chain", "pubs", "meta"}; meta[i] describes pubs[i]:
    cals: {"kind": "cal0"/"cal1", "fil": [5 phys qubits]}
    series: {"kind": "series", "N", "fold", "fil", "cz"}.
    """
    chain = find_chain(backend, chain_len)
    plan: dict = {"chain": chain, "pubs": [], "meta": []}

    # readout calibration pubs (opt level 0 so the X layer survives verbatim)
    for label, prep in (("cal0", False), ("cal1", True)):
        qc = QuantumCircuit(chain_len)
        if prep:
            qc.x(range(chain_len))
        pm = generate_preset_pass_manager(
            backend=backend, optimization_level=0, initial_layout=chain
        )
        isa = pm.run(qc)
        fil = list(isa.layout.final_index_layout())
        plan["pubs"].append(with_measurement(isa, fil, chain_len))
        plan["meta"].append({"kind": label, "fil": fil})

    for N in ns:
        pm = generate_preset_pass_manager(
            backend=backend, optimization_level=3, initial_layout=chain[:N]
        )
        isa_u = pm.run(build_ewl_gate_circuit(N))
        fil = list(isa_u.layout.final_index_layout())
        if not set(fil) <= set(chain):
            print(f"N={N}: layout escaped the chain: {fil}")
            sys.exit(1)
        n_cz = check_isa(isa_u, chain, N)
        print(f"  N={N}: transpiled to {backend.name}: depth {isa_u.depth()}, "
              f"cz {n_cz}, layout {fil}")
        for f in FOLDS:
            folded = fold_cz(isa_u, f)
            plan["pubs"].append(with_measurement(folded, fil, N))
            plan["meta"].append({"kind": "series", "N": N, "fold": f,
                                 "fil": fil, "cz": n_cz * f})
    return plan


def plan_from_job_circuits(circuits: list[QuantumCircuit], ns=NS) -> dict:
    """Reconstruct the batch plan from a job's own submitted circuits.

    fil is read off each pub's measure instructions (physical qubit measured
    into clbit j), so recovery does not depend on current calibration or on
    QPY layout metadata. Pub order is the deterministic build_batch order.
    """
    metas = [{"kind": "cal0"}, {"kind": "cal1"}]
    for N in ns:
        for f in FOLDS:
            metas.append({"kind": "series", "N": N, "fold": f})
    if len(circuits) != len(metas):
        print(f"job has {len(circuits)} pubs; expected {len(metas)}")
        sys.exit(1)
    for qc, m in zip(circuits, metas):
        fil_map: dict[int, int] = {}
        n_cz = 0
        for ci in qc.data:
            if ci.operation.name == "measure":
                clidx = qc.find_bit(ci.clbits[0]).index
                fil_map[clidx] = qc.find_bit(ci.qubits[0]).index
            elif ci.operation.name == "cz":
                n_cz += 1
        m["fil"] = [fil_map[j] for j in range(len(fil_map))]
        if m["kind"] == "series":
            m["cz"] = n_cz
    chain = metas[0]["fil"]
    return {"chain": chain, "pubs": circuits, "meta": metas}


# ── reduction to the active qubits (exact local simulation of the ISA) ─────────


def reduce_isa(isa: QuantumCircuit, active: list[int]) -> QuantumCircuit:
    """Rebuild an ISA circuit on len(active) qubits (local j = physical active[j])."""
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

    Uses the NATIVE to_dict form (numpy complex arrays): serializable=True
    encodes Kraus matrices as [re, im] pairs that from_dict cannot decode in
    aer 0.14.
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


# ── predictions (computed without reference to the N=4/5 counts being predicted) ──


def device_predictions(plan: dict, backend, refs: dict,
                       shots: int = 200_000, ns=NS) -> dict:
    """Per-N predicted payoff/advantage from the device noise model.

    'raw' = sampled with readout error; 'noro' = exact pre-measurement
    probabilities (what ideal readout mitigation would recover).
    """
    nm_full = NoiseModel.from_backend(backend)
    out: dict = {"model_built_utc": datetime.now(timezone.utc).isoformat(),
                 "backend": backend.name}
    for N in ns:
        meta_idx = next(i for i, m in enumerate(plan["meta"])
                        if m.get("N") == N and m.get("fold") == 1)
        pub = plan["pubs"][meta_idx]
        fil = plan["meta"][meta_idx]["fil"]
        small_nm = reduce_noise_model(nm_full, fil)
        small_meas = reduce_isa(pub, fil)
        sim = AerSimulator(method="density_matrix", noise_model=small_nm)
        counts = sim.run(small_meas, shots=shots).result().get_counts()
        p_raw = counts_to_probs(counts, N)
        small_u = strip_measures(small_meas)
        small_u.save_probabilities()
        probs = sim.run(small_u).result().data(0)["probabilities"]
        p_noro = np.asarray(probs, dtype=np.float64)
        p_noro = p_noro / p_noro.sum()  # density-matrix trace drift ~1e-9 under
        # noise trips expected_payoff's strict normalisation check
        classical = refs[N]["classical_ne_payoff"]
        s_raw = payoff_stats(p_raw, N, shots)
        s_noro = payoff_stats(p_noro, N, shots)
        out[str(N)] = {
            "raw": {"payoff": s_raw["mean"], "advantage": s_raw["mean"] - classical,
                    "p_ground": s_raw["p_ground"]},
            "noro": {"payoff": s_noro["mean"],
                     "advantage": s_noro["mean"] - classical,
                     "p_ground": s_noro["p_ground"]},
        }
    return out


def effective_p_prediction(measured_n3_payoff: float, refs: dict, ns=NS) -> dict:
    """Fit ONE depolarizing p to the N=3 mitigated payoff; predict N=4,5.

    Uses the repo's Month-4 noisy path (circuits.noise.build_ewl_circuit_noisy,
    GHZ topology, {u,cx} basis). Fit-one-predict-two: no N=4/5 information used.
    """
    from circuits.noise import build_ewl_circuit_noisy

    def q_payoff(N: int, p: float) -> float:
        probs = build_ewl_circuit_noisy(N, [q_strategy(N)] * N, topology="ghz", p=p)
        return float(np.mean(expected_payoff(probs, N)))

    lo, hi = 0.0, 0.10
    if q_payoff(3, lo) < measured_n3_payoff:
        p_eff = 0.0
    else:
        for _ in range(40):
            mid = (lo + hi) / 2
            if q_payoff(3, mid) > measured_n3_payoff:
                lo = mid
            else:
                hi = mid
        p_eff = (lo + hi) / 2
    out: dict = {"p_eff": p_eff, "fit_on": "N=3 mitigated fold-1 payoff"}
    for N in ns:
        pay = q_payoff(N, p_eff)
        out[str(N)] = {"payoff": pay,
                       "advantage": pay - refs[N]["classical_ne_payoff"]}
    return out


# ── analysis (shared by rehearsal, --hardware and --from-job) ──────────────────


def analyze_batch(counts_per_pub: list[dict], plan: dict, refs: dict,
                  shots: int, ns=NS, chain_len=CHAIN_LEN) -> dict:
    """counts (one dict per pub, plan order) -> per-N raw/mitigated/ZNE results."""
    meta = plan["meta"]
    mats5 = confusion_from_counts(counts_per_pub[0], counts_per_pub[1], chain_len)
    cal_fil = meta[0]["fil"]  # clbit j of the cal pubs measures physical cal_fil[j]
    mats_by_phys = {cal_fil[j]: mats5[j] for j in range(chain_len)}

    result: dict = {"chain": plan["chain"], "shots": shots, "series": {}}
    for N in ns:
        classical = refs[N]["classical_ne_payoff"]
        fil = next(m["fil"] for m in meta if m.get("N") == N)
        mats = [mats_by_phys[fil[j]] for j in range(N)]
        folds_out = {}
        mit_payoffs, mit_sigmas = [], []
        for f in FOLDS:
            idx = next(i for i, m in enumerate(meta)
                       if m.get("N") == N and m.get("fold") == f)
            p_raw = counts_to_probs(counts_per_pub[idx], N)
            p_mit = mitigate_probs(p_raw, mats)
            s_raw = payoff_stats(p_raw, N, shots)
            s_mit = payoff_stats(p_mit, N, shots)  # sigma: shot-noise approx
            folds_out[str(f)] = {
                "counts": counts_per_pub[idx],
                "raw": {**s_raw, "advantage": s_raw["mean"] - classical},
                "mitigated": {**s_mit, "advantage": s_mit["mean"] - classical},
            }
            mit_payoffs.append(s_mit["mean"])
            mit_sigmas.append(max(s_mit["sigma"], 1e-9))
        zne = zne_extrapolate(list(FOLDS), mit_payoffs, mit_sigmas)
        zne["advantage"] = zne["linear"] - classical
        zne["advantage_richardson"] = zne["richardson"] - classical
        result["series"][str(N)] = {
            "fil": fil,
            "ideal_payoff": refs[N]["q_payoff_per_player"],
            "classical_ne_payoff": classical,
            "ideal_advantage": refs[N]["advantage"],
            "q_is_nash_noiseless": refs[N]["q_is_nash"],
            "folds": folds_out,
            "zne": zne,
        }
    result["confusion_matrices"] = {
        str(cal_fil[j]): mats5[j].tolist() for j in range(chain_len)
    }
    return result


def print_summary(analysis: dict, ns=NS) -> None:
    print("\n  N | ideal adv | raw adv  | mitigated | ZNE(lin)  | P(0..0) raw")
    print("  --+-----------+----------+-----------+-----------+------------")
    for N in ns:
        s = analysis["series"][str(N)]
        f1 = s["folds"]["1"]
        print(f"  {N} | {s['ideal_advantage']:9.4f} "
              f"| {f1['raw']['advantage']:8.4f} "
              f"| {f1['mitigated']['advantage']:9.4f} "
              f"| {s['zne']['advantage']:9.4f} "
              f"| {f1['raw']['p_ground']:.4f}")


# ── dress rehearsal (spec D6) ───────────────────────────────────────────────────


def rehearse(backend, shots: int, refs: dict, ns=NS, chain_len=CHAIN_LEN) -> dict:
    """Simulate the ENTIRE batch + analysis on the device noise model. Returns
    the plan (reused for submission) after the ZNE-improves gate passes."""
    print("\n=== dress rehearsal on AerSimulator(device noise model) ===")
    plan = build_batch(backend, ns, chain_len)
    nm_full = NoiseModel.from_backend(backend)

    counts_per_pub = []
    for pub, m in zip(plan["pubs"], plan["meta"]):
        fil = m["fil"]
        small = reduce_isa(pub, fil)
        # noiseless remap check: EVERY pub is single-outcome without noise
        # (cz^k = cz for odd k, and the ideal circuit maps |0..0> to one state)
        ideal_counts = AerSimulator().run(small, shots=64).result().get_counts()
        if len(ideal_counts) != 1:
            print(f"reduce_isa remap check FAILED for {m}: {ideal_counts}")
            sys.exit(1)
        small_nm = reduce_noise_model(nm_full, fil)
        sim = AerSimulator(method="density_matrix", noise_model=small_nm)
        counts_per_pub.append(sim.run(small, shots=shots).result().get_counts())

    analysis = analyze_batch(counts_per_pub, plan, refs, shots, ns, chain_len)
    print_summary(analysis, ns)

    improved = 0
    for N in ns:
        s = analysis["series"][str(N)]
        ideal = s["ideal_payoff"]
        raw = s["folds"]["1"]["raw"]["mean"]
        zne = s["zne"]["linear"]
        better = abs(zne - ideal) < abs(raw - ideal)
        improved += better
        print(f"  N={N}: |raw-ideal|={abs(raw - ideal):.4f}  "
              f"|ZNE-ideal|={abs(zne - ideal):.4f}  "
              f"{'improved' if better else 'NOT improved'}")
    ok = improved >= 2
    print(f"rehearsal gate: ZNE improved {improved}/3 series -> "
          f"{'PASS' if ok else 'FAIL'}")
    if not ok:
        sys.exit(1)
    return plan


# ── persistence ────────────────────────────────────────────────────────────────


def git_provenance() -> dict:
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
    """Same block preregister_peff.py records (item 16 / G16), plus the runtime
    version (this is the submission path) and the OS (G20: committed artifacts
    have come from interpreters on other operating systems)."""
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


def chain_calibration(backend, chain: list[int]) -> dict:
    props = backend.properties()
    cal = {
        "backend": backend.name,
        "calibration_last_update": str(props.last_update_date),
        "chain": chain,
        "readout_error": {str(q): float(props.readout_error(q)) for q in chain},
        "t1_us": {str(q): float(props.t1(q)) * 1e6 for q in chain},
        "t2_us": {str(q): float(props.t2(q)) * 1e6 for q in chain},
        "cz_error": {},
    }
    for a, b in zip(chain, chain[1:]):
        try:
            cal["cz_error"][f"{a}_{b}"] = float(props.gate_error("cz", [a, b]))
        except Exception:  # noqa: BLE001
            cal["cz_error"][f"{a}_{b}"] = float(props.gate_error("cz", [b, a]))
    return cal


def save_run(analysis: dict, predictions: dict, plan: dict, job_info: dict,
             cal: dict, shots: int, cal_submit: dict | None = None) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results",
                           "hardware-scaling", ts)
    os.makedirs(out_dir, exist_ok=True)
    payload = {
        "experiment": "hardware-scaling-n345",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git": git_provenance(),
        "environment": environment_provenance(),
        "job": job_info,
        "shots": shots,
        "gamma": "pi/2",
        "note": ("advantage = measured cooperative (Q,..,Q) payoff minus the "
                 "ANALYTIC noiseless classical NE payoff; (Q,..,Q) is a pure NE "
                 "only at N=3 (Month-3 finding)."),
        "analysis": analysis,
        "predictions": predictions,
        "pub_meta": [{k: v for k, v in m.items()} for m in plan["meta"]],
    }
    with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    with open(os.path.join(out_dir, "calibration.json"), "w", encoding="utf-8") as fh:
        json.dump(cal, fh, indent=2)
    if cal_submit is not None:
        # G15: calibration.json above is fetched at analysis time; this one was
        # snapshotted at submission and identifies the calibration the cross-day
        # count should use.
        with open(os.path.join(out_dir, "calibration_at_submit.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(cal_submit, fh, indent=2)
    print(f"\nsaved: {os.path.relpath(os.path.join(out_dir, 'result.json'))}")
    return out_dir


def _save_pending_job_id(job_id: str, backend_name: str) -> None:
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results",
                           "hardware-scaling")
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()
    with open(os.path.join(out_dir, "pending_jobs.txt"), "a",
              encoding="utf-8") as fh:
        fh.write(f"{stamp}\t{backend_name}\t{job_id}\n")


def _submit_cal_path(job_id: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", "results",
                        "hardware-scaling",
                        f"pending-{job_id}-calibration.json")


def analyze_and_save(counts_per_pub: list[dict], plan: dict, refs: dict,
                     backend, job_info: dict, shots: int, ns=NS) -> None:
    analysis = analyze_batch(counts_per_pub, plan, refs, shots, ns, len(plan["chain"]))
    print_summary(analysis, ns)
    if 3 not in ns:
        # The fit-one-predict-many protocol is anchored on N=3 by the frozen
        # registration; without it there is nothing to fit.
        print("ERROR: --ns must include 3 (the p_eff fit anchor)")
        sys.exit(1)
    predictions = {
        "device_model": device_predictions(plan, backend, refs, ns=ns),
        "effective_p": effective_p_prediction(
            analysis["series"]["3"]["folds"]["1"]["mitigated"]["mean"], refs, ns),
    }
    others = ", ".join(
        f"N={N}: {predictions['effective_p'][str(N)]['advantage']:.4f}"
        for N in ns if N != 3)
    print(f"  effective p fitted at N=3: {predictions['effective_p']['p_eff']:.5f}"
          f" -> predicted mitigated advantage {others}")
    cal = chain_calibration(backend, plan["chain"])
    cal_submit = None
    sub_path = _submit_cal_path(job_info.get("job_id", ""))
    if job_info.get("job_id") and os.path.exists(sub_path):
        with open(sub_path, encoding="utf-8") as fh:
            cal_submit = json.load(fh)
    save_run(analysis, predictions, plan, job_info, cal, shots,
             cal_submit=cal_submit)


# ── main ───────────────────────────────────────────────────────────────────────


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", default=DEFAULT_BACKEND)
    ap.add_argument("--shots", type=int, default=DEFAULT_SHOTS)
    ap.add_argument("--rehearse", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--hardware", action="store_true",
                    help="rehearse, then submit the batch (spends quota)")
    ap.add_argument("--from-job", default=None, metavar="JOB_ID",
                    help="recover a submitted batch job and analyze it")
    ap.add_argument("--ns", default=None, metavar="3,4,5",
                    help="player counts to run (default 3,4,5 = the registered "
                         "batch). Recovering runs 1-3 needs the default.")
    ap.add_argument("--chain-len", type=int, default=None, metavar="L",
                    help=f"pinned chain length (default {CHAIN_LEN}); must be "
                         f">= max(--ns)")
    args = ap.parse_args()

    ns = NS if args.ns is None else tuple(
        int(x) for x in args.ns.replace(" ", "").split(",") if x)
    chain_len = CHAIN_LEN if args.chain_len is None else args.chain_len
    if args.ns is not None and args.chain_len is None:
        chain_len = max(CHAIN_LEN, max(ns))
    if chain_len < max(ns):
        print(f"ERROR: --chain-len {chain_len} is shorter than max(--ns) "
              f"{max(ns)}; every N runs on a prefix of the one pinned chain.")
        sys.exit(2)

    refs = run_noiseless_gates(args.shots, ns)

    if not (args.rehearse or args.report or args.hardware or args.from_job):
        print("(offline gates only; use --rehearse / --report / --hardware "
              "/ --from-job)")
        return

    service = load_service()
    backend = service.backend(args.backend)

    if args.from_job:
        job = service.job(args.from_job)
        print(f"job {args.from_job} status: {job.status()}")
        if str(job.status()) not in ("DONE", "JobStatus.DONE"):
            print("not finished; re-run later (the job id stays valid).")
            return
        pubs_in = job.inputs["pubs"]
        circuits = [p[0] if isinstance(p, (list, tuple)) else p for p in pubs_in]
        plan = plan_from_job_circuits(circuits, ns)
        result = job.result()
        counts_per_pub = [r.data.meas.get_counts() for r in result]
        shots = sum(counts_per_pub[0].values())
        analyze_and_save(counts_per_pub, plan, refs, backend,
                         {"job_id": args.from_job, "backend": backend.name,
                          "recovered": True}, shots, ns)
        return

    if args.hardware:
        # mandatory pre-submit gate
        plan = rehearse(backend, args.shots, refs, ns, chain_len)
    elif args.rehearse:
        rehearse(backend, args.shots, refs, ns, chain_len)
        return
    else:  # --report only
        plan = build_batch(backend, ns, chain_len)

    if args.report:
        print("\n=== transpile report (no submission) ===")
        for m in plan["meta"]:
            if m["kind"] == "series":
                print(f"  N={m['N']} fold={m['fold']}: cz={m['cz']}  "
                      f"fil={m['fil']}")
        try:
            prev = service.job(PREV_JOB_ID)
            usage = prev.metrics().get("usage", {})
            print(f"  previous 1-pub job usage: {usage}")
            qs = usage.get("quantum_seconds")
            if qs:
                n_pubs = len(plan["pubs"])
                print(f"  batch estimate ~ {qs:.1f} s x {n_pubs} pubs x 1.5 "
                      f"safety = {qs * n_pubs * 1.5:.0f} s QPU")
        except Exception as exc:  # noqa: BLE001
            print(f"  (previous-job metrics unavailable: {exc})")
        if not args.hardware:
            return

    if args.hardware:
        from qiskit_ibm_runtime import SamplerV2 as Sampler

        print(f"\n=== HARDWARE SUBMISSION: {len(plan['pubs'])} pubs x "
              f"{args.shots} shots on {backend.name} ===")
        job = Sampler(mode=backend).run(plan["pubs"], shots=args.shots)
        _save_pending_job_id(job.job_id(), backend.name)
        # G15: snapshot calibration NOW; the copy fetched at analysis time may
        # describe a later calibration than the one the job ran under.
        with open(_submit_cal_path(job.job_id()), "w", encoding="utf-8") as fh:
            json.dump(chain_calibration(backend, plan["chain"]), fh, indent=2)
        print(f"submitted job {job.job_id()} -- waiting (recover with: "
              f"python experiments/hardware_scaling.py --from-job "
              f"{job.job_id()})")
        result = job.result()
        counts_per_pub = [r.data.meas.get_counts() for r in result]
        analyze_and_save(counts_per_pub, plan, refs, backend,
                         {"job_id": job.job_id(), "backend": backend.name},
                         args.shots, ns)


if __name__ == "__main__":
    main()
