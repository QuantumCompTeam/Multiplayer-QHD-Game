> A systematic benchmark of how QEC decoders (MWPM, BP-OSD, Ambiguity Clustering) degrade when the *noise prior* they decode against goes stale — using real IBM Heron/Nighthawk calibration data to drive the drift, surface and bivariate-bicycle codes to stress it,  and a controlled prior-misspecification design so the central result holds even if no
> historical calibration can be recovered.

*Analysis date: 2026-06-02. All external claims web-verified; sources inline.*

---

## 0. TL;DR / thesis

Every decoder carries a **noise prior**: MWPM bakes calibration into edge weights, BP-OSD into
log-likelihood priors, Ambiguity Clustering into its BP stage. A device's calibration is the
ground truth that prior is meant to match — and that ground truth **drifts** over hours to days
(TLS-driven T1 fluctuations, gate/readout error wander). So "robustness to calibration drift" is,
precisely, **robustness to prior misspecification**.

The thesis of this project: *map the relationship between prior staleness and logical error rate
(LER), across decoder families and code families, and find out which decoders degrade gracefully
and which fall off a cliff.* The deliverable is an open dataset + a small benchmark library + a
paper reporting the first systematic **drift-penalty curves** for QEC decoders driven by real
IBM calibration data.

This reframing is not cosmetic — it is what makes the project (a) conceptually pointed rather than
a measurement chore, and (b) **robust to its single biggest execution risk** (see §1.1 and §4.1).

---

## 1. The open problem & why it is conceptually interesting

### The cited gap is real

The trigger is **Stein et al., arXiv:2601.16123** (22 Jan 2026), *"Calibration-Conditioned FiLM
Decoders for Low-Latency Decoding of Quantum Error Correction Evaluated on IBM Repetition-Code
Experiments"* (PNNL / Fordham / UCSD, + Lehigh & UW). They build a neural decoder whose CNN backbone
is modulated (FiLM = Feature-wise Linear Modulation) by an encoding of the device's calibration
data, explicitly to separate *slow* calibration drift from *fast* (µs-scale) syndrome decoding.
Verified headline: up to **11.1× lower LER vs hardware-informed MWPM**, strongest at d≥7.

Crucially — and this is the lever for the whole project — they **tested only 1D repetition codes
up to d=11** (on IBM Fez, Kingston, Pittsburgh; ~2.7M shots over ~400 calibration snapshots).
Surface codes are named explicitly as *future work*; bivariate-bicycle codes are not touched. The
paper demonstrates that conditioning on calibration *helps*, but says nothing systematic about
**how badly the standard, deployed decoders degrade without that conditioning, on codes anyone
actually plans to run.**

### Why this is interesting beyond "measuring a known effect"

The shallow version of this project ("calibration gets old, errors go up, let's plot it") is not
worth doing. The interesting version asks structural questions whose answers are *not* obvious a
priori:

- **Do soft-prior decoders degrade more gracefully than hard-weight ones?** MWPM commits to edge
  weights; a stale weight is a hard, possibly confidently-wrong, commitment. BP-OSD carries soft
  log-likelihoods and re-derives a solution; Ambiguity Clustering keeps multiple hypotheses alive.
  A plausible, testable hypothesis: **AC > BP-OSD > MWPM in drift-robustness**, and the *gap*
  between them widens as the prior ages. If true, that is a clean, citable structural result.
- **What is the "decoding half-life" of a calibration?** For a target LER, how stale can the prior
  get before the LER degrades by, say, 2×? Is that half-life code-dependent (surface vs gross),
  distance-dependent, decoder-dependent? This is the practically useful number a real QEC operator
  wants and nobody has published.
- **Is drift-penalty dominated by which parameters drift?** Readout drift vs two-qubit-gate drift
  vs T1 drift may hit different decoders unequally. Decomposing the penalty by parameter channel is
  a second-order result that falls out of the same data.

These are the questions that make the benchmark a *finding*, not a table.

---

## 2. What already exists (and the precise shape of the gap)

