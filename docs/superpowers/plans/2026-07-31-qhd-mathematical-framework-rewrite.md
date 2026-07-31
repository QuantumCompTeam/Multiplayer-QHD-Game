# QHD Mathematical Framework Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Version:** v2 — revised with the 2026-07-31 spec revision: IEEE TQE venue locked, style guide added as a deliverable, Section III consolidated to ten subsections (circuit realization and hardware estimators merged), and approval gates batched.

**Goal:** Establish a verified terminology, citation, style, and mathematical foundation for the QHD paper, then rewrite Section III one subsection at a time with batched approval gates and a mandatory section-level flow pass.

**Architecture:** This is the first execution plan derived from `docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md` (v2). It covers the dependency-setting work and Section III. Each subsection follows the same evidence chain: define its reader question, verify formulas against code or symbolic derivation, add only verified peer-reviewed citations, edit `paper/qhd.tex` following `paper/STYLE-GUIDE.md`, and compile in an isolated build directory. User approval happens at five defined gates rather than after every subsection: (G1) baseline + terminology + style guide, (G2) literature audit, (G3) first drafted subsection III-A for style calibration, (G4) the high-stakes III-G derivation, (G5) the complete Section III after its flow pass. Sections IV--VIII and the figure redesign receive separate plans only after Section III is approved.

**Tech Stack:** LaTeX/IEEEtran, BibTeX, Python 3.10+, NumPy, Qiskit 1.3.2, pytest, MiKTeX/pdfTeX, Crossref/publisher DOI records, existing QHD simulation code.

## Global Constraints

- Target venue: IEEE Transactions on Quantum Engineering — IEEEtran two-column template, approximately 16--20 pages including appendices; every equation, matrix, and table must fit one column unless deliberately set as a `figure*`/`table*` float.
- Target reader: mixed technical reader with undergraduate linear algebra, probability, and basic quantum-computing knowledge.
- Every drafted paragraph must comply with `paper/STYLE-GUIDE.md` (created in Task 2): topic sentences, ≤180-word paragraphs, ≤2 displayed equations per paragraph, plain-language reading after every displayed equation, subsection openers that answer "why now?", subsection closers that hand off.
- Define all game-theory, EWL, topology, mitigation, and paper-specific terms before use.
- Keep every central mathematical definition and derivation in the main manuscript.
- Final bibliography target: more than 50 relevant, verified, peer-reviewed sources; Section III citations must be authoritative primary sources wherever available.
- Preserve the Theory → Simulation → Hardware narrative.
- Do not alter or generate figures during this plan; the figure redesign (spec Section 8) is a separate plan.
- Do not strengthen restricted-menu equilibrium into full-SU(2) equilibrium.
- Keep the player payoff vector as primary evidence; fairness scalars are summaries.
- Distinguish analytic-baseline advantage from circuit-relative payoff gap everywhere.
- Distinguish ideal topology, compiled circuit, simulated noise, and physical-device noise.
- Never add an unverified citation, DOI, equation, numerical value, or theorem claim.
- If a proposed formula disagrees with code or symbolic verification, stop and show the discrepancy to the user instead of editing the manuscript.
- User approval gates are G1--G5 as defined in the Architecture note. Between gates, tasks proceed without stopping unless a verification fails; every task records a checkpoint note in the execution log.
- Do not commit unless the user explicitly requests a commit. If requested, stage only the files named in that task.

---

## File Structure

### Files created

- `paper/STYLE-GUIDE.md` — the binding prose rules from spec Section 7, checked at every gate.
- `paper/LITERATURE-AUDIT.md` — verified source ledger with research strand, supported claim, peer-review status, DOI/publisher URL, and BibTeX key.
- `paper/CLAIM-SOURCE-MAP.md` — maps each Section III definition, equation, proposition, and scope caveat to code, data, derivation, and citations.
- `tests/test_paper_claims.py` — executable regression checks for the mathematical statements used in Section III.
- `tests/test_paper_structure.py` — source-level guards for Section III subsection order and prohibited overclaims.

### Files modified

- `paper/qhd.tex:211-363` — replace the current formal-framework block with approved subsections III-A through III-J.
- `paper/references.bib` — add only verified peer-reviewed sources used by Section III.

### Files read as evidence

- `src/game/payoffs.py`
- `src/game/nash.py`
- `src/circuits/ewl.py`
- `src/circuits/n_player.py`
- `src/circuits/topologies.py`
- `src/hardware/mitigation.py`
- `docs/VERIFIED-FACTS.md`
- `docs/formulae.md`
- `docs/findings/2026-07-16-topology-vs-implementation-controls.md`
- `docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md`

