# Design: Hardware Scaling Curve (N=3,4,5) + Error Mitigation

**Date:** 2026-07-16
**Scope:** Month-5→6 upgrade — turn the single N=3 hardware point into an
IEEE-QCE-grade result: measured advantage vs N on ibm_fez, raw + readout-mitigated
+ ZNE, overlaid on noise-model predictions, repeatable for cross-day error bars.
**Status:** Approved (chat 2026-07-16); supersedes nothing — extends the Month-5
pipeline.

---

## 1. Goal & claims targeted

1. **Scaling:** measured (Q,…,Q) cooperative-profile payoff and advantage at
   N = 3, 4, 5 (GHZ) on real hardware, on one pinned qubit chain.
2. **Prediction:** two simulation predictions per N, computed from data
   *independent of the hardware counts*:
   (a) device noise model (qiskit-aer `NoiseModel.from_backend`, reduced to the
   executed qubits) and (b) the repo's Month-4 depolarizing path with a single
   effective p fitted at N=3 only → predicts N=4,5 (fit-one-predict-two).
3. **Mitigation:** tensored readout-error mitigation (M3-style) + zero-noise
   extrapolation via local cz folding. Report raw, mitigated, and ZNE.
4. **Repeats:** every run is one self-contained batch job; an aggregator computes
   mean ± std across ≥1 runs (cross-day repeats accumulate over the month).

## 2. Honesty constraints (from simulation ground truth, 2026-07-16)

- Ideal (Q,…,Q) → |0…0⟩ with P=1 at every N; payoffs V/N = 1.333/1.0/0.8;
  classical NE payoffs 1/3, 1/4, 1/5 → ideal advantage **1.0 / 0.75 / 0.6**.
- (Q,…,Q) is a **pure NE only at N=3**. At N=4 a unilateral Hawk deviation pays
  2.0 > 1.0; at N=5, 2.618 > 0.8 (fixed GHZ-derived Q_N; Month-3 finding).
  The hardware experiment measures the **cooperative-profile payoff**; NE status
  is a per-N simulation annotation, stated in every figure caption.
- Hardware "advantage" = measured Q-profile payoff − **analytic noiseless**
  classical NE payoff (same convention as the Month-5 N=3 run; stated in captions).

## 3. Decisions

- **D1 Circuits from src, not the prototype.** `circuits.gate_level.ghz_gate_circuit`
  is the N-generic hand-built J (CX ladder, 2(N−1) CX per J). The EWL circuit is
  J · U(q_strategy(N))^⊗N · J†. Two gates before any submission, per N:
  identity assertion (`Operator.equiv` vs dense J†·(U⊗…⊗U)·J) and a noiseless
  Aer dry-run reproducing `compute_advantage(N)` exactly. `experiments/hand_built_j.py`
  stays untouched (historical N=3 prototype).
- **D2 Pinned chain.** One 5-qubit linear chain on ibm_fez, chosen by minimizing
  Σ cz error (4 edges) + Σ readout error (5 nodes) over all simple paths
  (`src/hardware/chain.py`). N=3/4/5 use chain prefixes → same physical qubits
  across the curve (controlled variable). Layout pinned via `initial_layout`;
  measurement wiring uses `final_index_layout()` (tolerates transpiler permutation).
- **D3 One batch job.** pubs = [cal0, cal1] + [N ∈ {3,4,5} × fold ∈ {1,3,5}] =
  11 pubs × 4096 shots in ONE SamplerV2 job (calibration-matched mitigation,
  quota-efficient). Job id persisted to disk before polling; `--from-job` recovery.
- **D4 Readout mitigation.** Per-qubit 2×2 confusion matrices from cal0=|0…0⟩,
  cal1=|1…1⟩ (tensored), inverted by constrained least squares (p ≥ 0, Σp = 1)
  — `src/hardware/mitigation.py`. No new deps (mthree would risk the pinned env).
- **D5 ZNE by local cz folding.** cz is self-inverse ⇒ cz→cz³/cz⁵ is ISA-legal
  and scales the dominant error channel (cz EPG ~0.2% vs sx ~0.02%; the strategy
  layer compiles to virtual rz = error-free). Payoff extrapolated to fold 0 by
  weighted linear fit (primary) + Richardson (secondary), on readout-mitigated
  payoffs.
- **D6 Rehearsal before quota.** The full batch (folds + cals + analysis) runs
  end-to-end on `AerSimulator(noise_model=reduced from_backend model)` first.
  Gate: pipeline completes and ZNE beats raw for ≥2 of 3 N. Only then submit.
- **D7 Prediction artifacts.** The reduced device noise model dict is persisted
  in the run dir (offline-reproducible predictions); effective-p curve uses
  `circuits.noise.build_ewl_circuit_noisy` on the (Q,…,Q) profile only.
- **D8 Results.** `results/hardware-scaling/<UTC>/`: result.json (per N × fold:
  counts, raw/mitigated/ZNE payoff+advantage, shot-noise errors), calibration.json,
  reduced_noise_model.json, job.json, plots/. `scripts/plot_hardware_scaling.py`
  aggregates ≥1 run dirs → scaling figure with mean ± std.

## 4. Error budget (calibration 2026-07-15, best-chain estimate)

J+J† = 4(N−1) CX → 8/12/16 cz at N=3/4/5 (≈6/10/14 after transpile).
Naive fidelity ≈ (1−0.002)^cz · (1−0.004)^N → ~0.97/0.95/0.93; measured will be
slightly lower (crosstalk/idle). Advantage stays well above 0 at all N — the
result is the *decay curve matching prediction*, not survival alone.

## 5. Test plan

- `tests/test_gate_level.py`: extend GHZ dense-vs-gate equivalence to N=5,6.
- `tests/test_hardware_mitigation.py` (new): synthetic confusion matrices —
  mitigation recovers a known distribution (round-trip); ZNE recovers the
  intercept of synthetic linear/exponential decay; chain scorer picks the known
  best path on a toy graph.
- Full existing suite must stay green (94+ tests).
