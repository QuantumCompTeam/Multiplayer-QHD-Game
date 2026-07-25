"""Judge topology-batch runs against the LOCKED pre-registration.

Applies exactly the tests frozen in results/hardware-topology/preregistration.json
to every completed run under results/hardware-topology/. This script never
writes to the registration and refuses to run if the working copy of it differs
from HEAD -- a registration that can be edited after the data arrives is not a
registration.

  T1  equilibrium: all three unilateral Hawk deviation gaps at ghz N=3,
      gamma=pi/2 are >= 0 (sign test, judged at the registered sigma).
  T2  gamma: the same gap changes sign across the sweep -- negative at
      0.30pi, positive at 0.45pi. 0.40pi is reported but registered MARGINAL
      and does not count.
  T3  fairness: star N=4's per-player payoff vector is invariant under wiring
      permutation (threshold test at the registered threshold).
  T4a device noise model as-is, per cell, |z| <= 1.96.
  T4b same plus the cz-linear bias fitted on the GHZ runs, |z| <= 1.96.
      T4a vs T4b is a registered model comparison; the score line reports both.
  T5  ring N=4 null: smallest advantage of the 12 topology cells, positive,
      and ZNE pulls it back toward its zero ideal.

Usage (pinned env):
  conda run -n entangled-equilibria python scripts/judge_topology_run.py

Writes results/hardware-topology/<run>/judgments.json per run.
"""

import glob
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "experiments"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hardware_topology import series_key, series_meta  # noqa: E402

HW_DIR = os.path.join(REPO, "results", "hardware-topology")
PREREG = os.path.join(HW_DIR, "preregistration.json")
Z_CRIT = 1.96


def prereg_is_pristine() -> bool:
    """The registration must be byte-identical to the committed version."""
    rel = os.path.relpath(PREREG, REPO)
    try:
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rel],
                                 cwd=REPO, capture_output=True, text=True)
        if tracked.returncode != 0:
            print(f"REFUSING: {rel} is not committed. The registration must be "
                  f"committed BEFORE the data it judges.")
            return False
        diff = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel],
                              cwd=REPO)
        if diff.returncode != 0:
            print(f"REFUSING: {rel} differs from HEAD. A registration edited "
                  f"after the fact is not a registration.")
            return False
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSING: could not verify {rel} against git: {exc}")
        return False
    return True


def key_of(topology, N, gamma, profile, wiring) -> str:
    return series_key(series_meta(
        topology=topology, N=N, fold=1, gamma=gamma, profile=profile,
        wiring=wiring, fil=[0] * N, cz=0))


def measured(analysis, topology, N, gamma, profile, wiring):
    return analysis["series"].get(key_of(topology, N, gamma, profile, wiring))