---

### Task 1: Establish the Baseline and Non-Destructive Build Gate

**Files:**
- Read: `paper/qhd.tex`
- Read: `paper/references.bib`
- Read: `paper/figs/*`
- Create during verification only: `paper/.qhd-build-check/*`

**Interfaces:**
- Consumes: current complete manuscript, bibliography, and figure directory.
- Produces: a recorded baseline build result and a repeatable non-destructive build command used by every later task.

- [ ] **Step 1: Record the starting state**

Run:

```bash
git status --short -- paper/qhd.tex paper/references.bib paper/figs
```

Expected: `paper/qhd.tex` may be untracked; no assumption is made that the manuscript is committed.

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

Record existing warnings separately. Later tasks must not introduce new warnings.

- [ ] **Step 4: Record baseline page count**

Run:

```bash
pdfinfo .qhd-build-check/qhd.pdf
```

Record the page count in the plan execution notes. The Section III rewrite may add pages, but the final manuscript remains subject to the 16--20 page target.

- [ ] **Step 5: Remove the temporary build directory**

Run:

```bash
rm -rf .qhd-build-check
```

- [ ] **Step 6: Checkpoint note**

Record the baseline build status, warnings, and page count in the execution log. Do not edit prose in this task. The results are presented at gate G1 together with Task 2's deliverables.

---

### Task 2: Freeze the Terminology, Style Guide, and Claim-Scope Contract

**Files:**
- Create: `paper/STYLE-GUIDE.md`
- Create: `paper/CLAIM-SOURCE-MAP.md`
- Create: `tests/test_paper_structure.py`
- Read: `paper/qhd.tex:296-327`
- Read: `src/game/nash.py:1-19,142-216`
- Read: `src/game/payoffs.py:29-118`
- Read: `docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md` (Section 7)

**Interfaces:**
- Consumes: current terminology, implemented metric semantics, and spec Section 7.
- Produces: canonical names, definitions, and binding prose rules used by every later subsection.

- [ ] **Step 1: Create the style guide**

Copy spec Section 7 (7.1 Voice and tense, 7.2 Paragraph discipline, 7.3 Connective tissue, 7.4 Terminology and notation, 7.5 The flow pass) verbatim into `paper/STYLE-GUIDE.md`, prefixed with:

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
| cooperative fixed profile | $(Q_N,\ldots,Q_N)$ evaluated without assuming equilibrium | universal quantum Nash equilibrium | `src/circuits/ewl.py:q_strategy`, `src/game/nash.py` |
| restricted-menu equilibrium | no profitable unilateral deviation within $\{D,H,Q_N\}$ | full-SU(2) equilibrium | `src/game/nash.py:find_pure_nash` |
| circuit-relative payoff gap | fixed-profile mean payoff minus the best restricted classical circuit equilibrium under the same topology/noise path | analytic hardware advantage | `src/game/nash.py:compute_advantage` |
| analytic-baseline advantage | measured or simulated mean payoff minus $(V-C)/N$ | circuit-relative payoff gap | manuscript/hardware estimand |
| ground-state population | $P(0^N)$ | full-state fidelity unless fidelity is actually computed | outcome distribution |
| graph position | structural role such as star hub or leaf | player identity or physical qubit | topology and wiring-permutation evidence |
| payoff vector | $(\pi_1,\ldots,\pi_N)$ | scalar mean | `src/game/payoffs.py:expected_payoff` |
| fairness range | $\max_j\pi_j-\min_j\pi_j$ | complete fairness evidence | derived from payoff vector |
| player floor | $\min_j\pi_j$ | mean welfare | derived from payoff vector |
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

- [ ] **Step 4: Add prohibited phrasing guards**

Create `tests/test_paper_structure.py` with:

```python
from pathlib import Path

PAPER = Path("paper/qhd.tex")


def test_restricted_equilibrium_is_not_overstated():
    text = PAPER.read_text(encoding="utf-8")
    prohibited = [
        "full SU(2) Nash equilibrium on hardware",
        "unrestricted quantum Nash equilibrium",
        "universal quantum Nash equilibrium",
    ]
    for phrase in prohibited:
        assert phrase not in text


def test_ground_state_population_is_not_globally_called_fidelity():
    text = PAPER.read_text(encoding="utf-8")
    assert "ground-state probability (state fidelity)" not in text


def test_no_hype_adjectives():
    text = PAPER.read_text(encoding="utf-8")
    banned = ["groundbreaking", "remarkable", "surprisingly"]
    for word in banned:
        assert word not in text.lower(), f"style guide 7.1 bans '{word}'"
```

