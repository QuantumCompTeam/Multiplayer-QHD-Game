"""Replay published phase decisions from provider counts, not copied summaries."""
import hashlib
import json
from pathlib import Path

import pytest

from hardware.phase_validation import judge


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
    assert replay == result['judgment']
