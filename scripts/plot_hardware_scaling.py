"""Paper figure for the N=3,4,5 hardware scaling runs (+ caption).

Aggregates results/hardware-scaling/<ts>/result.json runs and writes
plots/hardware_scaling.{png,pdf} + caption.md into the NEWEST included run dir.

Sample selection (see load_runs): only runs whose series are exactly the
registered {3,4,5} batch, and only those on ONE physical chain -- the same two
filters scripts/judge_repeat_run.py applies, so the figure and the judge never
disagree about what counts as a repeat. Every excluded run is printed.

Error bars are cross-CALIBRATION-EPOCH, not cross-run: runs sharing a
calibration stamp are averaged into one point first, because two executions
under one calibration are one sample. With a single epoch the bars fall back to
within-run sigma and the caption says so explicitly.

  (A) advantage vs N: measured raw + ZNE with error bars, against the noiseless
      ideal, the device-noise-model prediction, and the effective-p curve
      (fitted at N=3 only -- fit-one-predict-two).
  (B) ZNE mechanics: readout-mitigated payoff vs cz-fold factor per N, with the
      weighted linear fit extrapolated to fold 0.
  (C) ground-state probability P(|0..0>) vs N, measured vs device model -- the
      fidelity decays ~3x faster than the advantage (the mean-payoff observable
      is first-order insensitive to single bit-flips from |0..0>).

Usage:
  conda run -n entangled-equilibria python scripts/plot_hardware_scaling.py            # all runs
  conda run -n entangled-equilibria python scripts/plot_hardware_scaling.py <run_dir> [<run_dir>..]
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


REGISTERED_SERIES = {"3", "4", "5"}


def calibration_stamp(run_dir: str) -> str:
    """The calibration this run actually EXECUTED under.

    calibration_at_submit.json is the snapshot taken at submission (item 16) and
    is the correct stamp for cross-day counting. calibration.json is fetched at
    analysis time and is only a fallback for runs predating item 16 (G15).
    """
    for name in ("calibration_at_submit.json", "calibration.json"):
        path = os.path.join(run_dir, name)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return str(json.load(fh)["calibration_last_update"])
    return f"unknown ({os.path.basename(run_dir)})"


def load_runs(argv: list[str]) -> tuple[list[tuple[str, list[dict]]], list[dict], str]:
    """Registered-batch, chain-matched runs, grouped into calibration epochs.

    Applies two filters the earlier version did not, each of which silently
    corrupted the aggregate:

      1. **Registered batch only.** The N=3..7 extension also measures N=3,4,5,
         so it was being folded into this curve even though
         scripts/judge_repeat_run.py excludes it explicitly as "not the
         registered batch". The judge and this figure now agree on the sample.
      2. **One physical chain only.** hardware_scaling.find_chain selects from
         live calibration, so the runs have drifted across chains
         ([59,75,74,73,79] and [20,21,22,23,24]). Averaging across them mixes
         calibration drift with a change of qubits -- the confound that
         invalidated topology T4. The chain of the newest qualifying run wins.

    Runs are then grouped by calibration stamp, because runs sharing a stamp are
    ONE epoch, not two independent samples: runs 1 and 2 differ by 18 hours yet
    carry the same stamp, so treating them as two points would understate the
    error bar. Every exclusion is printed -- a silently narrowed sample reads as
    "everything was included" when it was not.

    Explicit run dirs on the command line bypass both filters deliberately.
    """
    explicit = len(argv) > 1
    if explicit:
        dirs = list(argv[1:])
    else:
        dirs = sorted(glob.glob(os.path.join("results", "hardware-scaling", "*")))
        dirs = [d for d in dirs if os.path.exists(os.path.join(d, "result.json"))]
    if not dirs:
        print("no hardware-scaling runs found")
        sys.exit(2)

    loaded = []
    for d in dirs:
        with open(os.path.join(d, "result.json"), encoding="utf-8") as fh:
            loaded.append((d, json.load(fh)))

    if not explicit:
        kept = []
        for d, r in loaded:
            series = set(r["analysis"]["series"])
            if series != REGISTERED_SERIES:
                print(f"  excluded {os.path.basename(d)}: series "
                      f"{sorted(series)} != registered {sorted(REGISTERED_SERIES)}")
                continue
            kept.append((d, r))
        if not kept:
            print("no runs match the registered N=3,4,5 batch")
            sys.exit(2)
        target_chain = kept[-1][1]["analysis"]["chain"]
        loaded = []
        for d, r in kept:
            if r["analysis"]["chain"] != target_chain:
                print(f"  excluded {os.path.basename(d)}: chain "
                      f"{r['analysis']['chain']} != {target_chain} "
                      f"(not chain-matched; would confound qubit change with "
                      f"calibration drift)")
                continue
            loaded.append((d, r))

    by_stamp: dict[str, list[dict]] = {}
    for d, r in loaded:
        by_stamp.setdefault(calibration_stamp(d), []).append(r)
    grouped = sorted(by_stamp.items())
    print(f"  aggregating {len(loaded)} run(s) in {len(grouped)} calibration "
          f"epoch(s):")
    for stamp, rs in grouped:
        print(f"    {stamp}: {len(rs)} run(s)")
    return grouped, [r for _, r in loaded], loaded[-1][0]


def agg(epochs: list[tuple[str, list[dict]]], path_fn) -> tuple[float, float]:
    """Mean and error over calibration EPOCHS of a per-run scalar.

    Runs within an epoch are averaged first, so an epoch contributes one point
    however many times it was executed. The error is then the sample std across
    epochs -- a genuine cross-calibration estimate.

    With a single epoch there is no cross-epoch spread to measure, so the error
    falls back to the mean of the runs' own reported within-run sigmas. That is a
    different quantity and the caption says so rather than passing it off as a
    cross-day bar.
    """
    per_epoch, sigs = [], []
    for _, runs in epochs:
        vals = []
        for r in runs:
            v, s = path_fn(r)
            vals.append(v)
            sigs.append(s)
        per_epoch.append(float(np.mean(vals)))
    if len(per_epoch) == 1:
        return per_epoch[0], float(np.mean(sigs))
    return float(np.mean(per_epoch)), float(np.std(per_epoch, ddof=1))


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK, length=3)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)


def main() -> None:
    epochs, runs, latest_dir = load_runs(sys.argv)
    n_runs = len(runs)
    n_epochs = len(epochs)
    # The model curves (device model, p_eff) are the REGISTRATION ANCHOR's, not
    # an average: p_eff is refit per run and the registered value belongs to the
    # oldest run. Averaging them would silently move the registered number the
    # paper quotes.
    first = runs[0]
    chain = first["analysis"]["chain"]
    backend = first["job"]["backend"]
    shots = first["shots"]

    # --- aggregate measured quantities across runs -----------------------------
    raw_adv, raw_err, zne_adv, zne_err, pg_meas, pg_err = {}, {}, {}, {}, {}, {}
    for N in NS:
        k = str(N)
        raw_adv[N], raw_err[N] = agg(epochs, lambda r: (
            r["analysis"]["series"][k]["folds"]["1"]["raw"]["advantage"],
            r["analysis"]["series"][k]["folds"]["1"]["raw"]["sigma"]))
        zne_adv[N], zne_err[N] = agg(epochs, lambda r: (
            r["analysis"]["series"][k]["zne"]["advantage"],
            r["analysis"]["series"][k]["zne"]["linear_stderr"]))
        pg_meas[N], pg_err[N] = agg(epochs, lambda r: (
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
    # retention labels: the ideal itself falls as 3/N (game theory, not noise);
    # annotate measured/ideal so the staircase is never misread as decay
    for N in NS:
        ret = 100.0 * zne_adv[N] / ideal[N]
        axA.annotate(f"{ret:.1f}%\nof ideal", (N, zne_adv[N]),
                     textcoords="offset points", xytext=(10, -22),
                     fontsize=7.8, color=INK, ha="left")
    axA.text(3.02, 0.63, "ideal advantage = 3/N — the ceiling\nitself falls "
             "with N (game theory, not noise)", fontsize=7.8, color=MUTED)
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

    run_note = (f"{n_runs} run" + ("s" if n_runs > 1 else "")
                + f" in {n_epochs} calibration epoch"
                + ("s" if n_epochs > 1 else ""))
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
    epoch_list = "; ".join(f"{stamp} ({len(rs)} run{'s' if len(rs) > 1 else ''})"
                           for stamp, rs in epochs)
    cap = (
        f"**Figure — Scaling of the N-player GHZ EWL quantum advantage on "
        f"{backend} (IBM Heron r2), physical chain {chain} on every included "
        f"run, {shots} shots, {run_note}.** "
        f"Calibration epochs: {epoch_list}. "
        f"**(A)** Measured cooperative-profile advantage (mean (Q,…,Q) payoff "
        f"minus the analytic noiseless classical-Nash payoff 1/3, 1/4, 1/5) at "
        f"N = 3, 4, 5: raw (open) and readout-mitigated + ZNE (filled), against "
        f"the noiseless ideal (1.0, 0.75, 0.6), the device noise-model "
        f"prediction (diamonds; qiskit-aer NoiseModel.from_backend reduced to "
        f"the executed qubits), and a single-parameter depolarizing model with "
        f"p_eff = {ep['p_eff']:.4f} fitted to the N=3 point alone — its N=4,5 "
        f"values are predictions, not fits. The ideal, device-model and "
        f"depolarizing curves are the registration anchor's "
        f"({first['job']['job_id']}), not run averages, so the registered "
        f"p_eff is quoted unchanged. Error bars: "
        + (f"sample standard deviation across the {n_epochs} distinct "
           f"calibration epochs, with runs sharing a calibration stamp averaged "
           f"into one point first (two executions under one calibration are one "
           f"sample, not two); this is a cross-calibration estimate and excludes "
           f"within-run multinomial and weighted-fit error"
           if n_epochs > 1 else
           "multinomial shot noise (raw) and weighted-fit standard error (ZNE). "
           "Only ONE calibration epoch is represented, so these are within-run "
           "uncertainties and NOT a cross-calibration estimate") + ". "
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
        # Name every job. The previous version printed only the anchor's id next
        # to the NEWEST run's calibration figures, which read as though one job
        # produced both.
        jobs = ", ".join(r["job"]["job_id"] for r in runs)
        cap += (
            f" Newest included run's calibration "
            f"{cal['calibration_last_update'][:10]}: readout "
            f"{min(ro.values())*100:.2f}–{max(ro.values())*100:.2f}%, cz "
            f"{min(cz.values())*100:.2f}–{max(cz.values())*100:.2f}% on the "
            f"chain. Jobs aggregated: {jobs}."
        )
    cap_path = os.path.join(out_dir, "caption.md")
    open(cap_path, "w", encoding="utf-8").write(cap + "\n")
    print("wrote:", cap_path)


if __name__ == "__main__":
    main()
