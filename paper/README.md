# Paper — IEEE QCE submission draft

Target: IEEE International Conference on Quantum Computing and Engineering
(QCE). Thesis structure: the simulation noise findings are the contribution;
the hardware scaling runs test the registered predictions (the registered
model comparison favors per-gate decay, with the depolarizing fit as its
physical interpretation).

## Build

Overleaf: upload this `paper/` folder — IEEEtran is built in.
Locally: `latexmk -pdf main.tex` (needs a TeX distribution with IEEEtran).

## Status / division of labor

- All numbers already in `main.tex` are REAL, sourced from `results/`
  artifacts (each has a `% comment` naming its run dir + job id).
- `\todo{...}` markers (red in the PDF) are unwritten prose:
  - Prithvi: intro narrative, error-budget paragraph, robustness-mechanism
    link to fairness, conclusion.
  - Aasa: payoff-tensor section, zero-noise landscape section (advantage map
    regenerated at V=4/C=3 fixed-mode under item 13 on 2026-07-19 — see Figures
    below; gamma-sweep N2–N6 also current-convention), Month-4 noise-findings
    port from README §9.
- `references.bib` has two metadata TODOs (varsamis2025, flitney2002 year).
- Table II (scaling) gains cross-day error bars automatically as repeat runs
  accumulate (`TODOS.md` protocol); regenerate `figs/hardware_scaling.pdf`
  from `scripts/plot_hardware_scaling.py` after each run.

## Figures

- `figs/hardware_n3_validation.pdf` — from `results/hardware-n3/2026-07-16T013912Z/plots/`
- `figs/hardware_scaling.pdf` — from `results/hardware-scaling/2026-07-17T014458Z/plots/`
  (2-run aggregate; refreshed 2026-07-19).
- Advantage map: embedded at `main.tex` (Figs. `fig:advmap` + `fig:heat`) from
  `figs/advantage_vs_N.png` + `figs/topology_heatmap.png` — the V=4/C=3 fixed-mode
  regen `results/n-scaling-advantage/2026-07-19T0901Z`; gamma-sweep N2–N6
  current-convention. Star per-player figure (`per_player_advantage_star.png`)
  and gamma-sweep prose remain Aasa `\todo`s in the same subsection.
