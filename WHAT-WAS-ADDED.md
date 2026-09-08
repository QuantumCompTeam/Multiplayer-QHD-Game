# Complete Record of the September 2026 Journal-Strengthening Work

This document records the work added to **Multiplayer-QHD-Game** during the
48-hour IEEE Transactions on Quantum Engineering submission push. It covers
the scientific results, implementation, IBM hardware executions, manuscript
changes, validation, commits, and remaining author actions.

## 1. Main scientific additions

### 1.1 Cooperative phase family and corrected scaling law

The original project used

\[
Q_N=U(0,\pi/N,\pi/N).
\]

The revision generalizes this to the phase family

\[
Q_{N,m}=U(0,m\pi/N,m\pi/N),
\]

where integer `m` labels a phase branch. Every such branch returns the ideal
GHZ protocol to the cooperative outcome, up to a global phase.

A new alternative branch was defined as

\[
Q_N^\star=Q_{N,\lfloor N/2\rfloor}.
\]

At maximal entanglement, this branch is a strict Nash equilibrium within its
explicit finite menu `{D, H, Q_N*}` for every `N >= 2`. This repairs the
player-count failure of the original `m=1` phase within that restricted menu.

### 1.2 Exact incentive-compatibility boundary

For a unilateral deviation from the cooperative phase profile, the revision
derives

\[
t=\sin^2\gamma\sin^2(m\pi/N),
\]

\[
\pi_j(H,Q_{-j})=V(1-t), \qquad
\pi_j(D,Q_{-j})=(V-Ct)/N.
\]

The cooperative profile is a Nash equilibrium in `{D, H, Q_(N,m)}` exactly
when

\[
\sin^2\gamma\sin^2(m\pi/N)\ge 1-1/N.
\]

This produces a precise boundary in player count, cooperative phase, and
entanglement angle instead of relying only on numerical enumeration.

For the original `m=1` strategy, the restricted equilibrium survives only at
`N=2,3`. At `N=4` and above a Hawk deviation is profitable.

### 1.3 Explicit unrestricted-SU(2) counterexample

The revision also proves the important limitation that neither cooperative
phase branch is a Nash equilibrium against arbitrary single-qubit SU(2)
strategies. Against `Q_(N,m)`, the deviation

\[
U(\pi,0,-m\pi/N)
\]

produces the sole-Hawk outcome with certainty and pays the deviator `V`. Its
gain over cooperative play is `V(1-1/N)`.

This turns the restricted-strategy caveat into a constructive mathematical
result rather than a generic disclaimer.

### 1.4 Compact GHZ payoff evaluation through N=128

The ideal GHZ output was rewritten as a sum of at most four product states:

\[
|\psi_{out}\rangle=c^2A+icsB-icsX^{\otimes N}A+s^2X^{\otimes N}B,
\]

with `c=cos(gamma/2)`, `s=sin(gamma/2)`,
`A=(tensor_j U_j)|0...0>` and `B=(tensor_j U_j)|1...1>`.

Consequences:

- The ideal GHZ state has Schmidt rank at most four across every bipartition.
- Payoffs can be evaluated without allocating a `2^N` probability vector.
- The expectation involving `x_j/k` is evaluated with an exact polynomial
  integral and Gauss-Legendre quadrature.
- Prefix and suffix products give all-player payoff evaluation in quadratic
  classical work.
- Dense and compact calculations were cross-checked through `N=7`.
- The resource experiment was run through `N=128`.

This is mathematical and classical-simulation scalability. It is not a claim
of 128 simultaneous hardware qubits or computational quantum advantage.

### 1.5 Global unilateral best-response oracle

A fixed player's SU(2) strategy is represented by a real unit quaternion
`q`. With all opponents fixed, that player's payoff is a real quadratic form

\[
q^T M_j q.
\]

Ten circuit evaluations reconstruct the symmetric `4 x 4` matrix. Its largest
eigenvalue gives the global unilateral best-response payoff and its eigenvector
gives a witness strategy. Independent evaluation points validate the fitted
quadratic form and final witness.

This replaces local heuristic response optimization for fixed opponents. It
does not prove that symmetric profile searches find every equilibrium.

### 1.6 Payoff-observable sensitivity

For the original payoff rule, mean welfare obeys

\[
\bar\pi=V/N-(C/N)p(1^N).
\]

