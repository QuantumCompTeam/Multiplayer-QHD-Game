"""Offline tests for the topology-parameterised hardware batch core.

Everything here runs without network and without quota. The point is that the
circuit identity, the strategy profiles and the ISA safety check are all proven
correct BEFORE any of it is used to build a job that spends QPU time.
"""

import math

import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from circuits.ewl import U, q_strategy
from hardware.topology_hw import (
    ENTANGLERS,
    GATE_CIRCUITS,
    assert_circuit_identity,
    build_ewl_circuit,
    check_isa_on_set,
)

GAMMA = math.pi / 2
TOPOLOGIES = ["ghz", "ring", "star", "fully-connected", "w"]


@pytest.mark.parametrize("topology", TOPOLOGIES)
@pytest.mark.parametrize("N", [3, 4])
def test_build_matches_dense_reference(topology, N):
    """The gate-level build IS J-dagger (U x .. x U) J for every topology."""
    qc = build_ewl_circuit(N, topology, GAMMA)
    assert_circuit_identity(qc, N, topology, GAMMA)  # must not raise


def test_registries_agree_on_keys():
    assert set(GATE_CIRCUITS) == set(ENTANGLERS) == set(TOPOLOGIES)


def test_all_q_profile_is_the_default():
    a = build_ewl_circuit(3, "ghz", GAMMA)
    b = build_ewl_circuit(3, "ghz", GAMMA, profile=["Q", "Q", "Q"])
    assert Operator(a).equiv(Operator(b))


def test_hawk_deviation_differs_from_all_q():
    a = build_ewl_circuit(3, "ghz", GAMMA)
    b = build_ewl_circuit(3, "ghz", GAMMA, profile=["H", "Q", "Q"])
    assert not Operator(a).equiv(Operator(b))


def test_deviation_profile_matches_its_own_dense_reference():
    """A deviation circuit must also be exactly its dense reference.

    This is the assertion that makes the N=3 hardware equilibrium test
    trustworthy: the deviation payoff is only meaningful if the deviation
    circuit is provably the unitary we think it is.
    """
    for profile in (["H", "Q", "Q"], ["Q", "H", "Q"], ["D", "Q", "Q"]):
        qc = build_ewl_circuit(3, "ghz", GAMMA, profile=profile)
        assert_circuit_identity(qc, 3, "ghz", GAMMA, profile=profile)


@pytest.mark.parametrize("topology", TOPOLOGIES)
@pytest.mark.parametrize(
    "profile",
    [["Q", "Q", "Q"], ["H", "Q", "Q"], ["Q", "H", "Q"], ["Q", "Q", "H"],
     ["D", "Q", "Q"], ["H", "D", "Q"]],
)
def test_matches_the_repo_statevector_path(topology, profile):
    """Outcome probabilities must equal the repo's own validated EWL path.

    This is the ground-truth tie-in: circuits.n_player.build_ewl_circuit is what
    the payoff tensor and every simulation result in the paper are built on. If
    the hardware builder ever disagrees with it -- especially on the ASYMMETRIC
    profiles that the qubit-ordering convention makes visible -- the hardware
    numbers would not be comparable to the simulation numbers.
    """
    from circuits.n_player import build_ewl_circuit as sv_build
    from qiskit.quantum_info import Statevector

    from hardware.topology_hw import ENTANGLERS as ENT
    from hardware.topology_hw import strategy_matrix

    N = 3
    params = {"D": (0.0, 0.0, 0.0), "H": (math.pi, 0.0, 0.0),
              "Q": tuple(q_strategy(N))}
    expected = sv_build(N, [params[s] for s in profile],
                        entangler=ENT[topology], gamma=GAMMA)
    got = Statevector(build_ewl_circuit(N, topology, GAMMA, profile)).probabilities()
    assert got == pytest.approx(expected, abs=1e-10)
    # strategy_matrix must agree with the params it claims to encode
    for s in profile:
        assert strategy_matrix(s, N) == pytest.approx(U(*params[s]), abs=1e-12)


def test_profile_length_is_validated():
    with pytest.raises(ValueError, match="profile"):
        build_ewl_circuit(3, "ghz", GAMMA, profile=["Q", "Q"])


def test_unknown_strategy_label_is_rejected():
    with pytest.raises(ValueError, match="unknown strategy"):
        build_ewl_circuit(3, "ghz", GAMMA, profile=["Q", "Q", "X"])


def test_unknown_topology_is_rejected():
    with pytest.raises(KeyError):
        build_ewl_circuit(3, "banana", GAMMA)


def test_assert_circuit_identity_raises_on_a_wrong_circuit():
    """The gate must actually fire -- a mismatched circuit has to be caught."""
    wrong = build_ewl_circuit(3, "ghz", GAMMA, profile=["H", "Q", "Q"])
    with pytest.raises(AssertionError, match="circuit identity FAILED"):
        assert_circuit_identity(wrong, 3, "ghz", GAMMA)  # claims all-Q


# ── check_isa_on_set: the routed-topology safety gate ─────────────────────────


def _cz_circuit(pairs, width=8):
    qc = QuantumCircuit(width)
    for a, b in pairs:
        qc.cz(a, b)
    return qc


def test_counts_cz_on_allowed_qubits():
    qc = _cz_circuit([(1, 2), (2, 3)])
    assert check_isa_on_set(qc, allowed={1, 2, 3}, budget=10) == 2


def test_accepts_cz_on_a_non_chain_adjacent_pair():
    """The whole point of generalising: routed topologies use non-adjacent pairs.

    experiments/hardware_scaling.check_isa would reject (1,3) on chain
    [1,2,3] because they are not neighbours in the chain. Inside a pinned SET
    it is legitimate -- it is what SWAP routing produces.
    """
    qc = _cz_circuit([(1, 3)])
    assert check_isa_on_set(qc, allowed={1, 2, 3}, budget=10) == 1


def test_rejects_cz_off_the_pinned_set():
    qc = _cz_circuit([(1, 2), (2, 7)])
    with pytest.raises(AssertionError, match="off the pinned set"):
        check_isa_on_set(qc, allowed={1, 2, 3}, budget=10)


def test_rejects_non_cz_two_qubit_gate():
    qc = QuantumCircuit(4)
    qc.cx(0, 1)
    with pytest.raises(AssertionError, match="unexpected 2q gate"):
        check_isa_on_set(qc, allowed={0, 1}, budget=10)


def test_rejects_when_over_budget():
    qc = _cz_circuit([(1, 2)] * 11)
    with pytest.raises(AssertionError, match="exceeds budget"):
        check_isa_on_set(qc, allowed={1, 2}, budget=10)


def test_accepts_exactly_at_budget():
    qc = _cz_circuit([(1, 2)] * 10)
    assert check_isa_on_set(qc, allowed={1, 2}, budget=10) == 10


def test_single_qubit_gates_are_ignored():
    qc = QuantumCircuit(4)
    qc.x(0)
    qc.h(1)
    qc.cz(0, 1)
    assert check_isa_on_set(qc, allowed={0, 1}, budget=5) == 1
