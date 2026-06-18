"""Run the configured experiment (experiments/config.yaml) as part of `pytest`.

This links the experiment harness into the normal test run: a single `pytest`
exercises the 8 unit-test modules AND the sweep defined by experiments/config.yaml.
Edit config.yaml, run pytest, and the parametrized case list below changes to match
the new config — no separate `scripts/run_experiment.py` call needed.

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

from pathlib import Path

import pytest

from experiment.config import ExperimentConfig, load_config
from experiment.report import write_outputs
from experiment.sweep import STATUS_ERROR, run_cell, run_sweep

# Real shipped config, resolved independently of pytest's working directory.
CONFIG_PATH = Path(__file__).resolve().parents[1] / "experiments" / "config.yaml"
_CONFIG = load_config(CONFIG_PATH)

# Max profiles (strategy_names**N) a single cell may have to run inside the test.
# 10_000 runs a 3-strategy set through N=8 (3**8 = 6561); 3**9 = 19_683 skips.
# Bump this to include larger N at the cost of (rapidly growing) runtime.
PER_CELL_PROFILE_BUDGET = 10_000

# The end-to-end test only needs to prove the report/plots PIPELINE runs from
# config.yaml — the per-cell tests above already cover every feasible cell for
# correctness. So it uses a tighter budget to avoid re-running the expensive
# high-N tail (and rendering its plots) a second time. 1_000 => N<=6 for a
# 3-strategy set (3**6 = 729).
E2E_PROFILE_BUDGET = 1_000


def _profile_count(cell) -> int:
    return len(cell.strategy_names) ** cell.N


def _cell_id(cell) -> str:
    return f"{cell.topology}-N{cell.N}-g{cell.gamma_label}-V{cell.V:g}-C{cell.C:g}"


@pytest.mark.parametrize("cell", _CONFIG.cells, ids=[_cell_id(c) for c in _CONFIG.cells])
def test_config_cell_runs(cell) -> None:
    """Every config.yaml cell runs without erroring (findings are allowed)."""
    profiles = _profile_count(cell)
    if profiles > PER_CELL_PROFILE_BUDGET:
        pytest.skip(
            f"{cell.topology} N={cell.N}: {profiles:,} profiles exceeds budget "
            f"{PER_CELL_PROFILE_BUDGET:,}; lower N in config.yaml (or raise the "
            f"budget) to run this cell."
        )
    res = run_cell(cell)
    assert res.status != STATUS_ERROR, (
        f"{cell.topology} N={cell.N} errored: {res.message}"
    )


def test_config_experiment_end_to_end(tmp_path) -> None:
    """The full config.yaml pipeline (sweep -> report/plots) runs end to end.

    Restricted to cells within the feasibility budget and written to a temp dir
    (never to results/). Honors config.formats, so 'plots' also exercises the
    topology/circuit rendering path.
    """
    feasible = [c for c in _CONFIG.cells if _profile_count(c) <= E2E_PROFILE_BUDGET]
    if not feasible:
        pytest.skip(
            "no config.yaml cells within the end-to-end budget; lower N in "
            "config.yaml to run the experiment end-to-end test."
        )

    cfg = ExperimentConfig(
        name=_CONFIG.name,
        description=_CONFIG.description,
        cells=feasible,
        formats=_CONFIG.formats,
    )
    results = run_sweep(cfg.cells)
    run_dir = write_outputs(cfg, results, tmp_path / "run", "test")

    errored = [r for r in results if r.status == STATUS_ERROR]
    assert not errored, "errored cells: " + ", ".join(
        f"{r.cell.topology} N={r.cell.N} ({r.message})" for r in errored
    )
    if "md" in cfg.formats:
        assert (run_dir / "report.md").stat().st_size > 0
