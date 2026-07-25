"""Freeze the topology batch's predictions BEFORE any hardware submission.

Writes results/hardware-topology/preregistration.json. This is the same moat
the scaling result already has (results/hardware-scaling/preregistration.json):
the file is committed before the job is submitted, so the commit timestamp is
the evidence that the predictions predate the data.

The predictions come from the mandatory dress rehearsal on
AerSimulator(NoiseModel.from_backend(ibm_fez)) reduced to the pinned set --
the same gated path experiments/hardware_topology.py --hardware runs, called
with a fixed seed and a high shot count so the registration carries no
meaningful Monte-Carlo error of its own.

Four registered tests, in decreasing order of robustness to device-model error:

  T1 equilibrium (item 2)   Every unilateral Hawk deviation gap at ghz N=3,
                            gamma=pi/2 is >= 0. SIGN test. This is the paper's
                            restricted-menu equilibrium claim on hardware.
  T2 gamma (item 7)         The deviation gap CHANGES SIGN across the sweep:
                            negative at gamma=0.30pi, positive at 0.45pi. SIGN
                            test. 0.40pi is registered as marginal.
  T3 fairness (item 6)      The per-player payoff vector of star N=4 is
                            INVARIANT under wiring permutation -- the
                            unfairness is locked to the graph position, not to
                            the physical qubit. Threshold test.
  T4 per-cell advantage     Mitigated fold-1 advantage per cell vs the
                            registered sigma_predictive. Quantitative, and the
                            most exposed to device-model error; see
                            uncertainties_excluded.

Usage (pinned env):
  conda run -n entangled-equilibria python scripts/preregister_topology.py

Refuses to overwrite an existing registration: this file is frozen once written.
"""

import glob
import json
import math
import os
import statistics
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "experiments"))

import numpy as np  # noqa: E402

from hardware_topology import (  # noqa: E402
    DEVIATION_CELL,
    DEVIATION_PROFILES,
    GAMMA,
    GAMMA_CELL,
    GAMMA_SWEEP,
    WIRING_CELL,
    WIRING_PERMS,
    _onehot,
    build_full_batch,
    environment_provenance,
    git_provenance,
    ideal_payoff_mean,
    ideal_probs,
    load_service,
    pinned_calibration,
    rehearse,
    series_key,
    series_meta,
)
from game.payoffs import expected_payoff  # noqa: E402
from hardware.mitigation import counts_to_probs  # noqa: E402

OUT = os.path.join(REPO, "results", "hardware-topology", "preregistration.json")

SEED = 20260725          # rehearsal seed; recorded in the registration
PREDICT_SHOTS = 200_000  # shots used to BUILD the prediction (MC error ~ 0)
REGISTERED_SHOTS = 4096  # shots the hardware run will use; sigmas quoted here
Z_CRIT = 1.96
BACKEND = "ibm_fez"

# T3's threshold. The noiseless per-player vector of star N=4 is identical
# across wirings by construction (the logical circuit does not depend on the
# wiring), so any measured difference is device inhomogeneity plus shot noise.
# 3 sigma at the registered shot count, floored so a lucky run cannot make the
# test unfalsifiably tight.
WIRING_SIGMA_MULTIPLE = 3.0
WIRING_THRESHOLD_FLOOR = 0.05


