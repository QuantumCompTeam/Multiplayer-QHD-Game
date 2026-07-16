"""Pre-register COMPETING baseline predictions for the scaling repeats.

Extends the item-1 registration (results/hardware-scaling/preregistration.json,
which is immutable and is NOT touched -- this writes a separate file) with
three competitor models, each judged by the same conditional protocol as the
primary p_eff model: anchor on the day's N=3 mitigated fold-1 advantage,
predict that day's N=4/5 mitigated fold-1 advantages.

Competitors (all closed-form, no simulation):
  (a) cz-exponential  advantage retention decays exponentially in that run's
      transpiled fold-1 two-qubit-gate count: r = (A3/ideal3)^(1/cz3),
      pred_N = ideal_N * r^(cz_N). Gate counts read from the run's own
      pub_meta (run 1: cz = 6, 9, 14 at N = 3, 4, 5).
  (b) device-model    the run's own stored predictions.device_model.<N>.noro
      advantage (computed by the pipeline from backend calibration; 'noro' =
      ideal-readout, the mitigated-fold-1 comparator), anchored
      multiplicatively on N=3: pred_N = dm_N * (A3 / dm_3).
  (c) constant-retention (no-decay null)  whatever fractional deficit N=3
      shows applies unchanged at N=4/5: pred_N = ideal_N * (A3 / ideal_3).

Judging (registered here, applied by scripts/judge_repeat_run.py as
SECONDARY tests, clearly separated from the primary p_eff test):
  z_N = (measured_N - pred_N) / sigma_predictive(N, mitigated_fold1), with
  sigma_predictive taken from the PRIMARY registration -- a shared yardstick
  so competitor scores are comparable; these are model-comparison scores,
  not per-competitor calibrated intervals. Per-run score per model =
  z4^2 + z5^2 (lower is better); cumulative across repeats decides the
  best predictor of the scaling.

Timing: registered while repeat job d9chh0qneu4c739lvgb0 (submitted
2026-07-16T17:44:34Z, queued behind ibm_fez maintenance) had NOT returned;
the script refuses to run if any repeat run directory already exists, and
the commit timestamp vs the job's completion time proves the ordering.

Usage:  python scripts/preregister_baselines.py
Writes: results/hardware-scaling/preregistration-baselines.json
"""

import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
HW = os.path.join(REPO, "results", "hardware-scaling")
PRIMARY = os.path.join(HW, "preregistration.json")
OUT = os.path.join(HW, "preregistration-baselines.json")
NS = (3, 4, 5)

# 2q-gate count of the Month-4 logical {u,cx} GHZ circuit the primary p_eff
# model simulates (J + J-dagger, double CX ladder): 4(N-1). The hardware ISA
# circuits use the pub_meta cz counts instead (run 1: 6/9/14) -- the dose
# mismatch (ratios 0.75/0.75/0.875) is the declared N=5-deficit mechanism.
LOGICAL_CX = {N: 4 * (N - 1) for N in NS}


def fold1_cz(res: dict) -> dict[int, int]:
    return {m["N"]: m["cz"] for m in res["pub_meta"]
            if m.get("kind") == "series" and m.get("fold") == 1}


def corrected_fit_predict(res: dict) -> dict:
    """Item-5A competitor: the primary p_eff model with its 2q depolarizing
    dose rescaled per N to the run's ACTUAL transpiled cz count
    (p2_ratio = cz_N / logical_cx_N; 1q dose unchanged -- Part B territory).
    Fit on the day's N=3 mitigated fold-1 PAYOFF by the same 40-step
    bisection as the primary fit; predict N=4/5 advantages."""
    import numpy as np
    from circuits.ewl import q_strategy
    from circuits.noise import build_ewl_circuit_noisy
    from game.payoffs import expected_payoff

    cz = fold1_cz(res)
    ratio = {N: cz[N] / LOGICAL_CX[N] for N in NS}

    def pay(N: int, p: float) -> float:
        probs = build_ewl_circuit_noisy(
            N, [q_strategy(N)] * N, topology="ghz", p=p, p2_ratio=ratio[N])
        return float(np.mean(expected_payoff(probs, N)))

    target = res["analysis"]["series"]["3"]["folds"]["1"]["mitigated"]["mean"]
    lo, hi = 0.0, 0.10
    if pay(3, lo) < target:
        p_fit = 0.0
    else:
        for _ in range(40):
            mid = (lo + hi) / 2
            if pay(3, mid) > target:
                lo = mid
            else:
                hi = mid
        p_fit = (lo + hi) / 2
    out = {"p_fit": p_fit,
           "p2_ratio": {str(N): ratio[N] for N in NS}}
    for N in (4, 5):
        classical = res["analysis"]["series"][str(N)]["classical_ne_payoff"]
        out[str(N)] = pay(N, p_fit) - classical
    return out


