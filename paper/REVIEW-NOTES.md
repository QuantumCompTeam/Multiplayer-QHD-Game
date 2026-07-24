# IEEE Review Draft Notes

The compiled `main.pdf` is an evidence-preserving review draft, not a submission-ready manuscript. No numerical result was added or recomputed during the formatting pass.

## Author input

- Add Aasa Singh Bhui's preferred publication email to the IEEE author block.
- Obtain Aasa's game-theory sign-off on the exploratory T9 independent round-robin best-response rule and its interpretation.
- Complete final author review of all sections drafted from repository artifacts.

## Bibliography verification

- All eight cited publications were checked against authoritative publisher/DOI records.
- Every bibliography entry now includes a verified DOI, and no unverified citation remains.

## Scope and metric checks

- Full-SU(2) equilibrium is not established; current claims are restricted to
  unilateral deviations in the finite menu `{D,H,Q_N}`. The `N=4,5` hardware
  points are a fixed cooperative protocol, not equilibria.
- Simulation payoff gaps use a circuit-evaluated restricted `{D,H}` comparator,
  while hardware uses analytic `1/N`; these are distinct metrics.
- The two scaling executions provide same-recorded-calibration repeatability
  only; their result artifacts carry the same result-write-time snapshot, which
  does not prove an unchanged provider calibration. Cross-day runs remain
  pending.
- Existing Figure 6 error bars are the two-point sample SD and do not include
  within-run uncertainty; a future cross-day figure should separate within-run
  and between-day uncertainty.

## Hardware evidence still in progress

- Complete the registered target of 3--5 distinct calibration-day executions;
  the current executions share one recorded result-write-time calibration
  snapshot only.
- Validate environment provenance and `calibration_at_submit.json` on the next hardware execution.
- Make the repeat judge consume the submission-time calibration snapshot or document a manual verification step.
- Run the W-topology/wiring-permutation hardware control, or explicitly defer it and narrow the player-position claim.
- Regenerate the scaling figure and any cross-day uncertainty summary only after new repository artifacts exist.

## Submission checks

- Confirm the exact IEEE QCE submission category, current author instructions, and page limit.
- Rebuild after adding verified author metadata or making any future bibliography changes.
- Run a final citation, figure, accessibility, and PDF-conformance review.
- Prepare the final submission package only after the remaining author and hardware decisions are resolved.
