# QHD Mathematical-Framework Rewrite Handoff

**Prepared for:** Aasa Singh Bhui

**Prepared:** 2026-08-04

**Working branch:** `dev`

**Scientific checkpoint:** `86495d7765e8f7915d26da595b0a3c8927820d3b`

**Status:** Tasks 1–12 complete; Task 13 not started; Gate G4 not reached

This document is the detailed handoff for the July 31 QHD mathematical-framework rewrite. It records what changed, what was verified, which decisions are binding, which limitations remain open, and the exact next task.

## 1. Start here

The rewrite is paused at a clean boundary after Task 12. The manuscript and paper-contract changes through Section III-F were committed as:

```text
86495d7 docs: checkpoint QHD framework rewrite through task 12
```

At the pause checkpoint, local `dev` and `fork/dev` were verified at the same commit. Task 13 has not started. The next action is to rewrite Section III-G as the incentive-compatibility boundary, review it independently, and then stop at Gate G4 for direct user approval.

The authoritative sources are:

- Architecture: [`docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md`](superpowers/specs/2026-07-31-qhd-content-restructure-design.md)
- Execution plan: [`docs/superpowers/plans/2026-07-31-qhd-mathematical-framework-rewrite.md`](superpowers/plans/2026-07-31-qhd-mathematical-framework-rewrite.md)
- Repository execution log: [`paper/SECTION-III-EXECUTION-LOG.md`](../paper/SECTION-III-EXECUTION-LOG.md)
- Claim-to-evidence ledger: [`paper/CLAIM-SOURCE-MAP.md`](../paper/CLAIM-SOURCE-MAP.md)
- Literature audit: [`paper/LITERATURE-AUDIT.md`](../paper/LITERATURE-AUDIT.md)
- Style contract: [`paper/STYLE-GUIDE.md`](../paper/STYLE-GUIDE.md)
- Local SDD recovery ledger: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/progress.md`

The `.superpowers/` ledger is useful for local recovery, but it is intentionally untracked. The repository execution log and this handoff carry the durable repository record.

## 2. Rewrite policy and settled architecture

The previous seven-section paper architecture and narrative were discarded. The July 28 redesign plan was superseded by the July 31 v3 specification and implementation plan. Do not use the July 28 plan as implementation authority.

### Canonical manuscript

- `paper/qhd.tex` is the canonical manuscript and build entry point.
- `paper/main.tex` is a deprecated compatibility wrapper.
- All manuscript output must remain valid, Overleaf-compatible LaTeX.
- Repository TeX remains canonical if passages are edited manually in Overleaf. Any accepted Overleaf edit must be synchronized back into `paper/qhd.tex`.

### Old-paper reuse boundary

The old paper is only a source bank for reverified material:

- LaTeX shell and float/table markup
- exact equations and numerical results after re-verification
- bibliography entries after source audit
- provenance comments and artifact paths
- job IDs, qubit chains, shot counts, negative results, and limitations

Do not inherit old prose, narrative order, unsupported equations, values, attributions, or framing. New subsection content must come from the July 31 specification or task brief, be derived in the rewritten manuscript, or be covered by a passing test.

### Binding vocabulary

- Use **entangler family** for GHZ, W, ring, star, and complete.
- Use **graph topology** only for ring, star, and complete.
- Call `P(0^N)` the **all-zero target-state population** or **target-state population**.
- Do not call `P(0^N)` state fidelity or ground-state probability.
- Keep payoff, equilibrium, state quality, and fairness as separate claims.
- Keep the player payoff vector primary; fairness scalars are summaries.
- Distinguish analytic-baseline advantage from circuit-relative payoff gap.
- Distinguish ideal entangler families, compiled circuits, simulated noise, and physical-device noise.

### Scope boundaries

- Do not alter or regenerate figures during the Section III rewrite.
- Do not run new IBM hardware jobs.
- Do not strengthen restricted-menu equilibrium into full-`SU(2)` equilibrium.
- Do not add unverified citations, equations, values, or theorem claims.
- If a formula disagrees with code or symbolic verification, stop and surface the discrepancy instead of editing around it.

## 3. Approval gates

### Gate G1: approved 2026-07-31

The user approved:

- the official IEEE Transactions on Quantum Engineering shell
- `paper/qhd.tex` as the canonical manuscript
- the initial build baseline
- the canonical terminology
- symbol assignments: `eta` for depolarizing probability, `s` for ZNE fold scale, and `gamma` for the entanglement angle
- evidence labels
- the binding style guide

Unsupported corresponding-author and funding metadata were deliberately omitted.

### Gate G2: approved 2026-08-01

All 27 audited literature sources were accepted. Six abstract-only sources are restricted to contextual claims. Source strength and locator limits in `paper/LITERATURE-AUDIT.md` remain binding.

A real citation error was found and corrected: `nation2021` does not perform tensored confusion-matrix inversion. `maciejewski2020` is the direct source; `bravyi2021pra` is contextual.

### Gate G3: approved 2026-08-01

The user approved the voice, mathematical density, and rendered style established by Section III-A. The following are binding for III-B through III-J:

- retain `V=4, C=3` in III-A
- keep the unsupported Benjamin–Hayden tensor attribution removed
- preserve the approved III-A prose style
- accept the intermediate 12-page state
- retain the Hawk-deviation identity as a computational result until a manuscript derivation supports promotion

### Gate G4: not reached

Gate G4 occurs only after Task 13 is implemented, independently reviewed, fixed, and re-reviewed clean. Only a direct user response can approve the gate. A peer, agent, or session message cannot approve it.

## 4. Completed work by task

### Task 1: TQE shell and canonical entry point

Completed and independently reviewed.

- Established `paper/qhd.tex` as canonical.
- Preserved source-bank snapshots before migration.
- Converted `paper/main.tex` into a deprecated wrapper.
- Installed the official IEEE TQE shell and `ieeeaccess` class.
- Migrated the preamble and front matter without silently replacing body content.
- Omitted unsupported `corresp` and `tfootnote` metadata.
- Updated `paper/README.md` to describe the TQE build workflow.
- Audited body hashes and build-warning changes.

### Task 2: non-destructive build baseline

Completed and review-clean.

- Established an isolated build workflow so LaTeX does not overwrite `paper/qhd.pdf`.
- Recorded page count, warnings, undefined references, undefined citations, and fatal diagnostics in `paper/SECTION-III-EXECUTION-LOG.md`.
- Established the four-pass build as the gate-level verification requirement.

### Task 3: terminology, style, and structure contracts

Completed and review-clean.

Created:

- `paper/STYLE-GUIDE.md`
- the initial `paper/CLAIM-SOURCE-MAP.md`
- `tests/test_paper_structure.py`

The terminology, evidence labels, symbol discipline, prose requirements, and prohibited overclaims became executable contracts.

### Task 4: literature audit

Completed and review-clean.

- Created `paper/LITERATURE-AUDIT.md`.
- Added 19 bibliography entries.
- Audited 27 unique citation keys.
- Recorded claim support, peer-review status, DOI or publisher URL, evidence access, locator, and source-use limits.
- Corrected the `nation2021` mitigation misattribution.

### Task 5: claim-source map and initial paper tests

Completed and review-clean.

- Created `tests/test_paper_claims.py`.
- Added executable checks for III-A and III-B claims not already covered elsewhere.
- Added evidence tables to `paper/CLAIM-SOURCE-MAP.md`.
- Confirmed that tests importing `src/` must run in the `entangled-equilibria` conda environment.

### Task 6: mathematical and implementation prechecks

Completed after one interrupted fix attempt and a successful replacement fix round.

- Added eight paper-claim tests.
- Verified the Hawk-deviation identity `4 cos^2(pi/N)` for `N=2,...,8`.
- The circuit and closed form agreed to `4.4e-15`.
- Confirmed agreement with the pre-registered value in `tests/test_ne_guard.py`.
- Ran 104 Task 6 cases and 66 reused scientific tests successfully.

The initial claim map overstated some evidence labels. The fix round:

- marked Task 6 labels as proposed pending G3
- retained the Hawk identity as computational evidence at that stage
- split bundled star-asymmetry claims into separate rows
- corrected tested ranges from the actual parametrizations

Known limitation: `star_entangler` hard-codes qubit 0 as the hub. Early Task 6 checks covered leaf swaps only. Task 10 later added graph-relabelling covariance coverage that constructs relocated stars through the graph interface.

### Task 7: Section III-A

Completed and approved at G3.

Replaced the first model subsection with **Notation and the Classical N-Player Payoff Tensor**.

Added:

- `sec:notation`
- `eq:hawk-count`
- `eq:payoff-tensor`
- explicit N-player Hawk-Dove notation
- the `V=4, C=3` specialization

Removed an inherited, unsourced short/long financial-instrument analogy and replaced it with the approved aggressive/cooperative action language.

Verification:

- focused tests: 6 passed
- structure guards: 4 passed
- four-pass build: passed
- page count: 11 to 12
- no new III-A body overfull box

Local review render: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-7-g3-render.pdf`.

