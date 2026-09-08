# Repository cleanup — 2026-09-08

## Scope and findings

The sweep covered tracked-file inventory, byte-identical duplicates, large
artifacts, generated files, branch ancestry, build instructions, and CI.
Main contains three merge-history commits absent from the development branch,
with no additional file changes. Merge that history into the cleanup branch
before the normal push; do not rewrite history.

## Changes

- Remove seven obsolete `paper/main` LaTeX intermediates: aux, bbl, blg,
  fdb_latexmk, fls, log, and out. Ignore future intermediates only under
  `paper/`; research execution logs remain tracked.
- Ignore local `.superpowers/` session state and the documented isolated
  LaTeX build directory.
- Replace the identical root status snapshot with links to the current
  handoff and the preserved July snapshot in `docs/PROJECT-STATUS.md`.
- Correct the paper README's obsolete figure count, hardware aggregate
  description, and combined-figure provenance.
- Remove the README's MIT badge because there is no tracked license file,
  and remove the speculative arXiv badge. This does not grant or change a license.
- Include the citation-format change and the explicitly unfinished reference
  eligibility audit; do not advertise the bibliography as Q1-certified.

## Retained material

Result directories, preregistrations, superseded findings, original execution
logs, and historical manuscript assets preserve scientific provenance.
Copies of result figures in `paper/figs/` are intentional portable-build inputs.
The submission PDF and source/evidence ZIPs are deliverables, not disposable
caches. Local untracked PDFs and experimental runs are left untouched.

## Validation

The complete pytest suite in the pinned `entangled-equilibria` environment
passed: 919 passed, 4 skipped. Git integrity, whitespace checks, and Python
compilation passed. The rebuilt submission archive passed 498 evidence-file
hash checks and isolated LaTeX compilation without unresolved citations,
references, or overfull boxes. All 41 PDF citation links resolve to page 18.

## Open scientific work

Q1 eligibility and current retraction status are still pending verification in
`paper/Q1-REFERENCE-AUDIT.md`. Repository cleanup does not resolve that audit
or declare the manuscript ready for submission.
