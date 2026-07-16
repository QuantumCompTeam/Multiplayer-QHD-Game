"""Plot the N=3 GHZ EWL hardware-validation result as a paper-ready figure.

Reads a results/hardware-n3/<ts>/result.json (produced by
experiments/hardware_n3_ghz.py --hardware or experiments/fetch_result.py) and
writes a two-panel figure next to it under plots/:

  (A) measured probability over the 8 computational-basis outcomes, with the
      ideal (Q,Q,Q) target |000> = 1 shown as a reference outline;
  (B) measured per-player payoff against the classical-Nash and quantum-ideal
      reference lines -- the gap above classical Nash is the quantum advantage.

Usage:
  PYTHONPATH=src python scripts/plot_hardware_result.py \
      results/hardware-n3/2026-07-16T013912Z/result.json
"""

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from game.payoffs import index_to_bitstring  # noqa: E402

# --- palette: one data hue + neutral ink/reference (single series -> no legend,
# CVD-safe by construction; references are gray, identity carried by labels). ---
DATA = "#1f6feb"      # measured (accessible blue)
DATA_SOFT = "#9ec3fb"
INK = "#1b1f24"
MUTED = "#8b949e"
GRID = "#e6e8eb"


def load(path):
    d = json.load(open(path, encoding="utf-8"))
    counts = d["counts"]
    shots = sum(counts.values())
    N = int(d["N"])
    probs = np.zeros(2 ** N)
    for b, c in counts.items():
        probs[int(b, 2)] = c / shots
    return d, N, shots, probs


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK, length=3)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/plot_hardware_result.py <result.json>")
        sys.exit(2)
    path = sys.argv[1]
    d, N, shots, probs = load(path)

    payoff = np.array(d["measured_per_player_payoff"])
    mean_payoff = d["measured_q_payoff"]
    classical = d["classical_ne_payoff"]
    ideal_payoff = 4.0 / N            # V/N, the (Q,..,Q) ideal
    adv = d["measured_advantage"]
    ideal_adv = d["reference_advantage"]
    backend = d.get("backend", "hardware")

    plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                         "axes.edgecolor": MUTED, "text.color": INK,
                         "axes.labelcolor": INK, "xtick.color": INK,
                         "ytick.color": INK})
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.2, 4.2),
                                   gridspec_kw={"width_ratios": [1.35, 1]})

    # ---- Panel A: measured probability distribution over basis states ----
    labels = [f"|{index_to_bitstring(i, N)}⟩" for i in range(2 ** N)]
    x = np.arange(2 ** N)
    # ideal target: |000> should be 1.0 -- hollow reference behind the bars
    axA.bar(0, 1.0, width=0.62, facecolor="none", edgecolor=MUTED,
            linewidth=1.1, linestyle=(0, (4, 3)), zorder=2)
    bars = axA.bar(x, probs, width=0.62, color=DATA, zorder=3)
    style_axis(axA)
    axA.set_xticks(x)
    axA.set_xticklabels(labels, rotation=0, fontsize=8.5)
    axA.set_ylim(0, 1.06)
    axA.set_ylabel("measured probability")
    axA.set_title("(A)  Measured (Q,Q,Q) output distribution", fontsize=10.5,
                  loc="left", color=INK, pad=8)
    # direct-label the meaningful bars only
    for i, p in enumerate(probs):
        if p >= 0.02:
            axA.text(i, p + 0.02, f"{p:.3f}", ha="center", va="bottom",
                     fontsize=8.5, color=INK)
    axA.text(0.34, 0.9, "dashed = ideal target\n|000⟩ = 1", transform=axA.transAxes,
             fontsize=8.5, color=MUTED, va="top")

    # ---- Panel B: per-player payoff vs reference lines ----
    px = np.arange(N)
    axB.bar(px, payoff, width=0.55, color=DATA, zorder=3)
    style_axis(axB)
    axB.axhline(ideal_payoff, color=MUTED, linestyle=(0, (2, 2)), linewidth=1.2,
                zorder=2)
    axB.axhline(classical, color=MUTED, linestyle=(0, (2, 2)), linewidth=1.2,
                zorder=2)
    axB.set_xticks(px)
    axB.set_xticklabels([f"P{j+1}" for j in range(N)])
    # right margin holds the reference-line labels so they never touch the bars
    axB.set_xlim(-0.6, N - 1 + 1.35)
    axB.set_ylim(0, ideal_payoff * 1.18)
    axB.set_ylabel("per-player payoff")
    axB.set_title("(B)  Per-player payoff & quantum advantage", fontsize=10.5,
                  loc="left", color=INK, pad=8)
    for j, v in enumerate(payoff):
        axB.text(j, v + 0.015, f"{v:.3f}", ha="center", va="bottom",
                 fontsize=8.5, color=INK)
    label_x = N - 1 + 0.55
    axB.text(label_x, ideal_payoff, f"quantum ideal\nV/N = {ideal_payoff:.3f}",
             ha="left", va="center", fontsize=8, color=MUTED)
    axB.text(label_x, classical, f"classical Nash\n= {classical:.3f}",
             ha="left", va="center", fontsize=8, color=MUTED)

    fig.suptitle(
        f"N=3 GHZ EWL quantum-advantage validation on {backend} "
        f"({shots} shots)\n"
        f"measured advantage = {adv:.4f}   (ideal {ideal_adv:.1f}; "
        f"gap {ideal_adv - adv:.4f} = device noise)",
        fontsize=11, y=1.02, color=INK)

    out_dir = os.path.join(os.path.dirname(path), "plots")
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, "hardware_n3_validation.png")
    pdf = os.path.join(out_dir, "hardware_n3_validation.pdf")
    fig.savefig(png, dpi=220, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")  # vector, for the paper
    print("wrote:", os.path.relpath(png))
    print("wrote:", os.path.relpath(pdf))


if __name__ == "__main__":
    main()
