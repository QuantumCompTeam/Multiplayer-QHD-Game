"""N-player Hawk-Dove payoff functions (Benjamin-Hayden formula).

Interface contract (consumer side):
  expected_payoff(probs, N, V, C) accepts probs of shape (2**N,) — the direct
  output of any run_*_player function in circuits/. Shape is stable from N=2
  through N=6 without interface changes. result[j] = expected payoff for player j.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from config import C as DEFAULT_C, V as DEFAULT_V


def index_to_bitstring(i: int, n: int) -> str:
    """Return the Qiskit-convention bitstring for basis state index i with n qubits.

    Rightmost character = player 0 (qubit 0). Little-endian.
    Example: n=2, i=1 -> '01'  (player 0 Hawk, player 1 Dove).
    Example: n=2, i=2 -> '10'  (player 0 Dove, player 1 Hawk).
    """
    return format(i, f"0{n}b")


def outcome_payoff(i: int, N: int, V: float, C: float) -> npt.NDArray[np.float64]:
    """Return per-player payoffs for basis state index i (Benjamin-Hayden formula).

    Player j is Hawk iff (i >> j) & 1 == 1  (Qiskit little-endian, see config.py).
    k = number of Hawks = popcount(i).

    Benjamin-Hayden formula:
      k == 0:      all Dove  — each player gets V/N
      0 < k < N:   Hawks take all — each Hawk gets V/k, each Dove gets 0
      k == N:      all Hawk  — each player gets (V-C)/k  (conflict cost shared)

    Returns shape (N,). result[j] = payoff for player j in outcome i.
    """
    k = bin(i).count("1")
    dove_pay: float
    hawk_pay: float
    if k == 0:
        dove_pay = V / N
        hawk_pay = 0.0  # no Hawks present; value unused in the loop below
    elif k == N:
        dove_pay = 0.0
        hawk_pay = (V - C) / k
    else:
        dove_pay = 0.0
        hawk_pay = V / k

    payoffs = np.zeros(N, dtype=np.float64)
    for j in range(N):
        payoffs[j] = hawk_pay if (i >> j) & 1 else dove_pay
    return payoffs


def expected_payoff(
    probs: npt.NDArray[np.float64],
    N: int,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
) -> npt.NDArray[np.float64]:
    """Return expected per-player payoffs given a probability distribution.

    probs: shape (2**N,) — direct output of run_two_player or any run_*_player.
           probs[i] = P(measuring basis state |i>). Must sum to 1.
    Returns: shape (N,). result[j] = expected payoff for player j.
    Shape contract is stable from N=2 through N=6 without changes to this function.
    """
    result = np.zeros(N, dtype=np.float64)
    for i in range(2**N):
        result += probs[i] * outcome_payoff(i, N, V, C)
    return result
