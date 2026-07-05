# TODOS

Deferred work with enough context to pick up cold. Ordered newest-first.

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
