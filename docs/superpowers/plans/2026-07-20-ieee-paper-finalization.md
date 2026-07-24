# IEEE Paper Review-Draft Finalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a compiled, visually checked IEEE-format review PDF whose scientific numbers and claims remain traceable to existing repository evidence.

**Architecture:** Keep the existing single-file `IEEEtran` manuscript and six tracked figures. Apply surgical consistency corrections in `paper/main.tex`, remove printable unresolved metadata from `paper/references.bib`, record all remaining submission work in `paper/REVIEW-NOTES.md`, then install MiKTeX and build `paper/main.pdf`. Verify the source statically, compile without unresolved references or citations, run the repository's documentation checks, and inspect every PDF page.

**Tech Stack:** IEEEtran LaTeX, BibTeX, MiKTeX 25.12, latexmk, PowerShell 5.1, repository Conda environment `entangled-equilibria`, pytest.

## Global Constraints

- Do not introduce any numerical value, experimental result, uncertainty, shot count, device claim, statistical claim, or bibliographic fact that is unsupported by the repository or an authoritative publication record.
- Do not generate or recompute experimental data.
- Preserve provenance comments beside scientific claims and figures.
- Keep `N=4,5` described as a fixed cooperative protocol, not a certified Nash equilibrium.
- Keep T9 adaptation explicitly exploratory and pending game-theory sign-off.
- Keep per-player hardware reporting and same-sign `N=5` reproduction outside the preregistered-test scope.
- Keep hardware generalization limited to one device, one chain, and one calibration day.
- Do not redesign or replace any of the six existing figures.
- Produce a review draft, not a submission-ready claim.
- Do not commit implementation changes unless the user explicitly authorizes another commit; use review checkpoints instead.

## File Structure

- Modify `paper/main.tex`: manuscript wording, cross-reference, author block, and hardware aggregation clarification.
- Modify `paper/references.bib`: remove printable unresolved-metadata notes without inventing fields.
- Modify `paper/README.md`: correct stale paper status and document the verified local build command.
- Create `paper/REVIEW-NOTES.md`: centralize all unresolved pre-submission work.
- Generate `paper/main.pdf`: compiled IEEE review artifact.
- Do not modify files under `results/`, `paper/figs/`, `src/`, `experiments/`, or `scripts/`.

---

### Task 1: Lock the evidence boundary and capture pre-edit failures

**Files:**
- Read: `paper/main.tex`
- Read: `paper/references.bib`
- Read: `paper/README.md`
- Read: `docs/VERIFIED-FACTS.md`
- Read: `results/hardware-scaling/repeat-judgments.json`
- Read: `results/hardware-scaling/2026-07-17T014458Z/plots/caption.md`

**Interfaces:**
- Consumes: Existing repository artifacts and the approved design specification.
- Produces: A bounded edit list and reproducible static checks that fail on the current draft.

- [ ] **Step 1: Confirm a clean starting tree and current revision**

Run:

```bash
git status --short
git rev-parse --short HEAD
```

Expected: no output from `git status --short`; HEAD includes the approved design commit `a2ce611` or a descendant.

- [ ] **Step 2: Verify all manuscript figures exist without regenerating them**

Run from the repository root:

```bash
python - <<'PY'
from pathlib import Path

figs = [
    "advantage_vs_N.png",
    "topology_heatmap.png",
    "advantage_vs_gamma_N4.png",
    "per_player_advantage_star.png",
    "hardware_n3_validation.pdf",
    "hardware_scaling.pdf",
]
missing = [name for name in figs if not (Path("paper/figs") / name).is_file()]
assert not missing, f"missing figures: {missing}"
print("6/6 paper figures present")
PY
```

Expected: `6/6 paper figures present`.

- [ ] **Step 3: Capture the current source defects with an exact static check**

Run:

```bash
python - <<'PY'
from pathlib import Path

tex = Path("paper/main.tex").read_text(encoding="utf-8")
bib = Path("paper/references.bib").read_text(encoding="utf-8")
expected = {
    "visible author placeholder": r"\todo{email}" in tex,
    "broken results reference": r"\ref{sec:results}" in tex,
    "invalid mixed-equilibrium sentence": "probability $V/C$" in tex,
    "printable bibliography note": "note    = {TODO:" in bib,
}
for name, present in expected.items():
    print(f"{name}: {'FOUND' if present else 'MISSING'}")
assert all(expected.values()), expected
PY
```

