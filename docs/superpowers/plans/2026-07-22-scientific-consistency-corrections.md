# Scientific Consistency Corrections Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an evidence-consistent IEEE review draft by correcting the 15 verified scientific issues without recomputing results, replacing figures, or changing research code.

**Architecture:** Preserve every existing result artifact and all six manuscript figures. Reframe simulation plots and thresholds as comparisons against the circuit-evaluated restricted `{D,H}` equilibrium used by `src/game/nash.py`, while retaining the hardware metric against the analytic noiseless all-Hawk payoff `1/N`. Apply surgical wording corrections for strategy-domain scope, topology scope, hardware provenance, uncertainty semantics, registration timing, payoff mechanics, and model interpretation, then rebuild and inspect the PDF.

**Tech Stack:** IEEEtran LaTeX, BibTeX, MiKTeX, Python standard-library static checks, Conda environment `entangled-equilibria`, pytest.

## Global Constraints

- Work in the existing dirty `dev` tree; preserve all pre-existing user changes.
- Do not create a worktree.
- Do not commit or push.
- Modify only `paper/main.tex`, `paper/README.md`, `paper/REVIEW-NOTES.md`, generated LaTeX build outputs, and this plan/progress scratch state.
- Do not modify `src/`, `tests/`, `results/`, `scripts/`, `experiments/`, `paper/figs/`, bibliography records, or historical findings/status records.
- Do not generate or recompute simulation or hardware data.
- Do not redesign or replace any of the six existing figures.
- Preserve the live parameters `V=4`, `C=3`.
- Preserve all existing bibliography corrections and DOI metadata.
- Preserve the distinction that `N=4,5` hardware points are a fixed cooperative protocol, not certified equilibria.
- Replace every unqualified Nash claim for `Q_N` with a claim restricted to the finite menu `{D,H,Q_N}`; full-SU(2) equilibrium is not established.
- For simulation artifacts, define the plotted quantity as mean fixed-profile payoff minus the highest-mean pure equilibrium of the circuit-evaluated restricted `{D,H}` game under the same topology/noise.
- For hardware artifacts, define advantage as measured cooperative-profile payoff minus the analytic noiseless all-Hawk payoff `1/N`.
- Treat the T9 adaptation result as an exploratory W, `N=4`, finite-round pilot only.
- Treat per-player hardware analyses and repeated N=5 deficit sign as observational, not preregistered acceptance tests.
- Treat the two scaling executions as same-recorded-calibration executions, not cross-day replication.
- Call the CZ-exponential result the lowest-scoring registered candidate, not an operative physical law.
- If a statement cannot be reconciled from existing evidence, weaken or remove it rather than guessing.

---

### Task 1: Correct Simulation Metrics, Equilibrium Scope, and Topology Claims

**Files:**
- Modify: `paper/main.tex:28-399`
- Read: `.superpowers/sdd/scientific-claims-verification.md`
- Read: `src/game/nash.py`
- Read: `docs/formulae.md`
- Read: `results/n-scaling-advantage/2026-07-19T0901Z/report.md`
- Read: `docs/findings/2026-07-16-topology-vs-implementation-controls.md`
- Read: `docs/findings/2026-07-05-t9-adaptation-fairness.md`

**Interfaces:**
- Consumes: Existing simulation artifacts and the user-approved decision to preserve them.
- Produces: A manuscript whose simulation quantity, strategy domain, topology scope, gamma-zero interpretation, per-gate range, and adaptation scope match the recorded evidence.

- [ ] **Step 1: Add a two-metric definition before the simulation results**

Replace the current `Advantage metric and honesty conventions` subsection with wording that states both estimands explicitly:

```latex
\subsection{Payoff-gap metrics and honesty conventions}
The simulation artifacts report a \emph{circuit-relative payoff gap}: the mean
payoff of the fixed profile $(Q_N,\dots,Q_N)$ minus the highest-mean pure
Nash payoff found in the restricted $\{D,H\}^N$ game after those classical
labels pass through the same entangler and, where applicable, the same noisy
circuit. This comparator is topology- and noise-dependent. The hardware
sections instead report \emph{analytic-baseline advantage}: measured mean
cooperative-profile payoff minus the noiseless all-Hawk payoff
$(V-C)/N=1/N$ of the original classical game. We keep the two quantities
separate and do not compare their zero crossings directly.

Equilibrium status is also restricted: ``Nash'' below means no profitable
unilateral deviation within the finite menu $\{D,H,Q_N\}$, not equilibrium
against arbitrary SU(2) gates. Under noise the mean over players can hide
per-player losses; we therefore report per-player vectors alongside means.
Per-player hardware breakdowns are diagnostic analyses added after
registration; they are not part of the registered acceptance test.
```

