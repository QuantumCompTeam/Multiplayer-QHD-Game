"""Reproducible offline journal extension: phase table, scaling, raw sensitivity."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from game.compact_ghz import compact_payoffs
from game.observable_payoffs import counts_summary
from game.phase_branches import branch_predictions, phase_strategy
from results_io import new_run_dir, write_metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--bootstrap', type=int, default=2000)
    args = parser.parse_args()
    out = args.output or new_run_dir('journal-strengthening')
    out.mkdir(parents=True,exist_ok=True)
    phases = []
    benchmarks = []
    rng = np.random.default_rng(20260907)
    for n in [3,4,5,6,7,8,16,32,64,128]:
        phases.append({'N': n, 'original': branch_predictions(n,1),
                       'candidate': branch_predictions(n,n//2)})
        profile = [tuple(rng.uniform(-np.pi,np.pi,3)) for _ in range(n)]
        compact_payoffs(profile)  # warm quadrature cache
        tracemalloc.start()
        started = time.perf_counter()
        actual = compact_payoffs(profile)
        elapsed = time.perf_counter()-started
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        benchmarks.append({'N': n, 'seconds_with_tracemalloc': elapsed,
                           'python_tracked_peak_bytes': peak,
                           'mean': actual['mean'],
                           'dense_complex128_matrix_bytes': 16*4**n,
                           'memory_scope': 'Python/NumPy tracked allocations, not process RSS'})
    sensitivity = []
    sources = []
    for path in sorted((ROOT/'results/hardware-scaling').glob('*/result.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        series = data.get('analysis',{}).get('series',{})
        if not isinstance(series,dict):
            continue
        used = False
        for n, cell in series.items():
            counts = cell.get('folds',{}).get('1',{}).get('counts')
            if not counts:
                continue
            for ell in [0., .25, .5, 1.]:
                row = counts_summary(counts,ell,bootstrap=args.bootstrap,seed=907+int(n))
                row.update(source=path.relative_to(ROOT).as_posix(),
                           job_id=data.get('job',{}).get('job_id'),
                           chain=data.get('analysis',{}).get('chain'))
                sensitivity.append(row)
            used = True
        if used:
            sources.append({'path':path.relative_to(ROOT).as_posix(),
                            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    payload = {'status':'retrospective raw-count sensitivity; ideal phase derivations; CPU benchmark',
               'phases':phases,'benchmarks':benchmarks,'sensitivity':sensitivity,'sources':sources}
    (out/'results.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    write_metadata(out,'journal-strengthening',{'bootstrap':args.bootstrap,'seed':20260907,
                   'hardware_submitted':False,'sources':sources})
    fig, axes = plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
    small = phases[:5]
    for key,label in [('original','Original phase'),('candidate','Alternative phase')]:
        axes[0].plot([r['N'] for r in small],
                     [r[key]['restricted_margin'] for r in small], 'o-',label=label)
    axes[0].axhline(0,color='black',linewidth=.7)
    axes[0].set(xlabel='Players N',ylabel='Minimum D/H gap',title='Ideal restricted incentives')
    axes[0].legend(fontsize=8)
    selected = [r for r in sensitivity if '2026-07-25T180549Z' in r['source']]
    for ell in [0.,1.]:
        rows = sorted([r for r in selected if r['ell']==ell],key=lambda r:r['N'])
        if rows:
            axes[1].errorbar([r['N'] for r in rows],[r['retention'] for r in rows],
                            yerr=[1.96*r['mean_se']*r['N']/3 for r in rows],fmt='o-',label=f'Raw ell={ell:g}')
            axes[1].plot([r['N'] for r in rows],[r['uniform_retention'] for r in rows],
                         '--',label=f'Uniform ell={ell:g}')
    axes[1].set(xlabel='Players N',ylabel='Analytic-baseline retention',title='Payoff sensitivity')
    axes[1].legend(fontsize=7)
    axes[2].loglog([r['N'] for r in benchmarks],[r['seconds_with_tracemalloc'] for r in benchmarks],'o-')
    axes[2].set(xlabel='Players N',ylabel='Seconds (instrumented)',title='Exact compact GHZ evaluation')
    fig.savefig(out/'journal_extensions.pdf')
    fig.savefig(out/'journal_extensions.png',dpi=180)
    lines = ['# Offline journal-extension evidence','',
             'No new hardware data. Sensitivity uses raw fold-1 counts; uncertainty excludes calibration drift.',
             '','| N | original min gap | alternative min gap | unrestricted gain |',
             '|---|---:|---:|---:|']
    for r in small:
        lines.append(f"| {r['N']} | {r['original']['restricted_margin']:.6f} | {r['candidate']['restricted_margin']:.6f} | {r['candidate']['su2_gain']:.6f} |")
    lines += ['','## N=3–7 extension source, raw reweighting','',
              '| N | ell | retention | uniform comparator | player floor |','|---|---:|---:|---:|---:|']
    for r in selected:
        if r['ell'] in [0.,1.]:
            lines.append(f"| {r['N']} | {r['ell']:.0f} | {r['retention']:.6f} | {r['uniform_retention']:.6f} | {r['floor']:.6f} |")
    lines += ['','CPU timings include tracemalloc overhead; tracked allocation is not whole-process memory.',
              'Bootstrap intervals in JSON are pointwise and conditional on empirical support, not simultaneous equilibrium certificates.']
    (out/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(out)
    print(f'{len(phases)} phase rows; {len(benchmarks)} benchmarks; {len(sensitivity)} sensitivity rows')


if __name__ == '__main__':
    main()
