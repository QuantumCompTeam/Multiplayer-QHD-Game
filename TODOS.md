# TODOS

Deferred work with enough context to pick up cold. Ordered newest-first.

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
runs under `results/hardware-scaling/` into mean ± std. First run:
2026-07-16T074134Z (job d9c8fpn550hc73dl1tcg). If a run crashes mid-poll, the
job id is in `results/hardware-scaling/pending_jobs.txt`; recover with
`--from-job <id>`.

**Why:** One calibration day = one sample; IEEE-QCE reviewers expect run-to-run
variance. 3–5 repeats ≈ 15% of the monthly open-plan quota.

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
scaling figure (`PYTHONPATH=src python scripts/plot_hardware_scaling.py`),
which auto-aggregates all runs. Commit the run dir + judgments + plots.

## Pre-existing: test_gamma_sweep locale failure on Windows

`tests/test_gamma_sweep.py::test_gamma_subfolders_and_topology` reads report.md
via `Path.read_text()` with no encoding; on cp1252 consoles the UTF-8 "γ" reads
as mojibake and the assert fails. Passes with `PYTHONUTF8=1`. Fix is a one-word
change (`read_text(encoding="utf-8")`) — not applied yet because it predates the
hardware-scaling work (surfaced 2026-07-16 during full-suite verification).

## T9 adaptation & fairness pilot — DONE (provisional); follow-ups open

**Done:** Pilot answering "does independent best-response adaptation restore
per-player fairness under noise?" for W N=4. Verdict: no — it equalizes only by
collapsing welfare (p=0: mean 1.00→0.51), fails to converge (p=0.02 limit
cycle), or barely moves anything (p=0.05). Writeup:
`docs/findings/2026-07-05-t9-adaptation-fairness.md`; code `scripts/t9_*.py`;
data `results/t9-pilot/precise-*`.

**Open follow-ups:**
- Aasa to review the adaptation rule — "independent round-robin best response"
  is provisional; simultaneous BR / fictitious play / a fairness-constrained
  rule are alternatives that could change the p=0.02 verdict.
- Extend to N=5 (W N=5 and ring N=5 — the headline asymmetry cases); the pilot
  covers only W N=4.

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
