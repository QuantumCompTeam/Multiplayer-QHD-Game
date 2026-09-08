"""Global single-occurrence SU(2) responses for a fixed-channel payoff oracle.

This certifies a response to fixed opponents, not an equilibrium search. A
strategy-dependent compiler/noise path need not define a quadratic oracle.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from circuits.ewl import StrategyParams


def quaternion_params(q: np.ndarray) -> StrategyParams:
    """U(q)=q0 I+i(q1 X+q2 Y+q3 Z), using the repository's convention."""
    q = np.asarray(q, dtype=float)
    if q.shape != (4,) or not np.isfinite(q).all() or np.linalg.norm(q) == 0:
        raise ValueError("a finite nonzero quaternion of shape (4,) is required")
    q = q / np.linalg.norm(q)
    diagonal = np.hypot(q[0], q[3])
    offdiag = np.hypot(q[1], q[2])
    return (float(2*np.arctan2(offdiag, diagonal)),
            float(np.arctan2(q[3], q[0])), float(np.arctan2(-q[2], q[1])))


@dataclass(frozen=True)
class BestResponse:
    params: StrategyParams
    payoff: float
    gain: float
    reconstruction_residual: float
    matrix: np.ndarray


def best_response(payoff: Callable[[StrategyParams], float],
                  baseline: float, *, tolerance: float = 1e-8) -> BestResponse:
    """Reconstruct a 4x4 quadratic form and return its maximizing witness.

Ten fit evaluations, four independent deterministic reconstruction checks and
one witness evaluation. Failure rejects the fixed-quadratic assumption. Finite
checks are diagnostics, not a proof that an arbitrary supplied oracle is quadratic.
    """
    if not np.isfinite(baseline) or not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("finite baseline and positive tolerance required")
    basis = np.eye(4)
    matrix = np.zeros((4, 4))
    for i in range(4):
        matrix[i, i] = payoff(quaternion_params(basis[i]))
    for i in range(4):
        for j in range(i+1, 4):
            value = payoff(quaternion_params((basis[i]+basis[j])/np.sqrt(2)))
            matrix[i, j] = matrix[j, i] = value-(matrix[i,i]+matrix[j,j])/2
    if not np.isfinite(matrix).all():
        raise ValueError("nonfinite payoff oracle")
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    witness = eigenvectors[:, -1]
    params = quaternion_params(witness)
    actual = float(payoff(params))
    residual = abs(actual-float(eigenvalues[-1]))
    for q in np.array([[1,2,3,4], [-2,1,4,-3], [3,-4,1,2], [4,3,-2,1]], float):
        q /= np.linalg.norm(q)
        checked = float(payoff(quaternion_params(q)))
        if not np.isfinite(checked):
            raise ValueError("nonfinite payoff oracle at independent reconstruction check")
        residual = max(residual, abs(checked-float(q@matrix@q)))
    if not np.isfinite(actual) or not np.isfinite(residual) or residual > tolerance:
        raise ValueError(f"payoff oracle failed quadratic reconstruction: {residual:.3g}")
    return BestResponse(params, actual, max(0.0, actual-baseline), residual, matrix)
