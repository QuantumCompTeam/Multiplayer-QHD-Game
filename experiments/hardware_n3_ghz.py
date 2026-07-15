"""N=3 GHZ EWL hardware-validation pipeline (Month 5).

Two modes, selected by --hardware:

  (default)     Dry run on a NOISELESS AerSimulator. Reproduces the Month-2
                advantage = 1.0 using the validated src/ circuit construction,
                gated by a circuit-identity assertion that distinguishes the
                real Q_3 circuit from the earlier placeholder. No hardware.

  --hardware    Submit the SAME circuit to a real IBM Quantum backend via
                qiskit-ibm-runtime SamplerV2, read counts, and report the
                measured advantage. On real hardware the advantage decays from
                1.0 toward 0 with device noise -- that decay IS the validation.

The identity assertion AND the Aer dry-run both run before any hardware
submission, so credits are never spent on a wrong circuit or a broken build.

The transpiled depth / 2q-gate print is kept so we can watch how the 8x8 J
entangler synthesizes -- on Aer it stays a native UnitaryGate (see caveat), on
real hardware it decomposes to the backend basis (that is the number that
matters, and the hand-built J keeps it to 6 two-qubit gates).
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

# Windows consoles default to cp1252, which cannot encode the U+2297 (tensor)
# and U+2020 (dagger) glyphs this script prints. Force UTF-8 so a real run does
# not crash on a print AFTER a job has already been submitted.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Add src to the import path the same way scripts/n3_advantage.py does.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from qiskit.quantum_info import Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

from config import GAMMA
from circuits.ewl import U, q_strategy
from circuits.topologies import ghz_entangler
from game.payoffs import expected_payoff, index_to_bitstring
from game.nash import compute_advantage
from hand_built_j import build_ewl_qc_handbuilt  # PROTOTYPE: structure-aware J

N = 3
DEFAULT_SHOTS = 4096


def build_validated_circuit():
    """Build the N=3 GHZ EWL circuit and assert it IS the validated Q_3 unitary.

    J = cos(GAMMA/2) I + i sin(GAMMA/2) X⊗X⊗X via the hand-built structure-aware
    decomposition (6 two-qubit gates on ibm_marrakesh vs 35 for generic QSD);
    per-player Q_3 = U(0, pi/3, pi/3). Returns the measurement-free circuit.

    The circuit-identity assertion is the credit-protection gate: both the
    validated circuit and the old H+CX / qiskit-u placeholder collapse to |000>
    on a noiseless sim, so counts cannot tell them apart. We assert the full 8x8
    unitary instead. The reference is rebuilt from src primitives
    (ghz_entangler, U) as J† · (U⊗U⊗U) · J -- independent of the circuit's
    gate-assembly logic. count_ops() is NOT usable: every gate serializes to the
    generic label 'unitary', so a name-based check cannot see 'J'/'U'.
    Operator.equiv is the strongest and only reliable option.
    """
    qc = build_ewl_qc_handbuilt(N, GAMMA)

    _Uq = U(*q_strategy(N))
    _U_layer = np.kron(np.kron(_Uq, _Uq), _Uq)
    _J = ghz_entangler(N, GAMMA)
    _reference = Operator(_J.conj().T @ _U_layer @ _J)  # order: J, U-layer, J†
    if not Operator(qc).equiv(_reference):
        print("DISCREPANCY: constructed circuit is NOT the validated Q_3 unitary.")
        print("  count_ops:", dict(qc.count_ops()))
        sys.exit(1)
    print("Circuit-identity assertion PASSED (Operator.equiv vs J†·(U⊗U⊗U)·J).")
    return qc


def counts_to_advantage(counts, shots):
    """counts (MSB-left bitstrings) -> measured per-player payoff, advantage.

    compute_advantage is NOT closed-form: it runs the EXACT noiseless
    Statevector sim over all {D,H,Q}^3 profiles then does the Nash game theory.
    classical_ne_payoff (=1/3) and advantage (=1.0) are exact/deterministic and
    independent of any SAMPLING path, so they stay a valid reference baseline;
    the real hardware run is what makes this an independent validation.
    """
    probs = np.zeros(2 ** N, dtype=np.float64)
    for bitstr, c in counts.items():
        probs[int(bitstr, 2)] = c / shots  # MSB-left bitstring -> little-endian index

    measured = expected_payoff(probs, N)
    measured_q = float(np.mean(measured))
    ref = compute_advantage(N=N)
    classical_ne = ref["classical_ne_payoff"]
    measured_advantage = measured_q - classical_ne

    print()
    print("measured (Q,Q,Q) distribution (top 8 by probability):")
    for i in np.argsort(probs)[::-1][:8]:
        if probs[i] > 0:
            print(f"  |{index_to_bitstring(int(i), N)}>  P={probs[i]:.6f}")
    print("measured per-player payoff :", measured)
    print(f"measured (Q,Q,Q) payoff    : {measured_q:.6f}  (ref V/N = {4/3:.6f})")
    print(f"classical NE payoff        : {classical_ne:.6f}  (ref 1/3)")
    print(f"measured advantage         : {measured_advantage:.6f}")
    print(f"reference advantage        : {ref['advantage']:.6f}")
    return probs, measured, measured_q, measured_advantage, ref


def run_dry(qc, shots):
    """Noiseless Aer sampling. Serves as the second gate before hardware."""
    backend = AerSimulator()
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    isa = pm.run(qc)

    from qiskit_ibm_runtime import SamplerV2 as Sampler
    result = Sampler(mode=backend).run([isa], shots=shots).result()
    counts = result[0].data.meas.get_counts()

    print("counts:", counts)
    # CAVEAT: AerSimulator executes arbitrary UnitaryGates natively, so this
    # depth / 2q count does NOT reflect how J decomposes on hardware.
    print("transpiled depth:", isa.depth(), "| 2q gates:", isa.num_nonlocal_gates())
    return counts


def load_service():
    """Load a QiskitRuntimeService from a saved account or env token.

    Precedence: a saved account (QiskitRuntimeService.save_account) is used if
    present; otherwise QISKIT_IBM_TOKEN (+ optional QISKIT_IBM_CHANNEL /
    QISKIT_IBM_INSTANCE) is used. Fail loudly with setup instructions -- we do
    NOT want a cryptic auth error after the user thinks a job is submitting.
    """
    from qiskit_ibm_runtime import QiskitRuntimeService

    token = os.environ.get("QISKIT_IBM_TOKEN")
    # qiskit-ibm-runtime 0.36.1 accepts channels {'ibm_cloud', 'ibm_quantum'}.
    # The current free IBM Quantum Platform is 'ibm_cloud' (needs an instance
    # CRN); the legacy 'ibm_quantum' hub/group/project channel was sunset in 2025.
    channel = os.environ.get("QISKIT_IBM_CHANNEL", "ibm_cloud")
    instance = os.environ.get("QISKIT_IBM_INSTANCE")
    try:
        if token:
            kwargs = {"channel": channel, "token": token}
            if instance:
                kwargs["instance"] = instance
            return QiskitRuntimeService(**kwargs)
        return QiskitRuntimeService()  # saved account
    except Exception as exc:  # noqa: BLE001 -- surface any auth/config failure
        print("ERROR: could not initialise QiskitRuntimeService.")
        print(f"  {type(exc).__name__}: {exc}")
        print()
        print("Set up IBM Quantum access, then re-run with --hardware. Either:")
        print("  1) Save an account once (recommended), in a Python shell:")
        print("       from qiskit_ibm_runtime import QiskitRuntimeService")
        print("       QiskitRuntimeService.save_account(")
        print("           channel='ibm_cloud', token='<YOUR_TOKEN>',")
        print("           instance='<INSTANCE_CRN>', set_as_default=True)")
        print("  2) Or export env vars for this run:")
        print("       export QISKIT_IBM_TOKEN=<YOUR_TOKEN>")
        print("       export QISKIT_IBM_INSTANCE=<instance>   # if your plan needs it")
        sys.exit(2)


def run_hardware(qc, shots, backend_name):
    """Transpile to a real IBM backend and submit via SamplerV2. Returns
    (counts, backend_name, job_id, isa_depth, isa_2q)."""
    from qiskit_ibm_runtime import SamplerV2 as Sampler

    service = load_service()
    if backend_name:
        backend = service.backend(backend_name)
    else:
        backend = service.least_busy(operational=True, simulator=False,
                                     min_num_qubits=N)
    print(f"selected backend: {backend.name}")

    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    isa = pm.run(qc)
    depth, twoq = isa.depth(), isa.num_nonlocal_gates()
    # THIS is the real synthesis cost -- what the hand-built J was built to keep
    # small. On the {ecr/cz, rz, sx, x} basis the 6-CX J should stay shallow.
    print(f"transpiled to {backend.name}: depth {depth} | 2q gates {twoq}")

    job = Sampler(mode=backend).run([isa], shots=shots)
    print(f"submitted job {job.job_id()} -- waiting for result (queue may be long)...")
    result = job.result()
    counts = result[0].data.meas.get_counts()
    print("counts:", counts)
    return counts, backend.name, job.job_id(), depth, twoq


def git_provenance():
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain"], text=True).strip())
    except Exception:  # noqa: BLE001
        commit, dirty = None, None
    return {"commit": commit, "dirty": dirty}


def save_run(counts, shots, backend_name, job_id, isa_depth, isa_2q,
             measured, measured_q, measured_advantage, ref):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results",
                           "hardware-n3", ts)
    os.makedirs(out_dir, exist_ok=True)
    payload = {
        "experiment": "hardware-n3-ghz",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git": git_provenance(),
        "backend": backend_name,
        "job_id": job_id,
        "shots": shots,
        "N": N,
        "gamma": "pi/2",
        "isa_depth": isa_depth,
        "isa_2q_gates": isa_2q,
        "counts": counts,
        "measured_per_player_payoff": [float(x) for x in measured],
        "measured_q_payoff": measured_q,
        "measured_advantage": measured_advantage,
        "reference_advantage": ref["advantage"],
        "classical_ne_payoff": ref["classical_ne_payoff"],
    }
    path = os.path.join(out_dir, "result.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"\nsaved: {os.path.relpath(path)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hardware", action="store_true",
                    help="submit to a real IBM Quantum backend (spends credits)")
    ap.add_argument("--backend", default=None,
                    help="pin a backend by name (default: least-busy real device)")
    ap.add_argument("--shots", type=int, default=DEFAULT_SHOTS)
    args = ap.parse_args()

    # Gate 1: circuit identity. Gate 2: noiseless Aer dry-run reproduces 1.0.
    qc = build_validated_circuit()
    qc_measured = qc.copy()
    qc_measured.measure_all()  # measure_all creates creg 'meas'

    dry_counts = run_dry(qc_measured, args.shots)
    _, _, _, dry_adv, ref = counts_to_advantage(dry_counts, args.shots)
    TOL = 1e-6
    if abs(dry_adv - ref["advantage"]) >= TOL:
        print(f"\nDISCREPANCY: dry-run advantage {dry_adv:.6f} != reference "
              f"{ref['advantage']:.6f}. Not submitting to hardware -- investigate.")
        sys.exit(1)
    print(f"\nGate PASSED: identity + noiseless dry-run reproduce advantage "
          f"{ref['advantage']:.6f}.")

    if not args.hardware:
        print("(dry run only; pass --hardware to submit to a real backend.)")
        return

    print("\n=== HARDWARE SUBMISSION ===")
    counts, backend_name, job_id, depth, twoq = run_hardware(
        qc_measured, args.shots, args.backend)
    probs, measured, measured_q, measured_adv, ref = counts_to_advantage(
        counts, args.shots)
    save_run(counts, args.shots, backend_name, job_id, depth, twoq,
             measured, measured_q, measured_adv, ref)
    print(f"\nHardware advantage = {measured_adv:.6f} "
          f"(noiseless reference {ref['advantage']:.6f}). "
          "Any positive value validates that the quantum advantage survives on "
          "real hardware; the gap to 1.0 is device noise.")


if __name__ == "__main__":
    main()
