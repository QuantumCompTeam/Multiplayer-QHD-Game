# Pre-registered predictions — effective-p scaling model (frozen 2026-07-16)

**Status: FROZEN REGISTRATION.** Committed **before any repeat batch run**
(only run `2026-07-16T074134Z`, job `d9c8fpn550hc73dl1tcg`, existed at
registration time — see `results/hardware-scaling/pending_jobs.txt`). The
commit timestamp of this file is the registration timestamp. Canonical
numbers live in `results/hardware-scaling/preregistration.json`; this document
is the human-readable protocol. Neither may be edited after repeat runs exist
— corrections go in a new dated file.

## What is registered and why

The scaling claim rests on a one-parameter effective depolarizing model:
`p_eff` is fitted on the **N=3 mitigated fold-1 payoff only** and then
*predicts* N=4 and N=5 (fit-one-predict-two). Without a frozen prediction, the
planned repeat runs (TODOS.md) would just be "more data" that the curve is
re-drawn through. This registration converts them into a falsifiable test:
the predictions below were fixed, with propagated uncertainty intervals,
before any repeat data existed.

## Fit and model

- Fit target: N=3 mitigated fold-1 payoff of run 1 = 1.325266524396583.
- Model: Month-4 depolarizing model (`circuits/noise.py`, `{u,cx}` basis, GHZ
  topology), one parameter `p` on 1q and 2q gates alike, inverted by the
  production bisection (`experiments/hardware_scaling.py::effective_p_prediction`).
- **p_eff = 1.8376e-3** (exactly 0.001837649512845019, reproduced bit-exact at
  registration), bootstrap sigma 3.30e-4, 95% CI [1.19e-3, 2.49e-3].
- cz-fold f is modeled as the 2q depolarizing channel composed f times
  (p2 = 1−(1−p)^f), 1q errors not folded — this yields model ZNE predictions
  through the production `zne_extrapolate`, weighted like the pipeline.

## Registered predictions (advantage vs analytic classical NE)

| N | level           | predicted | σ_model | σ_meas  | 95% predictive interval |
|---|-----------------|-----------|---------|---------|-------------------------|
| 3 | mitigated fold-1| 0.991933  | 0.00141 | 0.00141 | anchor — not a test     |
| 3 | ZNE (linear)    | 0.994033  | 0.00107 | 0.00186 | [0.9898, 0.9982]        |
| 4 | mitigated fold-1| 0.742690  | 0.00126 | 0.00153 | [0.7388, 0.7466]        |
| 4 | ZNE (linear)    | 0.744470  | 0.00099 | 0.00174 | [0.7405, 0.7484]        |
| 5 | mitigated fold-1| 0.593170  | 0.00117 | 0.00156 | [0.5894, 0.5970]        |
| 5 | ZNE (linear)    | 0.594730  | 0.00095 | 0.00174 | [0.5908, 0.5986]        |

σ_model = fit uncertainty propagated through the model (p_eff refit per
bootstrap replicate); σ_meas = single-run measurement noise of the quantity a
repeat run reports (shot + mitigation + ZNE-fit); interval = predicted ±
1.96·√(σ_model² + σ_meas²).

## Uncertainty budget

Propagated (one joint parametric bootstrap, B=2000, seed=20260716, run in the
pinned `entangled-equilibria` env):

- **shot** — multinomial resampling of every series pub's 4096-shot counts;
- **mitigation** — binomial resampling of the per-qubit confusion-matrix
  entries (cal pubs were 4096 shots; raw cal counts are not persisted, so the
  stored per-qubit e0/e1 are resampled parametrically, consistent with the
  tensored readout model);
- **fit** — p_eff re-fitted per replicate by inverting the model curve
  (grid of 41 exact density-matrix sims per (N, fold), PCHIP interpolation,
  verified to 1e-11 against the exact simulator);
- **ZNE** — the weighted linear extrapolation re-run per replicate.

Explicitly **excluded** (cannot be estimated from one run): model-form error
and cross-day calibration drift. Drift is handled by the conditional test
below; model-form error is exactly what the test is for.

## Registered tests

1. **Conditional (primary, drift-robust).** For each repeat run: refit p_eff
   on *that run's* N=3 mitigated fold-1 payoff; that run's measured N=4 and
   N=5 advantages must fall inside 95% predictive intervals recentred on the
   refit predictions (same σ_predictive). This tests the *scaling shape*
   independent of day-to-day noise-level drift.
2. **Unconditional (secondary, assumes stationarity).** Repeat-run measured
   advantages compared against the table above as-is.

Falsification: with k repeat runs, ~0.05·k excursions per registered quantity
are expected by chance; a *systematic, same-signed* miss at N=4/5 across
repeats falsifies the one-parameter model at this precision (it does not
touch the measured advantages themselves, which stand on their own).

## Known tension at registration time (declared, not hidden)

Run 1's own N=4/5 measurements already sit **below** the model:

| N | level            | measured (run 1) | predicted | z      |
|---|------------------|------------------|-----------|--------|
| 4 | mitigated fold-1 | 0.738427         | 0.742690  | −2.14  |
| 4 | ZNE (linear)     | 0.740331         | 0.744470  | −2.07  |
| 5 | mitigated fold-1 | 0.583119         | 0.593170  | −5.17  |
| 5 | ZNE (linear)     | 0.588689         | 0.594730  | −3.05  |

So the sharp registered question for the repeats is: **is the N=5 deficit
(~0.010 in advantage, ~5σ statistical) reproducible?** If yes, the single-p
model is falsified at this precision — plausible mechanisms are the hardware
transpile using more 2q gates than the `{u,cx}` model circuit (14 cz vs 8 cx
at N=5) and idling decoherence on the longer chain, neither of which the
one-parameter model sees. If the deficit vanishes, run 1's N=5 point was a
bad-day fluctuation. Either outcome is informative; both are now falsifiable.

## Reproduction

```
conda run -n entangled-equilibria python scripts/preregister_peff.py
```

Deterministic (seeded bootstrap; env pinned: python 3.10.20, qiskit 1.3.2,
aer 0.14.2 — versions recorded in the JSON). The script hard-fails unless it
(G1) reproduces the stored p_eff bit-exactly via the production fit, (G2)
reproduces every stored mitigated payoff and ZNE intercept through the
production mitigation path, and (G3) bounds the interpolation error.