def fit_device_model_bias() -> dict:
    """Fit the Aer device-noise model's bias against the completed GHZ runs.

    Every hardware-scaling run stores predictions.device_model, the SAME kind
    of AerSimulator(NoiseModel.from_backend) prediction this registration is
    built from. Comparing it with what the device actually returned gives a
    measured, in-repo estimate of the model's error -- 9 points over 3
    calibration days (N=3,4,5 at 6/9/14 routed cz).

    All 9 deltas are negative: the model systematically OVER-predicts
    advantage, and the miss grows with cz. Fitting delta = beta*cz through the
    origin leaves a residual SD of ~0.0014 against ~0.0037 for a constant-bias
    baseline, so the one-parameter cz-linear form is the better description.

    Registering this as a COMPETING prediction, rather than silently folding it
    into the central value, follows the five-model precedent in
    results/hardware-scaling/repeat-judgments.json: let the simpler model
    compete in the open and report which one wins.
    """
    cz_by_n = {"3": 6, "4": 9, "5": 14}   # routed fold-1 cz on the pinned chain
    points = []
    for d in sorted(glob.glob(os.path.join(
            REPO, "results", "hardware-scaling", "2026-*"))):
        path = os.path.join(d, "result.json")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            r = json.load(fh)
        dm = r.get("predictions", {}).get("device_model")
        if not dm:
            continue
        for N, cz in cz_by_n.items():
            if N not in dm:
                continue
            # 'noro' = exact pre-measurement probabilities, i.e. what perfect
            # readout mitigation recovers -- the right comparator for the
            # MITIGATED measurement.
            pred = dm[N]["noro"]["advantage"]
            meas = r["analysis"]["series"][N]["folds"]["1"]["mitigated"]["advantage"]
            points.append({"run": os.path.basename(d), "N": int(N), "cz": cz,
                           "predicted": pred, "measured": meas,
                           "delta": meas - pred})
    if len(points) < 3:
        print("ERROR: too few completed scaling runs to fit the device-model bias")
        sys.exit(1)
    beta = (sum(p["cz"] * p["delta"] for p in points)
            / sum(p["cz"] ** 2 for p in points))
    resid = [p["delta"] - beta * p["cz"] for p in points]
    return {
        "form": "delta = beta * routed_cz_at_fold1, fitted through the origin",
        "beta": float(beta),
        "residual_sd": float(statistics.stdev(resid)),
        "n_points": len(points),
        "fitted_cz_range": [min(p["cz"] for p in points),
                            max(p["cz"] for p in points)],
        "constant_bias_baseline_residual_sd": float(
            statistics.stdev([p["delta"] - statistics.mean(
                [q["delta"] for q in points]) for p in points])),
        "all_deltas_negative": all(p["delta"] < 0 for p in points),
        "points": points,
    }


def per_player_sigma(probs: np.ndarray, N: int, shots: int) -> list[float]:
    """Multinomial shot-noise sigma of EACH player's mean payoff.

    payoff_stats returns only the sigma of the across-player mean; T1/T2/T3 all
    read individual players, so they need this.
    """
    cols = np.array([expected_payoff(_onehot(i, N), N) for i in range(2**N)])
    out = []
    for k in range(N):
        c = cols[:, k]
        mean = float(np.sum(probs * c))
        var = float(np.sum(probs * c**2) - mean**2)
        out.append(float(np.sqrt(max(var, 0.0) / shots)))
    return out


def find(analysis: dict, topology, N, gamma, profile, wiring) -> dict:
    key = series_key(series_meta(
        topology=topology, N=N, fold=1, gamma=gamma, profile=profile,
        wiring=wiring, fil=[0] * N, cz=0))
    if key not in analysis["series"]:
        print(f"ERROR: no series {key} in the rehearsal analysis")
        sys.exit(1)
    return analysis["series"][key]


def fold1_probs(s: dict) -> np.ndarray:
    return counts_to_probs(s["folds"]["1"]["counts"], s["N"])


def scaled_sigma(sigma_at_predict_shots: float) -> float:
    """Shot-noise sigma rescaled from PREDICT_SHOTS to REGISTERED_SHOTS."""
    return sigma_at_predict_shots * math.sqrt(PREDICT_SHOTS / REGISTERED_SHOTS)


def ideal_per_player(topology, N, gamma, profile) -> list[float]:
    return [float(x) for x in
            expected_payoff(ideal_probs(topology, N, gamma, profile), N)]