- [ ] **Step 2: Normalize abstract and contribution language**

Revise the abstract and contribution list so they say:

- For the GHZ entangler, fixed `Q_N` pays exactly `V/N`; other topologies are evaluated cell by cell and may or may not attain it.
- The profile passes the restricted `{D,H,Q_N}` deviation check at GHZ `N=2,3`; it is not claimed to be a full-SU(2) equilibrium.
- Do not call GHZ the only topology passing the restricted check at small N; ring and fully connected also pass at `N=3` in the fixed-mode artifact.
- Replace topology-wide “Nash equilibrium” summaries with “restricted-menu equilibrium” or “passes the restricted deviation check.”
- Describe W as a per-gate-retention outlier without claiming the matched-count study eliminates all absolute payoff ordering.
- Replace the adaptation headline with: `In an exploratory W N=4 finite-round pilot, no tested setting produced a beneficial converged fairness repair.`

- [ ] **Step 3: Correct the zero-noise landscape prose and captions**

Apply these exact scientific constraints:

- Replace `GHZ-family cooperative profile ... pays exactly V/N` with `For GHZ, the fixed profile pays exactly V/N`; describe each non-GHZ topology from the recorded cells.
- Keep ring `N=4` payoff-gap zero and star `N=6` deviation, but call the ring point `an N=4 interference zero`; remove `period-4` and any unverified recurrence implication.
- Retain the separate GHZ `N=2..8` deviation-formula check only if provenance names `docs/VERIFIED-FACTS.md` as a separate computation; do not attribute `N=7,8` to the `2026-07-19T0901Z` topology artifact.
- In Figure `fig:advmap`, define the y-axis quantity in the caption as the circuit-relative payoff gap. Replace `the fully symmetric case holds only at N<=3` with a cell-specific statement: filled markers indicate passing the restricted `{D,H,Q_N}` check, which depends on topology.
- In Figure `fig:heat`, replace `classical pure Nash payoff` with `circuit-evaluated restricted {D,H} equilibrium payoff`.
- In the star section, call all values circuit-relative payoff gaps.

- [ ] **Step 4: Correct the gamma-sweep interpretation**

Replace the opening gamma-sweep interpretation with wording equivalent to:

```latex
Sweeping $\gamma$ separates a cooperative payoff gap from an
entanglement-enabled restricted-menu equilibrium. At $\gamma=0$, $J=I$ and
the phase-only $Q_N$ profile is measurement-equivalent to all-Dove: its
positive payoff gap over all-Hawk is classical in outcome probabilities and
the profile does not pass the restricted deviation check. At nonzero
$\gamma$, the same sweep records when the fixed profile begins to pass that
finite-menu check.
```

Keep the recorded cell values, but replace every `pure Nash equilibrium` in this paragraph and Figure `fig:gamma` with `restricted-menu equilibrium` or `passes the restricted deviation check`.

- [ ] **Step 5: Correct noise-robustness metric and per-gate claims**

- Rename noise `advantage-zero crossings` as `circuit-relative payoff-gap zero crossings`.
- Explain that comparator drift in the noisy restricted `{D,H}` circuit game can drive these crossings; they are not crossings relative to analytic `1/N`.
- Remove the false sentence that ring is never a restricted pure equilibrium at `p=0`; the fixed-mode artifact records ring as passing at `N=2,3`.
- Change the XX-family normalized range from `2.1--2.7` to approximately `1.8--2.7`.
- Replace `indistinguishable` with `similar in the control table`; no statistical equivalence test was recorded.
- State that matched-count controls reduce gate-budget confounding within the XX family, while absolute GHZ-W ordering can remain because zero-noise payoff gaps differ.
- Keep W at approximately `0.8--1.0` per CX and describe it as the normalized-retention outlier.

- [ ] **Step 6: Narrow the adaptation pilot**

Replace the adaptation result with this scope:

