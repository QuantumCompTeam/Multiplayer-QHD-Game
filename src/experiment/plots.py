"""Matplotlib figures for a sweep.

advantage-vs-N lines + a topology x N heatmap always; advantage-vs-gamma lines + a
gamma x topology heatmap when gamma varies across the sweep.

Uses the non-interactive Agg backend so it runs headless. Only cells with status
"ok" contribute data points; missing/failed pairs render as greyed cells in heatmaps.
Returns the list of PNG filenames actually written.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless; no display required

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from experiment.sweep import STATUS_OK, CellResult  # noqa: E402

# Cycled so coincident series (topologies whose advantage is identical) stay
# distinguishable — the alternating dash/marker pattern reveals the overlap.
_LINESTYLES = ["-", "--", "-.", ":"]
_MARKERS = ["o", "s", "^", "D", "v", "P", "X"]


def _style(i: int) -> dict:
    return {
        "linestyle": _LINESTYLES[i % len(_LINESTYLES)],
        "marker": _MARKERS[i % len(_MARKERS)],
        "alpha": 0.8,
        "markersize": 6,
        "zorder": 3 + i,  # later series sit on top, but alpha keeps earlier ones visible
    }


def _legend_outside(ax) -> None:
    """Place the legend to the right of the axes so many series never overprint it."""
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0)


def _smooth_curve(xs, ys, n: int = 200):
    """Dense, shape-preserving (PCHIP) curve through (xs, ys).

    PCHIP (monotone cubic) is smooth but does NOT overshoot, so sharp real features
    (e.g. the ring's dip to 0 at N=4) stay honest rather than sprouting fake wiggles.
    Falls back to the raw points when there are too few to interpolate (<3); xs must
    be strictly increasing (true for the sorted, unique N / γ values in both callers).
    """
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    if len(xs) < 3:
        return xs, ys
    from scipy.interpolate import PchipInterpolator

    xq = np.linspace(xs.min(), xs.max(), n)
    return xq, PchipInterpolator(xs, ys)(xq)


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
        "N": len({r.cell.N for r in results}) > 1,
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
    for i, (label, pts) in enumerate(sorted(series.items())):
        pts.sort()
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        style = _style(i)
        marker = style.pop("marker")
        xq, yq = _smooth_curve(xs, ys)
        (line,) = ax.plot(xq, yq, label=label, **style)  # smooth curve, no markers
        # Real computed points marked on the curve.
        ax.plot(xs, ys, linestyle="none", marker=marker, color=line.get_color(),
                alpha=0.8, markersize=6, zorder=style["zorder"])
    ax.axhline(0.0, color="grey", linewidth=0.8, linestyle="--", zorder=1)
    ax.set_xlabel("N (players)")
    ax.set_ylabel("quantum advantage (QNE − CNE)")
    ax.set_title("Quantum advantage vs N")
    _legend_outside(ax)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=120, bbox_inches="tight")
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


def _advantage_vs_gamma(ok: list[CellResult], vary: dict[str, bool], out: Path) -> str:
    """Advantage vs entanglement strength gamma; filled marker where (Q,..,Q) is Nash.

    One line per topology (per (topology, N) if N also varies). The gamma at which a
    curve's markers switch from hollow (not Nash) to filled (Nash) is the entanglement
    threshold for the quantum equilibrium.
    """
    series: dict[str, list[tuple[float, float, bool]]] = {}
    for r in ok:
        key = r.cell.topology + (f" N={r.cell.N}" if vary["N"] else "")
        series.setdefault(key, []).append(
            (r.cell.gamma, float(r.advantage), bool(r.q_is_nash))  # type: ignore[arg-type]
        )

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, (label, pts) in enumerate(sorted(series.items())):
        pts.sort()
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        style = _style(i)
        marker = style.pop("marker")
        xq, yq = _smooth_curve(xs, ys)
        (line,) = ax.plot(xq, yq, label=label, **style)  # smooth curve, no markers
        color = line.get_color()
        # Filled marker where (Q,..,Q) is a pure Nash equilibrium, hollow where not.
        for x, y, is_nash in pts:
            ax.plot(
                x, y, marker=marker, color=color, alpha=0.8, zorder=style["zorder"],
                markerfacecolor=color if is_nash else "white",
                markeredgecolor=color,
            )
    ax.axhline(0.0, color="grey", linewidth=0.8, linestyle="--", zorder=1)
    # x ticks in units of pi for readability.
    xmax = max(r.cell.gamma for r in ok)
    n_ticks = 4
    ticks = [xmax * k / n_ticks for k in range(n_ticks + 1)]
    ax.set_xticks(ticks, [f"{t / math.pi:.2f}π" for t in ticks])
    ax.set_xlim(left=0.0)  # start the γ axis at the origin (no-entanglement baseline)
    ax.set_xlabel("entanglement γ (radians)")
    ax.set_ylabel("quantum advantage (QNE − CNE)")
    ax.set_title("Quantum advantage vs entanglement γ\n(filled = (Q,..,Q) is Nash)")
    _legend_outside(ax)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return out.name


def _gamma_topology_heatmap(ok: list[CellResult], out: Path) -> str | None:
    """Heatmap of advantage over (topology, gamma); '*' marks where (Q,..,Q) is Nash.

    Drawn only when a single N is present, so each (topology, gamma) maps to one cell.
    """
    if len({r.cell.N for r in ok}) != 1:
        return None  # ambiguous grid across N — the line plot covers this case
    cell_map: dict[tuple[str, float], tuple[float, bool]] = {}
    for r in ok:
        key = (r.cell.topology, r.cell.gamma)
        if key in cell_map:
            return None
        cell_map[key] = (float(r.advantage), bool(r.q_is_nash))  # type: ignore[arg-type]

    topologies = sorted({r.cell.topology for r in ok})
    gammas = sorted({r.cell.gamma for r in ok})
    grid = np.full((len(topologies), len(gammas)), np.nan)
    for i, topo in enumerate(topologies):
        for j, g in enumerate(gammas):
            if (topo, g) in cell_map:
                grid[i, j] = cell_map[(topo, g)][0]

    masked = np.ma.masked_invalid(grid)
    cmap = plt.cm.viridis.copy()
    cmap.set_bad(color="lightgrey")

    fig, ax = plt.subplots(figsize=(1.3 * len(gammas) + 2, 0.7 * len(topologies) + 2))
    im = ax.imshow(masked, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(gammas)), [f"{g / math.pi:.2f}π" for g in gammas])
    ax.set_yticks(range(len(topologies)), topologies)
    ax.set_xlabel("entanglement γ")
    ax.set_title("Advantage by topology × γ  ('*' = (Q,..,Q) is Nash)")
    for i, topo in enumerate(topologies):
        for j, g in enumerate(gammas):
            if not masked.mask[i, j]:
                star = "*" if cell_map[(topo, g)][1] else ""
                ax.text(j, i, f"{grid[i, j]:.2f}{star}", ha="center", va="center",
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
    # Advantage-vs-N is only meaningful when N actually varies; a single-N sweep
    # (e.g. the γ sweep) would otherwise stack every point on one x with an
    # exploded legend.
    if vary["N"]:
        written.append(_advantage_vs_n(ok, vary, plots_dir / "advantage_vs_N.png"))
    heatmap = _topology_heatmap(ok, plots_dir / "topology_heatmap.png")
    if heatmap:
        written.append(heatmap)

    # Entanglement-strength views — only meaningful when gamma is swept.
    if vary["gamma"]:
        written.append(
            _advantage_vs_gamma(ok, vary, plots_dir / "advantage_vs_gamma.png")
        )
        gamma_heatmap = _gamma_topology_heatmap(
            ok, plots_dir / "gamma_topology_heatmap.png"
        )
        if gamma_heatmap:
            written.append(gamma_heatmap)
    return written