def deviation_gap(analysis, cell, gamma, dev_profile, position):
    """payoff_k(all-Q) - payoff_k(H at k): >= 0 means the deviation does not pay."""
    topology, N = cell
    coop = find(analysis, topology, N, gamma, ["Q"] * N, list(range(N)))
    dev = find(analysis, topology, N, gamma, dev_profile, list(range(N)))
    v_c = coop["folds"]["1"]["mitigated"]["per_player"]
    v_d = dev["folds"]["1"]["mitigated"]["per_player"]
    s_c = per_player_sigma(fold1_probs(coop), N, REGISTERED_SHOTS)[position]
    s_d = per_player_sigma(fold1_probs(dev), N, REGISTERED_SHOTS)[position]
    ideal_c = ideal_per_player(topology, N, gamma, ["Q"] * N)[position]
    ideal_d = ideal_per_player(topology, N, gamma, dev_profile)[position]
    return {
        "position": position,
        "profile": dev_profile,
        "gamma": float(gamma),
        "gamma_over_pi": float(gamma / math.pi),
        "predicted_gap": float(v_c[position] - v_d[position]),
        "sigma_predictive": float(math.sqrt(s_c**2 + s_d**2)),
        "ideal_gap": float(ideal_c - ideal_d),
        "cooperative_payoff": float(v_c[position]),
        "deviator_payoff": float(v_d[position]),
    }