| Piece | Status (verified) | Relevance |
|---|---|---|
| **FiLM / calibration-conditioned decoder** | arXiv:2601.16123, Stein et al. Jan 2026. Repetition codes d≤11 only. | The motivation; we generalise its question to surface/gross codes and to *standard* decoders. |
| **MWPM** | Dennis–Kitaev–Landahl–Preskill 2002; impl. PyMatching v2 (Higgott/Gidney, sparse blossom). | Baseline #1. Hard-weight prior. |
| **BP-OSD** | Panteleev–Kalachev, *Quantum* 5, 585 (2021); Roffe et al. PRR 2020. Impl. `ldpc`. | Baseline #2. Soft prior. Standard qLDPC decoder. |
| **Ambiguity Clustering (AC)** | Wolanski & Barber (**Riverlane**), arXiv:2406.14527. ~27× faster than BP-OSD on the gross code (~135 µs/round). | Baseline #3. Multi-hypothesis; the "fast accurate qLDPC decoder." |
| **Gross code** [[144,12,12]] | Bravyi et al., *Nature* 627 (2024), arXiv:2308.07915. BP-OSD-decoded; circuit-level threshold ≈0.7% (≈0.65% for [[144,12,12]]). | Stress code #2. ("Gross code" is IBM shorthand, not Nature's term.) |
| **Rotated surface code** [[d²,1,d]] | Standard; MWPM-decoded. | Stress code #1. |

**Adjacent prior art (the closest anyone has come):**
- **DGR**, arXiv:2311.16214 — re-weights the decoding graph for drifted/correlated noise, but
  evaluated in *simulation* on surface/honeycomb codes; not a drift-vs-age benchmark.
- **Noise-aware decoding**, arXiv:2502.21044 — notes priors *could* be updated online for drift, but
  optimises priors rather than measuring degradation.
- **ReloQate** (arXiv:2603.00837) / **CaliQEC** — drift *detection* and in-situ recalibration, not a
  decoder-degradation curve.

**The gap, stated precisely:** *there is no published, systematic benchmark of decoder LER as a
function of calibration prior quality/age, across decoder families and code families, grounded in
real IBM calibration data.* The novelty is **defensible but not provable from search alone** —
absence in indices is not proof. Before claiming "first," read the related-work section of
2601.16123 directly and sweep IEEE QCE / ISCA / MICRO proceedings, where systems-flavoured QEC
drift studies tend to land.

---

## 3. Methodology / experimental design

The design has **two drift axes**, deliberately, so the science does not depend on a fragile data
source (see §4.1).

### Code families
- **Rotated surface codes**, d = 3, 5, 7, 9, (11) — decoded by MWPM and BP-OSD.
- **Gross code [[144,12,12]]** (and optionally a smaller [[72,12,6]] BB code for cost) — decoded by
  BP-OSD and AC.
- *(Optional control)* repetition code d≤11, to reproduce the FiLM paper's regime and tie results to
  prior work.

### Decoders
MWPM (PyMatching) · BP-OSD (`ldpc` / `stimbposd`) · Ambiguity Clustering (Riverlane's method;
reimplement or use available code) · *(stretch)* a reproduced FiLM baseline as the
"calibration-aware upper bound."

### Axis A — Synthetic prior misspecification (primary, history-independent)
The clean experiment. Given one calibration snapshot → noise model **N**:
1. Sample syndromes from the *true* model **N** (stim).
2. Decode them with a prior derived from a *perturbed* model **N′** (stale/wrong calibration).
3. **Drift penalty** = LER(decode under N′) − LER(decode under N, the matched oracle).

Sweep the perturbation magnitude (overall scale, and per-channel: readout-only, 2q-gate-only,
T1-only) and direction. This yields controlled drift-penalty curves **without needing any historical
data at all**, and lets us decompose the penalty by parameter channel.

### Axis B — Real drift (validation)
Using prospectively collected snapshots (§5, §7): form **(decode-time prior, actual-noise) pairs**
separated by real elapsed time Δt, and measure LER vs Δt — the genuine "calibration age" curve.
Axis B validates that the synthetic perturbations in Axis A are physically representative.

### Metrics
- **LER** per (code, distance, decoder, drift condition), with bootstrap CIs.
- **Drift penalty** ΔLER(perturbation) and ΔLER(Δt).
- **Robustness slope / decoding half-life**: prior staleness at which LER degrades 2× for a fixed
  target — reported per decoder and per code.
- **Per-channel sensitivity**: ∂LER/∂(readout), ∂(2q-gate), ∂(T1).

---

## 4. Critical analysis — the things that can break this, honestly rated

