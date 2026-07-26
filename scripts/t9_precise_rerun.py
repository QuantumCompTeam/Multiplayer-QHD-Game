"""T9 precise-mode rerun harness (one config per invocation).

Same adaptation rule as scripts/t9_adaptation_pilot.py -- independent round-robin
best response, still provisional pending Aasa's review -- reused UNCHANGED via
import (best_response_round / noisy_payoffs / classify). Only the stopping rule
differs from the pilot:

  converged  <=>  a full round-robin pass yields residual max unilateral gain
                  below GAIN_TOL (1e-4, "near-zero")
  cap        =    MAX_ROUNDS (50, generous); hitting it is reported plainly as
                  non-convergence, never forced into a converged number

Precise optimizer resolution throughout (the pilot's --fast path is never used).

Run from repo root (one process per config; single-threaded via cpu_limit, so
configs can run in parallel):
  python scripts/t9_precise_rerun.py w 4 0.00
  python scripts/t9_precise_rerun.py w 4 0.02
  python scripts/t9_precise_rerun.py w 4 0.02 --reverse-order
  python scripts/t9_precise_rerun.py w 4 0.05

Saves results/t9-pilot/precise-<UTC stamp>-<topology><N>-p<p>[-rev][-simul]/
results.json, same schema as the fast-mode pilot runs plus the stopping-rule
fields. Directories written before 2026-07-26 omit the <topology><N> segment;
all of those are w4.
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

import t9_adaptation_pilot as t9  # imports cpu_limit before numpy; rule reused as-is

import numpy as np  # noqa: E402

from circuits.ewl import q_strategy  # noqa: E402
from circuits.noise import build_ewl_circuit_noisy  # noqa: E402
from config import C, GAMMA, V  # noqa: E402
from experiment.topology_registry import canonical  # noqa: E402

GAIN_TOL = 1e-4  # residual unilateral gain below this after a full pass => converged
MAX_ROUNDS = 50  # generous cap; reaching it => honest non-convergence
# --rounds overrides it. Reaching the cap is reported as non-convergence
# either way, so a smaller budget can only ever UNDER-claim convergence.


def adapt_precise(topology, N, p):
    """t9 best-response dynamics from (Q_N,...,Q_N), gain-based stopping rule."""
    profile = [q_strategy(N)] * N
    prev_probs = build_ewl_circuit_noisy(
        N, profile, topology=topology, gamma=GAMMA, p=p
    )
    converged, rounds, residual = False, 0, None
    history = []
    for rnd in range(1, MAX_ROUNDS + 1):
        rounds = rnd
        profile, gain = t9.br_round(profile, topology, N, p, rnd == 1)
        probs = build_ewl_circuit_noisy(
            N, profile, topology=topology, gamma=GAMMA, p=p
        )
        delta = float(np.linalg.norm(probs - prev_probs))
        prev_probs = probs
        residual = gain
        history.append(
            {"round": rnd, "max_gain": gain, "prob_delta": delta,
             "payoffs": t9.noisy_payoffs(profile, topology, N, p).tolist()}
        )
        print(f"  round {rnd:2d}: max_gain={gain:.3e}  prob_delta={delta:.3e}",
              flush=True)
        if gain < GAIN_TOL:
            converged = True
            break
    return profile, converged, rounds, residual, history


def run_config(topology, N, p):
    print(f"=== T9 precise rerun: topology={topology} N={N} p={p:g} "
          f"(V={V:g}, C={C:g}, gamma=pi/2, rule={t9.RULE}, "
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

    profile, converged, rounds, residual, history = adapt_precise(topology, N, p)
    adapted = t9.noisy_payoffs(profile, topology, N, p)
    mean_a, spread_a = float(adapted.mean()), float(adapted.max() - adapted.min())

    status = ("converged" if converged
              else f"DID NOT CONVERGE (residual gain still >= {GAIN_TOL:g} "
                   f"at the {MAX_ROUNDS}-round cap)")
    print(f"Adapted ({t9.RULE} best response, provisional rule): {status} "
          f"after {rounds} round(s); residual max unilateral gain={residual:.2e}")
    print(f"  {np.round(adapted, 6)}")
    print(f"  mean={mean_a:.6f}  spread={spread_a:.6f}")
    for i, s in enumerate(profile):
        print(f"  player {i}: theta={s[0]:+.4f}  alpha={s[1]:+.4f}  beta={s[2]:+.4f}")
    still = [i for i in range(N) if adapted[i] < adapted.max() - t9.FAIR_TOL]
    print(f"  players still disadvantaged (> {t9.FAIR_TOL:g} below best): "
          f"{still if still else 'none'}")

    verdict = t9.classify(mean_b, spread_b, mean_a, spread_a)
    if not converged:
        verdict += " [caveat: dynamics did not converge -- endpoint is a snapshot]"
    print(f"Flag: {verdict}")
    print(f"  mean {mean_b:.4f} -> {mean_a:.4f}  |  "
          f"spread {spread_b:.4f} -> {spread_a:.4f}", flush=True)

    return {
        "topology": topology, "N": N, "p": p,
        "baseline": {"payoffs": baseline.tolist(), "mean": mean_b, "spread": spread_b},
        "adapted": {"payoffs": adapted.tolist(), "mean": mean_a, "spread": spread_a,
                    "profile": [list(s) for s in profile], "converged": converged,
                    "rounds": rounds, "residual_gain": residual},
        "history": history,
        "flag": verdict,
    }


def main():
    raw = sys.argv[1:]
    t9.FAST = False
    t9.REVERSE_ORDER = "--reverse-order" in raw
    global MAX_ROUNDS
    if "--rounds" in raw:
        i = raw.index("--rounds")
        if i + 1 >= len(raw):
            sys.exit("--rounds needs a value")
        MAX_ROUNDS = int(raw[i + 1])
        raw = raw[:i] + raw[i + 2:]
    if "--rule" in raw:
        i = raw.index("--rule")
        if i + 1 >= len(raw):
            sys.exit("--rule needs a value: round-robin | simultaneous")
        t9.RULE = raw[i + 1]
        if t9.RULE not in ("round-robin", "simultaneous"):
            sys.exit(f"unknown --rule {t9.RULE!r}")
        raw = raw[:i] + raw[i + 2:]      # strip the flag AND its value
    args = [a for a in raw if a != "--reverse-order"]
    topology = args[0] if len(args) > 0 else "w"
    N = int(args[1]) if len(args) > 1 else 4
    if len(args) != 3:
        sys.exit("usage: t9_precise_rerun.py TOPOLOGY N P [--reverse-order] "
                 "[--rule round-robin|simultaneous] [--rounds K]")
    p = float(args[2])

    result = run_config(topology, N, p)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    # Topology and N stayed out of this name while every run was W N=4. Caveat 2
    # adds ring and N=5, so two configs finishing in the same UTC minute would
    # otherwise resolve to an identical path and the second would overwrite the
    # first. Directories written before this change keep their old names.
    suffix = (f"{topology}{N}-p{p:g}" + ("-rev" if t9.REVERSE_ORDER else "")
              + ("-simul" if t9.RULE == "simultaneous" else ""))
    outdir = os.path.join("results", "t9-pilot", f"precise-{stamp}-{suffix}")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "results.json"), "w", encoding="utf-8") as f:
        json.dump({"config": {"topology": topology, "N": N, "ps": [p],
                              "V": V, "C": C, "gamma": GAMMA, "fast_mode": False,
                              "reverse_order": t9.REVERSE_ORDER,
                              # One key each. This dict previously carried TWO
                              # "rule" entries and TWO "max_rounds" entries; the
                              # later literal silently won, so every artifact
                              # claimed round-robin regardless of what ran.
                              "rule": t9.RULE,
                              "rule_note": ("independent best response, "
                                            "provisional pending review"),
                              "max_rounds": MAX_ROUNDS,
                              "gain_tol": GAIN_TOL,
                              "stopping_rule": "converged when a full pass has "
                                               "max unilateral gain < gain_tol; "
                                               "else stop at max_rounds and "
                                               "report non-convergence"},
                   "results": [result]}, f, indent=2)
    print(f"\nSaved: {outdir}/results.json")


if __name__ == "__main__":
    main()
