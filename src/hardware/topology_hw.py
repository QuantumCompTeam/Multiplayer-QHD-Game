"""Topology-parameterised EWL circuits for hardware batches.

`experiments/hardware_scaling.py` hardcodes the GHZ entangler and the all-Q
strategy profile, which is correct for the registered N=3,4,5 scaling batch and
must stay that way so its cross-day repeats remain byte-comparable. The topology
batch needs both as free variables, so the build and its circuit-identity
assertion live here as pure functions and are unit-tested offline (see
tests/test_hardware_topology.py) before any quota is spent.
"""

from __future__ import annotations

import math
from typing import Callable

import numpy as np
import numpy.typing as npt
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

from circuits.ewl import U, q_strategy
from circuits.gate_level import (
    fully_connected_gate_circuit,
    ghz_gate_circuit,
    ring_gate_circuit,
    star_gate_circuit,
    w_gate_circuit,
)
from circuits.topologies import (
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)

GATE_CIRCUITS: dict[str, Callable[..., QuantumCircuit]] = {
    "ghz": ghz_gate_circuit,
    "ring": ring_gate_circuit,
    "star": star_gate_circuit,
    "fully-connected": fully_connected_gate_circuit,
    "w": w_gate_circuit,
}

ENTANGLERS: dict[str, Callable[..., npt.NDArray[np.complex128]]] = {
    "ghz": ghz_entangler,
    "ring": ring_entangler,
    "star": star_entangler,
    "fully-connected": fully_connected_entangler,
    "w": w_entangler,
}


def strategy_matrix(name: str, N: int) -> npt.NDArray[np.complex128]:
    """The 2x2 SU(2) matrix for a discrete strategy label.

    D = Dove = U(0,0,0) = I; H = Hawk = U(pi,0,0); Q = the GHZ-derived
    q_strategy(N) = U(0, pi/N, pi/N). Same definitions the experiment harness
    uses (see experiments/config.yaml, `strategy_names`).
    """
    if name == "D":
        return U(0.0, 0.0, 0.0)
    if name == "H":
        return U(math.pi, 0.0, 0.0)
    if name == "Q":
        return U(*q_strategy(N))
    raise ValueError(f"unknown strategy label {name!r}; expected D, H or Q")


def _resolve_profile(N: int, profile: list[str] | None) -> list[str]:
    if profile is None:
        return ["Q"] * N
    if len(profile) != N:
        raise ValueError(
            f"profile has {len(profile)} entries but N={N}; they must match"
        )
    return list(profile)


def build_ewl_circuit(
    N: int,
    topology: str,
    gamma: float,
    profile: list[str] | None = None,
) -> QuantumCircuit:
    """J . (U_1 x .. x U_N) . J-dagger on N qubits, gate-level.

    `topology` selects the entangler; `profile` selects each player's strategy
    (default all-Q). Mirrors experiments/hardware_scaling.build_ewl_gate_circuit
    with both of its hardcodings lifted.
    """
    names = _resolve_profile(N, profile)
    mats = [strategy_matrix(n, N) for n in names]  # validates labels before build
    J = GATE_CIRCUITS[topology](N, gamma)
    qc = QuantumCircuit(N)
    qc.compose(J, inplace=True)
    for q in range(N):
        qc.append(UnitaryGate(mats[q], label=names[q]), [q])
    qc.compose(J.inverse(), inplace=True)
    return qc


def dense_reference(
    N: int,
    topology: str,
    gamma: float,
    profile: list[str] | None = None,
) -> Operator:
    """The dense J-dagger (U_1 x .. x U_N) J matrix the build must equal."""
    names = _resolve_profile(N, profile)
    # Qiskit is little-endian: a circuit applying U_j to qubit j has dense
    # operator U_{N-1} x .. x U_0, so the kron runs from the HIGHEST qubit down.
    # Symmetric profiles hide this (every factor is equal); deviation profiles
    # do not, which is exactly what the N=3 equilibrium test depends on.
    layer = strategy_matrix(names[N - 1], N)
    for q in range(N - 2, -1, -1):
        layer = np.kron(layer, strategy_matrix(names[q], N))
    J = ENTANGLERS[topology](N, gamma)
    return Operator(J.conj().T @ layer @ J)


def assert_circuit_identity(
    qc: QuantumCircuit,
    N: int,
    topology: str,
    gamma: float,
    profile: list[str] | None = None,
) -> None:
    """Gate 1: raise unless `qc` IS the validated dense unitary."""
    if not Operator(qc).equiv(dense_reference(N, topology, gamma, profile)):
        raise AssertionError(
            f"circuit identity FAILED for topology={topology} N={N} "
            f"profile={_resolve_profile(N, profile)}"
        )


def check_isa_on_set(isa: QuantumCircuit, allowed: set[int], budget: int) -> int:
    """Safety gate: every 2q gate is a cz inside `allowed`, count <= budget.

    Generalises experiments/hardware_scaling.check_isa, which additionally
    required each cz to sit on an ADJACENT pair of one pinned linear chain.
    That extra constraint is GHZ-on-a-line specific: ring, star,
    fully-connected and W all need routing on heavy-hex, so they legitimately
    place cz gates on pairs that are not adjacent in the chain. What still must
    hold is that no gate escaped the pinned qubits and that routing did not blow
    the gate budget. Returns the cz count.
    """
    n_cz = 0
    for ci in isa.data:
        if ci.operation.num_qubits != 2:
            continue
        if ci.operation.name != "cz":
            raise AssertionError(f"unexpected 2q gate {ci.operation.name!r}")
        pair = {isa.find_bit(q).index for q in ci.qubits}
        if not pair <= allowed:
            raise AssertionError(f"cz off the pinned set: {sorted(pair)}")
        n_cz += 1
    if n_cz > budget:
        raise AssertionError(f"cz count {n_cz} exceeds budget {budget} (routing?)")
    return n_cz