- [ ] **Step 5: Run the terminology guards**

Run:

```bash
python -m pytest tests/test_paper_structure.py -v
```

Expected: PASS against the current manuscript or a specific failure that identifies pre-existing wording to fix during the relevant subsection task.

- [ ] **Step 6: Gate G1**

Present the Task 1 baseline record, the terminology table, and the style guide. Ask the user to approve the exact canonical names and the style rules before writing any mathematical subsection. Do not continue past this gate without explicit approval.

---

### Task 3: Create the Section III Literature Audit

**Files:**
- Create: `paper/LITERATURE-AUDIT.md`
- Modify: `paper/references.bib`
- Read: current eight entries in `paper/references.bib`

**Interfaces:**
- Consumes: authoritative publisher pages, Crossref DOI records, and existing verified bibliography entries.
- Produces: verified references available to III-A through III-J.

- [ ] **Step 1: Create the audit schema**

Write:

```markdown
# QHD Literature Audit

| BibTeX key | Research strand | Claim supported | Publication | Year | Peer reviewed | DOI or publisher URL | Verification status |
|---|---|---|---|---:|---|---|---|
```

- [ ] **Step 2: Audit the existing bibliography**

For every existing BibTeX entry:

1. open the DOI or publisher record;
2. verify title, authors, venue, volume, pages/article number, year, and DOI;
3. record the exact paper claim it supports;
4. mark `verified` only after all fields agree.

- [ ] **Step 3: Research the Section III source set**

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

Target at least 18 verified sources for Section III, contributing to the paper-wide 50+ target.

- [ ] **Step 4: Add only cited verified entries to `references.bib`**

For each accepted source, add a complete BibTeX entry with DOI. Do not add a source until a planned Section III sentence names the claim it supports.

- [ ] **Step 5: Check BibTeX-key uniqueness**

Run:

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

Present the source list grouped by strand. The user approves or removes sources before they are cited in manuscript prose. Do not continue past this gate without explicit approval.

---

### Task 4: Add Classical Payoff and Welfare Regression Checks

**Files:**
- Create: `tests/test_paper_claims.py`
- Read: `src/game/payoffs.py`

**Interfaces:**
- Consumes: `outcome_payoff(i, N, V, C)` and `expected_payoff(probs, N, V, C)`.
- Produces: executable support for III-A and III-B.

- [ ] **Step 1: Add the payoff-tensor branch test**

Write:

```python
import numpy as np
import pytest

from game.payoffs import expected_payoff, outcome_payoff


@pytest.mark.parametrize("N", range(2, 9))
def test_n_player_payoff_tensor_branches(N):
    V, C = 4.0, 3.0
    all_dove = outcome_payoff(0, N, V, C)
    all_hawk = outcome_payoff(2**N - 1, N, V, C)
    one_hawk = outcome_payoff(1, N, V, C)

    np.testing.assert_allclose(all_dove, np.full(N, V / N))
    np.testing.assert_allclose(all_hawk, np.full(N, (V - C) / N))
    assert one_hawk[0] == pytest.approx(V)
    np.testing.assert_allclose(one_hawk[1:], np.zeros(N - 1))
```

- [ ] **Step 2: Add the total-welfare identity test**

Write:

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_total_welfare_identity_for_every_basis_state(N):
    V, C = 4.0, 3.0
    for outcome in range(2**N):
        expected_total = V - C if outcome == 2**N - 1 else V
        assert outcome_payoff(outcome, N, V, C).sum() == pytest.approx(expected_total)
```

- [ ] **Step 3: Add the expected-mean identity test**

Write:

```python
@pytest.mark.parametrize("N", range(2, 8))
def test_expected_mean_depends_only_on_all_hawk_probability(N):
    rng = np.random.default_rng(N)
    probs = rng.dirichlet(np.ones(2**N))
    payoff = expected_payoff(probs, N, 4.0, 3.0)
    predicted_mean = 4.0 / N - 3.0 * probs[-1] / N
    assert payoff.mean() == pytest.approx(predicted_mean)
