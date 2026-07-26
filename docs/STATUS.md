# Project Status — one page (re-orient in 60 s)

**Last updated:** 2026-07-26 (dev @ the plotter/paper commit, pushed to
fork/dev; PR #19 open into `QuantumCompTeam/dev`). Read first when returning
cold.

## Head of the line (2026-07-26)

**Item 3's registered target is met, and Fig. 6 is a real cross-calibration
figure for the first time.** Repeat run 4 (`2026-07-26T090122Z`, job
`d9isp42br2fc73e55pvg`, ~35 QPU-s) landed on a distinct calibration stamp
(`2026-07-26 13:29:01+05:30`), taking item 3 to **3 of the registered 3–5**.

- **There was never a multi-day wait.** The registered criterion is a differing
  calibration *stamp*; ibm_fez recalibrates several times a day.
- **`hardware_scaling.py` does NOT have `resolve_pinned_set`** — that fix
  (`f20521f`) landed only in `hardware_topology.py`, and the scaling
  registration records no pinned set. Left alone, `find_chain` would have taken
  `[58,71,70,69,68]`, a *fourth* chain. Run 4 used the pre-existing `--chain`
  flag to hold `[59,75,74,73,79]`, so the script stays byte-comparable for
  `--from-job` recovery of runs 1–3.
- **Chain-matching, not count, is now the binding constraint.** Only 2 of the 3
  epochs are on the anchor chain (run 3 took `[20,21,22,23,24]`). A third
  chain-matched epoch needs one more run after the next recalibration.
- **Both registered conditional tests FAIL on run 4** (N=4 z=−5.68, N=5
  z=−9.55) and the N=5 same-signed deficit reproduces **3 of 3**. Its magnitude
  is *not* stable across epochs — 0.0092 to 0.0186, a factor of two — which is
  now stated in the paper.
- **`plot_hardware_scaling.py` had two defects, now fixed.** It aggregated every
  dir with a `result.json`, folding the N=6,7 run that the judge *excludes* into
  the N=3,4,5 curve; and it reported first-run chain and job id as if they
  covered the aggregate. Selection now matches the judge and prints every
  exclusion. Error bars are cross-*epoch*, with same-stamp runs averaged first.
- **Item 10 caveat 2 closed** (`docs/findings/2026-07-26-t9-caveat2-n5-ring.md`):
  W N=5 reproduces W N=4; ring N=5 never converges at any p and fails in the
  *opposite* direction, spreading a perfectly fair baseline apart at exactly
  conserved mean welfare, most strongly at zero noise. Both caveats the pilot
  raised against itself are now tested and neither is supported. Sign-off is
  still Aasa's.
- **A paper claim was wrong, not just stale, and is corrected.** The text said
  the N=7 anomaly needs "the cross-day repeats that remain pending". It does
  not: item 3 repeats N=3,4,5 and Task 9 repeats the topology batch, so neither
  re-runs N=6,7. Settling it needs a dedicated `--ns 3,4,5,6,7` submission.
- **Paper is now 10 pages** (was 9) — the honesty additions cost about a page,
  against a typical IEEE QCE limit of 8. Venue is still Prithvi's call.
- **Quota:** 157 QPU-s all time, 155 in July.

## Head of the line (2026-07-25)

**The topology axis is on hardware.** The line that stood here — "every
hardware run in this repo is GHZ" — is no longer true. Job
`d9ia1pd0k0jc738jaqgg` ran 49 pubs across five topologies for 55 QPU-seconds,
and **four of five pre-registered tests passed**. Plan:
`docs/superpowers/plans/2026-07-25-hardware-topology-batch.md` (11 tasks;
0–8 done). Full write-up:
`docs/findings/2026-07-25-topology-hardware-run1.md`.

- **Run 1 results.** Every cell retained **97.9–99.6% of its ideal advantage**
  (mean 98.9%) across ghz/ring/star/fully-connected/W. The paper's central
  mechanism reproduced off-GHZ: ring N=5 and star N=5 sit at P(0…0) ≈ 0.10–0.11
  yet keep >99% of advantage, and GHZ N=5 lost 11.2% of ground-state
  probability but only 1.3% of advantage.
  - **T1 equilibrium PASS** — all three unilateral Hawk deviation gaps at
    ghz N=3 positive (+0.2895/+0.2726/+0.3512). The restricted-menu `{D,H,Q}`
    equilibrium is **hardware-verified**. Still *not* a full-SU(2) claim.
  - **T2 gamma PASS** — the registered sign change reproduced (−0.6877 at
    0.30π, +0.2467 at 0.45π). The 0.40π point, registered MARGINAL *in
    advance*, came back at +0.0067 — indistinguishable from zero.
  - **T3 fairness PASS** — star N=4's hub loses (~0.34) while leaves earn
    (~1.21), and this does **not** move when players are permuted across
    physical qubits. The unfairness is locked to the graph position, not the
    qubit. This is the control `paper/REVIEW-NOTES.md:38` demanded.
  - **T5 ring N=4 PASS** — zero noiseless advantage (deterministic `|1111>`),
    yet measured +0.0894; smallest of the 12 cells, positive, and ZNE pulls it
    back toward zero. Advantage manufactured purely by decoherence.
  - **T4 per-cell advantage FAIL, and confounded — do not quote it.** See below.
- **T4 is confounded and needs a chain-matched re-test.** ibm_fez recalibrated
  between registration (08:15:48+05:30) and submission (16:05:46+05:30), and
  `find_pinned_set` selects from live calibration, so the batch executed on
  `[137,147,146,145,144]` while the registered predictions described
  `[20,21,22,23,24]`. T4's z-scores therefore conflate device-model error,
  calibration drift and a different qubit set. T1/T2/T3/T5 are unaffected —
  every one is a within-job differential. **No T4 number enters `main.tex`
  until a chain-matched run exists.**
- **Fixed (`f20521f`): the pinned set now comes from the registration.**
  `resolve_pinned_set` precedence is `--pinned` > frozen registration > live
  calibration, and it prints what live *would* have picked. `--free-pinned`
  opts out deliberately and says the run is no longer comparable. Verified
  live: it holds `[20,21,22,23,24]` against drifted calibration and reproduces
  the registration's exact routed cz counts. This also makes the Task 9
  cross-day repeats controlled, which they previously could not be.
- **Task 10 done (`e8efec9`): N=6,7 are on hardware, and the chain held.**
  Job `d9if010gk0ls73f4avkg`, 17 pubs, 20 QPU-s, registered
  (`preregistration-n67.json`, frozen at `8d1e5d1`) and judged. **Advantage
  survives to N=7 at 98.1% of ideal while P(0…0) has fallen to 0.78.**
  Registered on `[97,107,108,109,110,111,98]` and *executed on the same* — the
  first run whose qubits provably match its registration, so its failures are
  model failures, not provenance failures.
  - **Both registered models FAILED.** M1 (depolarizing) over-predicts at every
    N; M2 (cz-exponential) over-predicts at N=4,5,6 then *under*-predicts at
    N=7. A one-parameter retention law fitted at N=3 cannot bend that way.
  - **The model race SPLIT, contradicting the existing ranking.** M2 is closer
    at N=4,5,6; M1 at N=7. **M2's lead in `repeat-judgments.json` does not
    extrapolate** — any paper text ranking the five models must be scoped to
    N≤5. The registration named this outcome in advance.
  - **Open thread: retention is not monotone** (99.15 / 97.51 / 97.33 / 96.29 /
    **98.13**%). N=7 keeps more of its ideal advantage than N=4,5,6 despite the
    most gates and the lowest fidelity, and its ZNE *overshoots* the ideal
    (0.4437 vs 0.4286), which no physical noise model can do. Cause
    undetermined — needs the Task 9 repeats before it is a result rather than
    an observation. `docs/findings/2026-07-25-scaling-n67-run1.md`.
- **Next: plan Task 9 — two more calibration days.** Wall-clock-gated, ~55
  QPU-s each, zero code change. Each repeat now runs chain-matched, so it
  doubles as the topology T4 re-test *and* tests the N=7 anomaly. Then Task 11
  (fold into the paper).
- **Quota:** 122 QPU-s consumed all time, 120 of it in July (55 topology + 20
  N=6,7 today). The Open Plan monthly allowance is still **unverified** —
  `usage()` is gated to the retired `ibm_quantum` channel and `instances()`
  returns empty on `ibm_cloud`, so it cannot be read from the API. Check
  quantum.cloud.ibm.com before Task 9.
- **Not blocked.** The IBM credential is a saved account in `~/.qiskit` and is
  verified working. Do **not** set `QISKIT_IBM_TOKEN`: the env var takes
  precedence over the saved account in `load_service()`, and exporting it leaks
  the token into the session transcript.
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
  advantage decays ~7× slower than state fidelity. **Confirmed off-GHZ on
  hardware 2026-07-25:** ring N=5 and star N=5 sit at P(0…0) ≈ 0.10–0.11 and
  still keep >99% of ideal advantage. It is a property of the payoff geometry,
  not of the GHZ state.
- **Topology (new, hardware):** all five topologies retained 97.9–99.6% of
  ideal advantage. The topology axis does not separate them by *magnitude* of
  retained advantage — it separates them by **structure**: star N=4 is
  position-locked unfair (hub 0.34 vs leaves 1.21), and ring N=4 has zero
  noiseless advantage, so what advantage it shows is manufactured by noise.
- **Scaling:** set per-two-qubit-gate decay, not fitted depolarizing strength.
  In the registered five-model comparison, cz-exponential retention leads
  **at N≤5 — and loses at N=7** (`e8efec9`, chain-matched). Scope the ranking
  claim to N≤5; it does not extrapolate.
  A cz-*linear* device-model bias correction fitted on GHZ (6–14 cz)
  **over-corrects beyond its fitting range** — the bias saturates. Directional
  only; the measurement it came from is chain-confounded (see head of line).
- **Reach (new, hardware):** the cooperative advantage survives to **N=7 at
  98.1% of ideal** with ground-state probability down to 0.78 — the
  first-order-insensitivity mechanism holds across the full N=3…7 curve.

## Why a reviewer trusts the process (the moat)

- **Pre-registered predictions** committed before hardware runs, judged after.
  `scripts/judge_topology_run.py` refuses to run unless the registration is
  byte-identical to HEAD, so a registration cannot be edited after the data
  arrives. The topology registration (`46f43d4`) sits four commits before its
  data (`5e682cc`) in public history.
- **Marginal points called in advance.** γ=0.40π was registered MARGINAL and
  excluded from pass/fail *before* submission; it came back at +0.0067.
- **Registered five-model comparison** — let a simpler baseline beat the
  depolarizing fit; reported honestly. Same pattern for T4a/T4b, where **both
  registered models failed** and it is written up as a failure.
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

- **Item 3** (cross-day repeats): **2 of 3–5 distinct calibrations.** Three
  runs exist, but runs 1 and 2 share one calibration stamp — run 2 carries
  `"distinct_calibration_vs_previous_runs": false` despite being 18 hours later
  *and* spanning an IBM maintenance window. Run 3 (`2026-07-25T035623Z`,
  job `d9i379d0k0jc738j18fg`) is the first genuinely distinct one. Fig. 6's
  cross-day error bars (plan Task 11 Step 4) depend on this count being 2.
- **Item 3 is NOT a multi-day wait.** The registered criterion is a *differing
  calibration stamp*, not a differing date, and ibm_fez recalibrated **three
  times on 2026-07-25** (08:15:48 / 16:05:46 / 22:32:49 +05:30). So item 3
  needs two more `--hardware` runs on the untouched scaling script (~35 QPU-s
  each) submitted after a recalibration — plausibly the same day. Detail and
  the honest counter-argument (same-day epochs may understate multi-day drift)
  are in `TODOS.md`.
- **Item 4** (five-model ranking) accumulated on run 3.
- **Item 16** (env-block capture) validated on run 3's artifact: `environment`
  and `calibration_at_submit.json` are both present.
- **Known, benign:** every `--hardware` run records `git.dirty: true`.
  `_save_pending_job_id` writes `pending_jobs.txt` and
  `pending-<id>-calibration.json` before polling for crash safety, and
  `git_provenance()` runs at save time. `dirty_files` enumerates exactly those
  two writes. The real fix is capturing provenance before submission, which
  edits `hardware_scaling.py` and therefore belongs in plan Task 10.
- **Pinned sets used to move between runs, and it cost us a test.** The
  scaling runs drifted (`[59,75,74,73,79]` on run 2); the topology batch drifted
  *within a single day*, registered on `[20,21,22,23,24]` and executed on
  `[137,147,146,145,144]`, which is what confounded T4. Since `f20521f` the
  chain is taken from the registration by default, so **future** runs are
  chain-matched and comparable across days. Existing artifacts are not:
  anything comparing the scaling runs to each other, or run 1 of the topology
  batch to its own registration, still carries this caveat.
- **Item 9** (topology + wiring-permutation hardware): run 1 landed
  (`5e682cc`). T3 answered `paper/REVIEW-NOTES.md:38` in the affirmative — the
  player-position claim does **not** need narrowing.

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
- **Item 9** (W-topology hardware + wiring-permutation controls) — **run 1
  landed 2026-07-25.** W N=3 retained 97.9% of ideal advantage at 42 cz (7× the
  gate count of GHZ N=3); the two star N=4 wiring permutations passed T3. Open
  only for the Task 9 repeats.

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
