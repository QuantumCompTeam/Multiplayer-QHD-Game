"""Plot the N=3 GHZ EWL hardware-validation result as a paper-ready figure.

Reads a results/hardware-n3/<ts>/result.json (from
experiments/hardware_n3_ghz.py --hardware or experiments/fetch_result.py) and,
if present, calibration.json alongside it, then writes a two-panel figure and a
ready-to-paste caption under plots/:

  (A) measured probability over the 8 computational-basis outcomes (measured vs
      noiseless ideal, grouped bars) with binomial shot-noise error bars;
  (B) measured per-player payoff against the classical-Nash and quantum-ideal
      reference lines, error bars propagating shot noise through the payoff.

Usage:
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/plot_hardware_result.py \
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
from game.payoffs import index_to_bitstring, expected_payoff  # noqa: E402

# one data hue + neutral ink/reference (measured=blue, ideal/reference=grey;
# identity carried by legend + labels, so CVD-safe by construction).
DATA = "#1f6feb"
IDEAL = "#b6bcc4"
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
    cal_path = os.path.join(os.path.dirname(path), "calibration.json")
    cal = json.load(open(cal_path, encoding="utf-8")) if os.path.exists(cal_path) else None
    return d, N, shots, probs, cal


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK, length=3)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)


def payoff_coeffs(N):
    """Per-outcome, per-player payoff C[i, j]: player j's payoff in basis state i.
    Recovered by evaluating expected_payoff on one-hot distributions."""
    C = np.zeros((2 ** N, N))
    for i in range(2 ** N):
        onehot = np.zeros(2 ** N)
        onehot[i] = 1.0
        C[i] = expected_payoff(onehot, N)
    return C


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/plot_hardware_result.py <result.json>")
        sys.exit(2)
    path = sys.argv[1]
    d, N, shots, probs, cal = load(path)

    payoff = np.array(d["measured_per_player_payoff"])
    classical = d["classical_ne_payoff"]
    ideal_payoff = 4.0 / N
    adv = d["measured_advantage"]
    ideal_adv = d["reference_advantage"]
    backend = d.get("backend", "hardware")

    # --- uncertainties (multinomial / binomial shot noise, M = shots) ---
    prob_err = np.sqrt(probs * (1.0 - probs) / shots)         # per basis state
    C = payoff_coeffs(N)                                       # (2^N, N)
    var_payoff = (C ** 2 * probs[:, None]).sum(0) - payoff ** 2
    payoff_err = np.sqrt(np.clip(var_payoff, 0, None) / shots)  # per player

    ideal_probs = np.zeros(2 ** N)
    ideal_probs[0] = 1.0                                       # (Q,Q,Q) -> |0..0>

    plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                         "text.color": INK, "axes.labelcolor": INK,
                         "xtick.color": INK, "ytick.color": INK})
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.6, 4.4),
                                   gridspec_kw={"width_ratios": [1.45, 1]})

    # ---- Panel A: measured vs ideal distribution, grouped bars ----
    x = np.arange(2 ** N)
    w = 0.4
    axA.bar(x - w / 2, ideal_probs, width=w, color=IDEAL, label="ideal (Q,Q,Q)",
            zorder=2)
    axA.bar(x + w / 2, probs, width=w, color=DATA, label="measured", zorder=3)
    axA.errorbar(x + w / 2, probs, yerr=prob_err, fmt="none", ecolor=INK,
                 elinewidth=0.9, capsize=2, zorder=4)
    style_axis(axA)
    axA.set_xticks(x)
    axA.set_xticklabels([f"|{index_to_bitstring(i, N)}⟩" for i in x], fontsize=8.5)
    axA.set_ylim(0, 1.08)
    axA.set_ylabel("probability")
    axA.set_title("(A)  Output distribution: measured vs ideal", fontsize=10.5,
                  loc="left", pad=8)
    for i, p in enumerate(probs):
        if p >= 0.02:
            axA.text(i + w / 2, p + prob_err[i] + 0.02, f"{p:.3f}", ha="center",
                     va="bottom", fontsize=8.3, color=INK)
    axA.legend(frameon=False, fontsize=8.5, loc="upper center")

    # ---- Panel B: per-player payoff vs reference lines, with error bars ----
    px = np.arange(N)
    axB.bar(px, payoff, width=0.55, color=DATA, zorder=3)
    axB.errorbar(px, payoff, yerr=payoff_err, fmt="none", ecolor=INK,
                 elinewidth=0.9, capsize=3, zorder=4)
    style_axis(axB)
    axB.axhline(ideal_payoff, color=MUTED, linestyle=(0, (2, 2)), linewidth=1.2)
    axB.axhline(classical, color=MUTED, linestyle=(0, (2, 2)), linewidth=1.2)
    axB.set_xticks(px)
    axB.set_xticklabels([f"P{j+1}" for j in range(N)])
    axB.set_xlim(-0.6, N - 1 + 1.45)
    axB.set_ylim(0, ideal_payoff * 1.2)
    axB.set_ylabel("per-player payoff")
    axB.set_title("(B)  Per-player payoff & advantage", fontsize=10.5,
                  loc="left", pad=8)
    for j, v in enumerate(payoff):
        axB.text(j, v + payoff_err[j] + 0.02, f"{v:.3f}", ha="center",
                 va="bottom", fontsize=8.3, color=INK)
    lx = N - 1 + 0.6
    axB.text(lx, ideal_payoff, f"quantum ideal\nV/N = {ideal_payoff:.3f}",
             ha="left", va="center", fontsize=8, color=MUTED)
    axB.text(lx, classical, f"classical Nash\n= {classical:.3f} (analytic)",
             ha="left", va="center", fontsize=8, color=MUTED)

    fig.suptitle(
        f"N=3 GHZ EWL quantum-advantage validation on {backend} ({shots} shots)\n"
        f"measured advantage = {adv:.4f}   (ideal {ideal_adv:.1f}; "
        f"gap {ideal_adv - adv:.4f} = device noise)",
        fontsize=11, y=1.03)

    out_dir = os.path.join(os.path.dirname(path), "plots")
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, "hardware_n3_validation.png")
    pdf = os.path.join(out_dir, "hardware_n3_validation.pdf")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    print("wrote:", os.path.relpath(png))
    print("wrote:", os.path.relpath(pdf))

    # ---- auto-generated caption (with calibration, if available) ----
    cap = (
        f"**Figure — Hardware validation of the N=3 GHZ EWL quantum advantage on "
        f"{backend} (IBM Heron r2).** The validated (Q,Q,Q) circuit — entangler J "
        f"decomposed to 6 native cz gates — was executed with {shots} shots. "
        f"**(A)** Measured output distribution over the eight computational-basis "
        f"states (blue) versus the noiseless ideal (grey); error bars are binomial "
        f"shot noise. {int(round(probs[0]*shots))}/{shots} shots "
        f"({probs[0]*100:.1f}%) fall in |0…0⟩, the ideal (Q,Q,Q) output. "
        f"**(B)** Measured per-player payoff (blue) against the analytic "
        f"classical-Nash baseline ({classical:.3f}, noiseless) and the quantum "
        f"ideal V/N = {ideal_payoff:.3f}; error bars propagate shot noise. The "
        f"measured mean payoff {float(np.mean(payoff)):.3f} gives advantage "
        f"{adv:.4f} vs the ideal {ideal_adv:.1f}. Note the advantage compares a "
        f"measured quantum payoff against the analytic (noiseless) classical Nash "
        f"equilibrium."
    )
    if cal:
        q = cal["physical_qubits_logical_order"]
        ro = cal["readout_error"]; t1 = cal["t1_us"]; t2 = cal["t2_us"]
        cz = cal.get("twoq_gate_error", {})
        cz_str = ", ".join(f"{k.replace('_','–')}: {v*100:.2f}%" for k, v in cz.items())
        cap += (
            f" Physical qubits {{{q[0]}, {q[1]}, {q[2]}}} (calibration "
            f"{cal['calibration_last_update'][:10]}): readout error "
            f"{min(ro.values())*100:.2f}–{max(ro.values())*100:.2f}%, "
            f"cz gate error {cz_str}, "
            f"T1 {min(t1.values()):.0f}–{max(t1.values()):.0f} µs, "
            f"T2 {min(t2.values()):.0f}–{max(t2.values()):.0f} µs."
        )
    cap_path = os.path.join(out_dir, "caption.md")
    open(cap_path, "w", encoding="utf-8").write(cap + "\n")
    print("wrote:", os.path.relpath(cap_path))


if __name__ == "__main__":
    main()
