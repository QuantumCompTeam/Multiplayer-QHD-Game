# Results

Generated experiment outputs, committed to git as part of the research record.
Each run lives in its own **timestamped** folder under a per-experiment
directory, so every result is labelled and reproducible. (`results/` is
blanket-ignored for convenience, so artifacts are committed with `git add -f`.)

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

## Coverage — what's actually here, and the gaps

Not every (N × topology × noise) cell has a committed run. This is the honest
map so a reader never mistakes absence for coverage. All payoff runs are at the
live convention V=4/C=3 unless marked retired.

| Experiment | N | Topologies | Noise | Status |
|---|---|---|---|---|
| `n-scaling-advantage/` | 2–6 | all 5 | 0 | **current** run `2026-07-19T0901Z` (+ 7 retired, see below) |
| `gamma-sweep/N2..N6` | 2–6 | all 5 | 0 | current-convention (V=4/C=3, fixed), regen 2026-07-19 |
| `noise-robustness/` | 2–5 | **GHZ, W, ring only** | p = 0→0.05 | current `2026-07-03T0213Z` (+ 1 retired `2026-07-02T1212Z`) |
| `topology-controls/` | 2–5 | GHZ, ring, star, FC | p = 0→0.05 | one control run `2026-07-16T172737Z` |
| `topology/` | per-topology | all 5 | 0 | per-topology reference runs |
| `hardware-n3/` | 3 | GHZ | device | one run `2026-07-16T013912Z` |
| `hardware-scaling/` | 3–**7** | GHZ | device | 4 runs at N=3–5 (**3 of 3–5 distinct calibrations — registered minimum met**; 2 of them chain-matched on `[59,75,74,73,79]`, which is the sample Fig. 6 aggregates) + N=3–7 extension `2026-07-25T180549Z`, excluded from Fig. 6 and from the judge as not the registered batch |
| `hardware-topology/` | 3–5 | **all 5** | device | one 49-pub batch `2026-07-25T114621Z` (topology + deviations + wirings + γ sweep) |
| `t9-pilot/` | 4, **5** | W, **ring** | 0 / 0.02 / 0.05 | adaptation pilot (provisional); both self-raised caveats closed 2026-07-26 (rule, and N=5 × {W, ring}) |

**Known coverage gaps** (unrun cells, not failures — see `src/experiment/report.py`,
which lists skipped cells explicitly per run):

- **Noise × {star, fully-connected}** — the Month-4 noise sweep covers only
  GHZ/W/ring. Star and fully-connected under depolarizing noise are unrun; the
  paper's noise claims are scoped to the three swept topologies.
- **Noise at N=6** — the noise sweep stops at N=5 (cost); the N=6 row exists
  only at zero noise.
- ~~**Hardware beyond GHZ**~~ — **closed 2026-07-25.** `hardware-topology/`
  runs ghz/ring/star/fully-connected/W on device. Still unrun on hardware:
  fully-connected N=5 (67 routed cz) and W N=4,5 (107, 219), all excluded on
  measured routed cz — see
  `docs/findings/2026-07-25-topology-hardware-feasibility.md`.
- **Cross-day hardware variance** — hardware-scaling has 2 of the 3–5 planned
  calibration *days* (three runs, but runs 1 and 2 share one calibration
  stamp). Item 3, gated on wall-clock, not on code. Fig. 6's error bars stay
  the two-point sample SD until this closes.
- **Absolute-magnitude noise prediction** — no registered model predicts the
  measured advantage magnitude: both the depolarizing and cz-exponential laws
  failed their registered tests at N=6,7, and the topology batch's per-cell
  predictions failed and were confounded by a mid-day recalibration. The
  structural claims are within-job differentials and do not rest on this.

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
