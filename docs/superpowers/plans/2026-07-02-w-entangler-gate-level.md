# Faithful Gate-Level W Entangler (T8) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the transpiled-dense-unitary W entangler fallback with an exact gate-level circuit, then re-run the Month-4 noise sweep so the RQ3 GHZ-vs-W headline no longer carries the "approximate" caveat.

**Architecture:** `J_W(gamma) = T · MCU(gamma) · T†` (exact, up to global phase): `T` is a CRy+CNOT cascade that maps `|0...01>` to `|W>` while provably fixing `|0...0>`; `MCU` is a single anti-controlled `e^{-i·gamma/2}·RX(-gamma)` on qubit 0. Approved spec with full derivation: `docs/superpowers/specs/2026-07-02-w-entangler-gate-level-design.md`.

**Tech Stack:** Python 3.10+, Qiskit 1.3.2 (pinned), qiskit-aer 0.14.2 (pinned), pytest.

## Global Constraints

- Do NOT modify `src/circuits/topologies.py` (the dense `w_entangler` stays the authoritative reference), `src/circuits/noise.py`, or `src/experiment/topology_registry.py`.
- `w_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit` keeps its exact name and signature — the registry wires it by reference.
- Sign conventions: project uses `exp(+i·gamma/2·...)`; Qiskit `RX(theta) = exp(-i·theta/2·X)`, hence `rx(-gamma)`.
- Qubit ordering is Qiskit little-endian: `|e_0>` (excitation on qubit 0) is basis index 1.
- Run tests from the repo root with plain `pytest ...` — `pyproject.toml` sets `pythonpath = ["src", "scripts"]` for pytest only.
- Commit after every task. NEVER add a `Co-Authored-By` trailer.
- Work on branch `dev`.

---

### Task 1: W-prep cascade `_w_prep_cascade`

**Files:**
- Modify: `src/circuits/gate_level.py` (add one import, one function)
- Test: `tests/test_gate_level.py` (append two tests)

**Interfaces:**
- Consumes: `circuits.topologies._w_state(N) -> np.ndarray` (already exists — the dense W statevector, all amplitudes `+1/sqrt(N)` on single-excitation states).
- Produces: `_w_prep_cascade(N: int) -> QuantumCircuit` in `circuits.gate_level` — Task 2 composes it and its `.inverse()`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_gate_level.py` (note: this file currently imports only from `config` and `experiment.topology_registry`; add the new imports right after the existing ones near the top of the file):

```python
import numpy as np
from qiskit.quantum_info import Statevector

from circuits.gate_level import _w_prep_cascade
from circuits.topologies import _w_state
```

And at the bottom of the file:

```python
# --- T8: W-prep cascade properties (spec D-T8.3) -------------------------------


@pytest.mark.parametrize("N", [2, 3, 4, 5])
def test_w_prep_maps_excitation_to_w_state(N: int) -> None:
    """T|e_0> = |W> EXACTLY (real +1/sqrt(N) amplitudes, not just up to phase).

    Exactness matters: the conjugation J_W = T . MCU . T-dagger needs T to hit
    _w_state on the nose, otherwise S_W's off-diagonal blocks pick up phases.
    """
    sv = Statevector.from_int(1, dims=2**N).evolve(_w_prep_cascade(N))
    np.testing.assert_allclose(sv.data, _w_state(N), atol=1e-12)


@pytest.mark.parametrize("N", [2, 3, 4, 5])
def test_w_prep_fixes_vacuum(N: int) -> None:
    """T|0...0> = |0...0> exactly — every cascade gate is controlled on a |0>.

    This is what makes the conjugation argument exact with no correction terms
    (spec D-T8.3); a drifted vacuum silently corrupts J_W's |0><W| block.
    """
    sv = Statevector.from_int(0, dims=2**N).evolve(_w_prep_cascade(N))
    expected = np.zeros(2**N, dtype=complex)
    expected[0] = 1.0
    np.testing.assert_allclose(sv.data, expected, atol=1e-12)
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `pytest tests/test_gate_level.py -v -k w_prep`
Expected: collection ERROR for the whole file — `ImportError: cannot import name '_w_prep_cascade'` (the import at the top fails before any test runs). That is the failing state.

