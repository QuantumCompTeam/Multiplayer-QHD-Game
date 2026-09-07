# Section III Execution Log

One entry per task: date, commands run, test results, new warnings,
page count, evidence classifications, gate decisions, approved exceptions.

## 2026-07-31 — Task 1, Steps 1–2

- Command: `diff paper/main.tex paper/qhd.tex > paper/.main-vs-qhd.diff; wc -l paper/.main-vs-qhd.diff`
- Result: `709 paper/.main-vs-qhd.diff`
- Classification: body-content divergence confirmed, not a preamble-only difference.
- `main.tex`-specific structure/content: the long-form abstract; combined `Background and Related Work`; separate `Model and Methods`; a top-level `Discussion`; and an unnumbered `Reproducibility` statement with repository, pinned software versions, and artifact traceability.
- `qhd.tex`-specific structure/content: an introduction roadmap; a standalone four-part `Related Work`; a reorganized `Proposed N-Player Quantum Hawk--Dove Framework`; simulation- and hardware-configuration tables; explicit `Architectural Interpretation`, `Scalability and Practicality`, and `Limitations and Future Work` subsections; and a four-part `Novelty and Technical Differentiation` section.
- Gate decision: the Task 1 hard stop triggered. Canonical prose selection is pending user resolution; no template download, preamble migration, `main.tex` change, README change, build, or figure change was performed.
- Page count: not measured because the hard stop precedes build verification.
- New warnings: none; no LaTeX build was run.
- Approved exceptions: none.

## 2026-07-31 — Task 1 resumed after user decision

- User decision: keep `paper/qhd.tex` as the canonical filename and temporary buildable scaffold; rewrite planned sections from scratch later, retaining only reverified relevant material.
- Source-bank snapshots created before manuscript edits:
  - `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/source-main-pre-phase1.tex` (SHA-256 `60bcdff0b3ce26b7b367639371a7de51ba3dd44ea1211f49fd3740fa8d8f5ac6`)
  - `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/source-qhd-pre-phase1.tex` (SHA-256 `c481dd3de87c66e1ce7301764dd1f3e926ea703d5cd64834ba5e46fa402d0f15`)
- Official source: IEEE Template Selector association for `Transactions, Journals and Letters` → `IEEE Transactions on Quantum Engineering` → `Original Research` → `LaTeX`.
- Metadata URL: `https://template-selector.ieee.org/api/ieee-template-selector/template/publication-type/1/publication-title/222`
- Download URL: `https://template-selector.ieee.org/api/ieee-template-selector/template/498/download`
- Archive: `TQE_Template.zip`; SHA-256 `8dfc37d3b07b62b99154e05aa01a5419865e4a3ea2b270a3c18931fced413528`; selector metadata created `2020-05-22T11:28:13Z`; sample title identifies the template as March 2020.
- Verified shell conventions from `tqe.tex`: `\documentclass{ieeeaccess}` with no options; `\history` and `\doi`; `\author` with `\authorrefmark`; `\address`; `\tfootnote`; `\markboth`; `\corresp`; `abstract` then `keywords`; `\titlepgskip=-15pt`; `\maketitle` after abstract and keywords.
- Installed official shell files from the verified archive: `paper/ieeeaccess.cls`, `paper/logo.png`, `paper/notaglinelogo.png`, and `paper/bullet.png`.
- Applied front matter: `\documentclass{ieeeaccess}` with no options; official `\history` and `\doi` placeholders; `\author`/`\authorrefmark`; two `\address` entries; `\markboth`; `abstract`; `keywords`; `\titlepgskip=-15pt`; and `\maketitle` after abstract/keywords. `\tfootnote` was omitted because no verified funding/support statement was available. `\corresp` was also omitted: `ieeeaccess.cls` initializes the field to empty, and no source establishes either author as corresponding author.
- Body-integrity check: PASS. The literal bytes beginning with `\section{Introduction}` and ending immediately before `\bibliographystyle{IEEEtran}` match the pre-Phase-1 `qhd.tex` snapshot exactly. Snapshot and current SHA-256: `7c4cd40d8ad085479aec357ebd284a82cd008e1979df6690175096ea93caf85f`. Figures were unchanged.
- Compatibility controls required by the official class while preserving body floats: preamble dimension `\xfigwd` for standard `figure` captions and terminal `\EOD`, as required by `ieeeaccess.cls`.
- Competing entry point: `paper/main.tex` converted to the required two-line deprecated wrapper; canonical entry remains `paper/qhd.tex`.
- README: target changed from IEEE QCE to IEEE TQE; build commands target `qhd.tex`; the inventory now states seven figures and includes `figs/hardware_topology.pdf`; the stale claim that Aasa's email was omitted was corrected.
- Exact pre-migration rebuild commands:
  1. `cd paper && rm -rf .qhd-pre-fix-check && mkdir .qhd-pre-fix-check`
  2. `pdflatex -interaction=nonstopmode -halt-on-error -jobname=qhd-pre -output-directory=.qhd-pre-fix-check ../.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/source-qhd-pre-phase1.tex > .qhd-pre-fix-check/pass1.stdout 2>&1`
  3. `bibtex .qhd-pre-fix-check/qhd-pre > .qhd-pre-fix-check/bibtex.stdout 2>&1`
  4. `pdflatex -interaction=nonstopmode -halt-on-error -jobname=qhd-pre -output-directory=.qhd-pre-fix-check ../.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/source-qhd-pre-phase1.tex > .qhd-pre-fix-check/pass2.stdout 2>&1`
  5. `pdflatex -interaction=nonstopmode -halt-on-error -jobname=qhd-pre -output-directory=.qhd-pre-fix-check ../.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/source-qhd-pre-phase1.tex > .qhd-pre-fix-check/pass3.stdout 2>&1`
- Pre-migration rebuild output: `pre_migration_four_pass_exit=0`; 11 pages; 0 overfull boxes; 1 font warning (`LaTeX Font Warning: Font shape 'OT1/ptm/m/scit' undefined`); 13 underfull boxes; and 14 repetitions of `Package hyperref Warning: Token not allowed in a PDF string (Unicode):`.
- Exact post-migration rebuild commands:
  1. `cd paper && rm -rf .qhd-build-check && mkdir .qhd-build-check`
  2. `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex > .qhd-build-check/pass1.stdout 2>&1`
  3. `bibtex .qhd-build-check/qhd > .qhd-build-check/bibtex.stdout 2>&1`
  4. `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex > .qhd-build-check/pass2.stdout 2>&1`
  5. `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex > .qhd-build-check/pass3.stdout 2>&1`
- Post-migration rebuild output: `post_migration_four_pass_exit=0`; 11 pages; no undefined references, undefined citations, emergency stop, fatal error, or other `LaTeX Warning` lines.
- Newly introduced exact overfull-box lines:
  - 2 occurrences: `Overfull \\hbox (9.2679pt too wide) in paragraph at lines 87--87`
  - 23 occurrences: `Overfull \\hbox (505.12177pt too wide) has occurred while \\output is active`
  - 1 occurrence: `Overfull \\hbox (32.93878pt too wide) in paragraph at lines 515--524`
- Newly introduced font-warning lines: `LaTeX Font Warning: Font shape 'T1/ptm/n/n' undefined`; `T1/phv/n/n`; `T1/ptm/n/it`; `T1/pcr/n/n`; `T1/ptm/n/sc`; and `LaTeX Font Warning: Some font shapes were not available, defaults substituted.`
- Newly introduced underfull-box categories: 11 output-routine occurrences at badness 10000, plus body/title occurrences at badness 5592, 5316, 1371, 2302, 2409, 1668, and 1377. The 14 hyperref package-warning lines are unchanged in count and message.
- The repeated `505.12177pt` output-routine overfull line also occurs when compiling the official TQE sample and originates in the supplied `ieeeaccess.cls` header/footer implementation.
- Preserved artifact: `paper/qhd.pdf` SHA-256 remains `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`.
- Page count: 11 before migration; 11 after migration.
- Temporary build cleanup: `paper/.qhd-pre-fix-check` and `paper/.qhd-build-check` removed after evidence extraction; `paper/qhd.pdf` remained unchanged.
- Gate decision: Task 1 Steps 3–7 and fix round 1 complete. Do not proceed to Task 2 in this execution.

## 2026-07-31 — Task 2, post-migration non-destructive baseline

- Branch: `dev`.
- Starting-state command: `git status --short -- paper/qhd.tex paper/main.tex paper/README.md paper/references.bib paper/figs`.
- Starting-state output: ` M paper/README.md`; ` M paper/main.tex`; `?? paper/qhd.tex`. These are pre-existing Task 1 changes; `paper/references.bib` and `paper/figs` were clean.
- Destructive-cleanup guard: `paper/.qhd-build-check` was absent. The task used a fail-if-present precondition and did not delete an unexpected directory.
- Full gate command sequence, run from `paper/`:
  1. `mkdir .qhd-build-check`
  2. `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex`
  3. `bibtex .qhd-build-check/qhd`
  4. `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex`
  5. `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex`
- Build result: PASS. All four compiler/bibliography invocations exited 0; BibTeX ended with `Done.`; the final pass ended with `Output written on ...\.qhd-build-check\qhd.pdf (11 pages, 645314 bytes).`; and `paper/.qhd-build-check/qhd.pdf` existed before cleanup.
- Required final-log scan:
  - `LaTeX Warning`: 0 matches.
  - `undefined references`: 0 matches.
  - `Citation .* undefined`: 0 matches.
  - `Emergency stop`: 0 matches.
  - `Fatal error`: 0 matches.
  - `Overfull \\hbox`: 26 matches in three disclosed categories: 2 occurrences of `Overfull \\hbox (9.2679pt too wide) in paragraph at lines 87--87`; 23 occurrences of `Overfull \\hbox (505.12177pt too wide) has occurred while \\output is active`; and 1 occurrence of `Overfull \\hbox (32.93878pt too wide) in paragraph at lines 515--524`.
- Supplemental final-log baseline: 6 LaTeX font-warning lines, 14 repeated hyperref PDF-string warning lines, 18 underfull-box lines (11 output-routine plus 7 body/title), 3 missing-font-map pdfTeX warnings, and 1 missing-destination pdfTeX warning for `section*.1`. MiKTeX also printed its update-check notice after each tool invocation.
- `pdfinfo .qhd-build-check/qhd.pdf`: 11 pages; page size `576 x 782.929 pts`; file size `645314 bytes`; PDF version `1.5`.
- Non-destructive artifact check: PASS. Before and after the build, both pre-existing PDFs remained byte-identical with SHA-256 `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`, size `569737`, and mtime `2026-07-26 23:36:29.604254600 +0530`:
  - `paper/qhd.pdf`
  - `qhd.pdf`
- Protected-input check: PASS. SHA-256 values were unchanged across the build for `paper/qhd.tex` (`79970f3f2ffa1a897fc9aae00cb85b731783ec4d941ab4ef035cf86a286cbfc6`), `paper/main.tex` (`2c4b2f1a9de70022e7fd92d5a0d2af6994f4ddf730760559af0ee8bfbf71f006`), `paper/README.md` (`ab0a247df82e434556dd1c7cd8dc75d2ac15ef5ef063407d253c3c72a66b77c9`), `paper/references.bib` (`6f4cd9f0b04f86e68c07be17413fe66714111cb2775eeba25df211fafa637e63`), and all seven files in `paper/figs/`.
- Cleanup: PASS. `rm -rf .qhd-build-check` removed only the temporary directory created by this task; the subsequent existence check reported `CLEANUP_PASS: paper/.qhd-build-check removed`.
- Files changed by Task 2 checkpointing: `paper/SECTION-III-EXECUTION-LOG.md` only. Manuscript prose, bibliography, figures, code, and tests were not edited.
- Gate decision: post-migration non-destructive baseline established for G1; later full gates must preserve the zero-match required diagnostics and must not add to the disclosed warning baseline.

## 2026-07-31 — Task 3, terminology, style, and claim-scope contracts

- Branch: `dev`.
- Requirements source: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-3-brief.md`.
- Created `paper/STYLE-GUIDE.md` with the required destination prefix followed by the exact source range `## 7. Prose Style Guide` through the end of Section 7.5, immediately before `## 8. Figure Redesign Specification`. Programmatic prefix and byte-for-text comparison: PASS.
- Created `paper/CLAIM-SOURCE-MAP.md` with the exact terminology table, canonical-symbol table, and evidence-label vocabulary required by the brief. Exact required-block comparison: PASS.
- Created `tests/test_paper_structure.py` with the planned four guards only. Exact planned-code comparison: PASS; no broader five-way vocabulary guard was added.
- Test command: `python -m pytest tests/test_paper_structure.py -v`.
- Exact test output:

```text
============================= test session starts =============================
platform win32 -- Python 3.9.13, pytest-7.4.4, pluggy-1.6.0 -- C:\Program Files\Python39\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\prith\Multiplayer-QHD-Game
configfile: pyproject.toml
plugins: anyio-4.9.0
collecting ... collected 4 items

tests/test_paper_structure.py::test_restricted_equilibrium_is_not_overstated PASSED [ 25%]
tests/test_paper_structure.py::test_no_hype_adjectives PASSED            [ 50%]
tests/test_paper_structure.py::test_section_iii_uses_canonical_target_state_name PASSED [ 75%]
tests/test_paper_structure.py::test_section_iii_does_not_claim_unsupported_state_fidelity PASSED [100%]

============================== 4 passed in 0.10s ==============================
```

- Planned-guard work items: none; all four guards pass against the pre-existing manuscript wording.
- Manuscript integrity: PASS. `paper/qhd.tex` remained byte-identical at SHA-256 `79970f3f2ffa1a897fc9aae00cb85b731783ec4d941ab4ef035cf86a286cbfc6`; semantic anchors `\label{sec:model}` and `\label{sec:sim}` remain present and unchanged.
- Figure integrity: PASS. All seven files in `paper/figs/` retained their pre-task SHA-256 values; no figure was edited.
- Page count: not measured; Task 3 requires structure tests and no LaTeX build or manuscript edit.
- Evidence classifications frozen: Proposition, Computational result, Simulation result, Registered hardware result, Observational hardware result, and Exploratory result.
- New warnings: none.
- Approved exceptions: none.
- Gate decision: Task 3 deliverables are complete and G1 materials are ready for review. Mathematical subsection drafting remains blocked until the user explicitly approves the canonical terminology, symbols, and style rules.
- G1 approval: approved by the user on 2026-07-31. The TQE shell, 11-page build baseline, canonical terminology, symbol assignments, evidence labels, and verbatim style guide are binding for subsequent tasks.

## 2026-07-31 — Task 4, Section III literature audit consolidation

- Branch: `dev`.
- Requirements source: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-4-brief.md`.
- Inputs consolidated (four completed read-only research lanes, all read, none modified):
  - `task-4-existing-bib-audit.md` (8 pre-existing bib entries re-verified)
  - `task-4-quantum-entanglement-sources.md` (8 sources: EWL, multiplayer quantum games, GHZ/W, graph states/automorphisms, equilibrium criticism)
  - `task-4-classical-network-sources.md` (7 sources: classical/multiplayer Hawk-Dove, strict dominance/welfare framing, network games)
  - `task-4-noise-mitigation-sources.md` (9 sources: depolarizing noise, readout mitigation, ZNE/gate folding, observable-specific resilience, circuit routing)
  - `paper/CLAIM-SOURCE-MAP.md` (read for approved G1 terminology/symbol consistency; not modified)
- Created `paper/LITERATURE-AUDIT.md` using the exact schema from the brief (BibTeX key, research strand, claim supported, publication, year, peer-review status, DOI/publisher URL, evidence access, locator, support type, verification status, notes).
- Deduplication across lanes: `eisert1999`/`eisert1999quantum` merged to existing key `eisert1999` (same DOI `10.1103/PhysRevLett.83.3077`); `benjamin2001`/`benjamin2001multiplayer` merged to existing key `benjamin2001` (same DOI `10.1103/PhysRevA.64.030301`); `temme2017`, `kandala2019`, `nation2021` re-verified by the noise-mitigation lane against the same existing-bib DOIs with no metadata discrepancy. A cross-lane evidence-access discrepancy on `eisert1999` (one lane full text, one lane abstract-only after a failed PDF re-fetch) was reconciled in favor of the lane with a specific equation/quote locator; recorded in `paper/LITERATURE-AUDIT.md`.
- Source count: **27 unique verified sources** after deduplication (8 pre-existing + 19 newly added). 21 of 27 at `full text` evidence access; 6 at `abstract only` (`varsamis2025`, `maynardsmith1973`, `broom1997`, `wood2015`, `dawes1980`, `galeotti2010`), each restricted to a contextual/definitional claim only, per the audit rule.
- Threshold check (brief requires ≥18 verified Section III sources at the full locator standard): **met**. 18 full-text sources map directly onto the brief's 12 named strands; 3 additional full-text sources (`nash1951`, `cross2019`, `li2019sabre`) extend beyond the literal 12-strand list and are recorded as bonus margin, not counted toward padding the minimum. No shortfall to disclose.
- CRITICAL FINDING recorded prominently in `paper/LITERATURE-AUDIT.md`: `nation2021` (M3) is matrix-free and does **not** perform tensored confusion-matrix inversion; `maciejewski2020` is the direct source for the tensor-product confusion matrix (Sec. 3.3.2, Eq. 15) plus constrained least squares (Sec. 4.3, Eq. 25); `bravyi2021pra` is contextual for the tensored noise model (Sec. III, Eq. 5) and direct for observable-specific error resilience (Sec. II, Eq. 2). `paper/qhd.tex` lines 211 and 654 currently cite `nation2021` for "tensored confusion-matrix inversion (constrained least squares)" — confirmed by direct grep of the manuscript — and this citation must be corrected during Section III drafting. No edit was made to `paper/qhd.tex` by this task.
- Updated `paper/references.bib`: added 19 new verified entries (`benjamin2001comment`, `vanenk2002classical`, `duer2000three`, `hein2004multiparty`, `hansenne2022symmetries`, `marinatto2000quantum`, `maynardsmith1973`, `broom1997`, `wood2015`, `nash1951`, `dawes1980`, `galeotti2010`, `teixeira2021`, `georgopoulos2021`, `maciejewski2020`, `bravyi2021pra`, `giurgicatiron2020`, `cross2019`, `li2019sabre`), each with a Section III claim named in `paper/LITERATURE-AUDIT.md`. All 8 pre-existing entries preserved unchanged; no entries deleted.
- BibTeX-key uniqueness check, exact command from the brief:

```bash
python - <<'PY'
from pathlib import Path
import re
text = Path("paper/references.bib").read_text(encoding="utf-8")
keys = re.findall(r"@\w+\{([^,]+),", text)
dupes = sorted({key for key in keys if keys.count(key) > 1})
assert not dupes, f"duplicate BibTeX keys: {dupes}"
print(f"verified bibliography entries present: {len(keys)}")
PY
```

- Exact output: `verified bibliography entries present: 27`. No duplicate keys (assertion passed). Count matches the 27-row `paper/LITERATURE-AUDIT.md` table exactly.
- Files touched by this task: `paper/LITERATURE-AUDIT.md` (created), `paper/references.bib` (19 entries appended, 8 preserved unchanged), `paper/SECTION-III-EXECUTION-LOG.md` (this entry). `paper/qhd.tex`, figures, tests, and code were not edited.

## 2026-08-01 — Citation-misattribution fix (`nation2021` → `maciejewski2020`, `bravyi2021pra`)

- G2 approval: the user explicitly approved all 27 sources in `paper/LITERATURE-AUDIT.md` on 2026-08-01, clearing the Gate G2 condition ("This source list ... requires explicit user approval or removal before any row is cited in Section III manuscript prose") and authorizing immediate citation edits in `paper/qhd.tex`.
- Problem (per Critical Finding in `paper/LITERATURE-AUDIT.md`): `paper/qhd.tex` lines 211 and 654 cited `nation2021` (Nation et al., PRX Quantum 2, 040326 — M3) for tensored confusion-matrix inversion / constrained least squares. M3's own abstract states it "does not form the full assignment matrix, or its inverse" and is a matrix-free preconditioned iterative method — the opposite of the claim it was cited for.
- Correct attribution applied: `maciejewski2020` (Quantum 4, 257) — direct source for the tensor-product confusion matrix (Sec. 3.3.2, Eq. 15) and constrained-least-squares reconstruction (Sec. 4.3, Eq. 25) — plus `bravyi2021pra` (Phys. Rev. A 103, 042605) — contextual support for the tensored assignment-matrix model (Sec. III, Eq. 5). Both keys verified present in `paper/references.bib` (lines 282 and 296 respectively) before editing.
- Edit site 1, `paper/qhd.tex` line 211 (Related Work, "N-player hardware scalability and error mitigation" subsection):
  - Before: `tensored confusion-matrix inversion for readout errors~\cite{nation2021}`
  - After: `tensored confusion-matrix inversion for readout errors~\cite{maciejewski2020,bravyi2021pra}`
- Edit site 2, `paper/qhd.tex` line 654 (Sec.~\ref{sec:hardware}, "Scaling at N=3,4,5 with Error Mitigation"):
  - Before: `Readout errors are corrected by tensored confusion-matrix inversion (constrained least squares)~\cite{nation2021};`
  - After: `Readout errors are corrected by tensored confusion-matrix inversion (constrained least squares)~\cite{maciejewski2020,bravyi2021pra};`
- No other change made: paragraphs, numbers, results, tables, and figures untouched. `nation2021` is no longer cited anywhere in `paper/qhd.tex` (confirmed by grep, no matches); its bib entry remains in `paper/references.bib` unmodified per the task's file-scope restriction.
- Build verification (non-destructive, isolated from tracked build artifacts):
  - Confirmed `paper/.qhd-build-check` did not already exist before starting.
  - Created `paper/.qhd-build-check/`, copied `qhd.tex`, `references.bib`, `ieeeaccess.cls`, `bullet.png`, `logo.png`, `notaglinelogo.png`, and the `figs/` directory into it.
  - Four-pass build run inside that directory: `pdflatex -interaction=nonstopmode -halt-on-error qhd.tex` (pass 1, exit 0) → `bibtex qhd` (exit 0, no warnings) → `pdflatex ... qhd.tex` (pass 2, exit 0) → `pdflatex ... qhd.tex` (pass 3, exit 0, final).
  - Citation resolution: pass 1 and pass 2 logs show the expected transient "Citation `...` undefined" warnings for all keys (normal before/mid bibtex-aux propagation, including `maciejewski2020` and `bravyi2021pra` at lines 211/654). Pass 3 (final) log contains **zero** "Citation ... undefined" and zero "undefined references" warnings — confirmed by `grep -i undefined pass3.log`, which returned only five unrelated pre-existing `LaTeX Font Warning: Font shape ... undefined` lines (font-substitution cosmetics, not citation/reference errors, and not introduced by this edit).
  - `qhd.bbl` confirmed to contain `\bibitem{maciejewski2020}` and `\bibitem{bravyi2021pra}`; no `nation2021` entry present in the built `.bbl`/`.aux`.
  - Page count: `pdfinfo qhd.pdf` on the temp-directory build reports **11 pages** (569,737-byte original vs. 646,079-byte temp rebuild — size difference is expected MiKTeX/font-embedding non-determinism across separate build runs, not a content change; page count matches the G1-approved 11-page baseline exactly).
  - `paper/qhd.pdf` and root `qhd.pdf`: confirmed byte-identical and untouched (mtime `Jul 26 23:36`, size 569,737 bytes, unchanged before and after the build check).
  - Cleanup: `paper/.qhd-build-check/` removed after verification; confirmed absent afterward.
- Undefined citations in final log: **0**.
- Test run, exact command and output:

```
$ python -m pytest tests/test_paper_structure.py -v
============================= test session starts =============================
platform win32 -- Python 3.9.13, pytest-7.4.4, pluggy-1.6.0
collected 4 items

tests/test_paper_structure.py::test_restricted_equilibrium_is_not_overstated PASSED [ 25%]
tests/test_paper_structure.py::test_no_hype_adjectives PASSED            [ 50%]
tests/test_paper_structure.py::test_section_iii_uses_canonical_target_state_name PASSED [ 75%]
tests/test_paper_structure.py::test_section_iii_does_not_claim_unsupported_state_fidelity PASSED [100%]

