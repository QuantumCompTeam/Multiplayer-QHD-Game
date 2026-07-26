# Hardware Topology, Equilibrium, and Fairness Batch — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Put the paper's topology, equilibrium, noise-robustness and per-player-fairness claims on real hardware, so the title's claim ("Entanglement Topology and Noise Determine Quantum Advantage") is backed by device data rather than simulation alone.

**Architecture:** A **new** experiment script (`experiments/hardware_topology.py`) built from a shared, offline-testable core (`src/hardware/topology_hw.py`), submitting one multi-topology SamplerV2 batch. `experiments/hardware_scaling.py` is left byte-identical for items 1/2/5/6/7 so that item 3 (cross-day repeats) re-runs the *registered* batch unchanged; item 4 (N=6,7) extends it later behind an opt-in `--ns` flag whose default reproduces the existing behaviour exactly.

**Tech Stack:** Python 3.10.20, qiskit 1.3.2, qiskit-aer 0.14.2, qiskit-ibm-runtime 0.36.1, numpy 1.26.4, scipy 1.13.1. Conda env `entangled-equilibria`. Backend `ibm_fez` (IBM Heron r2).

## Global Constraints

- Every command runs as `conda run -n entangled-equilibria python <script>` (item 17 / G10). No bare `python`, no `PYTHONPATH=src` prefix.
- `V=4`, `C=3` (`src/config.py`), `gamma = pi/2` unless a task sweeps it. This is the live convention (F1).
- **`results/hardware-scaling/preregistration.json` and `preregistration-baselines.json` are FROZEN. Never edit them.** New claims get new registration files.
- **`experiments/hardware_scaling.py` must not change behaviour under its current default flags** until Task 10. Runs 1 and 2 must stay recoverable via `--from-job`.
- Every hardware run must pass the three existing gates before submission: circuit-identity assertion, noiseless dry-run, and full dress rehearsal on the reduced device noise model.
- Job ids are persisted to `results/hardware-scaling/pending_jobs.txt` **before** polling.
- No numerical claim enters `paper/main.tex` without a `%`-comment naming the `results/` artifact it came from.
- Advantage sign convention: `advantage = measured cooperative payoff − analytic noiseless classical NE payoff (1/N)`. Simulation figures use the circuit-relative gap instead; never mix them.

---

## File Structure

| File | Responsibility |
|---|---|
| `src/hardware/topology_hw.py` (create) | Topology-parameterised EWL circuit build, deviation profiles, ISA safety check generalised from a linear chain to a pinned connected qubit set. Pure functions, no network. |
| `tests/test_hardware_topology.py` (create) | Offline tests for the above: circuit identity per topology, deviation-profile construction, ISA checker accept/reject. |
| `experiments/hardware_topology.py` (create) | The batch: plan → rehearse → submit → analyse → save. Mirrors `hardware_scaling.py`'s structure and safeguards. |
| `scripts/preregister_topology.py` (create) | Freezes predictions into `results/hardware-topology/preregistration.json` before any submission. |
| `scripts/judge_topology_run.py` (create) | Applies the registered tests to a completed run; writes `judgments.json`. |
| `experiments/hardware_scaling.py` (modify, Task 10 only) | Add `--ns` for the N=6,7 extension. Default unchanged. |
| `docs/findings/2026-XX-XX-*.md` | One finding per completed run. |
| `paper/main.tex` | Final claim updates, last. |

---

## Scheduling note (read before starting)

Item 3 (cross-day repeats) is the **only** item gated on wall-clock time — it needs executions on 3–5 *distinct calibration days*. It requires **zero code changes**: it is `experiments/hardware_scaling.py --hardware` on the untouched script, ~35 s of QPU. Task 0 fires it today so the calendar clock runs in parallel with Tasks 1–9. Deferring it until after Task 9 would add days to the critical path for no benefit.

---

### Task 0: Cross-day repeat run 3 (item 3 + item 8, no code change)

**Files:**
- Create: `results/hardware-scaling/<new-timestamp>/` (written by the script)
- Modify: none

