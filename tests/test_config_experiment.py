"""Run the configured experiment (experiments/config.yaml) as part of `pytest`.

A single `pytest` exercises the unit-test modules AND the sweep defined by
experiments/config.yaml, and leaves a persistent, readable results folder:
results/<config-name>/<UTC-timestamp>/ with report.md + results.json/csv + plots/
(exactly like scripts/run_experiment.py). Edit config.yaml, run pytest, open the report.

The configured sweep runs ONCE (module-scoped `configured_run` fixture); the per-cell
tests assert against those shared results, so no cell is computed twice.

WHAT FAILS vs WHAT IS A FINDING:
  - A cell that raises (unknown topology, simulation error) -> STATUS_ERROR -> FAIL.
  - A non-positive advantage or a non-Nash (Q,...,Q) is a research FINDING, not a bug
    (see game/nash.py and scripts/n3_advantage.py). These do NOT fail the test.

FEASIBILITY (hang-guard, NOT a silent cap):
  The experiment enumerates len(strategy_names)**N profiles per cell, each a 2^N-dim
  statevector simulation. Large N (e.g. config.yaml's N up to 15) is millions of
  profiles and would hang the suite for hours / OOM. Any cell whose profile count
  exceeds PER_CELL_PROFILE_BUDGET is SKIPPED (with a message), not failed. Raise the
  budget below, or lower N in config.yaml, to run those cells.
"""

from __future__ import annotations

import cpu_limit  # noqa: F401  (first project import: caps BLAS threads before numpy)

from pathlib import Path

import pytest

import results_io
from experiment.config import ExperimentConfig, load_config
from experiment.report import write_outputs
from experiment.sweep import STATUS_ERROR, run_sweep

# Real shipped config, resolved independently of pytest's working directory.
CONFIG_PATH = Path(__file__).resolve().parents[1] / "experiments" / "config.yaml"
_CONFIG = load_config(CONFIG_PATH)

# Max profiles (strategy_names**N) a single cell may have to run inside the test.
# 10_000 runs a 3-strategy set through N=8 (3**8 = 6561); 3**9 = 19_683 skips.
# Bump this to include larger N at the cost of (rapidly growing) runtime.
PER_CELL_PROFILE_BUDGET = 10_000


def _profile_count(cell) -> int:
    return len(cell.strategy_names) ** cell.N


def _cell_id(cell) -> str:
    return f"{cell.topology}-N{cell.N}-g{cell.gamma_label}-V{cell.V:g}-C{cell.C:g}"


def _slug(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in name)


@pytest.fixture(scope="module")
def configured_run():
    """Run the feasible config.yaml cells ONCE and write a persistent results folder.

    Returns (results_by_cell_id, run_dir). Shared across the per-cell tests so each
    cell is computed only once. Writes results/<name>/<UTC-ts>/ exactly like
    scripts/run_experiment.py (report.md + data + plots + metadata), so the outputs
    are there to open after `pytest`.
    """
    feasible = [c for c in _CONFIG.cells if _profile_count(c) <= PER_CELL_PROFILE_BUDGET]
    cfg = ExperimentConfig(
        name=_CONFIG.name,
        description=_CONFIG.description,
        cells=feasible,
        formats=_CONFIG.formats,
    )
    results = run_sweep(cfg.cells)

    ts = results_io.run_timestamp()
    run_dir = results_io.new_run_dir(_slug(cfg.name), ts)
    write_outputs(cfg, results, run_dir, ts)
    results_io.write_metadata(
        run_dir,
        cfg.name,
        params={
            "source": "pytest (tests/test_config_experiment.py)",
            "description": cfg.description,
            "n_cells": len(cfg.cells),
            "topologies": sorted({c.topology for c in cfg.cells}),
            "N_values": sorted({c.N for c in cfg.cells}),
            "per_cell_profile_budget": PER_CELL_PROFILE_BUDGET,
            "formats": cfg.formats,
        },
    )
    print(f"\n[config experiment] results written to {run_dir}")
    by_id = {_cell_id(r.cell): r for r in results}
    return by_id, run_dir


@pytest.mark.parametrize("cell", _CONFIG.cells, ids=[_cell_id(c) for c in _CONFIG.cells])
def test_config_cell_runs(cell, configured_run) -> None:
    """Every feasible config.yaml cell ran without erroring (findings are allowed)."""
    profiles = _profile_count(cell)
    if profiles > PER_CELL_PROFILE_BUDGET:
        pytest.skip(
            f"{cell.topology} N={cell.N}: {profiles:,} profiles exceeds budget "
            f"{PER_CELL_PROFILE_BUDGET:,}; lower N in config.yaml (or raise the "
            f"budget) to run this cell."
        )
    results_by_id, _ = configured_run
    res = results_by_id[_cell_id(cell)]
    assert res.status != STATUS_ERROR, (
        f"{cell.topology} N={cell.N} errored: {res.message}"
    )


def test_config_experiment_report_written(configured_run) -> None:
    """pytest leaves a persistent, readable results folder for the configured run."""
    _, run_dir = configured_run
    if "md" in _CONFIG.formats:
        assert (run_dir / "report.md").stat().st_size > 0
    if "json" in _CONFIG.formats:
        assert (run_dir / "results.json").stat().st_size > 0
    if "csv" in _CONFIG.formats:
        assert (run_dir / "results.csv").stat().st_size > 0
