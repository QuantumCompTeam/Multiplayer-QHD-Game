"""Matplotlib figures for a sweep: advantage-vs-N lines and a topology x N heatmap.

Uses the non-interactive Agg backend so it runs headless. Only cells with status
"ok" contribute data points; missing/failed (topology, N) pairs render as greyed
cells in the heatmap. Returns the list of PNG filenames actually written.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless; no display required

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from experiment.sweep import STATUS_OK, CellResult  # noqa: E402


def _secondary_label(r: CellResult, vary: dict[str, bool]) -> str:
    """Append any swept secondary params (gamma/V/C) that vary, to disambiguate."""
    parts: list[str] = []
    if vary["gamma"]:
        parts.append(f"γ={r.cell.gamma_label}")
    if vary["V"]:
        parts.append(f"V={r.cell.V:g}")
    if vary["C"]:
        parts.append(f"C={r.cell.C:g}")
    return (" (" + ", ".join(parts) + ")") if parts else ""


def _varying(results: list[CellResult]) -> dict[str, bool]:
    return {
        "gamma": len({r.cell.gamma_label for r in results}) > 1,
        "V": len({r.cell.V for r in results}) > 1,
        "C": len({r.cell.C for r in results}) > 1,
    }


def _advantage_vs_n(ok: list[CellResult], vary: dict[str, bool], out: Path) -> str:
    series: dict[str, list[tuple[int, float]]] = {}
    for r in ok:
        key = r.cell.topology + _secondary_label(r, vary)
        series.setdefault(key, []).append((r.cell.N, float(r.advantage)))  # type: ignore[arg-type]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for label, pts in sorted(series.items()):
        pts.sort()
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, marker="o", label=label)
    ax.axhline(0.0, color="grey", linewidth=0.8, linestyle="--")
    ax.set_xlabel("N (players)")
    ax.set_ylabel("quantum advantage (QNE − CNE)")
    ax.set_title("Quantum advantage vs N")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out.name


def _topology_heatmap(ok: list[CellResult], out: Path) -> str | None:
    """Heatmap of advantage over (topology, N).

    Skipped when secondary params (gamma/V/C) collide on a (topology, N) cell,
    since a single grid cell can't honestly show multiple values.
    """
    cell_map: dict[tuple[str, int], float] = {}
    for r in ok:
        key = (r.cell.topology, r.cell.N)
        if key in cell_map:
            return None  # ambiguous grid — line chart already covers this case
        cell_map[key] = float(r.advantage)  # type: ignore[arg-type]

    topologies = sorted({r.cell.topology for r in ok})
    ns = sorted({r.cell.N for r in ok})
    grid = np.full((len(topologies), len(ns)), np.nan)
    for i, topo in enumerate(topologies):
        for j, n in enumerate(ns):
            if (topo, n) in cell_map:
                grid[i, j] = cell_map[(topo, n)]

    masked = np.ma.masked_invalid(grid)
    cmap = plt.cm.viridis.copy()
    cmap.set_bad(color="lightgrey")

    fig, ax = plt.subplots(figsize=(1.2 * len(ns) + 2, 0.7 * len(topologies) + 2))
    im = ax.imshow(masked, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(ns)), [str(n) for n in ns])
    ax.set_yticks(range(len(topologies)), topologies)
    ax.set_xlabel("N (players)")
    ax.set_title("Quantum advantage by topology × N")
    for i in range(len(topologies)):
        for j in range(len(ns)):
            if not masked.mask[i, j]:
                ax.text(j, i, f"{grid[i, j]:.2f}", ha="center", va="center",
                        color="white", fontsize=8)
    fig.colorbar(im, ax=ax, label="advantage")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out.name


def write_plots(results: list[CellResult], plots_dir: str | Path) -> list[str]:
    """Write available plots into plots_dir; return the filenames written."""
    plots_dir = Path(plots_dir)
    ok = [r for r in results if r.status == STATUS_OK and r.advantage is not None]
    if not ok:
        return []
    plots_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    vary = _varying(results)
    written.append(_advantage_vs_n(ok, vary, plots_dir / "advantage_vs_N.png"))
    heatmap = _topology_heatmap(ok, plots_dir / "topology_heatmap.png")
    if heatmap:
        written.append(heatmap)
    return written
