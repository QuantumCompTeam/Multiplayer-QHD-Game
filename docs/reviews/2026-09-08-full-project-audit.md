# Full-project audit and FQCNN-format revision

## Scope and review method

Starting revision: `6e7e65a`. Review branch: `review/full-audit-fqcnn-format`.
This is a fresh technical audit of the repository and the September 7 additions,
not an external scientific peer-review verdict. The review checks mathematical
claims against alternative parameter grids and dense circuits, exercises invalid
inputs and numerical failure paths, replays saved hardware judgments, inspects
the simulation/optimization/mitigation/configuration paths, checks cited sources,
and builds and inspects the complete manuscript.

The supplied `FQCNN_journal.pdf` is the local formatting reference. It is not
added to the repository or presented as QHD research evidence. Existing raw
hardware results, registrations, and protected historical PDFs are preserved.
No additional QPU jobs were submitted for this audit.

## Defects found and addressed

| Severity | Defect and consequence | Correction | Regression evidence |
|---|---|---|---|
| P1 | NaN probabilities pass ordinary range/sum comparisons; NaN payoff tensors can make every profile appear Nash. | Reject nonfinite probabilities, game values, and payoff tensors before computing/certifying incentives. | Nonfinite producer and direct-tensor rejection tests. |
| P2 | A short strategy list silently leaves unspecified player gates as identity; excess strategies fail only inside Qiskit. | Require exactly N strategies on noiseless and noisy paths. | Missing/excess strategy tests for both circuit runners. |
| P2 | Negative or NaN two-qubit noise ratios silently remove or distort the requested channel. | Require a finite nonnegative `p2_ratio`. | Negative, NaN, and infinite ratio tests. |
| P2 | An independent best-response reconstruction check returning NaN can be swallowed by `max`; nonfinite tolerance can bypass validation. | Check each oracle result and the tolerance explicitly for finiteness. | Injected NaN at an independent check; NaN/infinite tolerance tests. |
| P2 | Readout correction returns the optimizer's vector even when SLSQP reports failure. Empty/invalid counts can also yield misleading inputs. | Require successful optimization, a finite normalized result, valid count widths and frequencies, and positive shot count. | Failed-solver injection and malformed-count tests; existing mitigation round trips. |
| P2 | Symmetric Nash search ranks and stops on player-zero stability before inspecting asymmetric graph roles, potentially skipping a better seed. | Check every player before ranking a candidate or early stopping. | Synthetic hub-stable/leaf-unstable candidate followed by a valid seed. The old final all-player check already prevented a false final certificate; the defect was premature search termination. |
| P2 | Duplicate hardware row IDs overwrite summaries; mismatched bitstring widths and an infinite epsilon are accepted. | Reject duplicate IDs, width mismatch and nonfinite epsilon. | Invalid-registration-input tests plus replay of all three saved jobs. |
| P2 | Two automatic runs started in the same minute share an output directory and can overwrite evidence. | Allocate collision-resistant automatic directories using atomic creation; retain explicitly named grouping. | Two same-minute runs receive different directories; explicit grouping still works. |
| P2 | Fractional player counts are silently truncated by `int(N)`; nonfinite game configuration reaches execution. | Validate integer player counts and finite V, C, gamma before expansion. | Fractional/bool/too-small N and nonfinite configuration tests. |
| P2 | Related Work attributes this exact allocation payoff to Benjamin–Hayden. | Attribute the multiplayer circuit construction to that work and identify the allocation rule separately. | Full-text source inspection described below. |
| P3 | Gamma comments say cooperative payoff falls away from maximal entanglement; the Q docstring says the two-player phase fails for every N>2. | State the correct phase-preservation and incentive distinction, including even-N cooperative branches. | Dense proof grid over every phase branch at N=2..6, three nonmaximal angles and V<C. |
| P3 | Active README and manuscript still describe a pending Task 12/III-G handoff; one test enforces that stale sentence. | Update active status, cross-references and the corresponding manuscript contract. Historical logs remain historical. | Document-anchor and manuscript-contract checks. |
| P3 | Compact-evaluation timing could be read as including quadrature setup. | State that the contraction is quadratic with available nodes and that benchmark timings warm the node cache. | Inspection of the benchmark procedure and manuscript wording. |

The initial 22 invalid-input/failure-path regression cases all failed against
the pre-fix code. They pass after correction. Subsequent tests cover premature
Nash-search stopping, result-directory collisions, configuration validation,
and the broader mathematical parameter grid.

## Scientific and provenance review

