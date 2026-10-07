# Results

Every simulation and hardware result used in the paper. Each run lives in its
own UTC-timestamped folder under a per-experiment directory and is never
overwritten; re-running an experiment creates a new folder.

Simulation runs contain `config.snapshot.yaml`, `metadata.json` (git commit,
Python version, parameters), `report.md`, `results.json`/`results.csv` and
`plots/`. Hardware runs contain `result.json` (counts and analysis),
`calibration.json`, and where available `calibration_at_submit.json`, the
provider calibration recorded when the job was submitted.

| Folder | Content | Used in the paper for |
|---|---|---|
| `n-scaling-advantage/2026-07-19T0901Z` | fixed profile, N=2–6, five families, zero noise | Figs. 1, 2, 4 |
| `n-scaling-advantage/2026-07-20T1800Z`, `2026-07-21T0405Z` | symmetric strategy search (`strategy_mode: nash`) | strategy-search method |
| `gamma-sweep/N2`–`N6` | entanglement-angle sweeps | Fig. 3 (N=4) and the thresholds in Sec. VI-A |
| `noise-robustness/2026-07-03T0213Z` | depolarizing sweep p=0–0.05, GHZ/W/ring, N=2–5 | noise-robustness section |
| `noise-robustness/2026-07-02T1212Z` | same sweep with the earlier transpiled-unitary W | W gate counts quoted for comparison |
| `topology-controls/2026-07-16T172737Z` | matched-count and compilation controls | Table III |
| `hardware-n3/2026-07-16T013912Z` | N=3 GHZ on ibm_fez | Fig. 6 |
| `hardware-scaling/` | N=3–5 runs (first execution and three repeats), N=3–7 extension, preregistered predictions and judgments | Table IV, Figs. 7–9 |
| `hardware-topology/2026-07-25T114621Z` | 49-circuit multi-topology batch and its preregistration | Table V, Fig. 10 |
| `phase-validation/` | alternative-phase circuits, device rehearsals, pilot and two complete hardware batches | Table VI |
| `journal-strengthening/2026-09-07-offline` | phase branches, payoff sensitivity, compact-evaluation timings | Fig. 5 |
| `t9-pilot/precise-*` | finite-round adaptation pilot | adaptation-pilot section |

Commands that regenerate each item are listed in the top-level `README.md`.
