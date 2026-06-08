"""Month-1 two-player EWL Hawk-Dove circuit.

Circuit sequence for N=2:
  |00> --[J(gamma)]-- [U(s0) x U(s1)] --[J_dag(gamma)]-- Statevector

Returns exact probabilities via Qiskit Statevector (no sampling, no randomness).

Interface contract (producer side):
  run_two_player returns NDArray[float64] of shape (4,) = (2**2,).
  probs[i] = P(measuring |i>). Bit ordering: Qiskit little-endian (see config.py).
  sum(result) == 1.0.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector

from circuits.ewl import U, make_J_dag_gate, make_J_gate, StrategyParams
from config import GAMMA


def run_two_player(
    s0: StrategyParams,
    s1: StrategyParams,
    *,
    gamma: float = GAMMA,
) -> npt.NDArray[np.float64]:
    """Run the 2-player EWL circuit and return exact outcome probabilities.

    s0: (theta, alpha, beta) for player 0 (qubit 0).
    s1: (theta, alpha, beta) for player 1 (qubit 1).
    gamma: entanglement parameter. Must equal pi/2 for the Nash equilibrium
           property to hold — see GAMMA guard in config.py.

    Returns shape (4,) = (2**2,). probs[i] = P(measuring basis state |i>).
    Bit ordering: player j is Hawk iff (i >> j) & 1 == 1 (Qiskit little-endian).
    """
    qc = QuantumCircuit(2)
    qc.append(make_J_gate(gamma), [0, 1])
    qc.append(UnitaryGate(U(*s0)), [0])
    qc.append(UnitaryGate(U(*s1)), [1])
    qc.append(make_J_dag_gate(gamma), [0, 1])
    return np.asarray(Statevector(qc).probabilities(), dtype=np.float64)