**Interfaces:**
- Consumes: nothing
- Produces: a third run directory; `calibration_at_submit.json` (first ever written — this is item 8's validation)

- [ ] **Step 1: Confirm the working tree is clean so provenance is not `dirty`**

Run: `git status --porcelain`
Expected: empty output. If not empty, commit or stash first — both existing runs recorded `"dirty": true` (G16) and this run exists partly to prove that is fixed.

- [ ] **Step 2: Confirm the credential is present**

Run: `conda run -n entangled-equilibria python -c "import os; print('token' if os.environ.get('QISKIT_IBM_TOKEN') else 'NO TOKEN')"`
Expected: `token`. If `NO TOKEN`, set `QISKIT_IBM_TOKEN` in the shell before continuing.

- [ ] **Step 3: Verify the device calibration stamp differs from runs 1 and 2**

Run: `conda run -n entangled-equilibria python experiments/hardware_scaling.py --report`
Expected: prints the pinned chain and a `calibration_last_update` that is **not** `2026-07-16 08:30:13+05:30`. If it matches, stop — this would not count as a distinct calibration day (see `TODOS.md`, "Caveat for runs 3–5").

- [ ] **Step 4: Submit**

Run: `conda run -n entangled-equilibria python experiments/hardware_scaling.py --hardware`
Expected: rehearsal gate prints `PASS`, a job id is appended to `results/hardware-scaling/pending_jobs.txt`, then a summary table and `saved: results/hardware-scaling/<ts>/result.json`.

- [ ] **Step 5: Verify item 8 (environment provenance) actually landed**

Run: `conda run -n entangled-equilibria python -c "import json,glob,os; d=sorted(glob.glob('results/hardware-scaling/2026-*'))[-1]; r=json.load(open(os.path.join(d,'result.json'))); print(d); print('env:', r.get('environment')); print('git:', r['git']); print('cal_at_submit:', os.path.exists(os.path.join(d,'calibration_at_submit.json')))"`
Expected: `env` is a dict containing `python`, `qiskit`, `qiskit_ibm_runtime`, `platform`; `git['dirty']` is `False`; `cal_at_submit: True`. All three were absent or wrong on runs 1 and 2 — this is the item-16 validation.

- [ ] **Step 6: Judge against the frozen registration**

Run: `conda run -n entangled-equilibria python scripts/judge_repeat_run.py`
Expected: writes `results/hardware-scaling/repeat-judgments.json` with `n_repeats_judged: 2` or more, and a `distinct_calibration_vs_previous_runs: true` flag on the new run.

- [ ] **Step 7: Commit**

```bash
git add results/hardware-scaling/
git commit -m "item-3: cross-day repeat run 3 on ibm_fez; validates item-16 env provenance"
```

---

### Task 1: Topology-parameterised EWL circuit builder

**Files:**
- Create: `src/hardware/topology_hw.py`
- Test: `tests/test_hardware_topology.py`

**Interfaces:**
- Consumes: `circuits.gate_level.{ghz,ring,star,fully_connected,w}_gate_circuit(N, gamma)`, `circuits.topologies.{ghz,ring,star,fully_connected,w}_entangler(N, gamma)`, `circuits.ewl.{U, q_strategy}`
- Produces:
  - `GATE_CIRCUITS: dict[str, Callable[[int, float], QuantumCircuit]]`
  - `ENTANGLERS: dict[str, Callable[[int, float], np.ndarray]]`
  - `build_ewl_circuit(N: int, topology: str, gamma: float, profile: list[str] | None = None) -> QuantumCircuit`
  - `assert_circuit_identity(qc: QuantumCircuit, N: int, topology: str, gamma: float, profile: list[str] | None = None) -> None`

`profile` is a list of length `N` over `{"D","H","Q"}`; `None` means all-`Q`. This is the seam Task 2 (equilibrium deviations) needs.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_hardware_topology.py
import math

import numpy as np
import pytest
from qiskit.quantum_info import Operator

from hardware.topology_hw import (
    ENTANGLERS,
    GATE_CIRCUITS,
    assert_circuit_identity,
    build_ewl_circuit,
)

GAMMA = math.pi / 2
TOPOLOGIES = ["ghz", "ring", "star", "fully-connected", "w"]


@pytest.mark.parametrize("topology", TOPOLOGIES)
@pytest.mark.parametrize("N", [3, 4])
def test_build_matches_dense_reference(topology, N):
    """The gate-level build IS J† (U⊗…⊗U) J for every topology."""
    qc = build_ewl_circuit(N, topology, GAMMA)
    assert_circuit_identity(qc, N, topology, GAMMA)  # must not raise


def test_registries_agree_on_keys():
    assert set(GATE_CIRCUITS) == set(ENTANGLERS) == set(TOPOLOGIES)


def test_all_q_profile_is_the_default():
    a = build_ewl_circuit(3, "ghz", GAMMA)
    b = build_ewl_circuit(3, "ghz", GAMMA, profile=["Q", "Q", "Q"])
    assert Operator(a).equiv(Operator(b))


def test_hawk_deviation_differs_from_all_q():
    a = build_ewl_circuit(3, "ghz", GAMMA)
    b = build_ewl_circuit(3, "ghz", GAMMA, profile=["H", "Q", "Q"])
    assert not Operator(a).equiv(Operator(b))


def test_profile_length_is_validated():
    with pytest.raises(ValueError, match="profile"):
        build_ewl_circuit(3, "ghz", GAMMA, profile=["Q", "Q"])


def test_unknown_topology_is_rejected():
    with pytest.raises(KeyError):
        build_ewl_circuit(3, "banana", GAMMA)
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'hardware.topology_hw'`

- [ ] **Step 3: Write the implementation**

```python
# src/hardware/topology_hw.py
"""Topology-parameterised EWL circuits for hardware batches.

`experiments/hardware_scaling.py` hardcodes the GHZ entangler and the all-Q
profile. The topology batch needs both as free variables, so the build and its
circuit-identity assertion live here as pure functions and are unit-tested
offline before any quota is spent.
"""

from __future__ import annotations

import math
from typing import Callable

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

from circuits.ewl import U, q_strategy
from circuits.gate_level import (
    fully_connected_gate_circuit,
    ghz_gate_circuit,
    ring_gate_circuit,
    star_gate_circuit,
    w_gate_circuit,
)
from circuits.topologies import (
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)

GATE_CIRCUITS: dict[str, Callable[..., QuantumCircuit]] = {
    "ghz": ghz_gate_circuit,
    "ring": ring_gate_circuit,
    "star": star_gate_circuit,
    "fully-connected": fully_connected_gate_circuit,
    "w": w_gate_circuit,
}

ENTANGLERS: dict[str, Callable[..., np.ndarray]] = {
    "ghz": ghz_entangler,
    "ring": ring_entangler,
    "star": star_entangler,
    "fully-connected": fully_connected_entangler,
    "w": w_entangler,
}


def strategy_matrix(name: str, N: int) -> np.ndarray:
    """The 2x2 SU(2) matrix for a discrete strategy label.

    D = Dove = U(0,0,0) = I; H = Hawk = U(pi,0,0); Q = the GHZ-derived
    q_strategy(N) = U(0, pi/N, pi/N). Same definitions as experiments/config.yaml.
    """
    if name == "D":
        return U(0.0, 0.0, 0.0)
    if name == "H":
        return U(math.pi, 0.0, 0.0)
    if name == "Q":
        return U(*q_strategy(N))
    raise ValueError(f"unknown strategy label {name!r}; expected D, H or Q")


def _resolve_profile(N: int, profile: list[str] | None) -> list[str]:
    if profile is None:
        return ["Q"] * N
    if len(profile) != N:
        raise ValueError(
            f"profile has {len(profile)} entries but N={N}; they must match"
        )
    return list(profile)


def build_ewl_circuit(
    N: int,
    topology: str,
    gamma: float,
    profile: list[str] | None = None,
) -> QuantumCircuit:
    """J · (U_1 ⊗ … ⊗ U_N) · J† on N qubits, gate-level.

    `topology` selects the entangler; `profile` selects each player's strategy
    (default all-Q). Mirrors experiments/hardware_scaling.build_ewl_gate_circuit
    with both hardcodings lifted.
    """
    names = _resolve_profile(N, profile)
    J = GATE_CIRCUITS[topology](N, gamma)
    qc = QuantumCircuit(N)
    qc.compose(J, inplace=True)
    for q in range(N):
        qc.append(UnitaryGate(strategy_matrix(names[q], N), label=names[q]), [q])
    qc.compose(J.inverse(), inplace=True)
    return qc


def dense_reference(
    N: int,
    topology: str,
    gamma: float,
    profile: list[str] | None = None,
) -> Operator:
    """The dense J† (U_1 ⊗ … ⊗ U_N) J matrix this build must equal."""
    names = _resolve_profile(N, profile)
    layer = strategy_matrix(names[0], N)
    for q in range(1, N):
        layer = np.kron(layer, strategy_matrix(names[q], N))
    J = ENTANGLERS[topology](N, gamma)
    return Operator(J.conj().T @ layer @ J)


def assert_circuit_identity(
    qc: QuantumCircuit,
    N: int,
    topology: str,
    gamma: float,
    profile: list[str] | None = None,
) -> None:
    """Gate 1: raise unless `qc` IS the validated dense unitary."""
    if not Operator(qc).equiv(dense_reference(N, topology, gamma, profile)):
        raise AssertionError(
            f"circuit identity FAILED for topology={topology} N={N} "
            f"profile={_resolve_profile(N, profile)}"
        )
```

- [ ] **Step 4: Run the tests to confirm they pass**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -v`
Expected: PASS, 14 tests.

Note on the `np.kron` ordering: `experiments/hardware_scaling.py:110-111` builds its reference with the same left-to-right `kron`, and its assertion passes against the shipped GHZ circuits, so this ordering is the one the repo's circuits use. If a topology fails only at `N=4`, suspect qubit-ordering convention and compare against `tests/test_gate_level.py` before changing anything here.

- [ ] **Step 5: Commit**

```bash
git add src/hardware/topology_hw.py tests/test_hardware_topology.py
git commit -m "feat: topology- and profile-parameterised EWL circuit builder for hardware batches"
```

---

### Task 2: Generalised ISA safety check (pinned qubit set, not linear chain)

**Files:**
- Modify: `src/hardware/topology_hw.py`
- Test: `tests/test_hardware_topology.py`

**Interfaces:**
- Consumes: Task 1's module
- Produces: `check_isa_on_set(isa: QuantumCircuit, allowed: set[int], budget: int) -> int`

`experiments/hardware_scaling.py:245-263` asserts every 2-qubit gate is a `cz` on an **adjacent pinned-chain pair**, with limit `4*(N-1)+2`. Non-linear topologies route off the chain, so that check would abort every ring/star/fully-connected/W submission. The safeguard's real content is "no `cz` escaped the pinned qubits, and the count did not blow up in routing" — that generalises; the linear-adjacency part does not.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_hardware_topology.py
from qiskit import QuantumCircuit

from hardware.topology_hw import check_isa_on_set


def _cz_circuit(pairs, width=8):
    qc = QuantumCircuit(width)
    for a, b in pairs:
        qc.cz(a, b)
    return qc


def test_counts_cz_on_allowed_qubits():
    qc = _cz_circuit([(1, 2), (2, 3)])
    assert check_isa_on_set(qc, allowed={1, 2, 3}, budget=10) == 2


def test_rejects_cz_off_the_pinned_set():
    qc = _cz_circuit([(1, 2), (2, 7)])
    with pytest.raises(AssertionError, match="off the pinned set"):
        check_isa_on_set(qc, allowed={1, 2, 3}, budget=10)


def test_rejects_non_cz_two_qubit_gate():
    qc = QuantumCircuit(4)
    qc.cx(0, 1)
    with pytest.raises(AssertionError, match="unexpected 2q gate"):
        check_isa_on_set(qc, allowed={0, 1}, budget=10)


def test_rejects_when_over_budget():
    qc = _cz_circuit([(1, 2)] * 11)
    with pytest.raises(AssertionError, match="exceeds budget"):
        check_isa_on_set(qc, allowed={1, 2}, budget=10)


def test_accepts_exactly_at_budget():
    qc = _cz_circuit([(1, 2)] * 10)
    assert check_isa_on_set(qc, allowed={1, 2}, budget=10) == 10
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -k check_isa -v`
Expected: FAIL — `ImportError: cannot import name 'check_isa_on_set'`

- [ ] **Step 3: Write the implementation**

```python
# append to src/hardware/topology_hw.py


def check_isa_on_set(isa: QuantumCircuit, allowed: set[int], budget: int) -> int:
    """Safety gate: every 2q gate is a cz inside `allowed`, count <= budget.

    Generalises experiments/hardware_scaling.check_isa, which additionally
    required each cz to sit on an ADJACENT pair of one pinned linear chain.
    That extra constraint is GHZ-on-a-line specific: ring, star,
    fully-connected and W all need routing on heavy-hex, so they legitimately
    place cz gates on non-adjacent-in-chain pairs of the pinned set. What still
    must hold is that no gate escaped the pinned qubits and that routing did
    not blow the gate budget. Returns the cz count.
    """
    n_cz = 0
    for ci in isa.data:
        if ci.operation.num_qubits != 2:
            continue
        if ci.operation.name != "cz":
            raise AssertionError(f"unexpected 2q gate {ci.operation.name!r}")
        pair = {isa.find_bit(q).index for q in ci.qubits}
        if not pair <= allowed:
            raise AssertionError(f"cz off the pinned set: {sorted(pair)}")
        n_cz += 1
    if n_cz > budget:
        raise AssertionError(f"cz count {n_cz} exceeds budget {budget} (routing?)")
    return n_cz
```

- [ ] **Step 4: Run the tests to confirm they pass**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -v`
Expected: PASS, 19 tests.

- [ ] **Step 5: Confirm nothing else regressed**

Run: `conda run -n entangled-equilibria python -m pytest tests/ -q`
Expected: the previously recorded `512 passed, 3 skipped` plus the 19 new = `531 passed, 3 skipped`. Any failure here is a regression — stop and fix before continuing.

- [ ] **Step 6: Commit**

```bash
git add src/hardware/topology_hw.py tests/test_hardware_topology.py
git commit -m "feat: pinned-qubit-set ISA safety check for routed (non-linear) topologies"
```

---

### Task 3: Feasibility report — routed cz counts on the real device

**Files:**
- Create: `experiments/hardware_topology.py` (report mode only)

**Interfaces:**
- Consumes: Task 1 + Task 2
- Produces: `--report` output; the measured cell list that Tasks 4–8 build on

This task decides *which cells are runnable* from measured data rather than assumption. Pre-routing counts (measured 2026-07-25) are GHZ `3/5/7`, star `2/3/4`, ring `3/4/5`, fully-connected `3/6/10`, W `18/38/60` at N=3/4/5. But ibm_fez is heavy-hex: max degree 3 and girth 12, so **ring has no native cycle below N=12, fully-connected has no native triangle, and star is native only up to a degree-3 hub (N≤4)**. Real routed counts are therefore the only usable number, and only the device can give them.

- [ ] **Step 1: Write the report script**

```python
# experiments/hardware_topology.py
"""Multi-topology EWL hardware batch (items 1, 2, 5, 6, 7).

Companion to experiments/hardware_scaling.py, which stays untouched so that
its frozen preregistration and its cross-day repeats (item 3) remain
byte-comparable. This script varies TOPOLOGY, STRATEGY PROFILE, GAMMA and
QUBIT WIRING, which that script hardcodes.

Modes:
  --report     Transpile report against the real coupling map: routed cz count
               and depth per (topology, N). Network read only, no job, no quota.
  --rehearse   Full dress rehearsal of the batch on the reduced device noise
               model, including the complete analysis. No job submitted.
  --hardware   Rehearse (mandatory gate), then submit ONE batch job, persisting
               the job id BEFORE polling.
  --from-job   Recover and analyse a submitted batch.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import math

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from hardware.topology_hw import GATE_CIRCUITS, build_ewl_circuit

GAMMA = math.pi / 2
DEFAULT_BACKEND = "ibm_fez"
REPORT_CELLS = [(t, N) for t in GATE_CIRCUITS for N in (3, 4, 5)]


def load_service():
    """Saved-account / env-token QiskitRuntimeService (same logic as Month 5)."""
    from qiskit_ibm_runtime import QiskitRuntimeService

    token = os.environ.get("QISKIT_IBM_TOKEN")
    channel = os.environ.get("QISKIT_IBM_CHANNEL", "ibm_cloud")
    instance = os.environ.get("QISKIT_IBM_INSTANCE")
    try:
        if token:
            kwargs = {"channel": channel, "token": token}
            if instance:
                kwargs["instance"] = instance
            return QiskitRuntimeService(**kwargs)
        return QiskitRuntimeService()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: could not initialise QiskitRuntimeService: {exc}")
        sys.exit(2)


def report(backend) -> None:
    """Routed cz count + depth per (topology, N) on the REAL coupling map."""
    print(f"transpile report on {backend.name} "
          f"(coupling map degree<=3 heavy-hex; routing is what costs)")
    print(f"{'topology':16s} {'N':>2s} {'cz':>5s} {'depth':>6s}  note")
    for topology, N in REPORT_CELLS:
        qc = build_ewl_circuit(N, topology, GAMMA)
        pm = generate_preset_pass_manager(backend=backend, optimization_level=3,
                                          seed_transpiler=7)
        try:
            isa = pm.run(qc)
        except Exception as exc:  # noqa: BLE001
            print(f"{topology:16s} {N:2d} {'--':>5s} {'--':>6s}  TRANSPILE FAILED: {exc}")
            continue
        n_cz = isa.count_ops().get("cz", 0)
        # ibm_fez N=3 GHZ ran at 6 cz and retained 95.5% ground state; treat
        # ~6x that as the point where the signal is no longer worth the quota.
        note = "ok" if n_cz <= 40 else "EXPENSIVE — justify before submitting"
        print(f"{topology:16s} {N:2d} {n_cz:5d} {isa.depth():6d}  {note}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", default=DEFAULT_BACKEND)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    if not args.report:
        print("(no mode selected; use --report)")
        return

    service = load_service()
    report(service.backend(args.backend))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the report**

Run: `conda run -n entangled-equilibria python experiments/hardware_topology.py --report`
Expected: a 15-row table. Record the output verbatim — it is the input to the next step.

- [ ] **Step 3: Record the decision**

Write the measured table into `docs/findings/2026-07-25-topology-hardware-feasibility.md`, and list the cells selected for the batch with the reason each excluded cell was dropped (routed cz over budget / transpile failure). **Do not** carry an excluded cell forward silently — the paper must be able to say which topology×N cells were attempted and why the others were not.

- [ ] **Step 4: Commit**

```bash
git add experiments/hardware_topology.py docs/findings/2026-07-25-topology-hardware-feasibility.md
git commit -m "item-9: transpile feasibility report for topology hardware cells on ibm_fez"
```

---

### Task 4: Batch plan — topology series (item 1)

**Files:**
- Modify: `experiments/hardware_topology.py`
- Test: `tests/test_hardware_topology.py`

**Interfaces:**
- Consumes: Tasks 1–3
- Produces: `build_batch(backend, cells, folds, gammas, wirings) -> dict` with keys `{"pinned", "pubs", "meta"}`; each `meta[i]` is one of
  - `{"kind": "cal0"|"cal1", "fil": [...]}`
  - `{"kind": "series", "topology": str, "N": int, "fold": int, "gamma": float, "profile": [...], "wiring": [...], "fil": [...], "cz": int}`

Every downstream stage keys off `meta`, so **all five experiment types (topology, deviation, fold, gamma, wiring) are the same pub kind with different fields.** That is the whole design: one uniform series record, five axes.

- [ ] **Step 1: Write the failing test for the plan shape**

```python
# append to tests/test_hardware_topology.py
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "hardware_topology",
    Path(__file__).resolve().parents[1] / "experiments" / "hardware_topology.py",
)
hardware_topology = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hardware_topology)