def build_registration(analysis, plan, cal, bias) -> dict:
    series_out = {}
    for key, s in sorted(analysis["series"].items()):
        f1 = s["folds"]["1"]
        shot_sigma = scaled_sigma(f1["mitigated"]["sigma"])
        corrected = f1["mitigated"]["advantage"] + bias["beta"] * f1["cz"]
        entry = {
            "topology": s["topology"], "N": s["N"],
            "gamma": s["gamma"], "gamma_over_pi": s["gamma"] / math.pi,
            "profile": s["profile"], "wiring": s["wiring"],
            "cz_fold1": f1["cz"],
            "classical_ne_payoff": s["classical_ne_payoff"],
            "ideal_payoff": s["ideal_payoff"],
            "ideal_advantage": s["ideal_advantage"],
            # T4a: the device noise model as-is.
            "mitigated_fold1": {
                "advantage": f1["mitigated"]["advantage"],
                "sigma_predictive": shot_sigma,
                "per_player": f1["mitigated"]["per_player"],
                "per_player_sigma": per_player_sigma(
                    fold1_probs(s), s["N"], REGISTERED_SHOTS),
            },
            # T4b: same, plus the cz-linear bias measured on the GHZ runs.
            "mitigated_fold1_cz_corrected": {
                "advantage": corrected,
                "correction": bias["beta"] * f1["cz"],
                "sigma_predictive": float(math.sqrt(
                    shot_sigma**2 + bias["residual_sd"]**2)),
                "extrapolates_beyond_fit": f1["cz"] > bias["fitted_cz_range"][1],
            },
            "raw_fold1": {
                "advantage": f1["raw"]["advantage"],
                "p_ground": f1["raw"]["p_ground"],
            },
        }
        if "zne" in s:
            entry["zne_linear"] = {"advantage": s["zne"]["advantage"]}
        series_out[key] = entry

    # ── T1: equilibrium, ghz N=3 at gamma = pi/2 ──────────────────────────────
    t1 = [deviation_gap(analysis, DEVIATION_CELL, GAMMA, p, p.index("H"))
          for p in DEVIATION_PROFILES]

    # ── T2: gamma sweep of the same gap (position 0), incl. the free pi/2 point
    t2 = [deviation_gap(analysis, GAMMA_CELL, g, ["H", "Q", "Q"], 0)
          for g in list(GAMMA_SWEEP) + [GAMMA]]

    # ── T3: wiring invariance of the per-player vector, star N=4 ─────────────
    topology, N = WIRING_CELL
    base = find(analysis, topology, N, GAMMA, ["Q"] * N, list(range(N)))
    v_base = base["folds"]["1"]["mitigated"]["per_player"]
    sig_base = per_player_sigma(fold1_probs(base), N, REGISTERED_SHOTS)
    t3_perms = []
    for w in WIRING_PERMS:
        s = find(analysis, topology, N, GAMMA, ["Q"] * N, w)
        v = s["folds"]["1"]["mitigated"]["per_player"]
        sig = per_player_sigma(fold1_probs(s), N, REGISTERED_SHOTS)
        pair_sigma = max(math.sqrt(a**2 + b**2) for a, b in zip(sig_base, sig))
        t3_perms.append({
            "wiring": w,
            "predicted_per_player": v,
            "predicted_max_abs_deviation": float(
                max(abs(a - b) for a, b in zip(v, v_base))),
            "threshold": max(WIRING_SIGMA_MULTIPLE * pair_sigma,
                             WIRING_THRESHOLD_FLOOR),
        })

    return {
        "registered_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Frozen predictions for the ibm_fez multi-topology EWL batch "
            "(items 1, 2, 5, 6, 7), registered before the job was submitted. "
            "Predictions come from the mandatory dress rehearsal on the "
            "reduced device noise model; the registered tests are judged by "
            "scripts/judge_topology_run.py."),
        "backend": BACKEND,
        "git": git_provenance(),
        "environment": environment_provenance(),
        "calibration_at_registration": cal,
        "protocol": {
            "seed": SEED,
            "shots_used_to_predict": PREDICT_SHOTS,
            "shots_registered": REGISTERED_SHOTS,
            "z_crit": Z_CRIT,
            "pinned": plan["pinned"],
            "n_pubs": len(plan["pubs"]),
            "model": (
                "AerSimulator(method='density_matrix', "
                "noise_model=NoiseModel.from_backend(ibm_fez) reduced to the "
                "pinned set), per-pub seed = SEED + pub_index"),
            "advantage_convention": (
                "advantage = measured profile payoff - analytic noiseless "
                "classical NE payoff 1/N. NOT comparable to the "
                "circuit-relative gap used by the simulation figures."),
            "uncertainties_propagated": [
                "multinomial shot noise at REGISTERED_SHOTS, per player and "
                "across-player mean",
            ],
            "uncertainties_excluded": [
                "device-model error: NoiseModel.from_backend is a Pauli/"
                "readout approximation and omits coherent errors, crosstalk "
                "and leakage. This is the DOMINANT unmodelled term and is why "
                "T1-T3 are sign/threshold tests rather than z-tests.",
                "calibration drift between registration and execution",
                "readout-mitigation amplification of shot noise (the quoted "
                "sigmas are computed on the raw distribution)",
            ],
            "registered_tests": {
                "T1_equilibrium": (
                    "At ghz N=3, gamma=pi/2, every unilateral Hawk deviation "
                    "gap payoff_k(Q,Q,Q) - payoff_k(H at k) is >= 0. PASS iff "
                    "all three gaps are >= 0 within 1.96 sigma_predictive. "
                    "This is the restricted-menu {D,H,Q} equilibrium claim; "
                    "it is NOT a full-SU(2) equilibrium claim."),
                "T2_gamma_sign_change": (
                    "The same gap at position 0 is NEGATIVE at gamma=0.30pi "
                    "and POSITIVE at gamma=0.45pi and 0.50pi, i.e. the "
                    "cooperative profile becomes an equilibrium as "
                    "entanglement increases. PASS iff both signs come back as "
                    "registered at 0.30pi and 0.45pi. gamma=0.40pi is "
                    "registered as MARGINAL (ideal gap +0.0469, within ~2 "
                    "sigma of zero) and does not count toward pass/fail."),
                "T3_wiring_invariance": (
                    "star N=4's per-player payoff vector is INVARIANT under "
                    "wiring permutation: the position-locked unfairness is a "
                    "property of the entanglement topology, not of which "
                    "physical qubit a player was assigned. PASS iff, for each "
                    "permuted wiring, max_j |v_perm[j] - v_identity[j]| <= the "
                    "registered threshold. FAILURE would mean the paper's "
                    "player-position claim must be narrowed to this device."),
                "T4a_per_cell_advantage_uncorrected": (
                    "Each cell's measured mitigated fold-1 advantage vs the "
                    "raw device-noise-model prediction; PASS iff |z| <= 1.96 "
                    "with z = (measured - predicted) / sigma_predictive, "
                    "sigma being shot noise only. REGISTERED EXPECTATION: this "
                    "FAILS LOW and systematically. All 9 GHZ points in "
                    "results/hardware-scaling/ over 3 calibration days missed "
                    "in the same direction. It is registered anyway so the "
                    "size of the device-model error is measured rather than "
                    "assumed."),
                "T4b_per_cell_advantage_cz_corrected": (
                    "The competing model: the same prediction plus a "
                    "cz-linear bias correction fitted on those 9 GHZ points "
                    "(beta per routed fold-1 cz, through the origin), with "
                    "sigma = sqrt(shot^2 + fit residual^2). The substantive "
                    "registered claim is that the device-model bias is a "
                    "property of GATE COUNT and TRANSFERS ACROSS TOPOLOGIES: "
                    "beta was fitted on GHZ alone and is applied here to ring, "
                    "star, fully-connected and W. W N=3 at 42 cz is a 3x "
                    "extrapolation beyond the 6-14 cz fitting range and is the "
                    "sharpest discriminator -- the two models differ there by "
                    "~0.036, far outside shot noise. PASS iff |z| <= 1.96. "
                    "Whichever of T4a/T4b scores better wins on the record; "
                    "this mirrors the five-model comparison already in "
                    "results/hardware-scaling/repeat-judgments.json."),
                "T5_ring4_null": (
                    "ring N=4 is the only cell whose NOISELESS advantage is "
                    "zero: its ideal circuit is deterministic on |1111> "
                    "(all-Hawk). Registered: (a) its measured mitigated fold-1 "
                    "advantage is the smallest of all 12 topology cells; (b) "
                    "it is POSITIVE, i.e. device noise moves this cell AWAY "
                    "from its ideal and toward advantage; (c) ZNE brings it "
                    "back toward zero, |zne| < |raw|."),
            },
        },
        "device_model_bias_fit": bias,
        "predictions": {
            "series": series_out,
            "T1_deviation_gaps": t1,
            "T2_gamma_gap_sweep": t2,
            "T3_wiring_invariance": {
                "cell": {"topology": topology, "N": N},
                "identity_wiring": list(range(N)),
                "identity_per_player": v_base,
                "identity_per_player_sigma": sig_base,
                "ideal_per_player": ideal_per_player(
                    topology, N, GAMMA, ["Q"] * N),
                "permutations": t3_perms,
            },
            "T5_ring4_null": {
                "ideal_payoff": ideal_payoff_mean("ring", 4, GAMMA, ["Q"] * 4),
                "ideal_advantage": find(analysis, "ring", 4, GAMMA,
                                        ["Q"] * 4, [0, 1, 2, 3])["ideal_advantage"],
                "predicted_raw_advantage": find(
                    analysis, "ring", 4, GAMMA, ["Q"] * 4,
                    [0, 1, 2, 3])["folds"]["1"]["raw"]["advantage"],
                "predicted_zne_advantage": find(
                    analysis, "ring", 4, GAMMA, ["Q"] * 4,
                    [0, 1, 2, 3])["zne"]["advantage"],
            },
        },
    }


