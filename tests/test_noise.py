"""Depolarizing-noise runner tests (Month-4 spec tests 1, 3, 12, 13).

The anchor is test_p0_equals_statevector: at p=0 the density-matrix noisy path must
reproduce the exact statevector result for every topology, proving the gate-level
circuit + transpile pipeline is faithful before any noise physics is trusted.
(Tests 4/6/7/... that need compute_advantage/prob_fn live with the analysis and
harness tasks.)
"""

from __future__ import annotations

import numpy as np
import pytest

from circuits.ewl import DOVE, HAWK, q_strategy
from circuits.n_player import build_ewl_circuit
from circuits.noise import build_ewl_circuit_noisy, build_noise_model
from config import GAMMA
from experiment.topology_registry import resolve

_ALL_TOPOLOGIES = ["ghz", "ring", "star", "fully-connected", "w"]


def _profiles(N: int) -> list[list[tuple[float, float, float]]]:
    q = q_strategy(N)
    return [
        [DOVE] * N,
        [q] * N,
        [HAWK] + [DOVE] * (N - 1),
    ]


# --- Test 1 (anchor): p=0 noisy == exact statevector --------------------------


@pytest.mark.parametrize("topology", _ALL_TOPOLOGIES)
@pytest.mark.parametrize("N", [2, 3])
def test_p0_equals_statevector(topology: str, N: int) -> None:
    entangler = resolve(topology, N)
    for strategies in _profiles(N):
        exact = build_ewl_circuit(N, strategies, entangler=entangler, gamma=GAMMA)
        noisy0 = build_ewl_circuit_noisy(
            N, strategies, topology=topology, gamma=GAMMA, p=0.0
        )
        np.testing.assert_allclose(
            noisy0, exact, atol=1e-6,
            err_msg=f"{topology} N={N}: p=0 noisy != exact statevector",
        )


# --- Test 3: probabilities stay valid under noise -----------------------------


@pytest.mark.parametrize("p", [0.01, 0.05])
def test_probs_normalized_under_noise(p: float) -> None:
    N = 3
    probs = build_ewl_circuit_noisy(
        N, [q_strategy(N)] * N, topology="ghz", gamma=GAMMA, p=p
    )
    assert probs.shape == (2**N,)
    assert (probs >= -1e-9).all()
    np.testing.assert_allclose(probs.sum(), 1.0, atol=1e-9)


# --- Test 12: noise model attaches to u and cx only ---------------------------


def test_build_noise_model() -> None:
    assert build_noise_model(0.0).noise_instructions == []
    instr = set(build_noise_model(0.05).noise_instructions)
    assert "u" in instr and "cx" in instr
    assert instr <= {"u", "cx"}


# --- Test 13: invalid p raises ------------------------------------------------


@pytest.mark.parametrize("bad_p", [-0.1, 1.5])
def test_noisy_invalid_p(bad_p: float) -> None:
    with pytest.raises(ValueError):
        build_ewl_circuit_noisy(
            2, [DOVE, DOVE], topology="ghz", gamma=GAMMA, p=bad_p
        )
    with pytest.raises(ValueError):
        build_noise_model(bad_p)