def test_series_meta_carries_every_axis():
    meta = hardware_topology.series_meta(
        topology="ghz", N=3, fold=1, gamma=GAMMA,
        profile=["Q", "Q", "Q"], wiring=[0, 1, 2], fil=[59, 75, 74], cz=6,
    )
    assert meta["kind"] == "series"
    for key in ("topology", "N", "fold", "gamma", "profile", "wiring", "fil", "cz"):
        assert key in meta, f"{key} missing from series meta"


def test_series_meta_rejects_wiring_of_wrong_length():
    with pytest.raises(ValueError, match="wiring"):
        hardware_topology.series_meta(
            topology="ghz", N=3, fold=1, gamma=GAMMA,
            profile=["Q", "Q", "Q"], wiring=[0, 1], fil=[59, 75, 74], cz=6,
        )
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -k series_meta -v`
Expected: FAIL — `AttributeError: module 'hardware_topology' has no attribute 'series_meta'`

- [ ] **Step 3: Implement `series_meta` and `build_batch`**

```python
# append to experiments/hardware_topology.py, above main()

from qiskit import QuantumCircuit
from qiskit.circuit import ClassicalRegister

from hardware.chain import best_linear_chain
from hardware.topology_hw import check_isa_on_set

FOLDS = (1, 3, 5)
DEFAULT_SHOTS = 4096
PIN_LEN = 5          # width of the pinned qubit set and of the cal circuits
CZ_BUDGET = 60       # per-pub routed cz ceiling; Task 3's report justifies it


