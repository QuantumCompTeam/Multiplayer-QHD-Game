"""Entangling operators for N-qubit EWL circuits.

Each entangler has signature

    (N: int, gamma: float) -> npt.NDArray[np.complex128]

returning the 2^N x 2^N unitary J_N matrix.

Graph-defined topologies (ring, star, fully-connected) will be produced in
Month 3 by a factory

    make_pairwise_entangler(G: nx.Graph) -> Entangler

that returns a closure of the same signature, keeping build_ewl_circuit's
interface stable through Month 6.
"""

from __future__ import annotations

import math
from typing import Callable, TypeAlias

import numpy as np
import numpy.typing as npt

from config import GAMMA

# Uniform entangler contract used by build_ewl_circuit and nash.py.
# Graph-based topologies close over their graph inside a factory; the
# signature exposed to callers is always (N, gamma) -> ndarray.
Entangler: TypeAlias = Callable[[int, float], npt.NDArray[np.complex128]]


def ghz_entangler(N: int, gamma: float = GAMMA) -> npt.NDArray[np.complex128]:
    """J_N(gamma) = cos(gamma/2) * I^(x)N + i * sin(gamma/2) * X^(x)N.

    X^(x)N is the N-fold tensor product of Pauli-X.  Its matrix has 1s on the
    anti-diagonal: X^(x)N |i> = |2^N - 1 - i> (all N bits flipped).

    Reduces to J_matrix(gamma) in ewl.py exactly at N=2 (same formula,
    same sign convention).  Verified by test_ghz_n2_matches_j_matrix.

    At gamma=pi/2, N=3: J_3 |000> = (|000> + i|111>) / sqrt(2).
    The relative phase i on |111> is required by the X^(x)N formula (Option A);
    the real-valued GHZ state (|000> + |111>) / sqrt(2) would be Option B
    (H+CNOT circuit) which does NOT reduce to J_matrix at N=2.
    """
    dim = 2 ** N
    x_n = np.zeros((dim, dim), dtype=np.complex128)
    for i in range(dim):
        x_n[i, dim - 1 - i] = 1.0
    c = math.cos(gamma / 2)
    s = math.sin(gamma / 2)
    return c * np.eye(dim, dtype=np.complex128) + 1j * s * x_n


def w_entangler(N: int, gamma: float = GAMMA) -> npt.NDArray[np.complex128]:  # noqa: ARG001
    """W-state EWL entangler. Implemented in Month 3."""
    raise NotImplementedError("w_entangler is implemented in Month 3")


def make_pairwise_entangler(graph: object) -> Entangler:
    """Factory for ring / star / fully-connected topologies. Implemented in Month 3.

    Returns a closure (N, gamma) -> ndarray so that build_ewl_circuit's
    interface does not change when graph topologies are added.
    """
    raise NotImplementedError("make_pairwise_entangler is implemented in Month 3")
