"""Paper figure for the N=3,4,5 hardware scaling runs (+ caption).

Aggregates one or more results/hardware-scaling/<ts>/result.json runs (mean
across runs, std as error when >1 run; shot-noise/fit errors when a single
run) and writes plots/hardware_scaling.{png,pdf} + caption.md into the NEWEST
run dir.

  (A) advantage vs N: measured raw + ZNE with error bars, against the noiseless
      ideal, the device-noise-model prediction, and the effective-p curve
      (fitted at N=3 only -- fit-one-predict-two).
  (B) ZNE mechanics: readout-mitigated payoff vs cz-fold factor per N, with the
      weighted linear fit extrapolated to fold 0.
  (C) ground-state probability P(|0..0>) vs N, measured vs device model -- the
      fidelity decays ~3x faster than the advantage (the mean-payoff observable
      is first-order insensitive to single bit-flips from |0..0>).

Usage:
  PYTHONPATH=src python scripts/plot_hardware_scaling.py            # all runs
  PYTHONPATH=src python scripts/plot_hardware_scaling.py <run_dir> [<run_dir>..]
"""

import glob
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = (3, 4, 5)
DATA = "#1f6feb"      # measured (single data hue)
BLUE_RAMP = ["#9ec3fb", "#5a94f0", "#1f6feb"]  # sequential by N (panel B)
INK = "#1b1f24"
MUTED = "#8b949e"
GRID = "#e6e8eb"


def load_runs(argv: list[str]) -> tuple[list[dict], str]:
    if len(argv) > 1:
        dirs = argv[1:]
    else:
        dirs = sorted(glob.glob(os.path.join("results", "hardware-scaling", "*")))
        dirs = [d for d in dirs if os.path.exists(os.path.join(d, "result.json"))]
    if not dirs:
        print("no hardware-scaling runs found")
        sys.exit(2)
    runs = [json.load(open(os.path.join(d, "result.json"), encoding="utf-8"))
            for d in dirs]
    return runs, dirs[-1]


def agg(runs: list[dict], path_fn) -> tuple[np.ndarray, np.ndarray]:
    """Mean and error across runs of a per-run scalar (path_fn(run) -> float).

    Single run: error = the run's own reported sigma (path_fn returns
    (value, sigma)); multiple runs: mean +/- std across runs.
    """
    vals, sigs = [], []
    for r in runs:
        v, s = path_fn(r)
        vals.append(v)
        sigs.append(s)
    vals = np.asarray(vals)
    if len(runs) == 1:
        return vals[0], sigs[0]
    return float(vals.mean()), float(vals.std(ddof=1))


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK, length=3)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)


