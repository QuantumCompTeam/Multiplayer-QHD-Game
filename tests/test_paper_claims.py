import itertools
import math
from pathlib import Path

import networkx as nx
import numpy as np
import pytest
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Operator
from scipy.linalg import expm

from circuits.ewl import DOVE, HAWK, U, q_strategy
from circuits.n_player import build_ewl_circuit
from circuits.topologies import (
    fully_connected_entangler,
    ghz_entangler,
    make_pairwise_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)
from circuits.topology_graphs import topology_graph
from game.payoffs import expected_payoff, outcome_payoff


def _piecewise_entry(bits, j, N, V, C):
    k = sum(bits)
    if k == 0:
        return V / N
    if k == N:
        return (V - C) / N
    return V / k if bits[j] == 1 else 0.0


@pytest.mark.parametrize("N", range(2, 8))
def test_payoff_tensor_matches_piecewise_formula_exhaustively(N):
    V, C = 4.0, 3.0
    for outcome in range(2**N):
        bits = [(outcome >> j) & 1 for j in range(N)]
        payoff = outcome_payoff(outcome, N, V, C)
        for j in range(N):
            assert payoff[j] == pytest.approx(
                _piecewise_entry(bits, j, N, V, C)
            ), f"outcome {outcome:0{N}b}, player {j}"


@pytest.mark.parametrize("N", range(2, 9))
def test_total_welfare_identity_for_every_basis_state(N):
    V, C = 4.0, 3.0
    for outcome in range(2**N):
        expected_total = V - C if outcome == 2**N - 1 else V
        assert outcome_payoff(outcome, N, V, C).sum() == pytest.approx(expected_total)


@pytest.mark.parametrize("N", range(2, 9))
def test_hawk_strictly_dominates_dove_for_live_parameters(N):
    V, C = 4.0, 3.0
    # Against every count m of Hawks among the other N-1 players,
    # playing Hawk must strictly beat playing Dove.
    for m in range(N):
        others = (1 << m) - 1          # m Hawks in the lowest other-player slots
        hawk_outcome = (others << 1) | 1
        dove_outcome = others << 1
        hawk_pay = outcome_payoff(hawk_outcome, N, V, C)[0]
        dove_pay = outcome_payoff(dove_outcome, N, V, C)[0]
        assert hawk_pay > dove_pay, f"m={m}"


@pytest.mark.parametrize("N", range(2, 8))
def test_expected_mean_depends_only_on_all_hawk_probability(N):
    rng = np.random.default_rng(N)
    probs = rng.dirichlet(np.ones(2**N))
    payoff = expected_payoff(probs, N, 4.0, 3.0)
    predicted_mean = 4.0 / N - 3.0 * probs[-1] / N
    assert payoff.mean() == pytest.approx(predicted_mean)


# --- III-F: GHZ cooperative fixed profile (Q_N, ..., Q_N) ---------------------


