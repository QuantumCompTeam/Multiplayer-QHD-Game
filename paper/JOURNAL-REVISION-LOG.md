# Journal revision, 7 September 2026

## Authorization and scope

The authors requested implementation toward a complete submission within
48 hours. After a concrete III-G draft and capped hardware registration were
prepared, the user explicitly instructed: "commit and run, no need of my
approval whatever is best do it". This authorizes the revised III-G boundary,
the scoped commits and hardware execution. The previous Task 12 stopping
point is historical; this revision does not require another G4 permission
request. The historical PDFs and prior experimental registrations are preserved.

## Claim and evidence addendum

| Claim | Evidence | Scope |
|---|---|---|
| Cooperative phase branches and exact incentive boundary | `incentive-boundary.tex`; `src/game/phase_branches.py`; `tests/test_journal_extensions.py` | Ideal GHZ; named finite strategy menu |
| Alternative branch works for every N at maximal angle | Same proof; finite dense cross-checks in `results/journal-strengthening/2026-09-07-offline/` | Mathematical scalability, not unlimited hardware or fixed-noise stability |
| Unrestricted counterstrategy defeats cooperative branches | Explicit analytic witness and dense unit tests | Single-qubit SU(2); rules out the claimed profiles, not every possible equilibrium |
| Four product branches; quadratic payoff evaluation | `src/game/compact_ghz.py`; dense comparisons; offline benchmark through N=128 | Ideal GHZ; classical algorithm, no computational quantum advantage |
| Original mean payoff rewards almost all bitstrings equally | Payoff identity and uniform-distribution unit tests | Uniform comparator is not a classical Nash equilibrium |
| Partial-conflict sensitivity | `src/game/observable_payoffs.py`; historical raw counts reweighted in offline results | Retrospective sensitivity, no new mitigated result or equilibrium claim |
| Global unilateral response oracle | `src/game/best_response.py`; numerical reconstruction checks; Landsburg precedent below | Fixed opponents and channel; not global equilibrium search |
| New hardware branch evidence | Committed manifests and QPY under `results/phase-validation/`; raw counts and job metrics in execution directories | Preserve registered pass/fail and all-player coverage; pilot cannot certify equilibrium |

## Literature addendum

Landsburg, *Nash Equilibria in Quantum Games*, Proc. AMS 139(12),
4423–4434 (2011), DOI 10.1090/S0002-9939-2011-10838-4.
Full publisher offprint accessed 2026-09-07:
https://www.thebigquestions.com/cv-academic/nashequilibria.pams.pdf.
Theorem 2.2, p.4427, explicitly identifies best responses with the largest
eigenvalue subspace of a real quadratic form on unit quaternions. Cited as
prior methodology; our implementation applies the single-gate quadratic
structure to fixed multiplayer opponents. No priority claim for this method.

Koh, Kumar and Goh, *Quantum Volunteer's Dilemma*, Phys. Rev. Research 7,
013104 (2025), DOI 10.1103/PhysRevResearch.7.013104. Author abstract and
journal metadata: https://arxiv.org/abs/2409.05708. Context only: a distinct
multiplayer cooperation game with analytic equilibrium results. It does not
establish novelty or validate the allocation rule in this manuscript.

## Scientific wording correction

The earlier phrase "not state fidelity" was too broad. The probability of
the all-zero outcome is the squared fidelity to the explicit pure target
|0...0>, although it does not establish fidelity to an arbitrary entangled
state. Manuscript structure checks now enforce that physically correct
scope instead of the earlier blanket exclusion.

## Reproducibility

Historical simulation environment remains pinned and unchanged. IBM's saved
platform-channel account requires a current runtime, isolated in
`.venv-hardware`. Its exact dependency freeze accompanies the pilot
registration. New circuits are checked against the dense ideal operator,
then against ideal compiled output, and rehearsed with the selected device
noise model. Registrations are committed before submission and verified
byte-for-byte against HEAD. Actual charged QPU time is reported in each
result's provider metrics; execution caps are not usage measurements.

## Executed hardware and final validation

- Pilot `dafce6642tqs73avos70`: 18 pubs, 4096 shots, 21 charged seconds.
- Complete `dafchf5nj4cs73ag6jvg`: 70 pubs, 4096 shots, 77 charged seconds.
- Repeat `dafcikd1ierc738n6j90`: same 70 pubs, 77 charged seconds.
- Total 175 seconds; 425 seconds remain relative to the original 600-second
  budget, excluding any other account activity.
- The complete-family registered criterion fails in both runs. N=4 and N=6
  pass in both; N=3 and N=5 pass only in the first; N=7 is unresolved in both.
  The repeat's minimum observed gap is slightly negative, not a significant
  demonstrated profitable deviation. No pooling or retrospective threshold
  change is used to claim success. Repeat plan was committed before submission.
- The repetitions occurred in one session and are not presented as
  independent calibration epochs.
- Full historical-environment regression: 858 passed, 3 skipped. Additional
  raw-count replay tests check the saved judgments rather than trusting summaries.
- The revised PDF builds in an isolated directory with resolved citations and
  references. The source archive and separate PDF are in `paper/submission`.
