"""Depolarizing-noise tests (Month-4 spec tests 1, 3-7, 9-13; test 2 lives in
tests/test_gate_level.py, test 8 with the registry tests there).

The anchor is test_p0_equals_statevector: at p=0 the density-matrix noisy path must
reproduce the exact statevector result for every topology, proving the gate-level
circuit + transpile pipeline is faithful before any noise physics is trusted.
"""

from __future__ import annotations

import numpy as np
import pytest

from circuits.ewl import DOVE, HAWK, q_strategy
from circuits.n_player import build_ewl_circuit
from circuits.noise import build_ewl_circuit_noisy, build_noise_model
from config import GAMMA, V
from experiment.config import ExperimentConfig, expand_cells
from experiment.plots import extract_pstar
from experiment.report import write_outputs
from experiment.sweep import STATUS_OK, run_sweep
from experiment.topology_registry import resolve
from game.nash import build_payoff_tensor, compute_advantage
from game.payoffs import expected_payoff

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


# --- Test 4: noise does not increase advantage (sanity, not a pinned value) ---


def test_advantage_decays_with_noise() -> None:
    N = 3
    clean = compute_advantage(N=N)
    noisy = compute_advantage(
        N=N,
        prob_fn=lambda n, params: build_ewl_circuit_noisy(
            n, params, topology="ghz", gamma=GAMMA, p=0.05
        ),
    )
    assert noisy["advantage"] <= clean["advantage"] + 1e-9


# --- Test 7: prob_fn injection seam is actually used ---------------------------


def test_prob_fn_injection() -> None:
    N = 2
    # Hand-built distribution: 50% |00> (both Dove), 50% |01> (player 0 Hawk).
    # Payoffs: player 0 = 0.5*(V/2) + 0.5*V = 0.75V; player 1 = 0.5*(V/2) = 0.25V.
    stub_probs = np.array([0.5, 0.5, 0.0, 0.0])
    calls: list[int] = []

    def stub(n: int, params: list) -> np.ndarray:
        calls.append(n)
        return stub_probs

    tensor = build_payoff_tensor(N, prob_fn=stub)
    assert len(calls) == 3**N  # every profile went through the stub
    for payoffs in tensor.values():
        np.testing.assert_allclose(payoffs, [0.75 * V, 0.25 * V])

    # compute_advantage passes the seam through: all profiles identical, so the
    # quantum and classical NE payoffs coincide and the advantage is exactly 0.
    result = compute_advantage(N=N, prob_fn=stub)
    np.testing.assert_allclose(result["advantage"], 0.0, atol=1e-12)


# --- Test 11: expected_payoff input guard (D6) ---------------------------------


def test_expected_payoff_guard() -> None:
    # Wrong shape raises.
    with pytest.raises(ValueError, match="shape"):
        expected_payoff(np.full(3, 1.0 / 3.0), 2)
    # Sum != 1 beyond atol raises.
    with pytest.raises(ValueError, match="normalised"):
        expected_payoff(np.array([0.26, 0.25, 0.25, 0.25]), 2)
    # A tiny negative within atol is clamped; payoff stays finite and matches
    # the clamped distribution.
    tiny = 5e-10
    probs = np.array([-tiny, 0.5, 0.25, 0.25 + tiny])
    payoffs = expected_payoff(probs, 2)
    assert np.isfinite(payoffs).all()
    clamped = np.array([0.0, 0.5, 0.25, 0.25 + tiny])
    np.testing.assert_allclose(payoffs, expected_payoff(clamped, 2))
    # A negative beyond atol is a broken producer: raises, never silently used.
    with pytest.raises(ValueError, match="negative"):
        expected_payoff(np.array([-1e-3, 0.5, 0.25, 0.251]), 2)


# --- Test 5: noise axis end-to-end through the harness -------------------------


