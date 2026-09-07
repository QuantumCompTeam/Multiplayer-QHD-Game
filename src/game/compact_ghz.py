"""Exact ideal GHZ payoff contraction, polynomial work and no 2**N arrays.

The final state is a sum of four product states. Gauss-Legendre quadrature
integrates the degree N-1 Hawk-count generating polynomials exactly (up to
floating point). This does not simulate gate noise or other entangler families.
"""
from __future__ import annotations

from functools import lru_cache
import math

import numpy as np

from circuits.ewl import StrategyParams, U


@lru_cache(maxsize=32)
def _quadrature(N: int):
    nodes, weights = np.polynomial.legendre.leggauss((N+1)//2)
    return (nodes+1)/2, weights/2


def compact_payoffs(strategies: list[StrategyParams], gamma: float = math.pi/2,
                    V: float = 4.0, C: float = 3.0) -> dict:
    """Return exact ideal payoff vector and endpoint probabilities in O(N^2)."""
    N = len(strategies)
    if N < 2 or not np.isfinite([gamma, V, C]).all():
        raise ValueError("N >= 2 and finite gamma,V,C required")
    gates = np.array([U(*params) for params in strategies])
    if not np.isfinite(gates).all():
        raise ValueError("strategies must be finite")
    a, b = gates[:, :, 0], gates[:, :, 1]
    branches = np.array([a, b, a[:, ::-1], b[:, ::-1]])
    c, s = math.cos(gamma/2), math.sin(gamma/2)
    coefficients = np.array([c*c, 1j*s*c, -1j*s*c, s*s])
    p0 = float(abs(coefficients @ np.prod(branches[:,:,0], axis=1))**2)
    pn = float(abs(coefficients @ np.prod(branches[:,:,1], axis=1))**2)
    integrals = np.zeros(N, complex)
    nodes, weights = _quadrature(N)
    for r in range(4):
        for t in range(4):
            weight = coefficients[r]*coefficients[t].conjugate()
            zero = branches[r,:,0]*branches[t,:,0].conjugate()
            one = branches[r,:,1]*branches[t,:,1].conjugate()
            for z, w in zip(nodes, weights):
                factors = zero + z*one
                prefix = np.concatenate(([1], np.cumprod(factors[:-1])))
                suffix = np.concatenate((np.cumprod(factors[:0:-1])[::-1], [1]))
                integrals += weight*w*one*prefix*suffix
    vector = V*p0/N + V*integrals.real - C*pn/N
    mean = V/N-C*pn/N
    if not np.allclose(vector.mean(), mean, atol=1e-9, rtol=1e-9):
        raise ArithmeticError("compact payoff contraction failed welfare identity")
    return {"payoff_vector": vector, "mean": mean, "p_zero": p0,
            "p_all_hawk": pn, "analytic_advantage": mean-(V-C)/N,
            "representation": "four_product_branches", "N": N}
