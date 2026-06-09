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

import numpy as np
import numpy.typing as npt
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector

from circuits.ewl import U, StrategyParams
from circuits.topologies import Entangler, ghz_entangler
from config import GAMMA


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
    gamma: entanglement parameter. Must equal pi/2 for Nash equilibrium
           property to hold -- see GAMMA guard in config.py.

    Returns shape (2**N,). probs[i] = P(measuring basis state |i>).
    Bit ordering: player j is Hawk iff (i >> j) & 1 == 1 (Qiskit little-endian).
    """
    j_mat = entangler(N, gamma)
    j_gate = UnitaryGate(j_mat, label="J")
    j_dag_gate = UnitaryGate(j_mat.conj().T, label="Jdag")

    qc = QuantumCircuit(N)
    qc.append(j_gate, list(range(N)))
    for qubit, params in enumerate(strategies):
        qc.append(UnitaryGate(U(*params)), [qubit])
    qc.append(j_dag_gate, list(range(N)))

    return np.asarray(Statevector(qc).probabilities(), dtype=np.float64)
