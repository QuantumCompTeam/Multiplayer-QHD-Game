# IEEE Review Draft Notes

The compiled `main.pdf` is an evidence-preserving review draft, not a submission-ready manuscript. No numerical result was added or recomputed during the formatting pass.

## Author input

- ~~Add Aasa Singh Bhui's preferred publication email to the IEEE author
  block.~~ **Done 2026-07-26:** `aasasingh2005@gmail.com`.
- **Still open — Aasa's game-theory sign-off on the T9 rule (item 10)**, but the
  decision is now evidence-backed. It cannot be closed from the repository side;
  it is a judgement about whether "independent round-robin best response" is the
  right rule. **What has changed:** the sequencing axis of that doubt was
  tested. Simultaneous best response — which removes move order entirely —
  reproduces all three verdicts, including the `p=0.02` non-convergence, whose
  residual gain stays flat at ~380x the convergence bar
  (`docs/findings/2026-07-26-t9-rule-sensitivity.md`). So the limit cycle is a
  property of the noisy best-response map, not of round-robin ordering.
  **The cell-coverage doubt was also tested** (caveat 2,
  `docs/findings/2026-07-26-t9-caveat2-n5-ring.md`): W `N=5` reproduces W `N=4`
  verdict-for-verdict, and ring `N=5` never converges at any noise level,
  failing in the opposite direction — it turns a perfectly fair `p=0` baseline
  into spread 1.3329 at exactly conserved mean welfare. Both caveats the pilot
  raised against its own verdict are now tested and neither is supported.
  Fictitious play and regret matching remain untested, as do star and
  fully-connected at `N=5`. The ring spread magnitudes are 50-round snapshots of
  non-convergent trajectories and are deliberately **not** promoted into the
  paper. Until sign-off the fairness paragraph stays hedged as exploratory,
  which is how it reads in Sec. IV-C and the conclusion — no text change is
  pending, only the decision.
- Complete final author review of all sections drafted from repository artifacts.

## Bibliography verification

- All eight cited publications were checked against authoritative publisher/DOI records.
- Every bibliography entry now includes a verified DOI, and no unverified citation remains.

## Scope and metric checks

- Full-SU(2) equilibrium is not established; current claims are restricted to
  unilateral deviations in the finite menu `{D,H,Q_N}`. The `N=4,5` hardware
  points are a fixed cooperative protocol, not equilibria. This is unchanged by
  the 2026-07-25 hardware equilibrium test, which measured deviations **within
  that same restricted menu** — it moved the claim from simulation to hardware,
  not from restricted to full SU(2).
- Simulation payoff gaps use a circuit-evaluated restricted `{D,H}` comparator,
  while hardware uses analytic `1/N`; these are distinct metrics.
- Runs 1 and 2 provide same-recorded-calibration repeatability only; their
  result artifacts carry the same result-write-time snapshot, which does not
  prove an unchanged provider calibration. Run 3 (2026-07-25) is the first
  genuinely distinct calibration day, so the count is 2 of 3--5.
- Provider calibration can change **within a single day**: the topology batch
  was registered at 08:15 and executed at 16:05 on a different pinned qubit set
  because the selector re-ran against fresh calibration. Runs since then hold
  the registered qubits explicitly. Any comparison across artifacts must check
  the pinned set, not only the date.
- ~~Existing Figure 6 error bars are the two-point sample SD and do not include
  within-run uncertainty.~~ **Fixed 2026-07-26.** Figure 6 is now a genuine
  cross-calibration aggregate: three executions in **two distinct calibration
  epochs**, all on chain `[59,75,74,73,79]`, with executions sharing a
  calibration stamp averaged into one point before the spread is taken. The bars
  still exclude within-run multinomial and weighted-fit error, so they are a
  stated lower bound rather than a total-uncertainty estimate.
- **`scripts/plot_hardware_scaling.py` had two defects that corrupted the
  aggregate; both fixed 2026-07-26.** It aggregated every directory containing a
  `result.json`, which folded the `N=3..7` extension into the `N=3,4,5` curve
  even though `judge_repeat_run.py` excludes it explicitly; and it reported
  chain and job id from the first run as if they covered the aggregate, emitting
  a caption asserting one chain for runs that used three. Selection now matches
  the judge, and every exclusion is printed.

