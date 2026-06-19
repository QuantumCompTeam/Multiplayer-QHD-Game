"""Per-player quantum advantage on ASYMMETRIC topologies (the star).

Vertex-transitive topologies (GHZ, ring, fully-connected, W) give a uniform
per-player advantage, so the scalar mean tells the whole story. The star is NOT
vertex-transitive: the hub (qubit 0) sits in a different structural position from
the leaves (qubits 1..N-1), so its advantage is a per-player VECTOR, not one
number. These tests pin that structure:

  - the leaves are mutually equal (the star's leaf-permutation automorphism),
  - the hub differs from the leaves (genuinely non-uniform),
  - the reported scalar advantage is exactly the mean of the per-player vector,
  - q_payoff_vector == classical_ne_payoff_vector + advantage_vector.

Fixed strategy mode (the default GHZ-derived Q) is used so the result is
deterministic and fast — no optimizer. V=4, C=3 matches the repo test convention.
See tests/test_nash_advantage.py for the symmetric-topology counterpart.
"""

from __future__ import annotations

import numpy as np
import pytest

from circuits.topologies import ghz_entangler, star_entangler
from game.nash import compute_advantage

_V, _C = 4.0, 3.0
_TOL = 1e-6


def _hub_and_leaves(vector: list[float]) -> tuple[float, list[float]]:
    """Split a per-player vector into (hub = player 0, leaves = players 1..N-1)."""
    return float(vector[0]), [float(x) for x in vector[1:]]


@pytest.mark.parametrize("N", [3, 4, 5])
def test_star_leaves_share_one_advantage(N: int) -> None:
    """At every N the star's leaves are interchangeable -> equal advantage.

    The hub (player 0) may or may not differ at small N (it does not at N=3,
    where the star payoff is incidentally uniform); the leaf-permutation
    symmetry, however, holds for all N.
    """
    r = compute_advantage(N=N, V=_V, C=_C, entangler=star_entangler)
    adv = r["advantage_vector"]
    assert len(adv) == N
    _, leaves = _hub_and_leaves(adv)
    np.testing.assert_allclose(leaves, [leaves[0]] * len(leaves), atol=_TOL,
                               err_msg="star leaves must share one advantage value")


@pytest.mark.parametrize("N", [4, 5])
def test_star_is_asymmetric_for_n_ge_4(N: int) -> None:
    """For N>=4 the star is genuinely non-uniform: hub differs from the leaves."""
    r = compute_advantage(N=N, V=_V, C=_C, entangler=star_entangler)
    assert r["symmetric"] is False, "star N>=4 is not vertex-transitive"
    hub, leaves = _hub_and_leaves(r["advantage_vector"])
    assert abs(hub - leaves[0]) > _TOL, "hub and leaf advantage should differ"


@pytest.mark.parametrize("N", [3, 4, 5])
def test_star_scalar_is_mean_and_vectors_consistent(N: int) -> None:
    """Scalar advantage == mean(vector); q = classical + advantage, per player."""
    r = compute_advantage(N=N, V=_V, C=_C, entangler=star_entangler)

    np.testing.assert_allclose(
        r["advantage"], float(np.mean(r["advantage_vector"])), atol=1e-9
    )
    q = np.asarray(r["q_payoff_vector"], dtype=float)
    cne = np.asarray(r["classical_ne_payoff_vector"], dtype=float)
    adv = np.asarray(r["advantage_vector"], dtype=float)
    np.testing.assert_allclose(q, cne + adv, atol=1e-9)


def test_star_n4_known_per_player_split() -> None:
    """Pin the headline star N=4 fixed-mode split: hub sacrificed, leaves gain.

    Under the GHZ-derived Q on the star at gamma=pi/2, V=4, C=3 the per-player
    advantage is [0, 1, 1, 1] (hub gains nothing over classical; each leaf gains
    1). This is the concrete face of "the mean (0.75) hides a per-player split".
    """
    r = compute_advantage(N=4, V=_V, C=_C, entangler=star_entangler)
    np.testing.assert_allclose(r["advantage_vector"], [0.0, 1.0, 1.0, 1.0], atol=_TOL)
    np.testing.assert_allclose(r["advantage"], 0.75, atol=_TOL)


def test_symmetric_topology_advantage_is_uniform() -> None:
    """Control: a vertex-transitive topology (GHZ) gives a uniform vector."""
    r = compute_advantage(N=4, V=_V, C=_C, entangler=ghz_entangler)
    assert r["symmetric"] is True
    adv = r["advantage_vector"]
    np.testing.assert_allclose(adv, [adv[0]] * len(adv), atol=_TOL)
