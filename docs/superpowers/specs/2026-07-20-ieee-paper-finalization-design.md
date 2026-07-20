# IEEE Paper Review-Draft Finalization Design

**Date:** 2026-07-20  
**Repository:** `Multiplayer-QHD-Game`  
**Target:** Reviewable IEEE conference-format PDF

## Goal

Produce an evidence-preserving IEEE-formatted review draft from the existing manuscript. The draft must be suitable for author review while remaining explicit about incomplete hardware validation and unresolved author sign-offs.

The work must not introduce any numerical value, experimental result, uncertainty, shot count, device claim, statistical claim, or bibliographic fact that is not supported by the repository or an authoritative publication record.

## Deliverables

1. `paper/main.pdf`: compiled IEEE-format review draft.
2. `paper/REVIEW-NOTES.md`: concise list of items that remain before submission.
3. Corrected paper sources required to build the PDF.
4. A reproducible local build command documented in `paper/README.md` if the current command requires adjustment.

## Manuscript Editing Scope

Preserve the existing single-file `IEEEtran` manuscript structure. Make surgical corrections only.

### Required corrections

- Remove the visible second-author email TODO from the review draft without inventing an address.
- Fix the undefined section reference to the simulation-results section.
- Correct the classical Hawk–Dove equilibrium description for the repository's live parameters, `V=4` and `C=3`. Under the stated payoff matrix, Hawk strictly dominates Dove, so all-Hawk is the relevant pure equilibrium and `V/C` is not an interior mixed-strategy probability.
- Normalize equilibrium wording throughout the abstract, contributions, results, captions, and discussion. The tested profile passes the repository's pure-deviation Nash check at `N=2,3`; wording may state that `N=3` is the only passing genuinely multiplayer case when the domain is explicitly restricted to `N>=3`.
- Clarify that the hardware scaling table reports the registration-source execution while the hardware scaling figure summarizes two executions from one calibration day.
- Preserve all scope qualifications:
  - the `N=4,5` fixed profile is not a certified equilibrium;
  - T9 adaptation is exploratory and pending game-theory sign-off;
  - per-player hardware reporting was not preregistered;
  - the repeated `N=5` deficit sign was observed outside the registered acceptance test;
  - hardware evidence covers one device, one chain, and one calibration day;
  - cross-day validation remains incomplete.
- Remove bibliography TODO text that would print in the review PDF. Do not fabricate missing authors, volumes, dates, identifiers, or publication details.
- Synchronize paper-facing status wording that directly affects review of the manuscript.

### Explicit exclusions

Do not:

- generate or recompute experimental data;
- add new simulations or hardware results;
- create error bars unsupported by existing artifacts;
- strengthen provisional claims;
- describe `N=4,5` as Nash equilibria;
- describe observational analyses as preregistered;
- redesign figures or replace result artifacts;
- perform broad repository cleanup;
- claim the manuscript is submission-ready.

## Evidence Policy

Every scientific number must trace to an existing repository artifact already cited by the manuscript or to a verified source in the repository's evidence ledger. Existing provenance comments beside claims and figures must be preserved unless their paths are demonstrably stale.

If a statement cannot be reconciled from repository evidence, weaken or remove it rather than guessing. Non-numerical editorial transitions may be rewritten for clarity, but they must not change the scientific meaning.

## Bibliography Policy

For the review draft:

- retain cited entries required for successful compilation;
- remove printable TODO notes;
- leave unresolved metadata listed in `paper/REVIEW-NOTES.md`;
- do not invent or infer missing publication fields;
- treat authoritative metadata verification as a pre-submission task unless it can be confirmed directly without ambiguity.

## Build Design

Install MiKTeX on Windows, including `latexmk`, BibTeX, `IEEEtran`, and the manuscript's package dependencies. Build from the `paper/` directory with:

```text
latexmk -pdf main.tex
```

Generated auxiliary files may remain untracked or be cleaned after verification. `paper/main.pdf` is the review artifact.

## Verification

A successful review build requires:

- no fatal LaTeX or BibTeX errors;
- no missing citation warnings after the final pass;
- no undefined references or rendered `??` markers;
- no visible TODO markers in the manuscript;
- all six existing figures present and rendered;
- no missing-font or missing-package errors;
- no severe overfull boxes that obscure or overlap content;
- equations, tables, captions, author blocks, and references readable in the two-column IEEE layout.

Visually inspect every PDF page for clipped figures, unreadable labels, broken equations, bad column breaks, displaced captions, and accidental blank pages.

## Review Notes

`paper/REVIEW-NOTES.md` must identify, at minimum:

- Aasa Singh Bhui's email address;
- unresolved Varsamis and Flitney bibliography metadata;
- Aasa's game-theory sign-off on the T9 learning rule;
- additional independent calibration-day hardware runs;
- validation of submission-time calibration provenance on the next run;
- the wiring-permutation/W-topology hardware control or an explicit deferral;
- target venue, current author instructions, and page limit;
- final author review and submission-package checks.

## Success Criterion

The task is complete when a cleanly rendered `paper/main.pdf` exists, all claims in the edited manuscript remain traceable to repository evidence, the build passes the verification checks above, and all unresolved submission work is visible in `paper/REVIEW-NOTES.md` rather than hidden or fabricated.
