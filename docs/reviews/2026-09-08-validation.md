# September 8 validation record

Audit starting revision: `6e7e65a`; branch: `review/full-audit-fqcnn-format`.

| Check | Result |
|---|---|
| Complete historical pinned-environment pytest suite | **898 passed, 3 skipped**, 345.69 seconds |
| Current hardware environment: audit, journal extensions and raw-result replay | **78 passed**, 23.45 seconds |
| Independent raw-bitstring payoff/confidence/provenance audit | All three jobs agree; every checked frozen-source hash matches |
| Ruff undefined-name checks (F821/F822/F823), source and scripts | Passed |
| Git whitespace check | Passed |
| LaTeX manuscript | 18 pages, no unresolved references/citations or overfull boxes |
| Portable source ZIP compiled in a fresh temporary directory | Passed, including BibTeX and three LaTeX passes |
| Evidence ZIP CRC and every manifest file hash | Passed |
| Historical root and paper PDFs | Both retain SHA256 `c7e77e3a7f0e871cdf77d05741a459e87025a6114ec89ef074e57aa7e7d65679` |

The full suite emits 292,890 warnings, principally inherited Qiskit/Aer
deprecations in the pinned historical stack. Three existing tests are skipped;
this is not a claim that those checks ran. An earlier audit run caught one stale
documentation anchor after a scientific comment was corrected. That anchor was
fixed, its focused checks passed, and the complete suite above was rerun cleanly.

The paper's title/author layout and body were visually compared with the supplied
FQCNN reference; the new evaluation table was also rendered and inspected.
The conference-style IEEEtran class matches that reference. Final target-journal
portal requirements and author declarations remain submission responsibilities.

## Reproduction

From the repository root, use the historical pinned environment for the full
suite; use the isolated modern hardware environment for the second command:

```text
python -m pytest -q --disable-warnings --tb=short
python -m pytest tests/test_audit_regressions.py tests/test_journal_extensions.py tests/test_registered_phase_results.py -q
python scripts/audit_phase_evidence.py
python -m ruff check src scripts --select F821,F822,F823
python scripts/build_submission.py
python scripts/check_submission_archive.py
git diff --check
```

The independent evidence script uses committed historical sources and therefore
requires this repository's Git history. Package compilation requires a LaTeX
installation. No command above submits a QPU job. The three recorded jobs retain
their original total charge of 175 seconds and their original acceptance results.

The initial push was blocked by the installed `gstack-redact-prepush` hook:
it reports `HIGH engine.input_too_large` when the added-line input exceeds its
1 MiB cap. The rejected push did not identify a specific credential. The new
branch's diff against the default branch includes older history; even historical
commit `03d642d` adds approximately 1.28 MB of scan input by itself. Ordinary
smaller pushes therefore cannot fully resolve the limit. The hook was not
disabled or bypassed. Following the user's explicit request to resolve the
blocker and create the PR, the local hook now passes the engine's supported
`maxBytes` option with a bounded 8 MiB limit. All input is still scanned and HIGH
findings still block. Checks verified that a clean input larger than 1 MiB is
scanned, a synthetic credential in that input is detected, and input exceeding
8 MiB is rejected. PR checks report the subsequent GitHub CI status.

The Phase 1 star chart was re-rendered from the retained results JSON with
two-decimal labels on all bars. The N=4 hub remains
`2.220446049250313e-16` in the source and displays `0.00`. The source JSON SHA256
remains `534ec53aaa486b798a82838027405c2cad53745aa72196390cdb9ca79939b963`.
The caption now describes N=4..6 and green mean bars. The user subsequently
approved Phases 2 and 3: ring values were recomputed on the pinned conda stack,
N-scaling markers now reflect Nash status, and the hardware figure is split
into three single-column PDFs with its caveats retained. The focused combined
checks passed (384 passed, 3 skipped). The initial Linux CI failures exposed
overly strict exact floating-point equality in three hardware replay tests;
the corrected test retains exact decisions and tolerates only numerical
roundoff in statistics. See the figure-phases review for the full record.

This record does not constitute external peer review or
prove absence of every defect. See the accompanying full-project audit for the
remaining scientific and methodological limitations.
