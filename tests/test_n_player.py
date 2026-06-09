"""Tests for build_ewl_circuit in n_player.py.

Two correctness guards before the Nash layer is built:
  1. N=2 path reproduces the Month-1 (Q,Q) -> (2,2) result via the new code.
  2. N=3 (D,D,D) profile gives V/N = 4/3 per player.

The N=3 DDD test is analytically exact:
  D = U(0,0,0) = Identity, so each player applies I to their qubit.
  J_3_dag @ (I x I x I) @ J_3 = J_3_dag @ J_3 = I_8.
  Therefore the output state is |000> with probability 1.
  outcome_payoff(0, N=3, V=4, C=3): k=0 Doves, each gets V/N = 4/3.

If the actual value disagrees with 4/3, that indicates a wiring error in
the circuit or payoff function -- execution stops, finding is reported.
"""

from __future__ import annotations

import numpy as np
import numpy.testing as npt

from circuits.ewl import DOVE, Q
from circuits.n_player import build_ewl_circuit
from game.payoffs import expected_payoff

_V, _C = 4.0, 3.0


def test_n2_qq_payoff() -> None:
    """build_ewl_circuit(2, [Q, Q]) must reproduce the Month-1 (Q,Q) -> (2,2) result.

    Confirms the N=2 path through n_player.py is equivalent to the original
    two_player.py implementation.
    """
    probs = build_ewl_circuit(2, [Q, Q])
    payoffs = expected_payoff(probs, N=2, V=_V, C=_C)
    npt.assert_allclose(payoffs, [2.0, 2.0], atol=1e-6)


def test_n3_ddd_payoff() -> None:
    """build_ewl_circuit(3, [D, D, D]) must give [4/3, 4/3, 4/3] per player.

    Analytically exact: D = Identity, J_dag @ J = I, output is |000> w.p. 1,
    Benjamin-Hayden k=0 formula: V/N = 4/3.

    FLAG: if actual != 4/3, this is a circuit or payoff wiring error, not a
    rounding issue -- do not adjust the formula to match the output.
    """
    probs = build_ewl_circuit(3, [DOVE, DOVE, DOVE])
    payoffs = expected_payoff(probs, N=3, V=_V, C=_C)
    expected_per_player = _V / 3.0  # = 4/3
    npt.assert_allclose(payoffs, [expected_per_player] * 3, atol=1e-6,
                        err_msg=f"N=3 DDD payoff should be V/N={expected_per_player:.6f} "
                                f"-- check circuit and payoff wiring, do not adjust formula")
