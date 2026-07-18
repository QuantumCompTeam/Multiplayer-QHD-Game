# Topology vs implementation: control study for the noise-robustness ordering

**Status: LOCKED CONTROL STUDY.** Simulation only (zero hardware quota).
Data: `results/topology-controls/2026-07-16T172737Z/results.json`;
script `scripts/topology_noise_controls.py`
(deterministic, seed 20260716, pinned `entangled-equilibria` env). The
restricted evaluator reproduces the locked noise-robustness CSV
(`results/noise-robustness/2026-07-03T0213Z`) to |Δ| ≤ 4.2e-14 before any
control runs (anchor gate).

## Question

The Month-4 noise-robustness ordering compares topologies through their
gate-level circuits, which differ in two-qubit-gate count and synthesis
(N=5: GHZ 16 cx, star 16, ring 20, fully-connected 40, W 136, J·U·J†
inclusive). Under the pinned per-gate depolarizing model, is the reported
ordering a **topology** effect or a **circuit-implementation** (gate-budget /
compilation) artifact?

## Controls run

- **A — gate-count matching**: every topology padded with identity pads
  (cx·cx pairs, `u(0,0,0)`) to the max u/cx budget at that N, over 5 pad
  placements. Pre-committed criterion: an ordering relation *survives A* only
  if it holds in **all** placements at p=0.01 and 0.02.
- **B — realization variance**: same entangler unitary, different circuits —
  transpiler optimization levels {0,2,3} (production = 1), 4 edge-order
  shuffles for the pairwise topologies (commuting RXX factors), reversed
  CX-ladder for GHZ. Every variant verified against the dense entangler
  (`Operator.equiv`) before use. Survives B = relation holds across **all**
  variant pairs.
- **C — per-2q-gate normalization**: initial advantage decay rate
  λ = −(dA/dp)/A(0) at p→0.005, divided by the cx count.
- **Nulls** (both exact, both verified): wiring/qubit-mapping permutation
  leaves the mean payoff invariant (Δ = 0.0) — mapping is not a confound for
  mean-advantage claims under the all-qubit-uniform model. And two circuits
  with the same per-qubit instruction order are the same noise channel
  (ASAP-repack: max |Δprob| = 2.8e-17) — **depth is not independently
  variable under per-gate noise**, so matched-count controls subsume
  matched-depth controls. Depth becomes a real variable only under
  time-based noise (T1/T2 device models) — out of scope of the locked claims,
  flagged as follow-up.

## Headline result: the per-gate decay rates

λ/cx, all N (control C):

| N | GHZ | ring | star | full | W |
|---|------|------|------|------|-----|
| 3 | 2.55 | 2.44 | 2.65 | 2.44 | 0.98 |
| 4 | 2.25 | — (A(0)=0) | 2.42 | 2.10 | 0.79 |
| 5 | 2.09 | 2.13 | 2.25 | 1.82 | 0.79 |

Within the XX-product family (GHZ/ring/star/fully-connected) the per-gate
rates are indistinguishable (2.1–2.7 across every N). **Their robustness
ordering is a gate-budget story.** W is the lone structural outlier: ~2.5–3×
*more* robust per gate than everything else — the opposite of its last-place
absolute standing.

## Verdict per locked claim (README §9)

