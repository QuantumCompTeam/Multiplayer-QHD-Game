"""Structure-aware decomposition of the N=3 EWL entangler
    J = exp(i*(gamma/2)*X⊗X⊗X) = H⊗³ · exp(i*(gamma/2)*Z⊗Z⊗Z) · H⊗³.

The ZZZ-rotation is a CX ladder folding parity onto q2, RZ(-gamma) on q2, then
the ladder uncomputed (4 CX per J). Verified Operator-equivalent to
circuits.topologies.ghz_entangler (see PROTOTYPE — not yet wired into src/).

Prototype for cutting the ibm_marrakesh CZ count (35 QSD -> 6) without changing
the validated unitary.
"""
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate

from circuits.ewl import U, q_strategy


def hand_built_J_circuit(gamma: float) -> QuantumCircuit:
    """3-qubit circuit implementing J = exp(i*(gamma/2)*XXX) exactly (4 CX)."""
    qc = QuantumCircuit(3, name="J_hb")
    qc.h([0, 1, 2])
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.rz(-gamma, 2)   # lambda = -2*(gamma/2); exp(i*(gamma/2)*Z2) up to the ladder
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.h([0, 1, 2])
    return qc


def hand_built_Jdag_circuit(gamma: float) -> QuantumCircuit:
    """Exact inverse of hand_built_J_circuit (J†)."""
    dag = hand_built_J_circuit(gamma).inverse()
    dag.name = "Jdag_hb"
    return dag


def build_ewl_qc_handbuilt(N: int, gamma: float) -> QuantumCircuit:
    """N=3 EWL circuit (J_hb · U(q_strategy)^⊗N · J_hb†), no measurement.

    Drop-in replacement for circuits.n_player.build_ewl_qc with the GHZ entangler:
    same unitary, structure-aware J instead of an 8x8 UnitaryGate. Only N=3.
    """
    assert N == 3, "hand-built J prototype is N=3 only"
    qc = QuantumCircuit(N)
    qc.compose(hand_built_J_circuit(gamma), range(N), inplace=True)
    for q in range(N):
        qc.append(UnitaryGate(U(*q_strategy(N)), label="U"), [q])
    qc.compose(hand_built_Jdag_circuit(gamma), range(N), inplace=True)
    return qc
