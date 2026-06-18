# Results

Generated experiment outputs. Each run lives in its own **timestamped** folder
under a per-experiment directory, so every result is labelled and reproducible.
These artifacts are committed to git as part of the research record.

## Layout

```
results/
  <experiment>/
    <UTC-timestamp>/        # e.g. 2026-06-18T0930Z  (UTC, colon-free)
      <artifacts...>
      metadata.json         # always present
```

`metadata.json` records: `experiment`, `created_utc` (ISO 8601), `git` (commit
hash + dirty flag), `python` version, and the run `params` (N range, topologies,
V, C, GAMMA, strategy set).

## Experiments

### `month2_n3_advantage/`
Source: `scripts/n3_advantage.py` — the Month-2 RQ1 checkpoint (N=3, GHZ).
- `summary.json` — full `compute_advantage(N=3)` result: per-player payoff
  vectors, classical NE, advantage, all pure NE, and the unilateral-deviation
  table (keyed `player{i}_{alt}`).

### `month3_topology_sweep/`
Source: `scripts/topology_sweep.py` — the Month-3 RQ2 topology × N sweep.
- `advantage_matrix.csv` — mean per-player advantage; rows = topology
  {GHZ, ring, star, full, W}, cols = N {2..6}. A trailing `*` marks an
  asymmetric topology (the value is the mean over players).
- `equilibrium_matrix.csv` — equilibrium structure per cell:
  `Q-NE` ((Q,…,Q) is Nash), `NE` (some pure NE exists), `-` (no pure NE).
- `per_player.json` — full per-player vectors and NE profiles for every
  (topology, N) cell.
- `heatmap.png` — advantage heatmap (topology × N).

## Regenerate

From the repo root (using the project venv):

```bash
PYTHONPATH=src .venv/bin/python scripts/n3_advantage.py
PYTHONPATH=src .venv/bin/python scripts/topology_sweep.py
```

Each invocation creates a fresh timestamped run folder; existing runs are never
overwritten.
