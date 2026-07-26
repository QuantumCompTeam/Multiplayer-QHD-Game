# T9 caveat 2 — does the adaptation verdict survive N=5 and the ring?

**Date:** 2026-07-26
**Answers:** caveat 2 of `docs/findings/2026-07-05-t9-adaptation-fairness.md`
(and honest-limit 3 of `docs/findings/2026-07-26-t9-rule-sensitivity.md`)
**Cost:** zero quota (simulation only)

## Why this exists

The T9 pilot covered exactly one cell: **W, N=4**. Its own caveat 2 named the
gap:

> "Extend to N=5 (W N=5 and ring N=5 — the headline asymmetry cases); the pilot
> covers only W N=4."

The rule-sensitivity run (2026-07-26) closed caveat 1 by showing the verdict does
not depend on move order, but it inherited the same single cell. So the standing
question for item 10 was whether "independent adaptation does not beneficially
restore fairness" is a property of the adaptation map or an accident of W N=4.

Six configurations: `{w, ring} x N=5 x p in {0, 0.02, 0.05}`, round-robin rule,
precise optimizer, 50-round cap, V=4, C=3, γ=π/2. Baselines are the fixed
(Q₅,…,Q₅) profile. No code change was needed — both T9 harnesses were already
parameterised on topology and N.

## Result 1: W N=5 reproduces W N=4 verdict-for-verdict

| p | baseline mean/spread | adapted mean/spread | converged? | verdict |
| --- | --- | --- | --- | --- |
| 0.00 | 0.8000 / 0.0000 | **0.4107** / 0.0001 | yes (3 rounds) | equalized **downward** |
| 0.02 | 0.7885 / 0.0753 | 0.7627 / 0.0673 | no (50-round cap, residual 8.9e-03) | **neither** |
| 0.05 | 0.7819 / 0.0125 | 0.7805 / 0.0091 | yes (4 rounds) | **neither** |

Against W N=4 (round-robin, from the pilot): p=0 equalized downward
(1.0000 → 0.5120), p=0.02 neither / no fixed point, p=0.05 neither / converged.
**All three verdicts are identical at N=5.** The p=0 case still collapses welfare
to buy equality — here to 51.3% of baseline, against 51.2% at N=4.

One difference, and it favours nothing: W N=4 p=0 did *not* converge inside 50
rounds (the rule-sensitivity run identified it as slow convergence, not a cycle),
whereas W N=5 p=0 converges in 3. The destination is the same; N=5 simply gets
there faster.

## Result 2: the ring is qualitatively worse — adaptation *manufactures* unfairness

| p | baseline mean/spread | adapted mean/spread | converged? | residual gain at cap |
| --- | --- | --- | --- | --- |
| 0.00 | 0.8000 / **0.0000** | 0.8000 / **1.3329** | no | **3.83e+00** |
| 0.02 | 0.7890 / 0.0149 | 0.7812 / **0.7640** | no | 1.74e+00 |
| 0.05 | 0.7836 / 0.0136 | 0.7784 / **0.4214** | no | 5.01e-01 |

Ring N=5 never converges, at any noise level, and the verdict is **NEITHER** in
all three cases. Three structural observations, each robust to the snapshot
caveat below:

1. **Adaptation destroys fairness rather than failing to restore it.** The ring
   baseline at p=0 is *perfectly* fair (all five players at exactly V/N = 0.8,
   spread 0.0000). Best response drives spread to 1.3329 — the endpoint payoff
   vector is `[0.000, 1.3329, 0.1774, 1.3329, 1.1568]`, with player 0 at zero.
   The pilot's W N=4 story was "equality bought by collapsing welfare"; the
   ring's is the opposite failure, and a worse one.

2. **Mean welfare is exactly conserved while inequality explodes.** At p=0 the
   mean is 0.800000 before and 0.800000 after, to six figures. This is pure
   redistribution — best response reshuffles a fixed pot rather than shrinking
   it. That is a different mechanism from the W p=0 collapse and the pilot did
   not exhibit it.

