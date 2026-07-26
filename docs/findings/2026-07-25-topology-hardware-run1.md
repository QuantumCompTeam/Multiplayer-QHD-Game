# Topology/equilibrium/fairness hardware batch, run 1 on ibm_fez

**Date:** 2026-07-25
**Job:** `d9ia1pd0k0jc738jaqgg` (ibm_fez, 49 pubs x 4096 shots, 55 QPU-seconds)
**Run:** `results/hardware-scaling/../hardware-topology/2026-07-25T114621Z/`
**Registration:** `results/hardware-topology/preregistration.json`, frozen in
commit `46f43d4` — **before** submission. Judgments:
`results/hardware-topology/2026-07-25T114621Z/judgments.json`
(`scripts/judge_topology_run.py`, which refuses to run unless the registration
is byte-identical to HEAD).

This is the first hardware run in the repo that is **not** GHZ-only. It puts
the topology axis, the restricted-menu equilibrium claim, the position-locked
unfairness claim and the gamma transition on device data.

## Headline

Four of the five registered tests **PASS**. The fifth (T4, per-cell advantage)
**FAILS in both of its registered forms**, and its failure is additionally
**confounded** by a mid-day recalibration — see "The confound" below, which is
the most important caveat in this document and must be read before any T4
number is quoted.

| test | claim | verdict |
| --- | --- | --- |
| T1 | all three unilateral Hawk deviation gaps at ghz N=3 are >= 0 | **PASS** |
| T2 | the deviation gap changes sign across the gamma sweep | **PASS** |
| T3 | star N=4's per-player payoffs are invariant under wiring permutation | **PASS** |
| T4a | device noise model as-is predicts per-cell advantage | **FAIL** (1/23, rms z 7.79) |
| T4b | same + cz-linear bias correction fitted on GHZ | **FAIL** (13/23, rms z 6.52) |
| T5 | ring N=4 is the smallest, positive, ZNE-corrigible cell | **PASS** |

## The confound (read before quoting any T4 number)

**ibm_fez recalibrated between registration and submission, and the batch ran
on different physical qubits than the registration predicted for.**

| | registration | execution |
| --- | --- | --- |
| calibration stamp | 2026-07-25 08:15:48+05:30 | 2026-07-25 16:05:46+05:30 |
| pinned set | `[20, 21, 22, 23, 24]` | `[137, 147, 146, 145, 144]` |
| sum cz error | 0.01327 | 0.00931 |
| sum readout error | 0.0245 | 0.0215 |
| mean T1 / T2 | 145.3 / 129.8 us | 124.1 / 89.5 us |

`find_pinned_set` selects the lowest-error chain from *live* calibration, so a
recalibration between the two runs silently moved the qubit set. The executed
chain is **better on gates and readout but worse on coherence**, so this is not
a one-way bias that can be argued away in a known direction.

**Consequence, stated plainly:** T4's z-scores conflate three distinct sources —
device-model error, calibration drift, and a different physical qubit set. T4
therefore does **not** cleanly test what it was registered to test, and the
comparison "T4b beats T4a" must not be reported as a clean model comparison.

**T1, T2, T3 and T5 are unaffected.** Every one of them is a *within-batch,
within-job* comparison: a payoff difference between two profiles measured on
the same qubits in the same job, a wiring permutation against its own twin in
the same job, or one cell ranked against the other eleven in the same job. The
design note in commit `add4378` argued the extra axes had to ride in the same
job because "the pinned set moves between calibration days". That reasoning
paid off in a way it did not anticipate: the pinned set moved *within a single
day*, and the differential tests survived it intact while the absolute test did
not.

This is a pipeline defect, not a physics result. See "What to fix" below.

## T1 — restricted-menu equilibrium at N=3 GHZ: PASS

Gap = `payoff_k(Q,Q,Q) - payoff_k(H at position k)`, mitigated, fold 1,
gamma = pi/2. A gap >= 0 means the unilateral Hawk deviation does not pay.

| deviator | predicted | measured | sigma | z | verdict |
| --- | --- | --- | --- | --- | --- |
| position 0 (HQQ) | +0.3310 | **+0.2895** | 0.0273 | −1.52 | PASS |
| position 1 (QHQ) | +0.3259 | **+0.2726** | 0.0272 | −1.96 | PASS |
| position 2 (QQH) | +0.3236 | **+0.3512** | 0.0272 | +1.01 | PASS |