### 4.1 ⚠️ CRITICAL: retroactive historical calibration is probably unavailable
`backend.properties(datetime=...)` (and `target_history`) returned timestamped historical snapshots
on the **legacy `ibm_quantum` channel** — but that channel was **retired 1 July 2025**, and the docs
state the datetime path raises `NotImplementedError` on cloud runtime, which is the only runtime left.
**So "backfill 4 weeks of historical snapshots" likely does not work today.** This is the single
biggest risk and it kills the naive version of the project.

*Mitigations (already baked into the design):*
- The science lives on **Axis A (synthetic)**, which needs only a *single* current snapshot.
- For **Axis B**, collect snapshots **prospectively** — current calibration is downloadable per QPU
  (CSV/API) with **no execution cost**, on the free Open Plan. Start day 1; accumulate over the
  project.
- Pursue the **FiLM paper's released data** (~400 snapshots across Fez/Kingston/Pittsburgh) as a
  possible historical backfill source.
- **Phase 0 action:** empirically confirm what the live API does *before* building anything on it.

### 4.2 No turnkey IBM-calibration → stim-DEM mapper (main engineering chunk)
Nothing maps `BackendProperties` directly to a stim detector error model. The building blocks exist —
Qiskit Aer `NoiseModel.from_backend()` extracts gate/T1/T2/readout errors; `qiskit-qec`'s `stim_tools`
bridges circuit ↔ stim ↔ DEM; `stimbposd` decodes with BP-OSD — but the **glue that converts
calibration numbers into per-location Pauli rates** must be written and validated. Budget real time
here; it is also the reusable core of the released library.

### 4.3 Heron/Nighthawk cannot natively host bivariate-bicycle codes
Heron is heavy-hex; **BB/gross codes need degree-6 connectivity** (that is the purpose of IBM's
experimental *Loon* processor). Nighthawk is square-lattice, degree-4. Verified: Nighthawk is real —
120 qubits, 218 tunable couplers, GA ~Jan 2026.
**Implication:** because this project is **simulation-only for circuits** and uses calibration only as
*noise parameters*, gross-code-on-Heron is a legitimate study of "what if a device with these error
rates ran this code" — but it is a **noise-parameter injection, not a connectivity-faithful layout**.
State this explicitly; do not imply Heron runs BB codes.

