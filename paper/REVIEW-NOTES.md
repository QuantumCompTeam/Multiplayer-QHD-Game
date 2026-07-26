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
  Fictitious play and regret matching remain untested, and only W `N=4` is
  covered. Until sign-off the fairness paragraph stays hedged as exploratory,
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
- Existing Figure 6 error bars are the two-point sample SD and do not include
  within-run uncertainty; a future cross-day figure should separate within-run
  and between-day uncertainty.

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

- **Cross-day executions: 2 of the registered 3--5 distinct calibration days.**
  Three scaling runs exist but runs 1 and 2 share one calibration stamp (run 2
  carries `distinct_calibration_vs_previous_runs: false`). Figure 6's error bars
  are still the two-point sample SD and still are not a cross-day estimate; that
  replacement is blocked on further distinct days, not on code.
- Make the repeat judge consume the submission-time calibration snapshot or document a manual verification step.
- **The N=7 retention anomaly is unexplained.** Retention is non-monotone
  (99.2/97.5/97.3/96.3/98.1%) and the `N=7` ZNE estimate overshoots the
  noiseless ideal, which no physical noise model can do. Reported in the text as
  an observation, not a result. Needs repeats before it is either explained or
  promoted.
- **No registered model predicts absolute advantage magnitude.** Both the
  device-noise model and the CZ-exponential law failed their registered tests at
  `N=6,7`, and the topology batch's per-cell predictions failed and were
  additionally confounded by a mid-day recalibration that moved the pinned set.
  The paper now says this explicitly and scopes the five-model ranking to
  `N <= 5`. If a reviewer asks for predictive noise modelling, the honest answer
  is that we do not have it.
- Regenerate the scaling figure and any cross-day uncertainty summary only after new repository artifacts exist.

## Submission checks

- Confirm the exact IEEE QCE submission category, current author instructions, and page limit.
- Rebuild after adding verified author metadata or making any future bibliography changes.
- Run a final citation, figure, accessibility, and PDF-conformance review.
- Prepare the final submission package only after the remaining author and hardware decisions are resolved.