```latex
An exploratory W-state pilot at $N=4$ tested one provisional independent
round-robin best-response rule. No tested setting produced a beneficial
converged fairness repair: at $p=0$ the dynamics reached the 50-round cap
near mean $0.51$ without converging; at $p=0.02$ they entered a payoff limit
cycle with lower mean and larger spread; and at $p=0.05$ they converged with
little change. The pilot does not test the W $N=5$ negative-player cells or
the ring $N=5$ wiring case, and it remains pending game-theory sign-off.
```

Remove claims that the `p=0` endpoint definitively equalized or that adaptation was tested across the headline W/ring systems.

- [ ] **Step 7: Add and run a task-specific static check**

Run from the repository root:

```bash
conda run -n entangled-equilibria python - <<'PY'
from pathlib import Path
tex = Path('paper/main.tex').read_text(encoding='utf-8')
required = [
    'circuit-relative payoff gap',
    'analytic-baseline advantage',
    'finite menu $\\{D,H,Q_N\\}$',
    'an $N{=}4$ ring interference zero',
    '50-round cap',
    'approximately 1.8',
]
for text in required:
    assert text in tex, text
for banned in [
    'period-4 interference',
    'indistinguishable across GHZ/ring/star/fully-connected',
    'For W and ring the fixed GHZ-derived $Q$ is never',
]:
    assert banned not in tex, banned
print('simulation consistency checks passed')
PY
```

Expected: `simulation consistency checks passed`.

- [ ] **Step 8: Review the diff without committing**

Run:

```bash
git diff --check -- paper/main.tex
git diff -- paper/main.tex
```

Expected: no whitespace errors; no files outside the approved scope changed by this task.

---

### Task 2: Correct Hardware Provenance, Statistics, and Mechanism Claims

**Files:**
- Modify: `paper/main.tex:400-638`
- Modify: `paper/REVIEW-NOTES.md`
- Modify: `paper/README.md`
- Read: `results/hardware-n3/2026-07-16T013912Z/result.json`
- Read: `results/hardware-n3/2026-07-16T013912Z/calibration.json`
- Read: `results/hardware-scaling/preregistration.json`
- Read: `results/hardware-scaling/preregistration-baselines.json`
- Read: `results/hardware-scaling/repeat-judgments.json`
- Read: `scripts/plot_hardware_scaling.py`

**Interfaces:**
- Consumes: The two-metric terminology established in Task 1.
- Produces: Hardware prose and captions with correct chain/calibration scope, quantity labels, uncertainty semantics, endpoint definitions, payoff mechanism, and model-strength claims.

- [ ] **Step 1: Correct the N=3 error-budget interpretation**

Replace the current `consistent with an independent-error picture` paragraph with wording equivalent to:

```latex
A product of the recorded readout and two-qubit fidelities gives a heuristic
ground-state probability of about $0.977$, whereas the measured value is
$3911/4096=0.955$. Under a fixed binomial interpretation the difference is
about $9.5$ standard deviations, so the product has the right order of
magnitude but substantially underpredicts non-ground weight; it is not a
calibrated statistical model of this execution.
```

Keep the recorded calibration values and the four-plus-two CZ split only as the arithmetic source, not as a consistency claim.

- [ ] **Step 2: Correct the `0.9978` quantity label**

Use this exact distinction:

```latex
The measured mean payoff is $1.3311$, or $99.835\%$ of the ideal payoff
$4/3$; subtracting the analytic all-Hawk baseline $1/3$ gives measured
advantage $0.9978$, or $99.780\%$ of the ideal advantage $1.0$.
```

- [ ] **Step 3: Correct the payoff-loss mechanism**

State the exact identity:

```latex
For every outcome with $0<k<N$ Hawks, total payoff remains $V$, so the mean
remains $V/N$. Only the all-Hawk outcome lowers total payoff to $V-C$:
\begin{equation}
\overline{\pi}=\frac{V}{N}-\frac{C}{N}P(1\ldots1).
\end{equation}
```

Replace every claim that generic `>=2`-Hawk outcomes reduce the mean. Do not claim that ZNE improves the mean by specifically suppressing CZ-created all-Hawk population unless a recorded population analysis supports it.

- [ ] **Step 4: Correct the scaling figure caption uncertainty**

For the existing two-run figure, replace the current error-bar sentence with:

```latex
Error bars show the sample standard deviation across the two
same-recorded-calibration execution estimates; they do not include the
within-run multinomial or weighted-fit standard errors and are not a
cross-day uncertainty estimate.
```