Therefore nearly every outcome except all-Hawk preserves the analytic
cooperative welfare. Uniform independent random bits retain
`1 - 2^(-N)` of the ideal analytic-baseline advantage, which is `99.21875%`
at `N=7`.

This explains why payoff advantage can remain high after the target-state
population has fallen. It also shows why high mean payoff alone is a weak
test of cooperation or equilibrium.

### 1.7 Partial-conflict sensitivity model

A parameterized alternative payoff rule was added:

\[
L_ell(k)=C[(1-ell)1_{k=N}+ell\,k(k-1)/(N(N-1))].
\]

It preserves the original endpoints and the two-player game while charging
for partial Hawk-Hawk conflicts. Historical raw hardware counts were
reweighted at `ell = 0, 0.25, 0.5, 1`.

At `ell=1`, recorded raw retention for `N=3..7` is approximately:

| N | Raw retention |
|---:|---:|
| 3 | 98.17% |
| 4 | 96.00% |
| 5 | 94.91% |
| 6 | 92.46% |
| 7 | 93.23% |

The uniform independent comparator is 75%. This analysis is retrospective and
does not constitute a new economic calibration or equilibrium test.

## 2. New IBM hardware work

All new runs used `ibm_fez` and prefixes of the pinned physical chain
`[141, 142, 143, 144, 145, 146, 147]`. Every circuit used 4096 shots.

### 2.1 Pilot

- Job: `dafce6642tqs73avos70`
- 18 circuits
- Charged QPU time: 21 seconds
- Tested one Hawk and one Dove deviation at `N=3,5,7`, plus controls.
- The measured deviations were discouraged at all sampled sizes.
- It was deliberately incapable of certifying equilibrium because it did not
  cover every player.

### 2.2 First complete batch

- Job: `dafchf5nj4cs73ag6jvg`
- 70 circuits
- Charged QPU time: 77 seconds
- Tested Hawk and Dove deviations for every player at `N=3..7`.
- Also included cooperative profiles, original-phase controls, unrestricted
  witnesses, and two calibration circuits.
- Every observed finite-menu deviation gap was positive.
- The registered 5% approximate-equilibrium criterion passed at `N=3,4,5,6`.
- The criterion failed at `N=7`, so the overall five-size registration failed.

### 2.3 Frozen same-chain repeat

- Job: `dafcikd1ierc738n6j90`
- Same committed 70 circuits and decision rule
- Charged QPU time: 77 seconds
- `N=4,6` passed again.
- `N=3,5` did not pass the conservative simultaneous bound in the repeat.
- `N=7` remained unresolved; its weakest point gap was slightly negative but
  did not establish a statistically significant profitable deviation.
- The two complete batches were judged separately and were not pooled to turn
  a failed registered test into a pass.
- The repeat occurred within the same session and is not claimed as evidence
  across independent calibration epochs.

Total provider-reported QPU charge for the three new jobs was **175 seconds**,
leaving 425 seconds relative to the original 600-second allocation, excluding
any unrelated account activity.

## 3. New source modules

### `src/game/phase_branches.py`

Provides the general phase strategy, alternative incentive-compatible branch,
analytic branch predictions, and unrestricted counterstrategy.

### `src/game/best_response.py`

Implements quaternion parameterization and the global fixed-opponent
best-response eigenvalue method.

### `src/game/compact_ghz.py`

Implements four-product-state GHZ payoff evaluation without dense outcome
enumeration.

### `src/game/observable_payoffs.py`

Implements payoff vectors from outcome counts, covariance and uncertainty
summaries, and the partial-conflict payoff family.

### `src/hardware/phase_validation.py`

Defines pilot and complete experiment rows, circuit-identity checks, ideal
probability checks, and simultaneous finite-sample judgment of all deviations.

### `src/game/strategy_opt.py`

The unilateral Nash-gap calculation now uses the global response oracle. The
cooperative symmetric optimizer remains a constrained numerical search.

## 4. New execution and analysis scripts

- `scripts/journal_analysis.py` generates the phase, compact-scaling, and
  payoff-sensitivity results and the three-panel journal figure.
- `scripts/prepare_phase_hardware.py` constructs circuits, pins the chain,
  records calibration, validates ideal behavior after compilation, performs a
  device-noise rehearsal, and creates immutable registration artifacts.
- `scripts/run_phase_hardware.py` requires the registration to be byte-identical
  to committed `HEAD`, checks source and QPY hashes, submits or recovers IBM
  jobs, saves pending job IDs before waiting, and writes raw counts and metrics.