def series_meta(*, topology, N, fold, gamma, profile, wiring, fil, cz) -> dict:
    """One uniform series record. Every experiment axis is a field here."""
    if len(wiring) != N:
        raise ValueError(f"wiring has {len(wiring)} entries but N={N}")
    if len(profile) != N:
        raise ValueError(f"profile has {len(profile)} entries but N={N}")
    return {"kind": "series", "topology": topology, "N": N, "fold": fold,
            "gamma": float(gamma), "profile": list(profile),
            "wiring": list(wiring), "fil": list(fil), "cz": cz}


def with_measurement(isa: QuantumCircuit, fil: list[int], n_meas: int) -> QuantumCircuit:
    """Append creg 'meas' and measure physical fil[j] -> clbit j."""
    qc = isa.copy()
    creg = ClassicalRegister(n_meas, "meas")
    qc.add_register(creg)
    for j in range(n_meas):
        qc.measure(fil[j], creg[j])
    return qc


def fold_cz(isa: QuantumCircuit, factor: int) -> QuantumCircuit:
    """Local ZNE folding: every cz -> cz^factor (odd factor; cz is self-inverse)."""
    assert factor % 2 == 1
    out = isa.copy_empty_like()
    for ci in isa.data:
        out.append(ci.operation, ci.qubits, ci.clbits)
        if ci.operation.name == "cz":
            for _ in range(factor - 1):
                out.append(ci.operation, ci.qubits, ci.clbits)
    return out


