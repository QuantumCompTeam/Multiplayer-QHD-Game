# Paper — IEEE Transactions on Quantum Engineering manuscript

Target: IEEE Transactions on Quantum Engineering (TQE), Original Research.
The canonical manuscript entry point is `qhd.tex`; `main.tex` is retained only
as a deprecated compatibility wrapper.

## Build

For the September 2026 journal revision, run `python scripts/build_submission.py`
from the repository root. It creates a separate draft PDF and portable source
archive in `paper/submission/`. See `JOURNAL-REVISION-LOG.md` for updated evidence
and `submission/README.md` for the author-facing upload checklist.

Overleaf: upload `submission/qhd-latex-source.zip` and select `qhd.tex`.
The current layout follows the supplied `FQCNN_journal.pdf`: IEEEtran's
conference-style letter-paper layout, 10pt two-column text, black headings,
and centered author blocks. This is the requested visual reference; the
article's research scope and target journal remain unchanged. The previous
TQE branded shell remains in the repository as a historical asset.

Run from the `paper/` directory and build into an isolated output directory:

```bash
rm -rf .qhd-build-check
mkdir .qhd-build-check
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex
bibtex .qhd-build-check/qhd
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex
```

The review artifact is `.qhd-build-check/qhd.pdf`. Do not compile directly over
the protected local `paper/qhd.pdf`. The source archive includes IEEEtran.cls.

## Status / division of labor

- The evidence-backed prose draft and all seven figures are present, but this is
  a review draft, not a submission-ready manuscript.
- Every numerical claim remains sourced from a named `results/` artifact in an
  adjacent LaTeX comment.
- Simulation payoff gaps use a circuit-evaluated restricted `{D,H}` comparator;
  hardware analytic-baseline advantage instead subtracts the noiseless
  all-Hawk payoff `1/N`. Their zero crossings are not interchangeable.
- Equilibrium claims are restricted to unilateral deviations in the finite
  menu `{D,H,Q_N}`; full-SU(2) equilibrium is not established. The `N=4,5`
  hardware points are a fixed cooperative protocol, not equilibria.
- The review draft includes Aasa's email as recorded in the canonical manuscript.
- Aasa must review the game-theory wording and sign off on the exploratory T9
  learning rule.
- The 27-source Section III literature audit is recorded in
  `LITERATURE-AUDIT.md`; every accepted entry includes a verified DOI or
  publisher record, evidence-access classification, and claim-use boundary.
- Table I reports the registration-source hardware execution;
  `figs/hardware_scaling.pdf` is a two-execution aggregate whose result
  artifacts carry the same recorded result-write-time calibration snapshot.
  This does not prove that the provider calibration was unchanged at execution
  time.
- Figure 6 error bars are the two-point sample standard deviation across those
  executions; they exclude within-run uncertainty and are not cross-day error
  bars. Cross-day hardware repeats and the resulting uncertainty update remain
  in progress.
- See `REVIEW-NOTES.md` for the complete pre-submission checklist.

## Figures

- `figs/hardware_n3_validation.pdf` — from
  `results/hardware-n3/2026-07-16T013912Z/plots/`
- `figs/hardware_scaling.pdf` — from
  `results/hardware-scaling/2026-07-17T014458Z/plots/` (two-execution aggregate;
  refreshed 2026-07-19).
- `figs/hardware_scaling_advantage.pdf`, `hardware_scaling_zne.pdf`, and
  `hardware_scaling_population.pdf` — approved single-column replacement,
  generated with `python scripts/plot_hardware_scaling.py --split`. A/C average
  the same two chain-matched calibration epochs; B uses the registration-source
  execution. The historical combined image remains available.
- `figs/hardware_topology.pdf` — from
  `results/hardware-topology/2026-07-25T114621Z/plots/`.
- `figs/advantage_vs_N.png` and `figs/topology_heatmap.png` — from the V=4/C=3
  fixed-mode regeneration
  `results/n-scaling-advantage/2026-07-19T0901Z/`.
- `figs/advantage_vs_gamma_N4.png` — from `results/gamma-sweep/N4/`.
- `figs/per_player_advantage_star.png` — from
  `results/n-scaling-advantage/2026-07-19T0901Z/results.json`, re-rendered
  September 8 with two-decimal labels on every bar, including the numerically
  zero N=4 hub. Original run artifacts and numerical data are unchanged.
