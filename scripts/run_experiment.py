"""Run a parameterized experiment sweep and write a readable report.

Tweak experiments/config.yaml, then run from the repo root:
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/run_experiment.py
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/run_experiment.py --config path/to.yaml

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

import cpu_limit  # noqa: E402,F401  (caps BLAS threads; MUST precede numpy import)
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
    modes = {c.strategy_mode for c in config.cells}
    if modes - {"fixed"}:
        print(
            f"  strategy_mode {sorted(modes)} runs a per-cell SU(2) optimization "
            f"(compute-heavy; cost grows with N and cell count) — progress below."
        )

    def _progress(event: str, info: dict) -> None:
        c = info["cell"]
        tag = f"[{info['index']}/{info['total']}] N={c.N} {c.topology} ({c.strategy_mode})"
        if event == "start":
            print(f"{tag} ...", end="", flush=True)
        else:
            r = info["result"]
            extra = ""
            if r.result is not None:
                extra = f" advantage={r.result['advantage']:.3f}"
                if r.strategy is not None:
                    extra += f", nash_gap={r.strategy['nash_gap']:.2e}, is_nash={r.strategy['is_nash']}"
            print(f"\r{tag} -> {r.status} in {info['elapsed']:.1f}s{extra}", flush=True)

    results = run_sweep(config.cells, on_event=_progress)

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
            "noise_p": sorted({c.noise_p for c in config.cells}),
            "strategy_names": list(config.cells[0].strategy_names),
            "formats": config.formats,
        },
    )

    # Topology diagrams live in a single shared results/topology/ folder (not in
    # each run folder). Refresh it from the config's topologies × N values.
    if "plots" in config.formats:
        from experiment.topology_registry import canonical
        from experiment.topology_viz import write_topology_folder
        from circuits.topology_graphs import KNOWN_TOPOLOGIES

        topos = sorted(
            {canonical(c.topology) for c in config.cells} & set(KNOWN_TOPOLOGIES)
        )
        ns = sorted({c.N for c in config.cells})
        if topos and ns:
            topo_dir = results_io.RESULTS_ROOT / "topology"
            write_topology_folder(topos, ns, topo_dir)
            print(f"Topology diagrams: {topo_dir}")

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
