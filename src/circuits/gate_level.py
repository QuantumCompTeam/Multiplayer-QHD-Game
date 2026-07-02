"""Gate-level (elementary-gate) EWL entangler circuits for the noisy path.

The noiseless path (circuits/n_player, circuits/topologies) applies each entangler
as a single dense 2^N x 2^N UnitaryGate -- exact and fast, but a monolithic gate
carries no per-gate noise. For Month-4 depolarizing analysis we need the SAME
unitary expressed as elementary gates, so a NoiseModel can attach 1- and 2-qubit
errors per physical gate (see Month-4 spec D3/2A).

Each builder returns a QuantumCircuit whose operator equals the corresponding dense
entangler in circuits/topologies up to a global phase -- verified by
tests/test_gate_level.py against those dense matrices, which stay authoritative.

Sign convention: the project uses exp(+i*gamma/2 * X..X), but Qiskit
RXXGate(theta) = exp(-i*theta/2 * X_i X_j), so every pairwise edge uses
RXXGate(-gamma). The GHZ global rotation exp(+i*gamma/2 * X^(x)N) is built by
conjugating a Z^(x)N parity rotation with Hadamards; RZ(phi) = exp(-i*phi/2 Z),
so the parity rotation uses RZ(-gamma).

W has no compact native-gate form, so w_gate_circuit transpiles the dense
w_entangler unitary to the pinned {u, cx} basis (Month-4 spec D2/1A). Its gate
count is synthesis-derived, so W noise results are labelled "approximate".
"""

from __future__ import annotations

import math

from qiskit import transpile
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import RXXGate, UnitaryGate

from circuits.topologies import w_entangler
from circuits.topology_graphs import topology_graph
from config import GAMMA

# Basis for the transpiled W fallback -- pinned so W's gate count (and thus its
# noise cost) is deterministic and version-independent (Month-4 spec D2/D3).
_PINNED_BASIS = ["u", "cx"]
_PINNED_OPT_LEVEL = 1


def pairwise_gate_circuit(
    edges: list[tuple[int, int]], N: int, gamma: float = GAMMA
) -> QuantumCircuit:
    """Entangle each (i, j) in `edges` via RXXGate(-gamma) = exp(+i*gamma/2 X_iX_j).

    All X_iX_j terms commute, so edge order does not matter. Reduces to a single
    RXX at N=2 (one edge), matching J_matrix(gamma).
    """
    qc = QuantumCircuit(N)
    for i, j in edges:
        qc.append(RXXGate(-gamma), [i, j])
    return qc


def ghz_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit:
    """Global EWL entangler exp(+i*gamma/2 * X^(x)N) as elementary gates.

    X^(x)N = H^(x)N Z^(x)N H^(x)N, so exp(+i*gamma/2 X^(x)N) =
    H^(x)N * exp(+i*gamma/2 Z^(x)N) * H^(x)N. The Z^(x)N parity rotation is a
    CNOT ladder that accumulates parity onto the last qubit, one RZ(-gamma), then
    the ladder uncomputed. O(N) two-qubit gates.
    """
    qc = QuantumCircuit(N)
    qc.h(range(N))
    for q in range(N - 1):
        qc.cx(q, q + 1)
    qc.rz(-gamma, N - 1)
    for q in reversed(range(N - 1)):
        qc.cx(q, q + 1)
    qc.h(range(N))
    return qc


def ring_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit:
    """Pairwise entangler on the cycle C_N (RXX per ring edge)."""
    edges = [(int(i), int(j)) for i, j in topology_graph("ring", N).edges()]
    return pairwise_gate_circuit(edges, N, gamma)


def star_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit:
    """Pairwise entangler on the star (hub = qubit 0), RXX per spoke."""
    edges = [(int(i), int(j)) for i, j in topology_graph("star", N).edges()]
    return pairwise_gate_circuit(edges, N, gamma)


def fully_connected_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit:
    """Pairwise entangler on K_N (RXX per edge, N(N-1)/2 edges)."""
    edges = [
        (int(i), int(j)) for i, j in topology_graph("fully-connected", N).edges()
    ]
    return pairwise_gate_circuit(edges, N, gamma)


def _w_prep_cascade(N: int) -> QuantumCircuit:
    """Cascade T with T|e_0> = |W> (all real +1/sqrt(N) amplitudes) and T|0..0> = |0..0>.

    Block k (k = 0..N-2): CRy(theta_k) control k -> target k+1, then CNOT
    control k+1 -> target k, with theta_k = 2*arccos(1/sqrt(N-k)). Each block
    moves sin(theta_k/2) of the excitation amplitude from qubit k to k+1,
    leaving cos(theta_k/2) * prod_{m<k} sin(theta_m/2) = 1/sqrt(N) behind.
    Every gate is controlled on a qubit that is |0> in the all-zeros state, so
    T fixes |0...0> exactly — required by the conjugation construction
    (spec 2026-07-02-w-entangler-gate-level-design.md, D-T8.3).
    """
    qc = QuantumCircuit(N)
    for k in range(N - 1):
        theta = 2.0 * math.acos(1.0 / math.sqrt(N - k))
        qc.cry(theta, k, k + 1)
        qc.cx(k + 1, k)
    return qc


def w_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit:
    """W entangler as gates: transpile the dense w_entangler unitary (APPROXIMATE).

    The S_W reflection has no compact native-gate form, so we synthesize the dense
    unitary into the pinned {u, cx} basis. The gate count is a synthesis artifact,
    not a physical W-prep circuit -- W noise results must be reported as
    approximate (Month-4 spec D2/1A). A faithful gate-level W is a TODO.
    """
    qc = QuantumCircuit(N)
    qc.append(UnitaryGate(w_entangler(N, gamma), label="Jw"), list(range(N)))
    return transpile(
        qc, basis_gates=_PINNED_BASIS, optimization_level=_PINNED_OPT_LEVEL
    )
