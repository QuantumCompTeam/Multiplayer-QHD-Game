"""Topology-adaptive quantum strategy optimization for EWL Hawk-Dove.

The fixed strategy ``q_strategy(N) = U(0, pi/N, pi/N)`` is derived for the GHZ
``X^(x)N`` entangler (see circuits/ewl.py); it is the gate that collapses
``J_N(pi/2)|0...0> = (|0...0> + i|1...1>)/sqrt(2)`` back to ``|0...0>`` after
``J_dag``.  Applied to a different entangler (ring / star / fully-connected / W)
it is no longer the right "miracle move", so the advantage measured with it is a
property of *that fixed strategy on the topology*, not of the topology's own best
quantum play.

This module computes the topology-appropriate symmetric SU(2) strategy directly
from the entangler, in two flavours:

  (A) COOPERATIVE  -- the symmetric gate that maximizes mean per-player payoff.
  (B) NASH         -- a symmetric gate that is a best response to itself
                      (continuous symmetric pure-strategy Nash), found by
                      best-response fixed-point iteration and certified by
                      ``nash_gap`` (the continuous analogue of nash.py's
                      deviation_check).

No new physics: every payoff is one ``build_ewl_circuit`` statevector fed to
``expected_payoff``.  Optimization is over the 3-parameter gate (theta, alpha,
beta), NOT over the 3^N discrete profile grid, so it scales in the same 2^N
statevector cost as the rest of the codebase.

Scope: symmetric (player-identical) strategies.  For vertex-transitive
topologies (GHZ, ring, fully-connected, W) the optimal play is symmetric, so a
symmetric search is exact.  The star is NOT vertex-transitive (hub != leaf): a
symmetric gate is a constrained sub-optimum there, so its Nash result is flagged
``symmetric_caveat=True``.  Recommended N <= 6 (matches expected_payoff's stable
shape contract and the sweep range).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.optimize import minimize

from circuits.ewl import DOVE, HAWK, StrategyParams, q_strategy
from circuits.n_player import build_ewl_circuit
from circuits.topologies import Entangler, ghz_entangler
from config import C as DEFAULT_C, GAMMA, V as DEFAULT_V
from game.payoffs import expected_payoff

# Convergence / certification tolerances.
NASH_TOL = 1e-6  # nash_gap below this certifies a symmetric Nash equilibrium
_FIXPOINT_TOL = 1e-8  # probability-vector L2 change that counts as a fixed point
_MAX_FIXPOINT_ITERS = 20


@dataclass
class StrategyOptResult:
    """Outcome of optimizing a symmetric strategy for one (entangler, N, gamma).

    params            -- (theta, alpha, beta) of the optimized symmetric gate
    payoff_per_player -- mean per-player payoff at the all-`params` profile
    nash_gap          -- max single-player gain from unilateral deviation
                         (<= NASH_TOL means `params` is a symmetric Nash eq.)
    is_nash           -- nash_gap <= NASH_TOL
    converged         -- optimizer/fixed-point reported success
    n_starts          -- number of multi-start initial points used
    mode              -- "cooperative" or "nash"
    symmetric_caveat  -- True when the topology is not vertex-transitive (star),
                         so a symmetric gate is a constrained sub-optimum
    """

    params: StrategyParams
    payoff_per_player: float
    nash_gap: float
    is_nash: bool
    converged: bool
    n_starts: int
    mode: str
    symmetric_caveat: bool = False


# --- payoff backbone ----------------------------------------------------------


def _profile_payoffs(
    profile: list[StrategyParams],
    N: int,
    entangler: Entangler,
    gamma: float,
    V: float,
    C: float,
) -> npt.NDArray[np.float64]:
    """Per-player payoff vector for an explicit N-player parameter profile."""
    probs = build_ewl_circuit(N, profile, entangler=entangler, gamma=gamma)
    return expected_payoff(probs, N, V, C)


def _symmetric_payoff(
    params: StrategyParams,
    N: int,
    entangler: Entangler,
    gamma: float,
    V: float,
    C: float,
) -> float:
    """Mean per-player payoff when all N players play `params`."""
    vec = _profile_payoffs([tuple(params)] * N, N, entangler, gamma, V, C)
    return float(np.mean(vec))


def _deviator_payoff(
    base: StrategyParams,
    dev: StrategyParams,
    player: int,
    N: int,
    entangler: Entangler,
    gamma: float,
    V: float,
    C: float,
) -> float:
    """Payoff to `player` when they play `dev` and everyone else plays `base`."""
    profile = [tuple(base)] * N
    profile[player] = tuple(dev)
    return float(_profile_payoffs(profile, N, entangler, gamma, V, C)[player])


# --- multi-start maximization over a single gate ------------------------------


def _starts(
    seed: int, extra: list[StrategyParams] | None = None, n_random: int = 4
) -> list[StrategyParams]:
    """Initial (theta, alpha, beta) points: analytic anchors + seeded random."""
    anchors: list[StrategyParams] = [DOVE, HAWK, (0.0, math.pi / 2, math.pi / 2)]
    if extra:
        anchors = list(extra) + anchors
    rng = np.random.default_rng(seed)
    randoms = [
        (
            float(rng.uniform(0.0, math.pi)),
            float(rng.uniform(-math.pi, math.pi)),
            float(rng.uniform(-math.pi, math.pi)),
        )
        for _ in range(n_random)
    ]
    return anchors + randoms


def _maximize(
    objective,
    starts: list[StrategyParams],
) -> tuple[StrategyParams, float, bool]:
    """Maximize a scalar objective over (theta, alpha, beta) via multi-start.

    Nelder-Mead (robust, derivative-free) from each start, then an L-BFGS-B
    polish on the best point.  Returns (best_params, best_value, converged).
    """
    neg = lambda x: -objective((float(x[0]), float(x[1]), float(x[2])))  # noqa: E731
    best_x: StrategyParams | None = None
    best_val = -np.inf
    any_success = False
    for s0 in starts:
        res = minimize(neg, np.asarray(s0, dtype=float), method="Nelder-Mead",
                       options={"xatol": 1e-8, "fatol": 1e-11, "maxiter": 2000})
        any_success = any_success or bool(res.success)
        val = -float(res.fun)
        if val > best_val:
            best_val = val
            best_x = (float(res.x[0]), float(res.x[1]), float(res.x[2]))
    assert best_x is not None
    bounds = [(0.0, math.pi), (-math.pi, math.pi), (-math.pi, math.pi)]
    polished = minimize(neg, np.asarray(best_x, dtype=float), method="L-BFGS-B",
                        bounds=bounds)
    if -float(polished.fun) > best_val:
        best_val = -float(polished.fun)
        best_x = (float(polished.x[0]), float(polished.x[1]), float(polished.x[2]))
    return best_x, best_val, any_success


# --- public API ---------------------------------------------------------------


def nash_gap(
    base: StrategyParams,
    N: int,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    *,
    seed: int = 0,
    check_all_players: bool = True,
) -> float:
    """Max gain any single player can get by deviating from the all-`base` profile.

    Continuous analogue of nash.py's deviation_check: for each player position,
    globally maximize that player's payoff (others fixed at `base`) and subtract
    the base payoff.  Return the largest such gain over all positions.  A value
    <= NASH_TOL certifies `base` is a symmetric Nash equilibrium.

    `check_all_players=True` (default) checks every position, so the certificate
    is valid even for asymmetric topologies (e.g. star, where hub and leaf gain
    differently).  For vertex-transitive topologies (GHZ, ring, fully-connected,
    W) every position is equivalent, so callers may pass False to check only
    player 0 — an N-fold speedup with no loss of validity.
    """
    base_vec = _profile_payoffs([tuple(base)] * N, N, entangler, gamma, V, C)
    worst = -np.inf
    starts = _starts(seed, extra=[base])
    players = range(N) if check_all_players else range(1)
    for player in players:
        def dev_obj(p: StrategyParams, _player: int = player) -> float:
            return _deviator_payoff(base, p, _player, N, entangler, gamma, V, C)

        _, best_dev, _ = _maximize(dev_obj, starts)
        worst = max(worst, best_dev - float(base_vec[player]))
    return float(worst)


def cooperative_strategy(
    N: int,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    *,
    seed: int = 0,
    symmetric_caveat: bool = False,
) -> StrategyOptResult:
    """Symmetric gate maximizing mean per-player payoff under `entangler`.

    Warm-started with the analytic GHZ solution q_strategy(N); for the GHZ
    entangler this recovers U(0, pi/N, pi/N) and the cooperative payoff V/N.
    """
    extra = [q_strategy(N)]
    starts = _starts(seed, extra=extra)

    def obj(p: StrategyParams) -> float:
        return _symmetric_payoff(p, N, entangler, gamma, V, C)

    params, payoff, converged = _maximize(obj, starts)
    gap = nash_gap(
        params, N, entangler, gamma, V, C, seed=seed,
        check_all_players=symmetric_caveat,
    )
    return StrategyOptResult(
        params=params,
        payoff_per_player=payoff,
        nash_gap=gap,
        is_nash=gap <= NASH_TOL,
        converged=converged,
        n_starts=len(starts),
        mode="cooperative",
        symmetric_caveat=symmetric_caveat,
    )


def nash_strategy(
    N: int,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    *,
    seed: int = 0,
    symmetric_caveat: bool = False,
) -> StrategyOptResult:
    """Symmetric continuous Nash strategy via best-response fixed-point iteration.

    Hold N-1 players at the current gate U_k, globally best-respond on the
    remaining player to get U_{k+1}, and iterate.  Convergence is judged on the
    INDUCED PROBABILITY VECTORS (gauge-invariant: immune to global-phase and
    (alpha,beta) parameter aliasing).  Several seeds are tried; the candidate
    with the smallest certified nash_gap is returned.
    """
    seeds = [q_strategy(N), DOVE]
    rng = np.random.default_rng(seed)
    seeds += [
        (
            float(rng.uniform(0.0, math.pi)),
            float(rng.uniform(-math.pi, math.pi)),
            float(rng.uniform(-math.pi, math.pi)),
        )
    ]

    best: StrategyOptResult | None = None
    br_starts = _starts(seed, n_random=2)
    for start in seeds:
        current = tuple(start)
        converged = False
        for _ in range(_MAX_FIXPOINT_ITERS):
            def br_obj(p: StrategyParams, _base: StrategyParams = current) -> float:
                return _deviator_payoff(_base, p, 0, N, entangler, gamma, V, C)

            nxt, _, _ = _maximize(br_obj, br_starts + [current])
            cur_probs = build_ewl_circuit(N, [current] * N, entangler=entangler, gamma=gamma)
            nxt_probs = build_ewl_circuit(N, [tuple(nxt)] * N, entangler=entangler, gamma=gamma)
            current = tuple(nxt)
            if float(np.linalg.norm(nxt_probs - cur_probs)) < _FIXPOINT_TOL:
                converged = True
                break
        payoff = _symmetric_payoff(current, N, entangler, gamma, V, C)
        gap = nash_gap(
            current, N, entangler, gamma, V, C, seed=seed,
            check_all_players=symmetric_caveat,
        )
        cand = StrategyOptResult(
            params=current,
            payoff_per_player=payoff,
            nash_gap=gap,
            is_nash=gap <= NASH_TOL,
            converged=converged,
            n_starts=len(seeds),
            mode="nash",
            symmetric_caveat=symmetric_caveat,
        )
        # Prefer a certified Nash; among those, the higher payoff.
        if best is None or (cand.is_nash, cand.payoff_per_player) > (
            best.is_nash, best.payoff_per_player
        ):
            best = cand
    assert best is not None
    return best


def optimal_strategy(
    mode: str,
    N: int,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    *,
    seed: int = 0,
    symmetric_caveat: bool = False,
) -> StrategyOptResult:
    """Dispatch to cooperative_strategy / nash_strategy by `mode`."""
    if mode == "cooperative":
        return cooperative_strategy(
            N, entangler, gamma, V, C, seed=seed, symmetric_caveat=symmetric_caveat
        )
    if mode == "nash":
        return nash_strategy(
            N, entangler, gamma, V, C, seed=seed, symmetric_caveat=symmetric_caveat
        )
    raise ValueError(f"unknown strategy mode {mode!r}; expected 'cooperative' or 'nash'")