Do not alter or regenerate the figure.

- [ ] **Step 5: Separate fold-1 and ZNE model endpoints**

State all four source-run values explicitly and label their roles:

```latex
For the registration-source execution, the registered primary
mitigated-fold-1 endpoint misses at $N=4$ by $0.0043$ ($2.14\sigma$) and at
$N=5$ by $0.0101$ ($5.17\sigma$). These source-run residuals are
retrospective because the registration was written after that execution.
For the displayed ZNE endpoint, the corresponding misses are $0.0041$
($2.07\sigma$) and $0.0060$ ($3.05\sigma$). The second execution is the
prospective registered repeat: its conditional $N=4$ endpoint passes and
its $N=5$ endpoint misses by $0.0092$ ($4.74\sigma$). The repeated deficit
sign is observational, not a registered sign test.
```

Remove `matches N=4` language for the source run because the registered 95% test failed narrowly.

- [ ] **Step 6: Weaken the model-ranking inference**

Replace `operative scaling law`, `physical interpretation`, and equivalent causal language with:

```latex
The CZ-exponential baseline is the lowest-scoring of the five registered
candidates in both same-recorded-calibration executions. It nevertheless
misses $N=5$ outside the shared 95\% comparison yardstick in both runs; that
yardstick is for ranking, not a model-specific calibrated interval.
Cross-day executions and model-specific predictive uncertainties are needed
before interpreting the ranking as a physical scaling law.
```

- [ ] **Step 7: Correct chain and calibration scope**

- Keep the scaling subsection's one-chain statement, scoped to the N=3,4,5 scaling series.
- Replace any whole-paper `one device, one chain, one calibration day` statement with: `The scaling series uses chain [59,75,74,73,79] and one recorded calibration snapshot; the separate N=3 validation used [136,143,142] and the preceding recorded calibration date.`
- Describe the two scaling runs as carrying the same recorded result-write-time calibration snapshot. Do not claim this proves they executed under the same provider calibration.

- [ ] **Step 8: Replace the unqualified `~3x` statement**

Use `several times faster` without a number. If a quantified note remains, define it as `about 3.7x for the N=3 to N=5 raw-retention drop` or `about 5.6x using ZNE retention`; do not present `3x` as a per-cell ratio.

- [ ] **Step 9: Update paper-facing status notes**

Add to `paper/REVIEW-NOTES.md`:

- Full-SU(2) equilibrium is not established; current claims are restricted to `{D,H,Q_N}`.
- Simulation payoff gaps use a circuit-evaluated restricted `{D,H}` comparator, while hardware uses analytic `1/N`.
- The two scaling executions provide same-recorded-calibration repeatability only; cross-day runs remain pending.
- Existing Figure 6 error bars are two-point sample SD and do not include within-run uncertainty; a future cross-day figure should separate within-run and between-day uncertainty.

Update `paper/README.md` status with the same two-metric and restricted-equilibrium definitions. Do not call the paper submission-ready.

- [ ] **Step 10: Run a hardware-claim static check**

Run:

```bash
conda run -n entangled-equilibria python - <<'PY'
from pathlib import Path
tex = Path('paper/main.tex').read_text(encoding='utf-8')
for text in [
    'about $9.5$ standard deviations',
    '$99.835\\%$ of the ideal payoff',
    'sample standard deviation across the two',
    'retrospective because the registration was written after that execution',
    'lowest-scoring of the five registered candidates',
    'Only the all-Hawk outcome',
]:
    assert text in tex, text
for banned in [
    'operative scaling law',
    'Ground-state probability decays $\\sim$3$\\times$',
    'correlated cz errors that create $\\ge$2-Hawk outcomes',
    "the same run's mean payoff is $0.9978$ of ideal",
]:
    assert banned not in tex, banned
print('hardware consistency checks passed')
PY
```

Expected: `hardware consistency checks passed`.

- [ ] **Step 11: Review the task diff without committing**

Run:

```bash
git diff --check -- paper/main.tex paper/README.md paper/REVIEW-NOTES.md
git diff -- paper/main.tex paper/README.md paper/REVIEW-NOTES.md
```

Expected: no whitespace errors; no result/source/figure files changed.

---

### Task 3: Build and Verify the Corrected Review PDF