```

- [ ] **Step 4: Run the new checks**

Run:

```bash
python -m pytest tests/test_paper_claims.py -v
```

Expected: PASS.

- [ ] **Step 5: Record evidence mapping**

Add the three test names to the III-A/III-B rows in `paper/CLAIM-SOURCE-MAP.md`.

---

### Task 5: Add Quantum Benchmark, Deviation, and Robustness Checks

**Files:**
- Modify: `tests/test_paper_claims.py`
- Read: `src/circuits/ewl.py`
- Read: `src/circuits/n_player.py`
- Read: `src/circuits/topologies.py`
- Read: `src/game/nash.py`

**Interfaces:**
- Consumes: `q_strategy`, `build_ewl_circuit`, `ghz_entangler`, `expected_payoff`, and `compute_advantage`.
- Produces: executable support for III-F, III-G, III-I, and III-J.

- [ ] **Step 1: Add the GHZ cooperative-output test**

```python
import math

from circuits.ewl import HAWK, q_strategy
from circuits.n_player import build_ewl_circuit
from circuits.topologies import ghz_entangler
from game.nash import compute_advantage


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

- [ ] **Step 2: Add the GHZ payoff and analytic-advantage test**

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_ghz_q_profile_payoff_and_analytic_advantage(N):
    probs = build_ewl_circuit(N, [q_strategy(N)] * N)
    payoff = expected_payoff(probs, N, 4.0, 3.0)
    np.testing.assert_allclose(payoff, np.full(N, 4.0 / N), atol=1e-10)
    assert payoff.mean() - 1.0 / N == pytest.approx(3.0 / N)
```

- [ ] **Step 3: Add the maximal-entanglement Hawk-deviation formula check**

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

- [ ] **Step 4: Add the restricted-equilibrium boundary check**

```python
@pytest.mark.parametrize(
    ("N", "expected_is_nash"),
    [(2, True), (3, True), (4, False), (5, False), (6, False), (7, False)],
)
def test_restricted_equilibrium_boundary(N, expected_is_nash):
    result = compute_advantage(N=N)
    assert result["q_is_nash"] is expected_is_nash
```

- [ ] **Step 5: Add the single-flip welfare check**

```python
@pytest.mark.parametrize("N", range(2, 9))
def test_single_bit_flip_preserves_total_welfare(N):
    all_dove_total = outcome_payoff(0, N, 4.0, 3.0).sum()
    for player in range(N):
        one_hawk_total = outcome_payoff(1 << player, N, 4.0, 3.0).sum()
        assert one_hawk_total == pytest.approx(all_dove_total)
```

- [ ] **Step 6: Run all mathematical checks**

Run:

```bash
python -m pytest tests/test_paper_claims.py -v
```

Expected: PASS before any theorem wording is added.

- [ ] **Step 7: Checkpoint note**

Record the exact tested formulas and finite $N$ range in the execution log, together with a proposed labeling: which statements may be labeled propositions and which must remain computational results. This labeling is confirmed with the user at gate G3 alongside the III-A style review.

---

### Task 6: Rewrite III-A, Notation and the Classical Payoff Tensor

**Files:**
- Modify: `paper/qhd.tex:213-253`
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Modify only if needed: `paper/references.bib`
- Test: `tests/test_paper_claims.py::test_n_player_payoff_tensor_branches`

**Interfaces:**
- Consumes: approved terminology, style guide, and tested payoff-tensor branches.
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
python -m pytest tests/test_paper_claims.py::test_n_player_payoff_tensor_branches -v
```

Expected: PASS.

- [ ] **Step 7: Compile and inspect**

Run the four-pass temporary build from Task 1. Inspect the page containing III-A for equation overflow, unexplained symbols, paragraph density, and every style-guide 7.1--7.4 rule.

- [ ] **Step 8: Gate G3 — style calibration**

Show the III-A source, the rendered page, and the Task 5 proposition-labeling proposal. This gate exists so the user corrects voice, density, and depth **once, early**, instead of at every subsection. Apply the user's calibration feedback to III-A before continuing; it becomes binding precedent for III-B through III-J.

---

### Task 7: Rewrite III-B, Classical Equilibrium and Welfare Geometry

**Files:**
- Modify: `paper/qhd.tex` immediately after III-A
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Test: `tests/test_paper_claims.py::test_total_welfare_identity_for_every_basis_state`
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
  tests/test_paper_claims.py::test_expected_mean_depends_only_on_all_hawk_probability \
  -v
