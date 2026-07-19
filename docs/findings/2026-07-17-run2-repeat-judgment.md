# Run 2 repeat judgment: N=5 deficit reproduces on ibm_fez

**Date:** 2026-07-17
**Source:** `results/hardware-scaling/repeat-judgments.json` (generated 2026-07-17T01:45:51Z)

Numbers in the primary, ranking, and per-player sections are read directly from
that file. The two claims that come from elsewhere (the failed first submission,
and the position of this run against the cross-day target) are marked inline
with their source.

## Run identity

| field | value |
| --- | --- |
| run | 2026-07-17T014458Z |
| job_id | d9cohq1htsac739c1iu0 |
| backend | ibm_fez |
| created_utc | 2026-07-17T01:44:58.964811+00:00 |
| chain | [59, 75, 74, 73, 79] |
| is_registration_source | false |
| p_eff_refit | 0.0016456338927582697 |
| commit | a936f17 |

The JSON records `backend` as ibm_fez for both judged runs. Registration central
value for comparison: `p_eff_central` = 0.001837649512845019, registered
2026-07-16T17:04:36Z.

## Primary conditional test

**N=5 reproduces the deficit.** Measured conditional +0.5846250840823848
against a predicted conditional of +0.5938528682272297, delta
-0.00922778414484493, z = -4.743563751102674, sigma_predictive
0.0019453273169776348, `pass_95` false. The JSON records run 1's registered
values as delta -0.010050998350082052 and z = -5.166738914507109, with
`same_sign_as_run1` set to true.

**N=4 passes.** Measured +0.7415761349129972 against a predicted conditional of
+0.7434293298233563, delta -0.0018531949103590684, z = -0.9323557046622736,
`pass_95` true.

The secondary unconditional checks split the same way: both N=4 variants
(`mitigated_fold1`, `zne_linear`) fall inside their 95% predictive intervals in
run 2, and both N=5 variants fall below theirs.

## Five-model ranking, both runs labelled

Run 1 is 2026-07-16T074134Z, the registration source. Run 2 is
2026-07-17T014458Z, this run. Scores are `scores_z2`, lower is better.

| model | run 1 score_z2 | run 2 score_z2 |
| --- | --- | --- |
| cz_exponential | 10.032095975636892 | 7.399852402490573 |
| transpiled_count_corrected | 29.93261198678005 | 22.25480363450175 |
| p_eff_primary | 31.29551915456605 | 23.37068422079156 |
| device_model_anchored | 38.862284568361446 | 27.563697136876158 |
| constant_retention | 46.03168503448163 | 34.410774522717176 |

`ranking_best_first` is identical in the two runs:

    cz_exponential, transpiled_count_corrected, p_eff_primary,
    device_model_anchored, constant_retention

cz-exponential ranks first in both. Every model's score improves in run 2 and
the relative order does not move.

The JSON attaches its own scoping note to this block: these are item-4
registered model-comparison scores on the shared sigma yardstick, separate from
the primary p_eff test above.

## Per-player floor (N=5, run 2, mitigated)

Per-player advantages: 0.5660502563047922, 0.5686312446217308,
0.5693112326199914, 0.5841782080462852, 0.634954478819125.

Worst player advantage +0.5661, spread 0.0689, `any_player_below_classical`
false. That flag is also false for N=3 and N=4 in this run, raw and mitigated.

## What this run does and does not add

**On the sharp question, reproduced 1 of 1.** The registered falsification
question asked whether the N=5 conditional deficit would reappear in a fresh
execution judged against the frozen predictions. It did, same sign, comparable
magnitude, and the judge's `same_sign_as_run1` flag confirms it.

**On the cross-day target, this is 1 calibration day, not 2.** Run 2 carries
`calibration_last_update` = 2026-07-16 08:30:13+05:30, identical to run 1's,
and sets `distinct_calibration_vs_previous_runs` to false. The stamp is
unchanged despite the ibm_fez maintenance window that fell between the two
submissions. The first submission of this batch, job d9chh0qneu4c739lvgb0,
failed backend-side during that maintenance (error 9603, RF hardware, 0 quantum
seconds billed) and was resubmitted as the job judged here; that history is
recorded in `TODOS.md`, under the heading "## Hardware scaling repeat runs
(cross-day error bars)" in the Run 2 progress bullet containing
"d9chh0qneu4c739lvgb0 failed backend-side" — not in the JSON.

So against the 3-5 cross-day target, the count stands at **1 of 3-5 calibration
days**. What run 2 establishes is execution-level repeatability of the deficit
on a single calibration. It does not yet speak to calibration-to-calibration
variance, which is the thing the cross-day target exists to measure. Runs 3
onward should have their calibration stamp checked before being counted toward
that target.

## Player index 4

The top per-player payoff in the N=5 block sits at player index 4, the last
position on the chain, in both hardware runs and in both the raw and mitigated
folds. Run 1 gives +0.6146158854166668 raw and +0.6222582829075554 mitigated;
run 2 gives +0.6275878906249999 raw and +0.634954478819125 mitigated.

Mitigated per-player advantage vectors, N=5, both runs:

| index | run 1 | run 2 |
| --- | --- | --- |
| 0 | 0.5685539934051271 | 0.5660502563047922 |
| 1 | 0.5795399989045174 | 0.5686312446217308 |
| 2 | 0.5719522204521466 | 0.5693112326199914 |
| 3 | 0.5732905905982917 | 0.5841782080462852 |
| 4 | 0.6222582829075554 | 0.634954478819125 |

In each run index 4 stands clear of the rest of the field. Excluding index 4,
the run-1 values span 0.010986 and the run-2 values span 0.018128; index 4 sits
0.042718 above the next highest in run 1 and 0.050776 above it in run 2. Both
figures are computed from the vectors above. The position does not move between
runs.

This echoes the position-locked asymmetry described in
`docs/findings/2026-07-05-t9-adaptation-fairness.md`, under the heading
"## Interpretation (provisional)" in the paragraph containing "not a
coordination failure that self-interested players", which reads the per-player
disadvantage under noise as a "structural feature of the entangler circuit"
rather than a coordination failure. That finding came from noiseless
simulation; the hardware repeats now point at the same position. Neither source
settles whether the effect is wiring or hardware, and this document does not
claim it does. Item 9's wiring-permutation controls are the registered test that
separates the two.
