"""Unit tests for EWL strategy unitary U and entangling matrix J."""

import numpy as np
import numpy.typing as npt

from circuits.ewl import J_matrix, Q, U, q_strategy
from config import GAMMA

SIGMA_X: npt.NDArray[np.complex128] = np.array(
    [[0, 1], [1, 0]], dtype=np.complex128
)


def test_dove_is_identity() -> None:
    """U(0,0,0) must equal the 2x2 identity (Dove = no action)."""
    assert np.allclose(U(0.0, 0.0, 0.0), np.eye(2, dtype=np.complex128), atol=1e-10)


def test_hawk_is_i_sigma_x() -> None:
    """U(pi,0,0) = i*sigma_X per the README formula.

    The global phase i is unobservable in measurement outcomes.
    Elementwise: U[0,1] = i, U[1,0] = i, U[0,0] = U[1,1] = 0.
    """
    assert np.allclose(U(np.pi, 0.0, 0.0), 1j * SIGMA_X, atol=1e-10)


def test_J_is_unitary() -> None:
    """J(gamma) must satisfy J @ J_dag = I_4 (unitary operator)."""
    jm = J_matrix(GAMMA)
    assert np.allclose(jm @ jm.conj().T, np.eye(4, dtype=np.complex128), atol=1e-10)


def test_q_strategy_n2_equals_q() -> None:
    """q_strategy(2) must equal Q = U(0, pi/2, pi/2) exactly.

    This is the core backward-compatibility assertion: the N-player formula
    reduces to the existing 2-player constant at N=2.  Both are computed as
    (0.0, math.pi/2, math.pi/2) so the comparison is exact float equality.
    """
    assert q_strategy(2) == Q, (
        f"q_strategy(2)={q_strategy(2)} != Q={Q}; "
        "the N-player generalisation broke backward compatibility"
    )
