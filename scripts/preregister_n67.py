"""Freeze the N=6,7 scaling predictions BEFORE the extended batch is submitted.

Writes results/hardware-scaling/preregistration-n67.json. This is a NEW file:
results/hardware-scaling/preregistration.json and preregistration-baselines.json
are FROZEN and are never touched here -- new claims get new registration files.

Same fit-one-predict-many protocol as the original registration, extended to
N=6,7, and it registers TWO competing models rather than one:

  M1 depolarizing p_eff   The primary model. Fit ONE depolarizing p on the
                          anchor run's N=3 mitigated fold-1 payoff (40-step
                          bisection, circuits.noise, GHZ, {u,cx} basis), then
                          predict N=6,7 with no N>3 information used.
  M2 cz-exponential       advantage_N = ideal_N * r^cz_N, with the single
                          parameter r = (A3/ideal_3)^(1/cz_3) fit on the same
                          N=3 anchor. Registered because it currently OUTSCORES
                          M1 in results/hardware-scaling/repeat-judgments.json,
                          and N=6,7 is where the two separate most.

The two models agree at N=3 by construction and diverge as cz grows, so the
extension is a genuine discriminator rather than a confirmation exercise.

The chain is pinned into the registration and must be held at submission with
`--chain`. Topology run 1 (job d9ia1pd0k0jc738jaqgg) was registered on one
qubit set and executed on another after a mid-day recalibration, which made its
per-cell predictions untestable; M2's predictions depend on the routed cz
counts, so the same drift would break them here.

Usage (pinned env):
  conda run -n entangled-equilibria python scripts/preregister_n67.py \
      --chain 97,107,108,109,110,111,98

Refuses to overwrite an existing registration.
"""

import argparse
import glob
import json
import math
import os
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "experiments"))

import numpy as np  # noqa: E402

from hardware_scaling import (  # noqa: E402
    DEFAULT_BACKEND,
    FOLDS,
    build_ewl_gate_circuit,
    environment_provenance,
    git_provenance,
    load_service,
    validate_chain,
)
from circuits.ewl import q_strategy  # noqa: E402
from circuits.noise import build_ewl_circuit_noisy  # noqa: E402
from game.nash import compute_advantage  # noqa: E402
from game.payoffs import expected_payoff  # noqa: E402
from qiskit.transpiler.preset_passmanagers import (  # noqa: E402
    generate_preset_pass_manager,
)

OUT = os.path.join(REPO, "results", "hardware-scaling", "preregistration-n67.json")
HW_DIR = os.path.join(REPO, "results", "hardware-scaling")
NS_EXT = (3, 4, 5, 6, 7)
NEW_NS = (6, 7)
REGISTERED_SHOTS = 4096
Z_CRIT = 1.96
SEED_TRANSPILER = None  # hardware_scaling transpiles without a seed; see note