def _assert_ghz_cooperative_benchmark_contract(text):
    heading = r"\subsection{GHZ Cooperative Benchmark}"
    start = text.index(heading)
    end = text.index(r"\subsection{", start + len(heading))
    block = text[start:end]
    compact = "".join(block.split()).replace("&", "").replace(r"\,", "")
    prose = " ".join(block.split())

    assert r"\begin{proposition}[Cooperative invariance in the entanglement angle]" in block
    assert r"Forevery$\gamma$" in compact
    assert block.count(r"\begin{proof}") == 1
    assert block.count(r"\end{proof}") == 1
    proof_start = block.index(r"\begin{proof}")
    proof_end = block.index(r"\end{proof}", proof_start) + len(r"\end{proof}")
    proof = block[proof_start:proof_end]
    proof_compact = "".join(proof.split()).replace("&", "").replace(r"\,", "")
    ordered_proof_fragments = [
        r"J_{\mathrm{GHZ}}(\gamma)\ket{0^N}",
        r"=\cos\!\left(\frac{\gamma}{2}\right)\ket{0^N}",
        r"+i\sin\!\left(\frac{\gamma}{2}\right)\ket{1^N}",
        r"e^{iN\pi/N}=e^{i\pi}=-1",
        r"e^{-iN\pi/N}=e^{-i\pi}=-1",
        r"Q_N^{\otimesN}\ket{0^N}=-\ket{0^N}",
        r"Q_N^{\otimesN}\ket{1^N}=-\ket{1^N}",
        (
            r"Q_N^{\otimesN}J_{\mathrm{GHZ}}(\gamma)\ket{0^N}"
            r"=-J_{\mathrm{GHZ}}(\gamma)\ket{0^N}"
        ),
        (
            r"J_{\mathrm{GHZ}}^\dagger(\gamma)"
            r"\bigl[-J_{\mathrm{GHZ}}(\gamma)\ket{0^N}\bigr]"
            r"=-\ket{0^N}"
        ),
    ]
    for fragment in ordered_proof_fragments:
        assert fragment in proof_compact, f"missing proof fragment: {fragment}"
    positions = [proof_compact.index(fragment) for fragment in ordered_proof_fragments]
    assert positions == sorted(positions), "GHZ phase-cancellation proof steps are out of order"

    assert (
        r"J_{\mathrm{GHZ}}^\dagger(\gamma)Q_N^{\otimesN}"
        r"J_{\mathrm{GHZ}}(\gamma)\ket{0^N}=-\ket{0^N}"
    ) in compact
    assert r"p(0^N)=1" in compact
    assert r"\pi_j=V/N" in compact
    assert r"\Delta_{\mathrm{ana}}=C/N" in compact
    assert r"\textit{Corollary (live parameters).}" in block
    assert r"\pi_j=\frac{4}{N},\qquad\Delta_{\mathrm{ana}}=\frac{3}{N}" in compact
    assert (
        "For the cooperative benchmark, $\\gamma$ is therefore a pure incentive dial: "
        "it can move the deviation incentives characterized in Sec.~\\ref{sec:incentive-boundary} "
        "while leaving the cooperative payoff exactly unchanged."
    ) in prose


def test_ghz_cooperative_benchmark_manuscript_contract():
    text = Path("paper/qhd.tex").read_text(encoding="utf-8")
    _assert_ghz_cooperative_benchmark_contract(text)


@pytest.mark.parametrize("N", range(2, 9))
def test_ghz_q_profile_returns_all_dove(N):
    probs = build_ewl_circuit(
        N,
        [q_strategy(N)] * N,
        entangler=ghz_entangler,
        gamma=math.pi / 2,
    )
    expected = np.zeros(2**N)
    expected[0] = 1.0
    np.testing.assert_allclose(probs, expected, atol=1e-10)


@pytest.mark.parametrize("N", range(2, 8))
@pytest.mark.parametrize("gamma_frac", [0.0, 0.2, 0.4, 0.5])
def test_ghz_cooperative_output_invariant_in_gamma(N, gamma_frac):
    probs = build_ewl_circuit(
        N,
        [q_strategy(N)] * N,
        entangler=ghz_entangler,
        gamma=gamma_frac * math.pi,
    )
    assert probs[0] == pytest.approx(1.0, abs=1e-10)
    assert np.max(np.delete(probs, 0)) < 1e-12


@pytest.mark.parametrize("N", range(2, 9))
def test_ghz_q_profile_payoff_and_analytic_advantage(N):
    probs = build_ewl_circuit(N, [q_strategy(N)] * N)
    payoff = expected_payoff(probs, N, 4.0, 3.0)
    np.testing.assert_allclose(payoff, np.full(N, 4.0 / N), atol=1e-10)
    assert payoff.mean() - 1.0 / N == pytest.approx(3.0 / N)


@pytest.mark.parametrize("N", range(2, 9))
def test_hawk_deviation_matches_closed_form_at_maximal_entanglement(N):
    strategies = [q_strategy(N)] * N
    strategies[0] = HAWK
    probs = build_ewl_circuit(N, strategies, gamma=math.pi / 2)
    payoff = expected_payoff(probs, N, 4.0, 3.0)[0]
    expected = 4.0 * math.cos(math.pi / N) ** 2
    assert payoff == pytest.approx(expected, abs=1e-10)


@pytest.mark.parametrize("N", range(2, 8))
@pytest.mark.parametrize("gamma_frac", [0.0, 0.2, 0.4, 0.5])
def test_dove_deviation_is_non_binding(N, gamma_frac):
    strategies = [q_strategy(N)] * N
    strategies[0] = DOVE  # the U(0,0,0) identity strategy
    probs = build_ewl_circuit(
        N, strategies, entangler=ghz_entangler, gamma=gamma_frac * math.pi
    )
    dev_payoff = expected_payoff(probs, N, 4.0, 3.0)[0]
    assert dev_payoff <= 4.0 / N + 1e-10