Expected: all four lines end in `FOUND`. This establishes that the post-edit source check is meaningful.

- [ ] **Step 4: Record the exact evidence used for the two-run clarification**

Read and retain these facts without changing them:

- `paper/README.md` identifies `paper/figs/hardware_scaling.pdf` as a two-run aggregate.
- `paper/main.tex` Table II identifies its values as a single run.
- `results/hardware-scaling/2026-07-17T014458Z/plots/caption.md` identifies the plot as two runs.
- `ITEMS.md` records one distinct calibration day.

Expected: wording changes in Task 2 distinguish executions from calibration days and do not add a new result.

- [ ] **Step 5: Review checkpoint**

Run:

```bash
git diff --exit-code
```

Expected: no diff. Task 1 is evidence collection only.

---

### Task 2: Correct manuscript consistency without changing the data

**Files:**
- Modify: `paper/main.tex:1-205`
- Modify: `paper/main.tex:466-520`

**Interfaces:**
- Consumes: The evidence boundary established in Task 1.
- Produces: A manuscript with consistent equilibrium language, no visible author placeholder, a valid results cross-reference, and an explicit single-run/two-execution distinction.

- [ ] **Step 1: Remove the visible author placeholder without inventing an email**

Replace the author block:

```latex
\IEEEauthorblockN{Aasa Singh Bhui}
\IEEEauthorblockA{VIT Vellore\\\todo{email}}
```

with:

```latex
\IEEEauthorblockN{Aasa Singh Bhui}
\IEEEauthorblockA{VIT Vellore}
```

Because no `\todo` invocation remains afterward, remove:

```latex
\newcommand{\todo}[1]{\textcolor{red}{[TODO: #1]}}
```

Keep `xcolor` because `hyperref` uses explicit link colors.

- [ ] **Step 2: Normalize the abstract's equilibrium boundary**

Replace:

```latex
--- but it is a self-enforcing equilibrium only at $N=3$. Second, under noise
```

with:

```latex
--- but it passes our pure-deviation equilibrium test only at $N=2,3$
(and only at $N=3$ among the genuinely multiplayer cases $N\ge3$). Second,
under noise
```

Retain the following sentence that names GHZ as a pure equilibrium at `N=2,3`.

- [ ] **Step 3: Qualify the registered prediction and observed repeat correctly**

Replace the abstract clause:

```latex
$N{=}4$ to 0.004 but over-predicts $N{=}5$ by 0.010, a registered
$\approx$5$\sigma$ deviation that reproduces across runs;
```

with:

```latex
$N{=}4$ to 0.004 but over-predicts $N{=}5$ by 0.010, an
$\approx$5$\sigma$ miss of the registered predictive interval; the same-sign
$N{=}5$ deficit recurs in a second execution, although sign reproduction was
not itself a preregistered test;
```

This preserves the repository values while separating the registered interval from the later observational repeat.

- [ ] **Step 4: Replace the contradictory opening motivation with the live game convention**

Replace the first Introduction paragraph at `paper/main.tex:69-80` with:

```latex
Financial markets are coordination problems with adversarial payoffs. When
traders compete over a scarce asset, each chooses between an aggressive
position --- capturing the full value if unopposed --- and a cooperative one
that shares value reliably. The Hawk--Dove game formalizes this tension. Under
the live convention used throughout this work, $V{=}4$ and $C{=}3$, Hawk
strictly dominates Dove in the two-player payoff matrix: it pays more against
either opposing action, so mutual Hawk is the unique classical pure Nash
equilibrium. Yet mutual Dove pays each player $V/2=2$, whereas mutual Hawk pays
only $(V-C)/2=0.5$. The resulting gap isolates the mechanism-design problem:
individually rational aggression destroys value that cooperation would
preserve. Classical remedies are external to the game, including trust between
counterparties, a trusted intermediary, or regulation that taxes defection.
```

The values `2` and `0.5` are direct evaluations of the payoff matrix already printed in the manuscript.

- [ ] **Step 5: Normalize contribution item 1**

Replace:

```latex
that the fixed GHZ-derived cooperative profile $(Q_N,\dots,Q_N)$ is a pure
Nash equilibrium only at $N=3$; for $N\ge4$ a unilateral Hawk deviation
```

with:

```latex
that the fixed GHZ-derived cooperative profile $(Q_N,\dots,Q_N)$ passes the
pure-deviation Nash check at $N=2,3$ --- only $N=3$ among the genuinely
multiplayer cases $N\ge3$; for $N\ge4$ a unilateral Hawk deviation
```

- [ ] **Step 6: Qualify contribution item 3's repeat claim**

Replace:

```latex
fitted at $N{=}3$ --- the registered primary prediction --- matches
$N{=}4$ to 0.004 while its $N{=}5$ miss (0.010, $\approx$5$\sigma$,
reproduced) leaves a registered per-two-qubit-gate decay baseline leading
```

with:

```latex
fitted at $N{=}3$ --- the registered primary prediction --- matches
$N{=}4$ to 0.004 while its $N{=}5$ miss (0.010, $\approx$5$\sigma$ relative
to the registered predictive interval) has the same sign in a second
execution; sign reproduction was observational, not a preregistered test. A
registered per-two-qubit-gate decay baseline leads
```

- [ ] **Step 7: Correct the Background equilibrium paragraph**

Replace `paper/main.tex:156-162` with:

```latex
We fix $V{=}4,\ C{=}3$ throughout (the repo's live convention,
\texttt{src/config.py}). At these values Hawk strictly dominates Dove: against
Dove it pays $V=4$ rather than $V/2=2$, and against Hawk it pays
$(V-C)/2=0.5$ rather than $0$. The unique classical pure Nash equilibrium is
therefore mutual Hawk, even though mutual Dove is Pareto-superior. The familiar
interior mixed equilibrium with Hawk probability $V/C$ applies only when
$V<C$; here $V/C=4/3$ lies outside the probability simplex. This distinction
is why the paper uses the all-Hawk payoff as its classical pure-equilibrium
baseline.
```

- [ ] **Step 8: Fix the undefined results reference**

Replace:

```latex
Sec.~\ref{sec:results}
```

with:

```latex
Sec.~\ref{sec:sim}
```

- [ ] **Step 9: Mark per-player hardware reporting as outside the registered acceptance test**

After the advantage-reporting conventions at `paper/main.tex:222-228`, add:

```latex
Per-player hardware breakdowns are diagnostic analyses added after
registration; they are not part of the registered acceptance test.
```

This preserves the per-player evidence while preventing it from being read as a preregistered outcome.

- [ ] **Step 10: Clarify the hardware table and figure populations**

Change the Table II caption to:

```latex
\caption{Measured advantage on ibm\_fez for the registration-source execution
(4096 shots; additional executions and cross-day repeats are reported
separately). Ideal advantage is $3/N$; retention is ZNE/ideal.}
```

Replace the complete existing Figure 6 caption with:

```latex
\caption{Two-execution aggregate of the $N$-player GHZ EWL quantum advantage
on ibm\_fez (IBM Heron r2), physical chain $[59,75,74,73,79]$, 4096 shots per
execution. Both executions use the same recorded calibration day;
Table~\ref{tab:scaling} reports the registration-source execution alone.
\textbf{(A)} Measured cooperative-profile advantage (mean $(Q,\ldots,Q)$
payoff minus the analytic noiseless classical-Nash payoff) at $N=3,4,5$:
raw (open) and readout-mitigated $+$ ZNE (filled), against the noiseless
ideal ($1.0, 0.75, 0.6$), the device noise-model prediction (diamonds), and
a single-parameter depolarizing model with $p_{\mathrm{eff}}=0.0018$ fitted
to the $N{=}3$ point alone --- its $N{=}4,5$ values are predictions, not
fits. Error bars: multinomial shot noise (raw) and weighted-fit standard
error (ZNE). \textbf{(B)} ZNE mechanics: readout-mitigated payoff vs cz
fold factor ($\lambda=1,3,5$) with the weighted linear fit extrapolated to
$\lambda=0$ (stars). \textbf{(C)} Ground-state probability
$P(|0\ldots0\rangle)$: the state fidelity decays several times faster than
the advantage because the mean-payoff observable is first-order insensitive
to single bit-flips from $|0\ldots0\rangle$. $(Q,\ldots,Q)$ is a pure Nash
equilibrium only at $N{=}3$ among the plotted genuinely multiplayer cases;
at $N{=}4,5$ the profile is the cooperative quantum protocol, not an
equilibrium.}
```

