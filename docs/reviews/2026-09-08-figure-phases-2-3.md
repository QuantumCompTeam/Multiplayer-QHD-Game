# Phase 2 result and Phase 3 proposal

The user approved the split, captions, commits and PR update after reviewing
this proposal. Phase 2's corrected marker figure and Phase 3's three separate
PDFs are now generated. The proposal below preserves the reviewed source
anchors at the time of approval; manuscript line numbers move after insertion.
Current figure labels are `fig:scaling`, `fig:scaling-zne` and
`fig:scaling-population`. The approved supporting details are in the scaling
body under "Calibration grouping and inclusion" and "Models and uncertainty".

## Phase 2: ring recomputation

Full unrounded return values, including vectors, equilibria and every deviation:
`docs/reviews/2026-09-08-ring-phase2.json:1` (`{`).
Interpreter and versions are recorded at that file's line 2 (`"interpreter"`).
The reproducible entry point is `scripts/verify_ring_phase2.py:24` (`def main():`).

| N | Fixed-profile mean | Best restricted classical-NE mean | Advantage | Restricted Q Nash? |
|---|---|---|---|---|
| 2 | 2.0 | 0.5 | 1.5 | true |
| 3 | 1.333333333333334 | 0.3333333333333333 | 1.0000000000000007 | true |
| 4 | 0.25 | 0.25 | 0.0 | false |
| 5 | 0.8000000000000009 | 0.2 | 0.600000000000001 | false |
| 6 | 0.6666666666666674 | 0.16666666666666666 | 0.5000000000000008 | false |

Row evidence: `docs/reviews/2026-09-08-ring-phase2.json:17`, `:75`, `:148`,
`:260`, `:363` (each anchored by `"q_payoff_per_player"`). All five differences
from the stored figure-source advantages are exactly 0.0 (anchors
`"advantage_difference": 0.0` at lines 70, 143, 255, 358, 476).

At N=4 the baseline remains 0.25 and the fixed profile pays only 0.25, so the
zero comes from the fixed profile losing the cooperative payoff, not a raised
baseline. Every player can improve by switching to Dove: player zero's payoff
becomes 1.1250000000000007 rather than 0.25. Evidence: the same JSON at line 155
(`"classical_ne_payoff": 0.25`) and line 213
(`"deviation_payoff": 1.1250000000000007`).

Verdict: the zero is real for the fixed Q_N strategy at N=4, gamma=pi/2, V=4,
C=3; it is not a general even-N effect because N=2 and N=6 have positive gaps.
Only N=4 is zero in the tested N=2..6 grid; this grid cannot establish uniqueness
over all larger N or arbitrary strategies and entanglement strengths.

Provenance passes: `src/config.py:35` (`V: float = 4.0`) and line 36
(`C: float = 3.0`) match the source run's
`results/n-scaling-advantage/2026-07-19T0901Z/config.snapshot.yaml:150`
(`V: 4.0`) and line 151 (`C: 3.0`) for ring N=4. The script verifies both
parameters in every ring JSON cell. Figure provenance is cited at
`paper/qhd.tex:894` (`% source:`) and line 906 (`% source:`).

### Marker defect and prepared local correction

`paper/qhd.tex:891` (`Filled markers indicate`) claims a Nash encoding.
However, `src/experiment/plots.py:94` (`series.setdefault`) retains only N and
advantage, and line 106 (`ax.plot(xs, ys`) plots all markers with their default
fill. The function never consults `q_is_nash`. Ring N=4 should be open under
the caption's convention. The gamma plot does implement this encoding at
`src/experiment/plots.py:194` (`markerfacecolor=color if is_nash else "white"`).

Prepared correction: carry each cell's Nash flag through the N-series and draw
each marker filled or open accordingly; preserve numerical values and connect
the same sampled points. The paper's N-scaling image was regenerated from the
saved JSON, preserving historical run artifacts. The cited plotting lines above
describe the pre-fix defect; the new flag is stored on line 94 and marker fill
is applied on line 109 (`markerfacecolor=line.get_color() if is_nash else "white"`).

## Phase 3: approved split proposal

Use three independent single-column vector-PDF figures, each placed at
`width=\linewidth`, with fonts and legends inspected at final paper size.
Retain `fig:scaling` for A to preserve existing cross-references; assign
`fig:scaling-zne` and `fig:scaling-population` to B and C. These are proposed
labels, not existing references.

B and C should be separate: B explains mitigation in the registration-source
execution, whereas C aggregates populations across calibration epochs. B uses
`scripts/plot_hardware_scaling.py:255` (`s = first["analysis"]["series"][str(N)]`);
C uses line 197 (`pg_meas[N], pg_err[N] = agg`). Their uncertainty bars therefore
have different meanings. Do not call all three panels cross-epoch aggregates.

### Caption A (three sentences)

