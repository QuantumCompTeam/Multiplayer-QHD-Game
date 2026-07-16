"""Unit tests for src/hardware: readout mitigation, ZNE, chain selection.

All tests are synthetic/offline -- no backend, no network. They pin the pure
math the hardware-scaling pipeline (experiments/hardware_scaling.py) relies on
before any quota is spent.
"""

from __future__ import annotations

import numpy as np
import pytest

from hardware.chain import best_linear_chain
from hardware.mitigation import (
    confusion_from_counts,
    counts_to_probs,
    mitigate_probs,
    tensored_confusion,
    zne_extrapolate,
)


# --- counts -> probs bit convention -------------------------------------------


def test_counts_to_probs_little_endian() -> None:
    """'011' (MSB-left) means qubit0=1, qubit1=1, qubit2=0 -> index 3."""
    probs = counts_to_probs({"011": 3, "100": 1}, 3)
    assert probs[int("011", 2)] == pytest.approx(0.75)
    assert probs[int("100", 2)] == pytest.approx(0.25)
    assert probs.sum() == pytest.approx(1.0)


# --- readout mitigation round-trip --------------------------------------------


def _apply_confusion(
    p_true: np.ndarray, mats: list[np.ndarray]
) -> np.ndarray:
    return tensored_confusion(mats) @ p_true


def test_confusion_from_counts_recovers_error_rates() -> None:
    """Synthetic calibration counts with known eps recover A_j exactly."""
    n, shots = 2, 10000
    # qubit0: P(1|0)=0.02; qubit1: P(1|0)=0.05  (cal0 counts, MSB-left keys)
    cal0 = {
        "00": int(shots * 0.98 * 0.95),
        "01": int(shots * 0.02 * 0.95),  # qubit0 flipped
        "10": int(shots * 0.98 * 0.05),  # qubit1 flipped
        "11": int(shots * 0.02 * 0.05),
    }
    # qubit0: P(0|1)=0.04; qubit1: P(0|1)=0.03
    cal1 = {
        "11": int(shots * 0.96 * 0.97),
        "10": int(shots * 0.04 * 0.97),
        "01": int(shots * 0.96 * 0.03),
        "00": int(shots * 0.04 * 0.03),
    }
    mats = confusion_from_counts(cal0, cal1, n)
    assert mats[0][1, 0] == pytest.approx(0.02, abs=1e-3)  # P(1|0) qubit0
    assert mats[0][0, 1] == pytest.approx(0.04, abs=1e-3)  # P(0|1) qubit0
    assert mats[1][1, 0] == pytest.approx(0.05, abs=1e-3)
    assert mats[1][0, 1] == pytest.approx(0.03, abs=1e-3)
    for m in mats:  # columns are probability distributions
        assert np.allclose(m.sum(axis=0), 1.0)


@pytest.mark.parametrize("n", [3, 5])
def test_mitigation_round_trip(n: int) -> None:
    """mitigate(A @ p_true) == p_true for a known confusion A."""
    rng = np.random.default_rng(7)
    p_true = rng.random(2**n)
    p_true /= p_true.sum()
    mats = [
        np.array([[1 - e0, e1], [e0, 1 - e1]])
        for e0, e1 in zip(
            rng.uniform(0.005, 0.03, n), rng.uniform(0.01, 0.05, n)
        )
    ]
    p_meas = _apply_confusion(p_true, mats)
    p_fix = mitigate_probs(p_meas, mats)
    assert np.allclose(p_fix, p_true, atol=1e-5)
    assert p_fix.sum() == pytest.approx(1.0, abs=1e-9)
    assert (p_fix >= -1e-12).all()


# --- ZNE extrapolation ----------------------------------------------------------


def test_zne_linear_recovers_intercept() -> None:
    """Exact linear decay y = 2.0 - 0.1*lambda -> intercept 2.0 at lambda=0."""
    z = zne_extrapolate([1, 3, 5], [1.9, 1.7, 1.5])
    assert z["linear"] == pytest.approx(2.0, abs=1e-12)
    assert z["richardson"] == pytest.approx(2.0, abs=1e-12)
    assert z["linear_slope"] == pytest.approx(-0.1, abs=1e-12)


def test_zne_richardson_exact_on_quadratic() -> None:
    """Richardson (exact polynomial) nails a quadratic that linear misses."""
    f = lambda lam: 1.0 - 0.05 * lam - 0.01 * lam**2  # noqa: E731
    z = zne_extrapolate([1, 3, 5], [f(1), f(3), f(5)])
    assert z["richardson"] == pytest.approx(1.0, abs=1e-12)
    assert z["linear"] != pytest.approx(1.0, abs=1e-4)  # linear is biased here


def test_zne_weighted_fit_uses_sigmas() -> None:
    """A wildly uncertain outlier point barely moves the weighted intercept."""
    z = zne_extrapolate([1, 3, 5], [1.9, 1.7, 0.0], sigmas=[0.01, 0.01, 1e6])
    assert z["linear"] == pytest.approx(2.0, abs=1e-3)


# --- chain selection ------------------------------------------------------------


def test_best_linear_chain_picks_lowest_error_path() -> None:
    """Line 0-1-2-3-4-5 with rising edge errors + a lure branch: best = [0..4]."""
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (2, 6)]
    edge_err = {
        frozenset((0, 1)): 0.001,
        frozenset((1, 2)): 0.002,
        frozenset((2, 3)): 0.003,
        frozenset((3, 4)): 0.004,
        frozenset((4, 5)): 0.050,  # makes ...-5 paths expensive
        frozenset((2, 6)): 0.100,  # branch is worse still
    }
    node_err = {q: 0.004 for q in range(7)}
    assert best_linear_chain(edges, edge_err, node_err, 5) == [0, 1, 2, 3, 4]


def test_best_linear_chain_canonical_orientation() -> None:
    """Returned path is oriented with path[0] < path[-1]."""
    edges = [(9, 8), (8, 7), (7, 6), (6, 5)]
    edge_err = {frozenset(e): 0.001 for e in edges}
    node_err = {q: 0.001 for q in range(5, 10)}
    path = best_linear_chain(edges, edge_err, node_err, 5)
    assert path == [5, 6, 7, 8, 9]


def test_best_linear_chain_no_path_raises() -> None:
    with pytest.raises(ValueError):
        best_linear_chain([(0, 1)], {frozenset((0, 1)): 0.1}, {0: 0.1, 1: 0.1}, 5)
