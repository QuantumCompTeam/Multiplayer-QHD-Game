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
from circuits.topologies import ghz_entangler
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
