"""Gate-level entangler validation (Month-4 foundation, spec tests 2 and 8).

The gate-level circuits in circuits/gate_level.py must implement exactly the same
unitary as the dense entanglers in circuits/topologies.py (up to a global phase),
otherwise the noisy path would simulate a different game than the noiseless one.
The dense matrices are authoritative; these tests pin the gate constructions and
the RXX(-gamma) / RZ(-gamma) sign choices against them.
"""

from __future__ import annotations

import numpy as np
import pytest
from qiskit.quantum_info import Operator, Statevector

from circuits.gate_level import _w_prep_cascade
from circuits.topologies import _w_state
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


# --- T8: W-prep cascade properties (spec D-T8.3) -------------------------------


@pytest.mark.parametrize("N", [2, 3, 4, 5])
def test_w_prep_maps_excitation_to_w_state(N: int) -> None:
    """T|e_0> = |W> EXACTLY (real +1/sqrt(N) amplitudes, not just up to phase).

    Exactness matters: the conjugation J_W = T . MCU . T-dagger needs T to hit
    _w_state on the nose, otherwise S_W's off-diagonal blocks pick up phases.
    """
    sv = Statevector.from_int(1, dims=2**N).evolve(_w_prep_cascade(N))
    np.testing.assert_allclose(sv.data, _w_state(N), atol=1e-12)


@pytest.mark.parametrize("N", [2, 3, 4, 5])
def test_w_prep_fixes_vacuum(N: int) -> None:
    """T|0...0> = |0...0> exactly — every cascade gate is controlled on a |0>.

    This is what makes the conjugation argument exact with no correction terms
    (spec D-T8.3); a drifted vacuum silently corrupts J_W's |0><W| block.
    """
    sv = Statevector.from_int(0, dims=2**N).evolve(_w_prep_cascade(N))
    expected = np.zeros(2**N, dtype=complex)
    expected[0] = 1.0
    np.testing.assert_allclose(sv.data, expected, atol=1e-12)


def test_w_gate_circuit_matches_dense_n5() -> None:
    """Exact W construction at the noise sweep's max N (existing tests stop at 4).

    Operator.equiv is global-phase tolerant but branch-relative-phase strict:
    it catches a missing e^{-i*gamma/2} on the MCU target or a wrong ctrl_state.
    """
    dense = Operator(resolve("w", 5)(5, GAMMA))
    gate = Operator(resolve_gate_circuit("w", 5, GAMMA))
    assert gate.equiv(dense)


@pytest.mark.parametrize("N", [5, 6])
def test_ghz_gate_circuit_matches_dense_large_n(N: int) -> None:
    """GHZ CX-ladder construction at the hardware-scaling Ns (existing stop at 4).

    The Month-5/6 hardware pipeline (experiments/hardware_scaling.py) builds its
    J from ghz_gate_circuit at N up to 5; pin the dense equivalence there (and at
    6 for headroom) so the hardware circuit can never drift from the validated
    entangler.
    """
    dense = Operator(resolve("ghz", N)(N, GAMMA))
    gate = Operator(resolve_gate_circuit("ghz", N, GAMMA))
    assert gate.equiv(dense)
