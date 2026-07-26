# T9 rule sensitivity — is the adaptation verdict an artifact of the rule?

**Date:** 2026-07-26
**Answers:** caveat 1 of `docs/findings/2026-07-05-t9-adaptation-fairness.md`
**Cost:** zero quota (simulation only)

## Why this exists

The T9 pilot's verdict — independent adaptation does not beneficially restore
fairness — rests on a *provisional modeling choice*: independent **round-robin**
best response. The finding's own caveat 1 states the risk plainly:

> "'Independent round-robin best response' is one of several defensible
> adaptation models … A different rule could change the verdict, especially at
> p=0.02."

That is an empirical claim, so it can be tested rather than argued. Item 10 asks
Aasa to sign off on the rule; this run establishes whether the sign-off is
load-bearing or a formality.

## What was tested

Round-robin is **sequential**: a player moving later in a round already sees the
earlier movers' updated strategies. The canonical alternative is **simultaneous**
best response — every player responds to the *same frozen profile* from the
start of the round, and all updates apply together.

Sequencing is precisely the assumption caveat 1 doubts, so removing it entirely
is the sharpest available test. It is also a *fair* test rather than a stacked
one: simultaneous best response is, if anything, **more** prone to oscillation
than sequential, so it cannot flatter the original result.

`scripts/t9_adaptation_pilot.py` gains `simultaneous_best_response_round` and a
`br_round` dispatcher; both harnesses take `--rule {round-robin,simultaneous}`,
defaulting to round-robin so all four committed pilot artifacts reproduce
unchanged (verified).

## Result: the verdict is rule-robust

W, N=4, V=4, C=3, γ=π/2. Baselines are the fixed (Q₄,…,Q₄) profile.

| p | rule | converged? | mean | spread | verdict |
| --- | --- | --- | --- | --- | --- |
| 0.00 | round-robin | no (50-round cap) | 1.0000 → 0.5120 | 0.0000 → 0.0002 | equalized **downward** |
| 0.00 | **simultaneous** | no (15-round cap) | 1.0000 → **0.5105** | 0.0000 → **0.0000** | equalized **downward** |
| 0.02 | round-robin | **no fixed point** (period 10 fwd / 7 rev) | 0.9799 → 0.8808 | 0.0142 → 0.0362 | **neither** |
| 0.02 | **simultaneous** | **no** (residual 3.8e-02 at 15 rounds) | 0.9799 → **0.8892** | 0.0142 → **0.1105** | **neither** |
| 0.05 | round-robin | yes (5 rounds) | 0.9593 → 0.9449 | 0.0140 → 0.0118 | **neither** |
| 0.05 | **simultaneous** | yes (6 rounds) | 0.9593 → **0.9450** | 0.0140 → **0.0128** | **neither** |

**All three verdicts are identical under both rules.** At p=0 the two rules land
on a mean of 0.5120 vs 0.5105 (0.15% apart); at p=0.05, 0.9449 vs 0.9450 (1e-4
apart) with the same convergence behaviour.

## The p=0.02 case specifically

This is the case caveat 1 singled out, and it is the one where the rules could
most plausibly have disagreed. They do not.

Under simultaneous updates the residual maximum unilateral gain sits at
**3.8e-02 — roughly 380× the 1e-4 convergence bar — and does not trend
downward**: rounds 2–15 read 3.1, 2.8, 3.6, 3.1, 2.8, 1.9, 2.6, 2.4, 3.4, 3.5,
3.1, 3.6, 3.9, 3.8 (×10⁻²). Best response simply does not settle.

**Conclusion: the p=0.02 non-convergence is a property of the noisy
best-response map, not of the move order.** Removing sequencing entirely does
not remove it. Caveat 1's specific worry is not supported.

## A distinction the original pilot did not draw

The two non-convergent cases fail for *different reasons*, visible in the
residual-gain trajectory under simultaneous updates:

- **p=0** — the residual decays monotonically (2.2e+00 → 3.4e-04 over 15 rounds).
  This is **slow convergence**, not a cycle; it is heading to the equalized-down
  fixed point and simply has not arrived inside the budget.
- **p=0.02** — the residual is **flat** at 2–4e-02 with no trend. There is no
  fixed point to arrive at.

The original pilot reported both as "did not converge" against a round cap. They
are not the same phenomenon, and the distinction matters: noise at p=0.02
destroys the fixed point rather than merely slowing the approach to it.

## Honest limits

1. **The simultaneous runs are bounded at 15 rounds** (`--rounds`, new), against
   round-robin's 50-round cap at p=0 and a ~3-period cycle characterization at
   p=0.02. Hitting a cap is reported as non-convergence either way, so a smaller
   budget can only ever **under**-claim convergence — it cannot manufacture the
   cycle. The qualitative verdicts are therefore sound.
2. **The p=0.02 magnitudes are not like-for-like.** Round-robin's mean/spread are
   time-averages over characterized periods; simultaneous's are a 15-round
   snapshot of an uncharacterized trajectory. Simultaneous *looks* worse on
   spread (0.111 vs 0.036) but confirming that would need the same
   cycle-characterization treatment. **Do not quote that comparison as a
   magnitude result.**
3. **Only W N=4 is covered** by *this* run, unchanged from the original pilot.
   Caveat 2 (W N=5, ring N=5) was closed separately the same day —
   `docs/findings/2026-07-26-t9-caveat2-n5-ring.md`. W N=5 reproduces these
   verdicts; ring N=5 never converges and fails in a different direction
   (spread grows from a perfectly fair baseline at conserved mean welfare). The
   simultaneous-rule cross-check above has *not* been extended to those cells.
4. **Two rules, not all rules.** Fictitious play and regret matching are still
   untested. Simultaneous was chosen because it isolates the sequencing
   assumption; a belief-based rule like fictitious play is a genuinely different
   model and could still differ.

## What this means for item 10

The sign-off question was "is the round-robin rule doing the work?" For the
sequential-vs-simultaneous axis the answer is **no** — the verdict, the
non-convergence at p=0.02, and the downward equalization at p=0 all survive
removing sequencing.

That does not close item 10, which remains Aasa's call. It changes what the call
requires: from adjudicating a modeling choice in the abstract to confirming a
result that has been shown not to depend on the most suspect part of that
choice.

## Reproduction

```bash
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py w 4 0.00 --rule simultaneous --rounds 15
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py w 4 0.02 --rule simultaneous --rounds 15
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py w 4 0.05 --rule simultaneous
```

Artifacts (each records `config.rule = "simultaneous"`):
- `results/t9-pilot/precise-2026-07-26T0844Z-p0-simul/results.json`
- `results/t9-pilot/precise-2026-07-26T0838Z-p0.02-simul/results.json`
- `results/t9-pilot/precise-2026-07-26T0825Z-p0.05-simul/results.json`

An earlier set of these three was generated and **discarded**: the results JSON
carried duplicate `"rule"` and `"max_rounds"` keys, and the later literal —
a hardcoded `"independent round-robin best response (provisional)"` — silently
won, so every artifact claimed round-robin regardless of what ran. The numbers
were correct and the optimizer is deterministic, so patching the field would
have produced an identical file; they were regenerated instead, because
committing an artifact that misstates how it was produced is the thing this
repo refuses to do elsewhere. The duplicate keys are fixed in
`scripts/t9_precise_rerun.py`. Regeneration reproduced every value exactly
(p=0.05: 0.9450/0.0128; p=0.02: 0.8892/0.1105; p=0: 0.5105/0.0000).
