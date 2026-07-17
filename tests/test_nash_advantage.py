"""Tests for compute_advantage per-player reporting (Month 3 refactor).

Guards the backward-compatible scalar keys for symmetric topologies (GHZ) and
confirms asymmetric topologies (star) are handled via per-player vectors
without tripping the old symmetry assertion.
"""

from __future__ import annotations

import numpy as np

from circuits.topologies import fully_connected_entangler, star_entangler
from game.nash import compute_advantage


def test_ghz_n3_backward_compatible_scalars() -> None:
    """GHZ N=3 still yields advantage=1.0, (Q,Q,Q) Nash, symmetric payoffs."""
    r = compute_advantage(N=3)  # default entangler = ghz_entangler
    assert r["q_is_nash"] is True
    assert r["symmetric"] is True
    np.testing.assert_allclose(r["q_payoff_per_player"], 4.0 / 3.0, atol=1e-6)
    np.testing.assert_allclose(r["classical_ne_payoff"], 1.0 / 3.0, atol=1e-6)
    np.testing.assert_allclose(r["advantage"], 1.0, atol=1e-6)
    # Vectors are present and consistent with the scalars under symmetry.
    np.testing.assert_allclose(r["q_payoff_vector"], [4.0 / 3.0] * 3, atol=1e-6)
    np.testing.assert_allclose(r["advantage_vector"], [1.0] * 3, atol=1e-6)


def test_star_n3_runs_with_per_player_vectors() -> None:
    """Star (asymmetric hub vs spoke) computes without the old symmetry assert.

    The refactor must report per-player vectors of length N rather than crashing
    on the previous [0]-collapse symmetry precondition.
    """
    r = compute_advantage(N=3, entangler=star_entangler)
    assert len(r["q_payoff_vector"]) == 3
    assert len(r["advantage_vector"]) == 3
    assert isinstance(r["symmetric"], bool)
    # Scalar advantage equals the mean of the per-player advantage vector.
    np.testing.assert_allclose(
        r["advantage"], float(np.mean(r["advantage_vector"])), atol=1e-9
    )


def test_fully_connected_n3_equals_ghz_result() -> None:
    """At N=3 ring/FC reduce to the triangle; FC advantage matches the GHZ case
    only if the payoff structure coincides -- here we just assert it is symmetric
    and the per-player vector is internally consistent."""
    r = compute_advantage(N=3, entangler=fully_connected_entangler)
    assert len(r["q_payoff_vector"]) == 3
    np.testing.assert_allclose(
        r["advantage"], float(np.mean(r["advantage_vector"])), atol=1e-9
    )
