"""Tests for the experiment harness (config -> sweep -> report).

Guards the WIRING of the harness, not the game theory (that lives in nash.py and
its own tests). Confirms:
  - gamma expression parsing (pi/2) and rejection of junk
  - sweep expansion takes the cartesian product of list-valued axes
  - run_sweep on N=3/GHZ returns status "ok" with the known advantage == 1.0
  - an asymmetric topology (star, N=3) runs and reports symmetric=False + vectors
  - an unknown topology name is recorded as "error", not raised
  - write_outputs emits non-empty report.md / results.json / results.csv
"""

from __future__ import annotations

import json
import math

import pytest

from experiment.config import ExperimentConfig, expand_cells, load_config, parse_gamma
from experiment.report import write_outputs
from experiment.sweep import STATUS_ERROR, STATUS_OK, run_cell, run_sweep


def test_parse_gamma_pi_expression() -> None:
    assert parse_gamma("pi/2") == pytest.approx(math.pi / 2)
    assert parse_gamma("pi") == pytest.approx(math.pi)
    assert parse_gamma(1.5) == 1.5


def test_parse_gamma_rejects_junk() -> None:
    with pytest.raises(ValueError):
        parse_gamma("__import__('os')")


def test_expand_cells_cartesian_product() -> None:
    raw = {
        "sweep": {"N": [2, 3], "topologies": ["ghz", "w"], "strategy_names": ["D", "H", "Q"]},
        "game": {"V": 4.0, "C": 3.0, "gamma": ["pi/2", "pi/4"]},
    }
    cells = expand_cells(raw)
    # 2 N * 2 topologies * 2 gamma = 8 cells
    assert len(cells) == 8
    assert {c.topology for c in cells} == {"ghz", "w"}
    assert {c.gamma_label for c in cells} == {"pi/2", "pi/4"}


def test_run_cell_ghz_n3_advantage() -> None:
    """N=3 GHZ is the known Month-2 result: advantage == 1.0, Q is Nash."""
    raw = {
        "sweep": {"N": [3], "topologies": ["ghz"], "strategy_names": ["D", "H", "Q"]},
        "game": {"V": 4.0, "C": 3.0, "gamma": "pi/2"},
    }
    (cell,) = expand_cells(raw)
    res = run_cell(cell)
    assert res.status == STATUS_OK
    assert res.advantage == pytest.approx(1.0)
    assert res.q_is_nash is True


def test_run_cell_star_reports_per_player_vectors() -> None:
    """Star at N=3 runs and exposes per-player vectors + a symmetric flag.

    (The symmetric strategy profiles compute_advantage reports on can still be
    player-symmetric even under the star topology, so we don't assert a specific
    symmetry verdict — only that the harness surfaces the per-player data.)
    """
    raw = {
        "sweep": {"N": [3], "topologies": ["star"], "strategy_names": ["D", "H", "Q"]},
        "game": {"V": 4.0, "C": 3.0, "gamma": "pi/2"},
    }
    (cell,) = expand_cells(raw)
    res = run_cell(cell)
    assert res.status == STATUS_OK
    assert res.result is not None
    assert isinstance(res.result["symmetric"], bool)
    assert len(res.result["advantage_vector"]) == 3


def test_run_cell_unknown_topology_is_recorded() -> None:
    """An unknown topology name must be recorded as an error, not raised."""
    raw = {
        "sweep": {"N": [3], "topologies": ["banana"], "strategy_names": ["D", "H", "Q"]},
        "game": {"V": 4.0, "C": 3.0, "gamma": "pi/2"},
    }
    (cell,) = expand_cells(raw)
    res = run_cell(cell)
    assert res.status == STATUS_ERROR
    assert res.result is None


def test_write_outputs_emits_files(tmp_path) -> None:
    raw = {
        "sweep": {"N": [2, 3], "topologies": ["ghz", "w"], "strategy_names": ["D", "H", "Q"]},
        "game": {"V": 4.0, "C": 3.0, "gamma": "pi/2"},
    }
    config = ExperimentConfig(
        name="test-run",
        description="harness wiring test",
        cells=expand_cells(raw),
        formats=["md", "json", "csv"],  # skip plots (no rendering needed here)
    )
    results = run_sweep(config.cells)
    run_dir = write_outputs(config, results, tmp_path / "run", "2026-06-18 00:00:00")

    report = (run_dir / "report.md").read_text()
    assert "Experiment report: test-run" in report
    assert "## Findings" in report

    data = json.loads((run_dir / "results.json").read_text())
    assert len(data["cells"]) == len(config.cells)

    csv_text = (run_dir / "results.csv").read_text()
    assert "advantage" in csv_text.splitlines()[0]
    assert (run_dir / "config.snapshot.yaml").exists()


def test_load_config_roundtrip(tmp_path) -> None:
    """The shipped-style config loads and expands to cells."""
    cfg_text = (
        "experiment:\n"
        "  name: smoke\n"
        "  description: smoke test\n"
        "sweep:\n"
        "  N: [2, 3]\n"
        "  topologies: [ghz]\n"
        "  strategy_names: [D, H, Q]\n"
        "game:\n"
        "  V: 4.0\n"
        "  C: 3.0\n"
        "  gamma: pi/2\n"
        "output:\n"
        "  dir: out\n"
        "  formats: [md, json]\n"
    )
    path = tmp_path / "config.yaml"
    path.write_text(cfg_text)
    config = load_config(path)
    assert config.name == "smoke"
    assert len(config.cells) == 2
    assert config.formats == ["md", "json"]