- `scripts/summarize_phase_hardware.py` produces a concise per-size summary
  from saved provider results.
- `scripts/build_submission.py` performs the four-pass LaTeX/BibTeX build,
  checks unresolved references, preserves historical PDFs, and creates a
  separate submission PDF, source ZIP, and hash manifest.
- `docs/reviews/2026-09-07-scalability-probe.py` and its JSON output preserve
  the exploratory finite-grid phase analysis.

## 5. Reproducibility and safety improvements

- A modern isolated `.venv-hardware` was created because the historical pinned
  IBM Runtime version could not use the current saved platform-channel account.
- The historical environment was left unchanged.
- Exact modern hardware dependencies were frozen with the pilot registration.
- Hardware circuits are checked against the dense operator and complete ideal
  output before submission.
- Compiled measurement mapping is checked against the pinned chain.
- Device-noise rehearsals run before QPU submission.
- Registrations and serialized QPY circuits are committed before execution.
- Execution caps were 60 seconds for the pilot and 100 seconds for complete
  batches; actual charged time is read from provider metrics.
- Pending job IDs are saved immediately so interrupted jobs can be recovered
  without duplicate submission.
- An automatic pytest fixture redirects test-generated result directories to a
  temporary location, preventing tests from rewriting historical evidence.

## 6. New tests and validation

### Tests added

- `tests/test_journal_extensions.py` checks the analytic phase formulas,
  restricted equilibrium boundary, unrestricted witness, compact GHZ payoffs,
  payoff sensitivity, uniform comparator, hardware circuit identities, and
  best-response reconstruction.
- `tests/test_registered_phase_results.py` reloads saved provider counts and
  recomputes each registered judgment rather than trusting copied summaries.
- `tests/test_paper_structure.py` was corrected so that it now states the
  physically accurate fidelity relationship.
- `tests/conftest.py` isolates test result writes.

### Validation completed

- Full historical-environment suite: **858 passed, 3 skipped**.
- Final focused science/manuscript/hardware replay suite:
  **425 passed, 3 skipped**.
- New extension tests in the modern hardware environment: **40 passed**.
- Revised manuscript: successful four-pass LaTeX/BibTeX build.
- September 7 PDF: 17 pages; current validated submission PDF: 18 pages.
- Source ZIP integrity: all entries passed CRC validation.
- No unresolved citations or references.
- Historical `paper/qhd.pdf` and root `qhd.pdf` were preserved byte-for-byte.

## 7. Manuscript changes

### Title and abstract

The title is now:

> Incentive Compatibility and Payoff Robustness in Multiplayer Quantum Games:
> Theory and Hardware Evidence

The abstract now distinguishes ideal restricted equilibrium, unrestricted
failure, mathematical scalability, hardware player count, high payoff
retention, and failed hardware criteria.

### Section III-G

`paper/incentive-boundary.tex` contains the formal phase-family proposition,
proof, alternative branch, unrestricted counterstrategy, and entanglement-angle
boundary.

### New simulation results

`paper/journal-results.tex` adds:

- alternative-phase incentive gaps;
- compact GHZ evaluation through `N=128`;
- the fixed-opponent global response oracle;
- original-payoff sensitivity;
- partial-conflict reweighting;
- the new three-panel figure.

### New hardware results

`paper/phase-hardware-results.tex` reports the pilot, complete batch, repeat,
confidence construction, pass/fail outcomes, QPU usage, and interpretation
limits.

### Limitations and scalability

`paper/journal-limitations.tex` now explicitly separates:

- mathematical scalability;
- classical computational scalability;
- physical qubit-count scaling;
- shrinking incentive margins;
- restricted-menu versus arbitrary-SU(2) equilibrium;
- centralized preparation and decoding assumptions;
- payoff-model sensitivity;
- topology versus circuit-budget effects;
- star role asymmetry versus ring circuit-order asymmetry;
- simplified noise models and mitigation assumptions;
- calibration drift and within-session replication;
- unresolved `N=7` incentives;
- the provisional nature of adaptation results;
- the illustrative status of market analogies.

### Literature and terminology corrections

- Added Landsburg's 2011 quadratic-form best-response precedent.
- Added Koh, Kumar and Goh's 2025 multiplayer quantum volunteer's dilemma as
  contextual prior work.
- Retained the Benjamin-Hayden warning about enlarged strategy spaces.
- Removed wording that implied entanglement eliminates external trust or
  institutions.
