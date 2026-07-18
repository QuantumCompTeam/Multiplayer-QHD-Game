# Item 11 — Stale-claim audit checklist (2026-07-17)

Audit classes: (a) (Q,…,Q)-is-NE claims at N=4/5 — pure quantum NE at N=3
only, N≥4 cliffs are classical-NE switches; (b) unqualified
topology-robustness claims — XX-product ordering is a gate-budget artifact
(λ/cx ≈ 2.1–2.7 at every N), W per-gate robustness (~2.5×, λ/cx ≈ 0.8)
survives with correct framing; (c) old payoff convention V=1000/C=550;
(d) p_eff presented as the best/winning predictor — cz-exponential leads the
registered five-model competition in runs 1–2 (run 1: 10.0, run 2: 7.4),
p_eff third and serving as physical interpretation.

Rules applied: remove/qualify only; registration JSONs untouched; every
number traceable (findings docs, README §9, item-11 spec, or
`results/hardware-scaling/repeat-judgments.json` for run-2 outcomes); no
commits (owner commits after review).

Statuses: CLEAN / EDITED / FLAGGED-FOR-ME / REGISTRATION-FILE-SKIPPED.

---

## README.md — EDITED (confirmed by owner, with 4 amendments)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (b) | 96 | Ring: "Moderate noise robustness: …" unqualified ranking | Removed the robustness qualifier; factual remainder kept |
| 2 | (b) | 115 | Fully-connected "Most noise-sensitive topology due to gate count and accumulated error" | Qualified: "at its natural gate budget — a gate-count effect (O(N²) edges), not a per-gate structural one" + §9 controls pointer |
| 3 | (a) | 268 | Results-table row: GHZ "loses pure-NE status at finite p for N≥3" | Corrected: NE loss at N=3 only; N=4,5 † thresholds are advantage-zero crossings; added gate-budget qualifier for orderings |
| 4 | (d) | 270 | "p_eff=0.0018 … predicts N=4 to 0.004, N=5 to 0.010" as unqualified success | Qualified: registered primary; N=5 miss ≈−5σ reproduced in run 2; cz-exponential leads both runs (run 1: 10.0, run 2: 7.4; cited to repeat-judgments.json) |
| 5 | (a) | 339–341 | "(Q,…,Q) stops being a pure NE at finite noise for every N ≥ 3 (…0.0197 at N=4, 0.0098 at N=5)" | Corrected: pure NE at p=0 only for GHZ N=2,3 (N=3 flip 0.04–0.045); N=4,5 values relabeled advantage-zero crossings; unsupported "most fragile" comparative removed |
| 6 | (d) | 438–441 | "the Month-4 noise model quantitatively predicts real-hardware scaling" | Success framing removed; qualified with registered standing (primary prediction; N=5 −0.010/≈−5σ reproduced; cz-exponential leads 7.4/10.0, p_eff third = physical interpretation). Protocol cited to the frozen competitors doc, outcomes to repeat-judgments.json |
| 7 | (b) | 63 | "— and identifying which topology yields the most robust cooperative equilibrium —" (goal statement presupposing robustness is a topology property) | Removed the clause by owner ruling (initially FLAGGED; resolution: pure removal) |
| 8 | — | 436 | "(single run; …)" inconsistent once run-2 references were introduced by edits 4/6 | Consistency repair by owner ruling: "runs 1–2" |

Class (c): no V=1000/C=550 occurrences (grep clean).

Observations logged, NOT edited (outside classes a–d):
- L137 (§5.2): "Nash equilibrium computation via Nashpy … support enumeration"
  contradicts the §6 table note (Nashpy reserved for 2-player
  cross-validation; N≥3 uses direct best-response enumeration).
- L461: scaling-figure embed points at the run-1 copy
  (`results/hardware-scaling/2026-07-16T074134Z/plots/hardware_scaling.png`);
  newest aggregate is under `2026-07-17T014458Z/` → **feeds item 13**.
- L78, L88 (§4): "Hypothesis:" bullets kept — labeled hypotheses adjudicated
  in §9.

---

