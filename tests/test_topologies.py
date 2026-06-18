"""Tests for entangling operators in topologies.py.

All assertions are against the X^(x)N formula (Option A).  In particular the
N=3 state test asserts (|000> + i|111>) / sqrt(2), NOT the real-valued GHZ
state (|000> + |111>) / sqrt(2) -- the latter would require Option B (H+CNOT),
which does not reduce to J_matrix at N=2.
"""

from __future__ import annotations

import math

import numpy as np
import numpy.testing as npt

from circuits.ewl import J_matrix
from circuits.topologies import (
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)
from config import GAMMA


def test_ghz_n2_matches_j_matrix() -> None:
    """ghz_entangler(2) must equal J_matrix(GAMMA) to machine precision.

    This is the core Option-A guarantee: the N-player formula reduces exactly
    to the Month-1 entangler.  If this fails, the refactor broke the contract.
    """
    npt.assert_allclose(ghz_entangler(2, GAMMA), J_matrix(GAMMA), atol=1e-12)


def test_ghz_n3_state_from_zero() -> None:
    """J_3(pi/2) |000> = (|000> + i|111>) / sqrt(2).

    Index 0 = |000> (all Dove); index 7 = |111> = 0b111 (all Hawk),
    Qiskit little-endian: bit j of index i encodes player j's action.
    """
    j3 = ghz_entangler(3, GAMMA)
    e_000 = np.zeros(8, dtype=np.complex128)
    e_000[0] = 1.0
    result = j3 @ e_000

    expected = np.zeros(8, dtype=np.complex128)
    expected[0] = 1.0 / math.sqrt(2)
    expected[7] = 1j / math.sqrt(2)

    npt.assert_allclose(result, expected, atol=1e-10)


def test_ghz_n2_is_unitary() -> None:
    j2 = ghz_entangler(2, GAMMA)
    npt.assert_allclose(j2 @ j2.conj().T, np.eye(4, dtype=np.complex128), atol=1e-12)


def test_ghz_n3_is_unitary() -> None:
    j3 = ghz_entangler(3, GAMMA)
    npt.assert_allclose(j3 @ j3.conj().T, np.eye(8, dtype=np.complex128), atol=1e-12)


# --- Month 3: pairwise topology entanglers -------------------------------

_PAIRWISE = [ring_entangler, star_entangler, fully_connected_entangler]


def test_pairwise_unitary() -> None:
    """Every pairwise topology is unitary at N=2,3,4."""
    for entangler in _PAIRWISE:
        for N in (2, 3, 4):
            j = entangler(N, GAMMA)
            dim = 2 ** N
            npt.assert_allclose(
                j @ j.conj().T,
                np.eye(dim, dtype=np.complex128),
                atol=1e-12,
                err_msg=f"{entangler.__name__} not unitary at N={N}",
            )


def test_pairwise_n2_matches_j_matrix() -> None:
    """At N=2 every pairwise topology is the single edge (0,1) == J_matrix."""
    for entangler in _PAIRWISE:
        npt.assert_allclose(
            entangler(2, GAMMA),
            J_matrix(GAMMA),
            atol=1e-12,
            err_msg=f"{entangler.__name__}(2) must equal J_matrix(GAMMA)",
        )


def test_fully_connected_differs_from_ghz_n3() -> None:
    """FC (sum of pairwise X_iX_j) must NOT coincide with GHZ (single X^(x)N) at N=3.

    Guards against accidentally re-deriving the global GHZ entangler.
    """
    fc3 = fully_connected_entangler(3, GAMMA)
    ghz3 = ghz_entangler(3, GAMMA)
    assert not np.allclose(fc3, ghz3, atol=1e-9)


def test_ring_equals_fully_connected_n3() -> None:
    """At N=3 the cycle C_3 equals the complete graph K_3 (triangle)."""
    npt.assert_allclose(
        ring_entangler(3, GAMMA), fully_connected_entangler(3, GAMMA), atol=1e-12
    )


def test_w_unitary() -> None:
    for N in (3, 4):
        j = w_entangler(N, GAMMA)
        dim = 2 ** N
        npt.assert_allclose(
            j @ j.conj().T, np.eye(dim, dtype=np.complex128), atol=1e-12
        )


def test_w_state_structure_at_max_entanglement() -> None:
    """w_entangler(N, pi/2)|0...0> = (|0...0> + i|W>)/sqrt(2).

    Single-excitation indices (2**j for j in range(N)) carry equal magnitude
    1/sqrt(2N); the all-zero index carries 1/sqrt(2); all else ~0.
    """
    for N in (3, 4):
        dim = 2 ** N
        e0 = np.zeros(dim, dtype=np.complex128)
        e0[0] = 1.0
        result = w_entangler(N, GAMMA) @ e0

        expected = np.zeros(dim, dtype=np.complex128)
        expected[0] = 1.0 / math.sqrt(2)
        for j in range(N):
            expected[2 ** j] += 1j / math.sqrt(2 * N)
        npt.assert_allclose(result, expected, atol=1e-10)
