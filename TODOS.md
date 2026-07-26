# TODOS

Deferred work with enough context to pick up cold. Ordered newest-first.

## Item-11 residue: ibm_marrakesh attribution on the N=3 gate counts

Two docstrings still attribute the N=3 entangler two-qubit-gate counts to
ibm_marrakesh:

- `experiments/hardware_n3_ghz.py:62` — "6 two-qubit gates on ibm_marrakesh vs
  35 for generic QSD"
- `experiments/hand_built_j.py:8` — "cutting the ibm_marrakesh CZ count
  (35 QSD -> 6)"

**Deliberately not edited.** The N=3 GHZ validation run went to ibm_fez
(c0a141f), but the files do not settle whether these counts were genuinely
measured against marrakesh during early prototyping — in which case the
attribution is correct and merely predates the move to fez — or whether the
backend name is stale. Resolving it needs the early transpile record.

Surfaced 2026-07-17 by a repo-wide `marrakesh` grep during the run-2 findings
writeup. `docs/` is clean; the only other hits are vendored qiskit
`fake_provider` files under `.venv-win/`.

## Device-noise (T1/T2) version of the topology controls

**What:** Re-run the topology-vs-implementation control study
(`scripts/topology_noise_controls.py`, finding
`docs/findings/2026-07-16-topology-vs-implementation-controls.md`) under a
device noise model (thermal relaxation + measured gate errors, e.g.
`NoiseModel.from_backend(ibm_fez)` reduced to a chain as in
`experiments/hardware_scaling.py`).

