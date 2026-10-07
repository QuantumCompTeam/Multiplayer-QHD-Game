# Incentive Compatibility and Payoff Robustness in Multiplayer Quantum Games

Code, data and manuscript for the paper
**"Incentive Compatibility and Payoff Robustness in Multiplayer Quantum Games:
Theory and Hardware Evidence"** by Prithvi Raghu, Aasa Singh Bhui,
J Vijayashree and J Jayashree (Vellore Institute of Technology).

The paper is in [`paper/qhd.pdf`](paper/qhd.pdf), built from
[`paper/qhd.tex`](paper/qhd.tex).

## Summary

We study an N-player Eisert–Wilkens–Lewenstein (EWL) allocation game, a
Hawk–Dove game with V=4 and C=3, under five entangler families (GHZ, W, ring,
star, fully connected), using exact simulation and IBM Heron r2 hardware
(ibm_fez) with up to seven players.

- **Incentive boundary.** For the GHZ entangler, the original cooperative phase
  Q_N (phase π/N) is a restricted {D,H,Q_N} equilibrium only for N=2,3. An
  alternative branch Q*_N is a strict restricted-menu equilibrium for every
  N≥2 at maximal entanglement. Both branches admit a profitable unrestricted
  SU(2) deviation.
- **Compact evaluation.** The ideal GHZ output is a sum of at most four product
  states, which gives exact payoff evaluation through N=128 without dense
  state vectors.
- **Landscape and noise.** Topology changes both the payoff gap and the
  equilibrium status. Under gate-level depolarizing noise, the GHZ, ring, star
  and fully connected families decay at similar rates per two-qubit gate, while
  W is the outlier.
- **Hardware.** The GHZ protocol retains 98–99% of its ideal advantage at
  N=3–5 after mitigation. Retention at N=6,7 falls below what uniformly random
  outcomes would give. Preregistered one-parameter noise models fail out of
  sample. All-player tests of Q*_N pass the preregistered incentive criterion
  at N=4,6 in both batches but fail the overall five-size test.

## Repository layout

```
paper/        manuscript: qhd.tex (+ \input files), references.bib, figs/, qhd.pdf
src/          circuits (EWL operator, entangler families, noise), game theory
              (payoffs, equilibria, phase branches, compact GHZ evaluation),
              experiment harness, hardware helpers
experiments/  sweep configs and the IBM hardware pipelines
scripts/      analysis, preregistration, judging and figure scripts
results/      every simulation and hardware result used in the paper
docs/         per-experiment findings notes and formula derivations
tests/        test suite, including checks of the paper's equations and claims
```

## Setup

Python 3.10. The simulation and analysis stack is pinned in `pyproject.toml`:

```bash
conda create -n entangled-equilibria python=3.10
conda activate entangled-equilibria
pip install -e ".[dev]"
pytest
```

Hardware submission additionally needs `qiskit-ibm-runtime` and a saved IBM
Quantum account. The original-phase runs used qiskit 1.3.2,
qiskit-ibm-runtime 0.36.1 and qiskit-aer 0.14.2; the alternative-phase runs
used qiskit 2.5.2, qiskit-ibm-runtime 0.49.0 and qiskit-aer 0.17.2. Recorded
hardware counts are in `results/`, so no IBM account is needed to reproduce the
analysis.

## Building the paper

```bash
cd paper
latexmk -pdf qhd.tex
```

## Reproducing the results

All commands run from the repository root. Sweeps write a new timestamped
folder under `results/`; the folder the paper uses is given in brackets.

| Paper item | Command |
|---|---|
| Figs. 1, 2, 4 (zero-noise landscape) | `python scripts/run_experiment.py --config experiments/n-scaling.yaml` [`results/n-scaling-advantage/2026-07-19T0901Z`] |
| Fig. 3 (γ sweep, N=4) | `python scripts/run_experiment.py --config experiments/gamma-sweep-N4.yaml` [`results/gamma-sweep/N4`] |
| Redraw Figs. 1–4 | `python scripts/plot_paper_simulation.py` |
| Noise robustness | `python scripts/run_experiment.py --config experiments/noise-sweep.yaml` [`results/noise-robustness/2026-07-03T0213Z`] |
| Table III (per-gate decay controls) | `python scripts/topology_noise_controls.py` [`results/topology-controls/2026-07-16T172737Z`] |
| Fig. 5 (phase branches, sensitivity, compact evaluation) | `python scripts/journal_analysis.py`, then `python scripts/plot_phase_sensitivity.py` [`results/journal-strengthening/2026-09-07-offline`] |
| Fig. 6 (N=3 hardware) | `python scripts/plot_hardware_result.py results/hardware-n3/2026-07-16T013912Z/result.json` |
| Table IV, Figs. 7–9 (N=3–5 scaling) | `python scripts/plot_hardware_scaling.py --split` |
| Scaling-model tests and repeats | `python scripts/judge_repeat_run.py`, `python scripts/judge_n67_run.py` |
| Table V, Fig. 10 (topology batch) | `python scripts/judge_topology_run.py`, then `python scripts/plot_hardware_topology.py results/hardware-topology/2026-07-25T114621Z` |
| Table VI (alternative-phase tests) | `python scripts/summarize_phase_hardware.py <run>/result.json` for each `results/phase-validation/2026-09-07-hardware-*` run; `python scripts/audit_phase_evidence.py` re-derives the verdicts from raw counts |
| Adaptation pilot | `python scripts/t9_precise_rerun.py` with `--rule round-robin\|simultaneous` and `--rounds` as needed [`results/t9-pilot/precise-*`] |

The judging scripts apply the predictions committed before each hardware
submission (`results/hardware-scaling/preregistration*.json`,
`results/hardware-topology/preregistration.json`). The hardware pipelines in
`experiments/hardware_*.py` and `scripts/run_phase_hardware.py` run their
offline checks by default and only submit to IBM with an explicit flag.

## Citation

```bibtex
@misc{raghu2026incentive,
  title  = {Incentive Compatibility and Payoff Robustness in Multiplayer
            Quantum Games: Theory and Hardware Evidence},
  author = {Raghu, Prithvi and Bhui, Aasa Singh and Vijayashree, J and
            Jayashree, J},
  year   = {2026},
  note   = {Code and data: https://github.com/QuantumCompTeam/Multiplayer-QHD-Game}
}
```
