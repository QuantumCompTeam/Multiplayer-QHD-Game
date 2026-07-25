"""Judge the extended N=3..7 scaling run against the LOCKED n67 registration.

Applies exactly the tests frozen in
results/hardware-scaling/preregistration-n67.json. Never writes to it, and
refuses to run unless it is committed and byte-identical to HEAD.

  T1  M1 (depolarizing p_eff) predicts N=6,7; PASS iff |z| <= 1.96.
  T2  M2 (cz-exponential) predicts N=6,7; PASS iff |z| <= 1.96.
  T3  the model race: which model is closer at N=6,7, and does that AGREE
      with the ranking the N=4,5 repeats already produced (M2 ahead)?
  T4  measured advantage strictly decreasing in N over 3,4,5,6,7.

Usage (pinned env):
  conda run -n entangled-equilibria python scripts/judge_n67_run.py [RUN_DIR]

Writes <run_dir>/judgments-n67.json.
"""

import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HW_DIR = os.path.join(REPO, "results", "hardware-scaling")
PREREG = os.path.join(HW_DIR, "preregistration-n67.json")
Z_CRIT = 1.96


def prereg_is_pristine() -> bool:
    rel = os.path.relpath(PREREG, REPO).replace("\\", "/")
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rel],
                             cwd=REPO, capture_output=True, text=True)
    if tracked.returncode != 0:
        print(f"REFUSING: {rel} is not committed. The registration must be "
              f"committed BEFORE the data it judges.")
        return False
    if subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel],
                      cwd=REPO).returncode != 0:
        print(f"REFUSING: {rel} differs from HEAD.")
        return False
    return True


def find_run(reg: dict, explicit: str | None) -> str | None:
    """The newest run carrying every N the registration predicts."""
    if explicit:
        return explicit
    want = {str(N) for N in reg["protocol"]["ns"]}
    for d in sorted(glob.glob(os.path.join(HW_DIR, "2026-*")), reverse=True):
        path = os.path.join(d, "result.json")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            r = json.load(fh)
        if want <= set(r.get("analysis", {}).get("series", {})):
            return d
    return None


