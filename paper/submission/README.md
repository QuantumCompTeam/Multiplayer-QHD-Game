# Submission files

Run `python scripts/build_submission.py` from the repository root with
MiKTeX/TeX Live available. The script preserves `paper/qhd.pdf` and the root
`qhd.pdf`, builds a separate draft, and creates a portable LaTeX source ZIP.
Use `qhd.tex` as the main document after extracting the source archive.

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

Validation: 858 tests passed, 3 skipped in the historical pinned environment
on 7 September 2026; 40 extension tests also passed in the isolated current
hardware environment. Legacy Qiskit deprecation warnings remain. The LaTeX
build checks for unresolved references/citations; inherited class output-box
warnings require visual inspection rather than treating every warning as an
unreadable page.

IEEE's [TQE submission page](https://tqe.ieee.org/submission-process/) links
the author portal and states no page limit. The
[IEEE author policy](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/)
requires disclosure of generated content and of overlapping publications.
The manuscript includes an acknowledgment describing Codex's contribution.
