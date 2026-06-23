"""Tests for topology-adaptive quantum strategy optimization (game.strategy_opt).

Scientific anchors used here:

* The mean per-player payoff is bounded by V/N for ANY topology: total payoff
  = V - C*P(all-hawk) <= V, with equality iff P(all-hawk)=0.  DOVE (identity)
  always reaches it because J_dag · I^(x)N · J = I returns |0...0>.  So the
  COOPERATIVE optimum is V/N for every entangler — a clean, topology-independent
  oracle.

* By Benjamin & Hayden, the EWL "miracle move" is NOT a Nash equilibrium against
  full SU(2).  So we do NOT assert q_strategy is a continuous Nash; nash_gap is
  expected to be >= 0 and may be strictly positive even on GHZ.  The nash mode
  searches for a symmetric pure Nash and honestly reports whether one was found.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from circuits.ewl import DOVE, q_strategy
from circuits.topologies import (
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)
from game.nash import compute_advantage
from game.strategy_opt import (
    NASH_TOL,
    cooperative_strategy,
    nash_gap,
    nash_strategy,
    optimal_strategy,
)

_V, _C = 4.0, 3.0
_GAMMA = math.pi / 2
_TOPOS = {
    "ghz": ghz_entangler,
    "ring": ring_entangler,
    "star": star_entangler,
    "fully-connected": fully_connected_entangler,
    "w": w_entangler,
}


@pytest.mark.parametrize("N", [2, 3, 4])
def test_cooperative_recovers_v_over_n_on_ghz(N: int) -> None:
    """COOPERATIVE optimum on GHZ must equal V/N (the proven mean-payoff bound)."""
    res = cooperative_strategy(N, ghz_entangler, _GAMMA, _V, _C)
    npt_payoff = res.payoff_per_player
    assert npt_payoff <= _V / N + 1e-6, "mean payoff cannot exceed V/N"
    assert npt_payoff == pytest.approx(_V / N, abs=1e-6), (
        f"cooperative optimum should reach V/N={_V/N}, got {npt_payoff}"
    )


@pytest.mark.parametrize("name", list(_TOPOS))
def test_cooperative_optimum_is_v_over_n_all_topologies_n3(name: str) -> None:
    """The cooperative optimum is V/N for EVERY topology (DOVE always reaches it)."""
    res = cooperative_strategy(3, _TOPOS[name], _GAMMA, _V, _C)
    assert res.payoff_per_player == pytest.approx(_V / 3.0, abs=1e-6)


def test_ring_n4_optimal_beats_misapplied_ghz_strategy() -> None:
    """HEADLINE: on C_4 the GHZ-derived Q scores 0.25/player; the ring's own
    cooperative optimum reaches V/N=1.0 — so the 'advantage=0' was an artifact of
    transplanting the GHZ strategy, not a property of the topology."""
    # The mis-applied GHZ strategy on the ring (what the legacy sweep measures):
    misapplied = compute_advantage(
        N=4, V=_V, C=_C, entangler=ring_entangler, gamma=_GAMMA
    )
    assert misapplied["q_payoff_vector"][0] == pytest.approx(0.25, abs=1e-6)

    # The ring's own cooperative optimum:
    coop = cooperative_strategy(4, ring_entangler, _GAMMA, _V, _C)
    assert coop.payoff_per_player == pytest.approx(_V / 4.0, abs=1e-6)
    assert coop.payoff_per_player > misapplied["q_payoff_vector"][0] + 0.5


def test_nash_gap_detects_deviation_from_dove() -> None:
    """all-DOVE is cooperative but NOT an equilibrium: a deviator gains, so
    nash_gap(DOVE) must be clearly positive (sanity check that nash_gap works)."""
    gap = nash_gap(DOVE, 3, ring_entangler, _GAMMA, _V, _C)
    assert gap > 1e-3, f"deviating from all-Dove should pay off, gap={gap}"


def test_nash_gap_nonnegative_on_optimized_point() -> None:
    """nash_gap is a max-over-deviations quantity, so it is >= -tol by construction."""
    res = cooperative_strategy(3, ring_entangler, _GAMMA, _V, _C)
    assert res.nash_gap >= -1e-9
    assert res.is_nash == (res.nash_gap <= NASH_TOL)


@pytest.mark.parametrize("name", list(_TOPOS))
def test_n2_reduces_to_single_edge(name: str) -> None:
    """At N=2 every topology is a single edge: cooperative optimum = V/2."""
    res = cooperative_strategy(2, _TOPOS[name], _GAMMA, _V, _C)
    assert res.payoff_per_player == pytest.approx(_V / 2.0, abs=1e-6)


def test_nash_strategy_runs_and_reports_honestly() -> None:
    """nash mode returns a well-formed result; per Benjamin-Hayden a full-SU(2)
    pure Nash may not exist, so we assert structure, not existence."""
    res = nash_strategy(2, ghz_entangler, _GAMMA, _V, _C)
    assert len(res.params) == 3
    assert math.isfinite(res.payoff_per_player)
    assert math.isfinite(res.nash_gap)
    assert isinstance(res.is_nash, bool)
    assert res.mode == "nash"


def test_star_carries_symmetric_caveat() -> None:
    """Star is not vertex-transitive; results must flag the symmetric caveat."""
    res = optimal_strategy(
        "cooperative", 3, star_entangler, _GAMMA, _V, _C, symmetric_caveat=True
    )
    assert res.symmetric_caveat is True


def test_backward_compat_q_params_equals_default() -> None:
    """compute_advantage with q_params=q_strategy(N) must equal the default path."""
    base = compute_advantage(N=3, V=_V, C=_C)
    override = compute_advantage(N=3, V=_V, C=_C, q_params=q_strategy(3))
    assert override["advantage"] == pytest.approx(base["advantage"], abs=1e-12)
    assert override["q_payoff_vector"] == pytest.approx(
        base["q_payoff_vector"], abs=1e-12
    )
    assert override["all_pure_nash"] == base["all_pure_nash"]


def test_determinism_same_seed() -> None:
    """Same seed → identical optimized parameters."""
    a = cooperative_strategy(3, ring_entangler, _GAMMA, _V, _C, seed=7)
    b = cooperative_strategy(3, ring_entangler, _GAMMA, _V, _C, seed=7)
    assert np.allclose(a.params, b.params, atol=1e-9)
    assert a.payoff_per_player == pytest.approx(b.payoff_per_player, abs=1e-12)
