"""N=3 GHZ EWL hardware-validation pipeline (Month 5).

Dry-run goal: reproduce the Month-2 advantage = 1.0 on a NOISELESS AerSimulator
using the validated src/ circuit construction, gated by a circuit-identity
assertion that distinguishes the real Q_3 circuit from the earlier placeholder.

Does NOT submit to real hardware. The transpiled depth / 2q-gate print is kept
so we can watch how the 8x8 J entangler synthesizes when we later target
ibm_marrakesh (see the caveat at that print).
"""

import os
import sys

# Add src to the import path the same way scripts/n3_advantage.py does.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from qiskit.quantum_info import Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_aer import AerSimulator

from config import GAMMA
from circuits.ewl import U, q_strategy
from circuits.topologies import ghz_entangler
from game.payoffs import expected_payoff, index_to_bitstring
from game.nash import compute_advantage
from hand_built_j import build_ewl_qc_handbuilt  # PROTOTYPE: structure-aware J

N = 3
SHOTS = 4096

# ── Task 1: build the VALIDATED N=3 GHZ EWL circuit ──
# J = cos(GAMMA/2) I + i sin(GAMMA/2) X⊗X⊗X via ghz_entangler; per-player
# Q_3 = U(0, pi/3, pi/3) via the project's custom U matrix. This is the exact
# construction behind the Month-2 advantage = 1.0 result.
# PROTOTYPE: use the hand-built structure-aware J (6 CZ on ibm_marrakesh vs 35
# QSD). Same unitary — the identity assertion below proves it against the
# ghz_entangler reference. Revert to build_ewl_qc(...) for the canonical path.
qc = build_ewl_qc_handbuilt(N, GAMMA)

# ── Task 2: circuit-identity assertion (before measurement) ──
# Both the validated circuit and the old H+CX / qiskit-u placeholder collapse to
# |000> on a noiseless sim, so counts cannot tell them apart. Assert the full
# 8x8 unitary instead. The reference is rebuilt from src primitives
# (ghz_entangler, U) as J† · (U⊗U⊗U) · J — independent of build_ewl_qc's
# gate-assembly logic, and unequal to the placeholder's unitary.
# count_ops() is NOT usable as the check: every validated gate (J, the three
# U's, J†) serializes to the generic label 'unitary', so a name-based check
# cannot see 'J'/'U'. Operator.equiv is the strongest and only reliable option.
_Uq = U(*q_strategy(N))
_U_layer = np.kron(np.kron(_Uq, _Uq), _Uq)
_J = ghz_entangler(N, GAMMA)
_reference = Operator(_J.conj().T @ _U_layer @ _J)  # circuit order: J, then U-layer, then J†
if not Operator(qc).equiv(_reference):
    print("DISCREPANCY: constructed circuit is NOT the validated Q_3 unitary.")
    print("  count_ops:", dict(qc.count_ops()))
    sys.exit(1)
print("Circuit-identity assertion PASSED (Operator.equiv vs J†·(U⊗U⊗U)·J).")

# Add measurement AFTER the identity check (measure_all creates creg 'meas').
qc.measure_all()

# ── Dry run on the noiseless simulator (NO hardware submission) ──
backend = AerSimulator()
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
isa = pm.run(qc)

result = Sampler(mode=backend).run([isa], shots=SHOTS).result()
counts = result[0].data.meas.get_counts()

print("counts:", counts)
# CAVEAT: AerSimulator executes arbitrary UnitaryGates natively, so this depth /
# 2q count does NOT reflect how J decomposes on hardware. Real synthesis depth
# appears only when transpiling to ibm_marrakesh's basis gates (the hardware step).
print("transpiled depth:", isa.depth(), "| 2q gates:", isa.num_nonlocal_gates())

# ── Task 3: counts → probs → measured advantage ──
probs = np.zeros(2 ** N, dtype=np.float64)
for bitstr, c in counts.items():
    probs[int(bitstr, 2)] = c / SHOTS  # MSB-left bitstring -> little-endian index

measured = expected_payoff(probs, N)
measured_q = float(np.mean(measured))

# Reference baseline. NOTE: compute_advantage is NOT closed-form — it runs the
# EXACT noiseless Statevector sim over all {D,H,Q}^3 profiles, then does the Nash
# game theory on that tensor. classical_ne_payoff (=1/3) and advantage (=1.0) are
# exact/deterministic and independent of the AerSimulator SAMPLING path measured
# above, so this remains a valid consistency check (sim-vs-sim on the noiseless
# backend; the real hardware run is what makes it an independent validation).
ref = compute_advantage(N=N)
classical_ne = ref["classical_ne_payoff"]
measured_advantage = measured_q - classical_ne

print()
print("measured (Q,Q,Q) distribution:")
for i, p in enumerate(probs):
    if p > 0:
        print(f"  |{index_to_bitstring(i, N)}>  P={p:.6f}")
print("measured per-player payoff :", measured)
print(f"measured (Q,Q,Q) payoff    : {measured_q:.6f}  (ref V/N = {4/3:.6f})")
print(f"classical NE payoff        : {classical_ne:.6f}  (ref 1/3)")
print(f"measured advantage         : {measured_advantage:.6f}")
print(f"reference advantage        : {ref['advantage']:.6f}")

# ── Task 4: PASS gate — identity assertion already passed above (or we exited). ──
TOL = 1e-6
delta = abs(measured_advantage - ref["advantage"])
if delta < TOL:
    print(f"\nPASS: identity assertion passed AND |measured − reference| = "
          f"{delta:.2e} < {TOL:g}. Month-2 advantage reproduced on AerSimulator.")
else:
    print(f"\nDISCREPANCY: |measured − reference| = {delta:.2e} >= {TOL:g}. "
          "Not adjusting numbers — investigate.")
    sys.exit(1)
