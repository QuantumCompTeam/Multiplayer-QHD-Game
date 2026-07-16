"""Judge hardware-scaling repeat runs against the LOCKED pre-registration.

Applies, to every run under results/hardware-scaling/ other than the
registration's source run, exactly the tests registered in
results/hardware-scaling/preregistration.json (frozen in the item-1 commit;
this script never writes to it and refuses to run if the working copy
differs from HEAD):

  primary   CONDITIONAL test: refit p_eff on that run's own N=3 mitigated
            fold-1 payoff (production bisection), predict that run's N=4/5
            mitigated fold-1 advantages, judge with the registered
            sigma_predictive (PASS iff |z| <= 1.96).
  sharp     does run 1's registered N=5 deficit (measured - predicted =
            -0.0101, z = -5.2) reproduce? Systematic same-signed misses
            across repeats falsify the one-parameter model.
  secondary UNCONDITIONAL test: measured advantages vs the registered pi95
            intervals as-is (assumes cross-day stationarity).

Also reports, per run and fold-1 series (raw + mitigated): the per-player
payoff vectors, worst-player advantage and per-player spread -- the mean can
stay on-prediction while individual players fall below classical.

Self-validation: judging the SOURCE run must reproduce the registered
p_eff exactly and the registered source_run_comparison z-scores.

Usage (pinned env):
  conda run -n entangled-equilibria python scripts/judge_repeat_run.py

Writes results/hardware-scaling/repeat-judgments.json (regenerated from all
runs each invocation; the pre-registration file is never touched).
"""

import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "experiments"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402

from hardware_scaling import effective_p_prediction  # noqa: E402
from game.nash import compute_advantage  # noqa: E402
from preregister_baselines import baseline_predictions  # noqa: E402

HW_DIR = os.path.join(REPO, "results", "hardware-scaling")
PREREG = os.path.join(HW_DIR, "preregistration.json")
BASELINES = os.path.join(HW_DIR, "preregistration-baselines.json")
OUT = os.path.join(HW_DIR, "repeat-judgments.json")
NS = (3, 4, 5)
Z_CRIT = 1.96


