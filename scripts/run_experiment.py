"""Run a parameterized experiment sweep and write a readable report.

Tweak experiments/config.yaml, then run from the repo root:
  PYTHONPATH=src python scripts/run_experiment.py
  PYTHONPATH=src python scripts/run_experiment.py --config path/to.yaml

Writes a timestamped run directory under results/<name>/<UTC-timestamp>/
(via results_io, the project-standard run-folder convention) containing:
  report.md             human-readable findings (primary deliverable)
  results.json          full structured results (incl. per-player vectors)
  results.csv           flat one-row-per-cell table
  config.snapshot.yaml  exact expanded cells used
  metadata.json         git commit / python / params provenance (results_io)
  plots/*.png           advantage-vs-N and topology x N heatmap

A non-positive advantage or non-Nash (Q,...,Q) is a FINDING, not a bug -- it is
reported, not hidden. Unknown/unimplemented topologies are recorded, not fatal.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import results_io  # noqa: E402
from experiment import load_config, run_sweep, write_outputs  # noqa: E402
from experiment.sweep import summarize  # noqa: E402


def _slug(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an experiment sweep and report.")
    parser.add_argument(
        "--config",
        default="experiments/config.yaml",
        help="Path to the YAML experiment config (default: experiments/config.yaml).",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Override the experiment name used in the run-dir label.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    if args.name:
        config.name = args.name

    print(f"Running '{config.name}': {len(config.cells)} cell(s)...")
    results = run_sweep(config.cells)

    timestamp = results_io.run_timestamp()
    run_dir = results_io.new_run_dir(_slug(config.name), timestamp)

    write_outputs(config, results, run_dir, timestamp)
    results_io.write_metadata(
        run_dir,
        config.name,
        params={
            "description": config.description,
            "n_cells": len(config.cells),
            "topologies": sorted({c.topology for c in config.cells}),
            "N_values": sorted({c.N for c in config.cells}),
            "V": sorted({c.V for c in config.cells}),
            "C": sorted({c.C for c in config.cells}),
            "gamma": sorted({c.gamma_label for c in config.cells}),
            "strategy_names": list(config.cells[0].strategy_names),
            "formats": config.formats,
        },
    )

    summary = summarize(results)
    print(
        f"Done. {summary.ok}/{summary.total} cells ran "
        f"({summary.positive_advantage} with advantage > 0, "
        f"{summary.not_implemented} not-implemented, {summary.error} errored)."
    )
    print(f"Report: {os.path.join(str(run_dir), 'report.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