## Hardware evidence: resolved 2026-07-25

- **Wiring-permutation control: RUN, and the claim holds.** The star `N=4`
  permutation test returned a per-player vector that moves by at most 0.035
  across three wirings while the hub--leaf split is unchanged (registered test
  T3, `results/hardware-topology/2026-07-25T114621Z/judgments.json`). The
  player-position claim does **not** need narrowing; Sec. IV-C is promoted to
  simulation-plus-hardware.
- **W topology: run.** W `N=3` executed at 42 routed cz and retained 97.9% of
  ideal advantage. W `N=4,5` were excluded on measured routed cz (107, 219),
  recorded in `docs/findings/2026-07-25-topology-hardware-feasibility.md`.
- **Restricted-menu equilibrium: hardware-verified.** All three unilateral Hawk
  deviation gaps at GHZ `N=3` positive (registered test T1). Stated as such in
  the abstract, Sec. IV and the conclusion.
- **Environment provenance and `calibration_at_submit.json`: validated** on run
  3 (`2026-07-25T035623Z`) and on both 2026-07-25 batches.

## Hardware evidence still in progress

- **Cross-calibration executions: 3 of the registered 3--5 — the minimum is
  met.** Four scaling runs exist; runs 1 and 2 share one calibration stamp, so
  the distinct stamps are 2026-07-16 08:30:13, 2026-07-25 08:15:48 and
  2026-07-26 13:29:01. **The binding constraint is now chain-matching, not
  count:** only 2 of the 3 epochs ran on `[59,75,74,73,79]`, because run 3 took
  `[20,21,22,23,24]` from live calibration. `hardware_scaling.py` has no
  `resolve_pinned_set` (that fix landed only in `hardware_topology.py`) and its
  registration records no pinned set, so run 4 was submitted with an explicit
  `--chain`. A third chain-matched epoch needs one further run after the next
  recalibration.
- **The `N=5` deficit magnitude is not stable across epochs** (0.0092 to 0.0186,
  a factor of two), which is now stated in Sec. IV and the limitations. The
  same-signed reproduction is 3 of 3.
- ~~Make the repeat judge consume the submission-time calibration snapshot.~~
  Done — it prefers `calibration_at_submit.json` and records the source per run;
  the figure now reads the same stamp for its epoch grouping.
- **The N=7 retention anomaly is unexplained, and neither repeat track will
  settle it.** Retention is non-monotone (99.2/97.5/97.3/96.3/98.1%) and the
  `N=7` ZNE estimate overshoots the noiseless ideal, which no physical noise
  model can do. Reported in the text as an observation, not a result. **The
  paper previously said this needed "the cross-day repeats that remain pending";
  that was wrong and is corrected.** Item 3 re-executes the registered
  `N=3,4,5` batch and plan Task 9 re-executes the topology batch — neither
  re-runs `N=6,7`. Settling it requires a dedicated
  `--ns 3,4,5,6,7 --chain-len 7` submission, which has not been run.
- **No registered model predicts absolute advantage magnitude.** Both the
  device-noise model and the CZ-exponential law failed their registered tests at
  `N=6,7`, and the topology batch's per-cell predictions failed and were
  additionally confounded by a mid-day recalibration that moved the pinned set.
  The paper now says this explicitly and scopes the five-model ranking to
  `N <= 5`. If a reviewer asks for predictive noise modelling, the honest answer
  is that we do not have it.
- ~~Regenerate the scaling figure and any cross-day uncertainty summary only after new repository artifacts exist.~~ Done 2026-07-26 against run 4; `paper/figs/hardware_scaling.pdf` now comes from `results/hardware-scaling/2026-07-26T090122Z/plots/`.
- **Page count is now 10, against a typical IEEE QCE limit of 8.** The 2026-07-26 honesty additions (Fig. 6 caption, the T9 robustness checks, the corrected `N=7` resolution path, the deficit-stability statement) cost roughly one page. The `N=6,7` subsection remains the most compressible block if the venue is confirmed at 8.

## Submission checks

- Confirm the exact IEEE QCE submission category, current author instructions, and page limit.
- Rebuild after adding verified author metadata or making any future bibliography changes.
- Run a final citation, figure, accessibility, and PDF-conformance review.
- Prepare the final submission package only after the remaining author and hardware decisions are resolved.