============================== 4 passed in 0.06s ==============================
```

- Files touched by this task: `paper/qhd.tex` (two citation-key edits, lines 211 and 654), `paper/SECTION-III-EXECUTION-LOG.md` (this entry). No other file modified; no commit made.
- Gate decision: Gate G2 required before any of these 27 sources is cited in Section III manuscript prose. Present the source list grouped by strand (see `paper/LITERATURE-AUDIT.md`) for explicit user approval or removal. Do not proceed to manuscript drafting without that approval. This task was not committed.

## 2026-08-01 - Task 5, classical payoff and welfare regression checks

- Created `tests/test_paper_claims.py` with the four regression checks specified in the Task 5 brief, verbatim:
  - `test_payoff_tensor_matches_piecewise_formula_exhaustively` (N=2..7): every player's payoff in every one of the 2**N basis outcomes against the displayed piecewise payoff tensor.
  - `test_total_welfare_identity_for_every_basis_state` (N=2..8): total payoff is V for every outcome except all-Hawk, where it is V-C.
  - `test_hawk_strictly_dominates_dove_for_live_parameters` (N=2..8): at V=4, C=3, Hawk strictly beats Dove against every count of opposing Hawks.
  - `test_expected_mean_depends_only_on_all_hawk_probability` (N=2..7): mean expected payoff equals V/N - C*p(1^N)/N for random Dirichlet probability vectors.
- Bit-order convention confirmed against `src/game/payoffs.py` before writing tests: bit j of the outcome integer is player j's action, LSB = player 0 (`outcome_payoff` docstring; `index_to_bitstring` docstring). Matches the plan assumption; no test was rewritten to fit a guess.
- Command: `python -m pytest tests/test_paper_claims.py -v`.
- Environment discrepancy found and resolved: the default `python` on PATH is Python 3.9.13, which lacks `int.bit_count()` (Python 3.10+, used by `outcome_payoff`) and fails 19 of 26 cases with `AttributeError`. This contradicts `pyproject.toml` (`requires-python = ">=3.10"`). Re-running in the repo's `entangled-equilibria` conda environment (Python 3.10.20) passes cleanly. No test was weakened and no source file was modified to work around this.
- Result: 26 passed, 0 failed, 0.37s (Python 3.10.20, `entangled-equilibria`).
- Binding requirement for later tasks: all pytest runs importing from `src/` must use the `entangled-equilibria` environment. `tests/test_paper_structure.py` passes on either interpreter because it only scans source text, so a green structure-test run does not prove the environment is correct.
- Added a `## Section III-A / III-B evidence` table to `paper/CLAIM-SOURCE-MAP.md` mapping each III-A/III-B claim to a `Proposition` evidence label and its supporting test name. No pre-existing III-A/III-B rows existed; the Task 3 evidence-label vocabulary was reused rather than overloading a terminology row.
- `paper/qhd.tex`, figures, `references.bib`, and `src/` were not modified. No commit was created.

## 2026-08-01 - Task 6: Quantum Benchmark, Deviation, and Covariance Regression Checks

Ran `python -m pytest tests/test_paper_claims.py -v` in the `entangled-equilibria` conda environment (Python 3.10.20). Result: **104 passed**, 0 failed (26 pre-existing Task-5 cases + 78 new Task-6 cases). Confirmed exports before writing imports: `DOVE = (0.0, 0.0, 0.0)`, `HAWK = (math.pi, 0.0, 0.0)`, `q_strategy(N)` in `src/circuits/ewl.py`; `build_ewl_circuit(N, strategies, *, entangler=ghz_entangler, gamma=GAMMA)` (keyword-only `entangler`/`gamma`, default `GAMMA = math.pi/2`) in `src/circuits/n_player.py`; `ghz_entangler`, `star_entangler` in `src/circuits/topologies.py`.

Formulas tested and finite ranges:
- III-F cooperative fixed profile: $P(0^N)=1$ at $\gamma=\pi/2$ for $N=2,\ldots,8$; invariance of $P(0^N)=1$ across $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$ for $N=2,\ldots,7$; payoff vector $=V/N$ and mean advantage $=C/N$ for $N=2,\ldots,8$ at $V{=}4,C{=}3$.
- III-F Hawk deviation at maximal entanglement: closed form $4\cos^2(\pi/N)$ verified exactly (within 1e-10) for $N=2,\ldots,8$ at $\gamma=\pi/2$. This is the blocking check from the brief — it passed on first implementation; no reconciliation was needed.
- III-F Dove deviation: non-bindingness ($\pi_{\text{dev}}\le V/N$) verified across $N=2,\ldots,7$ and $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$ — kept as a computational result (stated finite grid only), not a proposition.
- III-G equilibrium boundary: not re-implemented; referenced `tests/test_ne_guard.py` node IDs in the claim-source map.
- III-I star-orbit covariance: leaf-payoff equality at $N=3$; leaf-SWAP operator invariance at $N=4,\gamma=\pi/2$. Hub-choice is not exposed by `star_entangler`, so the hub-relocation half of the operator check was not implemented; this limitation is recorded in `paper/CLAIM-SOURCE-MAP.md`.
- III-J single-flip welfare invariance: verified for every deviating player at $N=2,\ldots,8$, $V{=}4,C{=}3$.

Proposed labeling (for confirmation at gate G3): Proposition — GHZ cooperative output at $\gamma=\pi/2$ and across the tested $\gamma$ grid, GHZ payoff/advantage identity, Hawk-deviation closed form, equilibrium boundary (reused), star leaf-orbit covariance (both payoff-vector and operator-level), single-flip welfare invariance. Computational result — Dove-deviation non-bindingness across the finite $\gamma$ grid, and the pinned star $N{=}4$ per-player split $[0,1,1,1]$ (reused from `tests/test_asymmetric_advantage.py`).

`paper/CLAIM-SOURCE-MAP.md` updated with a new III-F/III-G/III-I/III-J evidence table and the star hub-choice limitation note.

## 2026-08-01 - Task 6 fix round 1 (redo after the earlier attempt died mid-edit)

- Review verdict being addressed: PASS / APPROVED-with-findings, one OPEN Important finding and one Minor finding. The original fix round never reached the file (agent lost on a network error), so `paper/CLAIM-SOURCE-MAP.md` was still byte-identical to the baseline snapshot `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-6-fix0-claim-source-map.md` at the start of this round (verified by `diff`, no output).
- File scope: `paper/CLAIM-SOURCE-MAP.md` only for the fix itself. `paper/qhd.tex`, `tests/`, `references.bib`, and figures were not touched; `paper/qhd.tex` remains at SHA-256 `282866a02e59edcb342b743d88837afddab52f3404f7f11c8cdfc962c363766f` (the post-citation-fix value).
- Important finding — labels presented as settled. Addressed in four places:
  1. New `### Label status convention` subsection under Evidence labels: every label in the tables is a proposal until confirmed at G3; a proposed Proposition rests on its regression check alone until the derivation exists in `paper/qhd.tex`; unfulfilled rows are demoted to Computational result over the stated finite range.
  2. Both table headings now read `... evidence (labels proposed, pending Gate G3)`.
  3. Both label columns renamed `Evidence label` → `Proposed evidence label`.
  4. A preamble under the III-F/G/I/J heading states that no III-F/G/I/J derivation exists in `paper/qhd.tex` yet.
- Important finding — sharpest case (Hawk deviation). The row label changed from `Proposition` to `Computational result today; Proposition proposed but contingent — see the note below`, plus a dedicated note recording that `tests/test_paper_claims.py::test_hawk_deviation_matches_closed_form_at_maximal_entanglement` is numerical only, that `tests/test_ne_guard.py::test_candidate_identities` carries the algebraically identical form $2+2\cos(2\pi/N)$, and that `tests/test_ne_guard.py::test_boundary_inequality_agreement` calls that identity "as computed, not proven". Promotion at G3 is conditioned explicitly on Section III-F supplying the derivation.
- Minor finding — bundled star row. The single III-I per-player-asymmetry row carrying the combined `Proposition / Computational result` label was split into four rows, each with one claim, one proposed label, and one test node ID: leaf-advantage equality at $N=3,4,5$ (Proposition, from the leaf-permutation automorphism); hub $\neq$ leaves at $N=4,5$ only (Computational result — the test parametrizes exactly `[4, 5]`, so the earlier "$N\geq4$" phrasing overstated the tested range and was corrected); scalar-advantage-is-the-mean plus the per-player $q = \text{classical} + \text{advantage}$ identity at $N=3,4,5$ (Proposition, definitional in `compute_advantage`); and the pinned $N{=}4$ split $[0,1,1,1]$ with scalar mean $0.75$ (Computational result, single pinned point). Ranges were read off the `@pytest.mark.parametrize` decorators in `tests/test_asymmetric_advantage.py`, not assumed.
- Scope note disclosed rather than silently widened: the Task 5 III-A/III-B table was also marked proposed/pending G3. The review named only the Task 6 labels, but those four rows carry the identical defect under the same definition (no manuscript derivation exists for III-A/III-B either), and leaving them settled while marking the Task 6 rows proposed would make the file self-contradictory. No III-A/III-B claim, label, or test node ID was otherwise changed.
- Test command and result: `conda run -n entangled-equilibria python -m pytest tests/test_paper_structure.py -v` → `4 passed in 0.07s`. No manuscript text changed, so no rebuild was required and no page count was measured.
- New warnings: none. Approved exceptions: none.
- Gate decision: fix round 1 complete, both findings closed, nothing committed. Task 7 (Section III-A) may begin and must hard-stop at Gate G3.

## 2026-08-01 - Task 7, rewrite III-A (Notation and the Classical $N$-Player Payoff Tensor)

- Branch: `dev`. Requirements source: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-7-brief.md`; target subsection definition from `docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md` §III-A.
- Pre-task snapshot: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-7-pre-qhd.tex`, SHA-256 `282866a02e59edcb342b743d88837afddab52f3404f7f11c8cdfc962c363766f` (identical to `paper/qhd.tex` at task start).
- Post-task `paper/qhd.tex` SHA-256: `38c9edbf1054563324b789e48727c71ea935224f79443bce336263f25a28f63f`.
- Edit scope: exactly one subsection replaced — `\subsection{Problem Formulation}` (the first subsection inside `\label{sec:model}`) became `\subsection{Notation and the Classical $N$-Player Payoff Tensor}` with new `\label{sec:notation}`. No other subsection, figure, table, or bibliography entry was edited. `paper/references.bib` was not modified: all three cited keys already existed from Task 4.
- Step 1 (reader question): the brief's opening sentence is used verbatim as the first sentence of the subsection.
- Step 2 (notation, dependency order): $\mathcal{N}=\{1,\ldots,N\}$; $x=(x_1,\ldots,x_N)\in\{0,1\}^N$; $x_j=1$ Hawk, $x_j=0$ Dove; $V>0$; $C>0$; then $k(x)=\sum_j x_j$ as Eq. (1), `\label{eq:hawk-count}`. Every symbol is defined before first use.
- Step 3 (tensor): the brief's four-branch piecewise equation inserted verbatim as Eq. (2), `\label{eq:payoff-tensor}`.
- Step 4 (examples): $N=4$ readings of the all-Dove ($k=0$), one-Hawk ($k=1$), and all-Hawk ($k=4$) outcomes, kept algebraic in $V$ and $C$. No simulation or hardware number appears in III-A.
- Step 5 (citations): `maynardsmith1973` for the two-strategy value-and-cost structure; `broom1997` for the general symmetric multi-player matrix-game framework; `benjamin2001` for the $N$-player extension route with worked $N=3,4$ cases. Each usage stays inside the scope limit recorded in `paper/LITERATURE-AUDIT.md`.
- Substantive correction made while drafting: the pre-rewrite text called the general formula "a Benjamin--Hayden tensor~\cite{benjamin2001}". The Task 4 audit records that `benjamin2001` contains no fully general closed-form $2^N$ payoff tensor (only worked $N=3,4$ cases), so III-A now credits that paper for the extension construction and states the general closed form as this paper's own. The overstated attribution still exists in the following subsection (the pre-rewrite III-B) and must be removed when Task 8 rewrites it.
- Terminology decision recorded: `paper/CLAIM-SOURCE-MAP.md` reserves "payoff vector" for $(\pi_1,\ldots,\pi_N)$. III-A therefore writes $P(x)=(P_1(x),\ldots,P_N(x))$ for the per-outcome profile and states explicitly that "payoff vector" is reserved for the expected payoffs introduced later, so the spec's phrase "payoff vectors" in III-A does not collide with the frozen term.
- Deferred cross-references (deliberate, to keep the build free of undefined references): III-A refers to the later metrics subsection and to the next subsection in semantic prose without `\ref`, because `sec:metrics` and the III-B label do not exist yet. Task 17's flow pass wires these into semantic `\ref` form once the labels exist.
- Step 6, focused claim test, exact command and result: `conda run -n entangled-equilibria python -m pytest tests/test_paper_claims.py::test_payoff_tensor_matches_piecewise_formula_exhaustively -v` → `6 passed in 3.37s` ($N=2,\ldots,7$). Structure guards re-run afterwards: `tests/test_paper_structure.py` → `4 passed in 0.07s`.
- Step 7, build: non-destructive four-pass build in `paper/.qhd-build-check/` (copied inputs), plus a control four-pass build of the pre-task snapshot in `paper/.qhd-pre7-check/` so the warning delta is measured rather than assumed. All eight compiler/BibTeX invocations exited 0.
- Required final-log scan on the post-task build: `LaTeX Warning` 0; `undefined references` 0; `Citation .* undefined` 0; `Emergency stop` 0; `Fatal error` 0. The required zero-match set is preserved.
- Control build reproduced the G1 baseline exactly: 11 pages, 26 overfull, 18 underfull, 6 font warnings, 14 hyperref PDF-string warnings.
- Post-task build: **12 pages**, 28 overfull, 20 underfull, 6 font warnings, 16 hyperref PDF-string warnings. Attribution of every delta:
  - Page count 11 → 12. III-A grew from a compact problem statement into a full notation subsection, and the bibliography grew from 9 to 11 rendered entries because `maynardsmith1973` and `broom1997` are cited for the first time (`\bibitem` diff between the two builds shows exactly those two keys added).
  - Overfull 26 → 28: entirely the `505.12177pt ... while \output is active` class supplied by `ieeeaccess.cls`, 23 → 25 with the extra page. The two named body boxes are unchanged in count: 2 occurrences of `Overfull \hbox (9.2679pt too wide) in paragraph at lines 87--87` and 1 occurrence of `Overfull \hbox (32.93878pt too wide)` (line span moved 515--524 → 558--567 purely by the +43-line offset). **No new overfull box in III-A**; both new equations fit the column.
  - Underfull 18 → 20: output-routine occurrences 11 → 12 with the extra page, plus one new `Underfull \hbox (badness 3039) in paragraph at lines 35--40`. The log context shows this box is the `varsamis2025` bibliography entry (the line numbers index the `.bbl`), i.e. a bibliography line-break caused by the two added `\bibitem`s, not a III-A prose box. The seven pre-existing body/title underfull boxes are unchanged in badness and count.
  - Hyperref PDF-string warnings 14 → 16: the new subsection title contains `$N$`, which hyperref cannot put in a bookmark string. Cosmetic, class-level, and the same category already present 14 times.
