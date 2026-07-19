"""γ (entanglement-strength) sweep — runs on every `pytest`, with insight plots.

Sweeps the EWL entanglement parameter γ across the topologies, at every feasible N in
config.sweep.N. Each N gets its own subfolder with the actual content (no timestamp):

  results/gamma-sweep/
    N2/  report.md  results.json  results.csv  plots/  metadata.json  config.snapshot.yaml
    ...
    N8/  ...

Each N's plots/ holds advantage_vs_gamma.png (advantage vs γ; filled marker = (Q,..,Q) is
Nash) and gamma_topology_heatmap.png, and report.md carries the "Entanglement (γ) thresholds"
finding. Topology diagrams are NOT written here — they live in the shared results/topology/
folder (built by the `topology_folder` fixture).

LINKED TO experiments/config.yaml:
  - N values  = the feasible N in config.sweep.N (3-strategy: N with strat**N <= budget);
  - γ bounds  = config.game.gamma is the upper bound; γ swept from 0 up to it in GAMMA_STEPS
                points (if config.gamma is a list, its min→max are the bounds);
  - V, C, strategy set, topologies = taken from config too.

WHAT FAILS vs WHAT IS A FINDING: a cell that raises -> STATUS_ERROR -> FAIL. A
non-positive advantage or a non-Nash (Q,...,Q) at low γ is the *discovery*, not a bug.

Note: Running a full γ sweep at every feasible N (N2..N8) is slow (minutes; N=8 dominates).
Lower config.sweep.N, PER_CELL_PROFILE_BUDGET, or GAMMA_STEPS to speed it up.
"""

from __future__ import annotations

import cpu_limit  # noqa: F401  (first project import: caps BLAS threads before numpy)

import math
import shutil
from pathlib import Path

import pytest

import results_io
from experiment.config import Cell, ExperimentConfig, load_config
from experiment.report import write_outputs
from experiment.sweep import STATUS_ERROR, run_sweep

# --- linked to experiments/config.yaml ---------------------------------------
CONFIG_PATH = Path(__file__).resolve().parents[1] / "experiments" / "config.yaml"
_CONFIG = load_config(CONFIG_PATH)

# γ bounds from config.game.gamma (the upper bound). Single value -> sweep 0 → it;
# a list -> sweep its min → max.
_config_gammas = sorted({c.gamma for c in _CONFIG.cells})
_GAMMA_UPPER = max(_config_gammas)
_GAMMA_LOWER = min(_config_gammas) if len(_config_gammas) > 1 else 0.0
GAMMA_STEPS = 6  # number of γ points across the bounds (tunable)

# V, C, strategy set and topologies tracked from config for consistency.
_ref = _CONFIG.cells[0]
_TOPOLOGIES = sorted({c.topology for c in _CONFIG.cells})
_STRAT = len(_ref.strategy_names)

# Hang-guard: a cell whose profile count (strat**N) exceeds this is skipped, so a large
# config N can't make the suite run for hours. 10_000 => N<=8 for a 3-strategy set.
PER_CELL_PROFILE_BUDGET = 10_000

# Every N in config; the γ sweep runs at the feasible ones (others show as skips).
_ALL_N = sorted({c.N for c in _CONFIG.cells})
GAMMA_SWEEP_N_VALUES = [n for n in _ALL_N if _STRAT ** n <= PER_CELL_PROFILE_BUDGET]
# ------------------------------------------------------------------------------


def _gamma_values() -> list[float]:
    """GAMMA_STEPS γ points from the lower bound (0 when config.gamma is a single
    value) up to and including the upper bound — so the sweep starts at γ=0 (the
    no-entanglement baseline; J = identity) and the plots begin at the origin."""
    span = _GAMMA_UPPER - _GAMMA_LOWER
    return [_GAMMA_LOWER + span * k / (GAMMA_STEPS - 1) for k in range(GAMMA_STEPS)]


def _gamma_label(g: float) -> str:
    return f"{g / math.pi:.3g}π"