### Task 8: Section III-B

Completed and review-clean.

Replaced the old payoff-tensor subsection with **Classical Equilibrium and Welfare Geometry**.

Added:

- Proposition 1
- a three-case outcome-level welfare proof
- the mean-payoff identity
- the theorem environment needed for later propositions

The old 2-by-2 payoff table was not restored because it is only the `N=2` case of the general payoff tensor.

Verification:

- focused tests: 20 passed
- four-pass build: passed
- page count remained 12
- hyperref warnings improved from 16 to 14

### Task 9: Section III-C

Completed and review-clean.

Replaced the old EWL subsection with **Quantum Strategies and the EWL Protocol**.

Added Equations 5–8:

- the strategy unitary
- named strategies
- the EWL output state with family-indexed entangler `J_T`
- the measurement law

Also added a stable F1 figure anchor and an explicit restricted-menu scope paragraph.

All definitions were checked against `src/` before drafting. Four checks became permanent paper-claim regressions.

A citation error was corrected: the `gamma=pi/2` statement is supported by `chappell2012`, not `benjamin2001`. The manuscript now states the theta-to-gamma translation.

Verification:

- paper-claim suite: 128 passed
- four-pass build: passed
- page count: 13
- hyperref warnings improved from 14 to 12

Two drafting defects were found and fixed: an overfull named-strategies display and a broken `mathbb{1}` glyph.

