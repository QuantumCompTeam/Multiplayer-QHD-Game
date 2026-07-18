"""Matplotlib figures for a sweep, plus the noise-threshold p* extractor.

advantage-vs-N lines + a topology x N heatmap always; advantage-vs-gamma lines + a
gamma x topology heatmap when gamma varies across the sweep; 3D (N x p) advantage
surfaces per topology when noise_p varies (Month 4 / RQ3).

Uses the non-interactive Agg backend so it runs headless. Only cells with status
"ok" contribute data points; missing/failed pairs render as greyed cells in heatmaps.
Returns the list of PNG filenames actually written.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Sequence

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
    """Append any swept secondary params (gamma/V/C/noise_p) that vary, to disambiguate."""
    parts: list[str] = []
    if vary["gamma"]:
        parts.append(f"γ={r.cell.gamma_label}")
    if vary["V"]:
        parts.append(f"V={r.cell.V:g}")
    if vary["C"]:
        parts.append(f"C={r.cell.C:g}")
    if vary["noise_p"]:
        parts.append(f"p={r.cell.noise_p:g}")
    return (" (" + ", ".join(parts) + ")") if parts else ""


def _varying(results: list[CellResult]) -> dict[str, bool]:
    return {
        "N": len({r.cell.N for r in results}) > 1,
        "gamma": len({r.cell.gamma_label for r in results}) > 1,
        "V": len({r.cell.V for r in results}) > 1,
        "C": len({r.cell.C for r in results}) > 1,
        "noise_p": len({r.cell.noise_p for r in results}) > 1,
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
    ax.set_ylabel("quantum advantage (Q-profile − classical NE)")
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
    ax.set_ylabel("quantum advantage (Q-profile − classical NE)")
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


def extract_pstar(
    ps: Sequence[float],
    advantages: Sequence[float],
    q_is_nash: Sequence[bool],
) -> float | None:
    """Noise threshold p* for one (topology, N) series (Month-4 spec §4.4).

    p* is the smallest p at which the series loses its quantum advantage:
      - mean advantage <= 0 — linearly interpolated between the bracketing grid
        points (the published number must not be off by a grid step), or
      - (Q,...,Q) STOPS being a pure Nash equilibrium — a True->False flip,
        reported at the flip's grid point (a boolean has no in-between to
        interpolate),
    whichever happens at the smaller p. A series that was never Nash at any
    swept p has nothing to "stop" being — the Nash criterion is inert there and
    p* is governed by the advantage crossing alone (the caller should surface
    the never-Nash fact separately; it is a Month-3 fixed-mode finding
    (non-GHZ topologies, and GHZ itself at N >= 4), not noise fragility).
    Returns None when the advantage survives the whole grid
    (report as "> p_max", a finding, not a failure).

    Pure logic on already-computed series; feeds the published p* table. The
    series may be passed in any order — it is sorted by p here.
    """
    if not (len(ps) == len(advantages) == len(q_is_nash)):
        raise ValueError(
            f"extract_pstar: mismatched series lengths "
            f"{len(ps)}/{len(advantages)}/{len(q_is_nash)}"
        )
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    seen_nash = False
    prev_p: float | None = None
    prev_adv = 0.0
    for i in order:
        p, adv, nash = float(ps[i]), float(advantages[i]), bool(q_is_nash[i])
        if adv <= 0.0:
            if prev_p is None:
                return p  # dead already at the first grid point
            # prev_adv > 0 here (else we would have returned on that point).
            return prev_p + (p - prev_p) * prev_adv / (prev_adv - adv)
        if seen_nash and not nash:
            return p
        seen_nash = seen_nash or nash
        prev_p, prev_adv = p, adv
    return None


def _noise_surfaces(ok: list[CellResult], plots_dir: Path) -> list[str]:
    """3D advantage surface over (N, p), one PNG per topology (Month 4 / RQ3).

    Needs at least a 2x2 (N, p) grid per topology to define a surface; smaller
    series are skipped (the summary table still carries their numbers).
    """
    by_topo: dict[str, dict[tuple[int, float], float]] = {}
    for r in ok:
        by_topo.setdefault(r.cell.topology, {})[(r.cell.N, r.cell.noise_p)] = float(
            r.advantage  # type: ignore[arg-type]
        )

    written: list[str] = []
    noise_dir = plots_dir / "noise"
    for topo, cells in sorted(by_topo.items()):
        ns = sorted({n for n, _ in cells})
        ps = sorted({p for _, p in cells})
        if len(ns) < 2 or len(ps) < 2:
            continue
        grid = np.full((len(ps), len(ns)), np.nan)
        for (n, p), adv in cells.items():
            grid[ps.index(p), ns.index(n)] = adv

        noise_dir.mkdir(parents=True, exist_ok=True)
        xs, ys = np.meshgrid(ns, ps)
        fig = plt.figure(figsize=(7.5, 5.5))
        ax = fig.add_subplot(projection="3d")
        surf = ax.plot_surface(
            xs, ys, grid, cmap="viridis", edgecolor="k", linewidth=0.3, alpha=0.95
        )
        ax.set_xticks(ns)
        ax.set_xlabel("N (players)")
        ax.set_ylabel("depolarizing p")
        ax.set_zlabel("quantum advantage")
        ax.set_title(f"Advantage surface — {topo}")
        fig.colorbar(surf, shrink=0.6, pad=0.1, label="advantage")
        out = noise_dir / f"advantage_surface_{topo}.png"
        fig.savefig(out, dpi=120, bbox_inches="tight")
        plt.close(fig)
        written.append(f"noise/{out.name}")
    return written


def _per_player_advantage(ok: list[CellResult], plots_dir: Path) -> list[str]:
    """Per-player advantage bar charts for ASYMMETRIC topologies (one per topology).

    Vertex-transitive topologies have a uniform per-player advantage, so the
    scalar mean (covered by the other plots) is the whole story. For a topology
    with any `symmetric=False` cell (today: the star, hub vs leaves) the mean
    hides a per-player split, so we draw it explicitly: x-axis = N, with the
    per-player `advantage_vector` shown as grouped bars. Players are grouped by
    role — `hub` (player 0) and `leaf` (players 1..N-1, which share one value) —
    so the chart stays readable and generalises to any orbit structure.

    Returns the filenames written (one per asymmetric topology), or [] if none.
    """
    asym = [r for r in ok if r.result is not None and not r.result["symmetric"]]
    if not asym:
        return []

    written: list[str] = []
    topologies = sorted({r.cell.topology for r in asym})
    for topo in topologies:
        cells = sorted(
            (r for r in asym if r.cell.topology == topo), key=lambda r: r.cell.N
        )
        ns = [r.cell.N for r in cells]
        hub = [float(r.result["advantage_vector"][0]) for r in cells]
        # Leaves share one value (star automorphism); take player 1 as the leaf.
        leaf = [float(r.result["advantage_vector"][1]) for r in cells]
        mean = [float(r.advantage) for r in cells]  # type: ignore[arg-type]

        x = np.arange(len(ns), dtype=float)
        w = 0.28
        fig, ax = plt.subplots(figsize=(1.3 * len(ns) + 3, 4.5))
        ax.bar(x - w, hub, width=w, label="hub (player 0)", color="#c44e52", alpha=0.9)
        ax.bar(x, leaf, width=w, label="leaf (players 1..N-1)", color="#4c72b0", alpha=0.9)
        ax.bar(x + w, mean, width=w, label="mean (per-player)", color="#55a868", alpha=0.6)
        ax.axhline(0.0, color="grey", linewidth=0.8, linestyle="--", zorder=1)
        ax.set_xticks(x, [str(n) for n in ns])
        ax.set_xlabel("N (players)")
        ax.set_ylabel("quantum advantage (Q-profile − classical NE)")
        ax.set_title(
            f"Per-player advantage — {topo} (asymmetric: hub vs leaf)"
        )
        _legend_outside(ax)
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        out = plots_dir / f"per_player_advantage_{topo}.png"
        fig.savefig(out, dpi=120, bbox_inches="tight")
        plt.close(fig)
        written.append(out.name)
    return written


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

    # Per-player advantage for asymmetric topologies (the scalar mean hides the
    # hub/leaf split); only emitted when an asymmetric cell is present. Skipped
    # when noise_p is swept: gate-level noise makes even symmetric topologies
    # slightly player-asymmetric, and multiple p values per (topology, N) would
    # overprint the bars (the per-cell report still carries the vectors).
    if not vary["noise_p"]:
        written += _per_player_advantage(ok, plots_dir)

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

    # Noise-robustness surfaces (Month 4 / RQ3) — only when noise_p is swept.
    if vary["noise_p"]:
        written += _noise_surfaces(ok, plots_dir)
    return written
