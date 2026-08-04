# QHD Mathematical Framework Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Version:** v3 — revised after engineering review: TQE manuscript shell migration added as Task 1, entangler-family vocabulary and $P(0^N)$ renaming adopted, general-$\gamma$ cooperative proposition added, $\lambda$ symbol collision fixed ($\eta$ depolarizing, $s$ fold scale), exhaustive payoff-tensor test, Dove-deviation and permutation-covariance coverage, existing-test reuse mandated, semantic anchors replace authoritative line numbers, execution log added, gates G1--G5 confirmed.

> **Execution status (2026-08-04):** Tasks 1–12 and Gates G1–G3 are complete at checkpoint commit `86495d7`. Resume at Task 13 only. The unchecked boxes below are the original executable specification, not current completion tracking. Use `paper/SECTION-III-EXECUTION-LOG.md` and `docs/QHD-TASK12-HANDOFF.md` for the durable completion record.

**Goal:** Establish a verified terminology, citation, style, and mathematical foundation for the QHD paper, then rewrite Section III one subsection at a time with the five authorized approval gates and a mandatory section-level flow pass.

**Architecture:** This is the first execution plan derived from `docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md` (v3). It covers the TQE shell migration, the dependency-setting work, and Section III. Each subsection follows the same evidence chain: define its reader question, verify formulas against code or symbolic derivation, add only verified peer-reviewed citations, edit `paper/qhd.tex` following `paper/STYLE-GUIDE.md`, and compile in an isolated build directory. User approval happens at five gates: (G1) shell migration + baseline + terminology + style guide, (G2) literature audit, (G3) first drafted subsection III-A for style calibration, (G4) the high-stakes III-G derivation, (G5) the complete Section III after its flow pass. Sections IV--VIII and the figure redesign receive separate plans only after Section III is approved.

**Tech Stack:** LaTeX (official IEEE TQE template), BibTeX, Python 3.10+, NumPy, Qiskit 1.3.2, pytest, MiKTeX/pdfTeX, Crossref/publisher DOI records, existing QHD simulation code.

## Global Constraints

- Target venue: IEEE Transactions on Quantum Engineering — official TQE journal shell (migrated in Task 1), approximately 16--20 pages including appendices; every equation, matrix, and table must fit one column unless deliberately set as a `figure*`/`table*` float.
- Target reader: mixed technical reader with undergraduate linear algebra, probability, and basic quantum-computing knowledge.
- Every drafted paragraph must comply with `paper/STYLE-GUIDE.md` (created in Task 3).
- Vocabulary is binding per spec Sections 3.2--3.3: "entangler family" for the five-way comparison; "graph topology" only for ring, star, complete; $P(0^N)$ is the "all-zero target-state population" (shorthand "target-state population"); "ground-state population" and unsupported "state fidelity" are banned.
- Symbol discipline is binding per spec III-H: $\eta$ depolarizing probability, $s$ ZNE fold scale, $\gamma$ entanglement angle; no symbol defined twice.
- Reuse existing scientific tests as evidence; add only missing checks. Do not duplicate behavior already protected by `tests/test_topologies.py`, `tests/test_ne_guard.py`, `tests/test_asymmetric_advantage.py`, `tests/test_hardware_mitigation.py`, or `tests/test_noise.py`.
- File references in this plan use semantic anchors (LaTeX `\section`/`\label` boundaries, function names); any line numbers given are non-authoritative navigation hints.
- Every task records commands, test results, warnings, page counts, evidence classifications, and approved exceptions in `paper/SECTION-III-EXECUTION-LOG.md`.
- Keep every central mathematical definition and derivation in the main manuscript.
- Final bibliography target: more than 50 relevant, verified, peer-reviewed sources meeting the spec 10.2 locator standard; Section III citations must be authoritative primary sources wherever available.
- Preserve the Theory → Simulation → Hardware narrative.
- Do not alter or generate figures during this plan; the figure redesign (spec Section 8) is a separate plan.
- Do not run new IBM hardware jobs.
- Do not strengthen restricted-menu equilibrium into full-SU(2) equilibrium.
- Keep the player payoff vector as primary evidence; fairness scalars are summaries.
- Distinguish analytic-baseline advantage from circuit-relative payoff gap everywhere.
- Distinguish ideal entangler family, compiled circuit, simulated noise, and physical-device noise.
- Never add an unverified citation, DOI, equation, numerical value, or theorem claim.
- If a proposed formula disagrees with code or symbolic verification, stop and show the discrepancy to the user instead of editing the manuscript.
- User approval gates are exactly G1--G5. Between gates, tasks proceed without stopping unless a verification fails; every task records a checkpoint note in the execution log.
- Do not commit unless the user explicitly requests a commit. If requested, stage only the files named in that task.

---

## File Structure

### Files created

- `paper/SECTION-III-EXECUTION-LOG.md` — running record of commands, test results, warnings, page counts, evidence classifications, gate decisions, and approved exceptions.
- `paper/STYLE-GUIDE.md` — the binding prose rules from spec Section 7, checked at every gate.
- `paper/LITERATURE-AUDIT.md` — verified source ledger with research strand, supported claim, peer-review status, DOI/publisher URL, BibTeX key, evidence access, locator, support type, and verification notes.
- `paper/CLAIM-SOURCE-MAP.md` — maps each Section III definition, equation, proposition, and scope caveat to code, data, derivation, tests (existing and new), and citations.
- `tests/test_paper_claims.py` — executable regression checks for the mathematical statements used in Section III that are not already covered elsewhere.
- `tests/test_paper_structure.py` — source-level guards for Section III heading structure and prohibited overclaims.

### Files modified

- `paper/qhd.tex` — the Section III block: everything between `\section{...}\label{sec:model}` and `\section{...}\label{sec:sim}` (currently ~lines 217--371, non-authoritative hint) is replaced with approved subsections III-A through III-J. Task 1 additionally migrates the preamble/shell.
- `paper/main.tex` — becomes a thin wrapper or is removed (Task 1, user decision).
- `paper/README.md` — updated to name TQE and build `qhd.tex` (Task 1).
- `paper/references.bib` — add only verified peer-reviewed sources used by Section III.

### Files read as evidence

- `src/game/payoffs.py`
- `src/game/nash.py`
- `src/circuits/ewl.py`
- `src/circuits/n_player.py`
- `src/circuits/topologies.py`
- `src/circuits/topology_graphs.py`
- `src/hardware/mitigation.py` (independence-assumption comment near the top of the assignment-matrix code)
- `tests/test_topologies.py`, `tests/test_ne_guard.py`, `tests/test_asymmetric_advantage.py`, `tests/test_hardware_mitigation.py`, `tests/test_noise.py`
- `docs/VERIFIED-FACTS.md`
- `docs/formulae.md`
- `docs/findings/2026-07-16-topology-vs-implementation-controls.md`
- `docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md`

### Existing-test reuse map

| Claim | Existing authoritative test | This plan adds |
|---|---|---|
| Entangler unitarity and $C_3=K_3$ | `tests/test_topologies.py` (unitarity/coincidence block) | nothing — referenced in CLAIM-SOURCE-MAP |
| GHZ equilibrium boundary and Hawk values | `tests/test_ne_guard.py` (boundary block) | nothing — referenced in CLAIM-SOURCE-MAP |
| Star hub/leaf asymmetry | `tests/test_asymmetric_advantage.py` | general relabeling covariance only |
| Readout reconstruction and weighted ZNE | `tests/test_hardware_mitigation.py` | nothing — referenced in CLAIM-SOURCE-MAP |
| Noise-model instruction attachment | `tests/test_noise.py` | nothing — referenced in CLAIM-SOURCE-MAP |

---

### Task 1: TQE Journal Shell and Canonical Manuscript Entry

**Files:**
- Modify: `paper/qhd.tex` (preamble only — documentclass and TQE-required front matter)
- Modify or delete: `paper/main.tex`
- Modify: `paper/README.md`
- Create: `paper/SECTION-III-EXECUTION-LOG.md`
- Read: `paper/qhd.tex`, `paper/main.tex`

**Interfaces:**
- Consumes: the two current manuscript entry points and the IEEE Author Center TQE template.
- Produces: one canonical TQE-shell manuscript (`paper/qhd.tex`), a resolved fate for `main.tex`, an accurate README, and the execution log used by every later task.

- [ ] **Step 1: Create the execution log**

Write the header of `paper/SECTION-III-EXECUTION-LOG.md`:

