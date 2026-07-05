"""T9 p=0.02 limit-cycle characterization (precise mode, fixed round budget).

The precise-mode reruns showed the two p=0.02 configs do not converge to a
fixed point: the best-response map settles into a payoff limit cycle (forward
order ~period 11, reverse ~period 6-7) with residual unilateral gains that
never approach 1e-4. Chasing a convergence cap adds no information, so this
harness runs a FIXED round budget sized to cover ~3 full periods and then
characterizes the cycle itself: detected period, time-averaged mean payoff and
spread over one clean steady-state period, and the min/max range each takes
within it.

Same provisional adaptation rule as scripts/t9_adaptation_pilot.py, reused
UNCHANGED via import (best_response_round / noisy_payoffs); precise optimizer
path throughout (the pilot's --fast path is never used).

Robustness: results.json is checkpointed after EVERY round (atomic replace),
so an interrupted run keeps everything up to the interruption. Designed to be
launched detached from any interactive session.

Run from repo root (entangled-equilibria env; -u so the log streams):
  python -u scripts/t9_cycle_characterize.py w 4 0.02 --rounds 35 --outdir OUT
  python -u scripts/t9_cycle_characterize.py w 4 0.02 --rounds 20 \
      --reverse-order --outdir OUT
  python scripts/t9_cycle_characterize.py --analyze OUT   # redo analysis only
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

import t9_adaptation_pilot as t9  # imports cpu_limit before numpy; rule reused as-is

import numpy as np  # noqa: E402

from circuits.ewl import q_strategy  # noqa: E402
from config import C, GAMMA, V  # noqa: E402
from experiment.topology_registry import canonical  # noqa: E402


def save_checkpoint(outdir, payload):
    """Atomic write so a kill mid-write never leaves a truncated results.json."""
    tmp = os.path.join(outdir, "results.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, os.path.join(outdir, "results.json"))


def detect_period(pay):
    """Smallest period P whose last two windows of P rounds match best.

    Compares the final P payoff vectors against the P before them for every
    candidate P; multiples of the true period also match, so among candidates
    within 25% of the best match residual the SMALLEST P wins.
    """
    R = len(pay)
    if R // 2 < 2:
        return None, {}
    scan = {}
    for P in range(2, R // 2 + 1):
        seg = pay[R - 2 * P:]
        scan[P] = float(np.mean(np.linalg.norm(seg[P:] - seg[:P], axis=1)))
    dmin = min(scan.values())
    period = min(P for P, d in scan.items() if d <= dmin * 1.25 + 1e-12)
    return period, scan


def characterize(history):
    """Cycle statistics over one full steady-state period (the final P rounds)."""
    pay = np.array([h["payoffs"] for h in history])
    period, scan = detect_period(pay)
    if period is None:
        return {"statement": "history too short to characterize a cycle"}
    cyc = pay[-period:]
    means = cyc.mean(axis=1)
    spreads = cyc.max(axis=1) - cyc.min(axis=1)
    gains = [h["max_gain"] for h in history[-period:]]
    return {
        "period": period,
        "period_match_residual": scan[period],
        "period_scan": {str(P): d for P, d in scan.items()},
        "analysis_rounds": [len(history) - period + 1, len(history)],
        "time_avg_mean": float(means.mean()),
        "mean_range": [float(means.min()), float(means.max())],
        "time_avg_spread": float(spreads.mean()),
        "spread_range": [float(spreads.min()), float(spreads.max())],
        "per_player_time_avg": cyc.mean(axis=0).tolist(),
        "residual_gain_range": [float(min(gains)), float(max(gains))],
        "statement": (f"does not converge to a fixed point; oscillates on a "
                      f"~period-{period} limit cycle"),
    }


def print_cycle_report(cycle):
    if "period" not in cycle:
        print(f"Cycle analysis: {cycle['statement']}")
        return
    print(f"Cycle analysis (one full period = rounds "
          f"{cycle['analysis_rounds'][0]}..{cycle['analysis_rounds'][1]}):")
    print(f"  {cycle['statement']}")
    print(f"  period match residual (L2, vs previous period): "
          f"{cycle['period_match_residual']:.2e}")
    print(f"  time-averaged mean payoff: {cycle['time_avg_mean']:.6f}  "
          f"(range within cycle: {cycle['mean_range'][0]:.6f} .. "
          f"{cycle['mean_range'][1]:.6f})")
    print(f"  time-averaged spread:      {cycle['time_avg_spread']:.6f}  "
          f"(range within cycle: {cycle['spread_range'][0]:.6f} .. "
          f"{cycle['spread_range'][1]:.6f})")
    print(f"  per-player time-averaged payoffs: "
          f"{np.round(cycle['per_player_time_avg'], 6)}")
    print(f"  residual unilateral gain over the period: "
          f"{cycle['residual_gain_range'][0]:.2e} .. "
          f"{cycle['residual_gain_range'][1]:.2e}")


def run(topology, N, p, rounds, outdir):
    print(f"=== T9 cycle characterization: topology={topology} N={N} p={p:g} "
          f"rounds={rounds} (V={V:g}, C={C:g}, gamma=pi/2, "
          f"reverse_order={t9.REVERSE_ORDER}) ===", flush=True)

    baseline = t9.noisy_payoffs([q_strategy(N)] * N, topology, N, p)
    mean_b, spread_b = float(baseline.mean()), float(baseline.max() - baseline.min())
    print(f"Baseline (fixed Q_{N}): {np.round(baseline, 6)}")
    print(f"  mean={mean_b:.6f}  spread={spread_b:.6f}")
    key = (canonical(topology), N, p)
    if key in t9.ANCHOR:
        ok = np.allclose(np.round(baseline, 4), t9.ANCHOR[key], atol=1e-3)
        msg = ("match" if ok else "MISMATCH -- baseline is not the reported "
               "finding, treat results as suspect")
        print(f"  anchor vs locked report: {msg}", flush=True)

    payload = {
        "config": {"topology": topology, "N": N, "ps": [p],
                   "V": V, "C": C, "gamma": GAMMA, "fast_mode": False,
                   "reverse_order": t9.REVERSE_ORDER,
                   "rounds_budget": rounds,
                   "purpose": "characterize the p=0.02 limit cycle; fixed round "
                              "budget (~3 periods), no convergence chase",
                   "rule": "independent round-robin best response (provisional)"},
        "status": "running",
        "completed_rounds": 0,
        "baseline": {"payoffs": baseline.tolist(), "mean": mean_b,
                     "spread": spread_b},
        "history": [],
    }
    save_checkpoint(outdir, payload)

    profile = [q_strategy(N)] * N
    for rnd in range(1, rounds + 1):
        profile, gain = t9.best_response_round(profile, topology, N, p, rnd == 1)
        payoffs = t9.noisy_payoffs(profile, topology, N, p)
        entry = {"round": rnd, "max_gain": gain,
                 "payoffs": payoffs.tolist(),
                 "mean": float(payoffs.mean()),
                 "spread": float(payoffs.max() - payoffs.min())}
        payload["history"].append(entry)
        payload["completed_rounds"] = rnd
        save_checkpoint(outdir, payload)
        print(f"  round {rnd:2d}: max_gain={gain:.3e}  mean={entry['mean']:.6f}  "
              f"spread={entry['spread']:.6f}", flush=True)

    payload["final_profile"] = [list(s) for s in profile]
    payload["cycle"] = characterize(payload["history"])
    payload["status"] = "complete"
    save_checkpoint(outdir, payload)
    print_cycle_report(payload["cycle"])
    print(f"\nSaved: {outdir}/results.json", flush=True)


def analyze_only(outdir):
    path = os.path.join(outdir, "results.json")
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    payload["cycle"] = characterize(payload["history"])
    save_checkpoint(outdir, payload)
    print(f"Re-analyzed {payload['completed_rounds']} rounds from {path}")
    print_cycle_report(payload["cycle"])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("topology", nargs="?", default="w")
    ap.add_argument("N", nargs="?", type=int, default=4)
    ap.add_argument("p", nargs="?", type=float, default=0.02)
    ap.add_argument("--rounds", type=int, default=35)
    ap.add_argument("--reverse-order", action="store_true")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--analyze", metavar="OUTDIR",
                    help="skip the run; recompute the cycle block for an "
                         "existing results.json")
    args = ap.parse_args()

    if args.analyze:
        analyze_only(args.analyze)
        return

    t9.FAST = False
    t9.REVERSE_ORDER = args.reverse_order
    outdir = args.outdir
    if outdir is None:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
        suffix = f"p{args.p:g}" + ("-rev" if args.reverse_order else "")
        outdir = os.path.join("results", "t9-pilot",
                              f"precise-cycle-{stamp}-{suffix}")
    os.makedirs(outdir, exist_ok=True)
    run(args.topology, args.N, args.p, args.rounds, outdir)


if __name__ == "__main__":
    main()
