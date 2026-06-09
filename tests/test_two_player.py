"""Month-1 checkpoint: two-player EWL Hawk-Dove validation.

Proves three things:
  1. Classical strategy pairs reproduce the 2x2 Hawk-Dove payoff table exactly.
  2. (Q, Q) yields expected payoff (2.0, 2.0) — the quantum Nash equilibrium.
  3. Nash property: neither player improves above 2.0 by deviating from Q to
     any classical strategy (Hawk or Dove).

All results come from exact statevector simulation — no sampling, no hardcoding.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from circuits.ewl import DOVE, HAWK, Q
from circuits.two_player import run_two_player
from game.payoffs import expected_payoff

_V, _C, _N = 4.0, 3.0, 2


def _ep(s0: tuple[float, float, float], s1: tuple[float, float, float]) -> npt.NDArray[np.float64]:
    return expected_payoff(run_two_player(s0, s1), _N, _V, _C)


# -- Classical sanity: all four entries of the Hawk-Dove payoff matrix ----------

def test_classical_dove_dove() -> None:
    np.testing.assert_allclose(_ep(DOVE, DOVE), [2.0, 2.0], atol=1e-6)


def test_classical_dove_hawk() -> None:
    np.testing.assert_allclose(_ep(DOVE, HAWK), [0.0, 4.0], atol=1e-6)


def test_classical_hawk_dove() -> None:
    np.testing.assert_allclose(_ep(HAWK, DOVE), [4.0, 0.0], atol=1e-6)


def test_classical_hawk_hawk() -> None:
    np.testing.assert_allclose(_ep(HAWK, HAWK), [0.5, 0.5], atol=1e-6)


# -- Month-1 checkpoint ---------------------------------------------------------

def test_q_q_yields_cooperative_payoff() -> None:
    """(Q, Q) -> expected payoff (2.0, 2.0): the quantum Nash equilibrium.

    Passes iff GAMMA == pi/2 and J is built with the correct sign convention.
    Wrong gamma or wrong sign produces a payoff below (2, 2).
    """
    np.testing.assert_allclose(_ep(Q, Q), [2.0, 2.0], atol=1e-6)


# -- Nash property: Q is a best response to Q -----------------------------------

def test_nash_hawk_deviation_does_not_improve() -> None:
    """Player 0 deviating to HAWK while player 1 stays on Q must not exceed 2.0."""
    payoff = _ep(HAWK, Q)[0]
    assert payoff <= 2.0 + 1e-6, (
        f"Nash property violated: HAWK deviation yielded {payoff:.8f} > 2.0"
    )


def test_nash_dove_deviation_does_not_improve() -> None:
    """Player 0 deviating to DOVE while player 1 stays on Q must not exceed 2.0."""
    payoff = _ep(DOVE, Q)[0]
    assert payoff <= 2.0 + 1e-6, (
        f"Nash property violated: DOVE deviation yielded {payoff:.8f} > 2.0"
    )