- [ ] **Step 3: Implement `_w_prep_cascade`**

In `src/circuits/gate_level.py`, add `import math` below `from __future__ import annotations`, then add above `w_gate_circuit`:

```python
def _w_prep_cascade(N: int) -> QuantumCircuit:
    """Cascade T with T|e_0> = |W> (all real +1/sqrt(N) amplitudes) and T|0..0> = |0..0>.

    Block k (k = 0..N-2): CRy(theta_k) control k -> target k+1, then CNOT
    control k+1 -> target k, with theta_k = 2*arccos(1/sqrt(N-k)). Each block
    moves sin(theta_k/2) of the excitation amplitude from qubit k to k+1,
    leaving cos(theta_k/2) * prod_{m<k} sin(theta_m/2) = 1/sqrt(N) behind.
    Every gate is controlled on a qubit that is |0> in the all-zeros state, so
    T fixes |0...0> exactly — required by the conjugation construction
    (spec 2026-07-02-w-entangler-gate-level-design.md, D-T8.3).
    """
    qc = QuantumCircuit(N)
    for k in range(N - 1):
        theta = 2.0 * math.acos(1.0 / math.sqrt(N - k))
        qc.cry(theta, k, k + 1)
        qc.cx(k + 1, k)
    return qc
```

- [ ] **Step 4: Run the new tests to verify they pass**

Run: `pytest tests/test_gate_level.py -v -k w_prep`
Expected: 8 PASSED

- [ ] **Step 5: Run the full gate-level suite (no regressions)**

Run: `pytest tests/test_gate_level.py -v`
Expected: all PASSED (the existing W equivalence tests still exercise the old transpiled fallback — unchanged so far)

- [ ] **Step 6: Commit**

```bash
git add src/circuits/gate_level.py tests/test_gate_level.py
git commit -m "Feat: T8 W-prep cascade with exact excitation/vacuum properties"
```

---

### Task 2: Exact `w_gate_circuit` via conjugation

**Files:**
- Modify: `src/circuits/gate_level.py` (rewrite `w_gate_circuit`, module docstring, imports)
- Test: `tests/test_gate_level.py` (append one test)

**Interfaces:**
- Consumes: `_w_prep_cascade(N: int) -> QuantumCircuit` from Task 1.
- Produces: `w_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit` — same name/signature as today; `experiment.topology_registry` and `circuits.noise` pick it up with zero changes.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_gate_level.py`:

```python
def test_w_gate_circuit_matches_dense_n5() -> None:
    """Exact W construction at the noise sweep's max N (existing tests stop at 4).

    Operator.equiv is global-phase tolerant but branch-relative-phase strict:
    it catches a missing e^{-i*gamma/2} on the MCU target or a wrong ctrl_state.
    """
    dense = Operator(resolve("w", 5)(5, GAMMA))
    gate = Operator(resolve_gate_circuit("w", 5, GAMMA))
    assert gate.equiv(dense)