def find_pinned_set(backend) -> list[int]:
    """Best PIN_LEN-qubit linear chain; the pinned set is its qubits.

    A linear chain is still the right pin even for routed topologies: it is the
    lowest-error connected PIN_LEN-subgraph the existing selector can find, and
    pinning the SAME physical qubits across topologies is what makes the
    topology comparison a controlled one.
    """
    props = backend.properties()
    edge_err: dict[frozenset, float] = {}
    for a, b in backend.coupling_map.get_edges():
        key = frozenset((a, b))
        if key in edge_err:
            continue
        try:
            edge_err[key] = float(props.gate_error("cz", [a, b]))
        except Exception:  # noqa: BLE001 -- reversed direction
            edge_err[key] = float(props.gate_error("cz", [b, a]))
    nodes = {q for e in edge_err for q in e}
    node_err = {q: float(props.readout_error(q)) for q in nodes}
    chain = best_linear_chain([tuple(e) for e in edge_err], edge_err,
                              node_err, PIN_LEN)
    print(f"pinned set on {backend.name}: {chain}")
    return chain


def build_batch(backend, cells, folds=FOLDS, gammas=(GAMMA,),
                profiles=None, wirings=None) -> dict:
    """Build the full batch plan.

    cells:    [(topology, N), ...]                 -- item 1
    folds:    (1, 3, 5, ...)                       -- items 5 (noise axis) + ZNE
    gammas:   (pi/2, ...)                          -- item 7
    profiles: {(topology, N): [profile, ...]}      -- item 2 (deviations)
    wirings:  {(topology, N): [wiring, ...]}       -- item 6 (permutations)
    """
    pinned = find_pinned_set(backend)
    allowed = set(pinned)
    plan: dict = {"pinned": pinned, "pubs": [], "meta": []}

    for label, prep in (("cal0", False), ("cal1", True)):
        qc = QuantumCircuit(PIN_LEN)
        if prep:
            qc.x(range(PIN_LEN))
        pm = generate_preset_pass_manager(backend=backend, optimization_level=0,
                                          initial_layout=pinned)
        isa = pm.run(qc)
        fil = list(isa.layout.final_index_layout())
        plan["pubs"].append(with_measurement(isa, fil, PIN_LEN))
        plan["meta"].append({"kind": label, "fil": fil})

    profiles = profiles or {}
    wirings = wirings or {}
    for topology, N in cells:
        cell_profiles = profiles.get((topology, N), [["Q"] * N])
        cell_wirings = wirings.get((topology, N), [list(range(N))])
        for gamma in gammas:
            for profile in cell_profiles:
                for wiring in cell_wirings:
                    layout = [pinned[w] for w in wiring]
                    pm = generate_preset_pass_manager(
                        backend=backend, optimization_level=3,
                        initial_layout=layout, seed_transpiler=7)
                    isa_u = pm.run(build_ewl_circuit(N, topology, gamma, profile))
                    fil = list(isa_u.layout.final_index_layout())
                    n_cz = check_isa_on_set(isa_u, allowed, CZ_BUDGET)
                    print(f"  {topology:16s} N={N} gamma={gamma:.4f} "
                          f"profile={''.join(profile)} wiring={wiring}: "
                          f"cz {n_cz}, depth {isa_u.depth()}")
                    for f in folds:
                        plan["pubs"].append(
                            with_measurement(fold_cz(isa_u, f), fil, N))
                        plan["meta"].append(series_meta(
                            topology=topology, N=N, fold=f, gamma=gamma,
                            profile=profile, wiring=wiring, fil=fil,
                            cz=n_cz * f))
    print(f"batch: {len(plan['pubs'])} pubs")
    return plan
```

- [ ] **Step 4: Run the tests to confirm they pass**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -v`
Expected: PASS, 21 tests.

- [ ] **Step 5: Commit**

```bash
git add experiments/hardware_topology.py tests/test_hardware_topology.py
git commit -m "item-9: uniform five-axis batch plan builder (topology/profile/fold/gamma/wiring)"
```

---

### Task 5: Analysis over the uniform series records

**Files:**
- Modify: `experiments/hardware_topology.py`
- Test: `tests/test_hardware_topology.py`

**Interfaces:**
- Consumes: Task 4's `meta` records
- Produces: `series_key(meta) -> str`, `analyze_batch(counts_per_pub, plan, shots) -> dict`

Result keying: one string per distinct (topology, N, gamma, profile, wiring), with the fold axis nested underneath so ZNE still has its `1/3/5` series to extrapolate over.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_hardware_topology.py
def test_series_key_is_stable_and_excludes_fold():
    base = dict(topology="ghz", N=3, gamma=GAMMA, profile=["Q", "Q", "Q"],
                wiring=[0, 1, 2], fil=[59, 75, 74], cz=6)
    k1 = hardware_topology.series_key(hardware_topology.series_meta(fold=1, **base))
    k5 = hardware_topology.series_key(hardware_topology.series_meta(fold=5, **base))
    assert k1 == k5, "fold must not appear in the series key"


def test_series_key_separates_profiles_and_wirings():
    base = dict(topology="ghz", N=3, fold=1, gamma=GAMMA, fil=[59, 75, 74], cz=6)
    a = hardware_topology.series_key(hardware_topology.series_meta(
        profile=["Q", "Q", "Q"], wiring=[0, 1, 2], **base))
    b = hardware_topology.series_key(hardware_topology.series_meta(
        profile=["H", "Q", "Q"], wiring=[0, 1, 2], **base))
    c = hardware_topology.series_key(hardware_topology.series_meta(
        profile=["Q", "Q", "Q"], wiring=[1, 2, 0], **base))
    assert len({a, b, c}) == 3
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -k series_key -v`
Expected: FAIL — `AttributeError: module 'hardware_topology' has no attribute 'series_key'`

- [ ] **Step 3: Implement**

```python
# append to experiments/hardware_topology.py

import numpy as np