def main() -> None:
    if os.path.exists(OUT):
        print(f"REFUSING to overwrite {os.path.relpath(OUT)} -- a registration "
              f"is frozen once written. Delete it deliberately if you really "
              f"mean to re-register, and say so in the commit message.")
        sys.exit(1)

    bias = fit_device_model_bias()
    backend = load_service().backend(BACKEND)
    plan = build_full_batch(backend)
    analysis = rehearse(backend, plan, PREDICT_SHOTS, seed=SEED)
    cal = pinned_calibration(backend, plan["pinned"])
    reg = build_registration(analysis, plan, cal, bias)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=2)

    print("\n" + "=" * 78)
    print("REGISTERED PREDICTIONS (frozen)")
    print("=" * 78)
    print(f"\nT1 equilibrium -- ghz N=3, gamma=pi/2, deviation gaps "
          f"(>= 0 means the deviation does not pay):")
    for g in reg["predictions"]["T1_deviation_gaps"]:
        print(f"    position {g['position']} ({''.join(g['profile'])}): "
              f"predicted {g['predicted_gap']:+.4f} "
              f"+/- {g['sigma_predictive']:.4f}   (ideal {g['ideal_gap']:+.4f})")
    print(f"\nT2 gamma sweep -- same gap at position 0 (registered SIGN change):")
    for g in reg["predictions"]["T2_gamma_gap_sweep"]:
        print(f"    gamma = {g['gamma_over_pi']:.2f} pi: predicted "
              f"{g['predicted_gap']:+.4f} +/- {g['sigma_predictive']:.4f}   "
              f"(ideal {g['ideal_gap']:+.4f})")
    t3 = reg["predictions"]["T3_wiring_invariance"]
    print(f"\nT3 wiring invariance -- star N=4 per-player payoffs:")
    print(f"    ideal            {[round(x, 4) for x in t3['ideal_per_player']]}")
    print(f"    wiring {t3['identity_wiring']} "
          f"{[round(x, 4) for x in t3['identity_per_player']]}")
    for p in t3["permutations"]:
        print(f"    wiring {p['wiring']} "
              f"{[round(x, 4) for x in p['predicted_per_player']]}  "
              f"max dev {p['predicted_max_abs_deviation']:.4f} "
              f"<= {p['threshold']:.4f}")
    t5 = reg["predictions"]["T5_ring4_null"]
    print(f"\nT5 ring N=4 null -- ideal advantage {t5['ideal_advantage']:+.4f}, "
          f"predicted raw {t5['predicted_raw_advantage']:+.4f}, "
          f"ZNE {t5['predicted_zne_advantage']:+.4f}")
    b = reg["device_model_bias_fit"]
    print(f"\ndevice-model bias fit (from {b['n_points']} completed GHZ points, "
          f"cz {b['fitted_cz_range'][0]}-{b['fitted_cz_range'][1]}):")
    print(f"    beta = {b['beta']:.6f} per routed cz, residual SD "
          f"{b['residual_sd']:.6f}")
    print(f"    constant-bias baseline residual SD "
          f"{b['constant_bias_baseline_residual_sd']:.6f}; all deltas "
          f"negative: {b['all_deltas_negative']}")

    print(f"\nT4a/T4b per-cell mitigated fold-1 advantage "
          f"(sigma at {REGISTERED_SHOTS} shots):")
    print(f"    {'topology':16s} {'N':>2s} {'g/pi':>5s} {'profile':7s} "
          f"{'wiring':9s} {'cz':>3s} {'ideal':>8s} {'T4a':>9s} {'sigma':>7s} "
          f"{'T4b':>9s} {'sigma':>7s}")
    for key, e in reg["predictions"]["series"].items():
        a, c = e["mitigated_fold1"], e["mitigated_fold1_cz_corrected"]
        flag = " <-- extrapolated" if c["extrapolates_beyond_fit"] else ""
        print(f"    {e['topology']:16s} {e['N']:2d} {e['gamma_over_pi']:5.2f} "
              f"{''.join(e['profile']):7s} "
              f"{'-'.join(map(str, e['wiring'])):9s} {e['cz_fold1']:3d} "
              f"{e['ideal_advantage']:8.4f} "
              f"{a['advantage']:9.4f} {a['sigma_predictive']:7.4f} "
              f"{c['advantage']:9.4f} {c['sigma_predictive']:7.4f}{flag}")
    print(f"\nwrote {os.path.relpath(OUT)}")


if __name__ == "__main__":
    main()