## paper/main.tex — EDITED (confirmed by owner, with 3 rulings)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (a)-adj | 39–40 (abstract) | "GHZ loses its cooperative equilibrium fastest" — unsupported comparative (W/ring never have one) | Corrected: "the only topology whose cooperative profile is a pure equilibrium (N=2,3) — loses it at finite noise" |
| 2 | (b) | 40 (abstract) | "retains the largest mean advantage at small N" unqualified | Qualified: gate-budget attribution per matched-count controls; W per-gate exception |
| 3 | (d) | 42–48 (abstract) | "the landscape is *predictive* … predicts N=4 and N=5 to within 0.004 and 0.010" | "Predictive" framing removed; qualified: registered primary; N=4 to 0.004; N=5 over-predicted by 0.010 ≈5σ, reproduced; per-gate law leads registered comparison |
| 4 | (d) | 75–76 (intro) | "show the resulting noise model is quantitatively predictive on hardware" | Qualified: "test the resulting noise model against registered predictions on hardware" |
| 5 | (b) | 85–90 (contrib. 2) | Robustness dichotomy with no implementation qualifier | Qualified: gate-budget attribution appended; controls doc cited in comment |
| 6 | (d) | 91–95 (contrib. 3) | "predicts N=4,5 to ≤ 0.010" | Qualified: registered primary; N=4 0.004; N=5 miss 0.010/≈5σ reproduced; per-gate baseline leads |
| 7 | (a) | 170–174 (TODO) | Port instruction "GHZ NE-loss at finite p for N≥3: 0.045/0.0197/0.0098" | Corrected: NE-loss at N=3 only; N=4/5 values relabeled advantage-zero crossings; port from §9 as corrected 2026-07-17 |
| 8 | (d) | 248–254 | "computed independently of the measured counts … The simulation landscape is therefore quantitatively predictive of hardware." | Removed wrong independence phrase + "therefore predictive" conclusion; qualified with registered story; provenance comment cites both registrations + repeat-judgments.json (run 1: cz 10.0 vs p_eff 31.3; run 2: cz 7.4 vs p_eff 23.4) |
| 9 | (d) | 286–288 (Conclusion TODO) | "the noise model predicts hardware" | Corrected by owner ruling (same logic as #7): "the registered model comparison favors per-gate decay (with the depolarizing fit as its physical interpretation)" |

FLAGGED-FOR-ME (owner ruling: stays flagged, goes to the briefing packet as an
open item — joint decision with Aasa, interacts with venue split):
- L15–16 title: "Entanglement Topology and Noise Determine Quantum Advantage
  …" — noiseless landscape is genuinely topology-determined, but the
  noise-robustness ordering is gate-budget; the title overstates the noise
  axis.

Class (c): none — the "550" at L214 is inside job id `d9c8fpn550hc73dl1tcg`
(false positive).

Observations logged, NOT edited:
- L226 table caption "single run — repeats in progress" and L281 "one
  calibration day" remain accurate (run 2 shares run 1's calibration stamp).
- L20/L23: both author blocks say "VIT Chennai" (owner suspects
  copy-propagation). **Repo-wide `Chennai` grep addendum (3 hits):**
  `paper/main.tex:20`, `paper/main.tex:23`, `README.md:510` (BibTeX note
  "Undergraduate research project, VIT Chennai"). Affiliation correctness is
  an authorial fact the audit cannot verify — left for the owner.

---

## paper/README.md — EDITED (confirmed by owner)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (d) | 4–5 | "the hardware scaling run is the validation that the landscape is predictive" | Qualified: "tests the registered predictions (the registered model comparison favors per-gate decay, with the depolarizing fit as its physical interpretation)" |
| 2 | (c) | 20–21 | "the 2026-07-02 n-scaling run used V=1000/C=550" — true but understated; verified ALL 7 n-scaling runs (through 2026-07-16) and all 5 gamma-sweep runs are old-convention | Qualified with the verified scope (config.snapshot.yaml evidence) |

Observations: `figs/hardware_scaling.pdf` sourced from run-1 copy (L30);
refresh from the 2-run aggregate per the file's own protocol (item 13).

---

## experiments/config.yaml — EDITED (pulled forward by owner ruling)

| # | Class | Line (pre-edit) | Stale content | Action |
|---|---|---|---|---|
| 1 | (c) | 70, 73 | Live harness default `V: 1000` / `C: 550` — ACTIVE contamination source; explains why the 2026-07-16 n-scaling runs were still old-convention. Field comments themselves state defaults 4.0/3.0 | Corrected to `V: 4` / `C: 3` (one-line value corrections per owner ruling) |

Observation: commented-out sweep EXAMPLES at L82–83 (`# V: [4, 100, 1000]`,
`# C: [3, 55, 550]`) include the old values as illustrative sweep points —
left as-is (examples, not the convention in use); flag if you want them
scrubbed.

---

## paper/references.bib — CLEAN

Pure bibliographic metadata: no class (a)/(b)/(c)/(d) content. The
flitney2002 year discrepancy (README cites 2002; PLoS ONE version is 2012)
is already self-flagged with a TODO note in the entry — bibliographic
metadata, not a stale claim; left to the authors.

---

## docs/formulae.md — EDITED (confirmed by owner)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (a) | 302–304 | §8 never-Nash footnote parenthetical "(fixed-mode `Q_GHZ` on a non-GHZ topology)" presents non-GHZ as the only never-Nash case, implying (Q,…,Q) is a pure NE on GHZ at every N; GHZ N=4,5 series are also never-Nash (pure quantum NE at N=2,3 only), which is why the published N=4/5 thresholds are advantage-zero crossings | Qualified: "(fixed-mode `Q_GHZ` on a non-GHZ topology, and GHZ itself at N ≥ 4)" — minimal insertion |

Class (b): clean — §8 "noise cost scales with entangling gate count" is
already the correct gate-budget framing; no robustness-ordering claims.
Class (c): clean — no V=1000/C=550 occurrences (convention stated
symbolically as `C > V/2`).
Class (d): clean — no p_eff / hardware-prediction content.
Chennai: no hits.

Verification: §8 `p*` prose checked against `src/experiment/plots.py`
`extract_pstar` (L257–300) — mechanics match the code (interpolated
advantage crossing, Nash flip at grid point, None → "> p_max", never-Nash
surfaced by caller); only the parenthetical was stale.

**Tier-2 candidate logged (owner instruction):** the `extract_pstar`
docstring itself (`src/experiment/plots.py` ~L257–300) attributes never-Nash
to "a Month-3 fixed-mode finding" — same non-GHZ-only implication as the
formulae.md parenthetical; qualify the same way (GHZ N ≥ 4 is also
never-Nash) when the Tier-2 sweep reaches src/.

---

## Discrepancy record: run-order reversal in score lists (resolved by owner ruling)

Found while verifying TODOS.md L37 against
`results/hardware-scaling/repeat-judgments.json`. Authoritative values:
run 1 (2026-07-16T074134Z) cz-exponential 10.032 / p_eff 31.296;
run 2 (2026-07-17T014458Z) cz-exponential 7.400 / p_eff 23.371. The
already-applied audit edits listed "7.4" first under a "runs 1–2" label,
implying run 1 = 7.4 — reversed. TODOS.md itself had the attribution right.

Likely error source (owner note): the session summary's label-free ranking
list presented the run-2 scores without run attribution, and the audit
edits inherited that ordering.

Repairs applied (explicit labels, owner-approved):
- `paper/main.tex` provenance comment (pre-repair L277–279) → "(run 1:
  cz 10.0 vs p_eff 31.3; run 2: cz 7.4 vs p_eff 23.4)".