Add this non-rendered provenance comment immediately after the figure:

```latex
% aggregate source: results/hardware-scaling/2026-07-17T014458Z/plots/hardware_scaling.pdf
```

- [ ] **Step 11: Apply the same preregistration qualification in the hardware narrative**

Replace:

```latex
it over-predicts by $0.010$ ($\approx$5$\sigma$ of the registered predictive
interval), a deficit that reproduces on a second run.
```

with:

```latex
it over-predicts by $0.010$ ($\approx$5$\sigma$ of the registered predictive
interval). The deficit has the same sign in a second execution, an
observational repeat rather than a preregistered sign test.
```

- [ ] **Step 12: Run the post-edit static source check**

Run:

```bash
python - <<'PY'
from pathlib import Path

tex = Path("paper/main.tex").read_text(encoding="utf-8")
assert r"\todo{" not in tex
assert r"\ref{sec:results}" not in tex
assert "probability $V/C$;" not in tex
assert "only at $N=3$;" not in tex
assert "sign reproduction was observational" in tex
assert "Two-execution aggregate" in tex
assert "same recorded calibration day" in tex
assert r"\ref{sec:sim}" in tex
print("manuscript consistency checks passed")
PY
```

Expected: `manuscript consistency checks passed`.

- [ ] **Step 13: Review checkpoint**

Run:

```bash
git diff --check -- paper/main.tex
git diff -- paper/main.tex
```

Expected: no whitespace errors; every changed line traces to the approved design.

---

### Task 3: Move unresolved submission work out of the rendered manuscript

**Files:**
- Modify: `paper/references.bib:1-49`
- Modify: `paper/README.md:9-40`
- Create: `paper/REVIEW-NOTES.md`

**Interfaces:**
- Consumes: The unresolved metadata and sign-off list from the approved design.
- Produces: A compilable bibliography without printable TODO notes, accurate paper status documentation, and a single review checklist.

- [ ] **Step 1: Remove printable bibliography notes without adding metadata**

Change `varsamis2025` from:

```bibtex
  journal = {Advanced Quantum Technologies},
  year    = {2025},
  note    = {TODO: complete author list and volume}
```

into:

```bibtex
  journal = {Advanced Quantum Technologies},
  year    = {2025}
```

Change `flitney2002` from:

```bibtex
  pages   = {e36404},
  year    = {2012},
  note    = {TODO: README cites 2002; verify year (PLoS ONE version is 2012)}
```

into:

```bibtex
  pages   = {e36404},
  year    = {2012}
```

Keep the existing source comments at the top of the file because comments do not render. Do not change the citation key `flitney2002`; changing it is unnecessary for the review build.

- [ ] **Step 2: Create `paper/REVIEW-NOTES.md` with exact unresolved items**

Create:

```markdown
# IEEE Review Draft Notes

The compiled `main.pdf` is an evidence-preserving review draft, not a submission-ready manuscript. No numerical result was added or recomputed during the formatting pass.

## Author input

- Add Aasa Singh Bhui's preferred publication email to the IEEE author block.
- Obtain Aasa's game-theory sign-off on the exploratory T9 independent round-robin best-response rule and its interpretation.
- Complete final author review of all sections drafted from repository artifacts.

## Bibliography verification

- Verify the complete author list and publication metadata for `varsamis2025` against the published version.
- Reconcile the repository's `flitney2002` citation key/README wording with the cited PLoS ONE publication year, which is currently recorded as 2012 in `references.bib`.
- Verify page, article-number, DOI, and volume metadata for the 2025 references before submission.

## Hardware evidence still in progress

- Complete the registered target of 3--5 distinct calibration-day executions; the current executions share one recorded calibration day.
- Validate environment provenance and `calibration_at_submit.json` on the next hardware execution.
- Make the repeat judge consume the submission-time calibration snapshot or document a manual verification step.
- Run the W-topology/wiring-permutation hardware control, or explicitly defer it and narrow the player-position claim.
- Regenerate the scaling figure and any cross-day uncertainty summary only after new repository artifacts exist.

## Submission checks

- Confirm the exact IEEE QCE submission category, current author instructions, and page limit.
- Rebuild after adding verified author and bibliography metadata.
- Run a final citation, figure, accessibility, and PDF-conformance review.
- Prepare the final submission package only after the remaining author and hardware decisions are resolved.
```

