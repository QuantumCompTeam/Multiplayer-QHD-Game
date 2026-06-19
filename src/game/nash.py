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


def _strategy_map(
    N: int, q_params: StrategyParams | None = None
) -> dict[str, StrategyParams]:
    """Map strategy names to (theta, alpha, beta) parameter tuples for N players.

    "Q" is q_strategy(N) = U(0, pi/N, pi/N), the N-appropriate quantum Nash
    strategy for the GHZ entangler.  Classical strategies D and H are
    N-independent.

    `q_params` overrides what "Q" maps to.  Pass a topology-optimized gate (see
    game.strategy_opt) to evaluate a topology-appropriate quantum strategy
    instead of the fixed GHZ-derived one.  Default None keeps the GHZ behavior,
    so existing callers and the discrete {D,H,Q} sweep are unchanged.
    """
    return {"D": DOVE, "H": HAWK, "Q": q_params if q_params is not None else q_strategy(N)}


def build_payoff_tensor(
    N: int,
    strategy_names: list[str] = STRATEGY_NAMES,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
    q_params: StrategyParams | None = None,
) -> dict[tuple[str, ...], npt.NDArray[np.float64]]:
    """Evaluate all strategy profiles and return per-player payoffs.

    Iterates over all len(strategy_names)^N profiles.  For each profile,
    runs build_ewl_circuit -> expected_payoff.

    "Q" in strategy_names maps to q_strategy(N) = U(0, pi/N, pi/N), unless
    `q_params` overrides it (e.g. a topology-optimized gate from
    game.strategy_opt).

    Returns: dict mapping profile tuple -> shape (N,) payoff array.
    For N=3, strategy_names=["D","H","Q"]: 27 entries.

    Pure-strategy enumeration only.  Does not compute mixed-strategy equilibria.
    """
    smap = _strategy_map(N, q_params)
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
        own_payoffs = tensor[profile]  # hoisted out of the player/alt loops
        deviation = list(profile)  # reused scratch buffer, restored after each player
        is_nash = True
        for player in range(N):
            own = own_payoffs[player]
            for alt in strategy_names:
                if alt == profile[player]:
                    continue
                deviation[player] = alt
                dev_payoff = tensor[tuple(deviation)][player]
                if dev_payoff > own + 1e-9:
                    is_nash = False
                    break
            deviation[player] = profile[player]  # restore for the next player
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
    q_params: StrategyParams | None = None,
) -> dict[str, Any]:
    """Compute quantum advantage: quantum NE payoff vs classical NE payoff (RQ1).

    `q_params` overrides the strategy "Q" maps to (default: the GHZ-derived
    q_strategy(N)).  Pass a topology-optimized gate from game.strategy_opt to
    measure the advantage of the topology's OWN best quantum strategy rather
    than the fixed GHZ one.  Default None is byte-identical to prior behavior.

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

    Per-player reporting: payoffs are reported per player so that asymmetric
    topologies (e.g. star: hub vs spoke) are handled correctly.  The scalar
    keys are the mean over players; for symmetric topologies (GHZ, ring,
    fully-connected) the mean equals every player's payoff, so the scalars are
    identical to the pre-Month-3 values (backward compatible).  The `symmetric`
    flag reports whether the (Q,...,Q) profile and the selected classical NE
    are symmetric across players.

    Classical NE selection when multiple exist: the profile with the highest
    mean per-player payoff (most conservative advantage estimate).

    If no classical NE are found: classical_ne_payoff is NaN; flag and investigate.

    The (Q,...,Q) payoff is a SIMULATION RESULT, not an assumed value.
    If advantage <= 0 or q_is_nash is False, this is a finding about RQ1 --
    do not treat it as a bug.

    Returns dict with keys:
      q_payoff_per_player     float  -- mean per-player payoff at (Q,...,Q)
      q_payoff_vector         list   -- shape (N,) per-player payoff at (Q,...,Q)
      classical_ne_payoff     float  -- mean per-player payoff at the best classical NE
      classical_ne_payoff_vector list-- shape (N,) per-player payoff at that NE
      advantage               float  -- mean q_payoff - mean classical_ne_payoff
      advantage_vector        list   -- shape (N,) per-player advantage
      symmetric               bool   -- whether reported profiles are player-symmetric
      q_is_nash               bool   -- whether (Q,...,Q) is a pure NE
      all_pure_nash           list   -- all pure NE in strategy_names^N
      classical_nash_profiles list   -- pure NE of the restricted classical game
      deviation_check         dict   -- per-(player, alt) unilateral deviation
                                        from (Q,...,Q): payoff and dominance flag
    """
    tensor = build_payoff_tensor(N, strategy_names, V, C, entangler, gamma, q_params)
    all_nash = find_pure_nash(tensor, N, strategy_names)

    def _is_symmetric(vec: npt.NDArray[np.float64]) -> bool:
        return bool(np.allclose(vec, vec[0], atol=1e-8))

    # Classical NE: enumerate NE in the restricted classical-only game {D,H}^N.
    classical_names = [s for s in strategy_names if s != "Q"]
    classical_tensor = {
        p: tensor[p] for p in tensor if all(s in classical_names for s in p)
    }
    classical_nash_profiles = find_pure_nash(classical_tensor, N, classical_names)

    if classical_nash_profiles:
        # Pick the classical NE with the highest mean per-player payoff.
        best_classical = max(
            classical_nash_profiles, key=lambda p: float(np.mean(tensor[p]))
        )
        classical_ne_vector = np.asarray(tensor[best_classical], dtype=np.float64)
        classical_ne_payoff = float(np.mean(classical_ne_vector))
    else:
        classical_ne_vector = np.full(N, np.nan, dtype=np.float64)
        classical_ne_payoff = float("nan")

    q_profile = tuple("Q" for _ in range(N))
    q_payoff_vector = np.asarray(tensor[q_profile], dtype=np.float64)
    q_payoff_per_player = float(np.mean(q_payoff_vector))
    advantage_vector = q_payoff_vector - classical_ne_vector
    advantage = q_payoff_per_player - classical_ne_payoff
    q_is_nash = q_profile in all_nash
    symmetric = _is_symmetric(q_payoff_vector) and (
        not classical_nash_profiles or _is_symmetric(classical_ne_vector)
    )

    deviation_check: dict[tuple[int, str], dict[str, Any]] = {}
    for player in range(N):
        for alt in strategy_names:
            if alt == "Q":
                continue
            dev_profile = list(q_profile)
            dev_profile[player] = alt
            dev_payoff = float(tensor[tuple(dev_profile)][player])
            q_player_payoff = float(q_payoff_vector[player])
            deviation_check[(player, alt)] = {
                "deviation_payoff": dev_payoff,
                "q_payoff": q_player_payoff,
                "q_dominates": dev_payoff <= q_player_payoff + 1e-9,
            }

    return {
        "q_payoff_per_player": q_payoff_per_player,
        "q_payoff_vector": [float(x) for x in q_payoff_vector],
        "classical_ne_payoff": classical_ne_payoff,
        "classical_ne_payoff_vector": [float(x) for x in classical_ne_vector],
        "advantage": advantage,
        "advantage_vector": [float(x) for x in advantage_vector],
        "symmetric": symmetric,
        "q_is_nash": q_is_nash,
        "all_pure_nash": all_nash,
        "classical_nash_profiles": classical_nash_profiles,
        "deviation_check": deviation_check,
    }