### 4.4 Risk of an uninteresting result
If every decoder degrades identically and smoothly, the finding is thin. Three hedges: (a) the
per-channel decomposition (§3) almost certainly *does* differ across decoders; (b) the decoding
half-life is a useful number regardless of whether decoders differ; (c) the surface-vs-gross
comparison is itself novel. Even the null result ("calibration age barely matters below X hours for
surface codes") is publishable and operationally useful.

### 4.5 Novelty not provable from search
See §2. Defensible, contingent on a direct related-work check.

---

## 5. Toolchain & data pipeline

```
IBM Quantum Platform                stim                         decoders
─────────────────────              ──────                       ──────────
backend.properties()  ──extract──►  build noisy circuit   ──►   pymatching (MWPM)
(T1,T2,gate,readout,                (per-location Pauli         ldpc / stimbposd (BP-OSD)
 timestamps)            │            channels)                   AC (Riverlane method)
                        │                │                            │
                  calibration→Pauli   .detector_error_model()    LER, drift penalty
                  mapping (OUR glue)  + sinter parallel sampling  + half-life, CIs
```

- **stim** (Gidney, *Quantum* 2021) — syndrome sampling + DEM. Pauli-noise only ⇒ calibration must be
  **Pauli-twirled** (no native amplitude damping/coherent errors); state this approximation.
- **sinter** — parallel shot sampling + decoding.
- **pymatching** (MWPM), **ldpc** + **stimbposd** (BP-OSD), AC reimplementation.
- **Qiskit Aer `NoiseModel.from_backend()`** + **qiskit-qec `stim_tools`** — extraction + bridge.
- **Snapshot schema** (lock early): `{backend, timestamp, per-qubit {T1,T2,freq,readout_err},
  per-gate {error, length}, coupling map, software versions}` → versioned JSON/Parquet, one file per
  pull. This schema *is* the released dataset.

---

## 6. Phased development plan

Rewritten so prospective collection starts immediately and first results need **no** historical data.

- **Phase 0 — Reality check & data tap (Week 1).**
  Empirically test whether *any* historical retrieval works on the live API (kills/confirms §4.1).
  Stand up a **daily calibration-snapshot cron** for 2–3 backends (a Heron + Nighthawk if available).
  Lock the snapshot schema. Attempt to obtain the FiLM paper's dataset.

- **Phase 1 — Pipeline + MWPM baseline + synthetic harness (Weeks 2–6).**
  Build the calibration→stim-DEM glue (§4.2). Reproduce a clean MWPM rotated-surface-code LER curve
  (sanity vs literature thresholds). Implement the **Axis-A synthetic prior-misspecification harness**.
  → **First publishable results land here, independent of historical data.**

- **Phase 2 — Full decoder × code matrix on the synthetic axis (Weeks 7–12).**
  Add BP-OSD and AC; add the gross code. Produce drift-penalty curves and per-channel sensitivity for
  all (code, decoder) cells. Decoding half-life table.

- **Phase 3 — Real-drift validation (Weeks 13–18).**
  Use the now-accumulated prospective snapshots to build Axis-B (decode-time-prior, actual-noise)
  pairs; check that synthetic perturbations track real drift. Cross-backend comparison.

- **Phase 4 — Write-up & open release (Weeks 19–24).**
  Open dataset (snapshots + DEMs), benchmark library (the pipeline + harness), paper.

---

## 7. Threats to validity (call these out in the paper)

- **Pauli-only noise** (§5): real coherent/leakage errors are twirled away; drift penalties are
  lower-bounds on the true effect for some channels.
- **Layout mismatch** (§4.3): BB-on-Heron noise injection ≠ a real degree-6 device.
- **Simulation vs hardware**: only calibration is real; syndrome statistics are simulated. The result
  is "decoder behaviour under realistic, drifting noise *parameters*," not a hardware demonstration.
- **Single vendor**: IBM-only; generality to other platforms unestablished.
- **Snapshot cadence aliasing**: daily pulls may undersample sub-hour T1 excursions; report cadence.
- **AC reproduction fidelity**: if AC is reimplemented rather than using Riverlane's code, validate
  against their published speed/accuracy numbers before drawing robustness conclusions.

---

## 8. Deliverables & venue

- **Open dataset** — versioned calibration snapshots + derived DEMs for 2–3 backends.
- **Benchmark library** — the calibration→DEM pipeline + the drift-penalty harness, reusable by
  anyone running QEC experiments who needs to know how stale their decoder prior can get.
- **Paper** — first systematic decoder drift-penalty / decoding-half-life curves across decoder and
  code families. Target **PRX Quantum** or **IEEE Transactions on Quantum Engineering**.

---

## 9. Open questions / decision points

1. **Backends:** which 2–3? (A Heron + Nighthawk gives a lattice/connectivity contrast; adding a
   third Heron revision gives a same-architecture drift control.)
2. **AC:** reimplement, or seek Riverlane's implementation? (Affects Phase 2 scope and §7 validity.)
3. **FiLM baseline:** reproduce it as a calibration-aware upper bound, or cite-and-defer? (Reproduction
   is a meaningful extra chunk but strengthens the story.)
4. **Code scope:** include the gross code in the first paper, or split surface-first / BB-follow-up?
5. **Historical data:** if neither the live API nor the FiLM dataset yields history, the paper rests
   on Axis A + prospective Axis B only — acceptable, but worth deciding up front how prominently to
   frame "calibration *age*" vs "prior *misspecification*."

---

### Related notes
[[Surface Codes]] · [[Bivariate Bicycle Codes]] · [[BP-OSD]] · [[MWPM]] · [[Ambiguity Clustering]] · [[IBM Heron Nighthawk]] · [[FiLM Decoder]]

### Key references
- Stein et al., arXiv:2601.16123 (FiLM calibration-conditioned decoder, 2026)
- Bravyi et al., *Nature* 627, 778 (2024) / arXiv:2308.07915 (BB / gross code)
- Wolanski & Barber, arXiv:2406.14527 (Ambiguity Clustering, Riverlane)
- Panteleev & Kalachev, *Quantum* 5, 585 (2021) (BP-OSD)
- Dennis, Kitaev, Landahl, Preskill, *J. Math. Phys.* 43, 4452 (2002) (MWPM)
- Gidney, *Quantum* 5, 497 (2021) (stim) · Higgott (PyMatching, stimbposd) · Roffe (`ldpc`)
- Carroll et al., *npj QI* (2022), arXiv:2105.15201 (T1 drift / TLS) — physical basis for drift
````````````
