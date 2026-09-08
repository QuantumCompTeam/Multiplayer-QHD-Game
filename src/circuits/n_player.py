"""General N-qubit EWL Hawk-Dove circuit.

Circuit sequence for N players:
  |0...0> --[J(gamma)]-- [U(s_0) x ... x U(s_{N-1})] --[J_dag(gamma)]-- Statevector

Returns exact probabilities via Qiskit Statevector (no sampling, no randomness).

Interface contract (producer side):
  build_ewl_circuit returns NDArray[float64] of shape (2**N,).
  probs[i] = P(measuring |i>). Bit ordering: Qiskit little-endian.
  (i >> j) & 1 == 1  <=>  player j plays Hawk in outcome i.
  sum(result) == 1.0.

The entangler parameter accepts any Callable[[int, float], ndarray] so that
graph-based topologies (Month 3) can be passed in via make_pairwise_entangler(G)
without changing this function's signature.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import numpy.typing as npt
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector

from circuits.ewl import U, StrategyParams
from circuits.topologies import Entangler, ghz_entangler
from config import GAMMA


@lru_cache(maxsize=None)
def _entangler_gates(
    entangler: Entangler, N: int, gamma: float
) -> tuple[UnitaryGate, UnitaryGate]:
    """Return cached (J, J_dag) UnitaryGates for a given (entangler, N, gamma).

    The entangler matrix depends only on (entangler, N, gamma) and is identical
    across every strategy profile in a sweep cell, so building it -- and the two
    UnitaryGate wrappers -- once and reusing them avoids recomputing the
    2^N x 2^N unitary on each of the 3^N profiles. Keyed on the entangler
    function object (the module-level ghz_entangler / ring_entangler / ... are
    identity-stable and hashable) plus N and gamma.
    """
    j_mat = entangler(N, gamma)
    j_gate = UnitaryGate(j_mat, label="J")
    j_dag_gate = UnitaryGate(j_mat.conj().T, label="Jdag")
    return j_gate, j_dag_gate


def build_ewl_qc(
    N: int,
    strategies: list[StrategyParams],
    *,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
) -> QuantumCircuit:
    """Construct the N-player EWL circuit (J · per-player U · J†), no measurement.

    Separated from build_ewl_circuit so the circuit can be drawn (see
    experiment.topology_viz.draw_circuit) without re-deriving the protocol.

    The entangler J is a single boxed UnitaryGate spanning all N qubits, so the
    drawn circuit shows the protocol shape, which is the same for every topology
    at a given N -- the topology STRUCTURE lives in the entanglement graph, not
    this diagram. See build_ewl_circuit for the parameter contract.
    """
    if len(strategies) != N:
        raise ValueError(f"expected exactly {N} player strategies, got {len(strategies)}")
    j_gate, j_dag_gate = _entangler_gates(entangler, N, gamma)

    qc = QuantumCircuit(N)
    qc.append(j_gate, list(range(N)))
    for qubit, params in enumerate(strategies):
        qc.append(UnitaryGate(U(*params), label="U"), [qubit])
    qc.append(j_dag_gate, list(range(N)))
    return qc


def build_ewl_circuit(
    N: int,
    strategies: list[StrategyParams],
    *,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
) -> npt.NDArray[np.float64]:
    """Run an N-player EWL circuit and return exact outcome probabilities.

    N: number of players (qubits).
    strategies: list of N (theta, alpha, beta) parameter tuples, one per player.
                strategies[j] is applied to qubit j.
    entangler: callable (N, gamma) -> 2^N x 2^N unitary matrix.
               Defaults to ghz_entangler (the X^(x)N formula).
               Pass make_pairwise_entangler(G) for graph topologies (Month 3).
    gamma: entanglement parameter. Restricted equilibrium depends on the chosen
           branch and angle; see game.phase_branches for the GHZ boundary.

    Returns shape (2**N,). probs[i] = P(measuring basis state |i>).
    Bit ordering: player j is Hawk iff (i >> j) & 1 == 1 (Qiskit little-endian).
    """
    qc = build_ewl_qc(N, strategies, entangler=entangler, gamma=gamma)
    return np.asarray(Statevector(qc).probabilities(), dtype=np.float64)
