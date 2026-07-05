# T9 — Does adaptation restore per-player fairness under noise?

**Status: EXPLORATORY PILOT — PROVISIONAL.** The adaptation rule below
(independent round-robin best response) is a modeling choice pending Aasa's
game-theory sign-off. Treat the numbers as a directional pilot, not a locked
result. This finding is deliberately kept **out of the README §9 results table**
(which holds validated results) until the rule is reviewed.

## Question

The Month-4 noise analysis established a *noise-induced per-player asymmetry*:
under gate-level depolarizing noise the fixed cooperative profile (Q_N,…,Q_N)
pays players unequally, and the ring N=5 case has that disadvantage
**position-locked** to the entangler's circuit position (see
`scripts/asymmetry_diagnostics.py` and README §9). T9 asks the natural
follow-up:

> If each player is allowed to **adapt** their own strategy under the same noisy
> circuit, does the per-player payoff spread collapse (**fairness restored**),
> does only the group mean recover while the spread persists (**mean rescued**),
> or **neither**?

This rescopes the original T9 line ("noise-aware strategy optimization", still
deferred as a *symmetric-Q* config-harness feature — see `TODOS.md`) into a
concrete, testable dynamics question.

## Method

- **System:** W entangler, N=4, V=4, C=3, γ=π/2 — the cleanest asymmetric
  noisy case. Baseline is the fixed (Q₄,…,Q₄) profile whose per-player payoffs
  are anchored to the locked run `results/noise-robustness/2026-07-03T0213Z`.
- **Adaptation rule (PROVISIONAL):** independent best response, round-robin over
  players 0..N−1. Each player globally maximizes *their own* expected noisy
  payoff over their own (θ, α, β), holding all others fixed; iterate rounds
  until the induced noisy probability vector stops moving (same gauge-invariant
  criterion as `game.strategy_opt.nash_strategy`) or the map is detected cycling.
  Non-convergence is reported as-is, never forced into a converged number.
- **Reused, validated paths (unchanged):** `build_ewl_circuit_noisy`
  (per-gate depolarizing), `expected_payoff`, and the shared multi-start
  Nelder–Mead + L-BFGS-B optimizer `game.strategy_opt._maximize`. Precise
  optimizer resolution throughout (the pilot's `--fast` path is not used for any
  number quoted here).
- **p=0 control matters:** (Q_N,…,Q_N) is *not* a Nash equilibrium for the W
  entangler even noiselessly, so adaptation moves at p=0 too. Only the
  *difference* between the p=0 adapted profile and the p>0 adapted profiles is
  attributable to noise.
- **Confound check:** each interesting case is rerun with reverse move order
  (N−1..0) to test whether any residual disadvantage follows *move order* rather
  than *circuit position*.

## Results

| p | baseline mean / spread | adapted mean / spread | converged? | verdict |
|---|---|---|---|---|
| 0.00 | 1.0000 / 0.0000 | 0.5120 / 0.0002 | no (50-round cap) | **fairness "restored" but equalized DOWNWARD** — spread ~0 only because everyone defects to a far lower mean |
| 0.02 | 0.9799 / 0.0142 | **limit cycle** (time-avg 0.8808 / 0.0362) | **no fixed point** | **neither** — mean *falls* and spread *widens*; best response never settles |
| 0.05 | 0.9593 / 0.0140 | 0.9449 / 0.0118 | yes (5 rounds) | **neither** — adaptation changes almost nothing |

**The p=0.02 limit cycle.** Best-response dynamics have no fixed point at p=0.02:
they settle onto a payoff limit cycle with residual unilateral gains that never
approach the 1e-4 convergence bar. Characterized over ~3 periods with a fixed
round budget:

- forward order (0..3): period **10**, time-avg mean 0.8808, time-avg spread
  0.0362, per-player time-avg [0.9045, 0.8710, 0.8715, 0.8762]
- reverse order (3..0): period **7**, time-avg mean 0.8813, time-avg spread
  0.0392, per-player time-avg [0.9078, 0.8720, 0.8714, 0.8739]

The period depends on move order but the *shape* does not: player 0 stays the
best-off and the mean/spread time-averages agree to ~1e-3 across both orders —
so the cycle is a real property of the noisy best-response map, not an artifact
of the sweep direction.

## Interpretation (provisional)

Independent, selfish adaptation **does not beneficially restore fairness** at any
noise level tested:

- at **p=0** it equalizes only by collapsing collective welfare (mean 1.00 →
  0.51) — the "fair" outcome is everyone worse off;
- at **p=0.02** it *fails to converge at all*, and the time-averaged state is
  both **less fair** (spread 0.014 → 0.036) and **lower welfare** (mean 0.98 →
  0.88) than the fixed cooperative baseline;
- at **p=0.05** it converges but rescues neither (mean and spread essentially
  unchanged).

This is consistent with, and complements, the position-locked asymmetry finding:
the per-player disadvantage under noise is a **structural feature of the
entangler circuit**, not a coordination failure that self-interested players
would adapt away. If anything, letting players best-respond makes the group
worse off — a quantum-game analogue of a price-of-anarchy effect under noise.

## Open items / caveats

1. **Modeling rule pending review.** "Independent round-robin best response" is
   one of several defensible adaptation models (simultaneous best response,
   fictitious play, regret matching, a welfare-aware or fairness-constrained
   rule). Aasa's sign-off on the rule is required before any of this is quoted
   as a result. A different rule could change the verdict, especially at p=0.02.
2. **Scope.** Only W, N=4 is covered. The headline asymmetry (W N=5, two players
   negative; ring N=5) is *not* tested here. Extending to N=5 is the obvious next
   step but was left out of the pilot deliberately to keep cost bounded.
3. **Relation to the deferred TODO.** The `TODOS.md` "noise-aware strategy
   optimization" item (make `strategy_mode = cooperative|nash` run under noise
   for the *symmetric* Q) is a different, still-open feature; this pilot does not
   close it.

## Reproduction

Pinned env `entangled-equilibria` (qiskit 1.3.2, aer 0.14.2, numpy 1.26.4):

```bash
# precise reruns (convergent cases)
python scripts/t9_precise_rerun.py w 4 0.00
python scripts/t9_precise_rerun.py w 4 0.05
# the p=0.02 limit cycle (fixed round budget, both move orders)
python -u scripts/t9_cycle_characterize.py w 4 0.02 --rounds 35
python -u scripts/t9_cycle_characterize.py w 4 0.02 --rounds 20 --reverse-order
# re-run cycle analysis only, no simulation:
python scripts/t9_cycle_characterize.py --analyze <outdir>
```

Committed result artifacts (canonical set; `--fast` pilot runs and run logs are
intentionally not tracked):

- `results/t9-pilot/precise-2026-07-04T0433Z-p0/results.json`
- `results/t9-pilot/precise-2026-07-04T0401Z-p0.05/results.json`
- `results/t9-pilot/precise-cycle-2026-07-04T0509Z-p0.02/results.json`
- `results/t9-pilot/precise-cycle-2026-07-04T0509Z-p0.02-rev/results.json`
