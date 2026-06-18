"""N-player Hawk-Dove payoff functions (Benjamin-Hayden formula).

Interface contract (consumer side):
  expected_payoff(probs, N, V, C) accepts probs of shape (2**N,) — the direct
  output of any run_*_player function in circuits/. Shape is stable from N=2
  through N=6 without interface changes. result[j] = expected payoff for player j.
"""

from __future__ import annotations

from functools import lru_cache

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
    k = i.bit_count()  # popcount; Python 3.10+
    dove_pay: float
    hawk_pay: float
    if k == 0:
        dove_pay = V / N
        hawk_pay = 0.0  # no Hawks present; value unused below
    elif k == N:
        dove_pay = 0.0
        hawk_pay = (V - C) / k
    else:
        dove_pay = 0.0
        hawk_pay = V / k

    # Vectorised bit test: player j is Hawk iff bit j of i is set (little-endian).
    is_hawk = (i >> np.arange(N)) & 1
    return np.where(is_hawk, hawk_pay, dove_pay).astype(np.float64)


@lru_cache(maxsize=None)
def _payoff_matrix(N: int, V: float, C: float) -> npt.NDArray[np.float64]:
    """Cached (2**N, N) payoff matrix: P[i, j] = payoff for player j in outcome i.

    Built once per (N, V, C) and reused for every expected_payoff call, replacing
    the per-call Python loop over all 2**N outcomes.  Encodes the same
    Benjamin-Hayden formula as outcome_payoff (verified against it in tests):
      k == 0:      all Dove  -> V / N for every player
      0 < k < N:   each Hawk -> V / k, each Dove -> 0
      k == N:      all Hawk  -> (V - C) / k for every player
    where k = popcount(i) and player j is Hawk iff bit j of i is set.
    """
    dim = 2 ** N
    idx = np.arange(dim)
    bits = (idx[:, None] >> np.arange(N)) & 1  # (dim, N), little-endian
    k = bits.sum(axis=1)  # popcount per outcome
    dove = np.where(k == 0, V / N, 0.0)
    safe_k = np.maximum(k, 1)  # avoid div-by-zero at k==0 (hawk value unused there)
    hawk = np.where(k == N, (V - C) / safe_k, V / safe_k)
    return np.where(bits, hawk[:, None], dove[:, None]).astype(np.float64)


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
    # Interface contract (spec §4 / config.py): probs must be shape (2**N,) and normalised.
    if probs.shape != (2 ** N,):
        raise ValueError(
            f"expected_payoff: probs shape {probs.shape} does not match (2**{N},) = "
            f"({2**N},). Check that build_ewl_circuit returns the correct number of qubits."
        )
    if not np.isclose(probs.sum(), 1.0, atol=1e-6):
        raise ValueError(
            f"expected_payoff: probs sum to {probs.sum():.6f}, expected 1.0. "
            f"Circuit probabilities are not normalised."
        )
    # Expected payoff per player = sum_i probs[i] * P[i, :] = probs @ P, where P
    # is the cached (2**N, N) outcome-payoff matrix.  Replaces the per-outcome
    # Python loop with a single matrix-vector product.
    return probs @ _payoff_matrix(N, V, C)
