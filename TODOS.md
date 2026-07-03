# TODOS

Deferred work with enough context to pick up cold. Ordered newest-first.

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
