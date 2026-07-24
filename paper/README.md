# Paper — IEEE QCE review draft

Target: IEEE International Conference on Quantum Computing and Engineering
(QCE). Thesis structure: the simulation noise findings are the contribution;
the hardware scaling runs test registered predictions. The CZ-exponential
baseline is the lowest-scoring registered candidate in both recorded
executions, but this ranking is not yet a physical scaling law.

## Build

Overleaf: upload this complete `paper/` folder; IEEEtran is built in.

Windows local build:

```powershell
winget install --id MiKTeX.MiKTeX --exact --accept-package-agreements --accept-source-agreements
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error main.tex
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error main.tex
```

Run the commands from the `paper/` directory. The expected review artifact is
`main.pdf`. MiKTeX also supplies `latexmk`, but that convenience wrapper
requires a separate Perl installation; the explicit sequence above produces
the same bibliography and cross-reference passes without Perl.

## Status / division of labor

- The evidence-backed prose draft and all six figures are present, but this is
  a review draft, not a submission-ready manuscript.
- Every numerical claim remains sourced from a named `results/` artifact in an
  adjacent LaTeX comment.
- Simulation payoff gaps use a circuit-evaluated restricted `{D,H}` comparator;
  hardware analytic-baseline advantage instead subtracts the noiseless
  all-Hawk payoff `1/N`. Their zero crossings are not interchangeable.
- Equilibrium claims are restricted to unilateral deviations in the finite
  menu `{D,H,Q_N}`; full-SU(2) equilibrium is not established. The `N=4,5`
  hardware points are a fixed cooperative protocol, not equilibria.
- The review draft omits Aasa's unknown email rather than inventing it.
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
- `figs/advantage_vs_N.png` and `figs/topology_heatmap.png` — from the V=4/C=3
  fixed-mode regeneration
  `results/n-scaling-advantage/2026-07-19T0901Z/`.
- `figs/advantage_vs_gamma_N4.png` — from `results/gamma-sweep/N4/`.
- `figs/per_player_advantage_star.png` — from
  `results/n-scaling-advantage/2026-07-19T0901Z/`.