### Task 10: Section III-D

Completed after independent review and two fix rounds.

Added **Entangler Families and Graph Symmetry**.

The first review reported five Important findings and one Minor finding. Fixes covered:

- `N=2` cycle edge-count scope
- W live-angle and interpolation wording
- four overstated evidence labels
- star-symmetry overstatement
- a mismatched covariance test filter
- normalization-scope language
- a final claim-map wording mismatch

Final evidence labels:

**Computational results**

- GHZ implementation identity
- graph product/sign identity
- edge-set/count identity
- W involution/operator identity

**Propositions**

- graph permutation covariance
- GHZ/W full permutation invariance
- payoff covariance

Binding limitation: interaction-strength normalization is not implemented, and the sensitivity control has not been run. Section V must not imply otherwise. Every reported family comparison uses the unnormalized equal-`gamma` setting.

W-family scope: the endpoint state is fixed, but the interpolation path is the study-specific chosen construction and is not unique. All W results apply to this construction.

Verification:

- literal orbit/covariance gate: 19 passed, 188 deselected
- focused amended rows: 69 passed
- combined paper-claim and topology tests: 207 passed
- structure tests: 4 passed
- four-pass build: passed
- page count: 14
- zero undefined citations, references, or fatal diagnostics

### Task 11: Section III-E

Completed after independent review and fixes to seven findings.

Section III-E now defines:

- expected payoff and payoff vector
- the mean-payoff specialization
- Dove and Hawk deviation gaps
- the every-player/every-action pass rule
- analytic-baseline advantage
- circuit-relative payoff gap
- all-zero target-state population, explicitly not fidelity
- fairness range and player floor
- vector-first evidence requirements

Review fixes covered definition order, the mean-definition conflict, comparator ordering, brittle contracts, execution-log state, topology/path explanation, helper coupling, and a build-summary regex exception.