```

- [ ] **Step 2: Run it — this test passes ALREADY (old fallback is also correct, just not faithful)**

Run: `pytest tests/test_gate_level.py -v -k n5`
Expected: 1 PASSED. That is fine — this test is a regression guard for the rewrite, not a red-first driver; the real change is structural (faithful gates instead of synthesis). Verify it runs, then proceed.

- [ ] **Step 3: Rewrite `w_gate_circuit` and clean up the module**

In `src/circuits/gate_level.py`:

(a) Replace the entire `w_gate_circuit` function with:

```python
def w_gate_circuit(N: int, gamma: float = GAMMA) -> QuantumCircuit:
    """Exact W entangler J_W(gamma) = exp(i*gamma/2 * S_W) as elementary gates.

    Conjugation construction (spec 2026-07-02-w-entangler-gate-level-design.md):
    S_W acts as X on span{|0...0>, |W>} and as identity on the complement, so
    with T = _w_prep_cascade (T|e_0> = |W>, T|0...0> = |0...0>):

        J_W = T . exp(i*gamma/2 * S') . T-dagger

    where S' swaps |0...0> <-> |e_0>. That exponential is an anti-controlled
    (qubits 1..N-1 all |0>) gate U = e^{-i*gamma/2} * RX(-gamma) on qubit 0,
    times a global phase e^{i*gamma/2}. The e^{-i*gamma/2} inside U is the
    RELATIVE phase between the control branches and is required; RX(-gamma) =
    exp(+i*gamma/2 * X) matches the project sign convention. Gate count is
    physical: W-prep + one collective interaction + un-prep, O(N) blocks.
    """
    prep = _w_prep_cascade(N)
    u = QuantumCircuit(1, global_phase=-gamma / 2.0)
    u.rx(-gamma, 0)
    mcu = u.to_gate(label="expWX").control(N - 1, ctrl_state=0)
    qc = QuantumCircuit(N, global_phase=gamma / 2.0)
    qc.compose(prep.inverse(), inplace=True)
    # .control() puts controls first: qubits 1..N-1 are the (negative) controls,
    # qubit 0 is the rotation target.
    qc.append(mcu, list(range(1, N)) + [0])
    qc.compose(prep, inplace=True)
    return qc
```

(b) Delete the now-dead module-level constants and imports: `_PINNED_BASIS`, `_PINNED_OPT_LEVEL`, `from qiskit import transpile`, `UnitaryGate` (keep `RXXGate`), and `from circuits.topologies import w_entangler`. The import block becomes:

```python
import math

from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import RXXGate

from circuits.topology_graphs import topology_graph
from config import GAMMA
```

(c) Replace the last paragraph of the module docstring (the two sentences starting "W has no compact native-gate form, so w_gate_circuit transpiles ..." and ending "... labelled \"approximate\".") with:

```
W is built exactly by conjugation: J_W = T . MCU . T-dagger, where T is the
CRy+CNOT W-prep cascade (fixes |0...0>) and MCU is an anti-controlled
exp(i*gamma/2 * X) on qubit 0 — see
docs/superpowers/specs/2026-07-02-w-entangler-gate-level-design.md.
```

- [ ] **Step 4: Run the gate-level suite**

Run: `pytest tests/test_gate_level.py -v`
Expected: all PASSED — in particular `test_gate_circuit_matches_dense[2|3|4-w]`, `test_gate_circuit_gamma_dependence[w]`, and `test_w_gate_circuit_matches_dense_n5` now validate the NEW construction against the authoritative dense matrix. If a W equivalence test fails, the bug is in exactly one of: CRy angle, cascade CNOT direction, `ctrl_state`, MCU qubit order, or the `global_phase=-gamma/2` on `u` — the Task-1 prep tests isolate cascade bugs from MCU bugs.

- [ ] **Step 5: Run the whole test suite (noise path end-to-end)**

Run: `pytest`
Expected: all PASSED. `tests/test_noise.py::test_p0_equals_statevector` re-validates the noisy pipeline with the new W circuit at p=0 against the exact statevector result.

- [ ] **Step 6: Commit**

```bash
git add src/circuits/gate_level.py tests/test_gate_level.py
git commit -m "Feat: T8 exact gate-level W entangler via prep-conjugated anti-controlled RX"
```

---

### Task 3: Remove the "approximate" W labelling (code, configs, docs)

W noise results are no longer approximate, so every label added under Month-4
D2/1A comes out. This must land BEFORE the Task-4 re-run so the regenerated
report/plots are label-free.

**Files:**
- Modify: `src/experiment/plots.py`, `src/experiment/report.py`, `experiments/noise-sweep.yaml`, `experiments/config.yaml`, `docs/formulae.md`, `TODOS.md`, `docs/superpowers/specs/2026-07-01-noise-analysis-design.md`
- Test: existing suite (no new tests — pure label removal)

**Interfaces:**
- Consumes: nothing from Tasks 1-2 (text-only), but ordered after them so the statements become true.
- Produces: label-free report/plot generators for Task 4.

- [ ] **Step 1: `src/experiment/plots.py`**

(a) Line 26: delete `from experiment.topology_registry import canonical  # noqa: E402` — after (c) below it has no remaining use in this module.