- Rendered inspection: page 3 of the post-task build carries all of III-A. Eq. (1) and Eq. (2) sit inside the column with no overflow; every symbol on the page is defined before use; the subsection opens with the reader question and closes with the hand-off to equilibrium and welfare; paragraphs are 4 in number, all under the 180-word ceiling, none carrying more than two displayed equations, and each displayed equation is read back in plain language within the following sentence. Style rules 7.1--7.4 checked individually and satisfied.
- Rendered PDF preserved for the gate: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-7-g3-render.pdf`.
- Non-destructive artifact check: PASS. `paper/qhd.pdf` and root `qhd.pdf` remain byte-identical at SHA-256 `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`. Both temporary build directories were removed and verified absent.
- Carry-forward items for Task 8 (III-B), removed from III-A and not yet re-homed: the two-player payoff matrix table; the strict-dominance argument at $V{=}4,\ C{=}3$ ($V=4$ vs $V/2=2$ against Dove, $(V-C)/2=0.5$ vs $0$ against Hawk); "the unique classical pure Nash equilibrium is mutual Hawk, though mutual Dove is Pareto-superior"; and the scope note that the interior mixed equilibrium with Hawk probability $V/C$ needs $V<C$, whereas $V/C=4/3$ here lies outside the simplex. The Introduction (line 95) still says Hawk "strictly dominates Dove in the two-player payoff matrix", which III-B must support. `nash1951` and `dawes1980` are the audit-verified sources for that subsection.
- New warnings: three deltas, all attributed above; no new warning category. Approved exceptions: none. Nothing committed.
- Gate decision: **hard stop at Gate G3.** Style calibration on III-A and confirmation of the Task 6 evidence-label proposal are required before Task 8 (III-B) begins.

## 2026-08-01 - Gate G3 decision

- **G3 approved by the user on 2026-08-01.** Approval covers three things presented at the gate:
  1. **Style calibration.** III-A's voice, paragraph density, and depth are approved as drafted and are binding precedent for III-B through III-J: first-person plural, present tense for mathematics, one topic sentence per paragraph, a plain-language reading within one sentence of every displayed equation, an opening "why now" sentence, and a closing hand-off.
  2. **Evidence labels.** The Task 6 labeling stands exactly as written in `paper/CLAIM-SOURCE-MAP.md` after fix round 1. The Hawk-deviation closed form therefore remains a **computational result** over $N=2,\ldots,8$; it may be promoted to Proposition only if Task 13 (III-G) supplies the derivation in the manuscript, and until then no manuscript sentence may call it a proposition. The two split star rows keep their separate labels, and the $N=4,5$ tested range stands as corrected.
  3. **Open judgment calls.** Keeping `$V{=}4,\ C{=}3$` in III-A is approved explicitly. The dropped "Benjamin--Hayden tensor" attribution stays dropped. The 12-page count is accepted; no compression of III-A was requested.
- Consequence recorded for later tasks: the style rules above are no longer advisory for Section III; a violation in III-B through III-J is a review blocker under the same terms as the `paper/STYLE-GUIDE.md` rules themselves.

## 2026-08-01 - Task 8, rewrite III-B (Classical Equilibrium and Welfare Geometry)

- Branch: `dev`. Requirements source: plan Task 8; subsection definition from the spec §III-B.
- Pre-task `paper/qhd.tex` SHA-256: `38c9edbf1054563324b789e48727c71ea935224f79443bce336263f25a28f63f` (the post-Task-7, G3-approved state). Post-task SHA-256: `54a4c2b97de075f706e4ad6809319c6e49479c62107cab528bae595823e3d212`.
- Edit scope: the subsection immediately after III-A, `\subsection{$N$-Player Payoff Tensor}`, replaced by `\subsection{Classical Equilibrium and Welfare Geometry}` with new `\label{sec:classical-eq}`; plus one preamble addition, `\usepackage{amsthm}` and `\newtheorem{proposition}{Proposition}`, required by the plan's `proposition` environment and reused by the later III-F and III-G propositions. No other subsection, figure, table, or bibliography entry was edited; `paper/references.bib` was not modified, since `nash1951` and `dawes1980` already existed from Task 4.
- Step 1 (strict dominance): derived over the opponent-count parameter $m\in\{0,\ldots,N-1\}$ directly from the branches of Eq. (2), with the three comparisons $V$ vs $V/N$, $V/(m+1)>0$ vs $0$, and $(V-C)/N$ vs $0$. The subsection states plainly that the third comparison is strict exactly when $V>C$, so dominance is a property of the live parameters rather than of the Hawk--Dove structure.
- Step 2 (equilibrium and baseline): all-Hawk stated as the unique classical pure-strategy Nash equilibrium~\cite{nash1951}, paying $(V-C)/N=1/N$ per player at the live parameters, and named as the classical baseline for every advantage in the paper.
- Step 3 (welfare proposition): `Proposition 1 (Outcome-level welfare)` with Eq. (3), `\label{eq:outcome-welfare}`, and a proof that splits on $k(x)=0$, $0<k(x)<N$, and $k(x)=N$ separately, as the plan requires. This is the first proposition whose derivation exists in the manuscript, so its `Proposition` label in `paper/CLAIM-SOURCE-MAP.md` is now earned rather than proposed.
- Step 4 (mean identity): Eq. (4), `\label{eq:mean-welfare}`, deriving $\bar\pi = V/N - (C/N)\,p(1^N)$ by averaging the welfare identity over the outcome distribution $p$. $\bar\pi$ is introduced here as the mean over players; the per-player expected payoffs $(\pi_1,\ldots,\pi_N)$ remain reserved for the metrics subsection, consistent with the terminology decision recorded at Task 7.
- Step 5 (plain language): states that mean payoff depends on the distribution only through $p(1^N)$, that every other outcome redistributes the same total $V$, and that a protocol can raise mean welfare only by suppressing $p(1^N)$ — while possibly leaving players very unequally paid, which is the mean-versus-fairness gap Sec.~\ref{sec:sim} measures.
- Carry-forward items honoured from Task 7's list: the strict-dominance argument, the unique all-Hawk pure equilibrium, the Pareto comparison, and the $V/C$ mixed-equilibrium scope note are all re-homed here. The Introduction's phrase "strictly dominates Dove in the two-player payoff matrix" (line 95 pre-rewrite) is now supported: III-B gives the $N=2$ specialization of the tensor in prose ($V/2$ each under mutual Dove, $(V,0)$ under one-sided aggression, $(V-C)/2$ each under mutual Hawk).
- Deliberate deduplication, disclosed: the pre-rewrite `\begin{tabular}` $2\times2$ payoff matrix was not restored. It is the $N=2$ case of Eq. (2), so reprinting it would state the same rule twice; the specialization is given in prose instead. Reverting this is a one-paragraph change if the table is wanted back.
- Source-scope compliance: `maynardsmith1973` is cited only for the classical Hawk--Dove game as the origin of the interior mixed equilibrium, and the manuscript derives the $V/C$ condition from its own payoff structure rather than attributing an equilibrium value to that abstract-only source, as `paper/LITERATURE-AUDIT.md` requires. `dawes1980` carries only the social-dilemma definition. `nash1951` carries the pure-strategy equilibrium concept.
- New carry-forward for Task 12 (III-F), removed from the pre-rewrite subsection and not yet re-homed: "For the GHZ fixed profile $(Q_N,\dots,Q_N)$, the analytic GHZ cooperative outcome pays exactly $V/N$; its ideal analytic-baseline advantage is therefore $(V-1)/N=3/N$, a constant $3\times$ the classical payoff. This exact identity is scoped to that GHZ outcome; other topologies are evaluated cell by cell." The overstated "the payoff generalises as a Benjamin--Hayden tensor" attribution flagged at Task 7 was removed with that subsection and no longer appears anywhere in `paper/qhd.tex`.
- Step 6, focused tests, exact command and result: `conda run -n entangled-equilibria python -m pytest tests/test_paper_claims.py::test_total_welfare_identity_for_every_basis_state tests/test_paper_claims.py::test_hawk_strictly_dominates_dove_for_live_parameters tests/test_paper_claims.py::test_expected_mean_depends_only_on_all_hawk_probability -q` → `20 passed in 3.22s`.
- Step 7, build: non-destructive four-pass build in `paper/.qhd-build-check/`; all four invocations exited 0. Required final-log scan: `LaTeX Warning` 0; `undefined references` 0; `Citation .* undefined` 0; `Emergency stop` 0; `Fatal error` 0.
- Warning inventory after Task 8, against the post-Task-7 state (12 pages, 28 overfull, 20 underfull, 6 font, 16 hyperref):
  - Page count unchanged at **12**, despite III-B being substantially longer than the subsection it replaced and two further bibliography entries appearing (`\bibitem` count 11 → 13, adding `nash1951` and `dawes1980`).
  - Overfull unchanged at 28, with the identical three named body boxes (2 occurrences at `9.2679pt`, 1 at `32.93878pt`, line spans shifted by the edit offset) and 25 class-supplied output-routine boxes. **No new overfull box in III-B**; Eq. (3) and Eq. (4) and the proposition/proof block all fit the column.
  - Underfull unchanged at 20 (12 output-routine plus the same 8 body/title boxes, badnesses identical).
  - Hyperref PDF-string warnings 16 → **14**, back to the G1 baseline: III-A's new title added two, and retiring the `$N$-Player Payoff Tensor` title removed two.
  - Font warnings unchanged at 6.
- Rendered inspection: page 4 of the build carries the bulk of III-B. `Proposition 1 (Outcome-level welfare)` typesets correctly with the amsthm proof environment and QED box; both displayed equations sit inside the column; the subsection opens with the reader question and closes with a hand-off to the quantum construction; paragraph lengths and the one-plain-language-reading-per-equation rule are satisfied. Style rules 7.1--7.4 checked individually and satisfied under the G3-approved calibration.
- Rendered PDF preserved: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-8-render.pdf`.
- Non-destructive artifact check: PASS. `paper/qhd.pdf` and root `qhd.pdf` remain byte-identical at SHA-256 `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`. The temporary build directory was removed and verified absent.
- New warnings: none; the inventory improved by two hyperref lines and gained nothing. Approved exceptions: none. Nothing committed.
- Gate decision: Task 8 is a checkpoint, not a gate. Task 9 (III-C, Quantum Strategies and the EWL Protocol) may proceed. The next hard stop is Gate G4 at Task 13 (III-G, incentive compatibility).

## 2026-08-01 - Binding constraint: the old paper is a LaTeX scaffold, not a content source

- User instruction, 2026-08-01: "the older paper is not to be used for anything except its tex for base, that paper contains many errors and if it was not for the tex base i would have deleted it, please dont refer that."
- Binding interpretation for all remaining tasks: the pre-rewrite manuscript (`paper/main.tex`, the Phase-1 source snapshots, and any pre-rewrite subsection still standing in `paper/qhd.tex`) may supply build shell, float and table markup, and structural skeleton only. Its prose, numbers, equations, attributions, and framing may not be inherited. Every statement entering a rewritten subsection must be derived in the new manuscript, taken from the spec or the task brief, or backed by a passing regression check. The superseded `docs/superpowers/plans/2026-07-28-qhd-paper-redesign.md` is likewise out of scope and is not to be consulted or reconciled against.
- Effect on the carry-forward mechanism: carry-forward notes in this log are **re-derivation to-do lists, not text to paste**. The Task 12 (III-F) entry is restated on those terms below.
- Audit of the two already-drafted subsections against this rule:
  - III-A opening sentence, notation, payoff tensor, and $N=4$ examples — from the task brief and the spec, or derived here. Compliant. Payoff tensor covered by `test_payoff_tensor_matches_piecewise_formula_exhaustively` (6 passed).
  - `$V{=}4,\ C{=}3$` and the `src/config.py` provenance — verified directly against `src/config.py:35--36` (`V: float = 4.0`, `C: float = 3.0`), not taken on trust from the old prose. Compliant.
  - III-B strict dominance, unique all-Hawk equilibrium, $N=2$ specialization, `Proposition 1`, and the mean identity — all derived here from Eq. (2) and covered by the three focused tests (20 passed). The $V/C$ mixed-equilibrium condition was re-derived independently at $N=2$ (indifference gives $V-pC=0$, hence $p=V/C$) rather than inherited as an assertion. Compliant.
  - **One violation found and fixed.** III-A had inherited the old paper's instrument-level analogy, "Hawk is the aggressive position, a short ...; Dove is the cooperative position, a long ...". No source, no test, and not in the spec, which sanctions only "Hawk--Dove as a model of aggressive versus cooperative trading behavior" (spec §I-A) and requires market framings to be presented as interpretations rather than demonstrated deployments (spec §VII-E). The sentence now reads "Hawk is the aggressive action: it takes the whole contested value when unopposed, but destroys value when it meets itself. Dove is the cooperative action, which shares value reliably", and "contested asset" became "contested resource". Any instrument-level market mapping the paper wants belongs in Section I or VII as an explicit interpretation, not asserted as a definition in III-A.
