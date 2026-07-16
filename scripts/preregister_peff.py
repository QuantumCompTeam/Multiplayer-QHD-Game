"""Pre-register the effective-p scaling prediction BEFORE any repeat runs.

Freezes, from the single 2026-07-16 hardware-scaling run (ibm_fez job
d9c8fpn550hc73dl1tcg), the one-parameter depolarizing fit p_eff (fitted on the
N=3 mitigated fold-1 payoff ONLY -- fit-one-predict-two) and its predicted
advantages at N=3,4,5, with uncertainty intervals propagated through every
statistical stage of the pipeline. Committing this output before the repeat
batch runs (TODOS.md) turns them into a falsifiable test of the model instead
of post-hoc curve confirmation.

Uncertainty budget (ONE joint parametric bootstrap, seeded):
  shot        multinomial resampling of every series pub's 4096-shot counts
  mitigation  binomial resampling of the per-qubit confusion-matrix entries
              (cal pubs were 4096 shots; the raw cal counts are not persisted
              in result.json, so the stored per-qubit e0/e1 are resampled
              parametrically -- consistent with the tensored readout model)
  fit         p_eff re-fitted per replicate by inverting the model curve
  ZNE         the weighted-linear extrapolation re-run per replicate
Excluded (see the registration doc): model-form error and cross-day
calibration drift. Drift is handled by the registered CONDITIONAL test:
refit p_eff on each repeat run's own N=3, judge that run's N=4,5 against it.

Verification gates (all must pass before anything is written):
  G1  re-running the production fit reproduces the stored p_eff exactly;
  G2  the bootstrap pipeline, fed the ACTUAL counts/matrices, reproduces the
      stored mitigated payoffs and ZNE intercepts (production code path);
  G3  the interpolated model curve matches the exact simulator at p_eff.

Usage (pinned hardware env -- the env that produced the run):
  conda run -n entangled-equilibria python scripts/preregister_peff.py

Writes results/hardware-scaling/preregistration.json (canonical numbers).
"""

import json
import os
import platform
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "experiments"))

import numpy as np
from scipy.interpolate import PchipInterpolator

from hardware_scaling import effective_p_prediction, payoff_stats
from circuits.ewl import q_strategy
from circuits.noise import build_ewl_circuit_noisy
from game.nash import compute_advantage
from game.payoffs import expected_payoff
from hardware.mitigation import counts_to_probs, mitigate_probs, zne_extrapolate

RUN_DIR = os.path.join(REPO, "results", "hardware-scaling", "2026-07-16T074134Z")
OUT_PATH = os.path.join(REPO, "results", "hardware-scaling", "preregistration.json")
NS = (3, 4, 5)
FOLDS = (1, 3, 5)
SEED = 20260716
B = 2000
P_GRID = np.linspace(0.0, 0.005, 41)  # covers p_eff +/- ~10 sigma


# ── model curve: payoff vs p, per (N, cz-fold) ─────────────────────────────────


def fold_ratio(p: float, fold: int) -> float:
    """cz-fold f == the 2q depolarizing channel applied f times per cz site:
    exact composition p2 = 1-(1-p)^f, expressed as p2_ratio for the Month-4
    noise model. 1q `u` errors are NOT folded (hardware folds only cz)."""
    if fold == 1 or p == 0.0:
        return 1.0
    return (1.0 - (1.0 - p) ** fold) / p


def model_probs(N: int, p: float, fold: int) -> np.ndarray:
    probs = build_ewl_circuit_noisy(
        N, [q_strategy(N)] * N, topology="ghz", p=p, p2_ratio=fold_ratio(p, fold)
    )
    return probs / probs.sum()  # density-matrix trace drift ~1e-9


# ── fast payoff stats (bit-compatible with payoff_stats, precomputed cbar) ─────


def make_cbar(N: int) -> tuple[np.ndarray, np.ndarray]:
    cbar = np.empty(2**N)
    for i in range(2**N):
        v = np.zeros(2**N)
        v[i] = 1.0
        cbar[i] = float(np.mean(expected_payoff(v, N)))
    return cbar, cbar**2


def fast_stats(probs: np.ndarray, cbar: np.ndarray, cbar2: np.ndarray,
               shots: int) -> tuple[float, float]:
    mean = float(probs @ cbar)
    var = float(probs @ cbar2) - mean**2
    return mean, float(np.sqrt(max(var, 0.0) / shots))