(b) In the `_noise_surfaces` docstring, delete the final sentence: `W is titled "approximate" — its gate-level circuit is transpiler synthesis, not a physical W-prep circuit (spec D2).`

(c) Replace the two title lines

```python
        approx = " (approximate)" if canonical(topo) == "w" else ""
        ax.set_title(f"Advantage surface — {topo}{approx}")
```

with

```python
        ax.set_title(f"Advantage surface — {topo}")
```

- [ ] **Step 2: `src/experiment/report.py`** (keep the `canonical` import — still used by the GHZ-vs-W ordering block and elsewhere)

(a) In `_noise_findings`'s docstring, delete the final sentence: `All W rows are labelled approximate: W's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2).`

(b) Replace

```python
        label = f"{topo} _(approximate)_" if canonical(topo) == "w" else topo
```

with

```python
        label = topo
```

(c) Replace the headline header lines

```python
            "**GHZ vs W noise robustness (RQ3 headline — measured, not assumed; "
            "W is approximate, see above):**",
```

with

```python
            "**GHZ vs W noise robustness (RQ3 headline — measured, not assumed):**",
```

(d) In `_cell_detail`, delete the whole approximate-note block:

```python
    if r.cell.noise_p > 0 and canonical(r.cell.topology) == "w":
        lines += [
            "_W noise results are **approximate**: the W entangler's gate-level "
            "circuit is transpiler synthesis, not a physical W-prep circuit "
            "(Month-4 spec D2)._",
            "",
        ]
```

- [ ] **Step 3: `experiments/noise-sweep.yaml`**

(a) Delete the header comment block (3 lines): `# NOTE: W noise results are APPROXIMATE — W has no compact gate-level form, so` / `# its gate count is transpiler synthesis, not a physical W-prep circuit (spec` / `# D2). The report labels every W row accordingly.`

(b) In `experiment.description`, delete the trailing sentence `W results approximate (transpiled-unitary entangler, spec D2).`

- [ ] **Step 4: `experiments/config.yaml`** — delete the 3-line NOTE (lines starting `# NOTE: W-topology noise results are APPROXIMATE ...` through `... (Month-4 spec D2).`)

- [ ] **Step 5: `docs/formulae.md`** — replace the W bullet under "Gate-level entanglers"

```
- **W:** the dense `S_W` reflection has no compact native-gate form; it is
  **transpiled** to `{u, cx}` (pinned). Its gate count is synthesis-derived, so
  every W noise result is labelled **approximate** (spec D2).
```

with

```
- **W:** exact conjugation `J_W = T·MCU·T†` — `T` is the CRy+CNOT W-prep
  cascade (`θ_k = 2·arccos(1/√(N−k))`, fixes `|0…0⟩`), `MCU` an anti-controlled
  `exp(+iγ/2·X)` on qubit 0 (T8 spec, 2026-07-02).
```

- [ ] **Step 6: `TODOS.md`** — delete the entire "Faithful gate-level W entangler" section (heading through its `**Depends on:**` line), keeping "Noise-aware strategy optimization".

- [ ] **Step 7: `docs/superpowers/specs/2026-07-01-noise-analysis-design.md`** — in Implementation Tasks, change

```
- [ ] **T8 (P3)** — TODO: faithful gate-level W entangler (D2)
```

to

```
- [x] **T8 (P3)** — faithful gate-level W entangler (D2) — done, see
  `2026-07-02-w-entangler-gate-level-design.md`; the D2 "approximate" labelling
  is retired.
```

- [ ] **Step 8: Verify nothing stale remains and the suite passes**