def main() -> None:
    runs, latest_dir = load_runs(sys.argv)
    n_runs = len(runs)
    first = runs[0]
    chain = first["analysis"]["chain"]
    backend = first["job"]["backend"]
    shots = first["shots"]

    # --- aggregate measured quantities across runs -----------------------------
    raw_adv, raw_err, zne_adv, zne_err, pg_meas, pg_err = {}, {}, {}, {}, {}, {}
    for N in NS:
        k = str(N)
        raw_adv[N], raw_err[N] = agg(runs, lambda r: (
            r["analysis"]["series"][k]["folds"]["1"]["raw"]["advantage"],
            r["analysis"]["series"][k]["folds"]["1"]["raw"]["sigma"]))
        zne_adv[N], zne_err[N] = agg(runs, lambda r: (
            r["analysis"]["series"][k]["zne"]["advantage"],
            r["analysis"]["series"][k]["zne"]["linear_stderr"]))
        pg_meas[N], pg_err[N] = agg(runs, lambda r: (
            r["analysis"]["series"][k]["folds"]["1"]["raw"]["p_ground"],
            np.sqrt(r["analysis"]["series"][k]["folds"]["1"]["raw"]["p_ground"]
                    * (1 - r["analysis"]["series"][k]["folds"]["1"]["raw"]["p_ground"])
                    / r["shots"])))

    ideal = {N: first["analysis"]["series"][str(N)]["ideal_advantage"] for N in NS}
    dm = first["predictions"]["device_model"]
    dm_adv = {N: dm[str(N)]["raw"]["advantage"] for N in NS}
    dm_pg = {N: dm[str(N)]["raw"]["p_ground"] for N in NS}
    ep = first["predictions"]["effective_p"]
    ep_adv = {N: ep[str(N)]["advantage"] for N in NS}

    plt.rcParams.update({"font.size": 9.5, "font.family": "DejaVu Sans",
                         "text.color": INK, "axes.labelcolor": INK,
                         "xtick.color": INK, "ytick.color": INK})
    fig, (axA, axB, axC) = plt.subplots(
        1, 3, figsize=(12.8, 4.3), gridspec_kw={"width_ratios": [1.5, 1.05, 1.0]})

    # ---- (A) advantage vs N ----------------------------------------------------
    xs = np.array(NS, dtype=float)
    axA.plot(xs, [ideal[N] for N in NS], color=MUTED, ls=(0, (4, 3)), lw=1.3,
             marker="o", mfc="white", mec=MUTED, ms=6, zorder=2,
             label="noiseless ideal")
    axA.plot(xs, [ep_adv[N] for N in NS], color=MUTED, ls=(0, (1, 2)), lw=1.6,
             marker="s", mfc="white", mec=MUTED, ms=6, zorder=2,
             label=f"depolarizing p_eff={ep['p_eff']:.4f} (fit at N=3 only)")
    axA.plot(xs, [dm_adv[N] for N in NS], color=INK, ls="none",
             marker="D", mfc="white", mec=INK, ms=6, zorder=3,
             label="device noise model")
    axA.errorbar(xs - 0.04, [raw_adv[N] for N in NS],
                 yerr=[raw_err[N] for N in NS], color=DATA, ls="none",
                 marker="o", mfc="white", mec=DATA, ms=7, capsize=3, lw=1.2,
                 zorder=4, label="measured (raw)")
    axA.errorbar(xs + 0.04, [zne_adv[N] for N in NS],
                 yerr=[zne_err[N] for N in NS], color=DATA, ls="none",
                 marker="o", ms=7, capsize=3, lw=1.2, zorder=5,
                 label="measured (readout-mitigated + ZNE)")
    style_axis(axA)
    axA.set_xticks(list(NS))
    axA.set_xlabel("players N")
    axA.set_ylabel("advantage  (payoff − classical NE)")
    axA.set_title("(A)  Quantum advantage vs N on real hardware", loc="left",
                  fontsize=10.5, pad=8)
    axA.set_ylim(0.5, 1.06)
    axA.legend(frameon=False, fontsize=7.8, loc="upper right")

    # ---- (B) ZNE mechanics: payoff vs fold factor ------------------------------
    for i, N in enumerate(NS):
        s = first["analysis"]["series"][str(N)]
        folds = [1, 3, 5]
        pays = [s["folds"][str(f)]["mitigated"]["mean"] for f in folds]
        sigs = [s["folds"][str(f)]["mitigated"]["sigma"] for f in folds]
        c = BLUE_RAMP[i]
        axB.errorbar(folds, pays, yerr=sigs, color=c, ls="none", marker="o",
                     ms=5.5, capsize=2.5, lw=1.1, zorder=4)
        lam = np.linspace(0, 5.4, 10)
        z = s["zne"]
        axB.plot(lam, z["linear"] + z["linear_slope"] * lam, color=c, lw=1.1,
                 zorder=3)
        axB.plot([0], [z["linear"]], marker="*", ms=11, color=c, zorder=5)
        axB.text(5.45, pays[-1], f" N={N}", color=c, fontsize=8.5, va="center")
    style_axis(axB)
    axB.set_xticks([0, 1, 3, 5])
    axB.set_xlim(-0.35, 6.3)
    axB.set_xlabel("cz fold factor  (★ = extrapolated to 0)")
    axB.set_ylabel("mean (Q,…,Q) payoff")
    axB.set_title("(B)  Zero-noise extrapolation", loc="left", fontsize=10.5,
                  pad=8)

    # ---- (C) ground-state probability vs N -------------------------------------
    axC.plot(xs, [dm_pg[N] for N in NS], color=INK, ls="none", marker="D",
             mfc="white", mec=INK, ms=6, zorder=3, label="device noise model")
    axC.errorbar(xs, [pg_meas[N] for N in NS], yerr=[pg_err[N] for N in NS],
                 color=DATA, ls="none", marker="o", ms=7, capsize=3, lw=1.2,
                 zorder=4, label="measured")
    axC.axhline(1.0, color=MUTED, ls=(0, (4, 3)), lw=1.1, zorder=2)
    axC.text(2.98, 1.005, "ideal = 1", color=MUTED, fontsize=8)
    style_axis(axC)
    axC.set_xticks(list(NS))
    axC.set_xlabel("players N")
    axC.set_ylabel(r"P($|0{\ldots}0\rangle$)")  # mathtext: DejaVu lacks U+27E9
    axC.set_title("(C)  Ground-state probability", loc="left", fontsize=10.5,
                  pad=8)
    axC.set_ylim(0.8, 1.03)
    axC.legend(frameon=False, fontsize=7.8, loc="lower left")

    run_note = f"{n_runs} run" + ("s" if n_runs > 1 else "")
    fig.suptitle(
        f"N-player GHZ EWL quantum advantage on {backend} — pinned chain "
        f"{chain}, {shots} shots, {run_note}",
        fontsize=11.5, y=1.02)
    fig.tight_layout()

    out_dir = os.path.join(latest_dir, "plots")
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, "hardware_scaling.png")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(out_dir, "hardware_scaling.pdf"), bbox_inches="tight")
    print("wrote:", png)

    # ---- caption ----------------------------------------------------------------
    cal_path = os.path.join(latest_dir, "calibration.json")
    cal = (json.load(open(cal_path, encoding="utf-8"))
           if os.path.exists(cal_path) else None)
    zne3 = first["analysis"]["series"]["3"]["zne"]
    cap = (
        f"**Figure — Scaling of the N-player GHZ EWL quantum advantage on "
        f"{backend} (IBM Heron r2), physical chain {chain}, {shots} shots"
        f"{', ' + run_note if n_runs > 1 else ''}.** "
        f"**(A)** Measured cooperative-profile advantage (mean (Q,…,Q) payoff "
        f"minus the analytic noiseless classical-Nash payoff 1/3, 1/4, 1/5) at "
        f"N = 3, 4, 5: raw (open) and readout-mitigated + ZNE (filled), against "
        f"the noiseless ideal (1.0, 0.75, 0.6), the device noise-model "
        f"prediction (diamonds; qiskit-aer NoiseModel.from_backend reduced to "
        f"the executed qubits), and a single-parameter depolarizing model with "
        f"p_eff = {ep['p_eff']:.4f} fitted to the N=3 point alone — its N=4,5 "
        f"values are predictions, not fits. Error bars: multinomial shot noise "
        f"(raw) and weighted-fit standard error (ZNE)"
        + (", std across runs when several runs are aggregated" if n_runs > 1
           else "") + ". "
        f"**(B)** ZNE mechanics: readout-mitigated payoff vs cz fold factor "
        f"(cz → cz^λ, λ = 1, 3, 5; cz is self-inverse so the unitary is "
        f"unchanged) with the weighted linear fit extrapolated to λ = 0 (stars). "
        f"**(C)** Ground-state probability P(|0…0⟩): the state fidelity decays "
        f"several times faster than the advantage because the mean-payoff "
        f"observable is first-order insensitive to single bit-flips from "
        f"|0…0⟩ (a one-Hawk outcome still has mean payoff V/N). "
        f"(Q,…,Q) is a pure Nash equilibrium only at N=3; at N=4,5 the profile "
        f"is the cooperative quantum profile, not an equilibrium (unilateral "
        f"Hawk deviation profits in the noiseless game)."
    )
    if cal:
        ro = cal["readout_error"]; cz = cal["cz_error"]
        cap += (
            f" Calibration {cal['calibration_last_update'][:10]}: readout "
            f"{min(ro.values())*100:.2f}–{max(ro.values())*100:.2f}%, cz "
            f"{min(cz.values())*100:.2f}–{max(cz.values())*100:.2f}% on the "
            f"chain; job {first['job']['job_id']}."
        )
    cap_path = os.path.join(out_dir, "caption.md")
    open(cap_path, "w", encoding="utf-8").write(cap + "\n")
    print("wrote:", cap_path)


if __name__ == "__main__":
    main()
