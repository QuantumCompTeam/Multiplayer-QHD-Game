"""Month-1 two-player EWL Hawk-Dove circuit.

Thin wrapper around build_ewl_circuit(2, ...) so that the Month-1 public
interface (run_two_player) is unchanged while the implementation is shared
with the general N-player path.

Interface contract (unchanged from Month 1):
  run_two_player returns NDArray[float64] of shape (4,) = (2**2,).
  probs[i] = P(measuring |i>). Bit ordering: Qiskit little-endian.
  sum(result) == 1.0.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from circuits.ewl import StrategyParams
from circuits.n_player import build_ewl_circuit
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
           property to hold -- see GAMMA guard in config.py.

    Returns shape (4,) = (2**2,). probs[i] = P(measuring basis state |i>).
    Bit ordering: player j is Hawk iff (i >> j) & 1 == 1 (Qiskit little-endian).
    """
    return build_ewl_circuit(2, [s0, s1], gamma=gamma)
