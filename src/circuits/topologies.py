"""Entangling operators for N-qubit EWL circuits.

Each entangler has signature

    (N: int, gamma: float) -> npt.NDArray[np.complex128]

returning the 2^N x 2^N unitary J_N matrix.

Topologies implemented:
  ghz_entangler            -- global X^(x)N entangler (all-to-all GHZ; Month 2)
  ring_entangler           -- pairwise on a cycle graph C_N
  star_entangler           -- pairwise on a star (hub = qubit 0)
  fully_connected_entangler-- pairwise on the complete graph K_N
  w_entangler              -- W-state entangler (cos*I + i*sin*S_W reflection)

Graph-defined topologies (ring, star, fully-connected) are produced by the
factory

    make_pairwise_entangler(G: nx.Graph) -> Entangler

that returns a closure of the same (N, gamma) signature, keeping
build_ewl_circuit's interface stable through Month 6.

Sign convention: all pairwise factors use exp(+i*gamma/2 * X_i X_j) =
cos(gamma/2) I + i sin(gamma/2) X_i X_j, matching J_matrix / ghz_entangler
(NOT Qiskit RXXGate, which uses the opposite sign).  This guarantees every
pairwise entangler reduces to J_matrix(gamma) at N=2 (single edge).
"""

from __future__ import annotations

import math
from functools import lru_cache, reduce
from typing import Callable, TypeAlias

import networkx as nx
import numpy as np
import numpy.typing as npt

from circuits.topology_graphs import topology_graph
from config import GAMMA

# Uniform entangler contract used by build_ewl_circuit and nash.py.
# Graph-based topologies close over their graph inside a factory; the
# signature exposed to callers is always (N, gamma) -> ndarray.
Entangler: TypeAlias = Callable[[int, float], npt.NDArray[np.complex128]]

_I2 = np.eye(2, dtype=np.complex128)
_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)


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
    # X^(x)N has 1s on the anti-diagonal (X^(x)N |i> = |dim-1-i>); fliplr of the
    # identity builds it directly without a Python loop over 2^N rows.
    x_n = np.fliplr(np.eye(dim, dtype=np.complex128))
    c = math.cos(gamma / 2)
    s = math.sin(gamma / 2)
    return c * np.eye(dim, dtype=np.complex128) + 1j * s * x_n


@lru_cache(maxsize=None)
def _pauli_xx(i: int, j: int, N: int) -> npt.NDArray[np.complex128]:
    """N-qubit operator with Pauli-X on qubits i and j, identity elsewhere.

    Qiskit little-endian convention: qubit q corresponds to bit q of the basis
    index, so the full operator is the Kronecker product with qubit N-1 as the
    leftmost (most-significant) factor.  At N=2 with (i, j) = (0, 1) this yields
    X (x) X, matching J_matrix's XX block exactly.

    Memoised on (i, j, N): fully_connected_entangler builds N(N-1)/2 of these per
    construction, so caching avoids rebuilding identical 2^N Kronecker products.
    Callers treat the result as read-only (every use multiplies it into a fresh
    array), so the shared cached instance is safe.
    """
    ops = [_I2] * N
    ops[i] = _X
    ops[j] = _X
    # Little-endian: highest qubit index is the leftmost Kronecker factor.
    return reduce(np.kron, reversed(ops))


def _pairwise_matrix(
    edges: list[tuple[int, int]], N: int, gamma: float
) -> npt.NDArray[np.complex128]:
    """Build the pairwise entangler J = prod_{(i,j) in edges} exp(i*gamma/2 X_i X_j).

    All X_i X_j operators are products of Pauli-X only, hence mutually commute,
    so the product of exponentials equals exp(i*gamma/2 * sum X_i X_j) and is
    order-independent.  Each factor is exact: (X_i X_j)^2 = I, so
    exp(i*gamma/2 X_i X_j) = cos(gamma/2) I + i sin(gamma/2) X_i X_j.
    """
    dim = 2 ** N
    c = math.cos(gamma / 2)
    s = math.sin(gamma / 2)
    eye = np.eye(dim, dtype=np.complex128)
    result = eye.copy()
    for i, j in edges:
        factor = c * eye + 1j * s * _pauli_xx(i, j, N)
        result = factor @ result
    return result