def baseline_predictions(res: dict, ideal: dict[int, float]) -> dict:
    """The three competitors' conditional predictions from one run's data."""
    ana = res["analysis"]["series"]
    a3 = (ana["3"]["folds"]["1"]["mitigated"]["mean"]
          - ana["3"]["classical_ne_payoff"])
    cz = fold1_cz(res)
    r = (a3 / ideal[3]) ** (1.0 / cz[3])
    dm = {N: res["predictions"]["device_model"][str(N)]["noro"]["advantage"]
          for N in NS}
    corrected = corrected_fit_predict(res)
    out = {"anchor_A3": a3, "cz_fold1": {str(N): cz[N] for N in NS},
           "cz_exponential_r": r,
           "transpiled_count_corrected_fit": {
               "p_fit": corrected["p_fit"],
               "p2_ratio": corrected["p2_ratio"]}}
    for N in (4, 5):
        out[str(N)] = {
            "cz_exponential": ideal[N] * r ** cz[N],
            "device_model_anchored": dm[N] * (a3 / dm[3]),
            "constant_retention": ideal[N] * (a3 / ideal[3]),
            "transpiled_count_corrected": corrected[str(N)],
        }
    return out


def main() -> None:
    repeats = [d for d in glob.glob(os.path.join(HW, "*", "result.json"))
               if "2026-07-16T074134Z" not in d]
    if repeats:
        print("REFUSING: repeat run(s) already exist -- baselines can only "
              f"be registered against runs that have not landed: {repeats}")
        sys.exit(1)
    st = subprocess.run(
        ["git", "status", "--porcelain", "--",
         os.path.relpath(PRIMARY, REPO)],
        cwd=REPO, capture_output=True, text=True)
    if st.stdout.strip():
        print("REFUSING: primary preregistration.json differs from HEAD")
        sys.exit(1)

    prereg = json.load(open(PRIMARY, encoding="utf-8"))
    src_dir = os.path.join(REPO, prereg["source_run"]["dir"])
    res = json.load(open(os.path.join(src_dir, "result.json"),
                         encoding="utf-8"))
    ideal = {N: prereg["predicted_advantages"][str(N)]["ideal"] for N in NS}
    sigma = {N: prereg["predicted_advantages"][str(N)]["mitigated_fold1"]
                      ["sigma_predictive"] for N in NS}

    preds = baseline_predictions(res, ideal)

    # self-check on run 1 (its anchor == its own N=3, so these are the
    # baselines' analogue of source_run_comparison)
    self_check = {}
    for N in (4, 5):
        meas = (res["analysis"]["series"][str(N)]["folds"]["1"]["mitigated"]
                ["mean"]
                - res["analysis"]["series"][str(N)]["classical_ne_payoff"])
        row = {"measured_run1": meas}
        for model, pred in preds[str(N)].items():
            row[model] = {"predicted": pred, "delta": meas - pred,
                          "z": (meas - pred) / sigma[N]}
        self_check[str(N)] = row

    payload = {
        "registered_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": ("Competing baseline predictors for the scaling repeats, "
                    "registered before any repeat run landed. SECONDARY to "
                    "the primary p_eff registration (preregistration.json, "
                    "untouched). Conditional protocol: each model anchors on "
                    "the day's N=3 mitigated fold-1 advantage and predicts "
                    "that day's N=4/5."),
        "pending_job_not_yet_returned": "d9chh0qneu4c739lvgb0",
        "primary_registration": {
            "path": "results/hardware-scaling/preregistration.json",
            "registered_utc": prereg["registered_utc"],
        },
        "models": {
            "cz_exponential": ("advantage retention r^cz with r fit on the "
                               "day's N=3 (cz counts from that run's "
                               "pub_meta, fold 1)"),
            "device_model_anchored": ("the run's stored device-noise-model "
                                      "'noro' advantage, multiplicatively "
                                      "anchored on the day's N=3"),
            "constant_retention": ("no-decay null: N=3's fractional deficit "
                                   "applied unchanged at N=4/5"),
            "transpiled_count_corrected": (
                "item-5A (registered 2026-07-16, still before batch 2 "
                "returned): the primary p_eff depolarizing model with its "
                "2q dose rescaled per N to the run's ACTUAL transpiled cz "
                "counts (p2_ratio = cz_N / 4(N-1)); fit on the day's N=3 "
                "mitigated fold-1 payoff by the same bisection as the "
                "primary. This is the corrected SPECIFICATION of the "
                "primary model: if it scores near cz_exponential, the "
                "model competition partially resolves into a specification "
                "error in the original fit. 1q-count and raw-vs-mitigated "
                "corrections (item-5 Part B) are explicitly deferred."),
        },
        "judging": {
            "sigma_predictive": {str(N): sigma[N] for N in (4, 5)},
            "sigma_source": ("primary registration, mitigated_fold1 -- shared "
                             "yardstick; model-comparison scores, not "
                             "per-competitor calibrated intervals"),
            "score": "z4^2 + z5^2 per run, cumulative across repeats; "
                     "lower is better; the primary p_eff model competes on "
                     "the same score",
        },
        "run1_anchored_predictions": preds,
        "run1_self_check": self_check,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)

    print("registered baseline predictions (run-1 anchored):")
    print(f"  anchor A3 = {preds['anchor_A3']:.6f}, "
          f"cz = {preds['cz_fold1']}, r = {preds['cz_exponential_r']:.6f}")
    print("  N | model                      | predicted | run-1 measured | z")
    for N in (4, 5):
        for model in ("cz_exponential", "device_model_anchored",
                      "constant_retention", "transpiled_count_corrected"):
            row = self_check[str(N)][model]
            print(f"  {N} | {model:<26s} | {row['predicted']:9.6f} | "
                  f"{self_check[str(N)]['measured_run1']:14.6f} | "
                  f"{row['z']:+5.2f}")
    print(f"saved: {os.path.relpath(OUT, os.getcwd())}")


if __name__ == "__main__":
    main()