# --- III-I: star-orbit payoff-vector covariance -------------------------------


def test_star_payoff_vector_respects_leaf_orbit():
    # Hub is qubit 0; leaves 1 and 2 are in the same automorphism orbit,
    # so under the symmetric Q profile their payoffs must coincide.
    probs = build_ewl_circuit(3, [q_strategy(3)] * 3, entangler=star_entangler)
    payoff = expected_payoff(probs, 3, 4.0, 3.0)
    assert payoff[1] == pytest.approx(payoff[2], abs=1e-10)
    # And the hub is permitted to differ — do NOT assert payoff[0] == payoff[1].


def test_star_entangler_invariant_under_leaf_swap():
    """Conjugating the star unitary by a SWAP of two leaves must leave it fixed.

    star_entangler(N, gamma) hard-codes hub = qubit 0 (topology_graphs.py:
    nx.star_graph(N - 1)) and exposes no hub-choice parameter, so the
    hub-relocation half of the operator-level check (conjugating by a
    hub-leaf SWAP should yield "the star with the relocated hub") cannot be
    built from this constructor alone. Per the task-6 brief, only the
    leaf-exchange invariance is verified here; the limitation is recorded in
    paper/CLAIM-SOURCE-MAP.md.
    """
    N = 4
    gamma = math.pi / 2
    j_op = Operator(star_entangler(N, gamma))

    swap_leaves = QuantumCircuit(N)
    swap_leaves.swap(1, 2)
    swap_op = Operator(swap_leaves)

    conjugated = swap_op.adjoint().compose(j_op).compose(swap_op)
    assert conjugated == j_op


# --- III-J: single unilateral-deviation welfare invariance --------------------


@pytest.mark.parametrize("N", range(2, 9))
def test_single_bit_flip_preserves_total_welfare(N):
    all_dove_total = outcome_payoff(0, N, 4.0, 3.0).sum()
    for player in range(N):
        one_hawk_total = outcome_payoff(1 << player, N, 4.0, 3.0).sum()
        assert one_hawk_total == pytest.approx(all_dove_total)


# --- III-C: strategy unitary, named strategies, and the classical limit -------


def _manuscript_U(theta, alpha, beta):
    """Eq. (5) of paper/qhd.tex, transcribed from the printed matrix."""
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    return np.array(
        [
            [np.exp(1j * alpha) * c, 1j * np.exp(1j * beta) * s],
            [1j * np.exp(-1j * beta) * s, np.exp(-1j * alpha) * c],
        ],
        dtype=np.complex128,
    )


def test_strategy_unitary_matches_manuscript_matrix():
    rng = np.random.default_rng(0)
    for _ in range(200):
        theta, alpha, beta = rng.uniform(-math.pi, math.pi, 3)
        np.testing.assert_allclose(
            _manuscript_U(theta, alpha, beta), U(theta, alpha, beta), atol=1e-12
        )


def test_named_strategies_match_manuscript_definitions():
    assert DOVE == (0.0, 0.0, 0.0)
    assert HAWK == (math.pi, 0.0, 0.0)
    np.testing.assert_allclose(U(*DOVE), np.eye(2), atol=1e-12)
    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    np.testing.assert_allclose(U(*HAWK), 1j * sigma_x, atol=1e-12)


@pytest.mark.parametrize("N", range(2, 9))
def test_q_strategy_is_the_pi_over_n_phase_gate(N):
    assert q_strategy(N) == (0.0, math.pi / N, math.pi / N)
    expected = np.diag([np.exp(1j * math.pi / N), np.exp(-1j * math.pi / N)])
    np.testing.assert_allclose(U(*q_strategy(N)), expected, atol=1e-12)


@pytest.mark.parametrize(
    "entangler",
    [ghz_entangler, w_entangler, ring_entangler, star_entangler,
     fully_connected_entangler],
)
@pytest.mark.parametrize("N", range(3, 6))
def test_entangler_reduces_to_identity_at_zero_angle(entangler, N):
    """III-C states J_T(0) = I for every family, so gamma=0 is the classical game."""
    np.testing.assert_allclose(entangler(N, 0.0), np.eye(2**N), atol=1e-12)


# --- III-D: entangler families, edge sets, and graph symmetry -----------------
#
# These guard the printed operator definitions of Sec. III-D against the
# implementation. Unitarity of every family, the N=2 single-edge reduction, and
# the C_3 = K_3 identity are already covered by tests/test_topologies.py and are
# referenced rather than duplicated here.

