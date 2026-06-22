"""Draw entanglement-topology graphs and EWL circuit diagrams.

Two views of "the qubit topology being used":
  * Topology GRAPH  -- nodes = qubits/players, edges = entangling pairs. This is
    where the topology actually shows: ring (cycle), star (hub+spokes),
    fully-connected (all pairs). GHZ and W are global N-body entanglers with NO
    pairwise edge set, so they get a distinct "global" depiction (shaded region +
    label) rather than being drawn as a complete graph (which would look like
    fully-connected and mislead).
  * CIRCUIT diagram -- the EWL protocol J · per-player U · J†. The entangler J is
    a single boxed unitary, so this diagram has the same shape for every topology
    at a given N; it documents the protocol, not the topology structure.

Headless (Agg backend), 120 dpi, matching src/experiment/plots.py conventions.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # headless; no display required

import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402

from circuits.ewl import q_strategy  # noqa: E402
from circuits.n_player import build_ewl_qc  # noqa: E402
from circuits.topologies import Entangler, ghz_entangler  # noqa: E402
from circuits.topology_graphs import topology_graph  # noqa: E402

# Palette: pairwise topologies in blue, global (ghz/w) in amber.
_PAIRWISE_NODE = "#cfe3ff"
_PAIRWISE_EDGE = "#1f5fbf"
_GLOBAL_FILL = "#ffe6b3"
_GLOBAL_NODE = "#ffcf66"
_GLOBAL_EDGE = "#b8860b"


def _positions(graph: nx.Graph, name: str, N: int) -> dict[int, tuple[float, float]]:
    """Node layout: hub-centred for star, circular otherwise."""
    if name == "star":
        pos: dict[int, tuple[float, float]] = {0: (0.0, 0.0)}
        spokes = N - 1
        for k in range(1, N):
            ang = 2 * math.pi * (k - 1) / max(spokes, 1)
            pos[k] = (math.cos(ang), math.sin(ang))
        return pos
    return nx.circular_layout(graph)


def draw_topology_graph(name: str, N: int, *, ax: Any = None) -> Any:
    """Draw the topology graph for `name` at N qubits onto `ax` (created if None).

    Returns the matplotlib Figure containing the drawing.
    """
    graph = topology_graph(name, N)
    pos = _positions(graph, name, N)

    created = ax is None
    if created:
        _, ax = plt.subplots(figsize=(3.4, 3.4))

    if graph.graph["kind"] == "global":
        # Distinct global depiction: shaded region behind the nodes, faint dashed
        # spokes to a central marker, NO pairwise edges. Unmistakable vs. K_N.
        ax.add_patch(plt.Circle((0.0, 0.0), 1.32, color=_GLOBAL_FILL, alpha=0.55, zorder=0))
        for node, (x, y) in pos.items():
            ax.plot([0.0, x], [0.0, y], color=_GLOBAL_EDGE, lw=0.8, ls=":", zorder=1)
        nx.draw_networkx_nodes(
            graph, pos, ax=ax, node_color=_GLOBAL_NODE,
            edgecolors=_GLOBAL_EDGE, node_size=620,
        )
        nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10)
        ax.text(
            0.0, 0.0, name.upper(), ha="center", va="center",
            fontsize=11, fontweight="bold", color=_GLOBAL_EDGE, zorder=3,
        )
    else:
        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=_PAIRWISE_EDGE, width=2.0)
        nx.draw_networkx_nodes(
            graph, pos, ax=ax, node_color=_PAIRWISE_NODE,
            edgecolors=_PAIRWISE_EDGE, node_size=620,
        )
        nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10)

    ax.set_title(f"{name} · N={N}\n{graph.graph['label']}", fontsize=9)
    ax.set_aspect("equal")
    ax.set_axis_off()
    # Explicit SQUARE limits centred on the node cloud — keeps colinear layouts
    # (e.g. star at N=2/3: hub + opposite spokes all on one line) from collapsing to
    # a thin strip, and leaves room for the global topologies' shaded circle (r≈1.32).
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    half = max((max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2, 1.0) * 1.3
    half = max(half, 1.45)
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half, cy + half)
    return ax.figure


def draw_circuit(
    N: int,
    *,
    entangler: Entangler = ghz_entangler,
    gamma: float | None = None,
    strategies: list[tuple[float, float, float]] | None = None,
) -> tuple[str, Any]:
    """Render the EWL circuit for N players.

    Returns ("mpl", Figure) on success, or ("text", str) if the matplotlib drawer
    is unavailable (e.g. missing optional pylatexenc) — a graceful fallback that
    never aborts a run.
    """
    if strategies is None:
        strategies = [q_strategy(N)] * N
    kwargs: dict[str, Any] = {"entangler": entangler}
    if gamma is not None:
        kwargs["gamma"] = gamma
    qc = build_ewl_qc(N, strategies, **kwargs)
    try:
        fig = qc.draw(output="mpl", fold=-1)
        return "mpl", fig
    except Exception:  # noqa: BLE001 — fall back to text rendering
        return "text", str(qc.draw(output="text"))


def write_topology_folder(
    topologies: list[str], n_values: list[int], out_dir: str | Path
) -> dict[str, list[str]]:
    """Write INDIVIDUAL topology-graph + EWL-circuit images into a shared folder.

    Files are grouped into one subfolder per topology: `<topology>/<topology>_N{n}.png`
    for each (topology, N), and EWL circuits into `ewl/ewl_N{n}.png` per N (text
    `.txt` fallback if the matplotlib circuit drawer is unavailable). Deterministic
    paths make this overwrite-safe across runs and N-sets, so it suits a single
    shared `results/topology/` folder. Returns
    {"graphs": [relpaths], "circuits": [relpaths]} (paths relative to `out_dir`).
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ns = sorted(set(n_values))
    written: dict[str, list[str]] = {"graphs": [], "circuits": []}

    for name in topologies:
        subdir = out_dir / name
        subdir.mkdir(parents=True, exist_ok=True)
        for n in ns:
            fig = draw_topology_graph(name, n)
            fig.tight_layout()
            fname = f"{name}_N{n}.png"
            # No bbox_inches="tight": the square axes define the saved area, so
            # colinear layouts aren't cropped to a thin strip.
            fig.savefig(subdir / fname, dpi=120)
            plt.close(fig)
            written["graphs"].append(f"{name}/{fname}")

    ewl_dir = out_dir / "ewl"
    ewl_dir.mkdir(parents=True, exist_ok=True)
    for n in ns:
        kind, obj = draw_circuit(n)
        if kind == "mpl":
            fname = f"ewl_N{n}.png"
            obj.savefig(ewl_dir / fname, dpi=120, bbox_inches="tight")
            plt.close(obj)
        else:
            fname = f"ewl_N{n}.txt"
            (ewl_dir / fname).write_text(obj)
        written["circuits"].append(f"ewl/{fname}")

    return written