```markdown
# Section III Execution Log

One entry per task: date, commands run, test results, new warnings,
page count, evidence classifications, gate decisions, approved exceptions.
```

- [ ] **Step 2: Diff the two manuscript entry points before touching either**

Run:

```bash
diff paper/main.tex paper/qhd.tex > paper/.main-vs-qhd.diff; wc -l paper/.main-vs-qhd.diff
```

If the files diverge in *content* (not just preamble), STOP and present the divergence to the user — someone must decide which prose wins before migration, so verified content does not silently disappear. Record the decision in the execution log. Delete `paper/.main-vs-qhd.diff` afterwards.

- [ ] **Step 3: Obtain the official TQE template**

Download the IEEE TQE LaTeX template from the IEEE Author Center / IEEE Template Selector. Record the template version and source URL in the execution log. Do not guess the documentclass options — copy them from the official template.

- [ ] **Step 4: Migrate the `qhd.tex` preamble**

Replace `\documentclass[conference]{IEEEtran}` and any conference-only front matter with the official TQE journal setup from the template. Change nothing in the body prose in this task. Preserve all packages the body actually uses.

- [ ] **Step 5: Resolve the competing entry point**

Convert `paper/main.tex` into a thin wrapper:

```latex
% Deprecated entry point. The canonical manuscript is qhd.tex.
\input{qhd.tex}
```

or delete it if the user prefers (ask at G1 if the diff in Step 2 was clean; deletion is the simpler end state).

- [ ] **Step 6: Update `paper/README.md`**

Replace the IEEE QCE framing and `main.tex` build commands with the TQE target and:

```bash
pdflatex -interaction=nonstopmode -halt-on-error qhd.tex
bibtex qhd
pdflatex -interaction=nonstopmode -halt-on-error qhd.tex
pdflatex -interaction=nonstopmode -halt-on-error qhd.tex
```

- [ ] **Step 7: Verify the migrated shell builds**

Run the four-pass build from Task 2 Step 2 (non-destructive, `.qhd-build-check`). Expected: exit code 0. Record any *new* warnings versus the pre-migration build in the execution log.

---

### Task 2: Establish the Baseline and Non-Destructive Build Gate

**Files:**
- Read: `paper/qhd.tex`
- Read: `paper/references.bib`
- Read: `paper/figs/*`
- Modify: `paper/SECTION-III-EXECUTION-LOG.md`
- Create during verification only: `paper/.qhd-build-check/*`

**Interfaces:**
- Consumes: the migrated TQE-shell manuscript, bibliography, and figure directory.
- Produces: a recorded baseline build result and a repeatable non-destructive build command used by every later task.

- [ ] **Step 1: Record the starting state**

Run:

```bash
git status --short -- paper/qhd.tex paper/main.tex paper/README.md paper/references.bib paper/figs
```

- [ ] **Step 2: Build without overwriting `paper/qhd.pdf`**

Run from `paper/`:

```bash
rm -rf .qhd-build-check
mkdir .qhd-build-check
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex
bibtex .qhd-build-check/qhd
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.qhd-build-check qhd.tex
```

Expected: exit code 0 and `.qhd-build-check/qhd.pdf` exists.

Intermediate drafting tasks may use a faster single-pass check when the bibliography and cross-references are unchanged; every gate (G1--G5) requires the full four-pass build.

- [ ] **Step 3: Check the baseline log**

Search `.qhd-build-check/qhd.log` for:

```text
LaTeX Warning
undefined references
Citation .* undefined
Overfull \\hbox
Emergency stop
Fatal error
```

Record existing warnings in the execution log. Later tasks must not introduce new warnings.

- [ ] **Step 4: Record baseline page count**

Run:

```bash
pdfinfo .qhd-build-check/qhd.pdf
```

Record the page count in the execution log.

- [ ] **Step 5: Remove the temporary build directory**

```bash
rm -rf .qhd-build-check
```

- [ ] **Step 6: Checkpoint note**

Record build status, warnings, and page count in the execution log. Do not edit prose in this task. Results are presented at G1 together with Task 1 and Task 3 deliverables.

---

### Task 3: Freeze the Terminology, Style Guide, and Claim-Scope Contract

**Files:**
- Create: `paper/STYLE-GUIDE.md`
- Create: `paper/CLAIM-SOURCE-MAP.md`
- Create: `tests/test_paper_structure.py`
- Modify: `paper/SECTION-III-EXECUTION-LOG.md`
- Read: `paper/qhd.tex` (the metrics subsection inside `\label{sec:model}`)
- Read: `src/game/nash.py` (module docstring and `compute_advantage`)
- Read: `src/game/payoffs.py` (`outcome_payoff`, `expected_payoff`)
- Read: `docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md` (Sections 3.2, 3.3, 7)

**Interfaces:**
- Consumes: current terminology, implemented metric semantics, and spec Sections 3.2/3.3/7.
- Produces: canonical names, definitions, and binding prose rules used by every later subsection.

- [ ] **Step 1: Create the style guide**

Copy spec Section 7 (7.1--7.5) verbatim into `paper/STYLE-GUIDE.md`, prefixed with:

```markdown
# QHD Manuscript Style Guide

Binding for every drafted paragraph. Source of truth: spec Section 7 in
docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md.
Checked at every approval gate; violations are review blockers.
```

- [ ] **Step 2: Create the claim-source map header and terminology table**

Write these canonical entries to `paper/CLAIM-SOURCE-MAP.md`:

```markdown
# QHD Claim and Source Map

| Term | Canonical meaning | Must not be called | Primary implementation/evidence |
|---|---|---|---|
| entangler family | one of GHZ, W, ring, star, complete — the umbrella for five-way comparisons | topology (for the five-way set) | `src/circuits/topologies.py` |
| graph topology | edge structure of the pairwise families ring, star, complete only | — | `src/circuits/topology_graphs.py` |
| cooperative fixed profile | $(Q_N,\ldots,Q_N)$ evaluated without assuming equilibrium | universal quantum Nash equilibrium | `src/circuits/ewl.py:q_strategy`, `src/game/nash.py` |
| restricted-menu equilibrium | no profitable unilateral deviation within $\{D,H,Q_N\}$ | full-SU(2) equilibrium | `src/game/nash.py:find_pure_nash` |
| circuit-relative payoff gap | fixed-profile mean payoff minus the best restricted classical circuit equilibrium under the same family/noise path | analytic hardware advantage | `src/game/nash.py:compute_advantage` |
| analytic-baseline advantage | measured or simulated mean payoff minus $(V-C)/N$ | circuit-relative payoff gap | manuscript/hardware estimand |
| all-zero target-state population | $P(0^N)$; shorthand after definition: target-state population | ground-state population; state fidelity (unless full-state fidelity is computed) | outcome distribution |
| graph position | structural role such as star hub or leaf | player identity or physical qubit | topology and wiring-permutation evidence |
| payoff vector | $(\pi_1,\ldots,\pi_N)$ | scalar mean | `src/game/payoffs.py:expected_payoff` |
| fairness range | $\max_j\pi_j-\min_j\pi_j$ | complete fairness evidence | derived from payoff vector |
| player floor | $\min_j\pi_j$ | mean welfare | derived from payoff vector |

## Canonical symbols

| Symbol | Meaning | Never used for |
|---|---|---|
| $\eta$ | depolarizing probability | fold scale |
| $s$ | ZNE fold scale, $s\in\{1,3,5\}$ | noise strength |
| $\gamma$ | entanglement angle | anything else |
```

- [ ] **Step 3: Add an evidence-class vocabulary**

Add:

```markdown
## Evidence labels

- **Proposition:** proved in the main manuscript and covered by an executable regression check.
- **Computational result:** evaluated over a stated finite parameter range; not presented as a theorem.
- **Simulation result:** produced by the statevector or density-matrix pipeline.
- **Registered hardware result:** acceptance rule written before the execution.
- **Observational hardware result:** measured after execution without a preregistered pass rule.
- **Exploratory result:** provisional analysis that does not support a central claim.
```

- [ ] **Step 4: Add prohibited phrasing and naming guards**

Create `tests/test_paper_structure.py` with:

