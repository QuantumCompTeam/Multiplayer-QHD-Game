"""Tensored readout-error mitigation and zero-noise extrapolation.

Readout mitigation (M3-style, self-contained -- no mthree dependency in the
pinned env): per-qubit 2x2 confusion matrices are estimated from two
calibration circuits (prepare |0...0> and |1...1>), tensored into the full
2^n x 2^n assignment matrix A, and inverted by constrained least squares
(p >= 0, sum(p) = 1).

Bit ordering follows the project convention (src/config.py): little-endian,
qubit j = bit j of the integer index. Counts keys are Qiskit's MSB-left
bitstrings, so index = int(key, 2) -- identical to the rest of the repo.

ZNE: payoffs measured at odd cz-fold factors (1, 3, 5) are extrapolated to
fold 0 by a weighted linear fit (primary) and Richardson extrapolation
(exact polynomial through all points; secondary).
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from scipy.optimize import minimize


def counts_to_probs(counts: dict[str, int], n: int) -> npt.NDArray[np.float64]:
    """MSB-left bitstring counts -> probability vector, little-endian index."""
    if not isinstance(n, int) or n < 1 or not counts:
        raise ValueError("nonempty counts and a positive integer width are required")
    if any(len(key) != n or set(key)-{'0', '1'} for key in counts):
        raise ValueError("count bitstring width must match the register")
    if any(not isinstance(value, (int, np.integer)) or value < 0 for value in counts.values()):
        raise ValueError("counts must be nonnegative integers")
    shots = sum(counts.values())
    if shots <= 0:
        raise ValueError("counts must contain at least one shot")
    probs = np.zeros(2**n, dtype=np.float64)
    for bitstr, c in counts.items():
        probs[int(bitstr, 2)] += c / shots
    return probs


def confusion_from_counts(
    cal0_counts: dict[str, int], cal1_counts: dict[str, int], n: int
) -> list[npt.NDArray[np.float64]]:
    """Per-qubit confusion matrices A_j from the two calibration circuits.

    A_j[m, t] = P(measure m | true t):
        column t=0 from cal0 (prepared |0...0>), column t=1 from cal1 (|1...1>).
    Assumes uncorrelated (tensored) readout errors -- the standard M3-style
    approximation, exact to first order for these devices.
    """
    p0 = counts_to_probs(cal0_counts, n)
    p1 = counts_to_probs(cal1_counts, n)
    mats: list[npt.NDArray[np.float64]] = []
    for j in range(n):
        bit_j = (np.arange(2**n) >> j) & 1
        e0 = float(p0[bit_j == 1].sum())  # P(measure 1 | true 0)
        e1 = float(p1[bit_j == 0].sum())  # P(measure 0 | true 1)
        mats.append(np.array([[1 - e0, e1], [e0, 1 - e1]], dtype=np.float64))
    return mats


def tensored_confusion(mats: list[npt.NDArray[np.float64]]) -> npt.NDArray[np.float64]:
    """Full 2^n x 2^n assignment matrix.

    Little-endian index (qubit 0 = least-significant bit) means qubit n-1 is the
    most-significant kron factor: A = A_{n-1} (x) ... (x) A_0.
    """
    A = mats[-1]
    for m in reversed(mats[:-1]):
        A = np.kron(A, m)
    return A


def mitigate_probs(
    probs_meas: npt.NDArray[np.float64], mats: list[npt.NDArray[np.float64]]
) -> npt.NDArray[np.float64]:
    """Solve min ||A p - p_meas||^2 subject to p >= 0, sum(p) = 1."""
    A = tensored_confusion(mats)
    dim = len(probs_meas)
    x0, *_ = np.linalg.lstsq(A, probs_meas, rcond=None)
    x0 = np.clip(x0, 0.0, None)
    s = x0.sum()
    x0 = x0 / s if s > 0 else np.full(dim, 1.0 / dim)
    res = minimize(
        lambda x: float(np.sum((A @ x - probs_meas) ** 2)),
        x0,
        method="SLSQP",
        bounds=[(0.0, 1.0)] * dim,
        constraints=[{"type": "eq", "fun": lambda x: float(x.sum()) - 1.0}],
        options={"maxiter": 1000, "ftol": 1e-14},
    )
    result = np.asarray(res.x, dtype=np.float64)
    if (not res.success or not np.isfinite(result).all()
            or result.min() < -1e-9 or abs(result.sum()-1.) > 1e-9):
        raise RuntimeError(f"readout mitigation failed: {res.message}")
    return result


def zne_extrapolate(
    factors: list[int],
    values: list[float],
    sigmas: list[float] | None = None,
) -> dict[str, float]:
    """Extrapolate noisy values measured at cz-fold `factors` to fold 0.

    Returns {"linear": intercept, "linear_stderr": ..., "linear_slope": ...,
    "richardson": exact-polynomial-at-0}. Linear fit is weighted by 1/sigma
    when sigmas are given; stderr comes from the (unscaled) fit covariance.
    """
    x = np.asarray(factors, dtype=np.float64)
    y = np.asarray(values, dtype=np.float64)
    if sigmas is not None:
        w = 1.0 / np.asarray(sigmas, dtype=np.float64)
        coef, cov = np.polyfit(x, y, 1, w=w, cov="unscaled")
    else:
        coef, cov = np.polyfit(x, y, 1, cov=True)

    # Richardson: Lagrange polynomial through all points, evaluated at 0.
    rich = 0.0
    for i in range(len(x)):
        term = y[i]
        for j in range(len(x)):
            if j != i:
                term *= x[j] / (x[j] - x[i])
        rich += term

    return {
        "linear": float(coef[1]),
        "linear_stderr": float(np.sqrt(cov[1, 1])),
        "linear_slope": float(coef[0]),
        "richardson": float(rich),
    }