- `README.md` L447–448 → "(scores 10.0 and 7.4 in runs 1 and 2)".
- This document: class-(d) header definition, README entry #4, and
  paper/main.tex entry #8 relabeled the same way.

Scope: the cz↔p_eff pairing was consistent everywhere (7.4↔23.4,
10.0↔31.3) and the substantive claims (cz-exponential leads both runs;
p_eff third) were unaffected; only the run attribution was reversed.

---

## TODOS.md — CLEAN (confirmed by owner)

| # | Class | Line | Item checked | Result |
|---|---|---|---|---|
| — | (a) | — | No (Q,…,Q)-is-NE claims at any N | clean |
| — | (b) | — | No topology-robustness claims | clean |
| — | (c) | — | No V=1000/C=550 occurrences | clean |
| — | (d) | 37, 47–52 | L37 correctly names cz-exponential best registered predictor for run 2; L47–52 describe p_eff as the registered *primary test* — protocol fact, not a winning-model claim | clean |

Verification against `repeat-judgments.json`:
- L37 "(7.4 vs p_eff 23.4)" for run 2 — correct (7.400 / 23.371); this
  check exposed the run-order discrepancy recorded above.
- L36 run-2 z-values: N=4 −0.93 conditional PASS, N=5 −4.74 FAIL,
  same-sign-as-run-1 true — all match.
- L57 run-1 N=5 deficit "−0.0101, z=−5.2" — matches registered_run1_delta
  −0.01005 / z −5.167.
- L42 judge flag name `distinct_calibration_vs_previous_runs` — matches the
  JSON field exactly.
- L31 "registration anchor" — consistent with `is_registration_source: true`.

Citation-rule check: run-2 outcomes cite the judge/repeat-judgments path
(L54–59); preregistration.json and the frozen findings doc cited for
protocol only (L47–50) — compliant.

Chennai: no hits.

---

## docs/findings/2026-07-05-t9-adaptation-fairness.md — CLEAN (confirmed by owner; dated/historical, flag-only tier)