```python
import re
from pathlib import Path

PAPER = Path("paper/qhd.tex")


def _section_iii_block(text: str) -> str:
    """Section III = everything between \\label{sec:model} and \\label{sec:sim}."""
    start = text.index(r"\label{sec:model}")
    end = text.index(r"\label{sec:sim}")
    return text[start:end]


def test_restricted_equilibrium_is_not_overstated():
    text = PAPER.read_text(encoding="utf-8")
    prohibited = [
        "full SU(2) Nash equilibrium on hardware",
        "unrestricted quantum Nash equilibrium",
        "universal quantum Nash equilibrium",
    ]
    for phrase in prohibited:
        assert phrase not in text


def test_no_hype_adjectives():
    text = PAPER.read_text(encoding="utf-8").lower()
    for word in ["groundbreaking", "remarkable", "surprisingly"]:
        assert word not in text, f"style guide 7.1 bans '{word}'"


def test_section_iii_uses_canonical_target_state_name():
    # Scoped to Section III during Phase 1; later phase plans extend the ban
    # paper-wide as each section is rewritten.
    block = _section_iii_block(PAPER.read_text(encoding="utf-8"))
    assert "ground-state population" not in block
    assert "ground state population" not in block


def test_section_iii_does_not_claim_unsupported_state_fidelity():
    block = _section_iii_block(PAPER.read_text(encoding="utf-8"))
    assert "state fidelity" not in block  # III computes populations, not fidelities
```

If `\label{sec:model}`/`\label{sec:sim}` names change during the rewrite, update `_section_iii_block` in the same edit — the labels are the semantic anchors for this plan.

- [ ] **Step 5: Run the guards**

```bash
python -m pytest tests/test_paper_structure.py -v
```

Expected: PASS, or specific failures identifying pre-existing wording inside the current Section III block; record such failures in the execution log as work items for the relevant subsection task.

- [ ] **Step 6: Gate G1**

Present: the Task 1 migration record (template version, diff resolution, `main.tex` fate), the Task 2 baseline, the terminology and symbol tables, and the style guide. Ask the user to approve the exact canonical names, symbols, and style rules before writing any mathematical subsection. Do not continue past this gate without explicit approval.

---

### Task 4: Create the Section III Literature Audit

**Files:**
- Create: `paper/LITERATURE-AUDIT.md`
- Modify: `paper/references.bib`
- Modify: `paper/SECTION-III-EXECUTION-LOG.md`
- Read: current entries in `paper/references.bib`

**Interfaces:**
- Consumes: authoritative publisher pages, Crossref DOI records, full texts where accessible, and existing bibliography entries.
- Produces: verified references available to III-A through III-J.

- [ ] **Step 1: Create the audit schema (with evidence locators)**

Write:

```markdown
# QHD Literature Audit

| BibTeX key | Research strand | Claim supported | Publication | Year | Peer reviewed | DOI or publisher URL | Evidence access | Locator | Support type | Verification status | Notes |
|---|---|---|---|---:|---|---|---|---|---|---|---|
```

Column semantics:

- **Evidence access:** `full text` / `abstract only`.
- **Locator:** page, section, theorem, figure, or quoted passage that supports the claim.
- **Support type:** `direct` / `contextual` / `criticism`.
- Sources with `abstract only` access must not support detailed mathematical or methodological claims.

- [ ] **Step 2: Audit the existing bibliography**

For every existing BibTeX entry:

1. open the DOI or publisher record;
2. verify title, authors, venue, volume, pages/article number, year, and DOI;
3. record the exact paper claim it supports, the evidence access level, and the locator;
4. mark `verified` only after all fields agree and the locator is recorded.

- [ ] **Step 3: Research the Section III source set (full standard)**

Find primary peer-reviewed sources for:

```text
classical Hawk-Dove and evolutionary games
multiplayer Hawk-Dove payoff formulations
Eisert-Wilkens-Lewenstein quantum games
multiplayer quantum games
GHZ and W multipartite entanglement
graph states and graph automorphisms in quantum networks
quantum-game equilibrium scope and criticism
depolarizing channels and quantum noise
measurement-error mitigation
zero-noise extrapolation and local gate folding
observable-specific error resilience
network games and position-dependent fairness
```

Target at least 18 verified sources for Section III at the full locator standard. **Staging:** remaining strands (for Sections II, V--VII) are audited strand-by-strand in their own phase plans; do not serialize the entire 50+ audit ahead of Section III prose.

- [ ] **Step 4: Add only cited verified entries to `references.bib`**

For each accepted source, add a complete BibTeX entry with DOI. Do not add a source until a planned Section III sentence names the claim it supports.

- [ ] **Step 5: Check BibTeX-key uniqueness**

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

Expected: no duplicate keys.

- [ ] **Step 6: Gate G2**

Present the source list grouped by strand, with evidence access and locators visible. The user approves or removes sources before they are cited in manuscript prose. Do not continue past this gate without explicit approval.

---

### Task 5: Add Classical Payoff and Welfare Regression Checks

**Files:**
- Create: `tests/test_paper_claims.py`
- Modify: `paper/SECTION-III-EXECUTION-LOG.md`
- Read: `src/game/payoffs.py`

**Interfaces:**
- Consumes: `outcome_payoff(i, N, V, C)` and `expected_payoff(probs, N, V, C)`.
- Produces: executable support for III-A and III-B.

- [ ] **Step 1: Add the exhaustive payoff-tensor test**