All three gaps are positive and many sigma clear of zero. **The restricted-menu
`{D,H,Q}` equilibrium at N=3 GHZ is now hardware-verified**, not simulation-only.

This does **not** establish a full-SU(2) equilibrium; the menu restriction in
`paper/REVIEW-NOTES.md` "Scope and metric checks" stands unchanged.

Note that all three measured gaps are *closer to zero* than predicted (two of
three negative z), consistent with the device being noisier than the model —
the same direction as T4a, and the reason the gaps are still comfortably
positive is that a difference of two payoffs cancels common-mode noise.

## T2 — gamma drives the equilibrium transition: PASS

Same gap, position 0, swept in gamma. `results/gamma-sweep/N3` shows the
*cooperative payoff* is 1.333333 at every gamma, so the gap — not the payoff —
is the quantity gamma actually moves.

| gamma | ideal | predicted | measured | registered as |
| --- | --- | --- | --- | --- |
| 0.30 pi | −0.7031 | −0.6938 | **−0.6877** | significantly negative — confirmed |
| 0.40 pi | +0.0469 | +0.0485 | **+0.0067** | MARGINAL, not counted |
| 0.45 pi | +0.2599 | +0.2564 | **+0.2467** | significantly positive — confirmed |
| 0.50 pi | +0.3333 | +0.3310 | **+0.2895** | positive |

The registered sign change reproduced. The cooperative profile is **not** an
equilibrium at gamma = 0.30 pi and **is** one at gamma >= 0.45 pi, measured on
hardware.

The 0.40 pi point deserves note: it was registered as MARGINAL in advance
(predicted +0.0485, within ~2 sigma of zero) and explicitly excluded from
pass/fail. It came back at **+0.0067** — statistically indistinguishable from
zero. Registering it as marginal *before* seeing it is what makes that
statement credible rather than post-hoc. The crossing sits very close to
0.40 pi.

Scope limit, stated honestly: all four points are one cell (ghz N=3) and one
deviator position. T2 is evidence about gamma at N=3 GHZ, not evidence that the
transition generalises across topologies.

## T3 — position-locked unfairness is topology-locked, not qubit-locked: PASS

star N=4 per-player payoffs, mitigated, fold 1. Player 0 is the hub.

| wiring | per-player payoffs | max dev vs identity | threshold | verdict |
| --- | --- | --- | --- | --- |
| ideal | `[0.25, 1.25, 1.25, 1.25]` | — | — | — |
| `[0,1,2,3]` | `[0.3527, 1.2021, 1.2124, 1.2019]` | — | — | — |
| `[1,2,3,0]` | `[0.3360, 1.2171, 1.2176, 1.2121]` | 0.0167 | 0.0572 | PASS |
| `[3,2,1,0]` | `[0.3370, 1.2368, 1.1986, 1.2119]` | 0.0346 | 0.0572 | PASS |

