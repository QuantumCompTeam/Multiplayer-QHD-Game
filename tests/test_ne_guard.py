"""N=4/N=5 NE regression guard (item 18, resolves G9).

Pins the equilibrium boundary of the default game (GHZ entangler, V=4, C=3):
(Q,...,Q) is a pure NE at N=2,3 and NOT at N=4,5, where the unilateral Hawk
deviation beats it. Reference values are the registered ones in
docs/VERIFIED-FACTS.md D2/D5, reproduced within 1e-12.

The paper's hardware runs sit at N=3,4,5 on this exact boundary. A code change
that moves any of these numbers changes the game the paper measures — this
guard exists so that edit cannot land silently (G9: prior to this file, no test
asserted q_is_nash is False at N=4 or N=5 for any topology).
"""

from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
import pytest

from game.nash import compute_advantage

# docs/VERIFIED-FACTS.md D5 (raw sweep under the pinned env; defaults:
# GHZ, V=4, C=3). hawk_dev is the (player, "H") deviation_payoff entry —
# identical for every player (GHZ is vertex-transitive, D2).
D5 = {
    2: dict(q_is_nash=True, q_payoff=2.0, classical=0.5,
            advantage=1.5, hawk_dev=1.6872297554945904e-32),
    3: dict(q_is_nash=True, q_payoff=1.3333333333333333,
            classical=0.33333333333333331, advantage=1.0, hawk_dev=1.0),
    4: dict(q_is_nash=False, q_payoff=1.0, classical=0.25,
            advantage=0.75, hawk_dev=2.0000000000000009),
    5: dict(q_is_nash=False, q_payoff=0.80000000000000004,
            classical=0.20000000000000001, advantage=0.60000000000000009,
            hawk_dev=2.6180339887498949),
}
TOL = 1e-12  # the tolerance VERIFIED-FACTS D5 records the identities holding at


@lru_cache(maxsize=None)
def _adv(n: int) -> dict:
    return compute_advantage(N=n)  # defaults: GHZ, V=4, C=3, STRATEGY_NAMES


@pytest.mark.parametrize("n", sorted(D5))
def test_registered_values_reproduce(n: int) -> None:
    """Every D5 scalar reproduces within 1e-12, including the NE flag."""
    r, ref = _adv(n), D5[n]
    assert r["q_is_nash"] is ref["q_is_nash"], (
        f"N={n}: q_is_nash flipped — the equilibrium boundary moved"
    )
    np.testing.assert_allclose(r["q_payoff_per_player"], ref["q_payoff"], atol=TOL)
    np.testing.assert_allclose(r["classical_ne_payoff"], ref["classical"], atol=TOL)
    np.testing.assert_allclose(r["advantage"], ref["advantage"], atol=TOL)
    for player in range(n):
        np.testing.assert_allclose(
            r["deviation_check"][(player, "H")]["deviation_payoff"],
            ref["hawk_dev"], atol=TOL,
            err_msg=f"N={n} player {player}: Hawk deviation payoff moved",
        )


@pytest.mark.parametrize("n", sorted(D5))
def test_candidate_identities(n: int) -> None:
    """The four D5 identities: 4/N, 1/N, 3/N, and 2+2cos(2pi/N)."""
    r = _adv(n)
    np.testing.assert_allclose(r["q_payoff_per_player"], 4.0 / n, atol=TOL)
    np.testing.assert_allclose(r["classical_ne_payoff"], 1.0 / n, atol=TOL)
    np.testing.assert_allclose(r["advantage"], 3.0 / n, atol=TOL)
    np.testing.assert_allclose(
        r["deviation_check"][(0, "H")]["deviation_payoff"],
        2.0 + 2.0 * math.cos(2.0 * math.pi / n), atol=TOL,
    )


@pytest.mark.parametrize("n", sorted(D5))
def test_boundary_inequality_agreement(n: int) -> None:
    """q_is_nash agrees with 2 + 2*cos(2*pi/N) <= V/N (D5, 'as computed,
    not proven'). The transition sits between N=3 and N=4 at V=4."""
    predicted = (2.0 + 2.0 * math.cos(2.0 * math.pi / n)) <= 4.0 / n
    assert _adv(n)["q_is_nash"] == predicted


def test_g9_hawk_breaks_q_at_n4_n5() -> None:
    """The sharp G9 statement: at N=4 and N=5 the Hawk deviation strictly
    beats the (Q,...,Q) payoff, so q_dominates must be False there."""
    for n in (4, 5):
        r = _adv(n)
        for player in range(n):
            entry = r["deviation_check"][(player, "H")]
            assert entry["deviation_payoff"] > entry["q_payoff"], (
                f"N={n} player {player}: Hawk no longer beats Q"
            )
            assert entry["q_dominates"] is False
