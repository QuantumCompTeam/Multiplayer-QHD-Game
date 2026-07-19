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
conda run -n entangled-equilibria python scripts/run_experiment.py
conda run -n entangled-equilibria python scripts/topology_sweep.py
```

Each invocation creates a fresh timestamped run folder; existing runs are never
overwritten.

## Retired old-convention runs (V=1000/C=550)

Seven `n-scaling-advantage/` runs — 2026-07-02T0444Z/0525Z/0538Z/1247Z/1757Z and
2026-07-16T0736Z/0738Z — used the superseded payoff convention V=1000/C=550 (a
bounded `experiments/config.yaml` default regression, fixed 2026-07-17). They are
truthful historical records, each carrying a `RETIRED.md` note; **do not cite
their payoff numbers as current-convention.** The current-convention advantage
map (V=4/C=3, strategy_mode=fixed) is `n-scaling-advantage/2026-07-19T0901Z`.
The `gamma-sweep/N2..N6` folders are current-convention (V=4/C=3, fixed),
regenerated 2026-07-19 via `tests/test_gamma_sweep.py`. See
`docs/findings/2026-07-17-item11-stale-claim-audit.md` (item 13) and
`docs/VERIFIED-FACTS.md` F3.
