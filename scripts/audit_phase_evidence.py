"""Independent stdlib-only recomputation of the three September 7 raw results.

Does not import the game's payoff functions or the registered judge. It checks
the same estimands by direct bit-count arithmetic and verifies frozen source
hashes against Git, without network access or QPU submission.
"""
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message='evidence validation failed'):
    if not condition:
        raise ValueError(message)


def validate_counts(counts, shots):
    require(type(shots) is int and shots > 0, 'invalid shot count')
    require(bool(counts) and all(type(c) is int and c >= 0 for c in counts.values()),
            'invalid frequencies')
    require(sum(counts.values()) == shots, 'shot count mismatch')


def primary_rows(rows):
    primary = [r for r in rows if r['kind'] in {'H', 'D', 'old_Q'}]
    require(bool(primary), 'no deviation evidence')
    return primary


def reward_mean(counts, n, player):
    total = 0.
    for label, count in counts.items():
        require(len(label) == n and set(label) <= {'0', '1'}, 'invalid bitstring')
        k = label.count('1')
        reward = 4/n if k == 0 else (
            (1/n if k == n else 4/k) if label[-1-player] == '1' else 0.)
        total += count*reward
    return total/sum(counts.values())


def audit():
    experiments = [
        ('2026-09-07-device-pilot-v2', '2026-09-07-hardware-pilot', 'b9aaf5a'),
        ('2026-09-07-confirmatory', '2026-09-07-hardware-confirmatory', '76aa8fd'),
        ('2026-09-07-confirmatory', '2026-09-07-hardware-repeat', '76aa8fd')]
    audited = []
    for registration, execution, revision in experiments:
        directory = ROOT/'results/phase-validation'/registration
        manifest_bytes = (directory/'manifest.json').read_bytes()
        manifest = json.loads(manifest_bytes)
        result = json.loads((ROOT/'results/phase-validation'/execution/'result.json').read_text())
        require(hashlib.sha256(manifest_bytes).hexdigest() == result['pending']['registration_sha256'], 'manifest hash mismatch')
        relative = (directory/'manifest.json').relative_to(ROOT).as_posix()
        frozen_manifest = subprocess.check_output(['git', 'show', f'{revision}:{relative}'], cwd=ROOT)
        require(manifest_bytes == frozen_manifest, 'manifest differs from pre-execution revision')
        require(hashlib.sha256((directory/'circuits.qpy').read_bytes()).hexdigest() == manifest['qpy_sha256'], 'QPY hash mismatch')
        for path, expected in manifest['code_hashes'].items():
            frozen = subprocess.check_output(['git', 'show', f'{revision}:{path}'], cwd=ROOT)
            require(hashlib.sha256(frozen).hexdigest() == expected, path)
        require(len(result['counts']) == manifest['pub_count'], 'pub count mismatch')
        for sample in result['counts']:
            validate_counts(sample, manifest['shots'])
        rows = manifest['rows']
        counts = {row['id']: sample for row, sample in zip(rows, result['counts'])}
        primary = primary_rows(rows)
        saved = {g['id']: g for g in result['judgment']['gaps']}
        by_n = {}
        for row in primary:
            n, player = row['N'], row['player']
            coop, deviation = counts[f'n{n}-candidate'], counts[row['id']]
            gap = reward_mean(coop, n, player)-reward_mean(deviation, n, player)
            radius = sum(4*math.sqrt(math.log(2*len(primary)/manifest['alpha'])/(2*sum(c.values())))
                         for c in [coop, deviation])
            upper = (radius-gap)/(4/n)
            require(math.isclose(gap, saved[row['id']]['gap'], rel_tol=1e-12, abs_tol=1e-12), 'gap mismatch')
            require(math.isclose(upper, saved[row['id']]['simultaneous_upper_normalized_gain'], rel_tol=1e-12, abs_tol=1e-12), 'bound mismatch')
            by_n.setdefault(n, []).append((gap, upper))
        complete = all({r['player'] for r in primary if r['N']==n and r['kind']==kind} == set(range(n))
                       for n in by_n for kind in ['H', 'D'])
        passed = not manifest['pilot'] and complete and all(
            upper <= manifest['epsilon'] for values in by_n.values() for _, upper in values)
        require(passed == result['judgment']['epsilon_equilibrium_supported'], 'decision mismatch')
        audited.append({'job_id': result['pending']['job_id'], 'frozen_revision': revision,
                        'registered_pass': passed, 'complete_D_H_coverage': complete,
                        'charged_seconds': result['metrics']['usage']['qpu_charge_time_seconds'],
                        'per_N': {n: {'minimum_gap': min(g for g, u in values),
                                      'maximum_upper_normalized_gain': max(u for g, u in values)}
                                  for n, values in by_n.items()}})
    return {'audit': 'independent raw-bitstring arithmetic; all validations passed',
            'total_charged_seconds': sum(r['charged_seconds'] for r in audited),
            'runs': audited}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