def make_pairwise_entangler(graph: nx.Graph) -> Entangler:
    """Factory: build an Entangler from a graph defining which qubit pairs entangle.

    Returns a closure (N, gamma) -> 2^N x 2^N unitary that entangles every edge
    (i, j) of `graph` via exp(i*gamma/2 X_i X_j).  The closure asserts
    graph.number_of_nodes() == N so the graph's node set matches the circuit
    width; the (N, gamma) signature is preserved so build_ewl_circuit's
    interface does not change.

    Use the ring_entangler / star_entangler / fully_connected_entangler helpers
    below when you want a topology that adapts to N automatically.
    """
    edges = [(int(i), int(j)) for i, j in graph.edges()]
    n_nodes = graph.number_of_nodes()

    def entangler(N: int, gamma: float = GAMMA) -> npt.NDArray[np.complex128]:
        assert n_nodes == N, (
            f"make_pairwise_entangler: graph has {n_nodes} nodes but circuit "
            f"width N={N}. Build the graph for the right N."
        )
        return _pairwise_matrix(edges, N, gamma)

    return entangler


def ring_entangler(N: int, gamma: float = GAMMA) -> npt.NDArray[np.complex128]:
    """Pairwise entangler on the cycle graph C_N (each qubit to two neighbours).

    Reduces to J_matrix(gamma) at N=2 (single edge).  At N=3 the triangle
    C_3 equals K_3, so ring and fully-connected coincide.

    The graph comes from topology_graph("ring", N) -- the same object used by
    the visualization, so what is drawn is exactly what is entangled.
    """
    return make_pairwise_entangler(topology_graph("ring", N))(N, gamma)


def star_entangler(N: int, gamma: float = GAMMA) -> npt.NDArray[np.complex128]:
    """Pairwise entangler on the star graph (hub = qubit 0, N-1 spokes).

    Asymmetric topology: the hub is entangled with every spoke, spokes share no
    direct entanglement.  Player payoffs are NOT symmetric across players, so
    downstream analysis must use per-player reporting (see compute_advantage).
    Reduces to J_matrix(gamma) at N=2 (single edge).
    """
    return make_pairwise_entangler(topology_graph("star", N))(N, gamma)


def fully_connected_entangler(
    N: int, gamma: float = GAMMA
) -> npt.NDArray[np.complex128]:
    """Pairwise entangler on the complete graph K_N (every pair entangled).

    All N(N-1)/2 pairs are entangled via exp(i*gamma/2 X_i X_j).  This is
    distinct from ghz_entangler for N>=3: GHZ uses a single global X^(x)N term,
    while this uses the sum of all pairwise X_i X_j terms.  Reduces to
    J_matrix(gamma) at N=2.
    """
    return make_pairwise_entangler(topology_graph("fully-connected", N))(N, gamma)


def _w_state(N: int) -> npt.NDArray[np.complex128]:
    """Equal-superposition W state: (1/sqrt(N)) sum_j |0...010...0> (excitation on qubit j).

    Single-excitation basis state for qubit j has index 2**j (Qiskit little-endian).
    """
    dim = 2 ** N
    vec = np.zeros(dim, dtype=np.complex128)
    for j in range(N):
        vec[2 ** j] = 1.0
    return vec / math.sqrt(N)


def w_entangler(N: int, gamma: float = GAMMA) -> npt.NDArray[np.complex128]:
    """W-state EWL entangler: J_W(gamma) = cos(gamma/2) I + i sin(gamma/2) S_W.

    S_W is the Hermitian involution that swaps |0...0> with the W state
    |W> = (1/sqrt(N)) sum_j |e_j> and is the identity on the orthogonal
    complement:  S_W = I - |0><0| - |W><W| + |0><W| + |W><0|.
    Since S_W is Hermitian with S_W^2 = I, J_W = exp(i*gamma/2 S_W) is unitary.

    This mirrors the GHZ Option-A construction (cos*I + i*sin*involution).  At
    gamma=pi/2:  J_W |0...0> = (|0...0> + i|W>) / sqrt(2), i.e. equal-magnitude
    amplitude (1/sqrt(2N)) on every single-excitation basis state |2**j>, plus
    a 1/sqrt(2) component on |0...0> -- analogous to GHZ's |0...0> + i|1...1>.

    NOTE: the gamma-interpolation semantics for the W entangler are a design
    choice (the |0...0><->|W> reflection); confirm against the intended physics
    before publishing Month-3 W-state results.
    """
    dim = 2 ** N
    a = np.zeros(dim, dtype=np.complex128)
    a[0] = 1.0  # |0...0>
    b = _w_state(N)  # |W>
    # S_W: swap |a> <-> |b>, identity elsewhere (Hermitian involution).
    s_w = (
        np.eye(dim, dtype=np.complex128)
        - np.outer(a, a.conj())
        - np.outer(b, b.conj())
        + np.outer(a, b.conj())
        + np.outer(b, a.conj())
    )
    c = math.cos(gamma / 2)
    s = math.sin(gamma / 2)
    return c * np.eye(dim, dtype=np.complex128) + 1j * s * s_w
