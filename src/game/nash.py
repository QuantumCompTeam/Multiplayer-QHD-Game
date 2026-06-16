"""N-player Nash equilibrium analysis for EWL Hawk-Dove.

SCOPE: Pure-strategy enumeration over a finite discrete strategy set (default
{D, H, Q}).  This is NOT continuous / mixed-strategy Nash analysis over all of
SU(2); that is explicitly future work per the README.

NASHPY: not used here. Nashpy is built for 2-player normal-form games; the N>=2
path uses direct best-response enumeration (see find_pure_nash). Nashpy remains a
pinned dependency, reserved for future 2-player cross-validation (spec §2.3).

The "Q" label in strategy_names refers to q_strategy(N) = U(0, pi/N, pi/N),
the N-appropriate quantum Nash strategy, NOT the fixed U(0, pi/2, pi/2) which
is only valid at N=2.  See ewl.q_strategy for the derivation.

Public API:
  build_payoff_tensor  -- evaluate all strategy profiles, return payoff dict
  find_pure_nash       -- identify pure Nash equilibria by best-response check
  compute_advantage    -- quantum NE payoff vs classical NE payoff (RQ1)
"""

from __future__ import annotations

import itertools
from typing import Any

import numpy as np
import numpy.typing as npt

from circuits.ewl import DOVE, HAWK, StrategyParams, q_strategy
from circuits.n_player import build_ewl_circuit
from circuits.topologies import Entangler, ghz_entangler
from config import C as DEFAULT_C, GAMMA, V as DEFAULT_V
from game.payoffs import expected_payoff

# Default strategy set for all Month-2 computations.
STRATEGY_NAMES: list[str] = ["D", "H", "Q"]


def _strategy_map(N: int) -> dict[str, StrategyParams]:
    """Map strategy names to (theta, alpha, beta) parameter tuples for N players.

    "Q" is q_strategy(N) = U(0, pi/N, pi/N), the N-appropriate quantum Nash
    strategy.  Classical strategies D and H are N-independent.
    """
    return {"D": DOVE, "H": HAWK, "Q": q_strategy(N)}


def build_payoff_tensor(
    N: int,
    strategy_names: list[str] = STRATEGY_NAMES,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
) -> dict[tuple[str, ...], npt.NDArray[np.float64]]:
    """Evaluate all strategy profiles and return per-player payoffs.

    Iterates over all len(strategy_names)^N profiles.  For each profile,
    runs build_ewl_circuit -> expected_payoff.

    "Q" in strategy_names maps to q_strategy(N) = U(0, pi/N, pi/N).

    Returns: dict mapping profile tuple -> shape (N,) payoff array.
    For N=3, strategy_names=["D","H","Q"]: 27 entries.

    Pure-strategy enumeration only.  Does not compute mixed-strategy equilibria.
    """
    smap = _strategy_map(N)
    tensor: dict[tuple[str, ...], npt.NDArray[np.float64]] = {}
    for profile in itertools.product(strategy_names, repeat=N):
        params = [smap[s] for s in profile]
        probs = build_ewl_circuit(N, params, entangler=entangler, gamma=gamma)
        tensor[profile] = expected_payoff(probs, N, V, C)
    return tensor


def find_pure_nash(
    tensor: dict[tuple[str, ...], npt.NDArray[np.float64]],
    N: int,
    strategy_names: list[str] = STRATEGY_NAMES,
) -> list[tuple[str, ...]]:
    """Find all pure Nash equilibria by direct best-response check.

    A profile p is a pure NE iff for every player i and every alternative
    strategy s in strategy_names, payoff(p)[i] >= payoff(p')[i] where p' is p
    with player i switched to s.

    Tolerance 1e-9 absorbs floating-point noise; a deviation must improve
    payoff by more than that to disqualify a profile.

    Pure-strategy enumeration only.  See module docstring for scope caveat.
    """
    nash_profiles: list[tuple[str, ...]] = []
    for profile in tensor:
        is_nash = True
        for player in range(N):
            for alt in strategy_names:
                if alt == profile[player]:
                    continue
                deviation = list(profile)
                deviation[player] = alt
                dev_payoff = tensor[tuple(deviation)][player]
                if dev_payoff > tensor[profile][player] + 1e-9:
                    is_nash = False
                    break
            if not is_nash:
                break
        if is_nash:
            nash_profiles.append(profile)
    return nash_profiles


