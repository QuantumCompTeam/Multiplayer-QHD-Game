"""T9 pilot (rescoped): does adaptation restore per-player FAIRNESS, or only the mean?

Old T9 framing ("do players adapt strategies under noise?") is replaced by:
does letting each player adapt their strategy under gate-level noise collapse the
per-player payoff spread (fairness restored), rescue only the group mean while the
spread persists, or neither?

Adaptation rule (PROVISIONAL, modeling choice pending Aasa's sign-off):
independent best response -- round-robin over players in fixed order 0..N-1, each
player globally maximizes THEIR OWN expected noisy payoff over their own
(theta, alpha, beta), holding all other players fixed; iterate rounds until the
induced noisy probability vector stops moving (gauge-invariant, same criterion as
game.strategy_opt.nash_strategy) or the map is detected cycling. If it does not
converge, that is reported as-is, not forced.

Reuses the production paths validated by the Week-1 diagnostics unchanged:
  build_ewl_circuit_noisy (circuits/noise.py)  -- per-gate depolarizing payoffs
  expected_payoff        (game/payoffs.py)
  _maximize              (game/strategy_opt.py) -- multi-start NM + L-BFGS-B polish

The p=0.0 control column matters for interpretation: (Q,...,Q) is NOT a Nash
equilibrium for the W entangler even noiselessly, so adaptation will move at p=0
too. Only the DIFFERENCE between the p=0 adapted profile and the p>0 adapted
profiles is attributable to noise.

Additive pilot -- touches nothing in src/ and no Week-1 files.

Run from repo root (entangled-equilibria env):
  PYTHONPATH=src python scripts/t9_adaptation_pilot.py               # w 4, p in {0, 0.02, 0.05}
  PYTHONPATH=src python scripts/t9_adaptation_pilot.py ring 4 0.02   # topology N p [p ...]
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpu_limit  # noqa: E402,F401  (caps BLAS threads; MUST precede numpy import)

import numpy as np  # noqa: E402
from scipy.optimize import minimize  # noqa: E402

from circuits.ewl import DOVE, HAWK, StrategyParams, q_strategy  # noqa: E402
from circuits.noise import build_ewl_circuit_noisy  # noqa: E402
from config import C, GAMMA, V  # noqa: E402
from experiment.topology_registry import canonical  # noqa: E402
from game.payoffs import expected_payoff  # noqa: E402
from game.strategy_opt import _maximize  # noqa: E402

# Baseline anchors: results/noise-robustness/2026-07-03T0213Z report.md (4 dp).
ANCHOR = {
    ("w", 4, 0.0): [1.0, 1.0, 1.0, 1.0],
    ("w", 4, 0.02): [0.9898, 0.9756, 0.9768, 0.9772],
    ("w", 4, 0.05): [0.9675, 0.9627, 0.9535, 0.9536],
}

MAX_ROUNDS = 12
MAX_ROUNDS_FAST = 5
CONV_TOL = 1e-7   # induced-prob L2 delta + residual unilateral gain => converged
CONV_TOL_FAST = 1e-5  # matches the coarser optimizer resolution of --fast
STALL_LIMIT = 2   # rounds without delta improvement => cycling, stop honestly
FAIR_TOL = 1e-3   # spread below this counts as "fairness restored"

FAST = False  # set by the --fast CLI flag in main()
REVERSE_ORDER = False  # --reverse-order: round-robin N-1..0 instead of 0..N-1
# (confound check: does the post-adaptation advantage follow circuit position
# or move order?)


def _maximize_fast(objective, starts):
    """Coarse multi-start Nelder-Mead for --fast pilot runs.

    Same shape as game.strategy_opt._maximize but with looser tolerances, a
    shorter iteration budget, and no L-BFGS-B polish, so a full adaptation run
    fits in minutes. Precise (default) mode uses the shared _maximize.
    """
    neg = lambda x: -objective((float(x[0]), float(x[1]), float(x[2])))  # noqa: E731
    best_x, best_val = None, -np.inf
    for s0 in starts:
        res = minimize(neg, np.asarray(s0, dtype=float), method="Nelder-Mead",
                       options={"xatol": 1e-4, "fatol": 1e-8, "maxiter": 120})
        val = -float(res.fun)
        if val > best_val:
            best_val = val
            best_x = (float(res.x[0]), float(res.x[1]), float(res.x[2]))
    return best_x, best_val, True


def noisy_payoffs(profile, topology, N, p):
    probs = build_ewl_circuit_noisy(
        N, [tuple(s) for s in profile], topology=topology, gamma=GAMMA, p=p
    )
    return expected_payoff(probs, N, V, C)


def best_response_round(profile, topology, N, p, first_round):
    """One round-robin pass; returns (new profile, max unilateral gain seen)."""
    profile = [tuple(s) for s in profile]
    max_gain = 0.0
    order = range(N - 1, -1, -1) if REVERSE_ORDER else range(N)
    for i in order:
        def own_payoff(params: StrategyParams, _i=i):
            prof = list(profile)
            prof[_i] = tuple(params)
            return float(noisy_payoffs(prof, topology, N, p)[_i])

        anchors = [profile[i], q_strategy(N), DOVE, HAWK]
        starts = anchors if first_round else anchors[:2]
        old = own_payoff(profile[i])
        maximize = _maximize_fast if FAST else _maximize
        best_params, best_val, _ = maximize(own_payoff, starts)
        if best_val > old:
            max_gain = max(max_gain, best_val - old)
            profile[i] = tuple(best_params)
    return profile, max_gain


def adapt(topology, N, p):
    """Noisy best-response dynamics from the (Q_N,...,Q_N) baseline."""
    profile = [q_strategy(N)] * N
    prev_probs = build_ewl_circuit_noisy(
        N, profile, topology=topology, gamma=GAMMA, p=p
    )
    converged, best_delta, stalls, rounds, residual = False, float("inf"), 0, 0, None
    max_rounds = MAX_ROUNDS_FAST if FAST else MAX_ROUNDS
    conv_tol = CONV_TOL_FAST if FAST else CONV_TOL
    history = []
    for rnd in range(1, max_rounds + 1):
        rounds = rnd
        profile, gain = best_response_round(profile, topology, N, p, rnd == 1)
        probs = build_ewl_circuit_noisy(
            N, profile, topology=topology, gamma=GAMMA, p=p
        )
        delta = float(np.linalg.norm(probs - prev_probs))
        prev_probs = probs
        residual = gain
        history.append(
            {"round": rnd, "max_gain": gain, "prob_delta": delta,
             "payoffs": noisy_payoffs(profile, topology, N, p).tolist()}
        )
        if delta < conv_tol and gain < conv_tol:
            converged = True
            break
        if delta < best_delta - 1e-9:
            best_delta, stalls = delta, 0
        else:
            stalls += 1
            if stalls >= STALL_LIMIT:
                break  # cycling, not settling -- report honestly
    return profile, converged, rounds, residual, history


def classify(mean_b, spread_b, mean_a, spread_a):
    if spread_a < FAIR_TOL:
        if mean_a < mean_b - 1e-6:
            return ("FAIRNESS RESTORED -- BUT EQUALIZED DOWNWARD "
                    "(spread ~0 at a LOWER mean than baseline)")
        return "FAIRNESS RESTORED (spread ~0, mean not sacrificed)"
    if mean_a > mean_b + 1e-6:
        return "MEAN RESCUED, SPREAD PERSISTS (unfairness survives adaptation)"
    return "NEITHER (mean not improved and spread persists)"


def run_config(topology, N, p):
    print(f"\n=== T9 pilot: topology={topology} N={N} p={p:g} "
          f"(V={V:g}, C={C:g}, gamma=pi/2) ===")

    baseline = noisy_payoffs([q_strategy(N)] * N, topology, N, p)
    mean_b, spread_b = float(baseline.mean()), float(baseline.max() - baseline.min())
    print(f"Baseline (fixed Q_{N}): {np.round(baseline, 6)}")
    print(f"  mean={mean_b:.6f}  spread={spread_b:.6f}")
    key = (canonical(topology), N, p)
    if key in ANCHOR:
        ok = np.allclose(np.round(baseline, 4), ANCHOR[key], atol=1e-3)
        msg = ("match" if ok else "MISMATCH -- baseline is not the reported "
               "finding, treat results as suspect")
        print(f"  anchor vs locked report: {msg}")

    profile, converged, rounds, residual, history = adapt(topology, N, p)
    adapted = noisy_payoffs(profile, topology, N, p)
    mean_a, spread_a = float(adapted.mean()), float(adapted.max() - adapted.min())

    status = "converged" if converged else "DID NOT CONVERGE (cycling/cap)"
    print(f"Adapted (independent best response, provisional rule): {status} "
          f"after {rounds} round(s); residual max unilateral gain={residual:.2e}")
    print(f"  {np.round(adapted, 6)}")
    print(f"  mean={mean_a:.6f}  spread={spread_a:.6f}")
    for i, s in enumerate(profile):
        print(f"  player {i}: theta={s[0]:+.4f}  alpha={s[1]:+.4f}  beta={s[2]:+.4f}")
    still = [i for i in range(N) if adapted[i] < adapted.max() - FAIR_TOL]
    print(f"  players still disadvantaged (> {FAIR_TOL:g} below best): "
          f"{still if still else 'none'}")

    verdict = classify(mean_b, spread_b, mean_a, spread_a)
    if not converged:
        verdict += " [caveat: dynamics did not converge -- endpoint is a snapshot]"
    print(f"Flag: {verdict}")
    print(f"  mean {mean_b:.4f} -> {mean_a:.4f}  |  spread {spread_b:.4f} -> {spread_a:.4f}")

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
    global FAST, REVERSE_ORDER
    flags = {"--fast", "--reverse-order"}
    args = [a for a in sys.argv[1:] if a not in flags]
    FAST = "--fast" in sys.argv[1:]
    REVERSE_ORDER = "--reverse-order" in sys.argv[1:]
    if REVERSE_ORDER:
        print("[reverse-order mode: round-robin N-1..0 -- move-order confound check]")
    if FAST:
        print("[fast mode: coarse optimizer tolerances, round cap "
              f"{MAX_ROUNDS_FAST} -- pilot resolution, rerun precise to publish]")
    topology = args[0] if len(args) > 0 else "w"
    N = int(args[1]) if len(args) > 1 else 4
    ps = [float(a) for a in args[2:]] or [0.0, 0.02, 0.05]

    results = [run_config(topology, N, p) for p in ps]

    print("\n=== SUMMARY ===")
    for r in results:
        print(f"p={r['p']:g}: {r['flag']}")
        b, a = r["baseline"], r["adapted"]
        print(f"  mean {b['mean']:.4f} -> {a['mean']:.4f}   "
              f"spread {b['spread']:.4f} -> {a['spread']:.4f}   "
              f"(converged={a['converged']}, rounds={a['rounds']})")
    print("\nNOTE: adaptation rule (independent round-robin best response) is a "
          "provisional modeling choice pending Aasa's review; p=0 column is the "
          "no-noise control (Q_N is not a W-entangler equilibrium even at p=0).")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    outdir = os.path.join("results", "t9-pilot", stamp)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "results.json"), "w", encoding="utf-8") as f:
        json.dump({"config": {"topology": topology, "N": N, "ps": ps,
                              "V": V, "C": C, "gamma": GAMMA, "fast_mode": FAST,
                              "reverse_order": REVERSE_ORDER,
                              "rule": "independent round-robin best response "
                                      "(provisional)"},
                   "results": results}, f, indent=2)
    print(f"\nSaved: {outdir}/results.json")


if __name__ == "__main__":
    main()
