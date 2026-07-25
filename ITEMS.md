# ITEMS.md — item-number index

The only place item numbers are defined. Any "item N" reference anywhere in
this repo means row N of this table; a number without a row here is invalid.
Next free number: **20**. This file is an index, not a document — scope,
context, and progress live where the details column points. Do not add prose
here.

Defect ids (G*, F*) refer to `docs/VERIFIED-FACTS.md`. G13 (line-number
citation decay) is resolved by `tests/test_doc_anchors.py` rather than by an
item.

| # | title | status | resolves | details |
|---|---|---|---|---|
| 1 | — (completed before this index; title not reconstructed) | done | — | — |
| 2 | — (completed before this index; title not reconstructed) | done | — | — |
| 3 | Cross-day calibration target | open — **2 of 3–5 calibration days** (3 runs; runs 1+2 share one calibration stamp, run 3 `2026-07-25T035623Z` is the first distinct day). Gated on wall-clock, not code. Blocks Fig. 6 cross-day error bars (plan Task 11 Step 4) | — | TODOS.md, "Hardware scaling repeat runs (cross-day error bars)" |
| 4 | Registered model comparison (five-model scores_z2 ranking) | **N=6,7 extension done 2026-07-25** (`e8efec9`, job d9if010gk0ls73f4avkg, chain-matched). cz-exponential has the best score at N≤5 in all 3 runs but **loses at N=7, and both registered models fail there** — the ranking does not extrapolate and the paper is scoped to N≤5. Still accumulates per repeat run | — | docs/findings/2026-07-17-run2-repeat-judgment.md, "Five-model ranking"; results/hardware-scaling/preregistration-baselines.json |
| 5B | 1q/2q noise attribution | decided 2026-07-19: no new model; run 3 submits under the existing four registered models | — | docs/findings/2026-07-16-preregistered-baseline-competitors.md, "Item-5A addendum" |
| 6 | — (parallel track) | closed 2026-07-19 — never scoped; no G-defect, finding, data artifact, or paper `\todo` traces to it; not blocking the paper | — | — |
| 7 | — (completed before this index; title not reconstructed) | done | — | — |
| 8 | — (parallel track) | closed 2026-07-19 — never scoped; no G-defect, finding, data artifact, or paper `\todo` traces to it; not blocking the paper | — | — |
| 9 | Topology hardware + wiring-permutation controls | **run 1 done 2026-07-25** (`5e682cc`, job d9ia1pd0k0jc738jaqgg, 49 pubs, 55 QPU-s). 4 of 5 registered tests PASS: equilibrium (T1), γ sign change (T2), wiring invariance (T3), ring N=4 null (T5). T4 (per-cell magnitude) FAILED and is chain-confounded. Open only for the Task 9 repeats | separates player-4 position effect into wiring vs hardware | docs/superpowers/plans/2026-07-25-hardware-topology-batch.md; docs/findings/2026-07-17-run2-repeat-judgment.md, "Player index 4" |
| 10 | T9 learning rule | **blocked on Aasa — cannot be closed from this side.** The open item is a game-theory sign-off that the provisional "independent round-robin best response" rule is the right one; simultaneous BR / fictitious play / a fairness-constrained rule could change the p=0.02 verdict. Author metadata is now in the paper (aasasingh2005@gmail.com). Until sign-off the fairness paragraph stays hedged as exploratory, which is its current wording | — | TODOS.md, "T9 adaptation & fairness pilot"; docs/findings/2026-07-05-t9-adaptation-fairness.md |
| 11 | Stale-claim audit | done (124c09d, 2996528) | — | docs/findings/2026-07-17-item11-stale-claim-audit.md |
| 12 | Forgiving-observable disclosure | closed 2026-07-19 — never scoped; "forgiving" appears nowhere in the repo outside this row; no G-defect, finding, or paper `\todo` traces to it; not blocking the paper | — | — |
| 13 | Retire-vs-regenerate (corrected 5-directory old-convention set) | done 2026-07-19 — 7 old n-scaling dirs retired-with-note (RETIRED.md each + results/README); advantage map regenerated fixed-mode V=4/C=3 (2026-07-19T0901Z); gamma-sweep accepted from same-day pytest regen; 2 nash pytest dirs deleted | F3 | item-11 audit, "Item-13 handoff" section; results/README.md "Retired old-convention runs" |
| 14 | Start the paper | **hardware evidence folded in 2026-07-25** (`7c063e0`): 2 new Sec. IV subsections, Table II, Fig. 6; equilibrium + position-locked unfairness promoted to hardware; cz-exponential ranking scoped to N≤5. Builds clean at 9 pages. Open: Fig. 6 cross-day error bars (needs item 3), author metadata, venue/page-limit decision | — (must respect scope facts G17, G18, G19, G20) | — |
| 15 | Locale and cp1252 | **done 2026-07-26** — phase 2 landed: `.gitattributes` declares `text=auto`, pins source/docs/results artifacts to `eol=lf`, and marks binaries. Normalisation is now a property of the repo rather than of each contributor's `core.autocrlf` (the G20 hazard). Existing tracked files deliberately NOT renormalised — see the note in `.gitattributes` | — | TODOS.md, "Pre-existing: test_gamma_sweep locale failure" |
| 16 | Results-save hardening + environment provenance | **done 2026-07-26** — validated on run 3 and both 2026-07-25 batches, and the `git.dirty:true` root cause is fixed: `git_provenance()` is now captured BEFORE submission in both hardware scripts and threaded into `save_run`, with a `captured` field recording when. Recovery paths still stamp `at_save`, correctly | G15, G16 | env-block template: results/hardware-scaling/preregistration.json |
| 17 | One-command repro + artifact provenance | done 2026-07-19 — G1 (results/ un-ignored), G12 (graphify-out/ untracked), G4+G5 (.venv-win deleted), G10 (PYTHONPATH=src prefix stripped from 25 conda lines; 3 .sh helpers repointed to conda). G2/G3 swept earlier. | G1–G5, G10, G12 | docs/VERIFIED-FACTS.md, A5 + G-section; .gitignore; runTests.sh/runGammaSweep.sh/runAsymmetricTest.sh |
| 18 | CI + N=4/N=5 NE regression guard | done — validated on Actions 2026-07-19 (run 29670675020, dev push: 512 passed, 3 skipped) | G9 | guard: tests/test_ne_guard.py; workflow: .github/workflows/ci.yml (also enforces tests/test_doc_anchors.py) |
| 19 | Repo presentation | done 2026-07-19 — results/README wording + coverage-gap scope mapped (noise×{star,FC}, noise at N=6, hardware beyond GHZ, cross-day variance) | — | results/README.md "Coverage" section |
