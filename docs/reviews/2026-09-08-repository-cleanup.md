# Repository cleanup — 2026-09-08

## Scope and findings

The sweep covered tracked-file inventory, byte-identical duplicates, large
artifacts, generated files, branch ancestry, build instructions, and CI.
The reviewed development branch is a descendant of main, so publication can
use a normal fast-forward push without rewriting history.

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

Run the complete pytest suite in the pinned `entangled-equilibria` environment,
rebuild the submission artifacts, validate their hashes and isolated LaTeX
compilation, and check Git integrity and whitespace before publication.
The final test results are reported with the publication outcome.

## Open scientific work

Q1 eligibility and current retraction status are still pending verification in
`paper/Q1-REFERENCE-AUDIT.md`. Repository cleanup does not resolve that audit
or declare the manuscript ready for submission.