**The hub loses ~0.34 while every leaf earns ~1.21, and this does not move when
the players are permuted across physical qubits.** The unfairness is a property
of the entanglement topology — of *which graph position you occupy* — and not
of which qubit you were handed. This is the hardware control that
`paper/REVIEW-NOTES.md:38` asked for ("Run the W-topology/wiring-permutation
hardware control, or explicitly defer it and narrow the player-position
claim"); it ran, and the claim holds.

Honest note on test strength: I judged this test "weak" at registration time
because the predicted deviations (0.0034, 0.0045) sat ~13x below threshold. The
measured deviations are 0.0167 and 0.0346 — 5-8x larger than predicted, with
the second at 60% of the threshold. The test was **more discriminating than I
gave it credit for**, though a genuinely sharp version would need a threshold
set from measured device inhomogeneity rather than from a simulated prediction.

## T4 — per-cell advantage: FAIL in both registered forms

Registered as a two-model race. Both fail; see "The confound" before reading
anything into the margin.

| | T4a (model as-is) | T4b (cz-corrected) |
| --- | --- | --- |
| series passing \|z\| <= 1.96 | 1 / 23 | 13 / 23 |
| rms z | 7.79 | 6.52 |

**T4a's registered expectation was that it would fail low and systematically.
It did.** 22 of 23 cells measured *below* prediction. The single positive-z cell
is ring N=4 (+10.95) — and ring N=4 is the inverted cell where extra noise
*raises* advantage, so it too is consistent with "the device is noisier than
the model". All 23 cells point the same way. That much survives the confound,
because it is a statement about sign, not magnitude.

**T4b's substantive claim — that the bias is a property of gate count and
transfers across topologies — is not supported in its linear form.** The
structure of the residuals is informative:

| routed cz | cells | T4b z |
| --- | --- | --- |
| 4–10 (inside the 6–14 fit range) | ghz N=3 variants, star N=3/4, ring N=3, fc N=3 | −1.7 … +2.4, mostly passing |
| 14–42 (extrapolated) | ghz N=5 +5.49, star N=5 +9.19, ring N=5 +14.38, fc N=4 +11.78, **w N=3 +11.70** | systematically over-corrected |

Inside the fitted range the correction works; beyond it, the linear form
over-corrects badly. **The bias saturates rather than growing linearly in cz.**
W N=3 at 42 cz was registered in advance as "the sharpest discriminator" at a
3x extrapolation — it discriminated, and it falsified the linear model.

That conclusion is *directionally* robust to the confound (the over-correction
is far too large and too cz-ordered to be explained by a chain swap), but its
magnitude is not, and it should be re-tested on a run whose chain matches its
registration before it enters the paper.

**One outlier worth flagging:** ghz N=3 `QQH` at 6 cz measured 0.9719 against
0.9953 predicted (z = −22.0), far off its siblings `QQQ` 0.9886, `QHQ` 0.9950,
`HQQ` 0.9927 at comparable cz. That profile puts the deviating player on the
last qubit of the chain. Its *gap* (T1 position 2) was nonetheless the best of
the three at +0.3512 — a clean illustration of why differential tests survive
what absolute tests do not.

## T5 — ring N=4, the cell where noise creates advantage: PASS

ring N=4's noiseless circuit is deterministic on `|1111>` — all-Hawk, **zero
advantage on a perfect device**. All three registered sub-claims hold:

| sub-claim | result |
| --- | --- |
| (a) smallest advantage of the 12 topology cells | **yes** (0.0894 vs 0.59–0.99) |
| (b) positive, i.e. noise moves it *toward* advantage | **yes** (+0.0894 mitigated, +0.1137 raw) |
| (c) ZNE pulls it back toward its zero ideal | **yes** (+0.1137 raw -> +0.0367 ZNE) |

Predicted +0.0557 mitigated against +0.0894 measured: the effect is *stronger*
on hardware than the noise model expected, which is the same "device is noisier
than modelled" direction as everywhere else. A cell whose advantage is
manufactured entirely by decoherence, and which ZNE correctly extrapolates back
toward zero, is a sharp demonstration that the ZNE pipeline is not simply
inflating every number it touches.

## What to fix before Task 9

1. **Pin the qubit set from the registration.** `find_pinned_set` must not be
   allowed to silently re-select between registration and submission. Either
   pass the registered pinned set explicitly, or refuse to submit when the live
   selection differs from the registered one and require an override. Without
   this, T4 is untestable on every future run and the same confound recurs.
2. **Re-test T4 on a chain-matched run** before any T4 conclusion enters
   `paper/main.tex`. The cz-saturation result is interesting enough to be worth
   a clean measurement.
3. The `git.dirty: true` on this run is the known benign case
   (`dirty_files` is exactly the two crash-safety writes,
   `pending_jobs.txt` and `pending-<id>-calibration.json`). Real fix belongs in
   plan Task 10.

## Paper impact

- **Sec. IV-C position-locked unfairness** can be promoted from simulation-only
  to simulation-plus-hardware (plan Task 11 Step 2). T3 is the control
  `REVIEW-NOTES.md:38` required.
- **The N=3 restricted-menu equilibrium** can be stated as hardware-verified in
  the abstract, Sec. IV and the conclusion (plan Task 11 Step 3). T1 passed at
  all three deviation positions.
- **The gamma transition** is now a hardware result at N=3 GHZ, with the
  crossing bracketed near 0.40 pi.
- **No T4 number should enter the paper from this run** until the chain-matched
  re-test in item 1 above.