Cooperative-profile payoff advantage on ibm_fez at N=3,4,5, relative to the
analytic noiseless classical-Nash baseline, comparing raw and mitigated-plus-ZNE
measurements with ideal and noise-model curves. Error bars show the sample
standard deviation across two calibration epochs and are a lower bound on total
uncertainty; depolarizing values at N=4,5 are predictions from the N=3 fit.
The fixed profile passes the restricted pure-Nash check only at N=3; N=4,5
measure a cooperative protocol, not an equilibrium.

### Caption B (three sentences)

Zero-noise extrapolation of the readout-mitigated mean payoff in the
registration-source execution at N=3,4,5. Points at CZ fold factors 1,3,5 carry
within-run payoff standard errors; weighted linear fits extrapolate to zero
fold factor (stars). The N=4,5 profiles are cooperative protocols, not
restricted pure-Nash equilibria.

### Caption C (three sentences)

All-zero output probability on ibm_fez at N=3,4,5, compared with the device
noise-model prediction and ideal target. Measured points average calibration
epochs; error bars are the cross-epoch sample standard deviation and a lower
bound on total uncertainty. These are fixed-profile measurements, with the
restricted pure-Nash property holding only at N=3.

Caption evidence: `paper/qhd.tex:1142` (`Measured cooperative-profile advantage`),
`:1147` (`predictions, not fits`), `:1149` (`Error bars are the sample standard`),
`:1151` (`lower bound on total uncertainty`), and `:1158`
(`restricted-menu pure-Nash check only`). B's within-run bars are explicitly
`scripts/plot_hardware_scaling.py:258` (`sigs =`) and `:260` (`axB.errorbar`).
The saved honesty flags remain visible in
`results/hardware-scaling/2026-07-26T090122Z/result.json:168` and `:322`
(`"q_is_nash_noiseless": false`).

### Where displaced facts will land

Insert two named paragraphs immediately after `paper/qhd.tex:1108`
(`readout-mitigated payoff linearly to`) and before the existing scaling table:

1. **Calibration grouping and inclusion.** Keep chain [59,75,74,73,79], 4096
   shots per execution, three executions, the two stamps 2026-07-16 08:30:13
   +05:30 (two executions) and 2026-07-26 13:29:01 +05:30 (one), averaging within
   each stamp before taking the spread so one calibration is not counted twice.
   State that the fourth execution on [20,21,22,23,24] is excluded to avoid
   mixing qubit-allocation changes with calibration drift. State that the
   existing table and new B show the registration-source execution alone.
   Sources: `paper/qhd.tex:1134` (`[59,75,74,73,79]`), `:1137`
   (`2026-07-16 08:30:13`), `:1138` (`A fourth execution exists`), `:1140`
   (`Table~\ref{tab:scaling} reports`), and the timestamp offsets in
   `results/hardware-scaling/2026-07-26T090122Z/plots/caption.md:1`
   (`2026-07-16 08:30:13+05:30`).
2. **Models and uncertainty.** Retain p_eff=0.0018 fitted only at N=3; predictions
   at N=4,5; ideal/device/depolarizing curves from the registration anchor;
   cross-epoch sample standard deviation for A/C excluding within-run
   multinomial and weighted-fit errors; and B's separate within-run payoff
   standard errors. Preserve the lower-bound caveat in the body and A/C
   captions. Sources: `paper/qhd.tex:1146` (`0.0018`), `:1148`
   (`registration anchor's rather than run averages`), `:1150`
   (`within-run multinomial and weighted-fit standard errors`), and
   `scripts/plot_hardware_scaling.py:161` (`np.std(per_epoch, ddof=1)`).

Keep CZ-fold construction and the weighted extrapolation explanation in the
existing methods paragraph at `paper/qhd.tex:1106` (`extrapolation folds each cz
locally`); add that B illustrates the registration-source fit. Move the
single-bit-flip explanation beside C in the scaling body, retaining its link to
the observable discussion; source `paper/qhd.tex:1156` (`first-order insensitive`).
Keep the N=4,5 non-equilibrium caveat in the body and all three short captions;
source `paper/qhd.tex:1159` (`at $N{=}4,5$ the profile is the cooperative quantum`).

## PR status

PR #22 was created, but its first GitHub CI run failed three raw-result replay
tests; the other 895 tests passed and three were skipped. The replay test
previously demanded exact equality of nested floating-point results at
`tests/test_registered_phase_results.py:27` (`assert replay == result['judgment']`).
The CI diff shows last-digit differences in floating covariance/error statistics
between the Linux runner and the original Windows calculations. The prepared
local fix uses relative tolerance 1e-12 and absolute tolerance 1e-14 only for
floating statistics while retaining exact structure, hashes, shot counts, labels,
and all pass/fail booleans. A focused check proves that flipped decisions and
meaningful numerical changes still fail. The replay and experiment checks pass:
12 passed in the required conda environment. After manuscript integration,
the combined replay/experiment/manuscript/anchor checks passed: 384 passed,
3 skipped. The updated PR's GitHub checks are authoritative for Linux CI.