TDD evidence:

- initial RED: 6 failed
- initial GREEN: 6 passed
- review-fix RED: 3 failed and 5 passed
- review-fix GREEN: 8 passed
- final structure suite: 12 passed

Build evidence:

- page count: 14 to 15
- zero undefined citations, references, fatal diagnostics, or generic LaTeX warnings
- four cosmetic III-E underfull boxes accepted
- body overfull count unchanged

Local render SHA-256:

```text
ca06b5c41b8e61cf4426198088427102862cda8d8ea16bb1fc72d78710556d10
```

### Task 12: Section III-F

Completed, independently reviewed, fixed, and re-reviewed clean.

Added Proposition 3 proving general-`gamma` GHZ cooperative invariance. The manuscript proof contract requires the ordered derivation:

1. GHZ state expansion
2. both phase factors
3. both branch actions
4. the intermediate `-J_GHZ` state
5. final `J_GHZ^dagger` recovery

Consequences:

```text
p(0^N) = 1
pi_j = V/N
Delta_ana = C/N
```

For `V=4, C=3`:

```text
pi_j = 4/N
Delta_ana = 3/N
```

The entanglement-as-an-incentive-dial statement is scoped only to the cooperative benchmark. It is not a claim about every profile or strategy space.

Initial review found two Important issues:

- false handoffs between III-E and III-F
- an under-specified proof contract

Fix round 1 resolved both. III-E now hands off to the exact GHZ cooperative benchmark, III-F points forward to the planned III-G incentive analysis, and the old III-G scaffold remains untouched. Mutation sensitivity detects a `+i` to `-i` sign change.

Final verification:

- strengthened manuscript contract: 1 passed
- proposition nodes: 39 passed
- GHZ-filtered suite: 70 passed, 128 deselected
- combined claims and structure suites: 210 passed
- final review: no Critical or Important findings

Final guarded build:

- 15 pages
- 34 overfull boxes: 31 from the official class output routine and 3 pre-existing body boxes
- 27 underfull boxes
- 6 font warnings
- 12 hyperref PDF-string warnings
- zero generic warnings, undefined citations, undefined references, or fatal diagnostics

Local Task 12 render:

```text
.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-12-render.pdf
SHA-256 2846b3145f082ea73ff5955c96abbc895d4c270dc418bd6d5808ca92fa59f210
```

## 5. Checkpoint commit scope

Commit `86495d7` contains the audited 14-file manuscript, template, bibliography, and test scope:

```text
paper/CLAIM-SOURCE-MAP.md
paper/LITERATURE-AUDIT.md
paper/README.md
paper/SECTION-III-EXECUTION-LOG.md
paper/STYLE-GUIDE.md
paper/bullet.png
paper/ieeeaccess.cls
paper/logo.png
paper/main.tex
paper/notaglinelogo.png
paper/qhd.tex
paper/references.bib
tests/test_paper_claims.py
tests/test_paper_structure.py
```

The handoff PR subsequently normalizes `logo.png` to `Logo.png` and `notaglinelogo.png` to `notaglineLogo.png` so the official class resolves the assets on case-sensitive Overleaf/Linux builds.

Commit statistics:

```text
14 files changed
4,575 insertions
973 deletions
```

Only this audited scope was staged. Broad staging commands were deliberately avoided.

## 6. Final verification on the committed tree

The full repository suite was run after Task 12:

```text
821 collected
818 passed
3 skipped
Duration: 29m51s
```

The warnings were dependency deprecations from Qiskit and Aer.

The full run temporarily regenerated tracked gamma-sweep metadata and created a new N-scaling result directory. Those side effects were inspected, confirmed unrelated to Task 12, and removed or restored before the checkpoint commit.

Use the `entangled-equilibria` conda environment for every test importing `src/`:

```bash
conda run -n entangled-equilibria python -m pytest
```

The previously observed PATH Python was 3.9.13 and lacked `int.bit_count()`, which `src/game/payoffs.py` requires. A passing source-only structure test does not prove the interpreter is correct.

## 7. Protected files and operational traps