def verdict(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def judge(reg: dict, run: dict) -> dict:
    ns = reg["protocol"]["ns"]
    new_ns = reg["protocol"]["new_ns"]
    series = run["analysis"]["series"]
    meas = {N: series[str(N)]["folds"]["1"]["mitigated"]["advantage"] for N in ns}

    def model_rows(tag):
        m = reg[tag]
        rows = {}
        for N in ns:
            pred = m["advantage"][str(N)]
            sig = m["sigma_predictive"][str(N)]
            z = (meas[N] - pred) / sig
            rows[str(N)] = {"predicted": pred, "measured": meas[N],
                            "sigma_predictive": sig, "z": z,
                            "abs_error": abs(meas[N] - pred),
                            "verdict": verdict(abs(z) <= Z_CRIT)}
        return rows

    m1, m2 = model_rows("M1_depolarizing"), model_rows("M2_cz_exponential")
    t1_ok = all(m1[str(N)]["verdict"] == "PASS" for N in new_ns)
    t2_ok = all(m2[str(N)]["verdict"] == "PASS" for N in new_ns)

    race = {}
    for N in ns:
        a, b = m1[str(N)]["abs_error"], m2[str(N)]["abs_error"]
        race[str(N)] = {"m1_abs_error": a, "m2_abs_error": b,
                        "winner": "M2" if b < a else "M1"}
    new_winners = [race[str(N)]["winner"] for N in new_ns]
    m2_wins_new = all(w == "M2" for w in new_winners)

    decreasing = all(meas[ns[i]] > meas[ns[i + 1]] for i in range(len(ns) - 1))

    return {
        "judged_utc": datetime.now(timezone.utc).isoformat(),
        "registration_registered_utc": reg["registered_utc"],
        "registration_git_commit": reg.get("git", {}).get("commit"),
        "anchor_run": reg["anchor_run"]["dir"],
        "job": run.get("job"),
        "chain_registered": reg["protocol"]["chain"],
        "chain_executed": run["analysis"].get("chain"),
        "chain_matches": (list(reg["protocol"]["chain"])
                          == list(run["analysis"].get("chain") or [])),
        "routed_cz_registered": reg["protocol"]["routed_cz_fold1"],
        "routed_cz_executed": {
            str(m["N"]): m["cz"] for m in run.get("pub_meta", [])
            if m.get("kind") == "series" and m.get("fold") == 1},
        "T1_m1_depolarizing": {
            "claim": reg["protocol"]["registered_tests"]["T1_m1_depolarizing"],
            "p_eff": reg["M1_depolarizing"]["p_eff"],
            "series": m1, "verdict": verdict(t1_ok)},
        "T2_m2_cz_exponential": {
            "claim": reg["protocol"]["registered_tests"]["T2_m2_cz_exponential"],
            "r": reg["M2_cz_exponential"]["r"],
            "series": m2, "verdict": verdict(t2_ok)},
        "T3_model_race": {
            "claim": reg["protocol"]["registered_tests"]["T3_model_race"],
            "per_N": race,
            "winner_at_new_ns": new_winners,
            "m2_wins_both_new": m2_wins_new,
            "agrees_with_existing_ranking": m2_wins_new,
            "verdict": "M2" if m2_wins_new else (
                "M1" if all(w == "M1" for w in new_winners) else "SPLIT")},
        "T4_monotone_decay": {
            "claim": reg["protocol"]["registered_tests"]["T4_monotone_decay"],
            "measured": {str(N): meas[N] for N in ns},
            "verdict": verdict(decreasing)},
    }


def main() -> None:
    if not os.path.exists(PREREG):
        print(f"no registration at {os.path.relpath(PREREG)}")
        sys.exit(1)
    if not prereg_is_pristine():
        sys.exit(1)
    with open(PREREG, encoding="utf-8") as fh:
        reg = json.load(fh)

    run_dir = find_run(reg, sys.argv[1] if len(sys.argv) > 1 else None)
    if run_dir is None:
        print("no completed run carrying N=3..7 yet")
        return
    with open(os.path.join(run_dir, "result.json"), encoding="utf-8") as fh:
        run = json.load(fh)

    j = judge(reg, run)
    out = os.path.join(run_dir, "judgments-n67.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(j, fh, indent=2)

    print(f"=== {os.path.basename(run_dir)} (job "
          f"{(j.get('job') or {}).get('job_id')}) ===")
    print(f"  chain registered {j['chain_registered']}")
    print(f"  chain executed   {j['chain_executed']}  "
          f"-> {'MATCHES' if j['chain_matches'] else 'DRIFTED (predictions confounded)'}")
    print(f"\n  {'N':>2s} {'measured':>9s} {'M1 pred':>9s} {'z1':>7s} "
          f"{'M2 pred':>9s} {'z2':>7s}  closer")
    for N in reg["protocol"]["ns"]:
        a = j["T1_m1_depolarizing"]["series"][str(N)]
        b = j["T2_m2_cz_exponential"]["series"][str(N)]
        print(f"  {N:2d} {a['measured']:9.4f} {a['predicted']:9.4f} "
              f"{a['z']:+7.2f} {b['predicted']:9.4f} {b['z']:+7.2f}  "
              f"{j['T3_model_race']['per_N'][str(N)]['winner']}")
    print(f"\n  T1 M1 (depolarizing) at N=6,7 : "
          f"{j['T1_m1_depolarizing']['verdict']}")
    print(f"  T2 M2 (cz-exponential) at N=6,7: "
          f"{j['T2_m2_cz_exponential']['verdict']}")
    print(f"  T3 model race                  : "
          f"{j['T3_model_race']['verdict']} wins at N=6,7 "
          f"(agrees with existing ranking: "
          f"{j['T3_model_race']['agrees_with_existing_ranking']})")
    print(f"  T4 monotone decay in N         : "
          f"{j['T4_monotone_decay']['verdict']}")
    print(f"\n  wrote {os.path.relpath(out, REPO)}")


if __name__ == "__main__":
    main()