- Revised carry-forward for Task 12 (III-F), stated as claims to re-derive rather than text to reuse: the GHZ fixed profile $(Q_N,\ldots,Q_N)$ pays $V/N$ per player, giving an analytic-baseline advantage of $C/N=3/N$ over the classical $1/N$; and that identity is scoped to the GHZ cooperative outcome, with other entangler families evaluated case by case. Both are already covered by `tests/test_paper_claims.py::test_ghz_q_profile_payoff_and_analytic_advantage`; III-F must derive them, not quote them.
- Post-correction build: four-pass, all exits 0. Required final-log scan unchanged at zero for `LaTeX Warning`, `undefined references`, `Citation .* undefined`, `Emergency stop`, and `Fatal error`. 12 pages; 28 overfull; 20 underfull; 6 font warnings; 14 hyperref PDF-string warnings — identical to the post-Task-8 inventory. `paper/qhd.tex` SHA-256 is now `41c08af42fad11e0b1fa21998fcc11572c60a7fbf22ce71dfba1c4edccfbc157`. Temporary build directory removed and verified absent. Nothing committed.

## 2026-08-01 - Task 9, rewrite III-C (Quantum Strategies and the EWL Protocol)

- Branch: `dev`. Requirements source: plan Task 9; subsection definition from spec §III-C.
- Pre-task `paper/qhd.tex` SHA-256: `41c08af42fad11e0b1fa21998fcc11572c60a7fbf22ce71dfba1c4edccfbc157`. Post-task SHA-256: `dad210259b81d14af1afec294eeb183f4f3bd589383a69912baf5e1d24689786`.
- Edit scope: `\subsection{EWL Quantization and $N$-Player Strategies}` and its two `\subsubsection` blocks replaced by `\subsection{Quantum Strategies and the EWL Protocol}` with new `\label{sec:ewl}`. No other subsection edited; `paper/references.bib` unchanged (all cited keys already present from Task 4).
- **Step 6 was run before drafting, not after.** Every definition that entered the subsection was first checked against `src/circuits/ewl.py` and `src/circuits/topologies.py`, so no formula was written from memory of the old manuscript:
  - printed matrix $U(\theta,\alpha,\beta)$ vs `circuits.ewl.U` — agreement to `1e-12` over 200 random parameter triples;
  - `DOVE == (0,0,0)` and `HAWK == (pi,0,0)`; $U(0,0,0)=I$; $U(\pi,0,0)=i\sigma_x$ exactly;
  - `q_strategy(N) == (0, pi/N, pi/N)` and $U(0,\pi/N,\pi/N)=\mathrm{diag}(e^{i\pi/N},e^{-i\pi/N})$ for $N=2,3,4$;
  - $J_T(0)=I$ for all five entangler families at $N=3,4,5$ — checked because the manuscript asserts that $\gamma=0$ recovers the classical game, which is a claim about every family, not just GHZ.
