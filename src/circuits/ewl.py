"""EWL protocol: strategy unitary U(theta, alpha, beta), entangling operators
J and J-dagger, and named strategy constants DOVE, HAWK, Q, and q_strategy(N).
"""

from __future__ import annotations

import math
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from qiskit.circuit.library import UnitaryGate

from config import GAMMA

# (theta, alpha, beta) parameters for an SU(2) player strategy
StrategyParams: TypeAlias = tuple[float, float, float]


def U(theta: float, alpha: float, beta: float) -> npt.NDArray[np.complex128]:
    """Return the 2x2 SU(2) strategy unitary for the EWL protocol.

    U(theta, alpha, beta) = [ e^(i*alpha)*cos(theta/2)      i*e^(i*beta)*sin(theta/2)  ]
                            [ i*e^(-i*beta)*sin(theta/2)    e^(-i*alpha)*cos(theta/2)  ]

    Classical mappings:
      DOVE = U(0, 0, 0)        -> Identity
      HAWK = U(pi, 0, 0)       -> i*sigma_X  (global phase i; unobservable in measurement)
      Q    = U(0, pi/2, pi/2)  -> 2-player quantum Nash equilibrium strategy
    """
    c = math.cos(theta / 2)
    s = math.sin(theta / 2)
    return np.array(
        [
            [np.exp(1j * alpha) * c, 1j * np.exp(1j * beta) * s],
            [1j * np.exp(-1j * beta) * s, np.exp(-1j * alpha) * c],
        ],
        dtype=np.complex128,
    )


def J_matrix(gamma: float) -> npt.NDArray[np.complex128]:
    """Return the 4x4 EWL entangling matrix for 2 qubits.

    J(gamma) = exp(i*gamma/2 * X@X)
             = cos(gamma/2)*(I@I) + i*sin(gamma/2)*(X@X)

    At gamma=pi/2: J = (I@I + i*X@X) / sqrt(2)  (maximum entanglement).

    Built from its matrix definition — NOT via RXXGate, which implements
    exp(-i*gamma/2 * X@X) with the opposite sign convention.

    X@X in the 2-qubit computational basis ordered by Qiskit little-endian
    (index i: player j = bit j of i):
      |00> <-> |11>  (indices 0 and 3)
      |01> <-> |10>  (indices 1 and 2)
    """
    c = math.cos(gamma / 2)
    s = math.sin(gamma / 2)
    xx = np.array(
        [
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [1, 0, 0, 0],
        ],
        dtype=np.complex128,
    )
    return c * np.eye(4, dtype=np.complex128) + 1j * s * xx


def make_J_gate(gamma: float = GAMMA) -> UnitaryGate:
    """Return J(gamma) wrapped as a 2-qubit Qiskit UnitaryGate."""
    return UnitaryGate(J_matrix(gamma), label="J")


def make_J_dag_gate(gamma: float = GAMMA) -> UnitaryGate:
    """Return J-dagger(gamma) wrapped as a 2-qubit Qiskit UnitaryGate."""
    return UnitaryGate(J_matrix(gamma).conj().T, label="Jdag")


# Named strategy parameter tuples — pass directly to run_two_player(s0, s1)
DOVE: StrategyParams = (0.0, 0.0, 0.0)
HAWK: StrategyParams = (math.pi, 0.0, 0.0)
Q: StrategyParams = (0.0, math.pi / 2, math.pi / 2)  # N=2 quantum Nash strategy


def q_strategy(N: int) -> StrategyParams:
    """Return the N-player quantum Nash equilibrium strategy Q_N = U(0, pi/N, pi/N).

    Under the J_N(pi/2) entangler (X^(x)N formula), the symmetric strategy that
    collapses the post-J state back to |00...0> after J_dag is the phase-only gate
    U(0, alpha, alpha) with alpha satisfying the condition N * alpha = pi.
    This gives alpha = pi/N, so Q_N = U(0, pi/N, pi/N).

    Derivation sketch:
      J_N(pi/2)|00...0> = (|00...0> + i|11...1>) / sqrt(2)
      Q_N^(x)N maps |00...0> -> (i)^N * e^(i*(N-1)*alpha)|00...0>
                           ...  but the key is the RELATIVE phase:
      Q_N^(x)N on the two-component state:
        |00...0> component gains phase (e^(i*alpha))^N = e^(i*pi) = -1
        |11...1> component gains phase (e^(-i*alpha))^N = e^(-i*pi) = -1
      Both components acquire the same global phase -1, so the state is
      preserved up to global phase, and J_N_dag recovers |00...0>.

    Payoff: all-Dove outcome with probability 1 -> V/N per player.
    This is a Nash equilibrium: any unilateral deviation to D or H yields
    strictly less than V/N (verified numerically by compute_advantage).

    Scales as: N=2 -> U(0, pi/2, pi/2) = Q (the classic EWL result).
               N=3 -> U(0, pi/3, pi/3)
               N=k -> U(0, pi/k, pi/k)

    FINDING (paper-worthy): the quantum Nash strategy scales as pi/N.
    The N=2 strategy Q is not universal — it fails for N>2 under the X^(x)N
    entangler because 2*(pi/2) = pi but 3*(pi/2) ≠ pi. This was discovered
    during Month-2 simulation (simulation result, not prior assumption).
    """
    alpha = math.pi / N
    return (0.0, alpha, alpha)