def _cells_for_n(n: int) -> list[Cell]:
    return [
        Cell(
            N=n,
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


# All (N, topology, γ) cells across every config N (parametrization domain).
_CELLS = [cell for n in _ALL_N for cell in _cells_for_n(n)]


def _profile_count(cell) -> int:
    return len(cell.strategy_names) ** cell.N


def _cell_id(cell) -> str:
    # ASCII-safe id (gamma value, not the π label) for pytest case names + result keys.
    return f"N{cell.N}-{cell.topology}-g{cell.gamma:.4f}"


@pytest.fixture(scope="module")
def gamma_run(topology_folder):
    """Run the γ sweep at each feasible N ONCE, writing results/gamma-sweep/N{n}/.

    Returns (results_by_cell_id, root_dir, {N: n_dir}). Content is written directly
    into each N subfolder (no timestamp); the subfolder is cleared first for a clean
    overwrite.
    """
    root = results_io.RESULTS_ROOT / "gamma-sweep"
    by_id: dict[str, object] = {}
    n_dirs: dict[int, Path] = {}

    for n in GAMMA_SWEEP_N_VALUES:
        cfg = ExperimentConfig(
            name=f"gamma-sweep-N{n}",
            description=(
                f"Quantum advantage vs entanglement γ at N={n} across {_TOPOLOGIES}; "
                f"γ swept {_gamma_label(_GAMMA_LOWER)}→{_gamma_label(_GAMMA_UPPER)} "
                f"(config.game.gamma)"
            ),
            cells=_cells_for_n(n),
            formats=["md", "json", "csv", "plots"],
        )
        results = run_sweep(cfg.cells)

        n_dir = root / f"N{n}"
        if n_dir.exists():
            shutil.rmtree(n_dir)  # clean overwrite of this N's content
        write_outputs(cfg, results, n_dir, results_io.run_timestamp())
        results_io.write_metadata(
            n_dir,
            cfg.name,
            params={
                "source": "pytest gamma-sweep (tests/test_gamma_sweep.py)",
                "linked_to": "experiments/config.yaml",
                "N": n,
                "gamma_bounds": [_GAMMA_LOWER, _GAMMA_UPPER],
                "gamma_values": _gamma_values(),
                "gamma_steps": GAMMA_STEPS,
                "topologies": _TOPOLOGIES,
                "V": _ref.V,
                "C": _ref.C,
            },
        )
        for r in results:
            by_id[_cell_id(r.cell)] = r
        n_dirs[n] = n_dir

    print(f"\n[gamma sweep] results under {root} (N={GAMMA_SWEEP_N_VALUES})")
    return by_id, root, n_dirs


@pytest.mark.parametrize("cell", _CELLS, ids=[_cell_id(c) for c in _CELLS])
def test_gamma_cell_runs(cell, gamma_run) -> None:
    """Every feasible (N, topology, γ) cell runs without erroring (findings allowed)."""
    profiles = _profile_count(cell)
    if profiles > PER_CELL_PROFILE_BUDGET:
        pytest.skip(
            f"{cell.topology} N={cell.N}: {profiles:,} profiles exceeds budget "
            f"{PER_CELL_PROFILE_BUDGET:,}; lower config N or raise the budget."
        )
    results_by_id, _, _ = gamma_run
    res = results_by_id[_cell_id(cell)]
    assert res.status != STATUS_ERROR, (
        f"N={cell.N} {cell.topology} γ={cell.gamma_label} errored: {res.message}"
    )


def test_gamma_subfolders_and_topology(gamma_run, topology_folder) -> None:
    """Each N subfolder has its report + γ plot; the shared topology folder is populated."""
    _, _, n_dirs = gamma_run
    assert n_dirs, "no feasible N to sweep — lower config N or raise the budget"
    for n, n_dir in n_dirs.items():
        assert (n_dir / "report.md").stat().st_size > 0, f"N{n} report missing"
        assert (n_dir / "plots" / "advantage_vs_gamma.png").stat().st_size > 0, (
            f"N{n} advantage_vs_gamma.png missing"
        )
        report = (n_dir / "report.md").read_text(encoding="utf-8")
        assert "Entanglement (γ) thresholds" in report
    # Shared topology folder has individual topology images (not in the run folders).
    assert list(topology_folder.glob("*/*.png")), "results/topology/ has no graphs"
