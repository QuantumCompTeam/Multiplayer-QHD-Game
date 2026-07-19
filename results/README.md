# Results

Generated experiment outputs. Each run lives in its own **timestamped** folder
under a per-experiment directory, so every result is labelled and reproducible.
These artifacts are committed to git as part of the research record
(`git add -f`, since `results/` is blanket-ignored for convenience).

## Layout

```
results/
  <experiment>/
    <UTC-timestamp>/        # e.g. 2026-06-18T0930Z  (UTC, colon-free)
      <artifacts...>
      metadata.json         # simulation runs: experiment, created_utc, git
                            # (commit + dirty), python version, run params
```

Hardware runs (`hardware-scaling/`, `hardware-n3/`) record `result.json` +
`calibration.json` instead of `metadata.json`, and carry the same experiment /
created_utc / git fields. The cross-day hardware-scaling state
(`pending_jobs.txt`, `preregistration.json`, `preregistration-baselines.json`,
`repeat-judgments.json`) lives at `results/hardware-scaling/` root.

## Regenerate

From the repo root, in the pinned conda env (`entangled-equilibria`; see
README setup):

```bash
PYTHONPATH=src conda run -n entangled-equilibria python scripts/run_experiment.py
PYTHONPATH=src conda run -n entangled-equilibria python scripts/topology_sweep.py
```

Each invocation creates a fresh timestamped run folder; existing runs are never
overwritten.