def test_noise_axis_end_to_end(tmp_path) -> None:
    raw = {
        "sweep": {"N": [2], "topologies": ["ghz"]},
        "game": {"V": 4.0, "C": 3.0, "gamma": "pi/2"},
        "noise": {"p": [0.0, 0.02]},
    }
    config = ExperimentConfig(
        name="noise-e2e",
        description="Month-4 harness wiring test",
        cells=expand_cells(raw),
        formats=["md", "csv"],
    )
    results = run_sweep(config.cells)
    assert all(r.status == STATUS_OK for r in results), [r.message for r in results]

    run_dir = write_outputs(config, results, tmp_path / "run", "2026-07-02 00:00:00")
    report = (run_dir / "report.md").read_text(encoding="utf-8")
    assert "noise_p" in report
    csv_header = (run_dir / "results.csv").read_text(encoding="utf-8").splitlines()[0]
    assert "noise_p" in csv_header

    # Physics sanity on the two cells: noise must not increase the advantage.
    by_p = {r.cell.noise_p: r for r in results}
    assert by_p[0.02].advantage <= by_p[0.0].advantage + 1e-9


# --- Test 6: p* extraction (pure logic — feeds the published number) -----------


def test_pstar_extraction() -> None:
    # (a) advantage crosses 0 between grid points -> linear interpolation:
    # between (0.01, 0.5) and (0.02, -0.5) the zero crossing is at 0.015.
    assert extract_pstar(
        [0.0, 0.01, 0.02], [1.0, 0.5, -0.5], [True, True, True]
    ) == pytest.approx(0.015)
    # (b) never crosses -> None ("> p_max").
    assert extract_pstar([0.0, 0.01, 0.02], [1.0, 0.8, 0.6], [True, True, True]) is None
    # (c) q_is_nash flips True->False before the advantage crosses -> p* at the
    # flip grid point (a boolean has no in-between to interpolate).
    assert extract_pstar(
        [0.0, 0.01, 0.02], [1.0, 0.5, -0.5], [True, False, True]
    ) == pytest.approx(0.01)
    # A series that was NEVER Nash has nothing to "stop" being: the Nash
    # criterion is inert (that's a Month-3 fixed-mode finding, not noise
    # fragility) and p* comes from the advantage crossing alone.
    assert extract_pstar(
        [0.0, 0.01, 0.02], [1.0, 0.5, -0.5], [False, False, False]
    ) == pytest.approx(0.015)
    # Dead already at the first grid point -> p* is that point.
    assert extract_pstar([0.0, 0.01], [-0.1, -0.2], [True, True]) == pytest.approx(0.0)
    # Unsorted input is sorted internally.
    assert extract_pstar(
        [0.02, 0.0, 0.01], [-0.5, 1.0, 0.5], [True, True, True]
    ) == pytest.approx(0.015)
    # Mismatched lengths are a bug, not a silent misalignment.
    with pytest.raises(ValueError):
        extract_pstar([0.0, 0.01], [1.0], [True, True])


# --- Test 9: noise.p is a sweep axis, backward compatible -----------------------


def test_noise_p_sweep_axis() -> None:
    base = {
        "sweep": {"N": [2], "topologies": ["ghz"]},
        "game": {"V": 4.0, "C": 3.0, "gamma": "pi/2"},
    }
    # No noise key -> identical expansion to before, noise_p defaults to 0.0.
    cells = expand_cells(base)
    assert len(cells) == 1
    assert cells[0].noise_p == 0.0
    # A list is a sweep axis: 3 p values -> 3x the cells.
    swept = expand_cells({**base, "noise": {"p": [0.0, 0.01, 0.02]}})
    assert len(swept) == 3
    assert sorted(c.noise_p for c in swept) == [0.0, 0.01, 0.02]
    # A scalar is a single fixed point.
    scalar = expand_cells({**base, "noise": {"p": 0.02}})
    assert len(scalar) == 1
    assert scalar[0].noise_p == 0.02
    # Out-of-range p is rejected at config load, not at run time.
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        expand_cells({**base, "noise": {"p": [-0.1]}})


# --- Test 10: noise requires strategy_mode "fixed" (D4) -------------------------


def test_noise_requires_fixed_mode() -> None:
    raw = {
        "sweep": {"N": [2], "topologies": ["ghz"], "strategy_mode": "nash"},
        "game": {"V": 4.0, "C": 3.0, "gamma": "pi/2"},
        "noise": {"p": [0.02]},
    }
    with pytest.raises(ValueError, match="fixed"):
        expand_cells(raw)
    # p = 0 with a non-fixed mode stays valid (the exact path is used).
    assert len(expand_cells({**raw, "noise": {"p": [0.0]}})) == 1
    # Fixed mode with noise is the supported Month-4 combination.
    raw["sweep"]["strategy_mode"] = "fixed"
    assert len(expand_cells(raw)) == 1


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
