"""Execute/recover an explicitly committed phase-validation registration.

Submission requires --submit; never modifies saved accounts. A pending job is
persisted before polling, and its result can be recovered without resubmission.
Use the isolated hardware environment that created the QPY file.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'experiments'))

from hardware.phase_validation import judge


def durable_json(path, payload):
    """Flush to disk before atomically publishing a complete journal record."""
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with temporary.open('x', encoding='utf-8') as handle:
        json.dump(payload, handle, indent=2)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def submit_journaled(output, manifest, manifest_hash, sampler_factory, circuits):
    intent = {'registration_sha256': manifest_hash, 'backend': manifest['backend'],
              'cap_seconds': manifest['max_execution_time_seconds'],
              'submitted_utc': datetime.now(timezone.utc).isoformat(),
              'submission_tag': 'qhd-' + uuid.uuid4().hex}
    intent_path = output / 'submission-intent.json'
    if intent_path.exists() or (output / 'pending.json').exists():
        raise ValueError('submission already attempted; recover, never resubmit this directory')
    durable_json(intent_path, intent)
    sampler = sampler_factory(intent['submission_tag'])
    job = sampler.run(circuits, shots=manifest['shots'])
    pending = dict(intent, job_id=job.job_id())
    durable_json(output / 'pending.json', pending)
    return job, pending


def recover_journaled(service, output, manifest_hash):
    pending_path = output / 'pending.json'
    path = pending_path if pending_path.exists() else output / 'submission-intent.json'
    pending = json.loads(path.read_text(encoding='utf-8'))
    if pending['registration_sha256'] != manifest_hash:
        raise ValueError('pending job registration mismatch')
    if 'job_id' in pending:
        return service.job(pending['job_id']), pending
    # A timeout/crash after provider acceptance is resolved through its pre-saved
    # unique tag. Zero matches can mean indexing lag: never retry submission.
    jobs = service.jobs(job_tags=[pending['submission_tag']], limit=2)
    if len(jobs) != 1:
        raise RuntimeError('submission unresolved: expected one tagged job; retry recovery later, do not resubmit')
    job = jobs[0]
    pending['job_id'] = job.job_id()
    durable_json(pending_path, pending)
    return job, pending


def validate_registration(directory):
    directory = directory.resolve()
    relative = (directory/'manifest.json').relative_to(ROOT).as_posix()
    content = (directory/'manifest.json').read_bytes()
    committed = subprocess.run(['git','show',f'HEAD:{relative}'],cwd=ROOT,capture_output=True)
    if committed.returncode or committed.stdout != content:
        raise ValueError('registration must be byte-identical to the committed HEAD manifest')
    manifest = json.loads(content)
    if not manifest['backend'] or manifest['rehearsal_kind'] != 'device_model':
        raise ValueError('a pinned backend and complete device-model rehearsal are required')
    for relative, expected in manifest['code_hashes'].items():
        if hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'code changed after preparation: {relative}')
    if hashlib.sha256((directory/'circuits.qpy').read_bytes()).hexdigest() != manifest['qpy_sha256']:
        raise ValueError('prepared QPY circuits changed')
    if not 0 < manifest['max_execution_time_seconds'] <= 100:
        raise ValueError('phase experiment execution cap must be at most 100 seconds')
    return manifest, hashlib.sha256(content).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('registration',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--submit',action='store_true')
    parser.add_argument('--recover',action='store_true')
    args = parser.parse_args()
    manifest, manifest_hash = validate_registration(args.registration)
    if not args.submit and not args.recover:
        print(json.dumps({'validated':True,'pubs':manifest['pub_count'],
                          'cap_seconds':manifest['max_execution_time_seconds']}))
        return
    if args.submit and args.recover:
        parser.error('choose submit or recover')
    from qiskit import qpy
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    from hardware_scaling import chain_calibration
    service = QiskitRuntimeService()
    if args.submit:
        if args.output.exists():
            parser.error('output already exists; recover a pending job or choose a fresh epoch directory')
        with (args.registration/'circuits.qpy').open('rb') as handle:
            circuits = qpy.load(handle)
        if len(circuits) != manifest['pub_count']:
            raise ValueError('QPY pub count mismatch')
        backend = service.backend(manifest['backend'])
        calibration = chain_calibration(backend,manifest['chain'])
        args.output.mkdir(parents=True)
        (args.output/'calibration_at_submit.json').write_text(json.dumps(calibration,indent=2)+'\n',encoding='utf-8')
        def sampler_factory(tag):
            return SamplerV2(mode=backend, options={
                'max_execution_time': manifest['max_execution_time_seconds'],
                'environment': {'job_tags': [tag]}})
        job, pending = submit_journaled(args.output, manifest, manifest_hash,
                                        sampler_factory, circuits)
        print(f"Submitted {job.job_id()}; cap {manifest['max_execution_time_seconds']} s",flush=True)
    else:
        job, pending = recover_journaled(service, args.output, manifest_hash)
    result = job.result()
    counts = [pub.data.meas.get_counts() for pub in result]
    if len(counts) != manifest['pub_count']:
        raise ValueError('provider result pub count mismatch')
    rows = manifest['rows']
    decision = judge(rows,counts[:len(rows)],alpha=manifest['alpha'],
                     epsilon=manifest['epsilon'],pilot=manifest['pilot'])
    output = {'pending':pending,'counts':counts,'judgment':decision,
              'metrics':job.metrics(),'analysis_utc':datetime.now(timezone.utc).isoformat()}
    (args.output/'result.json').write_text(json.dumps(output,indent=2,default=str)+'\n',encoding='utf-8')
    print(args.output/'result.json')


if __name__ == '__main__':
    main()
