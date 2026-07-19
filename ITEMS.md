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
| 5B | 1q/2q noise attribution | open — any new model must register before run 3 | — | — |
| 6 | — (parallel track) | open — no scope recorded; not blocking the paper | — | — |
| 7 | — (completed before this index; title not reconstructed) | done | — | — |
| 8 | — (parallel track) | open — no scope recorded; not blocking the paper | — | — |
| 9 | W-topology hardware + wiring-permutation controls | open | separates player-4 position effect into wiring vs hardware | docs/findings/2026-07-17-run2-repeat-judgment.md, "Player index 4" |
| 10 | T9 learning rule | blocked on Aasa | — | TODOS.md, "T9 adaptation & fairness pilot"; docs/findings/2026-07-05-t9-adaptation-fairness.md |
| 11 | Stale-claim audit | done (124c09d, 2996528) | — | docs/findings/2026-07-17-item11-stale-claim-audit.md |
| 12 | Forgiving-observable disclosure | open | — | — |
| 13 | Retire-vs-regenerate (corrected 5-directory old-convention set) | open | F3 | item-11 audit, "Item-13 handoff" section |
| 14 | Start the paper | open | — (must respect scope facts G17, G18, G19, G20) | — |
| 15 | Locale and cp1252 | open — test fix done (3c5c39a); phase-1 line-ending report recorded 2026-07-19 | — | TODOS.md, "Pre-existing: test_gamma_sweep locale failure" |
| 16 | Results-save hardening + environment provenance | code landed 2026-07-19; validate on run 3 | G15, G16 | env-block template: results/hardware-scaling/preregistration.json |
| 17 | One-command repro + artifact provenance | open | G1, G2, G3, G4, G5, G10, G12 (G12 may defer to 19) | — |
| 18 | CI + N=4/N=5 NE regression guard | code landed 2026-07-19; workflow validates on first push | G9 | guard: tests/test_ne_guard.py; workflow: .github/workflows/ci.yml (also enforces tests/test_doc_anchors.py) |
| 19 | Repo presentation | open | — | — |
