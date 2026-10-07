"""Regenerate the four zero-noise simulation figures of the paper.

Reads committed results only:
  results/n-scaling-advantage/2026-07-19T0901Z/results.csv  (Figs. 1, 2, 4)
  results/gamma-sweep/N4/results.csv                         (Fig. 3)
and writes vector PDFs into paper/figs/.

Usage: python scripts/plot_paper_simulation.py
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
N_SCALING = ROOT / "results" / "n-scaling-advantage" / "2026-07-19T0901Z" / "results.csv"
GAMMA_N4 = ROOT / "results" / "gamma-sweep" / "N4" / "results.csv"
OUT = ROOT / "paper" / "figs"

# Paper order and names of the entangler families.
FAMILIES = ["ghz", "w", "ring", "star", "fully-connected"]
LABELS = {"ghz": "GHZ", "w": "W", "ring": "ring", "star": "star",
          "fully-connected": "fully connected"}
STYLES = {  # colour, marker, linestyle; distinguishable in greyscale
    "ghz": ("#1f4e79", "o", "-"),
    "w": ("#7f3f98", "v", "-"),
    "ring": ("#2e7d32", "^", "-."),
    "star": ("#c62828", "D", "--"),
    "fully-connected": ("#ef8a17", "s", ":"),
}
GAP_LABEL = "circuit-relative payoff gap"
COLUMN_WIDTH = 3.45  # inches, IEEE two-column


def _style() -> None:
    plt.rcParams.update({
        "font.size": 8, "axes.labelsize": 8, "legend.fontsize": 7,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,
    })


def _rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["status"] == "ok"]


def _is_true(value: str) -> bool:
    return value.strip().lower() == "true"


def _series(rows: list[dict], key: str) -> dict[str, list[tuple[float, float, bool]]]:
    out: dict[str, list[tuple[float, float, bool]]] = {f: [] for f in FAMILIES}
    for r in rows:
        out[r["topology"]].append((float(r[key]), float(r["advantage"]), _is_true(r["q_is_nash"])))
    for f in out:
        out[f].sort()
    return out


def _plot_lines(ax, series, offsets) -> None:
    for fam in FAMILIES:
        colour, marker, ls = STYLES[fam]
        xs = np.array([p[0] for p in series[fam]]) + offsets.get(fam, 0.0)
        ys = [p[1] for p in series[fam]]
        ax.plot(xs, ys, ls=ls, color=colour, lw=1.1, label=LABELS[fam], zorder=2)
        for x, y, nash in zip(xs, ys, [p[2] for p in series[fam]]):
            ax.plot(x, y, marker=marker, ms=4.2, color=colour, zorder=3,
                    markerfacecolor=colour if nash else "white", markeredgewidth=1.0)
    ax.axhline(0.0, color="0.5", lw=0.6, ls=":", zorder=1)
    ax.grid(axis="y", color="0.9", lw=0.5)


def advantage_vs_n(rows: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(COLUMN_WIDTH, 2.3))
    # Small horizontal offsets keep coincident markers visible.
    offsets = {"ghz": -0.08, "w": -0.04, "ring": 0.0, "star": 0.04, "fully-connected": 0.08}
    _plot_lines(ax, _series(rows, "N"), offsets)
    ax.set_xticks(range(2, 7))
    ax.set_xlabel("number of players $N$")
    ax.set_ylabel(GAP_LABEL)
    ax.legend(ncol=3, frameon=False, loc="lower left", handlelength=2.4,
              bbox_to_anchor=(0.0, 1.0), borderaxespad=0.2)
    fig.savefig(OUT / "advantage_vs_N.pdf")
    plt.close(fig)


def topology_heatmap(rows: list[dict]) -> None:
    ns = sorted({int(r["N"]) for r in rows})
    grid = np.full((len(FAMILIES), len(ns)), np.nan)
    for r in rows:
        grid[FAMILIES.index(r["topology"]), ns.index(int(r["N"]))] = float(r["advantage"])
    grid[np.abs(grid) < 1e-12] = 0.0
    fig, ax = plt.subplots(figsize=(COLUMN_WIDTH, 2.1))
    im = ax.imshow(grid, cmap="Greys", vmin=0.0, vmax=1.6, aspect="auto")
    for i in range(len(FAMILIES)):
        for j in range(len(ns)):
            v = grid[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if v > 0.9 else "black")
    ax.set_xticks(range(len(ns)), [str(n) for n in ns])
    ax.set_yticks(range(len(FAMILIES)), [LABELS[f] for f in FAMILIES])
    ax.set_xlabel("number of players $N$")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    cbar = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03)
    cbar.set_label(GAP_LABEL)
    cbar.ax.tick_params(labelsize=7)
    fig.savefig(OUT / "topology_heatmap.pdf")
    plt.close(fig)


def advantage_vs_gamma(rows: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(COLUMN_WIDTH, 2.3))
    series = _series(rows, "gamma")
    scaled = {f: [(g / math.pi, a, n) for g, a, n in pts] for f, pts in series.items()}
    offsets = {"ghz": -0.006, "star": 0.006}
    _plot_lines(ax, scaled, offsets)
    ticks = sorted({round(g, 2) for pts in scaled.values() for g, _, _ in pts})
    ax.set_xticks(ticks, ["0" if t == 0 else f"{t:g}$\\pi$" for t in ticks])
    ax.set_xlabel(r"entanglement angle $\gamma$")
    ax.set_ylabel(GAP_LABEL)
    ax.set_ylim(-0.05, 0.85)
    ax.legend(ncol=3, frameon=False, loc="lower left", handlelength=2.4,
              bbox_to_anchor=(0.0, 1.0), borderaxespad=0.2)
    fig.savefig(OUT / "advantage_vs_gamma_N4.pdf")
    plt.close(fig)


def per_player_star(rows: list[dict]) -> None:
    star = sorted((r for r in rows if r["topology"] == "star" and int(r["N"]) >= 4),
                  key=lambda r: int(r["N"]))
    ns = [int(r["N"]) for r in star]
    vectors = [json.loads(r["advantage_vector"]) for r in star]
    hub = [v[0] for v in vectors]          # implementation qubit 0 = paper player 1
    leaf = [float(np.mean(v[1:])) for v in vectors]
    mean = [float(np.mean(v)) for v in vectors]
    x = np.arange(len(ns))
    w = 0.26
    fig, ax = plt.subplots(figsize=(COLUMN_WIDTH, 2.2))
    bars = [(hub, "hub (player 1)", "#c62828", "", -w),
            (leaf, "leaf (players 2..$N$)", "#1f4e79", "", 0.0),
            (mean, "mean", "white", "////", w)]
    for vals, label, colour, hatch, dx in bars:
        b = ax.bar(x + dx, vals, w, label=label, color=colour, hatch=hatch,
                   edgecolor="black", linewidth=0.6)
        ax.bar_label(b, labels=[f"{abs(v):.2f}" if abs(v) < 5e-3 else f"{v:.2f}" for v in vals],
                     fontsize=6.5, padding=1.5)
    ax.set_xticks(x, [f"$N={n}$" for n in ns])
    ax.set_ylabel(GAP_LABEL)
    ax.set_ylim(0, 1.2)
    ax.legend(frameon=False, loc="upper center", ncol=3, fontsize=6.5,
              bbox_to_anchor=(0.5, 1.13), handlelength=1.5, columnspacing=1.0)
    ax.grid(axis="y", color="0.9", lw=0.5)
    ax.set_axisbelow(True)
    fig.savefig(OUT / "per_player_advantage_star.pdf")
    plt.close(fig)


def main() -> None:
    _style()
    OUT.mkdir(parents=True, exist_ok=True)
    n_rows = [r for r in _rows(N_SCALING) if float(r["noise_p"]) == 0.0]
    advantage_vs_n(n_rows)
    topology_heatmap(n_rows)
    per_player_star(n_rows)
    advantage_vs_gamma([r for r in _rows(GAMMA_N4) if float(r["noise_p"]) == 0.0])
    print(f"wrote 4 figures to {OUT}")


if __name__ == "__main__":
    main()
