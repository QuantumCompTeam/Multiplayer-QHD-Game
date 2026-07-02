"""Gate-level entangler validation (Month-4 foundation, spec tests 2 and 8).

The gate-level circuits in circuits/gate_level.py must implement exactly the same
unitary as the dense entanglers in circuits/topologies.py (up to a global phase),
otherwise the noisy path would simulate a different game than the noiseless one.
The dense matrices are authoritative; these tests pin the gate constructions and
the RXX(-gamma) / RZ(-gamma) sign choices against them.
"""

from __future__ import annotations

import pytest
from qiskit.quantum_info import Operator

from config import GAMMA
from experiment.topology_registry import (
    KNOWN_TOPOLOGIES,
    canonical,
    resolve,
    resolve_gate_circuit,
)

_ALL_TOPOLOGIES = ["ghz", "ring", "star", "fully-connected", "w"]


# --- Test 2: gate-level circuit == dense entangler (up to global phase) --------


@pytest.mark.parametrize("topology", _ALL_TOPOLOGIES)
@pytest.mark.parametrize("N", [2, 3, 4])
def test_gate_circuit_matches_dense(topology: str, N: int) -> None:
    """Operator(gate circuit) equals the dense entangler up to a global phase.

    Operator.equiv() is exactly "equal up to global phase" -- it does NOT absorb a
    wrong sign (exp(+i..) vs exp(-i..) are not global-phase related), so this is a
    real guard on the RXX(-gamma)/RZ(-gamma) conventions.
    """
    dense = Operator(resolve(topology, N)(N, GAMMA))
    gate = Operator(resolve_gate_circuit(topology, N, GAMMA))
    assert gate.equiv(dense), (
        f"{topology} N={N}: gate-level circuit does not match dense entangler "
        f"(up to global phase) -- check the RXX/RZ sign convention"
    )


@pytest.mark.parametrize("topology", _ALL_TOPOLOGIES)
def test_gate_circuit_gamma_dependence(topology: str) -> None:
    """A non-max gamma still matches the dense entangler (not just gamma=pi/2)."""
    N, gamma = 3, GAMMA / 2
    dense = Operator(resolve(topology, N)(N, gamma))
    gate = Operator(resolve_gate_circuit(topology, N, gamma))
    assert gate.equiv(dense)


# --- Test 8: registry parity (both views exist for every topology + aliases) ---


def test_registry_parity() -> None:
    """Every known topology resolves in BOTH views; keeps the noisy/noiseless
    paths from drifting (spec D5/4A)."""
    for name in KNOWN_TOPOLOGIES:
        entangler = resolve(name, 3)
        assert callable(entangler)
        circ = resolve_gate_circuit(name, 3, GAMMA)
        assert circ.num_qubits == 3


@pytest.mark.parametrize(
    "alias,expected", [("full", "fully-connected"), ("complete", "fully-connected"),
                       ("fully_connected", "fully-connected"), ("GHZ", "ghz")]
)
def test_aliases_resolve_in_both_views(alias: str, expected: str) -> None:
    """Aliases normalize identically for both the matrix and gate-circuit views."""
    assert canonical(alias) == expected
    assert callable(resolve(alias, 3))
    assert resolve_gate_circuit(alias, 3, GAMMA).num_qubits == 3


def test_unknown_topology_raises_in_both_views() -> None:
    with pytest.raises(ValueError):
        resolve("does-not-exist", 3)
    with pytest.raises(ValueError):
        resolve_gate_circuit("does-not-exist", 3, GAMMA)