Spot checks (all-Dove, all-Hawk, one-Hawk) are insufficient: an incorrect multi-Hawk allocation can preserve total welfare and still pass. Compare **every player in every basis outcome** against the displayed piecewise formula. Before trusting any failure, confirm the bit-order convention against `src/game/payoffs.py` (the existing convention: bit $j$ of the outcome integer is player $j$'s action, LSB = player 0).

```python
import numpy as np
import pytest

from game.payoffs import expected_payoff, outcome_payoff


def _piecewise_entry(bits, j, N, V, C):
    k = sum(bits)
    if k == 0:
        return V / N
    if k == N:
        return (V - C) / N
    return V / k if bits[j] == 1 else 0.0


@pytest.mark.parametrize("N", range(2, 8))
def test_payoff_tensor_matches_piecewise_formula_exhaustively(N):
    V, C = 4.0, 3.0
    for outcome in range(2**N):
        bits = [(outcome >> j) & 1 for j in range(N)]
        payoff = outcome_payoff(outcome, N, V, C)
        for j in range(N):
            assert payoff[j] == pytest.approx(
                _piecewise_entry(bits, j, N, V, C)
            ), f"outcome {outcome:0{N}b}, player {j}"
```

- [ ] **Step 2: Add the total-welfare identity test**

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_total_welfare_identity_for_every_basis_state(N):
    V, C = 4.0, 3.0
    for outcome in range(2**N):
        expected_total = V - C if outcome == 2**N - 1 else V
        assert outcome_payoff(outcome, N, V, C).sum() == pytest.approx(expected_total)
```

- [ ] **Step 3: Add the strict-dominance branch test**

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_hawk_strictly_dominates_dove_for_live_parameters(N):
    V, C = 4.0, 3.0
    # Against every count m of Hawks among the other N-1 players,
    # playing Hawk must strictly beat playing Dove.
    for m in range(N):
        others = (1 << m) - 1          # m Hawks in the lowest other-player slots
        hawk_outcome = (others << 1) | 1
        dove_outcome = others << 1
        hawk_pay = outcome_payoff(hawk_outcome, N, V, C)[0]
        dove_pay = outcome_payoff(dove_outcome, N, V, C)[0]
        assert hawk_pay > dove_pay, f"m={m}"
```

- [ ] **Step 4: Add the expected-mean identity test**

```python
@pytest.mark.parametrize("N", range(2, 8))
def test_expected_mean_depends_only_on_all_hawk_probability(N):
    rng = np.random.default_rng(N)
    probs = rng.dirichlet(np.ones(2**N))
    payoff = expected_payoff(probs, N, 4.0, 3.0)
    predicted_mean = 4.0 / N - 3.0 * probs[-1] / N
    assert payoff.mean() == pytest.approx(predicted_mean)
```

- [ ] **Step 5: Run the new checks**

```bash
python -m pytest tests/test_paper_claims.py -v
```

Expected: PASS.

- [ ] **Step 6: Record evidence mapping**

Add the test names to the III-A/III-B rows in `paper/CLAIM-SOURCE-MAP.md` and log the run in the execution log.

---

### Task 6: Add Quantum Benchmark, Deviation, and Covariance Checks

**Files:**
- Modify: `tests/test_paper_claims.py`
- Modify: `paper/SECTION-III-EXECUTION-LOG.md`
- Read: `src/circuits/ewl.py`
- Read: `src/circuits/n_player.py`
- Read: `src/circuits/topologies.py`
- Read: `tests/test_ne_guard.py`, `tests/test_topologies.py`, `tests/test_asymmetric_advantage.py`

**Interfaces:**
- Consumes: `q_strategy`, `build_ewl_circuit`, `ghz_entangler`, star entangler, `expected_payoff`. Confirm the exact exported names of the classical strategy constants (`HAWK`, and the Dove/identity constant) in `src/circuits/ewl.py` before writing imports.
- Produces: executable support for III-F, III-G, III-I, and III-J that is **not** already covered by existing tests (see reuse map).

- [ ] **Step 1: Add the GHZ cooperative-output test at maximal entanglement**

```python
import math

from circuits.ewl import HAWK, q_strategy   # confirm DOVE/identity export name too
from circuits.n_player import build_ewl_circuit
from circuits.topologies import ghz_entangler


@pytest.mark.parametrize("N", range(2, 9))
def test_ghz_q_profile_returns_all_dove(N):
    probs = build_ewl_circuit(
        N,
        [q_strategy(N)] * N,
        entangler=ghz_entangler,
        gamma=math.pi / 2,
    )
    expected = np.zeros(2**N)
    expected[0] = 1.0
    np.testing.assert_allclose(probs, expected, atol=1e-10)
```

- [ ] **Step 2: Add the general-$\gamma$ cooperative-invariance test (new proposition support)**

This supports the III-F general-$\gamma$ proposition: both GHZ branches acquire the identical phase $-1$ under $Q_N^{\otimes N}$, so the cooperative output is exactly $|0^N\rangle$ for every $\gamma$.

```python
@pytest.mark.parametrize("N", range(2, 8))
@pytest.mark.parametrize("gamma_frac", [0.0, 0.2, 0.4, 0.5])
def test_ghz_cooperative_output_invariant_in_gamma(N, gamma_frac):
    probs = build_ewl_circuit(
        N,
        [q_strategy(N)] * N,
        entangler=ghz_entangler,
        gamma=gamma_frac * math.pi,
    )
    assert probs[0] == pytest.approx(1.0, abs=1e-10)
    assert np.max(np.delete(probs, 0)) < 1e-12
```

- [ ] **Step 3: Add the GHZ payoff and analytic-advantage test**

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_ghz_q_profile_payoff_and_analytic_advantage(N):
    probs = build_ewl_circuit(N, [q_strategy(N)] * N)
    payoff = expected_payoff(probs, N, 4.0, 3.0)
    np.testing.assert_allclose(payoff, np.full(N, 4.0 / N), atol=1e-10)
    assert payoff.mean() - 1.0 / N == pytest.approx(3.0 / N)
```

- [ ] **Step 4: Add the maximal-entanglement Hawk-deviation formula check**

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_hawk_deviation_matches_closed_form_at_maximal_entanglement(N):
    strategies = [q_strategy(N)] * N
    strategies[0] = HAWK
    probs = build_ewl_circuit(N, strategies, gamma=math.pi / 2)
    payoff = expected_payoff(probs, N, 4.0, 3.0)[0]
    expected = 4.0 * math.cos(math.pi / N) ** 2
    assert payoff == pytest.approx(expected, abs=1e-10)
```

If this test fails, do not publish the formula. Stop and reconcile the algebra, sign convention, and code.

- [ ] **Step 5: Add the Dove-deviation non-binding test across the stated scope**

Analytic non-bindingness at $\gamma=\pi/2$ does not automatically extend elsewhere; test the whole planned grid. (Use the Dove/identity strategy constant confirmed in the Interfaces note.)

```python
@pytest.mark.parametrize("N", range(2, 8))
@pytest.mark.parametrize("gamma_frac", [0.0, 0.2, 0.4, 0.5])
def test_dove_deviation_is_non_binding(N, gamma_frac):
    strategies = [q_strategy(N)] * N
    strategies[0] = DOVE   # the U(0,0,0) identity strategy
    probs = build_ewl_circuit(
        N, strategies, entangler=ghz_entangler, gamma=gamma_frac * math.pi
    )
    dev_payoff = expected_payoff(probs, N, 4.0, 3.0)[0]
    assert dev_payoff <= 4.0 / N + 1e-10
```

- [ ] **Step 6: Add star-orbit payoff-vector covariance tests**

Operator-level covariance and its payoff consequence. Reuse the entangler constructors exercised in `tests/test_topologies.py`; do not re-test unitarity or $C_3=K_3$ (already covered there).

```python
from circuits.topologies import star_entangler


def test_star_payoff_vector_respects_leaf_orbit():
    # Hub is qubit 0; leaves 1 and 2 are in the same automorphism orbit,
    # so under the symmetric Q profile their payoffs must coincide.
    probs = build_ewl_circuit(3, [q_strategy(3)] * 3, entangler=star_entangler)
    payoff = expected_payoff(probs, 3, 4.0, 3.0)
    assert payoff[1] == pytest.approx(payoff[2], abs=1e-10)
    # And the hub is permitted to differ — do NOT assert payoff[0] == payoff[1].
```

Additionally add an operator-level check: conjugating the star entangler unitary by the SWAP of two leaves leaves it invariant, while conjugating by a hub-leaf SWAP yields the star with the relocated hub. Build the unitaries with `qiskit.quantum_info.Operator` on the same circuit constructors `tests/test_topologies.py` uses; if the constructor does not expose hub choice, verify the leaf-exchange invariance only and record the limitation in `paper/CLAIM-SOURCE-MAP.md`.

- [ ] **Step 7: Reference (do not duplicate) the equilibrium-boundary guard**

The restricted-equilibrium boundary $(N=2,3$ Nash; $N\geq4$ not$)$ is already protected by `tests/test_ne_guard.py`. Add that test's node IDs to the III-G row of `paper/CLAIM-SOURCE-MAP.md`; do not re-implement it.

- [ ] **Step 8: Add the single-flip welfare check**

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_single_bit_flip_preserves_total_welfare(N):
    all_dove_total = outcome_payoff(0, N, 4.0, 3.0).sum()
    for player in range(N):
        one_hawk_total = outcome_payoff(1 << player, N, 4.0, 3.0).sum()
        assert one_hawk_total == pytest.approx(all_dove_total)
```

- [ ] **Step 9: Run all mathematical checks**

```bash
python -m pytest tests/test_paper_claims.py -v
```

Expected: PASS before any theorem wording is added.

- [ ] **Step 10: Checkpoint note**

Record the exact tested formulas and finite $N,\gamma$ ranges in the execution log, together with a proposed labeling: which statements may be labeled propositions (analytic proof + regression check) and which must remain computational results. This labeling is confirmed with the user at gate G3 alongside the III-A style review.

---

### Task 7: Rewrite III-A, Notation and the Classical Payoff Tensor

**Files:**
- Modify: `paper/qhd.tex` — first subsection inside the `\label{sec:model}` block
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Modify only if needed: `paper/references.bib`
- Test: `tests/test_paper_claims.py::test_payoff_tensor_matches_piecewise_formula_exhaustively`

**Interfaces:**
- Consumes: approved terminology, style guide, and the exhaustively tested payoff tensor.
- Produces: symbols and payoff definitions used by every later subsection.

- [ ] **Step 1: Define the reader question**

Use this opening purpose:

```latex
Before quantizing the game, we need a payoff rule that assigns a value to every one of the $2^N$ classical outcomes and preserves each player's identity.
```

- [ ] **Step 2: Introduce notation in dependency order**

Define $\mathcal N=\{1,\ldots,N\}$, $x\in\{0,1\}^N$, $x_j=1$ for Hawk, $x_j=0$ for Dove, and $k(x)=\sum_jx_j$.

- [ ] **Step 3: Insert the complete tensor equation**

```latex
\begin{equation}
P_j(x)=
\begin{cases}
V/N, & k(x)=0,\\
V/k(x), & 0<k(x)<N \text{ and } x_j=1,\\
0, & 0<k(x)<N \text{ and } x_j=0,\\
(V-C)/N, & k(x)=N.
\end{cases}
\label{eq:payoff-tensor}
\end{equation}
```

- [ ] **Step 4: Explain each branch with one concrete example**

Use $N=4$ examples for all-Dove, one-Hawk, and all-Hawk outcomes. Keep the examples algebraic; do not introduce simulation or hardware results.

- [ ] **Step 5: Cite the classical and multiplayer game sources**

Every historical or inherited payoff claim must use a verified source from `paper/LITERATURE-AUDIT.md`.

- [ ] **Step 6: Run the focused claim test**

```bash
python -m pytest tests/test_paper_claims.py::test_payoff_tensor_matches_piecewise_formula_exhaustively -v
```

Expected: PASS.

- [ ] **Step 7: Compile and inspect**

Run the four-pass temporary build. Inspect the page containing III-A for equation overflow, unexplained symbols, paragraph density, and every style-guide 7.1--7.4 rule.

- [ ] **Step 8: Gate G3 — style calibration**

Show the III-A source, the rendered page, and the Task 6 proposition-labeling proposal. This gate exists so the user corrects voice, density, and depth **once, early**. Apply the calibration feedback to III-A before continuing; it becomes binding precedent for III-B through III-J. Record the calibration decisions in the execution log.

---

### Task 8: Rewrite III-B, Classical Equilibrium and Welfare Geometry

**Files:**
- Modify: `paper/qhd.tex` immediately after III-A
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Test: `tests/test_paper_claims.py::test_total_welfare_identity_for_every_basis_state`
- Test: `tests/test_paper_claims.py::test_hawk_strictly_dominates_dove_for_live_parameters`
- Test: `tests/test_paper_claims.py::test_expected_mean_depends_only_on_all_hawk_probability`

**Interfaces:**
- Consumes: $P_j(x)$ and $k(x)$ from III-A.
- Produces: classical baseline and welfare identity used by Sections III-I, IV-D, VI-D, and VII-B.

- [ ] **Step 1: Derive strict dominance for the fixed parameters**

Show, for $V=4,C=3$, that Hawk pays more than Dove against every pure opponent-count configuration. Scope the statement to the live parameter convention.

- [ ] **Step 2: State the classical equilibrium and baseline**

Derive all-Hawk as the unique classical pure equilibrium and its per-player payoff $(V-C)/N=1/N$.

- [ ] **Step 3: Prove the outcome-level welfare identity**

```latex
\begin{proposition}[Outcome-level welfare]
For every $x\in\{0,1\}^N$,
\begin{equation}
\sum_{j=1}^{N}P_j(x)
=V-C\,\mathbf 1_{\{x=1^N\}}.
\label{eq:outcome-welfare}
\end{equation}
\end{proposition}
```

The proof must cover $k=0$, $0<k<N$, and $k=N$ separately.

- [ ] **Step 4: Derive the expected-mean identity**

```latex
\begin{equation}
\bar\pi
=\frac{1}{N}\sum_xp(x)\sum_jP_j(x)
=\frac{V}{N}-\frac{C}{N}p(1^N).
\label{eq:mean-welfare}
\end{equation}
```

- [ ] **Step 5: Explain the result in plain language**

State that only all-Hawk probability lowers mean welfare; every other outcome redistributes total value $V$.

- [ ] **Step 6: Run the focused tests**

```bash
python -m pytest \
  tests/test_paper_claims.py::test_total_welfare_identity_for_every_basis_state \
  tests/test_paper_claims.py::test_hawk_strictly_dominates_dove_for_live_parameters \
  tests/test_paper_claims.py::test_expected_mean_depends_only_on_all_hawk_probability \
  -v
```

Expected: PASS.

- [ ] **Step 7: Compile, inspect, checkpoint**

Build, inspect proposition placement, equation width, and style-guide compliance. Record a checkpoint note and continue.

---

### Task 9: Rewrite III-C, Quantum Strategies and the EWL Protocol

**Files:**
- Modify: `paper/qhd.tex` after III-B
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Modify only with verified entries: `paper/references.bib`
- Read: `src/circuits/ewl.py` (strategy constructors)
- Read: `src/circuits/n_player.py` (`build_ewl_circuit`)

**Interfaces:**
- Consumes: classical outcome space and payoffs from III-A/III-B.
- Produces: $U(\theta,\alpha,\beta)$, $D$, $H$, $Q_N$, $J_T$, output state, and outcome probabilities.

- [ ] **Step 1: Give an intuitive protocol preview**

Explain in three sentences: entangle, apply local strategies, disentangle and measure. Add a `% FIGURE F1 ANCHOR` comment marking where the protocol schematic from spec Section 8.2 will be placed by the figure plan; do not create the figure now.

- [ ] **Step 2: Define the full SU(2) strategy matrix**

```latex
\begin{equation}
U(\theta,\alpha,\beta)=
\begin{pmatrix}
e^{i\alpha}\cos(\theta/2) & i e^{i\beta}\sin(\theta/2)\\
i e^{-i\beta}\sin(\theta/2) & e^{-i\alpha}\cos(\theta/2)
\end{pmatrix}.
\label{eq:strategy-unitary}
\end{equation}
```

- [ ] **Step 3: Define named strategies exactly**

```latex
D=U(0,0,0),\qquad
H=U(\pi,0,0),\qquad
Q_N=U(0,\pi/N,\pi/N).
```

State that $Q_N$ is GHZ-derived and is held fixed across entangler families for controlled comparison.

- [ ] **Step 4: Define the EWL state and measurement law**

```latex
\begin{equation}
|\psi_{\mathrm{out}}\rangle
=J_T^\dagger(\gamma)
\left(\bigotimes_{j=1}^{N}U_j\right)
J_T(\gamma)|0^N\rangle,
\end{equation}
\begin{equation}
p_T(x\mid\boldsymbol U)
=|\langle x|\psi_{\mathrm{out}}\rangle|^2.
\end{equation}
```

- [ ] **Step 5: Add scope language**

State that players physically have an SU(2) strategy space, while this paper's equilibrium test enumerates only $\{D,H,Q_N\}$.

- [ ] **Step 6: Verify matrix and named strategies against code**

Run a short Python check comparing `U(0,0,0)`, `U(pi,0,0)`, and `q_strategy(N)` with the manuscript definitions for $N=2,3,4$.

- [ ] **Step 7: Compile, inspect, checkpoint**

Check matrix width in the TQE column layout, style-guide compliance, and record a checkpoint note.

---

### Task 10: Rewrite III-D, Entangler Families and Graph Symmetry

**Files:**
- Modify: `paper/qhd.tex` after III-C
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Modify only with verified entries: `paper/references.bib`
- Read: `src/circuits/topologies.py`
- Read: `src/circuits/topology_graphs.py`
- Reuse: `tests/test_topologies.py` (unitarity, $C_3=K_3$) — reference, do not duplicate
- Test (new): star-orbit covariance tests from Task 6

**Interfaces:**
- Consumes: EWL operator $J_T$ from III-C and the spec 3.2 vocabulary.
- Produces: formal entangler families, the symmetry principle used by III-J and later fairness sections, and the normalized interaction-strength convention used by Section V.

- [ ] **Step 1: Open with the two-level vocabulary**

State explicitly: five entangler families are compared; only ring, star, and complete are graph topologies with an edge set; GHZ and W are global-interpolation constructions. Add a `% FIGURE F2 ANCHOR` comment for the entangler-family gallery.

- [ ] **Step 2: Define the GHZ operator**

```latex
\begin{equation}
J_{\mathrm{GHZ}}(\gamma)
=\cos\frac{\gamma}{2}I^{\otimes N}
+i\sin\frac{\gamma}{2}X^{\otimes N}.
\end{equation}
```

- [ ] **Step 3: Define pairwise graph entanglers**

```latex
\begin{equation}
J_G(\gamma)
=\prod_{(r,s)\in E(G)}
\exp\left(i\frac{\gamma}{2}X_rX_s\right).
\end{equation}
```

Define the ring $C_N$, star $S_N$ with hub 0, and complete graph $K_N$ edge sets.

- [ ] **Step 4: Define the W-state construction without hiding its design choice**

State the implemented involution $S_W$ and

```latex
J_W(\gamma)=\cos(\gamma/2)I+i\sin(\gamma/2)S_W.
```

Explicitly identify the interpolation as the construction used in this study, not the unique possible W entangler.

- [ ] **Step 5: Define the normalized interaction-strength convention**

State that equal $\gamma$ does not equalize total interaction strength across families (one global rotation versus $|E(G)|$ per-edge rotations), define the normalization convention (per-edge angle scaled by edge count, or equivalent as implemented), and state that Section V reports a sensitivity control under this convention. The exact convention must match what the simulation code implements — verify against `src/circuits/topologies.py` before writing; if no such normalization exists in code yet, present the convention as a definition for Section V's plan and say so in `paper/CLAIM-SOURCE-MAP.md`.

- [ ] **Step 6: State and derive permutation covariance**

Use a permutation operator $R_\sigma$ and derive:

```latex
R_\sigma J_G R_\sigma^\dagger=J_{\sigma(G)}.
```

Then explain the payoff-vector permutation under relabeling.

- [ ] **Step 7: State the graph-orbit corollary**

Under symmetric local strategies and permutation-symmetric noise, players in the same automorphism orbit have equal expected payoffs.

- [ ] **Step 8: Verify operator statements numerically**

Run the Task 6 covariance tests plus the existing `tests/test_topologies.py` suite:

```bash
python -m pytest tests/test_topologies.py tests/test_paper_claims.py -k "orbit or covariance" -v
```

Expected: PASS. Record existing-test node IDs in `paper/CLAIM-SOURCE-MAP.md` for unitarity and $C_3=K_3$.

- [ ] **Step 9: Compile, inspect, checkpoint**

Ensure the subsection explains the families before gate counts. Record a checkpoint note.

---

### Task 11: Rewrite III-E, Payoff, Advantage, Equilibrium, and Fairness Metrics

**Files:**
- Modify: `paper/qhd.tex` after III-D
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Test: `tests/test_paper_structure.py`

**Interfaces:**
- Consumes: $p_T(x\mid\boldsymbol U)$ and $P_j(x)$.
- Produces: every metric used in Sections IV--VII.

- [ ] **Step 1: Define expected player payoffs and the vector**

```latex
\begin{equation}
\pi_j(\boldsymbol U;T)
=\sum_x p_T(x\mid\boldsymbol U)P_j(x),
\qquad
\boldsymbol\pi=(\pi_1,\ldots,\pi_N).
\end{equation}
```

- [ ] **Step 2: Define the restricted equilibrium test and deviation gaps**

```latex
\begin{equation}
g_j(a)
=\pi_j(Q_N^{\otimes N})
-\pi_j(a,Q_{N,-j}),
\qquad a\in\{D,H\}.
\end{equation}
```

The profile passes the restricted test iff every $g_j(a)\ge0$ — both deviations, every player. (This definition is what the VI-F hardware evidence rule keys on.)

- [ ] **Step 3: Define both advantage metrics separately**

Insert separate equations and a two-row comparison table for analytic-baseline advantage and circuit-relative payoff gap.

- [ ] **Step 4: Define the all-zero target-state population**

Define $P(0^N)$ with its canonical name and shorthand per spec 3.3, and state why it is not a fidelity.

- [ ] **Step 5: Define fairness summaries**

```latex
S_\pi=\max_j\pi_j-\min_j\pi_j,
\qquad
F_\pi=\min_j\pi_j.
```

State that $\boldsymbol\pi$ remains the primary evidence.

- [ ] **Step 6: Run wording guards**

```bash
python -m pytest tests/test_paper_structure.py -v
```

Expected: PASS.

- [ ] **Step 7: Compile, inspect, checkpoint**

Check that no metric is used before definition. Record a checkpoint note.

---

### Task 12: Rewrite III-F, GHZ Cooperative Benchmark (Including the General-$\gamma$ Proposition)

**Files:**
- Modify: `paper/qhd.tex` after III-E
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Test: GHZ tests in `tests/test_paper_claims.py` (including `test_ghz_cooperative_output_invariant_in_gamma`)

**Interfaces:**
- Consumes: $Q_N$, $J_{\mathrm{GHZ}}$, payoff tensor, and analytic baseline.
- Produces: the cooperative payoff theorem and the general-$\gamma$ invariance used throughout the rest of the paper.

- [ ] **Step 1: Write the phase-cancellation derivation**

Show the action of $J_{\mathrm{GHZ}}(\gamma)$ on $|0^N\rangle$, the equal phase gained by the $|0^N\rangle$ and $|1^N\rangle$ branches under $Q_N^{\otimes N}$, and the recovery of $|0^N\rangle$ after $J^\dagger$.

- [ ] **Step 2: State the general-$\gamma$ cooperative-invariance proposition with proof**

```latex
\begin{proposition}[Cooperative invariance in the entanglement angle]
For every $\gamma$,
\begin{equation}
J_{\mathrm{GHZ}}^\dagger(\gamma)\,Q_N^{\otimes N}\,J_{\mathrm{GHZ}}(\gamma)\,|0^N\rangle
=-\,|0^N\rangle,
\end{equation}
hence $p(0^N)=1$, $\pi_j=V/N$, and $\Delta_{\mathrm{ana}}=C/N$ independently of $\gamma$.
\end{proposition}
```

Proof (four lines, must appear in the manuscript): $J_{\mathrm{GHZ}}(\gamma)|0^N\rangle=\cos(\gamma/2)|0^N\rangle+i\sin(\gamma/2)|1^N\rangle$; $Q_N$ multiplies $|0\rangle$ by $e^{i\pi/N}$ and $|1\rangle$ by $e^{-i\pi/N}$, so the $N$-fold products give phase $e^{i\pi}=-1$ on the all-zero branch and $e^{-i\pi}=-1$ on the all-one branch — the same phase; the state is therefore $-J_{\mathrm{GHZ}}(\gamma)|0^N\rangle$, and applying $J^\dagger$ returns $-|0^N\rangle$.

- [ ] **Step 3: Specialize to maximal entanglement and live parameters**

State the $\gamma=\pi/2$ benchmark as the corollary used by the experiments: $\pi_j=4/N$ and $\Delta_{\mathrm{ana}}=3/N$ for $V=4,C=3$.

- [ ] **Step 4: State the significance sentence**

One sentence, verbatim intent: the invariance means the entanglement angle can move deviation incentives (III-G) while leaving the cooperative payoff exactly unchanged — $\gamma$ is a pure incentive dial.

- [ ] **Step 5: Run the focused tests**

```bash
python -m pytest tests/test_paper_claims.py -k "ghz" -v
```

Expected: PASS, including the general-$\gamma$ invariance test.

- [ ] **Step 6: Compile, inspect, checkpoint**

Check proof length, notation continuity, and page density. Record a checkpoint note.

---

### Task 13: Rewrite III-G, Incentive Compatibility and the Entanglement-Angle Boundary

**Files:**
- Modify: `paper/qhd.tex` after III-F
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Test: deviation tests in `tests/test_paper_claims.py`; boundary guard reused from `tests/test_ne_guard.py`

**Interfaces:**
- Consumes: cooperative benchmark, the general-$\gamma$ invariance, and the deviation-gap definition.
- Produces: the restricted-equilibrium boundary and general-$\gamma$ incentive prediction.

- [ ] **Step 1: Derive the maximal-entanglement Hawk deviation**

Derive and verify:

```latex
\begin{equation}
\pi_j(H,Q_{N,-j};\pi/2)
=V\cos^2\left(\frac{\pi}{N}\right).
\end{equation}
```

For $V=4$, also show the equivalent form $2+2\cos(2\pi/N)$.

- [ ] **Step 2: Derive the Dove deviation with the same rigor as the Hawk deviation**

Derive its closed form. Before publishing it, numerically compare against `build_ewl_circuit` over $N=2,\ldots,5$ and $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$ (same gating as the Hawk formula — any mismatch blocks the edit). Then show the non-binding inequality across that stated $(N,\gamma)$ scope, supported by `test_dove_deviation_is_non_binding`. Do not claim non-bindingness beyond the tested scope.

- [ ] **Step 3: Derive the equilibrium inequality**

Compare the Hawk-deviation payoff with $V/N$ and establish the boundary at $N=2,3$ versus $N\ge4$. Cite the reused `tests/test_ne_guard.py` guard in `paper/CLAIM-SOURCE-MAP.md`.

- [ ] **Step 4: Derive and test the general-$\gamma$ Hawk formula**

Use the candidate formula (already numerically confirmed to $1.33\times10^{-15}$ during plan review):

```latex
\pi_j(H,Q_{N,-j};\gamma)
=V\left[1-\sin^2\gamma\,\sin^2\left(\frac{\pi}{N}\right)\right].
```

Re-run the comparison against `build_ewl_circuit` for $N=2,3,4,5$ and $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$ as part of this task. Any mismatch blocks the manuscript edit.

- [ ] **Step 5: Connect to the invariance proposition**

State explicitly: by III-F the cooperative payoff is $\gamma$-invariant, so the entanglement angle changes *only* the deviation side of the equilibrium inequality — this is the mechanism behind the entanglement-angle boundary.

- [ ] **Step 6: Run the deviation tests**

```bash
conda run -n entangled-equilibria python -m pytest tests/test_paper_claims.py -k "hawk_deviation or dove_deviation" -v
conda run -n entangled-equilibria python -m pytest tests/test_ne_guard.py -v
```

Expected: PASS.

- [ ] **Step 7: Add the honesty boundary**

State that the result proves equilibrium only in the discrete menu $\{D,H,Q_N\}$ and does not establish equilibrium against arbitrary SU(2) deviations.

- [ ] **Step 8: Gate G4 — high-stakes review**

This subsection carries the paper's central game-theoretic claim. Show the derivations (both deviations), the numerical cross-check tables, and the rendered pages. Do not continue past this gate without explicit approval. Record the decision in the execution log.

---

### Task 14: Rewrite III-H, Circuit Realization, Noise Channels, and Hardware Estimators

**Files:**
- Modify: `paper/qhd.tex` after III-G
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Modify only with verified entries: `paper/references.bib`
- Read: topology implementations and noise-path code
- Read: `src/hardware/mitigation.py` (including the separable-readout limitation comment)
- Reuse: `tests/test_hardware_mitigation.py`, `tests/test_noise.py` — reference, do not duplicate

**Interfaces:**
- Consumes: ideal entanglers from III-D and noisy outcome distributions.
- Produces: the ideal/circuit/simulation/device layer distinction, formal noise channels, the estimators applied in Section VI, and the single registered decision rule used by every Section VI sign/threshold claim.

- [ ] **Step 1: Introduce the four-layer distinction**

Use a compact table with rows for ideal operator, compiled circuit, simulated channel, and physical device.

- [ ] **Step 2: Define depolarizing channels with strength $\eta$**

```latex
\begin{equation}
\mathcal D_\eta^{(d)}(\rho)
=(1-\eta)\rho
+\eta\,\mathrm{Tr}(\rho)\frac{I_d}{d},
\end{equation}
```

with $d=2$ and $d=4$ for one- and two-qubit channels. ($\eta$, not $\lambda$ — the fold scale below is $s$; no symbol is reused.)

- [ ] **Step 3: State the implemented assignment rule**

Document how $\eta$ and the two-qubit ratio are applied to the pinned gate basis. Verify exact semantics against the noise implementation before writing. Cite `tests/test_noise.py` node IDs in `paper/CLAIM-SOURCE-MAP.md`.

- [ ] **Step 4: Explain circuit-cost confounding**

State why two entangler families can incur different routed two-qubit costs and why production-circuit robustness cannot automatically be attributed to the abstract family alone.

- [ ] **Step 5: Define the assignment matrices with their independence assumption**

```latex
A_j[m,t]=\Pr(\text{measure }m\mid\text{prepared }t),
\qquad
A=\bigotimes_jA_j.
```

Immediately beside the equation, state: the tensor-product form assumes separable per-qubit readout errors and does not model correlated readout crosstalk (the same limitation documented in `src/hardware/mitigation.py`). List correlated readout error among the excluded uncertainty/model components.

- [ ] **Step 6: Define constrained probability reconstruction**

```latex
\widehat p
=\arg\min_{p\ge0,\,\mathbf1^Tp=1}
\|Ap-p_{\mathrm{meas}}\|_2^2.
```

Confirm the manuscript description matches the implementation; cite `tests/test_hardware_mitigation.py` node IDs in `paper/CLAIM-SOURCE-MAP.md`.

- [ ] **Step 7: Define local gate folding and weighted ZNE with fold scale $s$**

```latex
y_s=a+bs+\epsilon_s,
\qquad
(\widehat a,\widehat b)
=\arg\min_{a,b}\sum_s
\frac{(y_s-a-b\,s)^2}{\sigma_s^2},
```

with $s\in\{1,3,5\}$ and extrapolated estimate $\widehat y(0)=\widehat a$.

- [ ] **Step 8: Define uncertainty scope and the registered decision rule**

State which variance enters the weighted fit and explicitly separate shot, fit, run, and calibration-epoch uncertainty. Then define the **single decision rule** every Section VI sign/threshold claim uses: a claim of positive gap (or sign change, or separation) passes only if its one-sided interval at the declared level excludes zero (or meets the registered non-inferiority margin). Name the claims this rule governs: equilibrium gaps, entanglement-angle sign change including the marginal $0.4\pi$ point, ring-$N{=}4$ retention, hub-versus-leaf separation.

- [ ] **Step 9: Cite primary sources**

Use verified peer-reviewed sources for depolarizing channels, NISQ noise, compilation/routing effects, measurement mitigation, ZNE, and local folding.

- [ ] **Step 10: Compile, inspect, checkpoint**

Check the table and channel equations in the TQE column layout. Ensure the subsection defines estimators without reporting results, and reads as one question ("what stands between the ideal operator and the measured number?"). Record a checkpoint note.

---

### Task 15: Rewrite III-I, Structural Robustness of the Payoff Observable

**Files:**
- Modify: `paper/qhd.tex` after III-H
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Test: `tests/test_paper_claims.py::test_single_bit_flip_preserves_total_welfare`

**Interfaces:**
- Consumes: welfare identity from III-B.
- Produces: the mechanism later tested by simulation and hardware state-quality comparisons.

- [ ] **Step 1: Prove the single-flip result**

Show:

```latex
\sum_\ell P_\ell(0^N)
=\sum_\ell P_\ell(e_j)
=V.
```

- [ ] **Step 2: Derive the ideal independent-flip corollary**

Under an explicitly idealized independent classical bit-flip model with rate $\epsilon$, derive:

```latex
\bar\pi(\epsilon)
=\frac{V}{N}-\frac{C}{N}\epsilon^N.
```

State that the formula does not describe arbitrary gate noise or correlated errors.

- [ ] **Step 3: Explain observable-specific robustness**

Use plain language to distinguish stable payoff expectation from a preserved quantum state, phrased against the all-zero target-state population (canonical name per spec 3.3).

- [ ] **Step 4: Run the focused test**

```bash
python -m pytest tests/test_paper_claims.py::test_single_bit_flip_preserves_total_welfare -v
```

Expected: PASS.

- [ ] **Step 5: Compile, inspect, checkpoint**

Check that the caveat is adjacent to the corollary. Record a checkpoint note.

---

### Task 16: Rewrite III-J, Player-Level Redistribution and Position-Locked Fairness

**Files:**
- Modify: `paper/qhd.tex` after III-I
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Modify only with verified entries: `paper/references.bib`
- Reuse: `tests/test_asymmetric_advantage.py` — reference, do not duplicate
- Test (new): star-orbit covariance tests from Task 6

**Interfaces:**
- Consumes: payoff vector, fairness metrics, permutation covariance, and observable robustness.
- Produces: the fairness mechanism later evaluated in simulation and hardware.

- [ ] **Step 1: State the central tension**

Explain that conservation of mean welfare does not conserve each player's payoff.

- [ ] **Step 2: Derive payoff-vector covariance under relabeling**

Show that relabeling players and graph vertices permutes $\boldsymbol\pi$ rather than changing its multiset of ideal values. Cite the Task 6 covariance tests and the existing `tests/test_asymmetric_advantage.py` node IDs in `paper/CLAIM-SOURCE-MAP.md`.

- [ ] **Step 3: State the graph-orbit consequence**

Explain why a star permits one hub payoff and one leaf payoff even under symmetric strategies.

- [ ] **Step 4: Define the fairness reading rule**

Require every asymmetric result to report:

```latex
\boldsymbol\pi,
\qquad
\bar\pi,
\qquad
S_\pi,
\qquad
F_\pi.
```

- [ ] **Step 5: Scope position locking carefully**

State the analytical symmetry prediction here. Reserve the empirical claim that the effect survives physical-qubit reassignment for Section VI-G, judged under the III-H decision rule.

- [ ] **Step 6: Cite network-game and fairness literature**

Use verified sources that discuss role-dependent or network-position-dependent outcomes. Do not claim those sources studied this quantum mechanism.

- [ ] **Step 7: Compile, inspect, checkpoint**

Check how this subsection transitions to analytical predictions. Record a checkpoint note.

---

### Task 17: Section III Flow Pass, Integration, and Verification

**Files:**
- Modify: `paper/qhd.tex` Section III as needed for flow and transitions
- Modify: `paper/CLAIM-SOURCE-MAP.md`, `paper/LITERATURE-AUDIT.md`, `paper/SECTION-III-EXECUTION-LOG.md`
- Modify: `tests/test_paper_structure.py`
- Test: `tests/test_paper_claims.py`, `tests/test_paper_structure.py`, plus the reused existing suites

**Interfaces:**
- Consumes: drafted III-A through III-J subsections.
- Produces: one coherent, compilable mathematical framework ready for Section IV planning.

- [ ] **Step 1: Run the full evidence suite**

```bash
python -m pytest tests/test_paper_claims.py tests/test_paper_structure.py tests/test_topologies.py tests/test_ne_guard.py tests/test_asymmetric_advantage.py -v
```

Expected: zero failures.

- [ ] **Step 2: Check the exact heading structure — each heading exactly once, in order, inside Section III**

Extend `tests/test_paper_structure.py`:

```python
APPROVED_III_HEADINGS = [
    "Notation and the Classical $N$-Player Payoff Tensor",
    "Classical Equilibrium and Welfare Geometry",
    "Quantum Strategies and the EWL Protocol",
    "Entangler Families and Graph Symmetry",
    "Expected Payoff, Advantage, Equilibrium, and Fairness",
    "GHZ Cooperative Benchmark",
    "Incentive Compatibility and the Entanglement-Angle Boundary",
    "Circuit Realization, Noise Channels, and Hardware Estimators",
    "Structural Robustness of the Payoff Observable",
    "Player-Level Redistribution and Position-Locked Fairness",
]


def test_section_iii_headings_exactly_once_in_order():
    block = _section_iii_block(PAPER.read_text(encoding="utf-8"))
    positions = []
    for heading in APPROVED_III_HEADINGS:
        assert block.count(heading) == 1, f"'{heading}' appears {block.count(heading)}x"
        positions.append(block.index(heading))
    assert positions == sorted(positions)
    assert block.count(r"\subsection{") == len(APPROVED_III_HEADINGS)
```

- [ ] **Step 3: Run the mandatory flow pass (style guide 7.5)**

Render the full PDF to page images and read Section III top to bottom in the rendered form, not the source. Then:

1. rewrite subsection openings/closings so each answers the question the previous one raised;
2. verify one authorial voice: consistent tense, "we" usage, and terminology;
3. verify every subsection opener says why the reader needs it now, and every closer hands off;
4. verify every displayed equation has a plain-language reading within two sentences;
5. fix every violation found; re-compile.

- [ ] **Step 4: Audit notation**

Search Section III for every symbol introduced. Confirm each is defined before its first use and used consistently: $x$, $k$, $P_j$, $\pi_j$, $\bar\pi$, $J_T$, $Q_N$, $g_j$, $\Delta_{\mathrm{ana}}$, $\Delta_{\mathrm{circ}}$, $S_\pi$, $F_\pi$, $A$, $\eta$, $s$, and $\gamma$. Confirm $\lambda$ does not appear with two meanings (it should not appear at all unless a future subsection introduces it once).

- [ ] **Step 5: Audit evidence labels**

For every proposition, computational result, and implementation definition, confirm that `paper/CLAIM-SOURCE-MAP.md` names its proof/test/code/citation source, including reused existing-test node IDs.

- [ ] **Step 6: Inspect page density**

Check Section III page images for:

```text
more than two dense displayed equations without explanation
matrices extending outside a column
definitions separated from their first use
paragraphs longer than approximately 180 words
unexplained acronyms
proofs interrupted by implementation details
```

- [ ] **Step 7: Check the page budget**

Record the new total page count and the pages occupied by Section III in the execution log. If Section III alone makes the 16--20 page target impossible, identify repetition or move only non-core implementation detail to Appendix A; do not remove core derivations.

- [ ] **Step 8: Run a clean four-pass build**

Use the non-destructive build command from Task 2. Expected: exit code 0, no undefined citations, and no undefined references.

- [ ] **Step 9: Gate G5 — Section III approval**

Present:

1. the complete Section III source;
2. rendered pages;
3. full test output (new + reused suites);
4. citation audit with locators;
5. page-count change;
6. flow-pass findings and fixes;
7. any remaining concerns.

Wait for explicit approval. Record the decision and any accepted exceptions in the execution log.

- [ ] **Step 10: Optional checkpoint commit**

Only if the user explicitly requests a commit:

```bash
git add paper/qhd.tex paper/main.tex paper/README.md paper/references.bib paper/STYLE-GUIDE.md paper/LITERATURE-AUDIT.md paper/CLAIM-SOURCE-MAP.md paper/SECTION-III-EXECUTION-LOG.md tests/test_paper_claims.py tests/test_paper_structure.py
git commit -m "paper: rewrite mathematical framework"
```

Do not add an attribution footer.

---

### Task 18: Close Phase 1 and Plan the Next Phases

**Files:**
- Read: approved Section III in `paper/qhd.tex`
- Read: hardware artifacts (Appendix E sources / archived job records) — Dove-deviation availability check
- Create later, only after approval: `docs/superpowers/plans/2026-07-31-qhd-analytical-predictions-rewrite.md`
- Create later, only after Section IV approval: `docs/superpowers/plans/2026-07-31-qhd-figure-redesign.md`

**Interfaces:**
- Consumes: user-approved Section III.
- Produces: a separate implementation plan for Section IV, the VI-F evidence-branch decision input, and (after Section IV) a figure-redesign plan implementing spec Section 8.

- [ ] **Step 1: Confirm the Section III approval record**

Record the user's explicit approval and any accepted wording exceptions in the execution log.

- [ ] **Step 2: Check the hardware artifacts for Dove-deviation executions**

Determine from the archived job records whether $g_j(D)$ was ever measured at GHZ $N=3$. Record the answer — it selects the VI-F branch (six gaps versus the narrowed Hawk-only claim) that the Section VI plan must implement. No new IBM jobs may be run to fill the gap.

- [ ] **Step 3: List the verified predictions now available**

The list must be generated from the approved Section III and include only claims with completed tests or derivations (including the general-$\gamma$ invariance proposition).

- [ ] **Step 4: Write the Section IV plan**

Create a new plan covering IV-A through IV-E of the consolidated spec, with each prediction mapped to its Section III equation/proposition and later simulation/hardware test. The Section IV plan must end by scheduling the figure-redesign plan (spec Section 8), because figures F1/F2 and all caption rewrites depend on the P1--P8 ledger that Section IV creates.

- [ ] **Step 5: Stop before implementation**

Present the Section IV plan to the user. Do not rewrite Section IV until the user approves that new plan.

---

## Plan Self-Review Checklist

- [ ] The TQE shell migration precedes all prose work, starts with the `main.tex`/`qhd.tex` diff, and resolves the competing entry point and README.
- [ ] Every Section III subsection in the consolidated spec (III-A through III-J, ten subsections) has exactly one rewrite task.
- [ ] Every central formula has a test, derivation gate, or implementation comparison; existing tests are reused, not duplicated.
- [ ] The payoff-tensor test is exhaustive over every player and every basis outcome.
- [ ] The general-$\gamma$ cooperative invariance is a proposition with an in-manuscript proof and a regression test.
- [ ] The Dove deviation gets a numerically gated closed form plus a scoped non-binding test, mirroring the Hawk treatment.
- [ ] $\eta$/$s$/$\gamma$ symbol discipline holds; $\lambda$ is not used for two quantities.
- [ ] The readout-independence assumption sits beside $A=\bigotimes_jA_j$ and correlated readout is an excluded component.
- [ ] The single registered decision rule is defined in III-H and named for every Section VI sign/threshold claim.
- [ ] The literature audit records evidence access, locator, and support type; abstract-only sources cannot support detailed claims; auditing is staged.
- [ ] File references use semantic anchors; line numbers are hints only.
- [ ] Approval gates are exactly G1--G5; the execution log records every checkpoint and gate.
- [ ] The heading test requires each approved heading exactly once, in order, inside Section III.
- [ ] The flow pass is a mandatory, named step before Section III approval.
- [ ] Figure anchors (F1, F2) are placed but no figures are generated in this plan; no new IBM hardware jobs.
- [ ] The two advantage metrics remain distinct; restricted equilibrium remains explicitly finite-menu; fairness remains vector-first; ideal family and implementation cost remain distinct.
- [ ] Builds are non-destructive and do not overwrite the user's existing PDF.
- [ ] No commit occurs without explicit user authorization.
- [ ] The plan contains no placeholders or deferred unspecified work.
