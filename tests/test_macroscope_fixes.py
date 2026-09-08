"""Failure-path regressions for the eight Macroscope review findings."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import zipfile

import pytest

import check_submission_archive as archive_check
import audit_phase_evidence as evidence_audit
import run_phase_hardware as hardware
import run_experiment
import verify_ring_phase2 as ring


@pytest.mark.parametrize('failure', ['response', 'pending_write'])
def test_interrupted_submission_recovers_by_presaved_tag(tmp_path, monkeypatch, failure):
    manifest = {'backend': 'test-device', 'max_execution_time_seconds': 60, 'shots': 8}
    job = SimpleNamespace(job_id=lambda: 'provider-job')
    accepted = []
    def factory(tag):
        def run(circuits, shots):
            intent = json.loads((tmp_path/'submission-intent.json').read_text())
            assert intent['submission_tag'] == tag
            accepted.append((tag, job))
            if failure == 'response':
                raise TimeoutError('provider accepted before response loss')
            return job
        return SimpleNamespace(run=run)
    original = hardware.durable_json
    def write(path, payload):
        if path.name == 'pending.json':
            raise OSError('interrupted pending write')
        original(path, payload)
    if failure == 'pending_write':
        monkeypatch.setattr(hardware, 'durable_json', write)
    with pytest.raises((TimeoutError, OSError)):
        hardware.submit_journaled(tmp_path, manifest, 'hash', factory, [])
    with pytest.raises(ValueError, match='already attempted'):
        hardware.submit_journaled(tmp_path, manifest, 'hash', factory, [])
    monkeypatch.setattr(hardware, 'durable_json', original)
    def jobs(*, job_tags, limit):
        assert job_tags == [accepted[0][0]]
        return [job]
    recovered, pending = hardware.recover_journaled(SimpleNamespace(jobs=jobs), tmp_path, 'hash')
    assert recovered is job and pending['job_id'] == 'provider-job'
    assert len(accepted) == 1
    assert json.loads((tmp_path/'pending.json').read_text()) == pending


@pytest.mark.parametrize('matches', [[], [object(), object()]])
def test_ambiguous_recovery_never_submits(tmp_path, matches):
    hardware.durable_json(tmp_path/'submission-intent.json',
                          {'registration_sha256': 'hash', 'submission_tag': 'tag'})
    with pytest.raises(RuntimeError, match='do not resubmit'):
        hardware.recover_journaled(SimpleNamespace(jobs=lambda **kw: matches), tmp_path, 'hash')
    assert not (tmp_path/'pending.json').exists()


def test_legacy_job_id_recovery_and_registration_mismatch(tmp_path):
    hardware.durable_json(tmp_path/'pending.json', {'registration_sha256': 'hash', 'job_id': 'legacy'})
    service = SimpleNamespace(job=lambda job_id: job_id)
    assert hardware.recover_journaled(service, tmp_path, 'hash')[0] == 'legacy'
    with pytest.raises(ValueError, match='registration mismatch'):
        hardware.recover_journaled(service, tmp_path, 'wrong')


@pytest.mark.parametrize('tamper', ['qhd.tex', 'IEEEtran.cls', 'IEEEtran.bst', 'qhd.bbl', 'extra'])
def test_source_zip_tampering_is_rejected(tamper):
    content = {name: name.encode() for name in ['qhd.tex', 'IEEEtran.cls', 'IEEEtran.bst', 'qhd.bbl']}
    hashes = {k: hashlib.sha256(v).hexdigest() for k, v in content.items()}
    manifest = {'files': {'qhd.tex': hashes['qhd.tex']},
                'ieeetran_cls_sha256': hashes['IEEEtran.cls'],
                'ieeetran_bst_sha256': hashes['IEEEtran.bst'], 'bbl_sha256': hashes['qhd.bbl']}
    content[tamper] = b'changed'
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        for name, value in content.items():
            archive.writestr(name, value)
    with zipfile.ZipFile(stream) as archive, pytest.raises(ValueError, match='source ZIP'):
        archive_check.verify_source(archive, manifest)


def test_audit_rejects_altered_manifest_with_optimization(tmp_path):
    root = tmp_path/'results/phase-validation'
    reg = root/'2026-09-07-device-pilot-v2'
    run = root/'2026-09-07-hardware-pilot'
    reg.mkdir(parents=True)
    run.mkdir()
    (reg/'manifest.json').write_text('{}')
    (run/'result.json').write_text(json.dumps({'pending': {'registration_sha256': 'wrong'}}))
    code = ('import sys; from pathlib import Path; sys.path.insert(0,"scripts"); '
            'import audit_phase_evidence as a; a.ROOT=Path(sys.argv[1]); a.audit()')
    result = subprocess.run([sys.executable, '-O', '-c', code, str(tmp_path)], capture_output=True)
    assert result.returncode != 0
    assert b'manifest hash mismatch' in result.stderr


def test_ring_mismatch_does_not_overwrite_evidence(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['verify_ring_phase2.py'])
    source = tmp_path/'results/n-scaling-advantage/2026-07-19T0901Z/results.json'
    source.parent.mkdir(parents=True)
    source.write_text(json.dumps({'cells': [{'N': 2, 'topology': 'ring', 'V': 4., 'C': 3., 'advantage': 1.5}]}))
    output = tmp_path/'docs/reviews/2026-09-08-ring-phase2.json'
    output.parent.mkdir(parents=True)
    output.write_text('original evidence')
    monkeypatch.setattr(ring, 'ROOT', tmp_path)
    monkeypatch.setattr(sys, 'prefix', str(tmp_path/'entangled-equilibria'))
    monkeypatch.setattr(ring.importlib.metadata, 'version', lambda name: {
        'qiskit': '1.3.2', 'qiskit-aer': '0.14.2', 'numpy': '1.26.4', 'scipy': '1.13.1'}[name])
    monkeypatch.setattr(ring, 'compute_advantage', lambda **kw: {'advantage': 0.})
    with pytest.raises(ValueError, match='ring advantage mismatch'):
        ring.main()
    assert output.read_text() == 'original evidence'


def test_ring_explicit_output_cannot_overwrite(tmp_path, monkeypatch):
    output = tmp_path/'existing.json'
    output.write_text('original')
    monkeypatch.setattr(sys, 'argv', ['verify_ring_phase2.py', '--output', str(output)])
    with pytest.raises(FileExistsError):
        ring.main()
    assert output.read_text() == 'original'


@pytest.mark.parametrize('counts', [{'0': -1, '1': 9}, {'0': 0.5, '1': 7.5},
                                   {'0': True, '1': 7}, {}])
def test_audit_rejects_invalid_frequencies(counts):
    with pytest.raises(ValueError, match='invalid frequencies'):
        evidence_audit.validate_counts(counts, 8)


@pytest.mark.parametrize('rows', [[], [{'kind': 'candidate'}]])
def test_audit_rejects_empty_deviation_evidence(rows):
    with pytest.raises(ValueError, match='no deviation evidence'):
        evidence_audit.primary_rows(rows)


@pytest.mark.skipif(sys.platform == 'win32', reason='POSIX directory durability path')
def test_journal_flushes_directory_entries(tmp_path, monkeypatch):
    import stat
    flushed = []
    original = hardware.os.fsync
    def fsync(fd):
        flushed.append(stat.S_ISDIR(hardware.os.fstat(fd).st_mode))
        original(fd)
    monkeypatch.setattr(hardware.os, 'fsync', fsync)
    hardware.durable_json(tmp_path/'intent.json', {'tag': 'test'})
    assert flushed[0] is False
    assert all(flushed[1:]) and len(flushed) >= 2


def test_experiment_cli_allocates_distinct_same_minute_runs(tmp_path, monkeypatch):
    config = tmp_path/'experiment.yaml'
    config.write_text('experiment:\n  name: collision-check\nsweep:\n  N: 2\n  topologies: [ghz]\noutput:\n  formats: [json]\n')
    monkeypatch.setattr(sys, 'argv', ['run_experiment.py', '--config', str(config)])
    monkeypatch.setattr(run_experiment.results_io, 'RESULTS_ROOT', tmp_path/'outputs')
    monkeypatch.setattr(run_experiment.results_io, 'run_timestamp', lambda: 'same-minute')
    assert run_experiment.main() == 0
    original = (tmp_path/'outputs/collision-check/same-minute/results.json').read_bytes()
    assert run_experiment.main() == 0
    assert (tmp_path/'outputs/collision-check/same-minute-001/results.json').exists()
    assert (tmp_path/'outputs/collision-check/same-minute/results.json').read_bytes() == original
