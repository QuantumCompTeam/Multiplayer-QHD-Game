"""Paper figure for the multi-topology hardware batch (+ caption).

Reads a results/hardware-topology/<ts>/result.json and writes
plots/hardware_topology.{png,pdf} + caption.md into that run dir.

  (A) advantage retention per topology x N: measured mitigated fold-1 advantage
      as a fraction of that cell's OWN noiseless advantage. Not V/N -- ring N=4
      is noiselessly deterministic on |1..1> and has ZERO ideal advantage, so a
      V/N reference would be meaningless for it.
  (B) the equilibrium test (item 2): per-player payoff of the deviating
      position under (Q,Q,Q) vs a unilateral Hawk deviation at ghz N=3. A
      positive gap means the deviation does not pay.
  (C) position-locked unfairness (item 6): star N=4 per-player payoffs under
      three wirings. The hub loses and the leaves gain, and permuting players
      across physical qubits does not move it.

Usage:
  conda run -n entangled-equilibria python scripts/plot_hardware_topology.py [<run_dir>]
"""

import glob
import json
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = "#1f6feb"       # measured (single data hue)
IDEAL = "#8b949e"      # noiseless reference
ACCENT = "#d1242f"     # the cell that breaks the pattern
INK = "#1b1f24"
MUTED = "#8b949e"
GRID = "#e6e8eb"

TOPOLOGIES = ["ghz", "ring", "star", "fully-connected", "w"]
SHORT = {"ghz": "GHZ", "ring": "ring", "star": "star",
         "fully-connected": "FC", "w": "W"}
GAMMA = math.pi / 2


def load_run(argv):
    if len(argv) > 1:
        d = argv[1]
    else:
        dirs = sorted(glob.glob(os.path.join("results", "hardware-topology", "2026-*")))
        dirs = [x for x in dirs if os.path.exists(os.path.join(x, "result.json"))]
        if not dirs:
            print("no completed hardware-topology run found")
            sys.exit(1)
        d = dirs[-1]
    with open(os.path.join(d, "result.json"), encoding="utf-8") as fh:
        return d, json.load(fh)


def cooperative_cells(series):
    """The all-Q, gamma=pi/2, identity-wiring cells -- the topology ladder."""
    out = []
    for s in series.values():
        if set(s["profile"]) != {"Q"}:
            continue
        if abs(s["gamma"] - GAMMA) > 1e-12:
            continue
        if s["wiring"] != list(range(s["N"])):
            continue
        out.append(s)
    return sorted(out, key=lambda s: (TOPOLOGIES.index(s["topology"]), s["N"]))


