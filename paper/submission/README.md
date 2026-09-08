# Submission files

Run `python scripts/build_submission.py` from the repository root with
MiKTeX/TeX Live available. The script preserves `paper/qhd.pdf` and the root
`qhd.pdf`, builds a separate draft, and creates a portable LaTeX source ZIP.
Use `qhd.tex` as the main document after extracting the source archive.

The September 8 layout follows `FQCNN_journal.pdf`, using black-and-white
IEEEtran conference-style formatting and the same evaluation/framework/
methods/results/discussion section sequence. The target remains a journal
article; the chosen class reflects the requested PDF reference.

`qhd-code-and-data.zip` supplies tracked source, experiments, tests, recorded
results, and evidence notes as a fixed snapshot of the now-public repository. Its
manifest hashes every included file. `frozen-phase-code/` preserves the exact
pre-execution code from commit `76aa8fd`, including all source hashes used in
both September 7 registrations. Current validation code is hardened separately;
the historical manifests and decisions are unchanged. Offline analyses can
use the archive; live submission/recovery checks still require a committed
Git checkout of the appropriate revision. No credentials or local virtual
environment are included.

The manuscript and source archive are prepared for author review and portal
upload; no journal submission has been made by this workflow. Complete the
author declarations listed at the end of the cover-letter draft before
sending it. That private completion note is not part of the letter to editors.

Evidence: `paper/JOURNAL-REVISION-LOG.md` maps new claims to code and results.
New offline analyses live in `results/journal-strengthening/2026-09-07-offline`.
Committed hardware registrations, serialized circuits, device rehearsals,
raw counts and charged-usage metrics live in `results/phase-validation`.
Historical simulation pins remain separate from the isolated hardware
environment, whose freeze accompanies the pilot registration.

September 8 validation: 898 tests passed, 3 skipped in the historical pinned
environment; 78 focused audit/extension/replay tests passed in the current
hardware environment. Legacy Qiskit deprecation warnings remain. The 18-page
manuscript and isolated source archive compile without unresolved references,
citations or overfull boxes. The independent raw-count audit reproduces all
three hardware judgments. See `docs/reviews/2026-09-08-validation.md` for the
complete record and reproduction commands.

IEEE's [TQE submission page](https://tqe.ieee.org/submission-process/) links
the author portal and states no page limit. The
[IEEE author policy](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/)
requires disclosure of generated content and of overlapping publications.
The manuscript includes an acknowledgment describing Codex's contribution.