def prereg_is_pristine() -> bool:
    """Both registrations must be byte-identical to the committed versions."""
    r = subprocess.run(
        ["git", "status", "--porcelain", "--",
         os.path.relpath(PREREG, REPO), os.path.relpath(BASELINES, REPO)],
        cwd=REPO, capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() == ""


def load_runs() -> list[tuple[str, dict, dict | None]]:
    runs = []
    for path in sorted(glob.glob(os.path.join(HW_DIR, "*", "result.json"))):
        d = os.path.basename(os.path.dirname(path))
        res = json.load(open(path, encoding="utf-8"))
        cal_path = os.path.join(os.path.dirname(path), "calibration.json")
        cal = (json.load(open(cal_path, encoding="utf-8"))
               if os.path.exists(cal_path) else None)
        runs.append((d, res, cal))
    return runs


def per_player_report(res: dict) -> dict:
    """Item-(c) block: fold-1 per-player payoff vectors, worst, spread."""
    out = {}
    for N in NS:
        s = res["analysis"]["series"][str(N)]
        classical = s["classical_ne_payoff"]
        blk = {}
        for kind in ("raw", "mitigated"):
            vec = s["folds"]["1"][kind]["per_player"]
            adv = [v - classical for v in vec]
            blk[kind] = {
                "per_player_payoff": vec,
                "per_player_advantage": adv,
                "worst_player_advantage": min(adv),
                "spread": max(vec) - min(vec),
                "any_player_below_classical": bool(min(adv) < 0),
            }
        out[str(N)] = blk
    return out


def judge_run(run_id: str, res: dict, cal: dict | None, prereg: dict,
              refs: dict, source_id: str, seen_cals: list) -> dict:
    is_source = run_id == source_id
    meas = {N: res["analysis"]["series"][str(N)]["folds"]["1"]["mitigated"]
            for N in NS}
    zne = {N: res["analysis"]["series"][str(N)]["zne"]["advantage"]
           for N in NS}

    # conditional (primary): refit on this run's N=3 anchor
    fit = effective_p_prediction(meas[3]["mean"], refs)
    cond = {}
    for N in (4, 5):
        pr = prereg["predicted_advantages"][str(N)]["mitigated_fold1"]
        predicted = fit[str(N)]["advantage"]
        measured = meas[N]["advantage"]
        z = (measured - predicted) / pr["sigma_predictive"]
        cond[str(N)] = {
            "predicted_conditional": predicted,
            "measured": measured,
            "delta": measured - predicted,
            "z": z,
            "sigma_predictive": pr["sigma_predictive"],
            "pass_95": bool(abs(z) <= Z_CRIT),
        }

    # competing baselines (secondary registered tests, item 4): same
    # conditional protocol, shared sigma yardstick, score = z4^2 + z5^2.
    ideal = {N: prereg["predicted_advantages"][str(N)]["ideal"] for N in NS}
    bp = baseline_predictions(res, ideal)
    competitors: dict = {}
    scores = {"p_eff_primary": sum(cond[str(N)]["z"] ** 2 for N in (4, 5))}
    for model in ("cz_exponential", "device_model_anchored",
                  "constant_retention"):
        blk = {}
        score = 0.0
        for N in (4, 5):
            sig = prereg["predicted_advantages"][str(N)]["mitigated_fold1"] \
                        ["sigma_predictive"]
            z = (meas[N]["advantage"] - bp[str(N)][model]) / sig
            blk[str(N)] = {"predicted_conditional": bp[str(N)][model],
                           "measured": meas[N]["advantage"],
                           "z": z, "pass_95": bool(abs(z) <= Z_CRIT)}
            score += z ** 2
        blk["score_z2"] = score
        scores[model] = score
        competitors[model] = blk
    ranking = sorted(scores, key=scores.get)

    # unconditional (secondary): registered intervals as-is
    uncond = {}
    for N in (4, 5):
        blk = {}
        for level, val in (("mitigated_fold1", meas[N]["advantage"]),
                           ("zne_linear", zne[N])):
            pr = prereg["predicted_advantages"][str(N)][level]
            lo, hi = pr["pi95"]
            blk[level] = {"measured": val, "pi95": [lo, hi],
                          "pass_95": bool(lo <= val <= hi)}
        uncond[str(N)] = blk

    cal_stamp = cal["calibration_last_update"] if cal else None
    distinct = cal_stamp is not None and cal_stamp not in seen_cals

    return {
        "run": run_id,
        "job_id": res["job"]["job_id"],
        "backend": res["job"]["backend"],
        "created_utc": res["created_utc"],
        "calibration_last_update": cal_stamp,
        "distinct_calibration_vs_previous_runs": bool(distinct),
        "chain": res["analysis"]["chain"],
        "is_registration_source": is_source,
        "p_eff_refit": fit["p_eff"],
        "conditional_primary": cond,
        "n5_deficit": {
            "delta": cond["5"]["delta"],
            "z": cond["5"]["z"],
            "registered_run1_delta": prereg["source_run_comparison"]["5"]
                                           ["mitigated_fold1"]["delta"],
            "registered_run1_z": prereg["source_run_comparison"]["5"]
                                       ["mitigated_fold1"]["z"],
            "same_sign_as_run1": bool(
                np.sign(cond["5"]["delta"])
                == np.sign(prereg["source_run_comparison"]["5"]
                                 ["mitigated_fold1"]["delta"])),
        },
        "unconditional_secondary": uncond,
        "competing_baselines_secondary": {
            "note": ("item-4 registration: preregistration-baselines.json; "
                     "model-comparison scores on the shared sigma yardstick, "
                     "separate from the primary p_eff test above"),
            "models": competitors,
            "scores_z2": scores,
            "ranking_best_first": ranking,
        },
        "per_player_fold1": per_player_report(res),
    }


def main() -> None:
    if not prereg_is_pristine():
        print("REFUSING TO JUDGE: preregistration.json differs from HEAD "
              "(the registration is immutable; restore it first).")
        sys.exit(1)
    prereg = json.load(open(PREREG, encoding="utf-8"))
    source_id = os.path.basename(prereg["source_run"]["dir"])
    refs = {N: compute_advantage(N=N) for N in NS}
    runs = load_runs()

    # self-validation on the source run
    src = next((r for r in runs if r[0] == source_id), None)
    if src is None:
        print(f"source run {source_id} not found")
        sys.exit(1)
    v = judge_run(src[0], src[1], src[2], prereg, refs, source_id, [])
    ok_p = abs(v["p_eff_refit"] - prereg["p_eff"]["central"]) < 1e-15
    ok_z = all(
        abs(v["conditional_primary"][str(N)]["z"]
            - prereg["source_run_comparison"][str(N)]["mitigated_fold1"]["z"])
        < 1e-9 for N in (4, 5))
    print(f"self-validation on source run: p_eff refit "
          f"{'exact' if ok_p else 'MISMATCH'}, registered z-scores "
          f"{'reproduced' if ok_z else 'MISMATCH'}")
    if not (ok_p and ok_z):
        sys.exit(1)

    judgments = []
    seen_cals: list = []
    for run_id, res, cal in runs:
        j = judge_run(run_id, res, cal, prereg, refs, source_id, seen_cals)
        if cal:
            seen_cals.append(cal["calibration_last_update"])
        judgments.append(j)
        tag = "SOURCE (anchor, not a test)" if j["is_registration_source"] \
            else "REPEAT"
        print(f"\n=== {run_id} [{tag}] job {j['job_id']} ===")
        print(f"  calibration {j['calibration_last_update']} "
              f"(distinct vs previous: "
              f"{j['distinct_calibration_vs_previous_runs']})")
        print(f"  p_eff refit on this run's N=3: {j['p_eff_refit']:.6e}")
        for N in (4, 5):
            c = j["conditional_primary"][str(N)]
            print(f"  N={N} conditional: measured {c['measured']:+.4f} vs "
                  f"predicted {c['predicted_conditional']:+.4f}  "
                  f"z={c['z']:+.2f}  "
                  f"{'PASS' if c['pass_95'] else 'FAIL'} (95%)")
        d = j["n5_deficit"]
        print(f"  N=5 deficit: {d['delta']:+.4f} (z={d['z']:+.2f}) vs run-1 "
              f"registered {d['registered_run1_delta']:+.4f} "
              f"(z={d['registered_run1_z']:+.2f}) -- same sign: "
              f"{d['same_sign_as_run1']}")
        cb = j["competing_baselines_secondary"]
        print("  secondary baselines (score z4^2+z5^2, lower better): "
              + "  ".join(f"{m}={cb['scores_z2'][m]:.1f}"
                          for m in cb["ranking_best_first"]))
        for N in NS:
            pp = j["per_player_fold1"][str(N)]["mitigated"]
            print(f"  N={N} per-player mitigated adv: "
                  f"{[round(a, 4) for a in pp['per_player_advantage']]}  "
                  f"worst {pp['worst_player_advantage']:+.4f}  "
                  f"spread {pp['spread']:.4f}")

    n_rep = sum(1 for j in judgments if not j["is_registration_source"])
    n_deficit = sum(1 for j in judgments
                    if not j["is_registration_source"]
                    and j["n5_deficit"]["same_sign_as_run1"]
                    and not j["conditional_primary"]["5"]["pass_95"])
    print(f"\nsummary: {n_rep} repeat run(s) judged; N=5 conditional "
          f"deficit (same-signed, |z|>1.96) reproduced in {n_deficit} "
          f"of {n_rep}")

    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "preregistration": {
            "path": "results/hardware-scaling/preregistration.json",
            "registered_utc": prereg["registered_utc"],
            "p_eff_central": prereg["p_eff"]["central"],
        },
        "n_repeats_judged": n_rep,
        "judgments": judgments,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"saved: {os.path.relpath(OUT, os.getcwd())}")


if __name__ == "__main__":
    main()