def verdict(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def judge_t1(reg, analysis) -> dict:
    out, all_ok = [], True
    for g in reg["predictions"]["T1_deviation_gaps"]:
        N, gamma, k = 3, g["gamma"], g["position"]
        coop = measured(analysis, "ghz", N, gamma, ["Q"] * N, list(range(N)))
        dev = measured(analysis, "ghz", N, gamma, g["profile"], list(range(N)))
        if coop is None or dev is None:
            out.append({"position": k, "verdict": "MISSING"})
            all_ok = False
            continue
        gap = (coop["folds"]["1"]["mitigated"]["per_player"][k]
               - dev["folds"]["1"]["mitigated"]["per_player"][k])
        sigma = g["sigma_predictive"]
        ok = gap >= -Z_CRIT * sigma
        all_ok &= ok
        out.append({"position": k, "profile": g["profile"],
                    "predicted_gap": g["predicted_gap"], "measured_gap": gap,
                    "sigma_predictive": sigma,
                    "z_vs_prediction": (gap - g["predicted_gap"]) / sigma,
                    "deviation_pays": gap < -Z_CRIT * sigma,
                    "verdict": verdict(ok)})
    return {"claim": reg["protocol"]["registered_tests"]["T1_equilibrium"],
            "gaps": out, "verdict": verdict(all_ok)}


def judge_t2(reg, analysis) -> dict:
    out = {}
    for g in reg["predictions"]["T2_gamma_gap_sweep"]:
        gamma, N = g["gamma"], 3
        coop = measured(analysis, "ghz", N, gamma, ["Q"] * N, list(range(N)))
        dev = measured(analysis, "ghz", N, gamma, ["H", "Q", "Q"],
                       list(range(N)))
        label = f"{g['gamma_over_pi']:.2f}pi"
        if coop is None or dev is None:
            out[label] = {"verdict": "MISSING"}
            continue
        gap = (coop["folds"]["1"]["mitigated"]["per_player"][0]
               - dev["folds"]["1"]["mitigated"]["per_player"][0])
        sigma = g["sigma_predictive"]
        out[label] = {"predicted_gap": g["predicted_gap"], "measured_gap": gap,
                      "sigma_predictive": sigma,
                      "significantly_negative": gap < -Z_CRIT * sigma,
                      "significantly_positive": gap > Z_CRIT * sigma}
    lo, hi = out.get("0.30pi", {}), out.get("0.45pi", {})
    ok = bool(lo.get("significantly_negative")) and bool(
        hi.get("significantly_positive"))
    return {"claim": reg["protocol"]["registered_tests"]["T2_gamma_sign_change"],
            "points": out,
            "marginal_point_not_counted": "0.40pi",
            "verdict": verdict(ok)}


def judge_t3(reg, analysis) -> dict:
    t3 = reg["predictions"]["T3_wiring_invariance"]
    topology, N = t3["cell"]["topology"], t3["cell"]["N"]
    gamma = reg["predictions"]["series"][key_of(
        topology, N, math.pi / 2, ["Q"] * N, list(range(N)))]["gamma"]
    base = measured(analysis, topology, N, gamma, ["Q"] * N, t3["identity_wiring"])
    if base is None:
        return {"verdict": "MISSING"}
    v_base = base["folds"]["1"]["mitigated"]["per_player"]
    out, all_ok = [], True
    for p in t3["permutations"]:
        s = measured(analysis, topology, N, gamma, ["Q"] * N, p["wiring"])
        if s is None:
            out.append({"wiring": p["wiring"], "verdict": "MISSING"})
            all_ok = False
            continue
        v = s["folds"]["1"]["mitigated"]["per_player"]
        dev = max(abs(a - b) for a, b in zip(v, v_base))
        ok = dev <= p["threshold"]
        all_ok &= ok
        out.append({"wiring": p["wiring"], "measured_per_player": v,
                    "max_abs_deviation": dev, "threshold": p["threshold"],
                    "predicted_max_abs_deviation":
                        p["predicted_max_abs_deviation"],
                    "verdict": verdict(ok)})
    return {"claim": reg["protocol"]["registered_tests"]["T3_wiring_invariance"],
            "identity_wiring": t3["identity_wiring"],
            "identity_measured_per_player": v_base,
            "ideal_per_player": t3["ideal_per_player"],
            "permutations": out, "verdict": verdict(all_ok)}


def judge_t4(reg, analysis) -> dict:
    rows, n_a, n_b, n = [], 0, 0, 0
    for key, e in reg["predictions"]["series"].items():
        s = analysis["series"].get(key)
        if s is None:
            rows.append({"series": key, "verdict": "MISSING"})
            continue
        meas = s["folds"]["1"]["mitigated"]["advantage"]
        row = {"series": key, "topology": e["topology"], "N": e["N"],
               "cz": e["cz_fold1"], "measured": meas}
        for tag, pred in (("T4a", e["mitigated_fold1"]),
                          ("T4b", e["mitigated_fold1_cz_corrected"])):
            z = (meas - pred["advantage"]) / pred["sigma_predictive"]
            row[tag] = {"predicted": pred["advantage"],
                        "sigma_predictive": pred["sigma_predictive"],
                        "z": z, "verdict": verdict(abs(z) <= Z_CRIT)}
        n += 1
        n_a += abs(row["T4a"]["z"]) <= Z_CRIT
        n_b += abs(row["T4b"]["z"]) <= Z_CRIT
        rows.append(row)
    rms_a = math.sqrt(sum(r["T4a"]["z"] ** 2 for r in rows if "T4a" in r) / n) if n else 0.0
    rms_b = math.sqrt(sum(r["T4b"]["z"] ** 2 for r in rows if "T4b" in r) / n) if n else 0.0
    return {
        "claim_a": reg["protocol"]["registered_tests"][
            "T4a_per_cell_advantage_uncorrected"],
        "claim_b": reg["protocol"]["registered_tests"][
            "T4b_per_cell_advantage_cz_corrected"],
        "series": rows,
        "score": {"n_series": n, "T4a_passed": n_a, "T4b_passed": n_b,
                  "T4a_rms_z": rms_a, "T4b_rms_z": rms_b,
                  "better_model": "T4b" if rms_b < rms_a else "T4a"},
        "verdict_T4a": verdict(n_a == n),
        "verdict_T4b": verdict(n_b == n),
    }


def judge_t5(reg, analysis) -> dict:
    ring4 = measured(analysis, "ring", 4, math.pi / 2, ["Q"] * 4, [0, 1, 2, 3])
    if ring4 is None:
        return {"verdict": "MISSING"}
    adv = ring4["folds"]["1"]["mitigated"]["advantage"]
    # the 12 topology cells: all-Q, gamma=pi/2, identity wiring
    others = [s["folds"]["1"]["mitigated"]["advantage"]
              for s in analysis["series"].values()
              if set(s["profile"]) == {"Q"}
              and abs(s["gamma"] - math.pi / 2) < 1e-12
              and s["wiring"] == list(range(s["N"]))]
    raw = ring4["folds"]["1"]["raw"]["advantage"]
    zne = ring4.get("zne", {}).get("advantage")
    a = all(adv <= o + 1e-12 for o in others)
    b = adv > 0
    c = zne is not None and abs(zne) < abs(raw)
    return {"claim": reg["protocol"]["registered_tests"]["T5_ring4_null"],
            "ideal_advantage": reg["predictions"]["T5_ring4_null"][
                "ideal_advantage"],
            "measured_mitigated_advantage": adv,
            "measured_raw_advantage": raw,
            "measured_zne_advantage": zne,
            "n_topology_cells_compared": len(others),
            "a_smallest_of_all_cells": bool(a),
            "b_positive": bool(b),
            "c_zne_moves_toward_zero": bool(c),
            "verdict": verdict(a and b and c)}


def judge_run(run_dir: str, reg: dict) -> dict:
    with open(os.path.join(run_dir, "result.json"), encoding="utf-8") as fh:
        run = json.load(fh)
    analysis = run["analysis"]
    j = {
        "judged_utc": datetime.now(timezone.utc).isoformat(),
        "run_dir": os.path.relpath(run_dir, REPO).replace("\\", "/"),
        "job": run.get("job"),
        "run_git_commit": run.get("git", {}).get("commit"),
        "registration_registered_utc": reg["registered_utc"],
        "registration_git_commit": reg.get("git", {}).get("commit"),
        "T1_equilibrium": judge_t1(reg, analysis),
        "T2_gamma_sign_change": judge_t2(reg, analysis),
        "T3_wiring_invariance": judge_t3(reg, analysis),
        "T4_per_cell_advantage": judge_t4(reg, analysis),
        "T5_ring4_null": judge_t5(reg, analysis),
    }
    cal = os.path.join(run_dir, "calibration_at_submit.json")
    if os.path.exists(cal):
        with open(cal, encoding="utf-8") as fh:
            j["calibration_at_submit"] = json.load(fh).get(
                "calibration_last_update")
    return j


def main() -> None:
    if not os.path.exists(PREREG):
        print(f"no registration at {os.path.relpath(PREREG)}; run "
              f"scripts/preregister_topology.py first")
        sys.exit(1)
    if not prereg_is_pristine():
        sys.exit(1)
    with open(PREREG, encoding="utf-8") as fh:
        reg = json.load(fh)

    runs = [d for d in sorted(glob.glob(os.path.join(HW_DIR, "2026-*")))
            if os.path.exists(os.path.join(d, "result.json"))]
    if not runs:
        print(f"no completed runs under {os.path.relpath(HW_DIR)} yet")
        return

    for run_dir in runs:
        j = judge_run(run_dir, reg)
        out = os.path.join(run_dir, "judgments.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(j, fh, indent=2)
        print(f"\n=== {os.path.basename(run_dir)} ===")
        for t in ("T1_equilibrium", "T2_gamma_sign_change",
                  "T3_wiring_invariance", "T5_ring4_null"):
            print(f"  {t:24s} {j[t].get('verdict')}")
        sc = j["T4_per_cell_advantage"]["score"]
        print(f"  {'T4a (model as-is)':24s} "
              f"{j['T4_per_cell_advantage']['verdict_T4a']} "
              f"({sc['T4a_passed']}/{sc['n_series']} series, "
              f"rms z {sc['T4a_rms_z']:.2f})")
        print(f"  {'T4b (cz-corrected)':24s} "
              f"{j['T4_per_cell_advantage']['verdict_T4b']} "
              f"({sc['T4b_passed']}/{sc['n_series']} series, "
              f"rms z {sc['T4b_rms_z']:.2f})")
        print(f"  better model: {sc['better_model']}")
        print(f"  wrote {os.path.relpath(out, REPO)}")


if __name__ == "__main__":
    main()
