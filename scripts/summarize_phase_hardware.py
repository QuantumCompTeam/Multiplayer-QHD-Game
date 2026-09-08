"""Summarize registered raw hardware evidence without changing its judgment."""
from pathlib import Path
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result', type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text(encoding='utf-8'))
    decision = result['judgment']
    table = []
    for n in sorted({g['N'] for g in decision['gaps']}):
        gaps = [g for g in decision['gaps'] if g['N'] == n]
        summary = decision['summaries'][f'n{n}-candidate']
        table.append({'N': n, 'minimum_observed_gap': min(g['gap'] for g in gaps),
                      'minimum_simultaneous_lower_gap': min(g['simultaneous_lower_gap'] for g in gaps),
                      'maximum_normalized_gain_upper': max(g['simultaneous_upper_normalized_gain'] for g in gaps),
                      'p_zero': summary['p_zero'], 'retention': summary['retention'],
                      'floor': summary['floor'], 'deviations_tested': len(gaps)})
    print(json.dumps({'job': result['pending']['job_id'],
                      'usage': result['metrics'].get('usage'),
                      'pilot': decision['pilot'],
                      'complete_coverage': decision['complete_D_H_coverage'],
                      'registered_pass': decision['epsilon_equilibrium_supported'],
                      'per_N': table}, indent=2))


if __name__ == '__main__':
    main()
