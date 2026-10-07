"""Regenerate the phase-branch / payoff-sensitivity / compact-evaluation figure.

Plot-only: reads the saved analysis in
  results/journal-strengthening/2026-09-07-offline/results.json
(produced by scripts/journal_analysis.py) and writes
paper/figs/journal_extensions.pdf. Nothing is recomputed, so the recorded
CPU timings are reproduced exactly.

Usage: python scripts/plot_phase_sensitivity.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results" / "journal-strengthening" / "2026-09-07-offline" / "results.json"
EXTENSION_RUN = "2026-07-25T180549Z"  # the N=3..7 hardware run
OUT = ROOT / "paper" / "figs" / "journal_extensions.pdf"


def main() -> None:
    plt.rcParams.update({
        "font.size": 8, "axes.labelsize": 8, "legend.fontsize": 7,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42,
    })
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.3), layout="constrained")

    small = [r for r in data["phases"] if r["N"] <= 7]
    ns = [r["N"] for r in small]
    ax = axes[0]
    ax.plot(ns, [r["original"]["restricted_margin"] for r in small], "o-",
            color="#1f4e79", ms=4, label=r"original $Q_N$")
    ax.plot(ns, [r["candidate"]["restricted_margin"] for r in small], "s--",
            color="#c62828", ms=4, label=r"alternative $Q_N^\star$")
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks(ns)
    ax.set(xlabel="number of players $N$", ylabel="minimum Hawk/Dove gap")
    ax.legend(frameon=False, loc="lower left")
    ax.set_title("(a)", loc="left", fontsize=8)

    ax = axes[1]
    rows = [r for r in data["sensitivity"] if EXTENSION_RUN in r["source"]]
    styles = {0.0: ("#1f4e79", "o"), 1.0: ("#2e7d32", "s")}
    for ell, (colour, marker) in styles.items():
        sel = sorted((r for r in rows if r["ell"] == ell), key=lambda r: r["N"])
        x = [r["N"] for r in sel]
        ax.errorbar(x, [r["retention"] for r in sel],
                    yerr=[1.96 * r["mean_se"] * r["N"] / 3 for r in sel],
                    fmt=marker + "-", color=colour, ms=4, capsize=2,
                    label=rf"measured, $\ell={ell:g}$")
        ax.plot(x, [r["uniform_retention"] for r in sel], ls=":", color=colour,
                label=rf"uniform random, $\ell={ell:g}$")
    ax.set_xticks(range(3, 8))
    ax.set(xlabel="number of players $N$", ylabel="analytic-baseline retention")
    ax.set_ylim(0.72, 1.01)
    ax.legend(frameon=False, loc="center right", bbox_to_anchor=(1.0, 0.42),
              ncol=1, fontsize=6.5)
    ax.set_title("(b)", loc="left", fontsize=8)

    ax = axes[2]
    bench = data["benchmarks"]
    ax.loglog([r["N"] for r in bench], [r["seconds_with_tracemalloc"] for r in bench],
              "o-", color="#1f4e79", ms=4)
    ax.set(xlabel="number of players $N$", ylabel="CPU time per evaluation (s)")
    ax.set_title("(c)", loc="left", fontsize=8)

    fig.savefig(OUT)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