```

Expected: PASS.

- [ ] **Step 7: Compile, inspect, checkpoint**

Build in `.qhd-build-check`, inspect proposition placement, equation width, and style-guide compliance. Record a checkpoint note and continue.

---

### Task 8: Rewrite III-C, Quantum Strategies and the EWL Protocol

**Files:**
- Modify: `paper/qhd.tex:255-274`
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Modify only with verified entries: `paper/references.bib`
- Read: `src/circuits/ewl.py:20-121`
- Read: `src/circuits/n_player.py:53-102`

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

State that $Q_N$ is GHZ-derived and is held fixed across topologies for controlled comparison.

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

Check matrix width in IEEE two-column format, style-guide compliance, and record a checkpoint note.

---

### Task 9: Rewrite III-D, Entanglement Topologies and Graph Symmetry

**Files:**
- Modify: `paper/qhd.tex:275-294`
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Modify only with verified entries: `paper/references.bib`
- Read: `src/circuits/topologies.py`
- Read: `src/circuits/topology_graphs.py`

**Interfaces:**
- Consumes: EWL operator $J_T$ from III-C.
- Produces: formal topology families and the symmetry principle used by III-J and later fairness sections.

- [ ] **Step 1: Define the GHZ operator**

```latex
\begin{equation}
J_{\mathrm{GHZ}}(\gamma)
=\cos\frac{\gamma}{2}I^{\otimes N}
+i\sin\frac{\gamma}{2}X^{\otimes N}.
\end{equation}
```

- [ ] **Step 2: Define pairwise graph entanglers**

```latex
\begin{equation}
J_G(\gamma)
=\prod_{(r,s)\in E(G)}
\exp\left(i\frac{\gamma}{2}X_rX_s\right).
\end{equation}
```

Define the ring $C_N$, star $S_N$ with hub 0, and complete graph $K_N$ edge sets. Add a `% FIGURE F2 ANCHOR` comment marking where the topology gallery from spec Section 8.2 will be placed by the figure plan.

- [ ] **Step 3: Define the W-state construction without hiding its design choice**

State the implemented involution $S_W$ and

```latex
J_W(\gamma)=\cos(\gamma/2)I+i\sin(\gamma/2)S_W.
```

Explicitly identify the interpolation as the construction used in this study, not the unique possible W entangler.

- [ ] **Step 4: State and derive permutation covariance**

Use a permutation operator $R_\sigma$ and derive:

```latex
R_\sigma J_G R_\sigma^\dagger=J_{\sigma(G)}.
```

Then explain the payoff-vector permutation under relabeling.

- [ ] **Step 5: State the graph-orbit corollary**

Under symmetric local strategies and permutation-symmetric noise, players in the same automorphism orbit have equal expected payoffs.

- [ ] **Step 6: Verify operator statements numerically**

Add a test that checks unitarity for every entangler at $N=2,3,4$ and checks that ring and fully connected coincide at $N=3$.

- [ ] **Step 7: Compile, inspect, checkpoint**

Ensure the topology subsection explains the graphs before gate counts. Record a checkpoint note.

---

### Task 10: Rewrite III-E, Payoff, Advantage, Equilibrium, and Fairness Metrics

**Files:**
- Modify: `paper/qhd.tex:296-317`
- Modify: `paper/CLAIM-SOURCE-MAP.md`
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

The profile passes the restricted test iff every $g_j(a)\ge0$.

- [ ] **Step 3: Define both advantage metrics separately**

Insert separate equations and a two-row comparison table for analytic-baseline advantage and circuit-relative payoff gap.

- [ ] **Step 4: Define fairness summaries**

```latex
S_\pi=\max_j\pi_j-\min_j\pi_j,
\qquad
F_\pi=\min_j\pi_j.
```

State that $\boldsymbol\pi$ remains the primary evidence.

- [ ] **Step 5: Run wording guards**

```bash
python -m pytest tests/test_paper_structure.py -v
```

Expected: PASS.

- [ ] **Step 6: Compile, inspect, checkpoint**

Check that no metric is used before definition. Record a checkpoint note.

---

### Task 11: Rewrite III-F, GHZ Cooperative Benchmark

**Files:**
- Modify: `paper/qhd.tex` after III-E
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Test: GHZ tests in `tests/test_paper_claims.py`

**Interfaces:**
- Consumes: $Q_N$, $J_{\mathrm{GHZ}}$, payoff tensor, and analytic baseline.
- Produces: the cooperative payoff theorem used throughout the rest of the paper.

- [ ] **Step 1: Write the phase-cancellation derivation**

Show the action of $J_{\mathrm{GHZ}}(\pi/2)$ on $|0^N\rangle$, the equal phase gained by the $|0^N\rangle$ and $|1^N\rangle$ branches under $Q_N^{\otimes N}$, and the recovery of $|0^N\rangle$ after $J^\dagger$.

- [ ] **Step 2: State the benchmark proposition**

```latex
\begin{proposition}[GHZ cooperative benchmark]
At $\gamma=\pi/2$, the profile $Q_N^{\otimes N}$ under the GHZ entangler produces $p(0^N)=1$. Hence
\begin{equation}
\pi_j=\frac{V}{N},
\qquad
\Delta_{\mathrm{ana}}=\frac{C}{N}.
\end{equation}
\end{proposition}
```

- [ ] **Step 3: Specialize to the live parameters**

State $\pi_j=4/N$ and $\Delta_{\mathrm{ana}}=3/N$ for $V=4,C=3$.

- [ ] **Step 4: Run the focused tests**

```bash
python -m pytest tests/test_paper_claims.py -k "ghz_q_profile" -v
```

Expected: PASS.

- [ ] **Step 5: Compile, inspect, checkpoint**

Check proof length, notation continuity, and page density. Record a checkpoint note.

---

### Task 12: Rewrite III-G, Incentive Compatibility and the Entanglement-Angle Boundary

**Files:**
- Modify: `paper/qhd.tex` after III-F
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Test: deviation and equilibrium tests in `tests/test_paper_claims.py`

**Interfaces:**
- Consumes: cooperative benchmark and deviation-gap definition.
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

- [ ] **Step 2: Derive the Dove deviation**

Derive its payoff and show that it does not bind the restricted equilibrium under the stated parameters.

- [ ] **Step 3: Derive the equilibrium inequality**

Compare the Hawk-deviation payoff with $V/N$ and establish the boundary at $N=2,3$ versus $N\ge4$.

- [ ] **Step 4: Derive and test the general-$\gamma$ formula**

Use the candidate formula

```latex
\pi_j(H,Q_{N,-j};\gamma)
=V\left[1-\sin^2\gamma\,\sin^2\left(\frac{\pi}{N}\right)\right].
```

Before adding it, numerically compare it with `build_ewl_circuit` for $N=2,3,4,5$ and $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$. Any mismatch blocks the manuscript edit.

- [ ] **Step 5: Run the restricted-equilibrium tests**

```bash
python -m pytest tests/test_paper_claims.py -k "hawk_deviation or restricted_equilibrium" -v
```

Expected: PASS.

- [ ] **Step 6: Add the honesty boundary**

State that the result proves equilibrium only in the discrete menu $\{D,H,Q_N\}$ and does not establish equilibrium against arbitrary SU(2) deviations.

- [ ] **Step 7: Gate G4 — high-stakes review**

This subsection carries the paper's central game-theoretic claim. Show the derivation, the numerical cross-check table, and the rendered pages to the user. Do not continue past this gate without explicit approval.

---

### Task 13: Rewrite III-H, Circuit Realization, Noise Channels, and Hardware Estimators

*(Merged subsection: the former III-H circuit/noise material and III-I estimator material now form one implementation-layer subsection, per spec Section 6.)*

**Files:**
- Modify: `paper/qhd.tex:286-327` and the block following it
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Modify only with verified entries: `paper/references.bib`
- Read: topology implementations and noise-path code
- Read: `src/hardware/mitigation.py`

**Interfaces:**
- Consumes: ideal entanglers from III-D and noisy outcome distributions.
- Produces: the ideal/circuit/simulation/device layer distinction, formal noise channels, and the estimators later applied in Section VI.

- [ ] **Step 1: Introduce the four-layer distinction**

Use a compact table with rows for ideal operator, compiled circuit, simulated channel, and physical device.

- [ ] **Step 2: Define depolarizing channels**

```latex
\begin{equation}
\mathcal D_\lambda^{(d)}(\rho)
=(1-\lambda)\rho
+\lambda\,\mathrm{Tr}(\rho)\frac{I_d}{d},
\end{equation}
```

with $d=2$ and $d=4$ for one- and two-qubit channels.

- [ ] **Step 3: State the implemented assignment rule**

Document how $p$ and the two-qubit ratio are applied to the pinned gate basis. Verify exact semantics against the noise implementation before writing.

- [ ] **Step 4: Explain circuit-cost confounding**

State why two abstract topologies can incur different routed two-qubit costs and why production-circuit robustness cannot automatically be attributed to graph topology alone.

- [ ] **Step 5: Define the assignment matrices**

```latex
A_j[m,t]=\Pr(\text{measure }m\mid\text{prepared }t),
\qquad
A=\bigotimes_jA_j.
```

- [ ] **Step 6: Define constrained probability reconstruction**

```latex
\widehat p
=\arg\min_{p\ge0,\,\mathbf1^Tp=1}
\|Ap-p_{\mathrm{meas}}\|_2^2.
```

Confirm the manuscript description matches the implementation.

- [ ] **Step 7: Define local gate folding and weighted ZNE**

```latex
y_\lambda=a+b\lambda+\epsilon_\lambda,
\qquad
(\widehat a,\widehat b)
=\arg\min_{a,b}\sum_\lambda
\frac{(y_\lambda-a-b\lambda)^2}{\sigma_\lambda^2},
```

with $\lambda\in\{1,3,5\}$ and extrapolated estimate $\widehat y(0)=\widehat a$.

- [ ] **Step 8: Define uncertainty scope**

State which variance enters the weighted fit and explicitly separate shot, fit, run, and calibration-epoch uncertainty.

- [ ] **Step 9: Cite primary sources**

Use verified peer-reviewed sources for depolarizing channels, NISQ noise, compilation/routing effects, measurement mitigation, ZNE, and local folding.

- [ ] **Step 10: Compile, inspect, checkpoint**

Check the table and channel equations in two-column layout. Ensure the subsection defines estimators without reporting results. This is the longest subsection in Section III; verify it still reads as one question ("what stands between the ideal operator and the measured number?") with two halves, not two unrelated topics glued together. Record a checkpoint note.

---

### Task 14: Rewrite III-I, Structural Robustness of the Payoff Observable

**Files:**
- Modify: `paper/qhd.tex` after III-H
- Modify: `paper/CLAIM-SOURCE-MAP.md`
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

Use plain language to distinguish stable payoff expectation from preserved quantum state.

- [ ] **Step 4: Run the focused test**

```bash
python -m pytest tests/test_paper_claims.py::test_single_bit_flip_preserves_total_welfare -v
```

Expected: PASS.

- [ ] **Step 5: Compile, inspect, checkpoint**

Check that the caveat is adjacent to the corollary. Record a checkpoint note.

---

### Task 15: Rewrite III-J, Player-Level Redistribution and Position-Locked Fairness

**Files:**
- Modify: `paper/qhd.tex` after III-I
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Modify only with verified entries: `paper/references.bib`
- Read: star topology and wiring-permutation evidence

**Interfaces:**
- Consumes: payoff vector, fairness metrics, permutation covariance, and observable robustness.
- Produces: the fairness mechanism later evaluated in simulation and hardware.

- [ ] **Step 1: State the central tension**

Explain that conservation of mean welfare does not conserve each player's payoff.

- [ ] **Step 2: Derive payoff-vector covariance under relabeling**

Show that relabeling players and graph vertices permutes $\boldsymbol\pi$ rather than changing its multiset of ideal values.

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

State the analytical symmetry prediction here. Reserve the empirical claim that the effect survives physical-qubit reassignment for Section VI-G.

- [ ] **Step 6: Cite network-game and fairness literature**

Use verified sources that discuss role-dependent or network-position-dependent outcomes. Do not claim those sources studied this quantum mechanism.

- [ ] **Step 7: Compile, inspect, checkpoint**

Check how this subsection transitions to analytical predictions. Record a checkpoint note.

---

### Task 16: Section III Flow Pass, Integration, and Verification

**Files:**
- Modify: `paper/qhd.tex` Section III as needed for flow and transitions
- Modify: `paper/CLAIM-SOURCE-MAP.md`
- Modify: `paper/LITERATURE-AUDIT.md`
- Modify: `tests/test_paper_structure.py`
- Test: `tests/test_paper_claims.py`
- Test: `tests/test_paper_structure.py`

**Interfaces:**
- Consumes: drafted III-A through III-J subsections.
- Produces: one coherent, compilable mathematical framework ready for Section IV planning.

- [ ] **Step 1: Run the full mathematical test suite**

```bash
python -m pytest tests/test_paper_claims.py tests/test_paper_structure.py -v
```

Expected: zero failures.

- [ ] **Step 2: Check subsection order**

Extend `tests/test_paper_structure.py` with the exact approved order:

```python
def test_mathematical_framework_subsection_order():
    text = PAPER.read_text(encoding="utf-8")
    headings = [
        "Notation and the Classical $N$-Player Payoff Tensor",
        "Classical Equilibrium and Welfare Geometry",
        "Quantum Strategies and the EWL Protocol",
        "Entanglement Topologies and Graph Symmetry",
        "Expected Payoff, Advantage, Equilibrium, and Fairness",
        "GHZ Cooperative Benchmark",
        "Incentive Compatibility and the Entanglement-Angle Boundary",
        "Circuit Realization, Noise Channels, and Hardware Estimators",
        "Structural Robustness of the Payoff Observable",
        "Player-Level Redistribution and Position-Locked Fairness",
    ]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)