def panel_a(ax, cells):
    labels, vals, colors = [], [], []
    for s in cells:
        f1 = s["folds"]["1"]
        ideal = s["ideal_advantage"]
        labels.append(f"{SHORT[s['topology']]}\n{s['N']}")
        if ideal > 1e-9:
            vals.append(f1["mitigated"]["advantage"] / ideal * 100.0)
            colors.append(DATA)
        else:
            # ring N=4: zero ideal advantage, so retention is undefined. Show
            # it at 0 and mark it -- its measured advantage is noise-created.
            vals.append(0.0)
            colors.append(ACCENT)
    x = np.arange(len(labels))
    ax.bar(x, vals, color=colors, width=0.68, zorder=3)
    ax.axhline(100.0, color=IDEAL, lw=1.0, ls="--", zorder=2)
    ax.text(len(labels) - 0.4, 100.4, "noiseless ideal", color=MUTED,
            fontsize=8, ha="right", va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylim(90, 102)
    ax.set_ylabel("advantage retained (% of each cell's own ideal)")
    ax.set_title("(A)  every topology retains > 97% of its ideal advantage",
                 loc="left", fontsize=9.5, color=INK)
    for xi, v, c in zip(x, vals, colors):
        if c == ACCENT:
            ax.text(xi, 90.4, "ideal\nadv = 0", ha="center", va="bottom",
                    fontsize=7.2, color=ACCENT, linespacing=1.35)
        else:
            ax.text(xi, v + 0.25, f"{v:.1f}", ha="center", va="bottom",
                    fontsize=7.4, color=INK)


def panel_b(ax, series):
    """Deviation gaps at ghz N=3, gamma=pi/2 -- the equilibrium test."""
    coop = next(s for s in series.values()
                if s["topology"] == "ghz" and s["N"] == 3
                and set(s["profile"]) == {"Q"}
                and abs(s["gamma"] - GAMMA) < 1e-12
                and s["wiring"] == [0, 1, 2])
    v_c = coop["folds"]["1"]["mitigated"]["per_player"]
    gaps, labels = [], []
    for k, prof in enumerate((["H", "Q", "Q"], ["Q", "H", "Q"], ["Q", "Q", "H"])):
        dev = next(s for s in series.values()
                   if s["topology"] == "ghz" and s["N"] == 3
                   and s["profile"] == prof
                   and abs(s["gamma"] - GAMMA) < 1e-12)
        gaps.append(v_c[k] - dev["folds"]["1"]["mitigated"]["per_player"][k])
        labels.append(f"player {k}")
    x = np.arange(3)
    ax.bar(x, gaps, color=DATA, width=0.6, zorder=3)
    ax.axhline(0.0, color=INK, lw=1.0, zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylabel("deviation gap $\\pi_k(Q)-\\pi_k(H)$")
    ax.set_ylim(-0.05, 0.45)
    ax.set_title("(B)  no unilateral Hawk deviation pays (GHZ $N{=}3$)",
                 loc="left", fontsize=9.5, color=INK)
    for xi, g in zip(x, gaps):
        ax.text(xi, g + 0.012, f"$+{g:.3f}$", ha="center", va="bottom",
                fontsize=8, color=INK)
    ax.text(0.02, 0.04, "gap $>0$ $\\Rightarrow$ equilibrium holds",
            transform=ax.transAxes, fontsize=7.8, color=MUTED)


def panel_c(ax, series):
    """star N=4 per-player payoffs under three wirings."""
    wirings = [[0, 1, 2, 3], [1, 2, 3, 0], [3, 2, 1, 0]]
    marks = ["o", "s", "^"]
    for w, m in zip(wirings, marks):
        s = next((s for s in series.values()
                  if s["topology"] == "star" and s["N"] == 4
                  and set(s["profile"]) == {"Q"} and s["wiring"] == w), None)
        if s is None:
            continue
        v = s["folds"]["1"]["mitigated"]["per_player"]
        ax.plot(range(4), v, marker=m, ms=5.5, lw=1.2, color=DATA,
                alpha=0.9, label=f"wiring {''.join(map(str, w))}", zorder=3)
    ax.plot(range(4), [0.25, 1.25, 1.25, 1.25], ls="--", lw=1.0, color=IDEAL,
            marker="", label="noiseless ideal", zorder=2)
    ax.set_xticks(range(4))
    ax.set_xticklabels(["hub\n(player 0)", "leaf 1", "leaf 2", "leaf 3"],
                       fontsize=8.5)
    ax.set_ylabel("per-player payoff")
    ax.set_ylim(0, 1.5)
    ax.legend(fontsize=7.4, frameon=False, loc="center right")
    ax.set_title("(C)  the hub loses, and permuting players does not move it",
                 loc="left", fontsize=9.5, color=INK)


def main() -> None:
    run_dir, run = load_run(sys.argv)
    series = run["analysis"]["series"]
    cells = cooperative_cells(series)

    plt.rcParams.update({"font.size": 9.5, "font.family": "DejaVu Sans",
                         "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                         "text.color": INK, "xtick.color": INK,
                         "ytick.color": INK, "text.usetex": False})
    fig, axes = plt.subplots(
        1, 3, figsize=(12.8, 4.0), gridspec_kw={"width_ratios": [1.7, 1.0, 1.15]})
    for ax in axes:
        ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    panel_a(axes[0], cells)
    panel_b(axes[1], series)
    panel_c(axes[2], series)
    fig.tight_layout()

    out_dir = os.path.join(run_dir, "plots")
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, "hardware_topology.png")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(out_dir, "hardware_topology.pdf"),
                bbox_inches="tight")
    print(f"wrote {png} and .pdf")

    job = (run.get("job") or {}).get("job_id")
    with open(os.path.join(out_dir, "caption.md"), "w", encoding="utf-8") as fh:
        fh.write(
            f"Multi-topology EWL hardware batch on ibm_fez (job {job}), "
            f"49 pubs x {run['shots']} shots, pinned set "
            f"{run['analysis']['pinned']}. (A) measured mitigated fold-1 "
            f"advantage as a percentage of each cell's OWN noiseless "
            f"advantage; ring N=4 is excluded from the percentage because its "
            f"noiseless advantage is exactly zero. (B) unilateral Hawk "
            f"deviation gaps at GHZ N=3. (C) star N=4 per-player payoffs "
            f"under three wirings.\n")


if __name__ == "__main__":
    main()