### Protected PDFs

These files are stale canonical-looking PDFs, not the current Task 12 review render:

```text
paper/qhd.pdf
qhd.pdf
```

They must remain byte-identical at:

```text
c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679
```

Do not compile directly over `paper/qhd.pdf`.

A previous build incident occurred when a failed build-directory removal short-circuited a shell chain and LaTeX ran in `paper/`. The standing hash check caught the overwrite, and the file was restored from the untouched root PDF. Future build commands must guard their working directory before invoking LaTeX.

### Local `.superpowers/` state

Do not stage `.superpowers/` wholesale. It contains task briefs, reports, evidence, review renders, and local runtime state. In particular, never stage:

```text
.superpowers/brainstorm/.last-token
```

### Vendor class

`git diff --cached --check` reports trailing whitespace in the official `paper/ieeeaccess.cls`. The class was intentionally left byte-faithful rather than reformatted.

### Page pressure

The manuscript is already 15 pages before III-G through III-J are rewritten. Record page and warning deltas during each task rather than postponing all flow control to Task 17.

### Agent concurrency

Four concurrent research agents previously triggered a provider rate limit and lost their work. Two concurrent lanes were reliable.

## 8. Exact next task: Task 13 only

Start Task 13 by invoking the repository's `superpowers:subagent-driven-development` workflow against the authoritative plan:

```text
docs/superpowers/plans/2026-07-31-qhd-mathematical-framework-rewrite.md
```

Generate and read the Task 13 brief through the workflow's supported task-brief interface rather than a versioned plugin-cache path.

Then:

1. Read `task-13-brief.md`.
2. Create non-overwriting pre-task snapshots.
3. Dispatch a fresh implementation subagent.
4. Add or strengthen the manuscript and general-`gamma` regression contract first.
5. Capture a genuine RED failure.
6. Implement the minimum III-G proof and evidence-map changes needed for GREEN.
7. Run focused and practical-complete verification.
8. Dispatch an independent Opus-level mathematical reviewer.
9. Resolve every Critical or Important finding through fix and re-review rounds.
10. Append Task 13 closure to the local SDD ledger and `paper/SECTION-III-EXECUTION-LOG.md`.
11. Stop at Gate G4 and wait for direct user approval.

Do not re-dispatch completed Tasks 10–12.

### Task 13 scientific requirements

Replace the old III-G **Architectural Interpretation** scaffold with the incentive-compatibility boundary. Required targets are:

- maximal-entanglement Hawk derivation
- Dove-deviation closed form
- numerical cross-check of the Dove-deviation result
- general-`gamma` Hawk regression and derivation
- restricted equilibrium boundary
- full-`SU(2)` honesty boundary

The section must state precisely what is proved, what is computationally checked, what holds only for the restricted strategy menu, and what is not established over full `SU(2)`.

### Task 13 verification requirements

At minimum:

- focused Hawk tests
- focused Dove tests
- `tests/test_ne_guard.py`
- practical-complete paper-claim tests
- paper-structure tests
- guarded control and final four-pass builds
- rendered-page inspection
- protected-PDF hash checks

After Task 13 is review-clean, stop. Do not begin Task 14 without Gate G4 approval.

## 9. Work after Gate G4

Only after direct G4 approval:

1. Task 14: Section III-H
2. Task 15: Section III-I
3. Task 16: Section III-J
4. Task 17: complete Section III integration and Gate G5
5. Task 18: inspect archived hardware artifacts and plan Section IV

No new hardware jobs are authorized.

Existing hardware evidence must not be overstated as a full restricted-menu equilibrium. Unless archived Dove-deviation executions are found, the defensible hardware statement remains that no profitable unilateral Hawk deviation was observed within the tested menu.

## 10. Handoff summary

Tasks 1–12 are implemented, tested, independently reviewed, and committed. Gates G1, G2, and G3 are approved. The rewritten manuscript currently runs through Section III-F and ends with the general-`gamma` GHZ cooperative-invariance proof.

Task 13 has not started. It is the next and only immediate implementation task. When its incentive-boundary mathematics is review-clean, stop at Gate G4 for direct user approval.
