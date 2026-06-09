"""Unit tests for the Benjamin-Hayden N-player Hawk-Dove payoff function.

Tests the 2-player payoff table (N=2, V=4, C=3) against all four classical
strategy combinations. Bit ordering: i=1 (0b01) -> player 0 Hawk (LSB=bit0).
"""

import numpy as np

from game.payoffs import outcome_payoff


def test_dove_dove() -> None:
    """i=0 (0b00): both Dove -> each gets V/N = 4/2 = 2."""
    np.testing.assert_allclose(outcome_payoff(0, 2, 4.0, 3.0), [2.0, 2.0], atol=1e-10)


def test_hawk_dove() -> None:
    """i=1 (0b01): player 0 Hawk (bit 0 set), player 1 Dove -> [4, 0]."""
    np.testing.assert_allclose(outcome_payoff(1, 2, 4.0, 3.0), [4.0, 0.0], atol=1e-10)


def test_dove_hawk() -> None:
    """i=2 (0b10): player 0 Dove, player 1 Hawk (bit 1 set) -> [0, 4]."""
    np.testing.assert_allclose(outcome_payoff(2, 2, 4.0, 3.0), [0.0, 4.0], atol=1e-10)


def test_hawk_hawk() -> None:
    """i=3 (0b11): both Hawk -> each gets (V-C)/k = (4-3)/2 = 0.5."""
    np.testing.assert_allclose(outcome_payoff(3, 2, 4.0, 3.0), [0.5, 0.5], atol=1e-10)