```

- [ ] **Step 3: Run the mandatory flow pass (style guide 7.5)**

Render the full PDF to page images and read Section III top to bottom in the rendered form, not the source. Then:

1. rewrite subsection openings/closings so each answers the question the previous one raised;
2. verify one authorial voice: consistent tense, "we" usage, and terminology throughout;
3. verify every subsection opener says why the reader needs it now, and every closer hands off;
4. verify every displayed equation has a plain-language reading within two sentences;
5. fix every violation found; re-compile.

- [ ] **Step 4: Audit notation**

Search Section III for every symbol introduced. Confirm each is defined before its first use and used consistently: $x$, $k$, $P_j$, $\pi_j$, $\bar\pi$, $J_T$, $Q_N$, $g_j$, $\Delta_{\mathrm{ana}}$, $\Delta_{\mathrm{circ}}$, $S_\pi$, $F_\pi$, $A$, $\lambda$, and $\gamma$.

- [ ] **Step 5: Audit evidence labels**

For every proposition, computational result, and implementation definition, confirm that `paper/CLAIM-SOURCE-MAP.md` names its proof/test/code/citation source.

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

Record the new total page count and the pages occupied by Section III. If Section III alone makes the 16--20 page target impossible, identify repetition or move only non-core implementation detail to Appendix A; do not remove core derivations.

- [ ] **Step 8: Run a clean four-pass build**

Use the non-destructive build command from Task 1. Expected: exit code 0, no undefined citations, and no undefined references.

- [ ] **Step 9: Gate G5 — Section III approval**

Present:

1. the complete Section III source;
2. rendered pages;
3. test output;
4. citation audit;
5. page-count change;
6. flow-pass findings and fixes;
7. any remaining concerns.

Wait for explicit approval.

- [ ] **Step 10: Optional checkpoint commit**

Only if the user explicitly requests a commit:

```bash
git add paper/qhd.tex paper/references.bib paper/STYLE-GUIDE.md paper/LITERATURE-AUDIT.md paper/CLAIM-SOURCE-MAP.md tests/test_paper_claims.py tests/test_paper_structure.py
git commit -m "paper: rewrite mathematical framework"
```

Do not add an attribution footer.

---

### Task 17: Close Phase 1 and Plan the Next Phases

**Files:**
- Read: approved Section III in `paper/qhd.tex`
- Create later, only after approval: `docs/superpowers/plans/2026-07-31-qhd-analytical-predictions-rewrite.md`
- Create later, only after Section IV approval: `docs/superpowers/plans/2026-07-31-qhd-figure-redesign.md`

**Interfaces:**
- Consumes: user-approved Section III.
- Produces: a separate implementation plan for Section IV, and (after Section IV, which fixes the P1--P8 ledger) a figure-redesign plan implementing spec Section 8.

- [ ] **Step 1: Confirm the Section III approval record**

Record the user's explicit approval and any accepted wording exceptions in the execution notes.

- [ ] **Step 2: List the verified predictions now available**

The list must be generated from the approved Section III and include only claims with completed tests or derivations.

- [ ] **Step 3: Write the Section IV plan**

Create a new plan covering IV-A through IV-E of the consolidated spec, with each prediction mapped to its Section III equation/proposition and later simulation/hardware test. The Section IV plan must end by scheduling the figure-redesign plan (spec Section 8), because figures F1/F2 and all caption rewrites depend on the P1--P8 ledger that Section IV creates.

- [ ] **Step 4: Stop before implementation**

Present the Section IV plan to the user. Do not rewrite Section IV until the user approves that new plan.

---

## Plan Self-Review Checklist

- [ ] Every Section III subsection in the consolidated spec (III-A through III-J, ten subsections) has exactly one rewrite task.
- [ ] Every central formula has a test, derivation gate, or implementation comparison.
- [ ] Citation research is separated from prose drafting and requires authoritative verification.
- [ ] The style guide exists before any prose is drafted, and every drafting task checks it.
- [ ] Approval gates are exactly G1--G5; no per-subsection stop outside III-A (calibration) and III-G (high stakes).
- [ ] The flow pass is a mandatory, named step before Section III approval.
- [ ] Figure anchors (F1, F2) are placed but no figures are generated in this plan.
- [ ] The two advantage metrics remain distinct.
- [ ] Restricted equilibrium remains explicitly finite-menu.
- [ ] Player-level fairness remains vector-first.
- [ ] Ideal topology and implementation cost remain distinct.
- [ ] Builds are non-destructive and do not overwrite the user's existing PDF.
- [ ] No commit occurs without explicit user authorization.
- [ ] The plan contains no placeholders or deferred unspecified work.
