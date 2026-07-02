# TODOS

Deferred work with enough context to pick up cold. Ordered newest-first.

## Faithful gate-level W entangler

**What:** Build a real gate-level circuit for the W-state EWL entangler `J_W(γ) =
cos(γ/2)·I + i·sin(γ/2)·S_W`, instead of transpiling the dense `S_W` reflection
matrix.

**Why:** RQ3's headline is "does GHZ collapse faster than W under noise." In the
Month-4 noise analysis, GHZ gets a faithful gate-level circuit (O(N) real gates)
but W falls back to a transpiled dense unitary whose gate count is a synthesis
artifact, not a physical W-prep circuit. So the single most important comparison in
the paper rests on the least faithful circuit. A faithful W makes the GHZ-vs-W
robustness claim reproducible and defensible.

**Current state:** Month-4 spec (`docs/superpowers/specs/2026-07-01-noise-analysis-design.md`,
decision D2/1A) ships W via the transpiled-unitary fallback, pinned to the {u,cx}
basis at a fixed optimization_level, with every W noise result labelled
"approximate." `w_entangler` lives in `src/circuits/topologies.py:190`; its
gamma-interpolation semantics (the |0…0⟩↔|W⟩ reflection) are already flagged for
physics review in the docstring.

**Where to start:** The standard W-state *prep* circuit is an Ry + cascaded-CNOT
chain, but that prepares |W⟩ from |0…0⟩ — it is NOT the same as the EWL `S_W`
reflection operator. Deriving a compact gate sequence for `exp(i·γ/2·S_W)` (or
redefining the W entangler to a physically-motivated construction) is the research
task. Confirm the intended physics first.

**Depends on:** Month-4 noise analysis landing (it defines the comparison this
improves).

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