| # | Class | Line | Item checked | Result |
|---|---|---|---|---|
| — | (a) | 43–44 | "(Q_N,…,Q_N) is *not* a Nash equilibrium for the W entangler even noiselessly" — correct never-Nash statement (matches corrected framing and formulae.md §8's non-GHZ case); no (Q,…,Q)-is-NE claims | clean |
| — | (b) | 87–91 | "structural feature of the entangler circuit" — within-topology position-locked asymmetry, already implementation-level attribution, not a cross-topology robustness ranking | clean |
| — | (c) | 29 | "V=4, C=3" current convention; baseline anchored to `results/noise-robustness/2026-07-03T0213Z` (verified current-convention list) | clean |
| — | (d) | — | No p_eff / hardware-prediction content | clean |

Factual-correctness check (this tier's stop-and-report trigger — not
tripped): results table matches the TODOS.md pilot summary exactly;
cross-references to the "noise-aware strategy optimization" TODO and the
"headline asymmetry cases (W N=5, ring N=5)" phrasing hold; the doc already
self-qualifies (PROVISIONAL header, rule pending Aasa's sign-off, excluded
from README §9).

Chennai: no hits.

---

## docs/findings/2026-07-16-topology-vs-implementation-controls.md — FLAGGED-FOR-ME (1 flag; never-edit tier; owner ruling recorded)

| # | Class | Line | Item | Ruling |
|---|---|---|---|---|
| 1 | (a) | 75–76 | L2 verdict header quotes the locked claim as "NE-criterion thresholds (GHZ p\* = 0.045 at N=3, 0.0197 at N=4, 0.0098 at N=5)" — the "NE-criterion" label on the N=4/5 values implies (Q,…,Q) had NE status to lose there; corrected: advantage-zero crossings (never-Nash at N≥4). It is a quotation of the pre-correction README §9 claim this study audited; the README source was corrected by this audit (README entry #3) | Owner: add a **dated editorial note post-audit** (queued on the closeout list with the Chennai pass); note text to identify the quote as the pre-correction README §9 phrasing this study audited and point to the item-11 audit for the corrected framing. NOT edited during the sweep. |

Clean on the other in-scope classes:
- (c): no V=1000/C=550; payoff-scale numbers consistent with V=4/C=3;
  anchored to current-convention locked run `2026-07-03T0213Z`.
- (d): no p_eff / hardware-prediction content.

Observations (no action): the L5 verdict is itself the corrected N≥4
classical-NE-switch story and the L2 body keeps NE language correctly
scoped to N=3; L125 "should be (and now are) flagged" remains true after
the audit's README edits; λ/cx table matches the audit header summary.
Class (b) content (L1/L4) not assessed per owner scoping — this doc is the
authority the class-(b) corrections cite.

Chennai: no hits.

---

## docs/superpowers/ clean batch — CLEAN (confirmed by owner; 5 of 7 files)

| File | Classes checked | Notes |
|---|---|---|
| specs/2026-06-08-ewl-scaffold-design.md | a,b,c,d | N=2 Q-is-NE claims only (correct); V=4/C=3 throughout; topologies are stubs, no robustness claims |
| specs/2026-06-09-n3-ghz-extension-design.md | a,b,c,d | All NE claims scoped to N=3 (correct, incl. the `Q_N = U(0,π/N,π/N)` FINDING block); V=4/C=3 |
| specs/2026-07-01-noise-analysis-design.md | a,b,c,d | GHZ-vs-W framed as question, "reported, not assumed"; p\* criterion generic; T8 [x] / T9 [ ] match TODOS.md |
| specs/2026-07-02-w-entangler-gate-level-design.md | a,b,c,d | Old ordering quoted only as "may move — do not carry forward" (§4.2) |
| plans/2026-07-02-w-entangler-gate-level.md | a,b,c,d | Old README text quoted only as replace-target instructions (Task 4, executed) |

Chennai: no hits in any of the 7 superpowers files.

---

## docs/superpowers/plans/2026-06-08-ewl-scaffold.md — FLAGGED-FOR-ME (1 flag; owner ruling: flag-only)

| # | Class | Line | Stale claim | Ruling |
|---|---|---|---|---|
| 1 | (b) | 672–673 | `w_entangler` stub docstring in the Task-9 file listing: "pairwise entanglement survives single-qubit loss (more noise-robust than GHZ for N > 4)" — unqualified cross-topology robustness claim (design-time literature hypothesis; under the controls study, absolute ordering is gate-budget and W was last in absolute terms in Month 4; only the per-gate framing survives) | Flag-only (dated implementation plan — historical record of the June stub text). **Tier-2 candidate kept logged:** verify the current `src/circuits/topologies.py` `w_entangler` docstring does not retain this sentence |

Observation (outside classes, no action): the `ghz_entangler` stub docstring
in the same listing (L662–664) describes the H+CNOT construction that the
Month-2 spec later rejected for the X^⊗N formula — stub predates the
decision, logged only.

---

## docs/superpowers/specs/2026-07-16-hardware-scaling-mitigation-design.md — EDITED (confirmed by owner, with changelog ruling)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (d) | 15–16 | §1 Goal 2: predictions "computed from data *independent of the hardware counts*" — false for prediction (b): the effective p is fitted to the run's own N=3 hardware point (as "fit-one-predict-two" admits). Same wrong independence phrase the audit removed from paper/main.tex (entry #8); this spec is where the paper inherited it | Edited: "computed without reference to the N=4/5 counts being predicted". Per owner ruling, a dated changelog block was appended to the spec so spec-as-approved vs spec-as-corrected stays distinguishable |

**Noted for item 14 (owner instruction):** §2 "Honesty constraints" is the
canonical corrected class-(a) phrasing for reuse — "(Q,…,Q) is a **pure NE
only at N=3**. At N=4 a unilateral Hawk deviation pays 2.0 > 1.0; at N=5,
2.618 > 0.8 (fixed GHZ-derived Q_N; Month-3 finding)" with NE status as a
per-N simulation annotation in every figure caption.

Everything else clean; §4's "advantage stays well above 0 at all N" held up
in both runs.

---

## src/experiment/plots.py — EDITED (confirmed by owner; Tier 2)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (a) | 273–274 | `extract_pstar` docstring: never-Nash "…is a Month-3 fixed-mode finding, not noise fragility" — the logged Tier-2 candidate; the attribution evokes only the Q_GHZ-on-non-GHZ-topology case, implying GHZ series always have Nash status to lose (GHZ N≥4 is also never-Nash) | Qualified: "…a Month-3 fixed-mode finding (non-GHZ topologies, and GHZ itself at N >= 4), not noise fragility" — owner ruling: phrasing matches formulae.md §8 exactly (commas, no em-dashes) |

Rest of file clean, incl. caption generators: "(filled = (Q,..,Q) is
Nash)" / "'\*' = (Q,..,Q) is Nash" figure annotations are data-driven
per-cell markers (`q_is_nash`), honest at every N. No V/C literals, no
p_eff, no robustness orderings. Docstring-only edit → no Tier-3
regeneration note needed.

**Addendum (2026-07-18, discrepancy caught and resolved by owner ruling):**
the entry above missed the y-axis label "quantum advantage (QNE − CNE)"
(L110/202/385) — the "QNE" acronym compresses the Q-profile-is-NE claim
into every figure. Caught during the report.py/nash.py pass, reported as a
discrepancy rather than silently amended. Ruling: relabel all four QNE
sites (3 here + report.py per-cell line) to "Q-profile − classical NE" —
"figures must not assert what the text denies." Applied. The "no Tier-3
regeneration note needed" line above no longer holds — existing run plot
PNGs carry the old label; see the Tier-3 propagation queue.

---

## src/circuits/topologies.py — CLEAN (confirmed by owner; Tier 2)

**Logged candidate resolved NEGATIVE:** the implemented `w_entangler`
docstring (L191–206) does not retain the scaffold-plan stub's "more
noise-robust than GHZ for N > 4" — the stub text was replaced at
implementation. Classes (a)/(c)/(d) also clean; no Chennai.

Observation (outside classes, no action): `w_entangler` NOTE at L203–205
("confirm against the intended physics before publishing Month-3 W-state
results") predates T8 spec D-T8.1 (keep the S_W semantics, decided
autonomously, "revisit if disagreed") → added to the Aasa briefing list
below per owner ruling.

---

## src/circuits/ewl.py — EDITED (confirmed by owner; Tier 2)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (a) | 89, 106–108, 114 | `q_strategy` docstring: "the N-player quantum Nash equilibrium strategy"; "This is a Nash equilibrium: any unilateral deviation to D or H yields strictly less than V/N" — **factually false at N≥4** (Hawk deviation pays 2.0 > 1.0 at N=4, 2.618 > 0.8 at N=5; Month-3 finding); "the quantum Nash strategy scales as pi/N" | One coherent edit: "GHZ-derived quantum strategy"; "pure Nash equilibrium at N=2,3 only: for N >= 4 a unilateral Hawk deviation beats V/N (2.0 vs 1.0 at N=4, 2.618 vs 0.8 at N=5 — Month-3 finding…)"; "the quantum strategy scales as pi/N" |

State-collapse derivation (all-Dove w.p. 1 → V/N at every N) correct,
untouched. L29/L85 already correctly scoped to N=2.

---

## src/experiment/report.py — EDITED (confirmed by owner; Tier 2; caption generator → Tier-3 propagation)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (a) | 268–269 | Never-Nash † footnote generator: "…a Month-3 finding about the topology, not noise fragility" — wrong for the GHZ N=4/5 rows the † marks | Qualified with the agreed phrasing: "…a Month-3 fixed-mode finding (non-GHZ topologies, and GHZ itself at N >= 4), not noise fragility" |
| 2 | (b) | 281 | RQ3 headline banner unqualified over "→ X degrades faster" verdicts | Banner qualified (compact form per owner ruling): "…measured, not assumed; at production gate budgets — see docs/findings/2026-07-16-topology-vs-implementation-controls.md" (verdict strings unchanged; banner scopes them) |
| 3 | (a) | 406 | Per-cell line "Advantage (QNE − CNE, mean)" | Relabeled "Advantage (Q-profile − classical NE, mean)" per the QNE ruling |

---

## src/game/nash.py — EDITED (confirmed by owner; Tier 2; minimal naming edits)

| # | Class | Line (pre-edit) | Item | Action |
|---|---|---|---|---|
| 1 | (a)-adj | 12 | "the N-appropriate quantum Nash strategy" (module docstring) | → "quantum strategy" |
| 2 | (a)-adj | 18 | API summary "compute_advantage -- quantum NE payoff vs classical NE payoff" | → "Q-profile payoff vs classical NE payoff" |
| 3 | (a)-adj | 49–50 | "the N-appropriate quantum Nash strategy for the GHZ entangler" (`_strategy_map`) | → "quantum strategy" |

No explicit N=4/5 claims; naming inherited from pre-Month-3 usage. Rest of
module clean and careful (L162 "may stop being Nash" is generic,
data-driven).

---

## src/ clean batch — CLEAN (confirmed by owner; 16 files + 4 __init__.py)

`payoffs.py`, `gate_level.py`, `noise.py`, `topology_graphs.py`,
`topology_registry.py`, `topology_viz.py`, `experiment/config.py`,
`experiment/sweep.py` (only `is_nash` field plumbing), `cpu_limit.py`,
`results_io.py`, `hardware/chain.py`, `hardware/mitigation.py`,
`two_player.py` (N=2-scoped, correct), `n_player.py`, `config.py`
(N=2-scoped comment, correct), `strategy_opt.py` (certification machinery,
honest `is_nash` reporting). Class (c): only "1000" in src/ is an optimizer
`maxiter` (false positive). Classes (d), Chennai: zero hits src-wide.

Observation (no action): n_player.py:95 "Must equal pi/2 for Nash
equilibrium property to hold" — necessary-condition phrasing, no N=4/5
claim.

---

## experiments/hardware_scaling.py — EDITED (confirmed by owner; Tier 2)

| # | Class | Line (pre-edit) | Stale claim | Action |
|---|---|---|---|---|
| 1 | (d) | 388 | Section comment "── predictions (independent of the hardware counts) ───" — same wrong independence phrase as the spec/paper; the section's own `effective_p_prediction` fits to the measured N=3 payoff | → "── predictions (computed without reference to the N=4/5 counts being predicted) ──" |

Rest already corrected framing: L33 "cooperative profile, not an
equilibrium claim at N=4,5"; L431–434 "Fit-one-predict-two: no N=4/5
information used".

---

## scripts/n3_advantage.py — EDITED (owner ruling; Tier 2)

| # | Class | Line (pre-edit) | Item | Action |
|---|---|---|---|---|
| 1 | (a)-adj | 6, 41 | Docstring "advantage = quantum NE - classical NE" and printed label "Advantage (QNE - CNE)" — N=3-scoped, where (Q,Q,Q) IS a pure NE, so factually true in context | Relabeled anyway: "Q-profile - classical NE" / "Advantage (Q-profile - CNE)" (column alignment preserved). Audit recommended leave-as-is (label true at N=3); **owner overruled**: post-audit invariant is that "QNE" greps to zero live sites, so any future occurrence is an instant flag |

---

## scripts/ clean batch — CLEAN (confirmed by owner; 14 of 15 files)

All four classes + Chennai clean. Notable verifications:
- `plot_hardware_scaling.py` (caption generator): generated caption already
  carries the corrected class-(a) annotation ("(Q,…,Q) is a pure Nash
  equilibrium only at N=3; at N=4,5 the profile is the cooperative quantum
  profile, not an equilibrium") and honest class-(d) framing ("predictions,
  not fits"). Newest generated captions are compliant.
- `preregister_peff.py` / `preregister_baselines.py` / `judge_repeat_run.py`:
  "primary" = registered-protocol fact; competition "clearly separated from
  the primary p_eff test" on a shared sigma yardstick — compliant.
- `topology_noise_controls.py` is itself the class-(b) authority.
- t9 scripts print the correct never-Nash caveat.
- Class (c): only "550" is inside job id `d9c8fpn550hc73dl1tcg`.

---

## experiments/ clean batch — CLEAN (confirmed by owner; 5 of 6 files)

`config.yaml` (EDITED earlier — pulled-forward V/C fix; strategy-mode docs
honest), `noise-sweep.yaml`, `hardware_n3_ghz.py`, `hand_built_j.py`,
`fetch_result.py`. No class hits, no Chennai.

---

## tests/ clean batch — CLEAN (confirmed by owner; all 15 test files)

Nash claims N=2/N=3-scoped where true, or explicitly honest about
non-existence (`test_strategy_opt`, `test_noise` never-Nash logic).
"10000 shots" is the only numeric hit (false positive). No robustness
orderings, no p_eff, no Chennai.

---

**Tier 2 closed.** The independence-phrase propagation chain — hardware
spec §1 → paper/main.tex §results → `experiments/hardware_scaling.py`
section comment — is now fully repaired at all three links.

---

## Tier-3 propagation queue (caption-generator fixes; "fixed at source, regenerates on next run")

- Noise-swept run `report.md` files (locked run
  `results/noise-robustness/2026-07-03T0213Z`, plus any other noise-swept
  runs): old † never-Nash footnote ("about the topology") and unqualified
  RQ3 banner — fixed at source in `src/experiment/report.py` (edits 1–2).
- All run plot PNGs with the "(QNE − CNE)" y-axis label
  (`advantage_vs_N`, `advantage_vs_gamma`, `per_player_advantage_*` across
  results/ runs) — relabeled at source in `src/experiment/plots.py`.
- Run `report.md` per-cell lines "Advantage (QNE − CNE, mean)" — fixed at
  source in `src/experiment/report.py` (edit 3).

---

## results/README.md — CLEAN (confirmed by owner; Tier 3, EDIT tier — no class findings)

Class (a): L35 "Q-NE ((Q,…,Q) is Nash)" is a legend describing the CSV
encoding, data-driven per cell. Classes (b)/(c)/(d), Chennai: clean.

Observations (outside classes, log only — **routing per owner ruling**):
- Coverage gap (documents only month2/month3 dirs; 8 more experiment dirs
  exist) → **routes to item 19 scope**.
- Regeneration commands use `.venv/bin/python` vs the pinned
  `entangled-equilibria` conda env — a wrong-env regeneration risk →
  **routes to item 17 scope**.

---

## Generated run reports & plots — FLAGGED (confirmed by owner; Tier 3, flag-only; propagation queue applied)

| Artifact set | Stale content | Note |
|---|---|---|
| `results/noise-robustness/2026-07-03T0213Z/report.md` (locked) and `2026-07-02T1212Z/report.md` (pre-T8, superseded) | Old † never-Nash footnote ("a Month-3 finding about the topology"), old unqualified RQ3 banner, 132 "Advantage (QNE − CNE, mean)" lines each | All three fixed at source (report.py edits 1–3); regenerates on next run. Locked reports NOT edited |
| 13 other `report.md` (gamma-sweep N2–N6; n-scaling-advantage ×8 incl. 2026-06-18 run pending addendum-B verification) | "Advantage (QNE − CNE, mean)" per-cell lines (614 QNE occurrences results-wide) | Fixed at source (report.py edit 3). All on the verified old-convention class-(c) list (item 13): their V=1000/C=550 values are **truthful records of old-convention runs** — flag-only |
| All run plot PNGs (`advantage_vs_N`, `advantage_vs_gamma`, `per_player_advantage_*`) | "(QNE − CNE)" y-axis label baked into images | Fixed at source (plots.py relabel); regenerates on next run |
| `results/hardware-scaling/*/plots/caption.md` (both runs) | — | Verified compliant ("pure Nash equilibrium only at N=3", "predictions, not fits") — no flags |
| `results/hardware-n3/…`, `results/t9-pilot/*` | — | N=3-scoped generator / data-only JSONs — no flags |

---

## results/hardware-scaling/repeat-judgments.json — CLEAN (confirmed by owner; Tier 3, flag-only tier)

Fully read during the TODOS.md verification pass. Embedded `note` field
frames the competition correctly ("separate from the primary p_eff test");
rankings are data (cz_exponential first in both runs). No stale claims.
This file is the designated citation target for run-2 evidence.

---

## Registration files — REGISTRATION-FILE-SKIPPED (confirmed by owner; class-(d) inspection only; NEVER edited)

| File | Class-(d) inspection result |
|---|---|
| `results/hardware-scaling/preregistration.json` | Compliant: `purpose` is honest fit-one-predict-two framing ("predictions committed BEFORE any repeat batch run"); primary test described as protocol; no winning-model claims |
| `results/hardware-scaling/preregistration-baselines.json` | Compliant: "SECONDARY to the primary p_eff registration", shared-yardstick scoring, "the primary p_eff model competes on the same score" |

Both untouched, consistent with the standing rule and the judge's HEAD-check.

---

## Frozen registration findings docs — CLEAN (confirmed by owner; flag-only tier; no flags)

- `docs/findings/2026-07-16-preregistered-peff-scaling-predictions.md`:
  declares run-1 tension openly (N=5 z −5.17), pre-commits falsification,
  self-enforces immutability ("corrections go in a new dated file"); "550"
  at L4 is the job id (false positive).
- `docs/findings/2026-07-16-preregistered-baseline-competitors.md`: CLEAN
  and itself the source of the corrected class-(d) framing ("the honest
  headline is 'advantage decays per two-qubit gate', not 'the depolarizing
  model predicts the scaling'"); item-5A declared-in-advance interpretation
  intact.

---

## audit-report-20260616-1834.md — CLEAN (confirmed by owner; flag-only tier; historical)

Located at repo root (not docs/ — noted for the record). All Nash
statements are N=2/3-era and period-accurate; "quantum Nash strategy"
naming (L53, L121) predates the Month-3 N≥4 finding — historical record,
no action. No (b)/(c)/(d)/Chennai hits.

---

## graphify-out/ — CLEAN (confirmed by owner; flag-only tier; generated snapshot)

`GRAPH_REPORT.md` node labels correctly scoped ("Q strategy (N=2 quantum
Nash)"). Generated pre-audit knowledge-graph snapshot (plus stored query
answer under `memory/`); any embedded pre-correction phrasing regenerates
on the next graphify run. No flags.

---

**Sweep proper closed (Tiers 1–4).** Addendum steps A–D follow.

---

## Aasa briefing list (accumulating; open items for joint decision)

1. **paper/main.tex title** (L15–16) — "…Noise Determine Quantum
   Advantage…" overstates the noise axis (robustness ordering is
   gate-budget). FLAGGED-FOR-ME, owner ruling: joint decision with Aasa,
   interacts with venue split (from the paper/main.tex entry).
2. **S_W physics sign-off (D-T8.1)** — `w_entangler`'s
   gamma-interpolation semantics (the |0…0⟩↔|W⟩ reflection) were kept by
   an autonomous decision in the T8 spec ("revisit if disagreed"); the
   docstring NOTE at `src/circuits/topologies.py:203-205` still asks for
   physics confirmation. Owner ruling 2026-07-17: open item for Aasa.
3. (Pre-existing, tracked in TODOS.md/t9 doc, listed for completeness:)
   t9 adaptation-rule sign-off — "independent round-robin best response"
   is provisional.
4. **Affiliation exact format** (owner ruling 2026-07-18): "VIT Vellore"
   vs the full formal "Vellore Institute of Technology, Vellore, India" —
   to be settled jointly with Aasa at submission time; the factual error
   (Chennai) is what was fixed in the addendum-A pass.

---

## Closeout queue (accumulating; executed after the sweep)

1. **Chennai → VIT Vellore fix pass** — **EXECUTED 2026-07-18** (addendum
   step A, owner go). Repo-wide grep confirmed exactly the 3 known live
   hits, no new ones; fixed: `paper/main.tex:20`, `paper/main.tex:23`,
   `README.md:510` → "VIT Vellore". The audit doc's own quoted records
   were excluded (history, not live claims).
2. **Dated editorial note in
   `docs/findings/2026-07-16-topology-vs-implementation-controls.md`** —
   **EXECUTED 2026-07-18** (owner ruling on flag #1 above): appended a
   dated editorial note identifying the L2 quote as the pre-correction
   README §9 phrasing this study audited, pointing to this audit for the
   corrected framing (advantage-zero crossings; NE-criterion only at N=3);
   study body untouched.

---

## Addendum records

**A — Chennai grep + fix pass (2026-07-18, executed on owner go).**
Repo-wide grep: exactly the 3 known live hits (`paper/main.tex:20`, `:23`,
`README.md:510`), no new ones; all fixed to "VIT Vellore". The audit doc's
own quoted records excluded (history, not live claims). Exact-format
decision (short vs full formal name) routed to the Aasa briefing list
(item 4).

**B — 2026-06-18 n-scaling run payoff convention (2026-07-18, resolved).**
`results/n-scaling-advantage/2026-06-18T0930Z/config.snapshot.yaml`: all
24 cells (N=2–6 × 5 topologies) carry V=4.0 / C=3.0, γ=π/2, {D,H,Q} —
**current convention**. Corroborated by the run's results.csv (N=3 GHZ
row: V=4.0, C=3.0, advantage 1.0 = C/N, q payoff 4/3, classical NE 1/3).
The run moves OFF the old-convention item-13 list onto the
current-convention list. Chronology note: this 06-18 run predates the
old-convention 07-02 runs — consistent with the contamination source being
the `experiments/config.yaml` V:1000/C:550 defaults (introduced after
06-18, fixed this audit).

**C — results/topology/ V-convention (2026-07-18, resolved: vacuous).**
No config.snapshot.yaml because it is not a run directory: it is the
shared, overwritten diagram folder written by
`topology_viz.write_topology_folder` (invoked outside the per-run flow —
see the report.py comment excluding it from run dirs). Its "config source"
is code constants (topology_graphs edge sets + the J·U·J† circuit
structure), not the experiment config. Verified V/C-free at three levels:
(i) generator — `topology_viz.py` has no V/C/payoff/config usage;
(ii) content — artifacts are graph drawings and circuit diagrams (e.g.
`ewl_N3.txt` is the bare J→U⊗3→J† circuit), no payoff numbers anywhere;
(iii) hence no data-level convention exposure exists to check. Off the
item-13 convention list entirely. Filesystem dates show writes on
2026-07-02 and 2026-07-16 (inside the regression window) — irrelevant
given V/C-independence.

**Incidental finding (C):** `results/topology/` is NOT in git — blanket
ignore rule `results/` (.gitignore:47) and never force-added, unlike the
committed run dirs. This contradicts results/README.md's "these artifacts
are committed to git as part of the research record" for this folder, and
its figures cannot be cited from git history. Routing decision deferred to
the closing summary (candidates: item 17 infra-risk or item 19 docs
scope).

---

## Figure references for item 13 (accumulating)

**Policy decision pending (owner):** superseded old-convention runs may be
retired-with-note rather than regenerated; only cited artifacts need
regeneration.

**Provenance (addendum B, 2026-07-18):** the old-convention set is a
**bounded config regression**, not drift — exactly 12 directories (7
n-scaling + 5 gamma-sweep) inside the window between 2026-06-18 (verified
current-convention) and 2026-07-02 (first old-convention run), caused by
the `experiments/config.yaml` V:1000/C:550 defaults and fixed 2026-07-17
by this audit. Retire-with-note can therefore cite cause and window, not
just "old runs"; nothing about those runs is scientifically suspect except
the payoff scale.

- README.md L461: embeds run-1 `hardware_scaling.png`; the auto-aggregated
  2-run figure lives in `results/hardware-scaling/2026-07-17T014458Z/plots/`.
- `paper/figs/hardware_scaling.pdf`: sourced from run-1 copy; refresh from
  the 2-run aggregate.
- **Old-convention (V=1000/C=550) figure-bearing runs, verified via
  config.snapshot.yaml:** the seven 2026-07 `results/n-scaling-advantage/*`
  runs (2026-07-02T0444Z/0525Z/0538Z/1247Z/1757Z, 2026-07-16T0736Z/0738Z)
  and all `results/gamma-sweep/N2..N6` runs (advantage_vs_gamma, heatmaps,
  per-player plots).
- Current-convention (V=4/C=3), no regeneration needed:
  `results/noise-robustness/2026-07-03T0213Z`, hardware runs, t9-pilot,
  and `results/n-scaling-advantage/2026-06-18T0930Z` (resolved by
  addendum B — V=4/C=3 verified in all 24 cells).
- `results/topology/` — **resolved by addendum C (2026-07-18): V-convention
  vacuous.** Shared diagram folder from `topology_viz.write_topology_folder`
  (topology graphs + EWL circuit structure only); the generator provably
  uses no V/C and the artifacts contain no payoff numbers. Off the
  convention list entirely. See the addendum-C record for the
  not-committed-to-git finding.
- Root cause of ongoing contamination fixed this audit:
  `experiments/config.yaml` defaults (entry above).

---

## Closing summary (addendum D, 2026-07-18) — AUDIT COMPLETE

### Totals per class (edits vs flags)

| Class | Edited (files) | Sites | Flags |
|---|---|---|---|
| (a) incl. (a)-adjacent | 8 — README.md, paper/main.tex, docs/formulae.md, src/experiment/plots.py, src/circuits/ewl.py, src/experiment/report.py, src/game/nash.py, scripts/n3_advantage.py | ~17 (incl. the 4-site QNE relabel + n3 sites) | controls-doc L2 quote (resolved: dated editorial note, executed) |
| (b) | 3 — README.md, paper/main.tex, src/experiment/report.py | 6 | scaffold-plan `w_entangler` stub (flag-only, historical); paper title (→ Aasa list) |
| (c) | 2 — paper/README.md, experiments/config.yaml (**root cause**) | 3 | 12 old-convention run dirs (truthful records; → item 13) |
| (d) | 5 — README.md, paper/main.tex, paper/README.md, hardware-scaling spec, experiments/hardware_scaling.py | 10 | registration files inspected-compliant, SKIPPED |

Cross-cutting actions: run-order discrepancy repair (README, main.tex, this
doc — explicit run labels); Chennai → VIT Vellore (3 sites); **QNE
invariant established: "QNE" greps to zero live code/doc sites — any future
occurrence is an instant flag**; Tier-3 propagation queue (all generated-
artifact staleness fixed at source, regenerates on next run);
independence-phrase chain repaired at all three links (spec → paper →
experiment code).

### FLAGGED-FOR-ME / open decisions

1. **Paper title** (noise axis overstated) — Aasa + venue split.
2. **S_W physics sign-off** (D-T8.1) — Aasa.
3. **t9 adaptation-rule sign-off** — Aasa (pre-existing).
4. **Affiliation exact format** (short vs full formal) — Aasa, at
   submission.
5. **experiments/config.yaml L82–83** commented sweep examples still show
   old values (`# V: [4, 100, 1000]` / `# C: [3, 55, 550]`) — scrub or
   keep as illustrative.
6. **results/topology/ not in git** — RESOLVED (owner ruling 2026-07-18):
   routed to **item 19** (presentation artifact, V/C-free, regenerates
   from code constants; fix = force-add or soften results/README wording
   at go-public time).
7. **Item-13 policy**: retire-with-note vs regenerate for the 12
   old-convention dirs.
8. flitney2002 year (references.bib self-flagged TODO) — authors.

### Item-13 handoff (verified old-convention directory list)

**Exactly 12 directories, verified via config.snapshot.yaml:**
`results/n-scaling-advantage/` 2026-07-02T0444Z, 0525Z, 0538Z, 1247Z,
1757Z; 2026-07-16T0736Z, 0738Z (7) + `results/gamma-sweep/` N2, N3, N4,
N5, N6 (5).

**Provenance (the sentence that makes the policy call easy):** these are a
**bounded config regression** — `experiments/config.yaml` V:1000/C:550
defaults introduced between 2026-06-18 (run verified current-convention,
addendum B) and 2026-07-02 (first contaminated run), fixed 2026-07-17 by
this audit. Nothing about the runs is scientifically suspect except the
payoff scale; a retire-note can cite cause, window, and fix. Cleared as
current-convention or convention-free: 2026-06-18T0930Z (B),
`results/topology/` (C, vacuous). Also on the item-13 plate: README L461
scaling-figure embed → 2-run aggregate; `paper/figs/hardware_scaling.pdf`
refresh; the Tier-3 propagation queue (QNE plot labels, report footers/
banners) regenerates with whichever runs item 13 chooses to regenerate.

### Process notes for the record

- The mid-sweep **pull-forward of experiments/config.yaml** (a live
  contamination vector outranking historical staleness) was retroactively
  vindicated by addendum B: the vector had already burned 12 runs inside a
  five-week window.
- Verification standard held throughout: claims traced to
  registration-frozen sources or **data-level checks that cannot be faked
  by stale metadata** (advantage = C/N exactly; z-values recomputed from
  repeat-judgments.json; bit-exact p_eff reproduction gates).
- Run-2 evidence cites `repeat-judgments.json` exclusively; both
  registration files verified untouched (judge HEAD-check intact).

---

*Audit COMPLETE 2026-07-18: Tiers 1–4 swept (docs, paper, src, scripts,
experiments, tests, results artifacts, registrations, historical docs,
graphify-out), addendum steps A–D executed. Every entry above was appended
after owner confirmation; open decisions are enumerated in the closing
summary. Nothing committed — owner commits after review.*
