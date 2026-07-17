# Item 11 — Stale-claim audit checklist (2026-07-17)

Audit classes: (a) (Q,…,Q)-is-NE claims at N=4/5 — pure quantum NE at N=3
only, N≥4 cliffs are classical-NE switches; (b) unqualified
topology-robustness claims — XX-product ordering is a gate-budget artifact
(λ/cx ≈ 2.1–2.7 at every N), W per-gate robustness (~2.5×, λ/cx ≈ 0.8)
survives with correct framing; (c) old payoff convention V=1000/C=550;
(d) p_eff presented as the best/winning predictor — cz-exponential leads the
registered five-model competition in runs 1–2 (scores 7.4 and 10.0), p_eff
third and serving as physical interpretation.

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
| 4 | (d) | 270 | "p_eff=0.0018 … predicts N=4 to 0.004, N=5 to 0.010" as unqualified success | Qualified: registered primary; N=5 miss ≈−5σ reproduced in run 2; cz-exponential leads both runs (7.4, 10.0; cited to repeat-judgments.json) |
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
| 8 | (d) | 248–254 | "computed independently of the measured counts … The simulation landscape is therefore quantitatively predictive of hardware." | Removed wrong independence phrase + "therefore predictive" conclusion; qualified with registered story; provenance comment cites both registrations + repeat-judgments.json (scores 7.4/10.0 vs p_eff 23.4/31.3) |
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

## Figure references for item 13 (accumulating)

**Policy decision pending (owner):** superseded old-convention runs may be
retired-with-note rather than regenerated; only cited artifacts need
regeneration.

- README.md L461: embeds run-1 `hardware_scaling.png`; the auto-aggregated
  2-run figure lives in `results/hardware-scaling/2026-07-17T014458Z/plots/`.
- `paper/figs/hardware_scaling.pdf`: sourced from run-1 copy; refresh from
  the 2-run aggregate.
- **Old-convention (V=1000/C=550) figure-bearing runs, verified via
  config.snapshot.yaml:** all `results/n-scaling-advantage/*` runs
  (2026-07-02T0444Z/0525Z/0538Z/1247Z/1757Z, 2026-07-16T0736Z/0738Z;
  2026-06-18T0930Z pending its Tier-3 turn) and all
  `results/gamma-sweep/N2..N6` runs (advantage_vs_gamma, heatmaps,
  per-player plots).
- Current-convention (V=4/C=3), no regeneration needed:
  `results/noise-robustness/2026-07-03T0213Z`, hardware runs, t9-pilot.
- `results/topology/` — V-convention unverified (no config.snapshot.yaml at
  the standard path); resolve in Tier 3.
- Root cause of ongoing contamination fixed this audit:
  `experiments/config.yaml` defaults (entry above).

---

*Audit progress: files 1–4 complete (README.md, paper/main.tex,
paper/README.md, paper/references.bib) plus experiments/config.yaml pulled
forward by owner ruling. Next in order: docs/formulae.md, TODOS.md,
docs/findings/*, docs/superpowers/*, then Tier 2 (src/scripts/experiments/
tests docstrings), Tier 3 (results artifacts, flag-only), Tier 4
(registrations and historical docs, flag-only). Entries appended after owner
confirmation per file.*
