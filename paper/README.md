# Paper — IEEE QCE submission draft

Target: IEEE International Conference on Quantum Computing and Engineering
(QCE). Thesis structure: the simulation noise findings are the contribution;
the hardware scaling run is the validation that the landscape is predictive.

## Build

Overleaf: upload this `paper/` folder — IEEEtran is built in.
Locally: `latexmk -pdf main.tex` (needs a TeX distribution with IEEEtran).

## Status / division of labor

- All numbers already in `main.tex` are REAL, sourced from `results/`
  artifacts (each has a `% comment` naming its run dir + job id).
- `\todo{...}` markers (red in the PDF) are unwritten prose:
  - Prithvi: intro narrative, error-budget paragraph, robustness-mechanism
    link to fairness, conclusion.
  - Aasa: payoff-tensor section, zero-noise landscape section (needs the
    advantage map regenerated at V=4, C=3 — the 2026-07-02 n-scaling run used
    V=1000/C=550), Month-4 noise-findings port from README §9.
- `references.bib` has two metadata TODOs (varsamis2025, flitney2002 year).
- Table II (scaling) gains cross-day error bars automatically as repeat runs
  accumulate (`TODOS.md` protocol); regenerate `figs/hardware_scaling.pdf`
  from `scripts/plot_hardware_scaling.py` after each run.

## Figures

- `figs/hardware_n3_validation.pdf` — from `results/hardware-n3/2026-07-16T013912Z/plots/`
- `figs/hardware_scaling.pdf` — from `results/hardware-scaling/2026-07-16T074134Z/plots/`
- Simulation figures (advantage map, noise surfaces): TODO after the V=4,C=3
  regeneration; captions to be drawn from the runs' report.md files.