**Why:** Under the pinned per-gate depolarizing model, depth and qubit
mapping are provably not free variables (see the study's null checks), so
the 2026-07-16 controls could only equalize gate counts. With T1/T2 idling
noise, depth and mapping become real confounds — the matched-depth control
the depolarizing model cannot express becomes meaningful there. Simulation
only, zero quota.

## Hardware scaling repeat runs (cross-day error bars)

**What:** Re-run `python experiments/hardware_scaling.py --hardware` (conda env
`entangled-equilibria`) on 3–5 different days. Each run is one ~35s-QPU batch
job on ibm_fez; `scripts/plot_hardware_scaling.py` automatically aggregates all
runs under `results/hardware-scaling/` into mean ± std. If a run crashes
mid-poll, the job id is in `results/hardware-scaling/pending_jobs.txt`;
recover with `--from-job <id>`.

**Progress:**
- Run 1: 2026-07-16T074134Z (job d9c8fpn550hc73dl1tcg) — registration anchor.
- Run 2: 2026-07-17T014458Z (job d9cohq1htsac739c1iu0). First attempt
  d9chh0qneu4c739lvgb0 failed backend-side (error 9603, RF hardware, during
  ibm_fez maintenance; 0 quantum seconds billed — checked before
  resubmitting). Judged: N=4 conditional PASS (z −0.93), N=5 FAIL (z −4.74,
  same-signed deficit as run 1 → reproduced 1/1); cz-exponential again the
  best registered predictor (7.4 vs p_eff 23.4).
- **Caveat for runs 3–5:** run 2's recorded `calibration_last_update` equals
  run 1's (2026-07-16 08:30+05:30) despite the intervening maintenance —
  distinct execution, NOT a distinct calibration day. Before counting a
  future run toward the 3–5 cross-day target, check its calibration stamp
  differs (the judge flags `distinct_calibration_vs_previous_runs`).
  As of item 16 (2026-07-19), submission writes
  `pending-<jobid>-calibration.json` and the run dir gains
  `calibration_at_submit.json`; use that stamp for cross-day counting, not
  the analysis-time `calibration.json` (G15).

**Why:** One calibration epoch = one sample; IEEE-QCE reviewers expect run-to-run
variance. 3–5 repeats ≈ 15% of the monthly open-plan quota.

**This is NOT a multi-day wait (observed 2026-07-26).** The registered criterion
above is a *differing calibration stamp*, not a differing calendar date, and
ibm_fez recalibrates several times per day. Three distinct stamps were observed
on 2026-07-25 alone:

| stamp (+05:30) | seen at |
|---|---|
| 2026-07-25 08:15:48 | topology registration |
| 2026-07-25 16:05:46 | topology submission (job d9ia1pd0k0jc738jaqgg) |
| 2026-07-25 22:32:49 | N=6,7 submission (job d9if010gk0ls73f4avkg) |

That drift is real, not cosmetic — it moved the selector's chosen chain from
`[20,21,22,23,24]` to `[137,147,146,145,144]` and is what confounded the
topology batch's T4. So item 3 needs **two more `--hardware` runs on the
untouched scaling script (~35 QPU-s each) submitted after a recalibration**,
which can plausibly happen the same day; it does not need three calendar days.

Counter-consideration to state honestly if collected same-day: recalibrations
8 hours apart sample *recalibration-to-recalibration* variance, which is the
registered criterion, but they may understate multi-day drift (thermal cycling,
longer maintenance). If the repeats are same-day, say "distinct calibrations"
rather than implying distinct days.

**Pre-registration (frozen 2026-07-16, BEFORE any repeat):** each repeat must
be judged against the frozen effective-p predictions in
`results/hardware-scaling/preregistration.json` (protocol + falsification
criteria: `docs/findings/2026-07-16-preregistered-peff-scaling-predictions.md`).
Primary test is the drift-robust conditional one (refit p_eff on that run's
N=3, judge its N=4/5). Do not edit the registration after repeats exist.

**After each repeat:** run
`conda run -n entangled-equilibria python scripts/judge_repeat_run.py` —
applies the registered conditional test, tracks whether the N=5 deficit
(run 1: −0.0101, z=−5.2) reproduces, reports per-player vectors/worst/spread,
and regenerates `results/hardware-scaling/repeat-judgments.json` (it refuses
to run if preregistration.json differs from HEAD). Then regenerate the
scaling figure (`conda run -n entangled-equilibria python scripts/plot_hardware_scaling.py`),
which auto-aggregates all runs. Commit the run dir + judgments + plots.

## Pre-existing: test_gamma_sweep locale failure on Windows — test fix DONE

`tests/test_gamma_sweep.py::test_gamma_subfolders_and_topology` read report.md
via `Path.read_text()` with no encoding; on cp1252 consoles the UTF-8 "γ" read
as mojibake and the assert failed. Passed with `PYTHONUTF8=1`. The one-word fix
(`read_text(encoding="utf-8")`) was applied in 3c5c39a (2026-07-19); the full
gamma suite passes in the conda env without PYTHONUTF8 (151 passed). Surfaced
2026-07-16 during full-suite verification.

**Item 15 phase 1 report (2026-07-19):** `core.autocrlf` = true, set at system
level (`C:/Program Files/Git/etc/gitconfig`); no `.gitattributes` exists in the
repo; of the 50 tracked files under `results/`, 34 are all-CRLF text and 16 are
binary — zero files with mixed line endings on disk.

## T9 adaptation & fairness pilot — DONE; both caveats closed, sign-off open

**Done:** Pilot answering "does independent best-response adaptation restore
per-player fairness under noise?" for W N=4. Verdict: no — it equalizes only by
collapsing welfare (p=0: mean 1.00→0.51), fails to converge (p=0.02 limit
cycle), or barely moves anything (p=0.05). Writeup:
`docs/findings/2026-07-05-t9-adaptation-fairness.md`; code `scripts/t9_*.py`;
data `results/t9-pilot/precise-*`.

**Both caveats are now tested; neither is supported.**
- ~~Caveat 1: the rule.~~ **Tested 2026-07-26**
  (`docs/findings/2026-07-26-t9-rule-sensitivity.md`). Simultaneous BR removes
  move order entirely and reproduces all three verdicts; the p=0.02 residual
  stays flat at ~380x the convergence bar, so the non-convergence belongs to the
  noisy best-response map, not to round-robin ordering. Fictitious play and
  regret matching remain untested.
- ~~Caveat 2: extend to N=5 (W N=5 and ring N=5).~~ **Done 2026-07-26**
  (`docs/findings/2026-07-26-t9-caveat2-n5-ring.md`). W N=5 reproduces W N=4
  verdict-for-verdict. Ring N=5 never converges at any p and is qualitatively
  worse: it turns a perfectly fair p=0 baseline (spread 0.0000) into spread
  1.3329 at *exactly conserved* mean welfare, and the divergence is strongest
  noiselessly, so topology rather than noise drives it. Ring spread magnitudes
  are 50-round snapshots and are not quotable as magnitude results.

**Still open:** Aasa's sign-off (item 10) — a judgement, not a computation.
Untested rules: fictitious play, regret matching, fairness-constrained. Untested
cells: star and fully-connected at N=5; ring cycle-period characterization.

Note: this is a *different* question from the "Noise-aware strategy
optimization" item below (a symmetric-Q config-harness feature, still open).

## Noise-aware strategy optimization

**What:** Let `strategy_mode = cooperative|nash` run under noise, so the
topology-optimized "Q" is optimized against the *same* noisy circuit it is scored
on.

**Why:** Currently `run_cell` computes the optimized Q with the noiseless matrix
entangler (`src/experiment/sweep.py:69`). Under noise that Q is optimized for a
different (clean) world than it's evaluated in — a silent inconsistency. Month-4
spec (D4/3A) rejects `noise_p > 0` with non-`fixed` strategy_mode at config load to
avoid shipping the inconsistent number. Making the optimizer noise-aware would lift
that restriction and answer "what is the best quantum strategy *under* noise."

**Current state:** Blocked by cost — `game.strategy_opt.optimal_strategy` runs
multi-start Nelder–Mead + L-BFGS-B (45s per-cell budget) on the noiseless
statevector path. Threading the density-matrix `prob_fn` through it would run the
optimizer on density-matrix sims per cell, which is expensive and needs its own
design (caching, reduced restarts, or coarser tolerance under noise).

**Where to start:** `src/game/strategy_opt.py` (`optimal_strategy`, `_symmetric_payoff`)
and the `prob_fn` seam added to `nash.py` in Month 4. Design a budget-aware noisy
optimization path before removing the D4 config guard.

**Depends on:** Month-4 noise analysis + `prob_fn` injection landing.