**Files:**
- Generate: `paper/main.pdf`
- Generate: `paper/main.aux`, `paper/main.bbl`, `paper/main.blg`, `paper/main.log`, `paper/main.out`
- Inspect: `paper/main.pdf`
- Test: `tests/test_doc_anchors.py`

**Interfaces:**
- Consumes: Corrected paper source and unchanged figures/results.
- Produces: A rebuilt IEEE review PDF plus an honest verification report.

- [ ] **Step 1: Run consolidated source assertions**

Run from the repository root:

```bash
conda run -n entangled-equilibria python - <<'PY'
from pathlib import Path
tex = Path('paper/main.tex').read_text(encoding='utf-8')
assert 'circuit-relative payoff gap' in tex
assert 'analytic-baseline advantage' in tex
assert 'finite menu $\\{D,H,Q_N\\}$' in tex
assert 'period-4 interference' not in tex
assert 'operative scaling law' not in tex
assert 'Error bars show the sample standard deviation' in tex
assert 'Only the all-Hawk outcome' in tex
assert '\\todo{' not in tex
print('consolidated manuscript checks passed')
PY
```

Expected: `consolidated manuscript checks passed`.

- [ ] **Step 2: Run a clean MiKTeX build**

From `paper/`, run:

```powershell
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error main.tex
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error main.tex
```

Expected: all commands exit 0 and `paper/main.pdf` has nonzero size.

- [ ] **Step 3: Scan the build log**

Run:

```bash
conda run -n entangled-equilibria python - <<'PY'
from pathlib import Path
log = Path('paper/main.log').read_text(encoding='utf-8', errors='replace')
fatal = [
    'Undefined control sequence',
    'LaTeX Error:',
    'Citation `',
    'There were undefined references',
    'Rerun to get cross-references right',
]
found = [token for token in fatal if token in log]
assert not found, found
pdf = Path('paper/main.pdf')
assert pdf.is_file() and pdf.stat().st_size > 0
print('clean build', pdf.stat().st_size)
for line in log.splitlines():
    if 'Overfull \\hbox' in line or 'Overfull \\vbox' in line:
        print(line)
PY
```

Expected: clean build line and no unresolved-reference/citation tokens. Any overfull warning must be checked visually.

- [ ] **Step 4: Inspect all PDF pages**

Read every page of `paper/main.pdf`. Confirm:

- title and author blocks render;
- abstract and keywords fit;
- all six figures render;
- revised captions fit and remain readable;
- equation for the all-Hawk mean mechanism fits its column;
- no `??`, clipped text, blank page, or severe overlap appears;
- references remain intact.

- [ ] **Step 5: Run the anchored-document regression test**

Run:

```bash
conda run -n entangled-equilibria python -m pytest tests/test_doc_anchors.py -q
```

Expected current repository state: 27 pre-existing stale-anchor failures, 136 passes, 3 skips. If the failure set changes or includes paper files, stop and investigate.

- [ ] **Step 6: Run targeted paper/source checks**

Run:

```bash
git diff --check -- paper/main.tex paper/README.md paper/REVIEW-NOTES.md
conda run -n entangled-equilibria python -m pytest tests/test_nash_advantage.py tests/test_strategy_opt.py -q
```

Expected: no diff whitespace errors; game-theory tests pass. These tests verify existing implementation behavior only and do not certify full-SU(2) equilibrium.

- [ ] **Step 7: Verify scope**

Run:

```bash
git status --short
git diff --name-only
```

Expected new intentional source modifications from this pass are limited to:

```text
paper/main.tex
paper/README.md
paper/REVIEW-NOTES.md
docs/superpowers/plans/2026-07-22-scientific-consistency-corrections.md
```

Existing gamma-sweep changes and build artifacts may still appear from the prior session; do not modify or claim ownership of them.

- [ ] **Step 8: Produce final evidence report**

Report:

- exact modified files;
- which of the 15 findings were corrected by wording versus clarified by scope;
- PDF page count and build status;
- citation/reference scan result;
- visual inspection result;
- targeted test results;
- the unchanged 27 stale-anchor failure concern;
- explicit statement that no result artifact, research code, experiment, script, or figure was changed or regenerated;
- remaining author/hardware items from `paper/REVIEW-NOTES.md`.

Do not call the manuscript submission-ready. Call it an evidence-consistent IEEE review draft.