- [ ] **Step 3: Correct `paper/README.md` status and build instructions**

Keep the existing target and thesis description. Replace the Build and Status sections with:

````markdown
## Build

Overleaf: upload this complete `paper/` folder; IEEEtran is built in.

Windows local build:

```powershell
winget install --id MiKTeX.MiKTeX --exact --accept-package-agreements --accept-source-agreements
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Run `latexmk` from the `paper/` directory. The expected review artifact is `main.pdf`.

## Status / division of labor

- The evidence-backed prose draft and all six figures are present.
- Every numerical claim remains sourced from a named `results/` artifact in an adjacent LaTeX comment.
- The review draft omits Aasa's unknown email rather than inventing it.
- Aasa must review the game-theory wording and sign off on the exploratory T9 learning rule.
- Bibliography metadata for `varsamis2025` and the Flitney year/key discrepancy remains a pre-submission check.
- Table II reports the registration-source hardware execution; `figs/hardware_scaling.pdf` is a two-execution aggregate from one recorded calibration day.
- Cross-day hardware repeats and the resulting uncertainty update remain in progress.
- See `REVIEW-NOTES.md` for the complete pre-submission checklist.
````

Retain the accurate figure source list, but remove the stale sentence claiming the gamma-sweep prose and star figure remain unwritten.

- [ ] **Step 4: Run static metadata checks**

Run:

```bash
python - <<'PY'
from pathlib import Path

tex = Path("paper/main.tex").read_text(encoding="utf-8")
bib = Path("paper/references.bib").read_text(encoding="utf-8")
readme = Path("paper/README.md").read_text(encoding="utf-8")
notes = Path("paper/REVIEW-NOTES.md").read_text(encoding="utf-8")
assert "TODO:" not in tex
assert "TODO:" not in bib
assert "gamma-sweep prose and star per-player figure" not in readme
for required in [
    "Aasa Singh Bhui's preferred publication email",
    "3--5 distinct calibration-day executions",
    "submission-time calibration snapshot",
    "W-topology/wiring-permutation hardware control",
    "IEEE QCE submission category",
]:
    assert required in notes, required
print("review metadata checks passed")
PY
```

Expected: `review metadata checks passed`.

- [ ] **Step 5: Review checkpoint**

Run:

```bash
git diff --check -- paper/references.bib paper/README.md paper/REVIEW-NOTES.md
git diff -- paper/references.bib paper/README.md paper/REVIEW-NOTES.md
```

Expected: no whitespace errors and no fabricated metadata.

---

### Task 4: Install MiKTeX and compile the IEEE review PDF

**Files:**
- Generate: `paper/main.pdf`
- Generate temporarily: `paper/main.aux`, `paper/main.bbl`, `paper/main.blg`, `paper/main.fdb_latexmk`, `paper/main.fls`, `paper/main.log`, `paper/main.out`

**Interfaces:**
- Consumes: Corrected `main.tex`, `references.bib`, and existing `paper/figs/` assets.
- Produces: A compiled IEEE two-column PDF and a build log for verification.

- [ ] **Step 1: Install the approved MiKTeX distribution**

Run in PowerShell:

```powershell
winget install --id MiKTeX.MiKTeX --exact --accept-package-agreements --accept-source-agreements
```

Expected: winget reports MiKTeX 25.12 installed successfully or already installed.

- [ ] **Step 2: Start a fresh shell and verify the compiler commands**

Run:

```powershell
latexmk --version
pdflatex --version
bibtex --version
```

Expected: all three commands exit successfully. If the current shell has stale `PATH`, start a new PowerShell process before retrying; do not reinstall immediately.

- [ ] **Step 3: Install missing LaTeX packages through MiKTeX if the first build requests them**

From `paper/`, run:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Expected first-pass outcomes:

- Success, or
- MiKTeX identifies a specific missing package. Install only that named package through MiKTeX Console/package manager, then rerun the same command.

Do not change manuscript source to work around a missing standard package.

- [ ] **Step 4: Run a clean final build**

Run from `paper/`:

```powershell
latexmk -C main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Expected: exit code 0 and `paper/main.pdf` exists with a nonzero size.