from game.payoffs import expected_payoff
from hardware.mitigation import (
    confusion_from_counts,
    counts_to_probs,
    mitigate_probs,
    zne_extrapolate,
)


def series_key(meta: dict) -> str:
    """Stable identity of a series across folds."""
    return (f"{meta['topology']}|N{meta['N']}|g{meta['gamma']:.6f}"
            f"|{''.join(meta['profile'])}|w{'-'.join(map(str, meta['wiring']))}")


def _onehot(i: int, N: int) -> np.ndarray:
    v = np.zeros(2**N)
    v[i] = 1.0
    return v


def payoff_stats(probs: np.ndarray, N: int, shots: int) -> dict:
    """Mean profile payoff + multinomial shot-noise sigma of the mean.

    Identical estimator to experiments/hardware_scaling.payoff_stats; per_player
    is kept because items 6 and 7 read the per-player floor, not the mean.
    """
    per_player = expected_payoff(probs, N)
    mean = float(np.mean(per_player))
    cbar = np.array([float(np.mean(expected_payoff(_onehot(i, N), N)))
                     for i in range(2**N)])
    var = float(np.sum(probs * cbar**2) - mean**2)
    return {"per_player": [float(x) for x in per_player],
            "mean": mean,
            "sigma": float(np.sqrt(max(var, 0.0) / shots)),
            "p_ground": float(probs[0])}


def analyze_batch(counts_per_pub: list[dict], plan: dict, shots: int) -> dict:
    """counts (plan order) -> per-series raw/mitigated/ZNE results."""
    meta = plan["meta"]
    mats_all = confusion_from_counts(counts_per_pub[0], counts_per_pub[1], PIN_LEN)
    cal_fil = meta[0]["fil"]
    mats_by_phys = {cal_fil[j]: mats_all[j] for j in range(PIN_LEN)}

    grouped: dict[str, list[int]] = {}
    for i, m in enumerate(meta):
        if m["kind"] == "series":
            grouped.setdefault(series_key(m), []).append(i)

    out: dict = {"pinned": plan["pinned"], "shots": shots, "series": {}}
    for key, idxs in grouped.items():
        first = meta[idxs[0]]
        N = first["N"]
        classical = 1.0 / N   # analytic noiseless all-Hawk payoff (V-C)/N at V=4,C=3
        mats = [mats_by_phys[first["fil"][j]] for j in range(N)]
        folds_out, mit_payoffs, mit_sigmas, fold_values = {}, [], [], []
        for i in sorted(idxs, key=lambda i: meta[i]["fold"]):
            f = meta[i]["fold"]
            p_raw = counts_to_probs(counts_per_pub[i], N)
            p_mit = mitigate_probs(p_raw, mats)
            s_raw = payoff_stats(p_raw, N, shots)
            s_mit = payoff_stats(p_mit, N, shots)
            folds_out[str(f)] = {
                "counts": counts_per_pub[i],
                "cz": meta[i]["cz"],
                "raw": {**s_raw, "advantage": s_raw["mean"] - classical},
                "mitigated": {**s_mit, "advantage": s_mit["mean"] - classical},
            }
            fold_values.append(f)
            mit_payoffs.append(s_mit["mean"])
            mit_sigmas.append(max(s_mit["sigma"], 1e-9))
        entry = {"topology": first["topology"], "N": N, "gamma": first["gamma"],
                 "profile": first["profile"], "wiring": first["wiring"],
                 "fil": first["fil"], "classical_ne_payoff": classical,
                 "folds": folds_out}
        if len(fold_values) >= 2:
            zne = zne_extrapolate(fold_values, mit_payoffs, mit_sigmas)
            zne["advantage"] = zne["linear"] - classical
            entry["zne"] = zne
        out["series"][key] = entry
    return out
```

- [ ] **Step 4: Run the tests to confirm they pass**

Run: `conda run -n entangled-equilibria python -m pytest tests/test_hardware_topology.py -v`
Expected: PASS, 23 tests.

- [ ] **Step 5: Commit**

```bash
git add experiments/hardware_topology.py tests/test_hardware_topology.py
git commit -m "item-9: per-series analysis with per-player vectors and per-series ZNE"
```

---

### Task 6: Rehearsal, submission, and save path

**Files:**
- Modify: `experiments/hardware_topology.py`

**Interfaces:**
- Consumes: Tasks 4–5
- Produces: `--rehearse`, `--hardware`, `--from-job` modes; run directories under `results/hardware-topology/<ts>/`

This task ports the three safeguards and the provenance block from `hardware_scaling.py` verbatim in behaviour: mandatory rehearsal before submission, job id persisted before polling, and the item-16 environment/calibration blocks.

- [ ] **Step 1: Port the safeguard and persistence helpers**

Copy these functions from `experiments/hardware_scaling.py` into `experiments/hardware_topology.py`, unchanged except where noted:
- `reduce_isa` (lines 342-355) — unchanged
- `strip_measures` (358-364) — unchanged
- `reduce_noise_model` (367-386) — unchanged
- `git_provenance` (574-588) — unchanged
- `environment_provenance` (591-607) — unchanged
- `chain_calibration` (610-626) — change the `cz_error` loop to walk `zip(pinned, pinned[1:])` over the pinned set (same code, renamed argument)
- `_save_pending_job_id` (665-672) and `_submit_cal_path` (675-678) — change the results subdirectory from `hardware-scaling` to `hardware-topology`

- [ ] **Step 2: Write the rehearsal gate**

```python
# append to experiments/hardware_topology.py

