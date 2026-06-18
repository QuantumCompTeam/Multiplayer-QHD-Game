"""Parameterized experiment harness: tweak config.yaml -> run sweep -> read report.

Public API:
  load_config   -- parse + validate experiments/config.yaml into ExperimentConfig
  run_sweep     -- evaluate every parameter cell via game.nash.compute_advantage
  write_outputs -- write report.md, results.json, results.csv, and plots/

The harness reuses compute_advantage from game.nash verbatim; it adds no game
theory of its own. Unimplemented topologies degrade gracefully to a "not-implemented"
cell status instead of aborting the run.
"""

from __future__ import annotations

from experiment.config import Cell, ExperimentConfig, load_config
from experiment.report import write_outputs
from experiment.sweep import CellResult, run_sweep

__all__ = [
    "Cell",
    "CellResult",
    "ExperimentConfig",
    "load_config",
    "run_sweep",
    "write_outputs",
]
