"""Payoffs directly from observed bitstrings, including conflict sensitivity.

ell=0 preserves the original game. ell>0 is an explicitly different payoff
model; reweighting observed profiles does not re-establish their equilibria.
"""
from __future__ import annotations

import numpy as np


def outcome_vector(bitstring: str, ell: float = 0., V: float = 4., C: float = 3.) -> np.ndarray:
    if not bitstring or set(bitstring) - {'0','1'} or len(bitstring) < 2:
        raise ValueError("expected a binary string with N >= 2")
    if not 0 <= ell <= 1 or not np.isfinite([V,C]).all() or V <= C or C <= 0:
        raise ValueError("require 0 <= ell <= 1 and finite V > C > 0")
    n = len(bitstring)
    bits = np.array([int(b) for b in reversed(bitstring)])
    k = int(bits.sum())
    if not k:
        return np.full(n, V/n)
    loss = C*((1-ell)*float(k == n) + ell*k*(k-1)/(n*(n-1)))
    return bits*(V-loss)/k


def counts_summary(counts: dict[str, int], ell: float = 0., V: float = 4., C: float = 3.,
                   *, bootstrap: int = 0, seed: int = 0) -> dict:
    """Raw estimators and multinomial uncertainty; no mitigation or NE claim."""
    if not counts or any(not isinstance(v,int) or v < 0 for v in counts.values()):
        raise ValueError("nonempty counts with nonnegative integer frequencies required")
    sizes = {len(k) for k in counts}
    shots = sum(counts.values())
    if len(sizes) != 1 or shots < 2:
        raise ValueError("consistent bitstring width and at least two shots required")
    n = sizes.pop()
    labels = list(counts)
    rewards = np.array([outcome_vector(k,ell,V,C) for k in labels])
    p = np.array([counts[k]/shots for k in labels])
    vector = p @ rewards
    centered = rewards-vector
    covariance = (centered.T * p) @ centered/(shots-1)
    total_reward = rewards.mean(axis=1)
    mean = float(vector.mean())
    mean_se = float(np.sqrt(np.dot(p,(total_reward-mean)**2)/(shots-1)))
    hist = np.zeros(n+1)
    for label, prob in zip(labels,p):
        hist[label.count('1')] += prob
    result = {"N": n, "ell": ell, "shots": shots, "per_player": vector.tolist(),
              "per_player_se": np.sqrt(np.diag(covariance)).tolist(),
              "payoff_covariance": covariance.tolist(), "mean": mean,
              "mean_se": mean_se, "floor": float(vector.min()),
              "spread": float(np.ptp(vector)), "p_zero": float(hist[0]),
              "p_all_hawk": float(hist[-1]), "hawk_count_histogram": hist.tolist(),
              "analytic_advantage": mean-(V-C)/n,
              "retention": (mean-(V-C)/n)/(C/n),
              "uniform_retention": 1-(1-ell)*2.**(-n)-ell/4,
              "uncertainty_scope": "raw multinomial sampling only; excludes calibration drift"}
    if bootstrap:
        draws = np.random.default_rng(seed).multinomial(shots,p,size=bootstrap)/shots
        vectors = draws @ rewards
        result['bootstrap_replicates'] = bootstrap
        result['retention_ci95_pointwise'] = np.quantile(
            (vectors.mean(axis=1)-(V-C)/n)/(C/n), [.025,.975]).tolist()
        result['floor_ci95_pointwise'] = np.quantile(vectors.min(axis=1), [.025,.975]).tolist()
    return result