3. **Noise damps the oscillation instead of causing it.** Residual gain at the
   cap falls monotonically with p (3.83 → 1.74 → 0.501) and so does induced
   spread (1.3329 → 0.7640 → 0.4214). The divergence is *strongest noiselessly*.
   Combined with W N=5 p=0 converging in 3 rounds, this isolates the cause:
   **topology, not noise, drives the ring's non-convergence.** That is the
   paper's own thesis showing up on the adaptation axis.

The p=0 trajectory is a clean oscillation, not a slow drift: `max_gain` sits at
exactly 2.000e+00 for rounds 1–7 with `prob_delta` at 1.414 (=√2) — best response
is flipping between deterministic basis outcomes. Recovered θ values are
multiples of π (player 0 at π, player 1 at 0, player 3 at 7π, player 4 at 2π),
i.e. players bouncing between D-like and H-like pure strategies.

## Honest limits

1. **Every ring endpoint is a 50-round snapshot of a non-convergent trajectory.**
   The spread magnitudes (1.3329 / 0.7640 / 0.4214) are **not** fixed-point
   properties and must not be quoted as magnitude results. What is sound is the
   qualitative content: non-convergence, the sign of the spread change, and the
   exact conservation of the mean at p=0. This is the same limit as
   honest-limit 2 of the rule-sensitivity finding.
2. **The ring cycles are not period-characterized.** `scripts/t9_cycle_characterize.py`
   did that for W N=4 p=0.02; the equivalent has not been run here, so "period
   2" is not claimed despite the √2 signature inviting it.
3. **Round-robin only.** The simultaneous-rule cross-check exists only at W N=4.
   Its conclusion — that the verdict is not a sequencing artifact — is evidence
   about the map, not a proof transferable to the ring, whose non-convergence is
   far more violent and where simultaneous updates are if anything more prone to
   oscillation.
4. **Two topologies at N=5, not five.** Star and fully-connected at N=5 are
   untested. W and ring were chosen because they are the headline asymmetry
   cases named by caveat 2.

## What this means for item 10

Caveat 2 is **answered, and the pilot's verdict strengthens rather than
weakens.** "Independent best-response adaptation does not beneficially restore
per-player fairness" now holds across two topologies and two player counts, by
three distinct failure modes:

- **W, p=0** — equality purchased by collapsing welfare to ~51% (both N=4 and N=5).
- **W, p>0** — barely moves anything, or fails to settle.
- **ring, all p** — never settles, and converts a perfectly fair allocation into
  an extremely unfair one at constant mean welfare.

Both caveats the pilot raised against its own verdict have now been tested and
neither is supported. Item 10 remains Aasa's call, but the call is now about
confirming a verdict that has survived removing the sequencing assumption
(caveat 1) and widening past the single W N=4 cell (caveat 2) — not about
adjudicating a modeling choice on one configuration.

The fairness paragraph in Sec. IV-C stays hedged as exploratory until sign-off;
nothing in this finding changes the paper text, and the ring numbers are
deliberately not promoted into it given limit 1.

## Reproduction

```bash
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py w 5 0.00
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py w 5 0.02
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py w 5 0.05
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py ring 5 0.00
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py ring 5 0.02
conda run -n entangled-equilibria python -u scripts/t9_precise_rerun.py ring 5 0.05
```

Artifacts:
- `results/t9-pilot/precise-2026-07-26T0904Z-w5-p0/results.json`
- `results/t9-pilot/precise-2026-07-26T0952Z-w5-p0.02/results.json`
- `results/t9-pilot/precise-2026-07-26T0908Z-w5-p0.05/results.json`
- `results/t9-pilot/precise-2026-07-26T0916Z-ring5-p0/results.json`
- `results/t9-pilot/precise-2026-07-26T0927Z-ring5-p0.02/results.json`
- `results/t9-pilot/precise-2026-07-26T0928Z-ring5-p0.05/results.json`

**Naming change.** These directory names carry a `<topology><N>` segment that
earlier ones do not. The old format was `precise-<stamp>-p<p>`, which encodes
neither topology nor N — harmless while every run was W N=4, but `w 5 0.00` and
`ring 5 0.00` completing in the same UTC minute would have resolved to an
identical path and silently overwritten one another. `scripts/t9_precise_rerun.py`
now includes both fields. Directories written before this change keep their old
names and are all w4.
