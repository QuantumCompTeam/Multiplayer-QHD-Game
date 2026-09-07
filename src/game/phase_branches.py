"""GHZ cooperative phase branches; the historical q_strategy is unchanged."""
from __future__ import annotations

import math

from circuits.ewl import StrategyParams


def phase_strategy(N: int, m: int = 1) -> StrategyParams:
    """Return Q_(N,m); integer branches are equivalent modulo N up to phase."""
    if not isinstance(N, int) or N < 2:
        raise ValueError("N must be an integer >= 2")
    if not isinstance(m, int):
        raise ValueError("m must be an integer")
    alpha = (m % N) * math.pi / N
    return 0.0, alpha, alpha


def incentive_phase_strategy(N: int) -> StrategyParams:
    """Branch nearest pi/2; ideal strict {D,H,Qstar} NE at gamma=pi/2."""
    return phase_strategy(N, N // 2)


def branch_predictions(N: int, m: int, gamma: float = math.pi / 2,
                       V: float = 4.0, C: float = 3.0) -> dict[str, float]:
    """Analytic unilateral incentives, not a noisy or unrestricted NE claim."""
    _, alpha, _ = phase_strategy(N, m)
    if not all(math.isfinite(v) for v in (gamma, V, C)) or V <= 0 or C <= 0:
        raise ValueError("finite gamma and positive finite V,C required")
    t = math.sin(gamma)**2 * math.sin(alpha)**2
    coop = V / N
    hawk = V * (1 - t)
    dove = coop - C * t / N
    return {"alpha": alpha, "cooperative": coop, "hawk": hawk, "dove": dove,
            "hawk_gap": coop - hawk, "dove_gap": coop - dove,
            "restricted_margin": min(coop - hawk, coop - dove),
            "su2_best_payoff": V, "su2_gain": V - coop}


def counter_strategy(N: int, m: int) -> StrategyParams:
    """Unrestricted witness yielding the sole-Hawk outcome at any gamma."""
    return math.pi, 0.0, -phase_strategy(N, m)[1]
