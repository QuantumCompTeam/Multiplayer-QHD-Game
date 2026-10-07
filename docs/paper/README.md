# Paper — IEEE Transactions on Quantum Engineering manuscript

Target: IEEE Transactions on Quantum Engineering (TQE), Original Research.
The manuscript lives in `paper/`: `qhd.tex` (entry point), its `\input` files,
`references.bib`, `figs/`, and the final built `qhd.pdf`. Process notes and
submission artifacts live here in `docs/paper/`.

## Build

For the September 2026 journal revision, run `python scripts/build_submission.py`
from the repository root. It creates a separate draft PDF and portable source
archive in `docs/paper/submission/`, and copies the final PDF to `paper/qhd.pdf`.
See `JOURNAL-REVISION-LOG.md` for updated evidence
and `submission/README.md` for the author-facing upload checklist.

Overleaf: upload `submission/qhd-latex-source.zip` and select `qhd.tex`.
The current layout follows the supplied `FQCNN_journal.pdf`: IEEEtran's
conference-style letter-paper layout, 10pt two-column text, black headings,
and centered author blocks. This is the requested visual reference; the
article's research scope and target journal remain unchanged. The previous
TQE branded shell (`ieeeaccess.cls` and logos) was removed; it is in git history.

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
`paper/qhd.pdf`; `build_submission.py` refreshes it. The source archive includes IEEEtran.cls.

## Status / division of labor

- The evidence-backed prose draft and its figures are present, but this is
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
- The hardware scaling figures are split into advantage, zero-noise
  extrapolation, and ground-state population. Advantage and population average
  runs within each calibration stamp before computing the cross-epoch sample
  standard deviation. These error bars are a coarse two-epoch spread and exclude
  within-run errors;
  the other-chain execution is excluded. The extrapolation panel uses the
  registration-source execution. See the Hardware Validation body text for
  the complete sample definition and the N=4,5 non-equilibrium caveat.
- Q1 eligibility, Google Scholar presence, and current retraction status remain
  under review; see `Q1-REFERENCE-AUDIT.md`. The existing bibliography is not
  certified against that new policy.
- See `REVIEW-NOTES.md` for the complete pre-submission checklist.

## Figures

- `figs/hardware_n3_validation.pdf` — from
  `results/hardware-n3/2026-07-16T013912Z/plots/`
- `figs/hardware_scaling_advantage.pdf`, `hardware_scaling_zne.pdf`, and
  `hardware_scaling_population.pdf` — approved single-column replacement,
  generated with `python scripts/plot_hardware_scaling.py --split`. A/C average
  the same two chain-matched calibration epochs; B uses the registration-source
  execution. The historical combined image remains in
  `results/hardware-scaling/2026-07-26T090122Z/plots/hardware_scaling.pdf`.
- `figs/hardware_topology.pdf` — `python scripts/plot_hardware_topology.py
  results/hardware-topology/2026-07-25T114621Z` (also writes the run's `plots/`).
- `figs/advantage_vs_N.pdf`, `figs/topology_heatmap.pdf`,
  `figs/advantage_vs_gamma_N4.pdf`, `figs/per_player_advantage_star.pdf` —
  `python scripts/plot_paper_simulation.py`, reading
  `results/n-scaling-advantage/2026-07-19T0901Z/results.csv` and
  `results/gamma-sweep/N4/results.csv`.
- `figs/journal_extensions.pdf` — `python scripts/plot_phase_sensitivity.py`,
  reading `results/journal-strengthening/2026-09-07-offline/results.json`
  (plot only; `scripts/journal_analysis.py` recomputes that analysis).
