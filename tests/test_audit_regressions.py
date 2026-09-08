"""Failure-path regressions found in the September 8 project audit."""
import itertools
from types import SimpleNamespace

import numpy as np
import pytest

from circuits.ewl import DOVE
from circuits.n_player import build_ewl_circuit
from circuits.noise import build_ewl_circuit_noisy, build_noise_model
from game.best_response import best_response
from game.nash import compute_advantage, find_pure_nash
from game.payoffs import expected_payoff
from game.phase_branches import branch_predictions, phase_strategy, counter_strategy
from game import strategy_opt
from hardware.mitigation import counts_to_probs, mitigate_probs
from hardware.phase_validation import experiment_rows, judge
from experiment.config import expand_cells
import results_io


def test_nan_probabilities_cannot_produce_an_equilibrium():
    with pytest.raises(ValueError, match='finite'):
        compute_advantage(2, prob_fn=lambda n, profile: np.full(2**n, np.nan))


def test_nan_payoff_tensor_cannot_certify_every_profile():
    tensor = {p: np.full(2, np.nan) for p in itertools.product(['D', 'H'], repeat=2)}
    with pytest.raises(ValueError, match='finite'):
        find_pure_nash(tensor, 2, ['D', 'H'])


@pytest.mark.parametrize('parameter', ['V', 'C'])
def test_nonfinite_game_values_rejected(parameter):
    with pytest.raises(ValueError, match='finite'):
        expected_payoff(np.array([1., 0., 0., 0.]), 2, **{parameter: np.nan})


@pytest.mark.parametrize('count', [1, 3])
@pytest.mark.parametrize('noisy', [False, True])
def test_missing_or_extra_player_strategy_is_rejected(count, noisy):
    with pytest.raises(ValueError, match='strateg'):
        if noisy:
            build_ewl_circuit_noisy(2, [DOVE]*count, topology='ghz', p=0.)
        else:
            build_ewl_circuit(2, [DOVE]*count)


@pytest.mark.parametrize('ratio', [-1., np.nan, np.inf])
def test_invalid_two_qubit_noise_ratio_is_rejected(ratio):
    with pytest.raises(ValueError, match='p2_ratio'):
        build_noise_model(.01, ratio)


def test_nan_independent_oracle_check_is_not_ignored():
    calls = 0
    def oracle(params):
        nonlocal calls
        calls += 1
        return np.nan if calls == 12 else 1.
    with pytest.raises(ValueError, match='nonfinite'):
        best_response(oracle, 1.)


@pytest.mark.parametrize('tolerance', [np.nan, np.inf])
def test_nonfinite_response_tolerance_is_rejected(tolerance):
    with pytest.raises(ValueError, match='tolerance'):
        best_response(lambda p: 1., 1., tolerance=tolerance)


@pytest.mark.parametrize('counts', [{}, {'00': 0}, {'00': -1, '01': 2}, {'000': 3}])
def test_invalid_raw_counts_are_not_silently_normalized(counts):
    with pytest.raises(ValueError):
        counts_to_probs(counts, 2)


def test_failed_readout_solver_does_not_return_a_physical_looking_result(monkeypatch):
    monkeypatch.setattr('hardware.mitigation.minimize', lambda *a, **k:
                        SimpleNamespace(success=False, x=np.array([.5, .5]),
                                        message='Iteration limit reached'))
    with pytest.raises(RuntimeError, match='mitigation'):
        mitigate_probs(np.array([.5, .5]), [np.eye(2)])


def test_duplicate_hardware_ids_are_rejected():
    rows = experiment_rows([3], pilot=True)
    rows[1]['id'] = rows[0]['id']
    with pytest.raises(ValueError, match='unique'):
        judge(rows, [{'000': 4096}]*len(rows), pilot=True)


def test_hardware_width_must_match_registered_player_count():
    rows = experiment_rows([3], pilot=True)
    with pytest.raises(ValueError, match='width'):
        judge(rows, [{'0000': 4096}]*len(rows), pilot=True)


def test_nonfinite_equilibrium_tolerance_is_rejected():
    rows = experiment_rows([3])
    with pytest.raises(ValueError, match='configuration'):
        judge(rows, [{'000': 4096}]*len(rows), epsilon=np.inf)


def test_hub_only_stability_does_not_skip_a_better_seed(monkeypatch):
    monkeypatch.setattr(strategy_opt, '_MAX_FIXPOINT_ITERS', 0)
    monkeypatch.setattr(strategy_opt, '_symmetric_payoff', lambda *a: 1.)
    def gap(params, *args, check_all_players=True, **kwargs):
        return .5 if check_all_players and params != DOVE else 0.
    monkeypatch.setattr(strategy_opt, 'nash_gap', gap)
    result = strategy_opt.nash_strategy(3, symmetric_caveat=True)
    assert result.params == DOVE
    assert result.is_nash


def test_automatic_runs_in_same_minute_do_not_share_output(monkeypatch, tmp_path):
    monkeypatch.setattr(results_io, 'RESULTS_ROOT', tmp_path)
    monkeypatch.setattr(results_io, 'run_timestamp', lambda: 'same-minute')
    first = results_io.new_run_dir('audit')
    second = results_io.new_run_dir('audit')
    assert first != second
    assert first.is_dir() and second.is_dir()
    assert results_io.new_run_dir('audit', 'explicit') == results_io.new_run_dir('audit', 'explicit')


@pytest.mark.parametrize('n', [3.5, True, 1])
def test_config_does_not_silently_change_player_count(n):
    with pytest.raises(ValueError, match='integers'):
        expand_cells({'sweep': {'N': n, 'topologies': 'ghz'}})


@pytest.mark.parametrize('name', ['V', 'C', 'gamma'])
def test_nonfinite_config_fails_before_experiment(name):
    with pytest.raises(ValueError, match='finite'):
        expand_cells({'sweep': {'N': 3, 'topologies': 'ghz'}, 'game': {name: np.nan}})


@pytest.mark.parametrize('n', [2, 3, 4, 5, 6])
def test_phase_proof_all_branches_and_nonlive_payoffs(n):
    # Independent audit grid includes identity/other branches, submaximal
    # angles and V<C; it does not only repeat the two published live branches.
    for m in range(n):
        for gamma in [.17, .83, 1.41]:
            prediction = branch_predictions(n, m, gamma, V=5., C=9.)
            base = [phase_strategy(n, m)]*n
            for deviation, target in [(DOVE, prediction['dove']),
                                      ((np.pi, 0., 0.), prediction['hawk']),
                                      (counter_strategy(n, m), 5.)]:
                profile = base.copy()
                profile[-1] = deviation
                actual = expected_payoff(build_ewl_circuit(n, profile, gamma=gamma), n, 5., 9.)
                assert actual[-1] == pytest.approx(target, abs=1e-10)