- Scope extension, disclosed: those checks were then promoted from throwaway scripts into four permanent guards appended to `tests/test_paper_claims.py`. The plan's Task 9 file list did not include the test file, but the binding rule of 2026-08-01 requires every manuscript statement to be derived, spec-sourced, or test-backed, and an ephemeral script satisfies none of those durably. Full suite after the addition: `conda run -n entangled-equilibria python -m pytest tests/test_paper_claims.py -q` → **128 passed in 3.48s** (104 pre-existing plus 24 new cases).
- Step 1 (protocol preview): three sentences — entangle the register, act locally and privately, undo the entangler and measure — plus the explicit statement that no signal passes between players during play. A `% FIGURE F1 ANCHOR` comment marks the schematic's future position; no figure was created, per the deferred-figure constraint.
- Steps 2--4: Eq. (5) `eq:strategy-unitary`; Eq. (6) `eq:named-strategies`; Eq. (7) `eq:ewl-state`; Eq. (8) `eq:outcome-prob`. The output-state equation is written with the family-indexed entangler $J_T(\gamma)$ rather than the GHZ-specific $J=e^{i\gamma X^{\otimes N}/2}$ the old text used, so III-D can define the five families without restating the protocol. The measured bitstring is tied back to the $x_j$ convention of III-A explicitly.
- Step 3 wording: $Q_N$ is stated as GHZ-derived and held fixed across entangler families, and the old universality implication is closed off — the familiar $Q=U(0,\pi/2,\pi/2)$ is named as the $N=2$ case of that family, not a universal quantum strategy.
- Step 5 (scope): states that players physically hold all of SU(2) while the equilibrium tests enumerate only $\{D,H,Q_N\}$, cites `benjamin2001comment` for the result that widening the deviation space to full SU(2) removes the EWL equilibrium, and commits the paper to the canonical term "restricted-menu equilibrium". `marinatto2000quantum` is cited once as a scope limiter for the alternative two-player-only quantization, within the audit's contextual-only restriction.
- Attribution correction (third of its kind): the pre-rewrite line credited `benjamin2001` jointly with `chappell2012` for "maximal entanglement at $\gamma=\pi/2$". The audit records that neither the symbol $\gamma$ nor the value $\pi/2$ appears in `benjamin2001`. The angle parameterization is now attributed to `chappell2012` alone, with the $\theta\leftrightarrow\gamma$ symbol translation stated in the text as the audit recommended.
- Carry-forward to Task 12 (III-F), to be re-derived rather than reused: the pre-rewrite claim that at $\gamma=\pi/2$ the profile $(Q_N,\ldots,Q_N)$ returns $\ket{0^N}$ exactly, and that this single-outcome structure is what makes the mean-payoff observable first-order insensitive to single bit-flips. Both are already covered by existing tests.
- Flagged for Task 10 (III-D), found while verifying: `w_entangler` in `src/circuits/topologies.py` carries an in-code note that "the gamma-interpolation semantics for the W entangler are a design choice (the $\ket{0\ldots0}\leftrightarrow\ket{W}$ reflection); confirm against the intended physics before publishing". III-D must either justify that choice in the manuscript or scope the W results to the stated construction. III-C makes no W-specific claim beyond $J_W(0)=I$, which is verified.
- Build defects found and fixed during Step 7, both introduced by this task:
  1. `Overfull \hbox (30.67943pt too wide) detected at line 409` — the three named strategies on one display line exceed the TQE column. Rewritten as a two-line `gathered` display; the box is gone.
  2. `\mathbb{1}` for the identity rendered as a broken glyph (amssymb's `\mathbb` covers uppercase letters only). Replaced with $I$, spelled out as "the identity on all $N$ qubits" on first use. No symbol collision: $I$ is not otherwise used as a symbol in the manuscript.
- Final build: four passes, all exits 0. Required final-log scan: `LaTeX Warning` 0; `undefined references` 0; `Citation .* undefined` 0; `Emergency stop` 0; `Fatal error` 0.
- Warning inventory against the post-Task-8 state (12 pages, 28 overfull, 20 underfull, 6 font, 14 hyperref): now **13 pages**, 30 overfull, 21 underfull, 6 font, **12 hyperref**. Attribution: the page increase reflects a substantially longer subsection plus two newly cited bibliography entries (`\bibitem` count 13 → 15, adding `benjamin2001comment` and `marinatto2000quantum`); overfull 28 → 30 and underfull 20 → 21 are entirely class-supplied output-routine boxes tracking the extra page, with the body boxes unchanged at the same three overfull and eight underfull entries; hyperref warnings *fell* by two because the retired subsection title contained `$N$` and the new one does not.
- Rendered inspection: pages 4 and 5 carry III-C. Eq. (5)'s $2\times2$ matrix fits the column, Eq. (6) fits after the `gathered` fix, and Eqs. (7)--(8) fit. Subsection opens with the reader question and closes with the hand-off to the entangler families. Style rules 7.1--7.4 satisfied under the G3-approved calibration. Render preserved: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-9-render.pdf`.
- **Process incident, disclosed.** One build attempt used `rm -rf .qhd-build-check && mkdir ... && cd ... && pdflatex ...`. The `rm` failed with "Device or resource busy" (a Windows handle on the directory), which short-circuited the `&&` chain, so the `cd` never happened and the subsequent `bibtex`/`pdflatex` commands — chained with `;` rather than `&&` — executed in `paper/` itself. That overwrote the protected artifact `paper/qhd.pdf` and left `qhd.aux`, `qhd.log`, `qhd.out`, and three redirect files in `paper/`. Detected by the standing post-build SHA-256 check, which reported `a52fee77...` instead of the expected `c7e77e3a...`. Recovery: `paper/qhd.pdf` was restored byte-identically from the untouched root `qhd.pdf` (both now `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`), and every stray file was removed. `paper/qhd.tex`, `paper/references.bib`, and `paper/figs/` were never written to. The pre-existing `paper/main.*` build artifacts predate this session and were not touched.
- Control adopted for every later build: the build script now runs `cd` and `mkdir` as separate guarded steps and aborts unless `pwd` ends in `.qhd-build-check` before any LaTeX command runs, so a failed cleanup can no longer cause a build in the manuscript directory.
- Non-destructive artifact check after recovery: PASS. `paper/qhd.pdf` and root `qhd.pdf` byte-identical at `c7e77e3a...`; temporary build directory removed and verified absent.
- New warnings: none beyond the page-tracking output-routine boxes; the two defects this task introduced were both fixed before the final build. Approved exceptions: none. Nothing committed.
- Gate decision: Task 9 is a checkpoint. Task 10 (III-D, Entangler Families and Graph Symmetry) may proceed, carrying the W-entangler interpolation question above. Next hard stop remains Gate G4 at Task 13.

## 2026-08-01 - Task 10, rewrite III-D (Entangler Families and Graph Symmetry)

- Branch: `dev`. Requirements source: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-10-brief.md`; subsection definition from spec §III-D and the binding two-level vocabulary of spec §3.2.
- Pre-task `paper/qhd.tex` SHA-256: `dad210259b81d14af1afec294eeb183f4f3bd589383a69912baf5e1d24689786` (the post-Task-9 state). Post-task SHA-256: `2a770869e78660b981dedad45df534a0556861975063f8affc1496b4ca1ec41d`.
- Edit scope: `\subsection{Entanglement Topologies}` and its two `\subsubsection` blocks (`Topology definitions`, `Gate-native realisation`) replaced by `\subsection{Entangler Families and Graph Symmetry}` with new `\label{sec:families}`. No other subsection, float, table, preamble line, or bibliography entry was edited. `paper/references.bib` unchanged: both newly cited keys (`duer2000three`, `hein2004multiparty`) already existed from Task 4.

### Verification against `src/` ran BEFORE any prose was drafted

Two throwaway scripts were run in the `entangled-equilibria` environment before the first sentence was written: 280 assertions in the first and 44 in the second, all PASS. Everything the subsection prints was checked against `src/circuits/topologies.py` and `src/circuits/topology_graphs.py` first.

- **GHZ operator.** `ghz_entangler(N, gamma)` equals `cos(gamma/2) I^{ox N} + i sin(gamma/2) X^{ox N}` for $N=2,\ldots,6$ at $\gamma\in\{0,0.3,\pi/4,\pi/2,1.9\}$, with $X^{\otimes N}$ rebuilt as an independent Kronecker product rather than reusing the implementation's `np.fliplr` shortcut.
- **Pairwise operator and sign convention.** `ring_entangler`, `star_entangler`, `fully_connected_entangler` equal $\prod_{(r,s)\in E}\exp(+i\tfrac{\gamma}{2}X_rX_s)$ computed with `scipy.linalg.expm` — a genuine matrix exponential, not the implementation's own `cos I + i sin XX` closed form. The $-i$ convention was checked to disagree, confirming the module docstring's "NOT Qiskit RXXGate" claim independently.
- **Edge sets and hub convention.** `topology_graph("ring", N)` is exactly $\{(j,j{+}1 \bmod N)\}$ with $|E|=N$; `topology_graph("star", N)` is exactly $\{(0,j)\}$ with hub qubit $0$ and $|E|=N-1$; `topology_graph("fully-connected", N)` is all $\binom{N}{2}$ pairs. Checked for $N=3,\ldots,7$. `ghz` and `w` return `kind == "global"` with zero edges, which is the code-level fact behind the manuscript's two-level vocabulary.
- **W operator.** $S_W=I-\ket{0^N}\bra{0^N}-\ket{W}\bra{W}+\ket{0^N}\bra{W}+\ket{W}\bra{0^N}$ is Hermitian with $S_W^2=I$, and `w_entangler` equals both $\cos(\gamma/2)I+i\sin(\gamma/2)S_W$ and $\exp(i\gamma S_W/2)$, for $N=2,\ldots,6$ over the same $\gamma$ grid.
- **Degeneracies.** $C_3=K_3$ at every tested $\gamma$; all three graph topologies coincide at $N=2$.
- **Permutation covariance.** $R_\sigma J_GR_\sigma^{\dagger}=J_{\sigma(G)}$ for random $\sigma$ at $N=3,4,5$ on all three graphs, including the star hub relocation $\sigma=(0\,1)$, whose relabelled edge set was confirmed to be $\{(0,1),(1,2),(1,3)\}$ — the star with the hub moved to vertex 1.
- **Global invariance.** $R_\sigma J_{\mathrm{GHZ}}R_\sigma^{\dagger}=J_{\mathrm{GHZ}}$ and $R_\sigma J_WR_\sigma^{\dagger}=J_W$ for random $\sigma$ at $N=3,4,5$.
- **Payoff-level covariance (the proposition).** $\pi_{\sigma(j)}(\sigma(G))=\pi_j(G)$ verified end-to-end through `build_ewl_circuit` + `expected_payoff` at $\gamma=\pi/2$, $V{=}4,C{=}3$. Automorphism orbits were computed by brute force and matched to payoff vectors: ring and complete are vertex-transitive (one orbit, all payoffs equal — e.g. ring $N=5$ gives $[0.8]\times5$); star has orbits $\{0\}$ and $\{1,\ldots,N-1\}$ with hub $\neq$ leaf at $N=4,5,6$ (star $N=4$: $(0.25,1.25,1.25,1.25)$, which is the $[0,1,1,1]$ advantage split of `tests/test_asymmetric_advantage.py` shifted by the classical baseline $1/N=0.25$).
- **Normalization: confirmed absent from the code before writing the convention.** A repository-wide grep over `src/` for `normali[sz]`, `per-edge`/`per_edge`, `scale.*gamma`, `/ len(edges)`, and `number_of_edges` returns only unrelated hits (`src/experiment/config.py` sweep-axis normalization, `src/experiment/topology_registry.py` alias normalization, `src/game/payoffs.py` probability normalization). `src/circuits/gate_level.py` appends one `RXXGate(-gamma)` per edge at the raw angle and `src/experiment/topology_registry.py` hands every family the same `gamma`. The manuscript therefore presents Eq. (13) as a forward-looking definition, states plainly that every number in the paper uses the unnormalized equal-$\gamma$ setting, and says the sensitivity control is not among the results reported. The gap is recorded in `paper/CLAIM-SOURCE-MAP.md`.

### What was written, and why each statement is admissible

- Step 1 (two-level vocabulary): five entangler families named; ring/star/complete identified as graph topologies with an edge set; GHZ and W identified as global constructions with none, so hub/leaf/orbit language is declared undefined for them. Sourced from spec §3.2 (binding) and verified against `topology_graphs.py`'s `kind` field. A `% FIGURE F2 ANCHOR` comment marks the gallery's future position; no figure was created.
- Step 2: Eq. (9) `eq:ghz-entangler`, transcribed verbatim from the brief and verified above. Plain-language reading: $X^{\otimes N}$ couples each outcome only to its bitwise complement, hence all-Dove to all-Hawk. `benjamin2001` is cited for the maximally entangled member $(I^{\otimes N}+iX^{\otimes N})/\sqrt2$ only — exactly the entangling gate the audit locates near that paper's Fig. 1(b) — and the interpolation is presented as this paper's own, respecting the audit's note that no $\gamma$ symbol or $\pi/2$ value appears in `benjamin2001`.
- Step 3: Eq. (10) `eq:graph-entangler`, verbatim from the brief; commutativity of the $X_rX_s$ factors stated (and used) as the reason the product is order-independent; edge sets and $m_G$ given inline to hold the display count down; the $N=2$ and $C_3=K_3$ degeneracies stated with the explicit consequence that ring-versus-complete claims are $N\ge4$ claims.
- Index-convention note added deliberately: the manuscript indexes players $1,\ldots,N$ (III-A) while the implementation indexes qubits from zero and pins the hub at qubit $0$. III-D states the translation once rather than letting the two conventions collide silently.
- Step 4: Eq. (11) `eq:w-involution` and Eq. (12) `eq:w-entangler`. The in-code warning flagged by Task 9 is handled in the open, not buried: the subsection states that the interpolation is a construction chosen here, that the endpoint $\ket{W}$ is fixed by the family's name but the path to it is not, that any Hermitian involution carrying $\ket{0^N}$ to $\ket{W}$ gives the same two endpoints and a different interior, that the reflection was adopted to put W and GHZ on identical algebraic footing, and that **every W result in this paper is a statement about this construction, not about W-type entanglement in general**.
- Step 5: Eq. (13) `eq:normalized-entangler`, plus the two limits of the convention (it equalizes total rotation angle, not entangling power or gate count; it leaves the global families untouched since $m=1$) and the explicit statement that no result here is computed under it.
- Step 6: $R_\sigma$ defined by $R_\sigma X_rR_\sigma^{\dagger}=X_{\sigma(r)}$ and $R_\sigma\ket{x}=\ket{\sigma(x)}$; Eq. (14) `eq:graph-covariance` derived factor by factor; the global families given as the degenerate case with the full symmetric group as symmetry group.
- Step 7: `Proposition 2 (Relabeling covariance of payoffs)`, Eq. (15) `eq:payoff-covariance`, with a proof composing three facts ($R_\sigma\ket{0^N}=\ket{0^N}$; the symmetric strategy layer commutes with $R_\sigma$; Eq. (14)) into $\ket{\psi_{\mathrm{out}}(\sigma(G))}=R_\sigma\ket{\psi_{\mathrm{out}}(G)}$, then using the fact that the payoff tensor depends on an outcome only through $(k(x),x_j)$. The orbit corollary is the case $\sigma(G)=G$, stated inside the proposition so no new theorem environment was needed. The noise clause is a hypothesis ("a channel that commutes with $R_\sigma$"), not an assertion about the device.
- $\pi_j=\sum_xp(x)P_j(x)$ is introduced here with an explicit forward pointer to the metrics subsection, following the precedent set when III-B introduced $\bar\pi$ ahead of III-E. No `\ref` is used for that pointer because `sec:metrics` does not exist yet; Task 17's flow pass wires it.
- Step 9 ordering: the families are defined in full before any cost statement appears. One verified cost sentence survives — because each edge is one two-qubit rotation, $m_G$ is the graph entangler's pre-routing two-qubit gate count — and the executed counts are deferred to Sec.~\ref{sec:hardware}.
- Citations, all within their `paper/LITERATURE-AUDIT.md` scope limits: `duer2000three` for the three-qubit SLOCC-inequivalence of GHZ and W (scoped explicitly to three qubits, which is what that paper proves); `chappell2012` for GHZ-type versus W-type comparison in $N$-player quantum games being an established question; `benjamin2001` as above; `hein2004multiparty` for the practice of reading structural symmetry off a graph and keeping it distinct from the equivalences of the state the graph defines. `hansenne2022symmetries` was **deliberately not cited**: the audit flags it for this strand, but its located claim is a network-generation no-go theorem that III-D makes no use of, and a decorative citation would violate the one-claim-per-paragraph rule.

### Inherited from the replaced prose

Nothing. The replaced `Topology definitions` and `Gate-native realisation` blocks contributed no sentence, number, attribution, or framing. Two specific things were dropped rather than carried:

1. The market analogies ("GHZ = centralised order book" and the rest) and their `Sec.~\ref{sec:archinterp}` pointer. The spec requires market framings to be presented as interpretations rather than definitions, and III-D is a definitions subsection. `\label{sec:archinterp}` still exists and is unaffected; an unreferenced label produces no warning.
2. The gate-native realisation claims: the pinned $\{u,cx\}$ basis, "$2(N{-}1)$ CX per $J$" for GHZ, the W prep-conjugated construction, "one $R_{XX}(-\gamma)$ per edge", and the `Table~\ref{tab:topology}` pointer. `Table~\ref{tab:topology}` is still referenced from Sec.~\ref{sec:hwtopology}, so removing this pointer created no undefined reference. Only the one gate-cost statement re-verified against `src/circuits/gate_level.py` (one two-qubit rotation per edge, hence $m_G$ before routing) was kept.

### Tests

- Scope decision: seven guards were appended to `tests/test_paper_claims.py` under a `III-D` heading, each guarding a printed equation or edge set that nothing previously covered. Unitarity, the $N=2$ single-edge reduction, $C_3=K_3$, and $J_T(0)=I$ were **reused by node ID, not duplicated**; the node IDs are recorded in `paper/CLAIM-SOURCE-MAP.md`.
- `conda run -n entangled-equilibria python -m pytest tests/test_topologies.py tests/test_paper_claims.py -q` -> **206 passed in 5.88s** (138 pre-existing: 128 in `test_paper_claims.py` after Task 9 plus 10 in `test_topologies.py`; **68 new cases** from the seven added guards). Split runs confirm the arithmetic: `tests/test_topologies.py` alone -> `10 passed in 2.36s`; `tests/test_paper_claims.py` alone -> `196 passed in 4.78s`; the seven new guards selected alone -> `68 passed, 128 deselected in 9.27s`.
- The brief's literal command, `pytest tests/test_topologies.py tests/test_paper_claims.py -k "orbit or covariance" -v`, selects only **1 passed, 205 deselected** — the new guards are named `..._covariant` / `..._covariance_...`, which the substring `covariance` does not match. Recorded so the discrepancy is not read as missing coverage. The corrected filter `-k "orbit or covarian or leaf_swap"` gives **20 passed, 186 deselected**.
- Reused node IDs re-run explicitly: `tests/test_topologies.py::test_pairwise_unitary`, `::test_ghz_n2_is_unitary`, `::test_ghz_n3_is_unitary`, `::test_w_unitary`, `::test_ring_equals_fully_connected_n3`, `::test_pairwise_n2_matches_j_matrix`, and `tests/test_asymmetric_advantage.py::test_star_leaves_share_one_advantage` -> **9 passed in 2.80s**.
- Structure guards: `conda run -n entangled-equilibria python -m pytest tests/test_paper_structure.py -q` -> **4 passed in 0.05s**. The hype-adjective, restricted-equilibrium, target-state-name, and state-fidelity guards all pass against the new prose.
- Two new third-party imports appear in `tests/test_paper_claims.py`: `networkx` and `scipy.linalg.expm`. Both are pinned first-order dependencies in `pyproject.toml` (`networkx==3.3`, `scipy==1.13.1`), so no dependency was added.

### Build

- Non-destructive four-pass build in a fresh `paper/.qhd-build-check/` populated by copying `qhd.tex`, `references.bib`, `ieeeaccess.cls`, `bullet.png`, `logo.png`, `notaglinelogo.png`, and `figs/`. The Task 9 control was enforced: the script aborts unless `pwd` ends in `.qhd-build-check`, and re-checks that guard before each of `bibtex`, pass 2, and pass 3. Guard line printed `GUARD OK: /c/Users/prith/Multiplayer-QHD-Game/paper/.qhd-build-check`.
- Exit codes: `pass1_exit=0`, `bibtex_exit=0`, `pass2_exit=0`, `pass3_exit=0`.
- Required final-log scan: `LaTeX Warning` 0; `undefined references` 0; `Citation .* undefined` 0; `Emergency stop` 0; `Fatal error` 0.
- Warning inventory against the post-Task-9 baseline (13 pages, 30 overfull, 21 underfull, 6 font, 12 hyperref): now **14 pages, 32 overfull, 22 underfull, 6 font, 12 hyperref**. Attribution of every delta:
  - Page count 13 -> 14. III-D is substantially longer than the two `\subsubsection` blocks it replaces (a proposition with proof, five displayed definitions, and the normalization disclosure), and the bibliography grew from 15 to 17 rendered entries because `duer2000three` and `hein2004multiparty` are cited for the first time (`\bibitem` diff shows exactly those two keys added).
  - Overfull 30 -> 32: entirely the class-supplied `Overfull \hbox (505.12177pt too wide) ... while \output is active` category, 27 -> 29 with the extra page. The three named body boxes are unchanged in count and size: 2 occurrences at `9.2679pt` (line 89, the title block) and 1 at `32.93878pt` (the pre-existing Sec.~V wiring-permutation paragraph, now at lines 886--895 purely by edit offset). **No new body overfull box**; all five displayed definitions, both covariance equations, and the proposition block fit the TQE column.
  - Underfull 21 -> 22: output-routine occurrences 13 -> 14 with the extra page; the 8 body/title boxes are unchanged in badness (5592, 5316 in the abstract/title block; 3039 in the `.bbl`; 2409, 2302, 1668, 1377, 1371 in Secs.~II, V and VI). **No new underfull box in III-D.**
  - Font warnings unchanged at 6; hyperref `Token not allowed in a PDF string` unchanged at 12, since neither the retired title nor the new one contains math.
- `Output written on qhd.pdf (14 pages, 700552 bytes).`
- Rendered inspection: pages 5 and 6 carry III-D. Eq. (9) through Eq. (15) all sit inside the column; `Proposition 2` numbers correctly after III-B's `Proposition 1` and typesets with the amsthm proof environment and QED box; the subsection opens with the reader question ("the output state is only as specific as the entangler inside it") and closes with the hand-off to the metrics subsection. Style rules 7.1--7.4 checked individually: first-person plural throughout, present tense for the mathematics, no hype adjectives, one topic sentence per paragraph, every paragraph under the 180-word ceiling, no paragraph carrying more than two displays, every display read back in plain language within the following sentence, and every cross-reference semantic. Terminology frozen in `paper/CLAIM-SOURCE-MAP.md` is respected: "entangler family" for all five-way statements, "graph topology" only for ring/star/complete, and $\gamma$ used for nothing but the entanglement angle.
- Render preserved: `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-10-render.pdf`.
- Defect found and fixed during the build round: in the proof, the inline `\bigotimes_{j}U` set its limits below the operator and crowded the line. Changed to `\bigotimes\nolimits_{j}U` and rebuilt; the final inventory above is from the rebuilt document. No overfull or underfull box was introduced at any point in this task, so no equation had to be restructured — the Task 9 `gathered` lesson was applied pre-emptively by keeping the edge sets and $m_G$ values inline rather than in a three-line display, and the `\mathbb{1}` lesson by using $I$ for the identity throughout.
- Non-destructive artifact check: PASS both before and after the build. `paper/qhd.pdf` and root `qhd.pdf` are byte-identical at SHA-256 `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`. The temporary build directory was removed and verified absent (`CLEANUP_PASS: paper/.qhd-build-check removed`).

### Carry-forward

- **III-E (metrics).** III-D uses $\pi_j=\sum_xp(x)P_j(x)$ with a prose forward pointer and no `\ref`. III-E must define the payoff vector formally and Task 17 must convert the pointer to a semantic `\ref`.
- **III-H / Section V (gate-native realisation).** The removed subsubsection's content — the pinned $\{u,cx\}$ basis, GHZ as a Hadamard-conjugated CNOT-ladder parity rotation, the W prep-conjugated construction, one $R_{XX}(-\gamma)$ per edge, and the two-qubit budget argument — is not re-homed anywhere yet. It must be re-derived against `src/circuits/gate_level.py` before it re-enters the manuscript; the CX counts in particular were never verified and must not be pasted back.
- **Section V (normalization).** Eq. (13) is defined but unimplemented. Section V must either report the sensitivity control under it or state that it did not, matching III-D's wording. It must not imply the control was run.
- **Section V (player indexing).** Sec.~V currently labels the star hub "player 0" (the figure caption in the star-symmetry subsection), while III-A/III-D index players from 1. The rewrite of Section V must reconcile this; III-D states the qubit-to-player translation explicitly so the fix is mechanical.
- **Section V (an empirical confirmation of Proposition 2 already in the manuscript).** The pre-rewrite Sec.~V paragraph on the wiring-permutation test reports that cyclically shifting the qubit-to-player wiring on the ring at $N=5$ permutes the whole per-player payoff vector rigidly to $\sim10^{-16}$. That is exactly Eq. (15) measured under the noisy path. Whoever rewrites Sec.~V should tie it back to `Proposition 2` explicitly instead of presenting it as an isolated diagnostic — after re-verifying the number, since it is pre-rewrite prose.
- **Market analogies.** The five per-family market analogies removed from III-D belong in Sec.~I or the architectural-interpretation subsection as explicit interpretations, per spec §VII-E. They currently survive only in `Sec.~\ref{sec:archinterp}`.
- **`hansenne2022symmetries`.** Verified in the audit, deliberately uncited so far. If a later fairness subsection needs a permutation-symmetry source with operational teeth, it is available within its located scope (network-generation no-go theorem).
- New warnings: none beyond the two output-routine overfull boxes and one output-routine underfull box that track the added page, all attributed above. Approved exceptions: none. Nothing committed; `git add`, `git commit`, and `git stash` were not run.
- Gate decision: Task 10 is a checkpoint, not a gate. Task 11 (III-E, Expected Payoff, Advantage, Equilibrium, and Fairness) may proceed. The next hard stop remains Gate G4 at Task 13 (III-G).

## 2026-08-01 - Task 10 independent review, fix rounds, and checkpoint closure

- This entry supersedes the former Task 10 checkpoint state "IMPLEMENTED BY SUBAGENT, REVIEW NOT YET RUN" without deleting that historical record.
- Independent review verdict: spec issues were found initially and task quality needed fixes. There were no Critical findings; the review reported five Important findings and one Minor wording finding.
- Fix round 1 addressed all six findings: the $N=2$ cycle edge-count scope and regression test; W live-angle and interpolation wording; demotion of four operator/identity evidence rows; the star hub/leaf overstatement; selection by the literal `orbit or covariance` test filter; and the scope of the manuscript normalization statement. Re-review found one remaining mismatch in the claim-map normalization wording.
- Fix round 2 narrowed `paper/CLAIM-SOURCE-MAP.md` to state that "every reported entangler-family comparison" uses the unnormalized equal-$\gamma$ setting. The focused text check passed, `tests/test_paper_structure.py` passed all 4 tests, and final re-review was clean with no new breakage.
- Final evidence-label ruling:
  - **Computational result:** GHZ implementation identity; graph product/sign identity; edge-set/count identity; W involution/operator identity.
  - **Proposition:** graph permutation covariance; GHZ/W full permutation invariance; payoff covariance.
- TDD evidence for the $N=2$ cycle correction: the new regression was RED against the unscoped manuscript statement and GREEN after the scope correction.
- Final test evidence: the literal orbit/covariance gate passed **19** tests with **188 deselected**; the focused amended rows passed **69** tests; the full paper-claims/topologies run passed **207** tests; and the structure suite passed **4** tests.
- Final build evidence: the guarded four-pass build exited 0, produced **14 pages**, and had zero undefined-citation, undefined-reference, emergency, or fatal diagnostics. Protected `paper/qhd.pdf` and root `qhd.pdf` remained byte-identical at SHA-256 `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`.
- Binding Section V requirement: interaction-strength normalization remains unimplemented and the normalized sensitivity control remains unrun. Neither may be described as completed; Section V must report the control if it is later run or state accurately that it was not.
- W-interpolation ruling: the manuscript continues to identify the interpolation as this study's chosen construction, not a unique W entangler. Task 10 review accepts that explicit disclosure as compliant and makes no uniqueness claim.
- Closure: Task 10 is complete in uncommitted working-tree changes with a clean review. This checkpoint approves no gate, attributes no new gate or scientific decision to the user, and records no user approval.
- Next action: Task 11, rewrite III-E metrics. The next hard stop remains Gate G4 after Task 13.

## 2026-08-02 - Task 11 implementation checkpoint: III-E metric contracts

- Status: **implemented, awaiting independent review**. This checkpoint records
  implementation and verification only; it does not claim Task 11 completion,
  independent approval, or a gate decision.
- Requirements source:
  `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-11-brief.md`.
- Exact pre-task snapshots were created with fail-if-present guards before any
  edit:
  - `task-11-pre-qhd.tex` — SHA-256
    `e160be3062723b31fded280aac6a5699e3a372cbe56b4bc3fd960a0efa689da4`
  - `task-11-pre-claim-source-map.md` — SHA-256
    `2ccb011ae929fb54cfbc1d8d53e41b8cad6076f9e44a4cb4fde0a1816e0864ac`
  - `task-11-pre-section-execution-log.md` — SHA-256
    `29e2b51863dc8a77c63a9fe9e1fdf25ce61285dd7c93cb4aea1fdca7bd713156`
  - `task-11-pre-test_paper_structure.py` — SHA-256
    `da50b4db15c16c303758d89fe569af42529ef186c1fa81f8afdc03d2857383d2`
- Manuscript scope: the old `Payoff-Gap Metrics and Honesty Conventions`
  scaffold was replaced by `Expected Payoff, Advantage, Equilibrium, and
  Fairness`, `\label{sec:metrics}`. No old prose, numerical result, citation,
  attribution, or framing was retained.
- Definitions inserted:
  - expected player payoff and full payoff vector,
    $\pi_j(\boldsymbol U;T)=\sum_xp_T(x\mid\boldsymbol U)P_j(x)$ and
    $\boldsymbol\pi=(\pi_1,\ldots,\pi_N)$;
  - mean payoff $\bar\pi(\boldsymbol U;T)=N^{-1}\sum_j\pi_j(\boldsymbol U;T)$,
    explicitly tied to the earlier welfare identity;
  - unilateral-deviation gaps
    $g_j(a)=\pi_j(Q_N^{\otimes N})-\pi_j(a,Q_{N,-j})$ for
    $a\in\{D,H\}$, with the pass rule requiring both deviations for every
    player under a fixed family/path;
  - analytic-baseline advantage
    $\Delta_{\mathrm{ana}}=\bar\pi-(V-C)/N$ and circuit-relative payoff gap
    $\Delta_{\mathrm{circ}}$, with separate symbols, equations, and a two-row
    comparator table;
  - all-zero target-state population
    $P(0^N)=p_T(0^N\mid\boldsymbol U)$, stated explicitly to be not state
    fidelity;
  - fairness range $S_\pi=\max_j\pi_j-\min_j\pi_j$ and player floor
    $F_\pi=\min_j\pi_j$, with the payoff vector retained as primary evidence.
- Definition-order correction: III-A no longer prints expected-payoff symbols
  before III-E, and Proposition 2 in III-D now states payoff covariance directly
  as equality of the underlying expectation sums. The proposition's scientific
  content and regression evidence are unchanged; `paper/CLAIM-SOURCE-MAP.md`
  was updated to match the printed Eq. (15).
- Evidence contract: `paper/CLAIM-SOURCE-MAP.md` now has a Section III-E table
  that classifies all rows as definitions/reporting contracts rather than
  simulation or hardware results. It also repeats that interaction-strength
  normalization remains unimplemented and its sensitivity control unrun.
- Mandatory TDD, initial cycle:
  `conda run -n entangled-equilibria python -m pytest
  tests/test_paper_structure.py -k 'section_iii_e' -v` was RED against the old
  scaffold (**6 failed, 4 deselected**) and GREEN after the replacement
  (**6 passed, 4 deselected**). Artifacts: `task-11-red-tests.txt` and
  `task-11-green-tests.txt`.
- Review-fix TDD cycle: strengthened full-equation, source-order, and first-use
  contracts produced RED (**3 failed, 5 passed, 4 deselected**) before the
  notation/table fixes and GREEN (**8 passed, 4 deselected**) after them.
  Artifacts: `task-11-review-fix-red-tests.txt` and
  `task-11-review-fix-green-tests.txt`.
- Final required test command:
  `conda run -n entangled-equilibria python -m pytest
  tests/test_paper_structure.py -v` -> **12 passed in 0.14s**. The tests are
  contract-focused: complete equations, required names/rules, source ordering,
  and first definition; they do not snapshot full paragraphs.
- Final wording scan: old III-E headings absent; ambiguous bare advantage prose
  labels 0; both canonical comparator names present in prose and table;
  all-zero/not-fidelity boundary present; both advantage equations precede the
  table; expected-player-payoff notation first appears at its III-E definition.
  Artifact: `task-11-wording-scans-final-2.txt`.
- Final guarded build: fresh
  `task-11-build-tmp-final/{pre,post}` directories under the SDD workspace;
  exact `pwd` guard passed before every `pdflatex` and `bibtex` call. Both
  control and post-change sequences exited 0 for pass 1, BibTeX, pass 2, and
  pass 3. Only the temporary build directory was deleted.
- Build diagnostics, pre-task control -> post-task: pages **14 -> 15**; overfull
  boxes **32 -> 34**, entirely the class-supplied output-routine category added
  with the page (body overfull boxes remained **3 -> 3**, with the same two
  title boxes and one pre-existing later-body box); underfull boxes **22 -> 27**
  (one page-tracking output-routine box and four cosmetic III-E line-break/table
  boxes); font warnings **6 -> 6**; hyperref PDF-string warnings **12 -> 12**;
  undefined citations **0 -> 0**; undefined references **0 -> 0**; fatal or
  emergency diagnostics **0 -> 0**; generic `LaTeX Warning` lines **0 -> 0**.
- Rendered inspection: pages 5--7 show the III-D/III-E/III-F transition. All
  equations fit the column; the non-floating two-row table follows both
  advantage equations; the fairness paragraph completes before the next
  subsection. Final render:
  `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-11-render.pdf`,
  SHA-256 `ca06b5c41b8e61cf4426198088427102862cda8d8ea16bb1fc72d78710556d10`.
- Protected artifacts passed before and after verification:
  `paper/qhd.pdf` and root `qhd.pdf` remain byte-identical at SHA-256
  `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`.
- Files modified by Task 11: `paper/qhd.tex`, `paper/CLAIM-SOURCE-MAP.md`,
  `paper/SECTION-III-EXECUTION-LOG.md`, and `tests/test_paper_structure.py`.
  No source, simulation, result, bibliography, or figure file was changed; no
  commit, stage, reset, clean, stash, or progress-ledger update was performed.
- Approved exceptions: none. Concerns for review: four cosmetic III-E underfull
  boxes are disclosed above; no body overfull box or semantic warning was added.

## 2026-08-02 - Task 11 independent review and checkpoint closure

- Historical-record rule: the Task 11 entry above remains unchanged as the
  implementation-time state, **implemented, awaiting independent review**. This
  closure records the later independent-review result without rewriting or
  deleting that checkpoint.
- Final independent-review verdict: all seven findings **ADDRESSED**; no new
  Critical or Important breakage; **SPEC PASS / QUALITY PASS**.
- Findings resolved:
  1. definition-before-use and mean-definition conflict;
  2. comparator-table order;
  3. incomplete and brittle contract tests;
  4. missing execution-log checkpoint;
  5. unexplained suppression of the fixed entangler-family `T` and applicable
     implementation/noise path in the compact deviation equation;
  6. III-E extraction-helper coupling to neighboring subsection names;
  7. build-summary regex exception.
- TDD evidence: the initial focused cycle was RED with **6 failed** and then
  GREEN with **6 passed**; the review-fix cycle was RED with **3 failed / 5
  passed** and then GREEN with **8 passed**; the final full structure suite was
  **12 passed**.
- Manuscript outcome: Section III-E now defines expected player payoffs and the
  full payoff vector; specializes the previously defined mean payoff; defines
  both `D` and `H` deviation gaps and requires every action for every player to
  pass; separates analytic-baseline advantage from the circuit-relative payoff
  gap; defines the all-zero target-state population and states explicitly that
  it is not fidelity; and defines the fairness range and player floor while
  retaining the payoff vector as primary, vector-first evidence.
- Build evidence: the guarded pre-task control and final four-pass builds both
  exited 0. Page count changed **14 -> 15**. The final build has zero undefined
  citations, zero undefined references, zero fatal/emergency diagnostics, and
  zero generic `LaTeX Warning` lines. Body overfull boxes remained **3 -> 3**.
  Four cosmetic III-E underfull boxes are disclosed and non-blocking.
- Final render: `task-11-render.pdf`, SHA-256
  `ca06b5c41b8e61cf4426198088427102862cda8d8ea16bb1fc72d78710556d10`.
- Protected artifacts remain byte-identical: `paper/qhd.pdf` and root `qhd.pdf`
  both retain SHA-256
  `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`.
- Binding Section V carry-forward: interaction-strength normalization remains
  unimplemented and the normalization control remains unrun. This limitation
  remains binding and must not be described as completed in Section V.
- Ledger completion: `Task 11: complete (uncommitted working-tree changes, review clean)`.
- Gate status: this checkpoint claims no gate decision and no user approval.
- Next action: Task 12, III-F cooperative-invariance proof. The next hard stop
  remains Gate G4 after Task 13.

## 2026-08-02 - Task 12 implementation checkpoint: III-F GHZ cooperative benchmark

- Status: **implemented, awaiting independent review**. This entry records the
  implementation and verification only; it does not claim Task 12 completion,
  user approval, independent approval, or Gate G4.
- Requirements source:
  `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-12-brief.md`.
- Exact non-overwriting pre-task snapshots were created before editing:
  - `task-12-pre-qhd.tex` — SHA-256
    `2785595e76de66555e25005a101a31b397e41c79006154fcc43d6d02dcb45dc7`
  - `task-12-pre-claim-source-map.md` — SHA-256
    `d0c0ffff3de2d51ef307c841d476b90b76a62b4dd616e4c61a0183eb14e86d71`
  - `task-12-pre-section-execution-log.md` — SHA-256
    `b58d9fee7c03a9c69f3bfa09b7603e52aa4c6cf8d9dfa726de8701519883a5df`
  - `task-12-pre-test_paper_claims.py` — SHA-256
    `f0a9f894d39305c435bf6304d8f1c36ee4ef78ba23c7b056a277b845155fd58d`
- Manuscript scope: the old `Noise Model and Simulation Paths` III-F scaffold,
  including its table, was replaced by `GHZ Cooperative Benchmark`,
  `\label{sec:ghz-benchmark}`. No old III-F prose, equation, number, citation, or
  framing was retained; no citation, figure, simulation result, or normalization
  claim was added.
- `Proposition 3 (Cooperative invariance in the entanglement angle)` states for
  every $\gamma$ that
  $J_{\mathrm{GHZ}}^\dagger Q_N^{\otimes N}J_{\mathrm{GHZ}}\ket{0^N}
  =-\ket{0^N}$, hence $p(0^N)=1$, $\pi_j=V/N$, and
  $\Delta_{\mathrm{ana}}=C/N$. The proof prints the GHZ two-branch state,
  the equal $N$-fold phases $e^{i\pi}=e^{-i\pi}=-1$, the resulting
  $-J_{\mathrm{GHZ}}\ket{0^N}$ state, and recovery of $-\ket{0^N}$ after
  applying $J_{\mathrm{GHZ}}^\dagger$.
- The live-parameter corollary specializes the maximal-entanglement benchmark to
  $V=4,C=3$: $\pi_j=4/N$ and $\Delta_{\mathrm{ana}}=3/N$. The significance
  sentence scopes the ``pure incentive dial'' language to this cooperative
  benchmark and says only that $\gamma$ can move the deviation incentives of
  III-G while leaving this cooperative payoff unchanged.
- `paper/CLAIM-SOURCE-MAP.md` now has one calibrated III-F Proposition row. It
  distinguishes the analytic proof and manuscript contract from the finite-grid
  numerical regressions, with exact node IDs and ranges. The Hawk/Dove deviation
  rows were assigned to III-G, and Task 12 does not promote them.
- Mandatory TDD: the new
  `tests/test_paper_claims.py::test_ghz_cooperative_benchmark_manuscript_contract`
  was RED against the old scaffold because the canonical heading was absent
  (**1 failed**), then GREEN after the replacement (**1 passed**). Artifacts:
  `task-12-red-test.txt`, `task-12-green-test-final.txt`.
- Exact proposition-related nodes: **39 passed** across the manuscript contract,
  general-$\gamma$ output regression ($N=2,\ldots,7$ over
  $\{0,0.2\pi,0.4\pi,0.5\pi\}$), maximal-entanglement output regression
  ($N=2,\ldots,8$), and live payoff/analytic-baseline regression
  ($N=2,\ldots,8$).
- Final required tests in `entangled-equilibria`: GHZ filter **70 passed, 128
  deselected**; complete `tests/test_paper_claims.py` **198 passed**; complete
  `tests/test_paper_structure.py` **12 passed**.
- Final focused scan: old III-F heading/prose/table label absent; exactly one
  general-$\gamma$ proposition and proof; both branch phases and the final
  disentangling recovery present; incentive-dial scope correct; no global
  payoff-invariance claim, bare ambiguous advantage, or metric redefinition.
- Guarded control and final builds ran in fresh directories under the Task 12
  workspace. An exact `pwd` equality guard ran before every `pdflatex` and
  `bibtex`. Both four-pass sequences exited 0. Control -> final diagnostics:
  pages **15 -> 15**; overfull boxes **34 -> 34** (body **3 -> 3**, output-routine
  **31 -> 31**); underfull boxes **27 -> 27**; font warnings **6 -> 6**;
  hyperref PDF-string warnings **12 -> 12**; generic LaTeX warnings,
  undefined citations, undefined references, and fatal/emergency diagnostics
  all **0 -> 0**.
- Rendered inspection of pages 5--8 confirms the III-E/III-F/old-III-G boundary,
  proof fit, equation fit, and page density. The proof and corollary remain on
  page 7 with no new body overflow. Preserved render: `task-12-render.pdf`,
  SHA-256 `6ae517007f64a11de095c94050da10ba8c2af878f9d8c1b4940f4d19b44cbd68`.
- Protected artifacts passed before and after verification: `paper/qhd.pdf` and
  root `qhd.pdf` remain byte-identical at SHA-256
  `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`.
- Temporary build directories are removed only after the report evidence is
  extracted. Files modified by Task 12 are `paper/qhd.tex`,
  `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`, and
  `tests/test_paper_claims.py`; no source implementation, bibliography, figure,
  progress ledger, or protected PDF was modified.
- Review concern: the rendered next subsection is still the old III-G
  `Architectural Interpretation` scaffold. Task 13 must replace it with the
  planned incentive-compatibility derivation; Task 12 does not treat that old
  scaffold as content evidence.

## 2026-08-02 - Task 12 independent review, fix round 1, and checkpoint closure

- Historical-record rule: the Task 12 implementation entry above remains
  unchanged as **implemented, awaiting independent review**. This closure adds
  the later review and fix-round record without deleting or rewriting that
  checkpoint.
- Initial independent-review verdict: the mathematics, corollaries, and evidence
  calibration were correct. There were no Critical or Minor findings. The
  review reported two Important findings: false III-E/III-F handoffs and an
  under-specified manuscript proof contract.
- Fix round 1 addressed both findings:
  1. III-E now hands off truthfully to the exact GHZ cooperative benchmark.
  2. III-F references the planned Section III-G analysis rather than claiming
     false adjacency to the existing scaffold; the old III-G `Architectural
     Interpretation` scaffold remains untouched.
  3. The manuscript contract now requires exactly one proof environment and
     checks, in source order, the GHZ state expansion, both $N$-fold phases,
     both branch actions, the intermediate
     $-J_{\mathrm{GHZ}}(\gamma)\ket{0^N}$ state, and the final
     $J_{\mathrm{GHZ}}^\dagger$ recovery of $-\ket{0^N}$.
- Mutation sensitivity: an in-memory mutation of the proof branch from `+i` to
  `-i` was detected by the strengthened checker. The canonical manuscript was
  not modified for this check, and its canonical recheck passed.
- Final re-review: both Important findings were **ADDRESSED**; no new Critical or
  Important breakage was found; the mathematical verdict remained correct; the
  review was clean.
- Final test evidence already produced for this closure: strengthened manuscript
  contract **1 passed**; exact proposition nodes **39 passed**; required GHZ
  filter **70 passed, 128 deselected**; combined claims and structure suites
  **210 passed**.
- Final guarded rebuild: **15 pages**; **34 overfull boxes total** (**31** class
  output-routine and **3** pre-existing body); **27 underfull boxes**; **6** font
  warnings; **12** hyperref PDF-string warnings; and zero generic warnings,
  undefined citations, undefined references, or fatal/emergency diagnostics.
- Final inspected render: `task-12-render.pdf`, SHA-256
  `2846b3145f082ea73ff5955c96abbc895d4c270dc418bd6d5808ca92fa59f210`.
- Protected PDFs remain byte-identical: `paper/qhd.pdf` and root `qhd.pdf` both
  retain SHA-256
  `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679`.
- Cleanup: the scratch helper and build directory were inspected and removed;
  evidence `.txt` artifacts were preserved. No concern remains.
- Ledger fix-round line: `Task 12: fix round 1/5 (2 addressed, 0 open — truthful handoffs; ordered proof contract with mutation sensitivity; uncommitted)`.
- Ledger completion line: `Task 12: complete (uncommitted working-tree changes, review clean)`.
- Gate status: this closure claims no user approval and no Gate G4 approval.
- Next action: Task 13, III-G incentive boundary. After Task 13 and its clean
  review, stop at Gate G4 for explicit user approval.

## 2026-09-07 submission revision continuation

The user subsequently authorized implementation, commits and hardware runs:
"commit and run, no need of my approval whatever is best do it". The earlier
Task 12 stop is superseded for this scoped revision. See
[JOURNAL-REVISION-LOG.md](JOURNAL-REVISION-LOG.md) for the III-G proof,
claim/evidence addendum, new source audit, and hardware registration policy.