def rehearse(backend, plan: dict, shots: int) -> dict:
    """Simulate the ENTIRE batch + analysis on the reduced device noise model.

    Mandatory pre-submission gate. Two checks must pass:
      (a) every pub is single-outcome noiselessly (the ideal circuit maps
          |0..0> to one basis state, and cz^k = cz for odd k);
      (b) ZNE moves the majority of all-Q series toward the ideal.
    """
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel

    print("\n=== dress rehearsal on AerSimulator(device noise model) ===")
    nm_full = NoiseModel.from_backend(backend)
    counts_per_pub = []
    for pub, m in zip(plan["pubs"], plan["meta"]):
        small = reduce_isa(pub, m["fil"])
        ideal = AerSimulator().run(small, shots=64).result().get_counts()
        if len(ideal) != 1:
            print(f"remap check FAILED for {m}: {ideal}")
            sys.exit(1)
        sim = AerSimulator(method="density_matrix",
                           noise_model=reduce_noise_model(nm_full, m["fil"]))
        counts_per_pub.append(sim.run(small, shots=shots).result().get_counts())

    analysis = analyze_batch(counts_per_pub, plan, shots)
    coop = [s for s in analysis["series"].values()
            if set(s["profile"]) == {"Q"} and "zne" in s]
    improved = 0
    for s in coop:
        ideal_payoff = 4.0 / s["N"]        # V/N, the analytic cooperative payoff
        raw = s["folds"]["1"]["raw"]["mean"]
        zne = s["zne"]["linear"]
        better = abs(zne - ideal_payoff) < abs(raw - ideal_payoff)
        improved += better
        print(f"  {s['topology']:16s} N={s['N']}: |raw-ideal|="
              f"{abs(raw - ideal_payoff):.4f} |ZNE-ideal|="
              f"{abs(zne - ideal_payoff):.4f} "
              f"{'improved' if better else 'NOT improved'}")
    ok = improved > len(coop) / 2
    print(f"rehearsal gate: ZNE improved {improved}/{len(coop)} cooperative "
          f"series -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        sys.exit(1)
    return analysis
```

**Note on the rehearsal threshold:** `hardware_scaling.py` requires `>= 2 of 3`. Here the denominator varies with the cell list, so the gate is "strict majority of cooperative series." A ring or W cell failing to improve under ZNE is expected and is data, not a bug — but a *majority* failing means the batch is not worth submitting.

- [ ] **Step 3: Write the submit and recover paths**

```python
# append to experiments/hardware_topology.py

import json
from datetime import datetime, timezone


def save_run(analysis: dict, plan: dict, job_info: dict, cal: dict,
             shots: int, cal_submit: dict | None = None) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results",
                           "hardware-topology", ts)
    os.makedirs(out_dir, exist_ok=True)
    payload = {
        "experiment": "hardware-topology",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git": git_provenance(),
        "environment": environment_provenance(),
        "job": job_info,
        "shots": shots,
        "note": ("advantage = measured profile payoff minus the ANALYTIC "
                 "noiseless classical NE payoff 1/N. This is the hardware "
                 "convention; simulation figures use the circuit-relative gap "
                 "and the two are NOT comparable."),
        "analysis": analysis,
        "pub_meta": plan["meta"],
    }
    with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    with open(os.path.join(out_dir, "calibration.json"), "w", encoding="utf-8") as fh:
        json.dump(cal, fh, indent=2)
    if cal_submit is not None:
        with open(os.path.join(out_dir, "calibration_at_submit.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(cal_submit, fh, indent=2)
    print(f"\nsaved: {os.path.relpath(os.path.join(out_dir, 'result.json'))}")
    return out_dir


def submit(backend, plan: dict, shots: int) -> str:
    """Submit ONE batch job, persisting the id and calibration BEFORE polling."""
    from qiskit_ibm_runtime import SamplerV2

    cal_submit = chain_calibration(backend, plan["pinned"])
    sampler = SamplerV2(mode=backend)
    job = sampler.run(plan["pubs"], shots=shots)
    job_id = job.job_id()
    _save_pending_job_id(job_id, backend.name)
    with open(_submit_cal_path(job_id), "w", encoding="utf-8") as fh:
        json.dump(cal_submit, fh, indent=2)
    print(f"submitted job {job_id}; id and submit-time calibration persisted.")
    return job_id
```

- [ ] **Step 4: Wire the modes into `main()`**

Replace the `main()` written in Task 3 so `--rehearse`, `--hardware` and `--from-job` build the plan via `build_batch(...)` with the cell list decided in Task 3, call `rehearse(...)` as a mandatory gate before `submit(...)`, and route `--from-job` through `analyze_batch` + `save_run`. Recovery reconstructs `plan["meta"]` by re-running `build_batch` against the same pinned set and asserting the pub count matches the job's; if it does not, abort rather than guess (this is why the pinned set is written into `result.json`).

- [ ] **Step 5: Rehearse end to end with no quota spent**

Run: `conda run -n entangled-equilibria python experiments/hardware_topology.py --rehearse`
Expected: per-cell transpile lines, then a rehearsal table, then `rehearsal gate: ... PASS`. No job id is printed and `pending_jobs.txt` is unchanged.

- [ ] **Step 6: Commit**

```bash
git add experiments/hardware_topology.py
git commit -m "item-9: rehearsal gate, crash-safe submission, and provenance-complete save path"
```

---

### Task 7: Preregister the batch's predictions (before any submission)

**Files:**
- Create: `scripts/preregister_topology.py`
- Create: `results/hardware-topology/preregistration.json` (written by the script)

**Interfaces:**
- Consumes: Task 6's rehearsal analysis
- Produces: a frozen registration file

This is the step that makes these results reviewer-proof rather than exploratory — it is the same moat the scaling result already has. **It must run and be committed before Task 8 submits anything.**

- [ ] **Step 1: Write the registration script**

The script runs the rehearsal on the device noise model and freezes, per series:
- predicted mitigated fold-1 advantage and its predictive sigma;
- for the deviation profiles (item 2): the predicted **deviation gap** `payoff(Q,Q,Q) − payoff(H,Q,Q)` per deviating position, and the registered claim *"all deviation gaps are ≥ 0 at N=3 GHZ"* — this is the hardware equilibrium test, and it is falsifiable;
- for the wiring permutations (item 6): the registered null *"the per-player payoff vector permutes with the wiring"*, scored as the max deviation between the permuted and unpermuted vectors, with a registered threshold;
- for the γ sweep (item 7): the predicted advantage at each γ.

Record `registered_utc`, the git commit, the environment block from `environment_provenance()`, and the exact rehearsal seed. Mirror the structure of `results/hardware-scaling/preregistration.json`.

- [ ] **Step 2: Run it**

Run: `conda run -n entangled-equilibria python scripts/preregister_topology.py`
Expected: writes `results/hardware-topology/preregistration.json`; prints the registered predictions.

- [ ] **Step 3: Commit BEFORE submitting**

```bash
git add scripts/preregister_topology.py results/hardware-topology/preregistration.json
git commit -m "item-9: freeze topology-batch predictions before any hardware submission"
```

The commit timestamp is the evidence that the predictions predate the data. Do not proceed to Task 8 until this is committed.

---

### Task 8: Submit the batch (items 1, 2, 5, 6, 7)

**Files:**
- Create: `results/hardware-topology/<ts>/`

- [ ] **Step 1: Confirm the tree is clean and the registration is committed**

Run: `git status --porcelain && git log --oneline -1`
Expected: empty porcelain output; HEAD is the Task 7 registration commit.

- [ ] **Step 2: Submit**

Run: `conda run -n entangled-equilibria python experiments/hardware_topology.py --hardware`
Expected: rehearsal `PASS`, job id persisted, summary table, `saved: results/hardware-topology/<ts>/result.json`.

If the poll drops, recover with `--from-job <id>` using the id in `results/hardware-topology/pending_jobs.txt`. Do **not** resubmit without first checking whether the original job was billed.

- [ ] **Step 3: Judge against the registration**

Run: `conda run -n entangled-equilibria python scripts/judge_topology_run.py`
Expected: writes `results/hardware-topology/<ts>/judgments.json` with a pass/fail per registered test.

- [ ] **Step 4: Write the finding**

Create `docs/findings/2026-XX-XX-topology-hardware-run1.md` recording, per registered test, the prediction, the measurement, and the verdict — **including the ones that failed**. A failed registered prediction reported honestly is worth more to this paper than a passed one, and the five-model precedent in `repeat-judgments.json` is the template.

- [ ] **Step 5: Commit**

```bash
git add results/hardware-topology/ docs/findings/
git commit -m "item-9: topology/equilibrium/gamma/wiring hardware batch run 1 + registered judgments"
```

---

### Task 9: Repeat the topology batch on distinct calibration days

- [ ] **Step 1:** Repeat Task 8 on 2 further distinct calibration days, checking each time that `calibration_at_submit.json` carries a stamp not seen in a previous run.
- [ ] **Step 2:** After each, re-run `scripts/judge_topology_run.py` and append to the findings doc.
- [ ] **Step 3:** Commit each run separately so the calibration days stay individually traceable.

---

### Task 10: N=6,7 scaling extension (item 4)

**Files:**
- Modify: `experiments/hardware_scaling.py:79` (`NS`), `:82` (`CHAIN_LEN`), `:309-336` (`plan_from_job_circuits`), `:707-753` (`main`)
- Create: `results/hardware-scaling/preregistration-n67.json`

**This task must come after Tasks 0 and 9**, because it changes the script that item 3's cross-day repeats run on.

- [ ] **Step 1: Add `--ns` and `--chain-len` flags whose defaults reproduce today's behaviour exactly**

Replace the module-level `NS`/`CHAIN_LEN` reads with values threaded from `main()`, defaulting to `(3,4,5)` and `5`. `plan_from_job_circuits` currently rebuilds the pub order from module-level `NS`, so it must take `ns` as a parameter; recovery of runs 1–3 then requires `--from-job <id> --ns 3,4,5`, which is the default. Document that in the module docstring.

- [ ] **Step 2: Verify the default path is unchanged**

Run: `conda run -n entangled-equilibria python -m pytest tests/ -q`
Expected: same pass count as Task 2 Step 5.

Run: `conda run -n entangled-equilibria python experiments/hardware_scaling.py`
Expected: byte-identical offline-gate output to before the change (`N=3/4/5` identity + dry-run PASS lines). If it differs at all, the refactor is wrong.

- [ ] **Step 3: Report N=6,7 feasibility**

Run: `conda run -n entangled-equilibria python experiments/hardware_scaling.py --report --ns 3,4,5,6,7 --chain-len 7`
Expected: a 7-qubit chain and per-N cz counts. GHZ needs `2N-3` cz pre-routing and is linear-chain native, so routing should add nothing; if it does, the chain selector found a non-path and that must be fixed before submitting.

- [ ] **Step 4: Preregister the N=6,7 predictions in a NEW file**

Create `results/hardware-scaling/preregistration-n67.json` by fitting `p_eff` on the N=3 point of the most recent run and predicting N=6,7 — the same fit-one-predict-many protocol, extended. **Do not touch `preregistration.json`.** Also register the competing cz-exponential prediction, since the whole point is that it currently outscores the depolarizing fit and N=6,7 is where they separate most.

- [ ] **Step 5: Commit the registration, then submit**

```bash
git add experiments/hardware_scaling.py results/hardware-scaling/preregistration-n67.json
git commit -m "item-4: --ns flag + frozen N=6,7 predictions (preregistration-n67)"
```

Then: `conda run -n entangled-equilibria python experiments/hardware_scaling.py --hardware --ns 3,4,5,6,7 --chain-len 7`

---

### Task 11: Fold the hardware evidence into the paper

**Files:**
- Modify: `paper/main.tex`, `paper/REVIEW-NOTES.md`, `docs/VERIFIED-FACTS.md`, `docs/STATUS.md`, `ITEMS.md`, `results/README.md`

- [ ] **Step 1:** Add the topology hardware table and figure to Sec. IV, with `%`-comments naming the source artifacts.
- [ ] **Step 2:** Promote the Sec. IV-C position-locked-unfairness claim from simulation-only to simulation-plus-hardware, or narrow it if the wiring test did not reproduce on device. `REVIEW-NOTES.md:38` tracks this decision.
- [ ] **Step 3:** If the N=3 deviation gaps came back non-negative, state the restricted-menu equilibrium as hardware-verified in the abstract, Sec. IV and the conclusion. If any came back negative, say so and keep the simulation-only phrasing.
- [ ] **Step 4:** Replace the two-point sample-SD error bars in Fig. 6 with cross-day error bars from Tasks 0 and 9, and update the caption, which currently states they are not a cross-day estimate.
- [ ] **Step 5:** Update `docs/STATUS.md` — it still claims "~12 `\todo`s remain" and that Aasa's sections are unwritten; both are stale as of `d7ee2f5`.
- [ ] **Step 6:** Rebuild and check the page count against the target venue's limit.

Run: `cd paper && latexmk -pdf main.tex`
Expected: builds clean; `Output written on main.pdf (N pages, ...)`.

- [ ] **Step 7: Commit**

```bash
git add paper/ docs/ ITEMS.md results/README.md
git commit -m "paper: fold topology/equilibrium/cross-day hardware evidence into the draft"
```

---

## Self-review notes

**Coverage.** Item 1 → Tasks 3,4,8. Item 2 → Tasks 1 (`profile` seam), 7 (registered deviation-gap test), 8. Item 5 → Task 4 (`folds` axis, extended beyond 1/3/5). Item 6 → Tasks 4 (`wirings` axis), 7 (registered permutation null). Item 7 → Task 4 (`gammas` axis). Item 3 → Task 0 + Task 9. Item 4 → Task 10. Item 8 → Task 0 Step 5.

**Known gaps, deliberately left open.**
1. Task 3's report decides the cell list; Tasks 4–8 cannot name their exact cells until it has run. This is intentional — heavy-hex routing costs are not predictable from the pre-routing gate counts, and guessing them would waste quota.
2. Task 6 Step 4 and Task 7 Step 1 describe their code rather than showing it, because both depend on Task 3's measured cell list. They must be filled in before those tasks execute.
3. `scripts/judge_topology_run.py` is specified by its contract in Tasks 7–8 but has no task of its own; fold it into Task 7 when the registration's exact schema is settled.
