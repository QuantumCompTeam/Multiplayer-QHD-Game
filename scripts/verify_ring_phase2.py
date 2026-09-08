"""Recompute the figure's ring cells in the pinned conda environment."""
import importlib.metadata
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from config import V, C, GAMMA
from circuits.topologies import ring_entangler
from game.nash import compute_advantage


def serializable(value):
    if isinstance(value, dict):
        return {str(k): serializable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serializable(v) for v in value]
    if hasattr(value, 'tolist'):
        return serializable(value.tolist())
    return value


def main():
    if Path(sys.prefix).name != 'entangled-equilibria':
        raise ValueError(f'required conda environment: {sys.prefix}')
    versions = {name: importlib.metadata.version(name) for name in
                ['qiskit', 'qiskit-aer', 'numpy', 'scipy']}
    if versions != {'qiskit': '1.3.2', 'qiskit-aer': '0.14.2',
                    'numpy': '1.26.4', 'scipy': '1.13.1'}:
        raise ValueError(f'unsupported versions: {versions}')
    source = ROOT / 'results/n-scaling-advantage/2026-07-19T0901Z/results.json'
    stored = {r['N']: r for r in json.loads(source.read_text())['cells']
              if r['topology'] == 'ring'}
    output = {'interpreter': sys.executable, 'versions': versions,
              'V': V, 'C': C, 'gamma': GAMMA, 'source': str(source.relative_to(ROOT)),
              'cells': []}
    for n in range(2, 7):
        if stored[n]['V'] != V or stored[n]['C'] != C:
            raise ValueError(f'source convention mismatch at N={n}')
        result = serializable(compute_advantage(N=n, V=V, C=C, gamma=GAMMA, entangler=ring_entangler))
        row = {'N': n, 'result': result,
               'stored_advantage': stored[n]['advantage'],
               'advantage_difference': result['advantage'] - stored[n]['advantage']}
        if row['advantage_difference'] != 0:
            raise ValueError(f'ring advantage mismatch at N={n}: {row["advantage_difference"]}')
        output['cells'].append(row)
        print(json.dumps(row, indent=2), flush=True)
    destination = ROOT / 'docs/reviews/2026-09-08-ring-phase2.json'
    destination.write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(destination)


if __name__ == '__main__':
    main()