def compute_advantage(
    N: int = 3,
    strategy_names: list[str] = STRATEGY_NAMES,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
) -> dict[str, Any]:
    """Compute quantum advantage: quantum NE payoff vs classical NE payoff (RQ1).

    Advantage is defined as:
        advantage = q_payoff_per_player - classical_ne_payoff

    where:
    - q_payoff_per_player is the per-player payoff at (Q,...,Q) with
      Q = q_strategy(N), taken from simulation (not assumed).
    - classical_ne_payoff is derived from find_pure_nash on the RESTRICTED
      classical tensor (only strategies without "Q"), i.e. the Nash equilibrium
      of the classical-only game.

    Selection rule when multiple classical pure NE exist:
      Use the highest per-player symmetric payoff among classical NE.
      Rationale: this gives the most conservative (smallest) advantage estimate,
      making the paper's claim stronger by understating rather than overstating
      the quantum benefit.

    If no classical NE are found: classical_ne_payoff is NaN; flag and investigate.

    The (Q,...,Q) payoff is a SIMULATION RESULT, not an assumed value.
    If advantage <= 0 or q_is_nash is False, this is a finding about RQ1 --
    do not treat it as a bug.

    Returns dict with keys:
      q_payoff_per_player     float  -- per-player payoff at (Q,...,Q)
      classical_ne_payoff     float  -- best (highest) classical pure NE payoff
      advantage               float  -- q_payoff - classical_ne_payoff
      q_is_nash               bool   -- whether (Q,...,Q) is a pure NE
      all_pure_nash           list   -- all pure NE in strategy_names^N
      classical_nash_profiles list   -- pure NE of the restricted classical game
      deviation_check         dict   -- per-(player, alt) unilateral deviation
                                        from (Q,...,Q): payoff and dominance flag
    """
    tensor = build_payoff_tensor(N, strategy_names, V, C, entangler, gamma)
    all_nash = find_pure_nash(tensor, N, strategy_names)

    # SYMMETRY PRECONDITION: this function collapses tensor[p][0] to a single
    # per-player payoff, which assumes all players receive equal payoffs under p.
    # True for the GHZ entangler + symmetric strategy profiles. For asymmetric
    # topologies (star hub vs spoke, weighted ring) player payoffs differ, so the
    # collapse would silently misreport. Assert symmetry on every profile we
    # collapse before reading [0].
    # Month-3 TODO: replace [0] collapse with per-player reporting for non-symmetric topologies.
    def _assert_symmetric(profile: tuple[str, ...]) -> None:
        pay = tensor[profile]
        assert np.allclose(pay, pay[0], atol=1e-8), (
            f"compute_advantage: payoffs for {profile} are not symmetric across "
            f"players ({pay}). This function assumes a GHZ-symmetric topology; for "
            "star/ring topologies use per-player payoff reporting (Month 3)."
        )

    # Classical NE: enumerate NE in the restricted classical-only game {D,H}^N.
    classical_names = [s for s in strategy_names if s != "Q"]
    classical_tensor = {
        p: tensor[p] for p in tensor if all(s in classical_names for s in p)
    }
    classical_nash_profiles = find_pure_nash(classical_tensor, N, classical_names)

    if classical_nash_profiles:
        # Player 0 payoff is representative for symmetric profiles under GHZ.
        for p in classical_nash_profiles:
            _assert_symmetric(p)
        classical_ne_payoff = max(
            float(tensor[p][0]) for p in classical_nash_profiles
        )
    else:
        classical_ne_payoff = float("nan")

    q_profile = tuple("Q" for _ in range(N))
    # Symmetric profile + symmetric GHZ entangler => all players get equal payoff.
    _assert_symmetric(q_profile)
    q_payoff_per_player = float(tensor[q_profile][0])
    advantage = q_payoff_per_player - classical_ne_payoff
    q_is_nash = q_profile in all_nash

    deviation_check: dict[tuple[int, str], dict[str, Any]] = {}
    for player in range(N):
        for alt in strategy_names:
            if alt == "Q":
                continue
            dev_profile = list(q_profile)
            dev_profile[player] = alt
            dev_payoff = float(tensor[tuple(dev_profile)][player])
            deviation_check[(player, alt)] = {
                "deviation_payoff": dev_payoff,
                "q_payoff": q_payoff_per_player,
                "q_dominates": dev_payoff <= q_payoff_per_player + 1e-9,
            }

    return {
        "q_payoff_per_player": q_payoff_per_player,
        "classical_ne_payoff": classical_ne_payoff,
        "advantage": advantage,
        "q_is_nash": q_is_nash,
        "all_pure_nash": all_nash,
        "classical_nash_profiles": classical_nash_profiles,
        "deviation_check": deviation_check,
    }