_I2 = np.eye(2, dtype=np.complex128)
_PAULI_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
_III_D_GAMMAS = [0.0, 0.3, math.pi / 4, math.pi / 2, 1.9]


def _kron_all(ops):
    out = np.array([[1.0 + 0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


def _xx(r, s, N):
    """X_r X_s in the little-endian convention (qubit N-1 is the leftmost factor)."""
    ops = [_I2] * N
    ops[r] = _PAULI_X
    ops[s] = _PAULI_X
    return _kron_all(list(reversed(ops)))


def _permutation_matrix(sigma, N):
    """R_sigma of Sec. III-D: bit r of the input becomes bit sigma(r) of the output."""
    dim = 2**N
    mat = np.zeros((dim, dim), dtype=np.complex128)
    for i in range(dim):
        j = 0
        for r in range(N):
            if (i >> r) & 1:
                j |= 1 << sigma[r]
        mat[j, i] = 1.0
    return mat


@pytest.mark.parametrize("N", range(2, 7))
@pytest.mark.parametrize("gamma", _III_D_GAMMAS)
def test_ghz_entangler_matches_manuscript_formula(N, gamma):
    """Eq. J_GHZ(g) = cos(g/2) I^(x)N + i sin(g/2) X^(x)N, Sec. III-D."""
    expected = math.cos(gamma / 2) * np.eye(2**N) + 1j * math.sin(
        gamma / 2
    ) * _kron_all([_PAULI_X] * N)
    np.testing.assert_allclose(ghz_entangler(N, gamma), expected, atol=1e-12)


def test_manuscript_scopes_cycle_edge_count_at_n2():
    """III-D must distinguish the simple-graph C_2 degeneracy from m_{C_N}=N."""
    manuscript = Path("paper/qhd.tex").read_text(encoding="utf-8")
    assert "For $N\\ge3$, the standard counts are $m_{C_N}=N$" in manuscript
    assert (
        "At $N=2$, $C_2$ degenerates to the single edge $(1,2)$, "
        "so $m_{C_2}=1$" in manuscript
    )
    assert topology_graph("ring", 2).number_of_edges() == 1


@pytest.mark.parametrize("N", range(3, 8))
def test_graph_topology_edge_sets_match_manuscript(N):
    """Sec. III-D's edge sets and the counts m_{C_N}=N, m_{S_N}=N-1, m_{K_N}=N(N-1)/2.

    Player j of the manuscript is qubit j-1 of the implementation, so the
    manuscript's hub (player 1) is qubit 0 here.
    """
    def undirected(graph):
        return sorted(tuple(sorted(e)) for e in graph.edges())

    ring = topology_graph("ring", N)
    assert undirected(ring) == sorted(
        tuple(sorted((j, (j + 1) % N))) for j in range(N)
    )
    assert ring.number_of_edges() == N

    star = topology_graph("star", N)
    assert undirected(star) == sorted((0, j) for j in range(1, N))
    assert star.number_of_edges() == N - 1

    complete = topology_graph("fully-connected", N)
    assert undirected(complete) == sorted(itertools.combinations(range(N), 2))
    assert complete.number_of_edges() == N * (N - 1) // 2

    # GHZ and W carry no edge set: Sec. III-D calls them global constructions.
    for name in ("ghz", "w"):
        glob = topology_graph(name, N)
        assert glob.graph["kind"] == "global"
        assert glob.number_of_edges() == 0


@pytest.mark.parametrize(
    "name, entangler",
    [
        ("ring", ring_entangler),
        ("star", star_entangler),
        ("fully-connected", fully_connected_entangler),
    ],
)
@pytest.mark.parametrize("N", (3, 4, 5))
def test_graph_entangler_is_the_product_of_per_edge_exponentials(name, entangler, N):
    """Eq. J_G(g) = prod_{(r,s) in E(G)} exp(+i g/2 X_r X_s), Sec. III-D.

    The matrix exponential is taken independently of the closed form the
    implementation uses, so this also pins the +i sign convention: the -i
    convention is checked to disagree.
    """
    edges = [tuple(sorted(e)) for e in topology_graph(name, N).edges()]
    for gamma in _III_D_GAMMAS:
        expected = np.eye(2**N, dtype=np.complex128)
        for r, s in edges:
            expected = expm(1j * (gamma / 2) * _xx(r, s, N)) @ expected
        np.testing.assert_allclose(entangler(N, gamma), expected, atol=1e-10)

    gamma = 0.7
    wrong_sign = np.eye(2**N, dtype=np.complex128)
    for r, s in edges:
        wrong_sign = expm(-1j * (gamma / 2) * _xx(r, s, N)) @ wrong_sign
    assert not np.allclose(entangler(N, gamma), wrong_sign, atol=1e-8)


@pytest.mark.parametrize("N", range(2, 7))
def test_w_entangler_matches_manuscript_involution(N):
    """Sec. III-D's S_W and J_W(g) = cos(g/2) I + i sin(g/2) S_W = exp(i g/2 S_W)."""
    dim = 2**N
    zero = np.zeros(dim, dtype=np.complex128)
    zero[0] = 1.0
    w = np.zeros(dim, dtype=np.complex128)
    for j in range(N):
        w[2**j] = 1.0
    w /= math.sqrt(N)

    s_w = (
        np.eye(dim, dtype=np.complex128)
        - np.outer(zero, zero.conj())
        - np.outer(w, w.conj())
        + np.outer(zero, w.conj())
        + np.outer(w, zero.conj())
    )
    np.testing.assert_allclose(s_w, s_w.conj().T, atol=1e-12)
    np.testing.assert_allclose(s_w @ s_w, np.eye(dim), atol=1e-12)

    for gamma in _III_D_GAMMAS:
        expected = math.cos(gamma / 2) * np.eye(dim) + 1j * math.sin(gamma / 2) * s_w
        np.testing.assert_allclose(w_entangler(N, gamma), expected, atol=1e-12)
        np.testing.assert_allclose(
            w_entangler(N, gamma), expm(1j * (gamma / 2) * s_w), atol=1e-10
        )


@pytest.mark.parametrize("name", ("ring", "star", "fully-connected"))
@pytest.mark.parametrize("N", (3, 4, 5))
def test_graph_entangler_permutation_covariance(name, N):
    """Eq. R_sigma J_G R_sigma^dagger = J_{sigma(G)}, Sec. III-D.

    Every permutation is exercised, not only the automorphisms, so this covers
    the star hub relocation that tests/test_paper_claims.py's leaf-SWAP check
    (an automorphism) cannot reach.
    """
    graph = topology_graph(name, N)
    base = make_pairwise_entangler(graph)(N, math.pi / 2)
    for sigma in itertools.permutations(range(N)):
        mat = _permutation_matrix(sigma, N)
        relabelled = nx.relabel_nodes(graph, {r: sigma[r] for r in range(N)}, copy=True)
        np.testing.assert_allclose(
            mat @ base @ mat.conj().T,
            make_pairwise_entangler(relabelled)(N, math.pi / 2),
            atol=1e-10,
        )


@pytest.mark.parametrize("entangler", (ghz_entangler, w_entangler))
@pytest.mark.parametrize("N", (3, 4, 5))
def test_global_entanglers_are_invariant_under_every_permutation(entangler, N):
    """Sec. III-D states GHZ and W are fixed by the full symmetric group."""
    j_op = entangler(N, math.pi / 2)
    for sigma in itertools.permutations(range(N)):
        mat = _permutation_matrix(sigma, N)
        np.testing.assert_allclose(mat @ j_op @ mat.conj().T, j_op, atol=1e-10)


@pytest.mark.parametrize("name", ("ring", "star", "fully-connected"))
@pytest.mark.parametrize("N", (3, 4, 5))
def test_payoff_vector_relabeling_covariance(name, N):
    """Proposition: pi_{sigma(j)}(sigma(G)) = pi_j(G) under a symmetric profile."""
    graph = topology_graph(name, N)
    strategies = [q_strategy(N)] * N

    def payoffs(g):
        probs = build_ewl_circuit(
            N, strategies, entangler=make_pairwise_entangler(g), gamma=math.pi / 2
        )
        return expected_payoff(probs, N, 4.0, 3.0)

    base = payoffs(graph)
    for sigma in itertools.permutations(range(N)):
        relabelled = nx.relabel_nodes(graph, {r: sigma[r] for r in range(N)}, copy=True)
        moved = payoffs(relabelled)
        for j in range(N):
            assert moved[sigma[j]] == pytest.approx(base[j], abs=1e-10)
