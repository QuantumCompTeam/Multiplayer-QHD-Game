# Paper — IEEE Transactions on Quantum Engineering manuscript

Target: IEEE Transactions on Quantum Engineering (TQE), Original Research.
The canonical manuscript entry point is `qhd.tex`; `main.tex` is retained only
as a deprecated compatibility wrapper.

## Build

Overleaf: upload this complete `paper/` folder, including `ieeeaccess.cls` and
the TQE shell image assets, then set `qhd.tex` as the main document.

Run from the `paper/` directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error qhd.tex
bibtex qhd
pdflatex -interaction=nonstopmode -halt-on-error qhd.tex
pdflatex -interaction=nonstopmode -halt-on-error qhd.tex
```

The expected manuscript artifact is `qhd.pdf`. These commands use the official
TQE LaTeX shell distributed by the IEEE Template Selector in
`TQE_Template.zip`.

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
- All eight cited publications were checked against authoritative publisher/DOI
  records; every entry includes a verified DOI, and no unverified citation remains.
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
- `figs/hardware_topology.pdf` — from
  `results/hardware-topology/2026-07-25T114621Z/plots/`.
- `figs/advantage_vs_N.png` and `figs/topology_heatmap.png` — from the V=4/C=3
  fixed-mode regeneration
  `results/n-scaling-advantage/2026-07-19T0901Z/`.
- `figs/advantage_vs_gamma_N4.png` — from `results/gamma-sweep/N4/`.
- `figs/per_player_advantage_star.png` — from
  `results/n-scaling-advantage/2026-07-19T0901Z/`.