**L1 — "N=3: GHZ retains the most mean advantage at p=0.05 (0.333/33%)
versus ring (0.200/20%) and W (0.047/9%)."  PARTIAL — the W comparison
collapses into "more gates = more noise".**
GHZ>W and ring>W survive A (10/10 placements) and B (all pairs) in *absolute*
advantage — but only because W's noiseless advantage is half theirs (0.5 vs
1.0) and stays half under matching. The *retention/fragility* reading ("W
degrades fastest") collapses: per gate, W is the most robust topology in the
study (λ/cx 0.98 vs 2.4–2.7), and at matched budgets W's retention
(0.191/0.5 = 38% at p=0.02) beats GHZ's (0.192–0.304/1.0 = 19–30%). GHZ>ring
survives B (40/40) but fails A (8/10, `middle` placement) and their per-gate
rates are equal within 5% — GHZ>ring is a budget effect (8 vs 12 cx), not
topology.

**L2 — NE-criterion thresholds (GHZ p\* = 0.045 at N=3, 0.0197 at N=4,
0.0098 at N=5).  COLLAPSES as a topology constant.**
Padding GHZ N=3 to W's budget keeps (Q,Q,Q) a pure NE through p=0.05 in the
pre/post placements (baseline flips at 0.045): the p\* values move with gate
budget and placement, so they characterize *the production circuit*, not the
topology. W's "never a pure NE" is a noiseless Month-3 structure fact and
survives everything.

**L3 — "W keeps a positive mean advantage across the whole grid."
SURVIVES, strengthened.** Positive in every realization variant (76–136 cx)
and unchanged by matching (W is the budget target). Adding control C, W is
per-gate the most noise-robust topology of the five. Per-player caveats from
the locked run still apply.

**L4 — "Ring holds the largest positive mean advantage at N=5; GHZ N=5 goes
negative from p≈0.01; W decays to ≈0.001."  PARTIAL — survives compilation
at p≥0.02, not at the claimed onset, and not count-matching.**
The ring>W>GHZ ordering holds across all realization pairs at p=0.02 and
0.05, and GHZ N=5 is negative in every realization by p=0.02 (−0.024 to
−0.034). But the claimed onset "from p≈0.01" is production-specific: at
opt2/3 (14 cx) GHZ N=5 is **+0.424** at p=0.01 (ring>GHZ then fails 12 of 40
variant pairs). Fails A: at matched budgets each pairwise relation holds in
only 6/10 placement×p cells (padded GHZ *beats* W and ring in the pre/post
placements). So the N=5 ordering is a property of the topologies *at their
natural gate budgets* in the p≥0.02 regime, not of the entanglement
structure at fixed noise dose.

**L5 — "Noise kills GHZ's mean advantage at N≥4 mainly by raising the
classical baseline."  SURVIVES — and the controls sharpen it into the
central mechanism.** The advantage cliff is a classical-NE profile switch in
the noisy {D,H} game (GHZ N=4: NE payoff 0.41 → 0.98 between p=0.01 and
0.02 while the Q payoff is nearly intact, 0.97 → 0.94). Near the switch the
metric is knife-edge in *implementation details*: GHZ N=4 at opt3 (10 cx
instead of 12) is **+0.435** at p=0.02 vs **−0.032** in production, and
fully-connected N=4 spans **0.012 ↔ 0.233** across commuting edge-order
shuffles of the same unitary at the same gate count. The collapse *onsets*
are therefore compilation-dependent at both N=4 (production p≈0.015–0.02,
opt3 past 0.02) and N=5 (production p≈0.01, opt2/3 between 0.01 and 0.02);
what is realization-stable is that every GHZ N=4/5 realization is negative
by p=0.05 and p=0.02 respectively.

## Honest reframe

For GHZ/ring/star/fully-connected, the noise-robustness ordering under the
per-gate depolarizing model is **circuit architecture, not entanglement
topology**: equal per-gate decay rates mean the ordering tracks the cx budget
of the chosen synthesis, plus the (implementation-sensitive) timing of
classical-NE switches. Statements of the form "topology X is more
noise-robust than Y" are only licensed in this codebase as "X's production
circuit at its natural gate budget is more robust than Y's" — the README
claims should be (and now are) flagged accordingly. The two results that
survive as genuine structure effects: **W's ~2.5× per-gate robustness**
(inverting its "least robust" reputation) and **W's never-NE status**.
First-look control rows for the two topologies without locked claims: star
is the most robust of all five at N=4/5 at its natural budget (+0.162/+0.091
at p=0.05); fully-connected's production N=4/5 numbers sit on an NE-switch
knife edge and should not be quoted without a realization-spread band.

## Scope

- The claims and controls live in the pinned per-gate depolarizing model
  (p on every u and cx, no idling noise). Under device noise (T1/T2), depth
  and mapping become real variables — that is the hardware-model follow-up,
  not this study.
- "Advantage" everywhere = mean (Q,…,Q) payoff − noisy classical NE payoff,
  the locked run's own metric, evaluated restrictedly ({D,H}^N tensor + Q
  profile + 2N deviations) and anchored to the locked CSV at 1e-14.
- N=2 is excluded (all pairwise topologies coincide with GHZ's J there).

## Reproduction

```
conda run -n entangled-equilibria python scripts/topology_noise_controls.py
```

Gates: locked-CSV anchor (12 cells), dense-unitary equivalence for every
realization variant, exact nulls for mapping and depth. `--smoke` runs an
N=3-only version in ~2 minutes.

---

**Editorial note (2026-07-18, item-11 stale-claim audit):** the L2 verdict
header quotes the locked claim as "NE-criterion thresholds (GHZ p\* = 0.045
at N=3, 0.0197 at N=4, 0.0098 at N=5)". That is the pre-correction README
§9 phrasing this study audited, quoted verbatim. Corrected framing (see
`docs/findings/2026-07-17-item11-stale-claim-audit.md`): with the fixed
GHZ-derived Q, (Q,…,Q) is a pure NE at N=2,3 only, so the N=4/5 values are
advantage-zero crossings (the Nash-flip criterion is inert there); only the
N=3 value 0.045 is an NE-criterion threshold. The study body is unaffected —
its own L2 analysis already scopes NE language to N=3.
