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
| 3 | Cross-day calibration target | open — 1 of 3–5 calibration days | — | TODOS.md, "Hardware scaling repeat runs (cross-day error bars)" |
| 4 | Registered model comparison (five-model scores_z2 ranking) | open — accumulates per repeat run | — | docs/findings/2026-07-17-run2-repeat-judgment.md, "Five-model ranking"; results/hardware-scaling/preregistration-baselines.json |
| 5B | 1q/2q noise attribution | decided 2026-07-19: no new model; run 3 submits under the existing four registered models | — | docs/findings/2026-07-16-preregistered-baseline-competitors.md, "Item-5A addendum" |
| 6 | — (parallel track) | closed 2026-07-19 — never scoped; no G-defect, finding, data artifact, or paper `\todo` traces to it; not blocking the paper | — | — |
| 7 | — (completed before this index; title not reconstructed) | done | — | — |
| 8 | — (parallel track) | closed 2026-07-19 — never scoped; no G-defect, finding, data artifact, or paper `\todo` traces to it; not blocking the paper | — | — |
| 9 | W-topology hardware + wiring-permutation controls | open | separates player-4 position effect into wiring vs hardware | docs/findings/2026-07-17-run2-repeat-judgment.md, "Player index 4" |
| 10 | T9 learning rule | blocked on Aasa | — | TODOS.md, "T9 adaptation & fairness pilot"; docs/findings/2026-07-05-t9-adaptation-fairness.md |
| 11 | Stale-claim audit | done (124c09d, 2996528) | — | docs/findings/2026-07-17-item11-stale-claim-audit.md |
| 12 | Forgiving-observable disclosure | closed 2026-07-19 — never scoped; "forgiving" appears nowhere in the repo outside this row; no G-defect, finding, or paper `\todo` traces to it; not blocking the paper | — | — |
| 13 | Retire-vs-regenerate (corrected 5-directory old-convention set) | done 2026-07-19 — 7 old n-scaling dirs retired-with-note (RETIRED.md each + results/README); advantage map regenerated fixed-mode V=4/C=3 (2026-07-19T0901Z); gamma-sweep accepted from same-day pytest regen; 2 nash pytest dirs deleted | F3 | item-11 audit, "Item-13 handoff" section; results/README.md "Retired old-convention runs" |
| 14 | Start the paper | open | — (must respect scope facts G17, G18, G19, G20) | — |
| 15 | Locale and cp1252 | open — test fix done (3c5c39a); phase-1 line-ending report recorded 2026-07-19 | — | TODOS.md, "Pre-existing: test_gamma_sweep locale failure" |
| 16 | Results-save hardening + environment provenance | code landed 2026-07-19; validate on run 3 | G15, G16 | env-block template: results/hardware-scaling/preregistration.json |
| 17 | One-command repro + artifact provenance | done 2026-07-19 — G1 (results/ un-ignored), G12 (graphify-out/ untracked), G4+G5 (.venv-win deleted), G10 (PYTHONPATH=src prefix stripped from 25 conda lines; 3 .sh helpers repointed to conda). G2/G3 swept earlier. | G1–G5, G10, G12 | docs/VERIFIED-FACTS.md, A5 + G-section; .gitignore; runTests.sh/runGammaSweep.sh/runAsymmetricTest.sh |
| 18 | CI + N=4/N=5 NE regression guard | done — validated on Actions 2026-07-19 (run 29670675020, dev push: 512 passed, 3 skipped) | G9 | guard: tests/test_ne_guard.py; workflow: .github/workflows/ci.yml (also enforces tests/test_doc_anchors.py) |
| 19 | Repo presentation | done 2026-07-19 — results/README wording + coverage-gap scope mapped (noise×{star,FC}, noise at N=6, hardware beyond GHZ, cross-day variance) | — | results/README.md "Coverage" section |
