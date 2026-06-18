"""γ (entanglement-strength) sweep — runs on every `pytest`, with insight plots.

Sweeps the EWL entanglement parameter γ at a FIXED player count across the topologies,
to surface how the quantum advantage and the (Q,...,Q) Nash property depend on
entanglement strength. Writes a persistent results folder
(results/gamma-sweep-N{N}/<UTC-ts>/) containing:
  - advantage_vs_gamma.png      (advantage vs γ; filled marker = (Q,..,Q) is Nash)
  - gamma_topology_heatmap.png  (advantage by topology × γ; '*' = Nash)
  - report.md with an "Entanglement (γ) thresholds" finding.

LINKED TO experiments/config.yaml: the sweep tracks the config so editing config.yaml
also steers this test —
  - N        = the LARGEST N in config.sweep.N (fixed across the γ sweep);
  - γ bounds = config.game.gamma is the UPPER bound; γ is swept from ~0 up to it in
               GAMMA_STEPS points (if config.gamma is a list, its min→max are the bounds);
  - V, C, strategy set, topologies = taken from config too, so the numbers match the
    main experiment.
Tune GAMMA_STEPS below for a finer/coarser γ grid.

WHAT FAILS vs WHAT IS A FINDING: a cell that raises -> STATUS_ERROR -> FAIL. A
non-positive advantage or a non-Nash (Q,...,Q) at low γ is the *discovery*, not a bug.
"""

from __future__ import annotations

import cpu_limit  # noqa: F401  (first project import: caps BLAS threads before numpy)

import math
from pathlib import Path

import pytest

import results_io
from experiment.config import Cell, ExperimentConfig, load_config
from experiment.report import write_outputs
from experiment.sweep import STATUS_ERROR, run_sweep

# --- linked to experiments/config.yaml ---------------------------------------
CONFIG_PATH = Path(__file__).resolve().parents[1] / "experiments" / "config.yaml"
_CONFIG = load_config(CONFIG_PATH)

# N: largest player count in config.sweep.N, held fixed across the γ sweep.
GAMMA_SWEEP_N = max(c.N for c in _CONFIG.cells)

# γ bounds from config.game.gamma (the upper bound). If config.gamma is a single value,
# sweep ~0 → that value; if it is a list, sweep its min → max.
_config_gammas = sorted({c.gamma for c in _CONFIG.cells})
_GAMMA_UPPER = max(_config_gammas)
_GAMMA_LOWER = min(_config_gammas) if len(_config_gammas) > 1 else 0.0
GAMMA_STEPS = 6  # number of γ points across the bounds (tunable)

# V, C, strategy set and topologies also tracked from config for consistency.
_ref = next(c for c in _CONFIG.cells if c.N == GAMMA_SWEEP_N)
_TOPOLOGIES = sorted({c.topology for c in _CONFIG.cells})

# Hang-guard: skip a cell whose profile count (strategy_names**N) exceeds this, so a
# large config N can't make the suite run for hours. 10_000 => N<=8 (3-strategy set).
PER_CELL_PROFILE_BUDGET = 10_000
# ------------------------------------------------------------------------------


def _gamma_values() -> list[float]:
    """GAMMA_STEPS γ points from the lower bound (0 when config.gamma is a single
    value) up to and including the upper bound — so the sweep starts at γ=0 (the
    no-entanglement baseline; J = identity) and the plots begin at the origin."""
    span = _GAMMA_UPPER - _GAMMA_LOWER
    return [_GAMMA_LOWER + span * k / (GAMMA_STEPS - 1) for k in range(GAMMA_STEPS)]


def _gamma_label(g: float) -> str:
    return f"{g / math.pi:.3g}π"


_CELLS = [
    Cell(
        N=GAMMA_SWEEP_N,
        topology=topo,
        strategy_names=_ref.strategy_names,
        V=_ref.V,
        C=_ref.C,
        gamma=g,
        gamma_label=_gamma_label(g),
    )
    for topo in _TOPOLOGIES
    for g in _gamma_values()
]


def _profile_count(cell) -> int:
    return len(cell.strategy_names) ** cell.N


def _cell_id(cell) -> str:
    # ASCII-safe id (gamma value, not the π label) for pytest case names + result keys.
    return f"{cell.topology}-g{cell.gamma:.4f}"


@pytest.fixture(scope="module")
def gamma_run():
    """Run the γ sweep ONCE and write a persistent results folder with the new plots."""
    feasible = [c for c in _CELLS if _profile_count(c) <= PER_CELL_PROFILE_BUDGET]
    cfg = ExperimentConfig(
        name=f"gamma-sweep-N{GAMMA_SWEEP_N}",
        description=(
            f"Quantum advantage vs entanglement γ at N={GAMMA_SWEEP_N} (largest N in "
            f"config.yaml) across {_TOPOLOGIES}; γ swept up to {_ref.gamma_label} "
            f"(config.game.gamma)"
        ),
        cells=feasible,
        formats=["md", "json", "csv", "plots"],
    )
    results = run_sweep(cfg.cells)

    ts = results_io.run_timestamp()
    run_dir = results_io.new_run_dir(cfg.name, ts)
    write_outputs(cfg, results, run_dir, ts)
    results_io.write_metadata(
        run_dir,
        cfg.name,
        params={
            "source": "pytest gamma-sweep (tests/test_gamma_sweep.py)",
            "linked_to": "experiments/config.yaml",
            "N": GAMMA_SWEEP_N,
            "gamma_bounds": [_GAMMA_LOWER, _GAMMA_UPPER],
            "gamma_values": _gamma_values(),
            "gamma_steps": GAMMA_STEPS,
            "topologies": _TOPOLOGIES,
            "V": _ref.V,
            "C": _ref.C,
            "per_cell_profile_budget": PER_CELL_PROFILE_BUDGET,
        },
    )
    print(f"\n[gamma sweep] results written to {run_dir}")
    by_id = {_cell_id(r.cell): r for r in results}
    return by_id, run_dir


@pytest.mark.parametrize("cell", _CELLS, ids=[_cell_id(c) for c in _CELLS])
def test_gamma_cell_runs(cell, gamma_run) -> None:
    """Every (topology, γ) cell runs without erroring (findings are allowed)."""
    profiles = _profile_count(cell)
    if profiles > PER_CELL_PROFILE_BUDGET:
        pytest.skip(
            f"{cell.topology} N={cell.N}: {profiles:,} profiles exceeds budget "
            f"{PER_CELL_PROFILE_BUDGET:,}; lower GAMMA_SWEEP_N to run this cell."
        )
    results_by_id, _ = gamma_run
    res = results_by_id[_cell_id(cell)]
    assert res.status != STATUS_ERROR, (
        f"{cell.topology} γ={cell.gamma_label} errored: {res.message}"
    )


def test_gamma_plots_and_findings_written(gamma_run) -> None:
    """The γ sweep produces both insight plots and the entanglement-threshold finding."""
    _, run_dir = gamma_run
    plots = run_dir / "plots"
    assert (plots / "advantage_vs_gamma.png").stat().st_size > 0
    # Single N => the topology × γ heatmap is unambiguous and should be written.
    assert (plots / "gamma_topology_heatmap.png").stat().st_size > 0
    report = (run_dir / "report.md").read_text()
    assert "Entanglement (γ) thresholds" in report
