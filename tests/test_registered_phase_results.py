"""Replay published phase decisions from provider counts, not copied summaries."""
import hashlib
import json
from pathlib import Path

import pytest

from hardware.phase_validation import judge


def assert_replay_equal(actual, expected):
    """Preserve exact decisions; allow platform roundoff in float statistics."""
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_replay_equal(actual[key], expected[key])
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            assert_replay_equal(left, right)
    elif isinstance(expected, float):
        assert actual == pytest.approx(expected, rel=1e-12, abs=1e-14)
    else:
        assert type(actual) is type(expected)
        assert actual == expected


def test_replay_comparison_preserves_decisions_and_meaningful_differences():
    assert_replay_equal({'value': 0.1 + 0.2, 'passed': False},
                        {'value': 0.3, 'passed': False})
    with pytest.raises(AssertionError):
        assert_replay_equal({'passed': True}, {'passed': False})
    with pytest.raises(AssertionError):
        assert_replay_equal({'value': 0.300001}, {'value': 0.3})


@pytest.mark.parametrize('registration,execution', [
    ('2026-09-07-device-pilot-v2', '2026-09-07-hardware-pilot'),
    ('2026-09-07-confirmatory', '2026-09-07-hardware-confirmatory'),
    ('2026-09-07-confirmatory', '2026-09-07-hardware-repeat'),
])
def test_registered_raw_phase_result_replays(registration, execution):
    root = Path('results/phase-validation')
    directory = root / registration
    manifest = json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    result = json.loads((root/execution/'result.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((directory/'circuits.qpy').read_bytes()).hexdigest() == manifest['qpy_sha256']
    assert len(result['counts']) == manifest['pub_count']
    assert all(sum(counts.values()) == manifest['shots'] for counts in result['counts'])
    rows = manifest['rows']
    replay = judge(rows, result['counts'][:len(rows)], alpha=manifest['alpha'],
                   epsilon=manifest['epsilon'], pilot=manifest['pilot'])
    assert_replay_equal(replay, result['judgment'])
