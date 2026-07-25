# Project Status — one page (re-orient in 60 s)

**Last updated:** 2026-07-25 (dev @ f94ee35). Read first when returning cold.

## Head of the line (2026-07-25)

**Every hardware run in this repo is GHZ.** The title claims topology
determines advantage; the topology axis, the noise-robustness dichotomy, and
the position-locked-unfairness claim are all simulation-only. That is the
submission-readiness gap. Plan:
`docs/superpowers/plans/2026-07-25-hardware-topology-batch.md` (11 tasks).

- **Landed** (commits `2b83fb7`, `f94ee35`): `src/hardware/topology_hw.py`
  (topology- and profile-parameterised EWL build + pinned-set ISA check) and
  `experiments/hardware_topology.py` (five-axis batch plan, per-series
  analysis, `--report`). 70 new tests; full suite **583 passed, 3 skipped**.
- **Blocked on an IBM credential**, nothing else: Task 0 (cross-day repeat
  run 3 — the only wall-clock-gated item, ~35 s QPU, zero code change),
  Task 3 (transpile feasibility report, network read only, no quota), then
  Tasks 6–11.
- **Do not touch `experiments/hardware_scaling.py`** until plan Task 10.
  Item 3 re-runs the *identical* registered batch; editing `NS`, the entangler
  or the pub order breaks `--from-job` recovery of runs 1–2 and makes run 3
  non-comparable.
- **Do not edit `results/hardware-scaling/preregistration*.json`.** New claims
  get new registration files.
- ibm_fez is heavy-hex (degree ≤3, girth 12): no native triangle, no cycle
  below N=12. Pre-routing gate counts understate ring and fully-connected cost;
  only GHZ is free. Cell selection comes from the measured `--report`, not from
  pre-routing numbers.

**Venue note:** IEEE QCE26's technical-paper deadline (2026-04-27) has passed;
the conference is 2026-09-13/18 in Toronto. Venue choice is Prithvi's call and
is deliberately not encoded anywhere in the repo.

## One question

Does two-player quantum Hawk–Dove advantage survive real **N-player**
networks — topology, noise, hardware? **Answer: yes, sharper edges.**

## Through-line (the actual result)

- **N=3:** GHZ cooperative profile is a genuine symmetric pure Nash equilibrium.
  Reproduced on ibm_fez at **0.9978 ideal** (job `d9br6l66hjac73fg3g7g`).
- **N=4,5:** equilibrium *breaks* (a unilateral Hawk deviation profits), but the
  cooperative payoff keeps a large measurable advantage (0.739/0.584 ideal
  0.75/0.60). Framed as a **fixed cooperative protocol**, not an equilibrium (G19).
- **The mechanism:** mean payoff is *first-order insensitive to single
  bit-flips* — a property of payoff geometry, not the device. That is why
  advantage decays ~7× slower than state fidelity.
- **Scaling:** set per-two-qubit-gate decay, not fitted depolarizing strength.
  In the registered five-model comparison, cz-exponential retention leads runs.

## Why a reviewer trusts the process (the moat)

- **Pre-registered predictions** committed before hardware runs, judged after.
- **Registered five-model comparison** — let a simpler baseline beat the
  depolarizing fit; reported honestly.
- **VERIFIED-FACTS.md:** every number traces to file:line.
- Honesty notes inside artifacts themselves.

## State of the paper (item 14)

**Full draft exists as of `d7ee2f5`.** `main.tex` has **zero** `\todo` markers
left — Aasa's three sections (payoff tensor, zero-noise landscape, Month-4 port)
were written in `c993ff8`/`d7ee2f5`, and the advantage-map figure is embedded
(`fig:advmap`, `fig:heat`). Builds to 7 pages; all 8 references carry verified
DOIs. The paper is no longer the bottleneck — the hardware evidence is.

Remaining paper-side work is in `paper/REVIEW-NOTES.md`: Aasa's publication
email, item-10 T9 sign-off (keeps the fairness paragraph hedged as
"exploratory"), and the claim updates that depend on the hardware runs above
(plan Task 11).

## Hardware runs (blocked — wait, don't act)

- **Item 3** (cross-day repeats): 1 of 3–5 done. Run 3 needs a different
  ibm_fez calibration stamp; item 16's `calibration_at_submit.json` records it.
- **Item 4** (five-model ranking) auto-accumulates on run 3.
- **Item 16** (env-block capture) self-validates on run 3's artifact.

## Recently closed (2026-07-19, commits cd5c094 + 03d642d)

- **Item 13** — 7 old-convention n-scaling dirs retired-with-note (`RETIRED.md`
  each + `results/README`); advantage map regenerated fixed-mode V=4/C=3
  (`2026-07-19T0901Z`); gamma-sweep accepted from same-day pytest regen; 2
  nash-mode pytest artifacts deleted; hardware figures point at the 2-run
  aggregate. Resolves F3.
- **Item 17** — all 5 G-defects disposed: `results/` un-ignored (G1),
  `graphify-out/` untracked (G12), `.venv-win/` deleted (G4+G5), conda
  convention swept (G10, PYTHONPATH=src prefix stripped from 25 lines), 3
  `.sh` helpers repointed to conda. Resolves G1–G5, G10, G12.
- **Item 18** — CI + N=4/N=5 NE regression guard validated on Actions
  (run 29670675020: 512 passed, 3 skipped). Resolves G9.

## Open, unblocked

- **Item 19** (repo presentation) — done 2026-07-19. `results/README` wording
  tightened + coverage-gap scope mapped (noise×{star,FC}, noise at N=6,
  hardware beyond GHZ, cross-day variance).
- **Decisions (yours):** item 15 phase-2 `.gitattributes`. Items 6 / 8 / 12
  closed 2026-07-19 — never scoped, nothing traces to them, not blocking.
- **Item 9** (W-topology hardware + wiring-permutation controls) — open.

## Waiting on Aasa (out of the picture until first draft)

- **Item 10** (T9 learning rule) — sign-off; fairness paragraph hedged as
  exploratory.
- Aasa's 3 paper sections: payoff tensor, zero-noise landscape, Month-4 port.
  If he stays out, these become Prithvi's after the first draft exists.

## Key files

- Paper: `paper/main.tex` · status/owners: `paper/README.md`
- Work queue: `ITEMS.md` (index) · `TODOS.md` (deferred detail)
- Provenance: `docs/VERIFIED-FACTS.md` · findings: `docs/findings/`
- Preregistrations: `results/hardware-scaling/preregistration*.json`
