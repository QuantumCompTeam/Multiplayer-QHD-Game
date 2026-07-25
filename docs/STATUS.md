# Project Status — one page (re-orient in 60 s)

**Last updated:** 2026-07-25 (dev @ 46f43d4). Read first when returning cold.

## Head of the line (2026-07-25)

**Every hardware run in this repo is GHZ.** The title claims topology
determines advantage; the topology axis, the noise-robustness dichotomy, and
the position-locked-unfairness claim are all simulation-only. That is the
submission-readiness gap. Plan:
`docs/superpowers/plans/2026-07-25-hardware-topology-batch.md` (11 tasks).

- **Not blocked.** The IBM credential is a saved account in `~/.qiskit` and is
  verified working. Do **not** set `QISKIT_IBM_TOKEN`: the env var takes
  precedence over the saved account in `load_service()`, and exporting it leaks
  the token into the session transcript.
- **Tasks 0–7 done** (`2b83fb7`, `f94ee35`, `97329fb`, `35fdb54`, `69ff56d`,
  `add4378`, `46f43d4`). `src/hardware/topology_hw.py`, the five-axis batch
  plan, the feasibility report, the rehearsal/submit/recover path, and the
  **frozen registration** `results/hardware-topology/preregistration.json`.
- **Next: plan Task 8 — the first submission.** 49 pubs, ~60–90 s QPU.
  Rehearsal passes with zero quota (49/49 pubs reproduce their logical
  distribution exactly; ZNE improves 12/12 cooperative series).
  **Verify the Open Plan monthly quota at quantum.cloud.ibm.com first** —
  `usage()` is gated to the retired `ibm_quantum` channel and `instances()`
  returns empty on `ibm_cloud`, so it cannot be read from the API. 47 QPU-s
  consumed all time, 45 of it in July.
- **Do not touch `experiments/hardware_scaling.py`** until plan Task 10.
  Item 3 re-runs the *identical* registered batch; editing `NS`, the entangler
  or the pub order breaks `--from-job` recovery of runs 1–2 and makes run 3
  non-comparable.
- **Do not edit `results/hardware-scaling/preregistration*.json`**, nor
  `results/hardware-topology/preregistration.json` now that it is committed.
  New claims get new registration files.
- **The heavy-hex cost warning that used to sit here was wrong at N≤5.** Girth
  12 is a true statement about the coupling graph but overstates cost at the
  sizes this paper runs: measured routed cz is ring 10/20/28 and
  fully-connected 10/31 at N=3/4(/5). The transpiler closes short cycles with a
  few SWAPs rather than routing a 12-cycle. The real casualty is W (42 cz at
  N=3, 107 and 219 at N=4,5). See
  `docs/findings/2026-07-25-topology-hardware-feasibility.md`.

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

## Hardware runs

- **Item 3** (cross-day repeats): **2 of 3–5 distinct calibration days.** Three
  runs exist, but runs 1 and 2 share one calibration stamp — run 2 carries
  `"distinct_calibration_vs_previous_runs": false`. Run 3 (`2026-07-25T035623Z`,
  job `d9i379d0k0jc738j18fg`) is the first genuinely distinct day. Fig. 6's
  cross-day error bars (plan Task 11 Step 4) depend on this count being 2.
- **Item 4** (five-model ranking) accumulated on run 3.
- **Item 16** (env-block capture) validated on run 3's artifact: `environment`
  and `calibration_at_submit.json` are both present.
- **Known, benign:** every `--hardware` run records `git.dirty: true`.
  `_save_pending_job_id` writes `pending_jobs.txt` and
  `pending-<id>-calibration.json` before polling for crash safety, and
  `git_provenance()` runs at save time. `dirty_files` enumerates exactly those
  two writes. The real fix is capturing provenance before submission, which
  edits `hardware_scaling.py` and therefore belongs in plan Task 10.
- **Pinned sets move between calibration days** (run 2 used
  `[59,75,74,73,79]`; 2026-07-25 uses `[20,21,22,23,24]`). Topology comparisons
  *within* one batch are controlled by construction; comparisons *across*
  batches are not. Plan Task 9 must be read with that in mind.

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
- **Item 9** (W-topology hardware + wiring-permutation controls) — registered,
  awaiting submission. W N=3 and two star N=4 wiring permutations are both in
  the frozen batch; the wiring control is registered as test T3.

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