- [ ] **Step 5: Verify the log has no unresolved references or citations**

Run from the repository root:

```bash
python - <<'PY'
from pathlib import Path

log = Path("paper/main.log").read_text(encoding="utf-8", errors="replace")
fatal = [
    "Undefined control sequence",
    "LaTeX Error:",
    "Citation `",
    "There were undefined references",
    "Rerun to get cross-references right",
]
found = [token for token in fatal if token in log]
assert not found, f"build log contains: {found}"
pdf = Path("paper/main.pdf")
assert pdf.is_file() and pdf.stat().st_size > 0
print(f"clean build: {pdf.stat().st_size} bytes")
PY
```

Expected: `clean build: <positive number> bytes`.

- [ ] **Step 6: Report layout warnings without silently ignoring them**

Run:

```bash
python - <<'PY'
from pathlib import Path

log = Path("paper/main.log").read_text(encoding="utf-8", errors="replace")
for line in log.splitlines():
    if "Overfull \\hbox" in line or "Overfull \\vbox" in line or "Underfull \\hbox" in line:
        print(line)
PY
```

Expected: either no output or a bounded warning list to inspect against the PDF. Fix only warnings that cause visible overlap, clipping, or unreadable layout.

---

### Task 5: Verify the PDF visually and run repository checks

**Files:**
- Inspect: `paper/main.pdf`
- Inspect: `paper/main.log`
- Test: `tests/test_doc_anchors.py`

**Interfaces:**
- Consumes: The compiled review artifact from Task 4.
- Produces: Verified evidence that the PDF is readable, free of visible placeholders, and compatible with repository documentation checks.

- [ ] **Step 1: Determine the PDF page count**

Read `paper/main.pdf` with the PDF reader. Record the page count reported by the reader.

Expected: at least one page and no PDF parsing error.

- [ ] **Step 2: Inspect every PDF page**

Read all pages in batches of no more than 20 pages. Check:

- title and both author names render;
- no red placeholder appears in the author block;
- abstract and keywords fit the first page;
- equations do not cross columns;
- all six figures render with readable captions;
- Table II fits its column;
- the two-column flow has no accidental blank page;
- references render without printable metadata notes;
- no `??` appears in cross-references;
- no figure, caption, or equation is clipped.

Expected: no visual blocker. If a visible blocker exists, make the smallest LaTeX layout correction and repeat Tasks 4.4 through 5.2.

- [ ] **Step 3: Run the anchored-document regression test**

Run from the repository root:

```bash
conda run -n entangled-equilibria python -m pytest tests/test_doc_anchors.py -q
```

Expected: PASS.

- [ ] **Step 4: Run the full repository test suite**

Run:

```bash
conda run -n entangled-equilibria python -m pytest -q
```

Expected: all tests pass, with only the repository's documented skips. If a failure is unrelated to the paper diff, report it with exact output rather than changing unrelated code.

- [ ] **Step 5: Verify the final diff is limited to the approved scope**

Run:

```bash
git status --short
git diff --check
git diff --stat
git diff -- paper/main.tex paper/references.bib paper/README.md paper/REVIEW-NOTES.md
```

Expected intentional files:

```text
paper/main.tex
paper/references.bib
paper/README.md
paper/REVIEW-NOTES.md
paper/main.pdf
```

Build auxiliaries must remain ignored or be removed before handoff. No file under `results/`, `src/`, `experiments/`, `scripts/`, or `paper/figs/` may change.

- [ ] **Step 6: Final evidence report**

Report:

- PDF path and page count;
- MiKTeX and latexmk versions;
- build command and exit status;
- unresolved-reference/citation scan result;
- visual-inspection result;
- anchored-document and full-suite test results;
- exact modified files;
- remaining items from `paper/REVIEW-NOTES.md`;
- explicit statement that no numerical result was added, recomputed, or fabricated.

Do not call the paper submission-ready. Call it an IEEE-formatted review draft.