Run: `grep -ri approximate src/ experiments/ TODOS.md | grep -vi "approximation"` (or the Grep tool) — expected: no W-labelling hits remain in `src/` or `experiments/`.
Run: `pytest`
Expected: all PASSED (report/plot tests, if any assert on labels, get fixed as part of this task — check failures and update the corresponding assertion text).

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "Chore: retire the D2 'approximate' W labelling (T8 makes W exact)"
```

---

### Task 4: Re-run the noise sweep and update README with the new measured results

W's gate count — hence its noise cost — changed, so all W noise numbers change.
The RQ3 ordering must be RE-READ from the new run, never carried forward.

**Files:**
- Create: `results/noise-robustness/<new timestamp>/` (generated by the run)
- Modify: `README.md` (§9 table row + "Month 4 — Noise Robustness (RQ3)" subsection)

**Interfaces:**
- Consumes: everything from Tasks 1-3.
- Produces: the updated RQ3 headline for the paper.

- [ ] **Step 1: Run the sweep** (long job — density-matrix sims for N up to 5 across 11 p values × 3 topologies; the previous run took roughly an hour-scale wall clock; run in background and wait)

```bash
PYTHONPATH=src python scripts/run_experiment.py --config experiments/noise-sweep.yaml
```

(PowerShell: `$env:PYTHONPATH='src'; python scripts/run_experiment.py --config experiments/noise-sweep.yaml`)

Expected: a new `results/noise-robustness/<ts>/` with `report.md`, `results.json`, `results.csv`, `config.snapshot.yaml`, `plots/` — and NO "approximate" strings anywhere in `report.md`.

- [ ] **Step 2: Read the new p\* table and GHZ-vs-W ordering** from `results/noise-robustness/<ts>/report.md` ("Noise thresholds p\*" section). Sanity checks before trusting it: every p=0 row must reproduce the Month-3 noiseless advantage (compare a couple of cells against the previous run's p=0 rows — they must be identical, since Tasks 1-3 didn't touch the noiseless path); GHZ and ring rows must match the previous run closely (their circuits are unchanged; tiny drift means something is wrong — stop and investigate rather than shipping). Only the W rows may move.

- [ ] **Step 3: Update `README.md`**

(a) §9 results table, "Noise robustness surface" row: replace the note's `GHZ crosses zero before W at every N≥3 (W approximate)` with whatever the NEW measured ordering is (drop "(W approximate)"), and keep the test-count reference accurate.

(b) "Month 4 — Noise Robustness (RQ3)" subsection: point the "Full run:" line at the new `results/noise-robustness/<ts>/`; replace the W row of the p\* table with the new values and remove the `*(approximate)*` marker; GHZ/ring rows stay (verified unchanged in Step 2). Rewrite the two W-related findings bullets ("GHZ crosses zero before W…" caveat text and the "W saturates to the maximally-mixed payoff…" bullet) to describe the NEW data — in particular, the old explanation "its transpiled circuit has a synthesis-derived (large) gate count" is no longer true and must not survive in any form. State the new W gate-count story (physical prep-conjugated circuit) and the new measured behaviour, whatever it is.

- [ ] **Step 4: Full suite one last time**

Run: `pytest`
Expected: all PASSED.

- [ ] **Step 5: Commit (include the new results directory — prior runs are committed too)**

```bash
git add README.md results/noise-robustness/
git commit -m "Feat: T8 re-run noise sweep with exact W entangler; refresh RQ3 results"
```

---

## Self-review notes (spec coverage)

- Spec D-T8.1 (physics decision): no code — recorded in the spec; Task 2's docstring links it.
- Spec D-T8.2/D-T8.3 (construction + cascade): Tasks 1-2, tests 1-3 of spec §3 map to `test_w_prep_*` and `test_w_gate_circuit_matches_dense_n5` plus the pre-existing N=2..4 equivalence tests.
- Spec §4 items 1-2 → Task 4; item 3 → Task 3 (steps 1-5); item 4 → Task 3 (steps 6-7).
- Spec §6 failure modes: each has a named catching test (see Task 2 step 4 note).
