"""Draw a single entanglement topology and/or its EWL circuit on demand.

Examples (from repo root):
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/draw_topology.py --topology star --N 5
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/draw_topology.py --topology ghz --N 4 --what both
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/draw_topology.py --topology ring --N 6 --out /tmp/diag

Topology names accept the same aliases as the experiment harness (e.g. "full" ->
"fully-connected"). Writes PNG(s) to --out, or to a results_io run folder by default.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpu_limit  # noqa: E402,F401  (caps BLAS threads; MUST precede numpy import)

import matplotlib.pyplot as plt  # noqa: E402

import results_io  # noqa: E402
from experiment.topology_registry import canonical, resolve  # noqa: E402
from experiment.topology_viz import draw_circuit, draw_topology_graph  # noqa: E402


def _parse_gamma(text: str) -> float:
    # Reuse the harness's whitelist parser for "pi/2"-style values.
    from experiment.config import parse_gamma

    return parse_gamma(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Draw a qubit entanglement topology.")
    parser.add_argument("--topology", required=True, help="ghz | ring | star | fully-connected | w (aliases ok)")
    parser.add_argument("--N", type=int, required=True, help="number of qubits/players")
    parser.add_argument("--gamma", default="pi/2", help="entanglement parameter (number or pi-expression)")
    parser.add_argument("--what", choices=["graph", "circuit", "both"], default="both")
    parser.add_argument("--out", default=None, help="output directory (default: a results_io run folder)")
    args = parser.parse_args()

    name = canonical(args.topology)
    gamma = _parse_gamma(args.gamma)

    if args.out:
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = results_io.new_run_dir("topology_diagrams")

    written: list[Path] = []

    if args.what in ("graph", "both"):
        fig = draw_topology_graph(name, args.N)
        path = out_dir / f"{name}_N{args.N}_graph.png"
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        written.append(path)

    if args.what in ("circuit", "both"):
        entangler = resolve(name, args.N)
        kind, obj = draw_circuit(args.N, entangler=entangler, gamma=gamma)
        if kind == "mpl":
            path = out_dir / f"{name}_N{args.N}_circuit.png"
            obj.savefig(path, dpi=120, bbox_inches="tight")
            plt.close(obj)
        else:
            path = out_dir / f"{name}_N{args.N}_circuit.txt"
            path.write_text(obj)
        written.append(path)

    for p in written:
        print(f"Wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