- The cooperative phase family, exact D/H incentive inequality, alternative
  phase, and unrestricted witness agree with the independent dense checks.
  The all-N statement remains ideal and restricted to the named menu.
- The compact representation and payoff contraction are consistent with the
  dense reference on tested finite sizes. This is classical analysis scaling,
  not a physical 128-player experiment or a quantum speedup.
- All three September 7 judgments are recomputed from raw provider counts.
  Their pass/fail decisions are unchanged by validation hardening.
  `scripts/audit_phase_evidence.py` independently implements the raw-bitstring
  payoff and simultaneous confidence-bound arithmetic without importing the
  production payoff or judging functions, and checks frozen source hashes.
- The two full batches both fail their overall five-size registration. N=4,6
  pass in both; N=3,5 pass only in the first; N=7 is unresolved in both.
- Every source hash in the pilot and full registrations exactly matches its
  committed pre-execution source bytes at `b9aaf5a` / `76aa8fd`.
- All five retrospective sensitivity input hashes still match the retained
  historical result files.
- The hardened current code intentionally differs from registered execution
  code. The supplement preserves the frozen source revision. Live recovery or
  resubmission must use the appropriate committed checkout rather than bypassing
  a source-hash failure. Historical manifests are not edited to fit new code.
- Original QPU charge remains 175 seconds for the three jobs; this audit uses
  no additional device quota.

Benjamin and Hayden's [full paper](https://arxiv.org/pdf/quant-ph/0007038),
especially pp. 2–4, supplies the EWL multiplayer construction and minority-game
and Prisoner's-Dilemma examples. It does not supply the allocation rule used
here. Landsburg's quadratic-form result remains methodological precedent,
not a claimed new best-response theorem. Existing abstract-only literature
restrictions remain in force.

## FQCNN formatting and structure

The reference PDF is letter paper (612 x 792 points), uses a 10pt Times-family
body, a roughly 24pt centered title, centered author blocks, two columns,
black section headings, Roman section numbers, lettered subsections, and
standard IEEE figure/table captions. QHD now uses
`IEEEtran[conference,letterpaper,10pt]` to match those features. Its authors,
research title, equations, and evidence remain QHD-specific.

The reference's nine-part sequence is adapted as:

1. Introduction
2. Related Work
3. Evaluation Questions and Evidence Boundaries
4. Proposed N-Player Quantum Hawk–Dove Framework
5. Computation and Validation Protocol
6. Experimental Results and Analysis
7. Discussion
8. Novelty and Technical Differentiation
9. Conclusion, preceded by unnumbered Data and Code Availability

New `evaluation-boundaries.tex` gives the question/evidence/claim-boundary table.
New `validation-methods.tex` gathers exact simulation, noisy compilation, and
uncertainty procedures. Hardware setup moves into `hardware-setup.tex` under
methods. Simulation and hardware result subsections move under the combined
results section; interpretation and limitations move under Discussion.
Section references use labels so the reorganization does not hard-code old
numbers. Tests expand included TeX files to verify the actual section order,
unique labels, and resolved references.

This matches the user's supplied PDF layout. It is a journal-content manuscript
using that reference's conference-style class, not a claim that the layout is
the branded TQE publisher shell. The historical shell is retained as an asset.

## Submission and accessibility

GitHub initially reported the repository PRIVATE. The user changed visibility
during the audit, and GitHub subsequently reported PUBLIC. The manuscript now
uses the public repository URL. The supplement additionally gives reviewers a
fixed, hashed snapshot of code, tests, experiments, data and source provenance.

The LaTeX source archive includes IEEEtran.cls and the current included TeX
files. The code-and-data archive includes the exact pre-execution source under
`frozen-phase-code/` and an evidence manifest. Accounts, credentials, local
virtual environments and the supplied reference PDF are excluded.

## Remaining scientific limitations

No test suite guarantees absence of every defect. In particular, hardware
stationarity, correlated drift, mitigation model adequacy and economic realism
cannot be established by code tests. The repeated jobs are within one session,
not independent calibration epochs. Symmetric candidate search remains limited,
the menu is externally stipulated, and both cooperative branches fail against
the explicit unrestricted SU(2) witness. Those are retained scientific limits,
not issues hidden by the fixes or converted into passing acceptance tests.

## Validation record

Completed full-suite, archive-integrity and PDF-build results are recorded
in `2026-09-08-validation.md`. PR #22's Linux CI passed with 899 tests and
3 skips after the figure follow-up. Subsequent Macroscope corrections and
their validation are recorded in `2026-09-08-macroscope-resolution.md`;
the latest PR checks govern readiness of that revision.