def latest_run() -> tuple[str, dict]:
    """The most recent completed scaling run -- the fit anchor."""
    runs = sorted(glob.glob(os.path.join(HW_DIR, "2026-*")))
    for d in reversed(runs):
        path = os.path.join(d, "result.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return d, json.load(fh)
    print("ERROR: no completed scaling run to anchor on")
    sys.exit(1)


def q_payoff(N: int, p: float) -> float:
    probs = build_ewl_circuit_noisy(N, [q_strategy(N)] * N, topology="ghz", p=p)
    return float(np.mean(expected_payoff(probs, N)))


def fit_p_eff(target_payoff: float) -> float:
    """The registered 40-step bisection, identical to hardware_scaling's."""
    lo, hi = 0.0, 0.10
    if q_payoff(3, lo) < target_payoff:
        return 0.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if q_payoff(3, mid) > target_payoff:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def measure_cz(backend, chain: list[int], ns) -> dict[int, int]:
    """Routed fold-1 cz per N on the pinned chain -- M2's dose variable."""
    out = {}
    for N in ns:
        pm = generate_preset_pass_manager(
            backend=backend, optimization_level=3, initial_layout=chain[:N])
        isa = pm.run(build_ewl_gate_circuit(N))
        fil = list(isa.layout.final_index_layout())
        if not set(fil) <= set(chain):
            print(f"ERROR: N={N} layout escaped the chain: {fil}")
            sys.exit(1)
        out[N] = isa.count_ops().get("cz", 0)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--backend", default=DEFAULT_BACKEND)
    ap.add_argument("--chain", required=True, metavar="Q0,...,Q6",
                    help="the 7-qubit chain to register AND to submit on")
    args = ap.parse_args()

    if os.path.exists(OUT):
        print(f"REFUSING to overwrite {os.path.relpath(OUT)} -- a registration "
              f"is frozen once written.")
        sys.exit(1)

    chain = [int(x) for x in args.chain.replace(" ", "").split(",") if x]
    backend = load_service().backend(args.backend)
    try:
        validate_chain(backend.coupling_map.get_edges(), chain, len(chain))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(2)
    if len(chain) < max(NS_EXT):
        print(f"ERROR: chain of {len(chain)} is shorter than max N {max(NS_EXT)}")
        sys.exit(2)

    anchor_dir, anchor = latest_run()
    a3_payoff = anchor["analysis"]["series"]["3"]["folds"]["1"]["mitigated"]["mean"]
    ideal = {N: compute_advantage(N=N)["advantage"] for N in NS_EXT}
    classical = {N: compute_advantage(N=N)["classical_ne_payoff"] for N in NS_EXT}
    a3_adv = a3_payoff - classical[3]

    cz = measure_cz(backend, chain, NS_EXT)

    # ── M1: one depolarizing p fitted at N=3 ─────────────────────────────────
    p_eff = fit_p_eff(a3_payoff)
    m1 = {N: q_payoff(N, p_eff) - classical[N] for N in NS_EXT}

    # ── M2: one retention r fitted at N=3, dosed by routed cz ────────────────
    r = (a3_adv / ideal[3]) ** (1.0 / cz[3])
    m2 = {N: ideal[N] * r ** cz[N] for N in NS_EXT}

    # Shot-noise sigma at the registered shot count, from the M1 predicted
    # distribution. Device-model error is NOT included -- see below.
    sigma = {}
    for N in NS_EXT:
        probs = build_ewl_circuit_noisy(N, [q_strategy(N)] * N,
                                        topology="ghz", p=p_eff)
        cbar = np.array([float(np.mean(expected_payoff(
            np.eye(2**N)[i], N))) for i in range(2**N)])
        mean = float(np.sum(probs * cbar))
        var = float(np.sum(probs * cbar**2) - mean**2)
        sigma[N] = float(np.sqrt(max(var, 0.0) / REGISTERED_SHOTS))

    reg = {
        "registered_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Frozen N=6,7 extension of the scaling curve (item 4), registered "
            "before the extended batch was submitted. TWO competing "
            "one-parameter models, both fit on the SAME N=3 anchor and both "
            "extrapolated with no N>3 information. Judged after the run."),
        "does_not_supersede": [
            "results/hardware-scaling/preregistration.json",
            "results/hardware-scaling/preregistration-baselines.json",
        ],
        "backend": args.backend,
        "git": git_provenance(),
        "environment": environment_provenance(),
        "anchor_run": {
            "dir": os.path.relpath(anchor_dir, REPO).replace("\\", "/"),
            "job_id": anchor.get("job", {}).get("job_id"),
            "created_utc": anchor.get("created_utc"),
            "n3_mitigated_fold1_payoff": a3_payoff,
            "n3_mitigated_fold1_advantage": a3_adv,
        },
        "protocol": {
            "ns": list(NS_EXT),
            "new_ns": list(NEW_NS),
            "folds": list(FOLDS),
            "chain": chain,
            "chain_len": len(chain),
            "n_pubs": 2 + len(NS_EXT) * len(FOLDS),
            "shots_registered": REGISTERED_SHOTS,
            "z_crit": Z_CRIT,
            "routed_cz_fold1": {str(N): cz[N] for N in NS_EXT},
            "submit_with": (
                f"conda run -n entangled-equilibria python "
                f"experiments/hardware_scaling.py --hardware --ns "
                f"{','.join(map(str, NS_EXT))} --chain {','.join(map(str, chain))}"),
            "recover_with": (
                f"--from-job <id> --ns {','.join(map(str, NS_EXT))}"),
            "chain_must_be_held": (
                "The chain above is part of the registration. M2's predictions "
                "are dosed by routed cz, which depends on the chain, so the "
                "submission MUST pass --chain. Topology run 1 "
                "(d9ia1pd0k0jc738jaqgg) was registered on [20,21,22,23,24] and "
                "executed on [137,147,146,145,144] after a mid-day "
                "recalibration; its per-cell predictions were untestable as a "
                "result. Do not repeat that here."),
            "uncertainties_propagated": [
                "multinomial shot noise at 4096 shots on the M1 predicted "
                "distribution",
            ],
            "uncertainties_excluded": [
                "device-model error: the DOMINANT unmodelled term. The nine "
                "GHZ points in results/hardware-scaling/ show the Aer device "
                "model over-predicting advantage 9 times out of 9. Both M1 and "
                "M2 are fit on a MEASURED N=3 point rather than on the device "
                "model, so they are less exposed than a raw device-model "
                "prediction, but neither is immune.",
                "calibration drift between registration and execution",
                "transpiler non-determinism: hardware_scaling transpiles "
                "without seed_transpiler, so routed cz could differ on a "
                "re-transpile. The registered cz counts above are what the "
                "judge must compare against.",
            ],
            "registered_tests": {
                "T1_m1_depolarizing": (
                    "Measured mitigated fold-1 advantage at N=6 and N=7 vs M1; "
                    "PASS iff |z| <= 1.96."),
                "T2_m2_cz_exponential": (
                    "Same measurement vs M2; PASS iff |z| <= 1.96."),
                "T3_model_race": (
                    "Which model has the smaller |measured - predicted| at "
                    "N=6 and N=7, and does the winner AGREE with the ranking "
                    "the N=4,5 repeats already produced? M2 currently "
                    "outscores M1 there. If M2 wins again at the two largest "
                    "N, the cz-dose description of this device is supported "
                    "over the fitted-depolarizing one; if it loses, the "
                    "existing ranking does not extrapolate and the paper must "
                    "say so."),
                "T4_monotone_decay": (
                    "Measured advantage is strictly decreasing in N across "
                    "3,4,5,6,7. A non-monotone curve would indicate the chain "
                    "is not uniform in quality and the scaling read is "
                    "confounded by qubit selection rather than by N."),
            },
        },
        "ideal_advantage": {str(N): ideal[N] for N in NS_EXT},
        "classical_ne_payoff": {str(N): classical[N] for N in NS_EXT},
        "M1_depolarizing": {
            "p_eff": p_eff,
            "fit_on": "N=3 mitigated fold-1 payoff of the anchor run",
            "advantage": {str(N): m1[N] for N in NS_EXT},
            "sigma_predictive": {str(N): sigma[N] for N in NS_EXT},
        },
        "M2_cz_exponential": {
            "r": r,
            "form": "advantage_N = ideal_N * r ** routed_cz_fold1_N",
            "fit_on": "N=3 mitigated fold-1 advantage of the anchor run",
            "advantage": {str(N): m2[N] for N in NS_EXT},
            "sigma_predictive": {str(N): sigma[N] for N in NS_EXT},
        },
        "separation": {
            str(N): {"m1_minus_m2": m1[N] - m2[N],
                     "in_sigmas": (m1[N] - m2[N]) / sigma[N]}
            for N in NS_EXT
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=2)

    print("\n" + "=" * 74)
    print("REGISTERED N=6,7 PREDICTIONS (frozen)")
    print("=" * 74)
    print(f"anchor run: {reg['anchor_run']['dir']} "
          f"(job {reg['anchor_run']['job_id']})")
    print(f"  N=3 mitigated fold-1 advantage = {a3_adv:.6f}")
    print(f"chain: {chain}")
    print(f"p_eff = {p_eff:.6f}   r = {r:.6f}\n")
    print(f"  {'N':>2s} {'cz':>3s} {'ideal':>8s} {'M1 depol':>9s} "
          f"{'M2 cz-exp':>10s} {'M1-M2':>8s} {'sigma':>7s} {'sep':>7s}")
    for N in NS_EXT:
        sep = (m1[N] - m2[N]) / sigma[N]
        mark = "  <- NEW" if N in NEW_NS else ""
        print(f"  {N:2d} {cz[N]:3d} {ideal[N]:8.4f} {m1[N]:9.4f} "
              f"{m2[N]:10.4f} {m1[N] - m2[N]:8.4f} {sigma[N]:7.4f} "
              f"{sep:6.1f}s{mark}")
    print(f"\nwrote {os.path.relpath(OUT)}")
    print(f"submit with:\n  {reg['protocol']['submit_with']}")


if __name__ == "__main__":
    main()