# ── verification gates ─────────────────────────────────────────────────────────


def gate(ok: bool, label: str, detail: str = "") -> None:
    print(f"  {label}: {'PASS' if ok else 'FAIL'} {detail}")
    if not ok:
        sys.exit(1)


def main() -> None:
    res = json.load(open(os.path.join(RUN_DIR, "result.json"), encoding="utf-8"))
    shots = res["shots"]
    ana = res["analysis"]
    stored = res["predictions"]["effective_p"]
    measured_n3 = ana["series"]["3"]["folds"]["1"]["mitigated"]["mean"]
    refs = {N: compute_advantage(N=N) for N in NS}
    mats_by_phys = {q: np.array(m) for q, m in ana["confusion_matrices"].items()}
    fil = {N: ana["series"][str(N)]["fil"] for N in NS}
    p_emp = {(N, f): counts_to_probs(
        ana["series"][str(N)]["folds"][str(f)]["counts"], N)
        for N in NS for f in FOLDS}
    cbars = {N: make_cbar(N) for N in NS}

    # G1: the production fit, re-run, reproduces the stored p_eff exactly.
    print("=== verification gates ===")
    central = effective_p_prediction(measured_n3, refs)
    p_eff = central["p_eff"]
    gate(abs(p_eff - stored["p_eff"]) < 1e-15, "G1 p_eff reproduction",
         f"(refit {p_eff!r} vs stored {stored['p_eff']!r})")

    # G2: production mitigation + ZNE path on the ACTUAL counts reproduces
    # every stored mitigated payoff and ZNE intercept.
    worst = 0.0
    for N in NS:
        mats = [mats_by_phys[str(q)] for q in fil[N]]
        means, sigmas = [], []
        for f in FOLDS:
            s = payoff_stats(mitigate_probs(p_emp[(N, f)], mats), N, shots)
            st = ana["series"][str(N)]["folds"][str(f)]["mitigated"]
            worst = max(worst, abs(s["mean"] - st["mean"]),
                        abs(s["sigma"] - st["sigma"]))
            means.append(s["mean"])
            sigmas.append(max(s["sigma"], 1e-9))
            m_fast, s_fast = fast_stats(mitigate_probs(p_emp[(N, f)], mats),
                                        *cbars[N], shots)
            worst = max(worst, abs(m_fast - s["mean"]), abs(s_fast - s["sigma"]))
        zne = zne_extrapolate(list(FOLDS), means, sigmas)
        worst = max(worst, abs(zne["linear"] - ana["series"][str(N)]["zne"]["linear"]))
    gate(worst < 1e-9, "G2 pipeline reproduction", f"(worst |delta| {worst:.2e})")

    # model curves on the p grid (exact sims), PCHIP interpolants
    print("=== model curves (density-matrix sims on the p grid) ===")
    curve = {}
    for N in NS:
        for f in FOLDS:
            pays = np.array([fast_stats(model_probs(N, p, f), *cbars[N], shots)[0]
                             for p in P_GRID])
            assert np.all(np.diff(pays) < 0), f"payoff not monotone (N={N},f={f})"
            curve[(N, f)] = PchipInterpolator(P_GRID, pays)
        print(f"  N={N}: folds {FOLDS} done")
    inv31 = PchipInterpolator(curve[(3, 1)](P_GRID)[::-1], P_GRID[::-1])

    # G3: interpolation error at the fitted point
    e_curve = abs(float(curve[(3, 1)](p_eff)) - measured_n3)
    e_inv = abs(float(inv31(measured_n3)) - p_eff)
    gate(e_curve < 1e-7 and e_inv < 1e-7, "G3 interpolation",
         f"(|curve| {e_curve:.1e}, |inverse p| {e_inv:.1e})")

    # registered central numbers: fold-1 from the production fit; ZNE from the
    # model fold series at p_eff through the production extrapolator, weighted
    # by the same 4096-shot sigmas the analysis pipeline uses.
    central_zne, zne_weights = {}, {}
    for N in NS:
        means, sigmas = [], []
        for f in FOLDS:
            m, s = fast_stats(model_probs(N, p_eff, f), *cbars[N], shots)
            means.append(m)
            sigmas.append(max(s, 1e-9))
        central_zne[N] = zne_extrapolate(list(FOLDS), means, sigmas)["linear"]
        zne_weights[N] = sigmas

    # ── joint parametric bootstrap ────────────────────────────────────────────
    print(f"=== bootstrap: B={B}, seed={SEED} ===")
    rng = np.random.default_rng(SEED)
    chain = [str(q) for q in ana["chain"]]
    e01 = {q: (float(mats_by_phys[q][1, 0]), float(mats_by_phys[q][0, 1]))
           for q in chain}
    p_star_all = np.empty(B)
    meas_f1 = {N: np.empty(B) for N in NS}
    meas_zne = {N: np.empty(B) for N in NS}
    model_f1 = {N: np.empty(B) for N in NS}
    model_zne = {N: np.empty(B) for N in NS}
    clipped = 0
    for b in range(B):
        mats_star = {}
        for q in chain:
            e0, e1 = e01[q]
            e0s = rng.binomial(shots, e0) / shots
            e1s = rng.binomial(shots, e1) / shots
            mats_star[q] = np.array([[1 - e0s, e1s], [e0s, 1 - e1s]])
        pays = {}
        for N in NS:
            mats = [mats_star[str(q)] for q in fil[N]]
            ms, ss = [], []
            for f in FOLDS:
                p_raw = rng.multinomial(shots, p_emp[(N, f)]) / shots
                m, s = fast_stats(mitigate_probs(p_raw, mats), *cbars[N], shots)
                ms.append(m)
                ss.append(max(s, 1e-9))
            pays[N] = ms
            meas_f1[N][b] = ms[0] - refs[N]["classical_ne_payoff"]
            meas_zne[N][b] = (zne_extrapolate(list(FOLDS), ms, ss)["linear"]
                              - refs[N]["classical_ne_payoff"])
        ps = float(inv31(pays[3][0]))
        if not P_GRID[0] <= ps <= P_GRID[-1]:
            clipped += 1
            ps = float(np.clip(ps, P_GRID[0], P_GRID[-1]))
        p_star_all[b] = ps
        for N in NS:
            model_f1[N][b] = (float(curve[(N, 1)](ps))
                              - refs[N]["classical_ne_payoff"])
            mzne = zne_extrapolate(
                list(FOLDS), [float(curve[(N, f)](ps)) for f in FOLDS],
                zne_weights[N])["linear"]
            model_zne[N][b] = mzne - refs[N]["classical_ne_payoff"]
        if (b + 1) % 500 == 0:
            print(f"  {b + 1}/{B}")
    if clipped:
        print(f"  WARNING: {clipped} replicates clipped to the p grid")

    # ── assemble + write ──────────────────────────────────────────────────────
    def pred(center: float, model_arr: np.ndarray, meas_arr: np.ndarray,
             anchor: bool = False) -> dict:
        sm = float(np.std(model_arr, ddof=1))
        sme = float(np.std(meas_arr, ddof=1))
        sp = float(np.hypot(sm, sme))
        out = {
            "advantage": center,
            "sigma_model": sm,
            "sigma_measurement": sme,
            "sigma_predictive": sp,
            "pi68": [center - sp, center + sp],
            "pi95": [center - 1.96 * sp, center + 1.96 * sp],
            "model_ci95": [float(np.percentile(model_arr, 2.5)),
                           float(np.percentile(model_arr, 97.5))],
        }
        if anchor:
            out["anchor"] = ("fit target -- reproduces run 1 by construction; "
                             "not an independent test")
        return out

    payload = {
        "registered_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": ("Frozen fit-one-predict-two prediction: p_eff fitted on the "
                    "N=3 mitigated fold-1 payoff of run 2026-07-16T074134Z; "
                    "N=4,5 advantages are predictions committed BEFORE any "
                    "repeat batch run."),
        "source_run": {
            "dir": os.path.relpath(RUN_DIR, REPO).replace(os.sep, "/"),
            "job_id": res["job"]["job_id"],
            "backend": res["job"]["backend"],
            "created_utc": res["created_utc"],
            "git_commit_of_run": res["git"]["commit"],
        },
        "environment": {
            "python": platform.python_version(),
            "qiskit": __import__("qiskit").__version__,
            "qiskit_aer": __import__("qiskit_aer").__version__,
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
        },
        "protocol": {
            "seed": SEED,
            "bootstrap_replicates": B,
            "clipped_replicates": clipped,
            "shots": shots,
            "fit_target": "N=3 mitigated fold-1 payoff",
            "model": ("Month-4 depolarizing model (circuits.noise, {u,cx} "
                      "basis, GHZ topology): ONE parameter p on 1q and 2q "
                      "gates alike"),
            "fold_model": ("cz-fold f => 2q depolarizing composed f times "
                           "(p2 = 1-(1-p)^f); 1q errors not folded"),
            "p_grid": {"min": float(P_GRID[0]), "max": float(P_GRID[-1]),
                       "points": len(P_GRID), "interpolation": "pchip"},
            "uncertainties_propagated": ["shot (multinomial resampling)",
                                         "mitigation (binomial cal resampling)",
                                         "fit (p_eff refit per replicate)",
                                         "ZNE (weighted fit per replicate)"],
            "uncertainties_excluded": ["model-form error",
                                       "cross-day calibration drift"],
            "registered_tests": {
                "conditional (primary, drift-robust)": (
                    "for each repeat run: refit p_eff on that run's N=3 "
                    "mitigated fold-1 payoff; that run's measured N=4 and N=5 "
                    "mitigated fold-1 advantages must fall inside the 95% "
                    "predictive intervals recentred on the refit prediction "
                    "(same sigma_predictive)"),
                "unconditional (secondary, assumes stationarity)": (
                    "repeat-run measured advantages vs the pi95 intervals "
                    "below as-is"),
            },
        },
        "p_eff": {
            "central": p_eff,
            "sigma": float(np.std(p_star_all, ddof=1)),
            "ci95": [float(np.percentile(p_star_all, 2.5)),
                     float(np.percentile(p_star_all, 97.5))],
        },
        "predicted_advantages": {
            str(N): {
                "ideal": refs[N]["advantage"],
                "classical_ne_payoff": refs[N]["classical_ne_payoff"],
                "mitigated_fold1": pred(stored[str(N)]["advantage"],
                                        model_f1[N], meas_f1[N],
                                        anchor=(N == 3)),
                "zne_linear": pred(
                    central_zne[N] - refs[N]["classical_ne_payoff"],
                    model_zne[N], meas_zne[N]),
            } for N in NS
        },
        "verification": {"g1_p_eff_exact": True, "g2_pipeline_max_delta": worst,
                         "g3_interp_error": {"curve": e_curve, "inverse": e_inv}},
    }
    # source-run self-check: where run 1's OWN measurements sit relative to the
    # registered intervals. z != 0 here is model-form tension visible already
    # at registration time -- the repeats test whether it reproduces.
    payload["source_run_comparison"] = {}
    for N in NS:
        cls = refs[N]["classical_ne_payoff"]
        rows = {}
        for level, meas in (
            ("mitigated_fold1",
             ana["series"][str(N)]["folds"]["1"]["mitigated"]["mean"] - cls),
            ("zne_linear", ana["series"][str(N)]["zne"]["advantage"]),
        ):
            d = payload["predicted_advantages"][str(N)][level]
            rows[level] = {
                "measured_run1": meas,
                "predicted": d["advantage"],
                "delta": meas - d["advantage"],
                "z": (meas - d["advantage"]) / d["sigma_predictive"],
            }
        payload["source_run_comparison"][str(N)] = rows
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)

    print(f"\np_eff = {p_eff:.6e}  (sigma {payload['p_eff']['sigma']:.2e}, "
          f"95% CI [{payload['p_eff']['ci95'][0]:.2e}, "
          f"{payload['p_eff']['ci95'][1]:.2e}])")
    print("\n  N | level           | predicted adv | 95% predictive int | run-1 z")
    print("  --+-----------------+---------------+--------------------+--------")
    for N in NS:
        for level in ("mitigated_fold1", "zne_linear"):
            d = payload["predicted_advantages"][str(N)][level]
            z = payload["source_run_comparison"][str(N)][level]["z"]
            tag = " (anchor)" if "anchor" in d else ""
            print(f"  {N} | {level:<15s} | {d['advantage']:13.6f} "
                  f"| [{d['pi95'][0]:.4f}, {d['pi95'][1]:.4f}]   | {z:+5.1f}"
                  f"{tag}")
    print(f"\nsaved: {os.path.relpath(OUT_PATH, os.getcwd())}")


if __name__ == "__main__":
    main()