- Corrected “not state fidelity”: `P(0^N)` equals squared fidelity to the
  explicit pure target `|0...0>`, but it is not fidelity to an arbitrary ideal
  entangled state and does not determine other populations or coherences.
- Replaced remaining incorrect “ground-state probability” wording with
  “target-state population.”

### Submission presentation

- Removed the template's placeholder DOI and publication date language.
- Replaced the sample 2016 volume footer with “Manuscript for peer review.”
- Added an IEEE-policy-compatible acknowledgment of Codex-assisted generated
  text, code, and analyses, together with the validation level.
- Added an editor cover-letter draft and submission checklist.

## 8. New figures, reports, and records

- `paper/figs/journal_extensions.pdf`
- `results/journal-strengthening/2026-09-07-offline/results.json`
- `results/journal-strengthening/2026-09-07-offline/report.md`
- `results/journal-strengthening/2026-09-07-offline/journal_extensions.pdf`
- `results/journal-strengthening/2026-09-07-offline/journal_extensions.png`
- `docs/reviews/2026-09-07-journal-strengthening-plan.md`
- `paper/JOURNAL-REVISION-LOG.md`
- Addenda in `paper/CLAIM-SOURCE-MAP.md`, `paper/LITERATURE-AUDIT.md`, and
  `paper/SECTION-III-EXECUTION-LOG.md`.
- Immutable registrations, QPY files, rehearsals, calibration snapshots, raw
  counts, judgments, and provider metrics under `results/phase-validation/`.

## 9. Submission artifacts

The ready-to-review deliverables are:

- `paper/submission/qhd-submission-draft.pdf`
- `paper/submission/qhd-latex-source.zip`
- `paper/submission/build-manifest.json`
- `paper/submission/cover-letter-draft.md`
- `paper/submission/README.md`

No journal submission was made automatically.

Before portal upload, the authors must personally confirm:

- corresponding author;
- approval of the final manuscript by both authors;
- funding statement;
- competing-interest statement;
- any related, prior, or concurrent submissions;
- final public repository/data URL;
- whether the manuscript acknowledgment accurately describes the AI assistance.

## 10. Honest interpretation of the strengthened paper

The strongest defensible claims are now:

1. The cooperative phase is a family, and the original `pi/N` choice is not
   incentive-compatible beyond three players in the stated finite menu.
2. A different phase branch supplies an ideal all-`N` restricted-menu
   equilibrium, but an explicit SU(2) deviation defeats both cooperative
   branches when the strategy space is unrestricted.
3. Ideal GHZ payoffs can be evaluated compactly through much larger `N`
   without dense state enumeration.
4. Mean payoff can outlive target-state concentration because of the payoff
   observable, so welfare retention and incentive compatibility must be
   measured separately.
5. On current hardware, the alternative phase gives reproducible registered
   incentive support at `N=4,6`; `N=7` remains unresolved despite high mean
   payoff retention.
6. Much of the apparent topology robustness ordering is explained by compiled
   two-qubit gate budget, while W remains a per-gate structural outlier.

The paper does not claim continuous-SU(2) Nash equilibrium, distributed-market
deployment, computational quantum advantage, or unlimited physical scaling.

## 11. Commits created

| Commit | Purpose |
|---|---|
| `b9aaf5a` | Add verified phase incentives and register capped IBM pilot |
| `76aa8fd` | Record pilot and preregister complete deviation batch |
| `cefa199` | Preserve first complete result and freeze replication plan |
| `d32b9b0` | Add manuscript proof, compact scaling, limitations, and replicated hardware evidence |
| `eefbba6` | Finalize review footer and validation notes |
| `3225edd` | Package reviewed PDF and portable LaTeX source |

The work was performed on branch `docs/qhd-task12-handoff`.

## 12. September 8 audit and reference-format revision

The follow-up branch `review/full-audit-fqcnn-format` hardens numerical and
configuration validation, fixes premature asymmetric Nash-search stopping and
automatic result-directory collisions, and adds 37 regression/structure tests.
It also adds an independent raw-count evidence audit and portable-archive check.
The paper now follows the supplied FQCNN PDF's IEEEtran layout and nine-section
structure. A hashed code-and-data supplement preserves current and frozen
pre-execution sources. No further QPU time was spent.

See [the complete findings](docs/reviews/2026-09-08-full-project-audit.md) and
[the validation record](docs/reviews/2026-09-08-validation.md) for defects,
checks, and remaining scientific limitations.
