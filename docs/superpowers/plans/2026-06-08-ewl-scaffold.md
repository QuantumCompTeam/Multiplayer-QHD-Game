# Entangled Equilibria — Month-1 EWL Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the minimal repo skeleton and make all 14 Month-1 pytest tests pass, proving that (Q, Q) is a quantum Nash equilibrium with payoff (2, 2) for V=4, C=3.

**Architecture:** `src/` holds two independent subtrees — `circuits/` (Prithvi's layer) and `game/` (Aasa's layer) — that never import each other. They communicate only through a `npt.NDArray[np.float64]` of shape `(2**N,)` returned by `run_two_player`, a shape that is stable from N=2 through N=6. Everything beyond Month 1 is a stub with a signed `NotImplementedError`.

**Tech Stack:** Python 3.10, Qiskit 1.3.2, qiskit-aer 0.14.2, NumPy 1.26.4, pytest 8+, mypy (strict), ruff. Conda env: `entangled-equilibria`. All commands use `conda run -n entangled-equilibria`.

---

## File Map

| File | Status | Responsibility |
|------|--------|----------------|
| `pyproject.toml` | Create | Pinned deps; pytest `pythonpath = ["src"]`; mypy strict; ruff config |
| `src/config.py` | Create | V=4, C=3, GAMMA=π/2; full bit-ordering convention doc |
| `src/circuits/__init__.py` | Create | Empty — marks circuits as a package |
| `src/circuits/ewl.py` | Create | `U(θ,α,β)`, `J_matrix`, `make_J_gate`, `make_J_dag_gate`, `DOVE`/`HAWK`/`Q` |
| `src/circuits/two_player.py` | Create | `run_two_player(s0, s1)` → `NDArray[float64]` shape `(4,)` |
| `src/circuits/topologies.py` | Create | Stubs: `ghz_entangler`, `w_entangler`, `pairwise_entangler` (Month 3) |
| `src/game/__init__.py` | Create | Empty — marks game as a package |
| `src/game/payoffs.py` | Create | `outcome_payoff`, `expected_payoff`, `index_to_bitstring` |
| `src/game/nash.py` | Create | Stub: `nash_equilibria` (Month 2) |
| `src/analysis/__init__.py` | Create | Empty — marks analysis as a package |
| `src/analysis/topology_sweep.py` | Create | Module-level stub (Month 3) |
| `src/analysis/noise_sweep.py` | Create | Module-level stub (Month 4) |
| `tests/test_ewl.py` | Create | 3 gate-level unit tests |
| `tests/test_payoffs.py` | Create | 4 payoff formula unit tests |
| `tests/test_two_player.py` | Create | 7 tests — 4 classical sanity + Month-1 checkpoint + 2 Nash property |
| `results/.gitkeep` | Create | Placeholder for simulation outputs |

---

## Task 0: Install Dependencies

- [ ] **Run the one-time install**

```powershell
conda run -n entangled-equilibria pip install qiskit==1.3.2 qiskit-aer==0.14.2 nashpy==0.0.19 networkx==3.3 numpy==1.26.4 scipy==1.13.1 matplotlib==3.9.2 pytest mypy ruff
```

Expected: pip installs all packages without error. Verify with:

```powershell
conda run -n entangled-equilibria python -c "import qiskit; print(qiskit.__version__)"
```

Expected output: `1.3.2`

---

## Task 1: pyproject.toml

**Files:** Create `pyproject.toml`

- [ ] **Create pyproject.toml with full contents**

```toml
[project]
name = "entangled-equilibria"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "qiskit==1.3.2",
    "qiskit-aer==0.14.2",
    "nashpy==0.0.19",
    "networkx==3.3",
    "numpy==1.26.4",
    "scipy==1.13.1",
    "matplotlib==3.9.2",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "mypy>=1.10", "ruff>=0.5"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.mypy]
strict = true
python_version = "3.10"
ignore_missing_imports = true

[tool.ruff.lint]
select = ["E", "F", "I"]
```

- [ ] **Verify pytest can find the test directory (no tests collected yet is fine)**

```powershell
conda run -n entangled-equilibria pytest --collect-only
```

Expected output contains: `no tests ran` or `0 items` (no error, just nothing collected yet).

---

## Task 2: src/config.py

**Files:** Create `src/config.py`

- [ ] **Create directory structure and config.py**

```powershell
New-Item -ItemType Directory -Force src
```

- [ ] **Create `src/config.py` with full contents**

```python
"""Single source of truth for game parameters and the bit-ordering convention.

BIT ORDERING CONVENTION
=======================
All probability arrays in this project follow Qiskit's statevector
little-endian ordering. Qubit j occupies bit position j (value 2**j)
of the integer index.

For an N-qubit system, integer index i encodes:
  player j plays Hawk  <=>  (i >> j) & 1 == 1
  player j plays Dove  <=>  (i >> j) & 1 == 0

Worked example (N=2):
  i=0 (0b00) -> player 0 Dove, player 1 Dove
  i=1 (0b01) -> player 0 HAWK, player 1 Dove   (bit 0 = player 0)
  i=2 (0b10) -> player 0 Dove, player 1 HAWK   (bit 1 = player 1)
  i=3 (0b11) -> player 0 HAWK, player 1 HAWK

This matches Statevector.probabilities() output directly — no reordering needed.
Use index_to_bitstring(i, N) in game/payoffs.py for human-readable labels.
"""

import math

V: float = 4.0  # resource value
C: float = 3.0  # conflict cost (must satisfy C > V/2 for meaningful Hawk-Dove dynamics)

GAMMA: float = math.pi / 2
# CRITICAL: maximum entanglement requires gamma = pi/2.
# Symptom of wrong gamma: (Q,Q) payoff falls below (2,2) and Nash property fails.
# Do not change without re-running test_two_player.py.
```

---

## Task 3: src/circuits/ewl.py

**Files:** Create `src/circuits/__init__.py`, `src/circuits/ewl.py`

- [ ] **Create circuits package**

```powershell
New-Item -ItemType Directory -Force src\circuits
New-Item -ItemType File src\circuits\__init__.py
```

- [ ] **Create `src/circuits/ewl.py` with full contents**

```python
"""EWL protocol: strategy unitary U(θ,α,β), entangling operators J and J†,
and named strategy constants DOVE, HAWK, Q.
"""

from __future__ import annotations

import math
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from qiskit.circuit.library import UnitaryGate

from config import GAMMA

# (theta, alpha, beta) parameters for an SU(2) player strategy
StrategyParams: TypeAlias = tuple[float, float, float]


def U(theta: float, alpha: float, beta: float) -> npt.NDArray[np.complex128]:
    """Return the 2×2 SU(2) strategy unitary for the EWL protocol.

    U(θ,α,β) = [ e^(iα)·cos(θ/2)      i·e^(iβ)·sin(θ/2)  ]
               [ i·e^(-iβ)·sin(θ/2)   e^(-iα)·cos(θ/2)   ]

    Classical mappings:
      DOVE = U(0, 0, 0)         -> Identity
      HAWK = U(π, 0, 0)         -> i·σX  (global phase i; unobservable in measurement)
      Q    = U(0, π/2, π/2)     -> quantum Nash equilibrium strategy
    """
    c = math.cos(theta / 2)
    s = math.sin(theta / 2)
    return np.array(
        [
            [np.exp(1j * alpha) * c, 1j * np.exp(1j * beta) * s],
            [1j * np.exp(-1j * beta) * s, np.exp(-1j * alpha) * c],
        ],
        dtype=np.complex128,
    )


def J_matrix(gamma: float) -> npt.NDArray[np.complex128]:
    """Return the 4×4 EWL entangling matrix for 2 qubits.

    J(γ) = exp(i·γ/2 · X⊗X) = cos(γ/2)·(I⊗I) + i·sin(γ/2)·(X⊗X)

    At γ=π/2: J = (I⊗I + i·X⊗X) / √2  (maximum entanglement).

    Built from its matrix definition — NOT via RXXGate, which implements
    exp(-i·γ/2·X⊗X) with the wrong sign convention.
    """
    c = math.cos(gamma / 2)
    s = math.sin(gamma / 2)
    # X⊗X in computational basis |00>,|01>,|10>,|11> (Qiskit little-endian)
    # X⊗X maps: |00><->|11>, |01><->|10>
    xx = np.array(
        [
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [1, 0, 0, 0],
        ],
        dtype=np.complex128,
    )
    return c * np.eye(4, dtype=np.complex128) + 1j * s * xx


def make_J_gate(gamma: float = GAMMA) -> UnitaryGate:
    """Return J(gamma) wrapped as a 2-qubit Qiskit UnitaryGate."""
    return UnitaryGate(J_matrix(gamma), label="J")


def make_J_dag_gate(gamma: float = GAMMA) -> UnitaryGate:
    """Return J†(gamma) wrapped as a 2-qubit Qiskit UnitaryGate."""
    return UnitaryGate(J_matrix(gamma).conj().T, label="J†")


# Named strategy parameter tuples — pass directly to run_two_player(s0, s1)
DOVE: StrategyParams = (0.0, 0.0, 0.0)
HAWK: StrategyParams = (math.pi, 0.0, 0.0)
Q: StrategyParams = (0.0, math.pi / 2, math.pi / 2)
```

---

## Task 4: tests/test_ewl.py — Write and Run

**Files:** Create `tests/test_ewl.py`

- [ ] **Create tests directory and test_ewl.py**

```powershell
New-Item -ItemType Directory -Force tests
```

- [ ] **Create `tests/test_ewl.py` with full contents**

```python
"""Unit tests for EWL strategy unitary U and entangling matrix J."""

import numpy as np
import numpy.typing as npt

from circuits.ewl import J_matrix, U
from config import GAMMA

SIGMA_X: npt.NDArray[np.complex128] = np.array(
    [[0, 1], [1, 0]], dtype=np.complex128
)


def test_dove_is_identity() -> None:
    """U(0,0,0) must equal the 2×2 identity (Dove = no action)."""
    assert np.allclose(U(0.0, 0.0, 0.0), np.eye(2, dtype=np.complex128), atol=1e-10)


def test_hawk_is_i_sigma_x() -> None:
    """U(π,0,0) = i·σX per the README formula.

    The global phase i is unobservable in measurement outcomes.
    Elementwise: U[0,1] = i, U[1,0] = i, U[0,0] = U[1,1] = 0.
    """
    assert np.allclose(U(np.pi, 0.0, 0.0), 1j * SIGMA_X, atol=1e-10)


def test_J_is_unitary() -> None:
    """J(γ) must satisfy J @ J† = I₄ (unitary operator)."""
    jm = J_matrix(GAMMA)
    assert np.allclose(jm @ jm.conj().T, np.eye(4, dtype=np.complex128), atol=1e-10)
```

- [ ] **Run test_ewl.py and verify all 3 tests pass**

```powershell
conda run -n entangled-equilibria pytest tests/test_ewl.py -v
```

Expected output:
```
tests/test_ewl.py::test_dove_is_identity PASSED
tests/test_ewl.py::test_hawk_is_i_sigma_x PASSED
tests/test_ewl.py::test_J_is_unitary PASSED

3 passed
```

- [ ] **Commit**

```powershell
git add src/config.py src/circuits/__init__.py src/circuits/ewl.py tests/test_ewl.py pyproject.toml
git commit -m "feat: add config, EWL gates, and gate unit tests (3 passing)"
```

---

## Task 5: src/game/payoffs.py

**Files:** Create `src/game/__init__.py`, `src/game/payoffs.py`

- [ ] **Create game package**

```powershell
New-Item -ItemType Directory -Force src\game
New-Item -ItemType File src\game\__init__.py
```

- [ ] **Create `src/game/payoffs.py` with full contents**

```python
"""N-player Hawk-Dove payoff functions (Benjamin-Hayden formula).

Interface contract (producer side):
  expected_payoff(probs, N, V, C) accepts probs of shape (2**N,) — the direct
  output of any run_*_player function in circuits/. Shape is stable from N=2
  through N=6 without interface changes. result[j] = expected payoff for player j.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from config import C as DEFAULT_C, V as DEFAULT_V


def index_to_bitstring(i: int, n: int) -> str:
    """Return the Qiskit-convention bitstring for basis state index i with n qubits.

    Rightmost character = player 0 (qubit 0). Little-endian.
    Example: n=2, i=1 -> '01'  (player 0 Hawk, player 1 Dove).
    Example: n=2, i=2 -> '10'  (player 0 Dove, player 1 Hawk).
    """
    return format(i, f"0{n}b")


def outcome_payoff(i: int, N: int, V: float, C: float) -> npt.NDArray[np.float64]:
    """Return per-player payoffs for basis state index i (Benjamin-Hayden formula).

    Player j is Hawk iff (i >> j) & 1 == 1  (Qiskit little-endian, see config.py).
    k = number of Hawks = popcount(i).

    Formula:
      k == 0           : all Dove  — each gets V/N
      0 < k < N        : Hawks take all — each Hawk gets V/k, each Dove gets 0
      k == N           : all Hawk  — each gets (V-C)/k  (conflict cost shared)

    Returns shape (N,). result[j] = payoff for player j in outcome i.
    """
    k = bin(i).count("1")
    dove_pay: float
    hawk_pay: float
    if k == 0:
        dove_pay = V / N
        hawk_pay = 0.0  # no Hawks present; value unused in loop below
    elif k == N:
        dove_pay = 0.0
        hawk_pay = (V - C) / k
    else:
        dove_pay = 0.0
        hawk_pay = V / k

    payoffs = np.zeros(N, dtype=np.float64)
    for j in range(N):
        payoffs[j] = hawk_pay if (i >> j) & 1 else dove_pay
    return payoffs


def expected_payoff(
    probs: npt.NDArray[np.float64],
    N: int,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
) -> npt.NDArray[np.float64]:
    """Return expected per-player payoffs given a probability distribution.

    probs: shape (2**N,) — direct output of run_two_player or any run_*_player.
           probs[i] = P(measuring basis state |i>). Must sum to 1.
    Returns: shape (N,). result[j] = expected payoff for player j.
    Shape contract is stable from N=2 through N=6 without changes to this function.
    """
    result = np.zeros(N, dtype=np.float64)
    for i in range(2**N):
        result += probs[i] * outcome_payoff(i, N, V, C)
    return result
```

---

## Task 6: tests/test_payoffs.py — Write and Run

**Files:** Create `tests/test_payoffs.py`

- [ ] **Create `tests/test_payoffs.py` with full contents**

```python
"""Unit tests for the Benjamin-Hayden N-player Hawk-Dove payoff function.

Tests the 2-player payoff table (N=2, V=4, C=3) against all four classical
strategy combinations. Bit ordering: i=1 (0b01) -> player 0 Hawk (LSB=bit0).
"""

import numpy as np

from game.payoffs import outcome_payoff


def test_dove_dove() -> None:
    """i=0 (0b00): both Dove -> each gets V/N = 4/2 = 2."""
    np.testing.assert_allclose(outcome_payoff(0, 2, 4.0, 3.0), [2.0, 2.0], atol=1e-10)


def test_hawk_dove() -> None:
    """i=1 (0b01): player 0 Hawk (bit 0 set), player 1 Dove -> [4, 0]."""
    np.testing.assert_allclose(outcome_payoff(1, 2, 4.0, 3.0), [4.0, 0.0], atol=1e-10)


def test_dove_hawk() -> None:
    """i=2 (0b10): player 0 Dove, player 1 Hawk (bit 1 set) -> [0, 4]."""
    np.testing.assert_allclose(outcome_payoff(2, 2, 4.0, 3.0), [0.0, 4.0], atol=1e-10)


def test_hawk_hawk() -> None:
    """i=3 (0b11): both Hawk -> each gets (V-C)/k = (4-3)/2 = 0.5."""
    np.testing.assert_allclose(outcome_payoff(3, 2, 4.0, 3.0), [0.5, 0.5], atol=1e-10)
```

- [ ] **Run test_payoffs.py and verify all 4 tests pass**

```powershell
conda run -n entangled-equilibria pytest tests/test_payoffs.py -v
```

Expected output:
```
tests/test_payoffs.py::test_dove_dove PASSED
tests/test_payoffs.py::test_hawk_dove PASSED
tests/test_payoffs.py::test_dove_hawk PASSED
tests/test_payoffs.py::test_hawk_hawk PASSED

4 passed
```

- [ ] **Commit**

```powershell
git add src/game/__init__.py src/game/payoffs.py tests/test_payoffs.py
git commit -m "feat: add Benjamin-Hayden payoff function and payoff unit tests (4 passing)"
```

---

## Task 7: src/circuits/two_player.py

**Files:** Create `src/circuits/two_player.py`

- [ ] **Create `src/circuits/two_player.py` with full contents**

```python
"""Month-1 two-player EWL Hawk-Dove circuit.

Circuit sequence for N=2:
  |00> --[J(γ)]-- [U(s0) ⊗ U(s1)] --[J†(γ)]-- Statevector

Returns exact probabilities via Qiskit Statevector (no sampling, no randomness).

Interface contract (producer side):
  run_two_player returns NDArray[float64] of shape (4,) = (2**2,).
  probs[i] = P(measuring |i>). Bit ordering: Qiskit little-endian (see config.py).
  sum(result) == 1.0.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector

from circuits.ewl import U, make_J_dag_gate, make_J_gate, StrategyParams
from config import GAMMA


def run_two_player(
    s0: StrategyParams,
    s1: StrategyParams,
    *,
    gamma: float = GAMMA,
) -> npt.NDArray[np.float64]:
    """Run the 2-player EWL circuit and return exact outcome probabilities.

    s0: (theta, alpha, beta) for player 0 (qubit 0).
    s1: (theta, alpha, beta) for player 1 (qubit 1).
    gamma: entanglement parameter. Must equal pi/2 for the Nash equilibrium
           property to hold — see GAMMA guard in config.py.

    Returns shape (4,) = (2**2,). probs[i] = P(measuring basis state |i>).
    Bit ordering: player j is Hawk iff (i >> j) & 1 == 1 (Qiskit little-endian).
    """
    qc = QuantumCircuit(2)
    qc.append(make_J_gate(gamma), [0, 1])
    qc.append(UnitaryGate(U(*s0)), [0])
    qc.append(UnitaryGate(U(*s1)), [1])
    qc.append(make_J_dag_gate(gamma), [0, 1])
    return np.asarray(Statevector(qc).probabilities(), dtype=np.float64)
```

---

## Task 8: tests/test_two_player.py — Write and Run (Month-1 Checkpoint)

**Files:** Create `tests/test_two_player.py`

- [ ] **Create `tests/test_two_player.py` with full contents**

```python
"""Month-1 checkpoint: two-player EWL Hawk-Dove validation.

Proves three things:
  1. Classical strategy pairs reproduce the 2×2 Hawk-Dove payoff table exactly.
  2. (Q, Q) yields expected payoff (2.0, 2.0) — the quantum Nash equilibrium.
  3. Nash property: neither player improves above 2.0 by deviating from Q to
     any classical strategy (Hawk or Dove).

All results come from exact statevector simulation — no sampling, no hardcoding.
"""

import numpy as np

from circuits.ewl import DOVE, HAWK, Q
from circuits.two_player import run_two_player
from game.payoffs import expected_payoff

_V, _C, _N = 4.0, 3.0, 2


def _ep(s0: tuple[float, float, float], s1: tuple[float, float, float]) -> np.ndarray:  # type: ignore[type-arg]
    return expected_payoff(run_two_player(s0, s1), _N, _V, _C)


# ── Classical sanity: all four entries of the Hawk-Dove payoff matrix ──────────

def test_classical_dove_dove() -> None:
    np.testing.assert_allclose(_ep(DOVE, DOVE), [2.0, 2.0], atol=1e-6)


def test_classical_dove_hawk() -> None:
    np.testing.assert_allclose(_ep(DOVE, HAWK), [0.0, 4.0], atol=1e-6)


def test_classical_hawk_dove() -> None:
    np.testing.assert_allclose(_ep(HAWK, DOVE), [4.0, 0.0], atol=1e-6)


def test_classical_hawk_hawk() -> None:
    np.testing.assert_allclose(_ep(HAWK, HAWK), [0.5, 0.5], atol=1e-6)


# ── Month-1 checkpoint ─────────────────────────────────────────────────────────

def test_q_q_yields_cooperative_payoff() -> None:
    """(Q, Q) -> expected payoff (2.0, 2.0): the quantum Nash equilibrium.

    Passes iff GAMMA == pi/2 and J is built with the correct sign convention.
    Wrong gamma or wrong sign produces a payoff below (2, 2).
    """
    np.testing.assert_allclose(_ep(Q, Q), [2.0, 2.0], atol=1e-6)


# ── Nash property: Q is a best response to Q ──────────────────────────────────

def test_nash_hawk_deviation_does_not_improve() -> None:
    """Player 0 deviating to HAWK while player 1 stays on Q must not exceed 2.0."""
    payoff = _ep(HAWK, Q)[0]
    assert payoff <= 2.0 + 1e-6, (
        f"Nash property violated: HAWK deviation yielded {payoff:.8f} > 2.0"
    )


def test_nash_dove_deviation_does_not_improve() -> None:
    """Player 0 deviating to DOVE while player 1 stays on Q must not exceed 2.0."""
    payoff = _ep(DOVE, Q)[0]
    assert payoff <= 2.0 + 1e-6, (
        f"Nash property violated: DOVE deviation yielded {payoff:.8f} > 2.0"
    )
```

- [ ] **Run test_two_player.py and verify all 7 tests pass**

```powershell
conda run -n entangled-equilibria pytest tests/test_two_player.py -v
```

Expected output:
```
tests/test_two_player.py::test_classical_dove_dove PASSED
tests/test_two_player.py::test_classical_dove_hawk PASSED
tests/test_two_player.py::test_classical_hawk_dove PASSED
tests/test_two_player.py::test_classical_hawk_hawk PASSED
tests/test_two_player.py::test_q_q_yields_cooperative_payoff PASSED
tests/test_two_player.py::test_nash_hawk_deviation_does_not_improve PASSED
tests/test_two_player.py::test_nash_dove_deviation_does_not_improve PASSED

7 passed
```

If `test_q_q_yields_cooperative_payoff` fails with a payoff below 2.0: the J operator has a sign error. Check that `J_matrix` in `ewl.py` uses `+1j * s * xx` (not `-1j`). Do NOT change GAMMA.

- [ ] **Commit**

```powershell
git add src/circuits/two_player.py tests/test_two_player.py
git commit -m "feat: add two-player EWL circuit and pass Month-1 checkpoint (7 passing)"
```

---

## Task 9: Remaining Stubs

**Files:** Create `src/circuits/topologies.py`, `src/game/nash.py`, `src/analysis/__init__.py`, `src/analysis/topology_sweep.py`, `src/analysis/noise_sweep.py`

- [ ] **Create `src/circuits/topologies.py` with full contents**

```python
"""Stub: N-player entanglement topology circuits. Month 3.

All functions raise NotImplementedError. Signatures are final — do not change
them when implementing; only replace the raise with a real circuit body.
"""

from __future__ import annotations

import networkx as nx
from qiskit.circuit import QuantumCircuit


def ghz_entangler(N: int, gamma: float) -> QuantumCircuit:
    """Return N-qubit GHZ entangling circuit parameterised by gamma. Month 3.

    Circuit: Hadamard on qubit 0, then CNOT(0, j) for j in 1..N-1.
    At gamma=pi/2 produces |GHZ> = (|0...0> + |1...1>) / sqrt(2).
    """
    raise NotImplementedError("Month 3: GHZ entangler for N-player circuit")


def w_entangler(N: int, gamma: float) -> QuantumCircuit:
    """Return N-qubit W-state entangling circuit parameterised by gamma. Month 3.

    Recursive F-gate + CNOT construction; pairwise entanglement survives
    single-qubit loss (more noise-robust than GHZ for N > 4).
    """
    raise NotImplementedError("Month 3: W-state entangler for N-player circuit")


def pairwise_entangler(graph: nx.Graph, gamma: float) -> QuantumCircuit:
    """Return circuit applying Rxx(gamma) per edge of graph. Month 3.

    graph: NetworkX graph where nodes are qubit indices and edges define
           entanglement links (ring, star, or fully-connected).

    SIGN CONVENTION WARNING: Qiskit RXXGate(θ) implements exp(-i·θ/2·X⊗X).
    This is the OPPOSITE sign from J in ewl.py (which uses exp(+i·γ/2·X⊗X)).
    When implementing, either negate gamma or construct via UnitaryGate to
    maintain consistent convention with the 2-player circuit.
    """
    raise NotImplementedError("Month 3: pairwise entangler for graph-topology circuit")
```

- [ ] **Create `src/game/nash.py` with full contents**

```python
"""Stub: Nash equilibrium computation via Nashpy. Month 2.

Signature is final — do not change it when implementing.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def nash_equilibria(
    payoff_tensor: npt.NDArray[np.float64],
) -> list[tuple[npt.NDArray[np.float64], ...]]:
    """Compute Nash equilibria via Nashpy support enumeration. Month 2.

    payoff_tensor: shape (N, M, M, ...) where N = players, M = strategy count.
    Returns list of Nash equilibria as tuples of mixed-strategy probability arrays.
    """
    raise NotImplementedError("Month 2: Nash equilibria via Nashpy support enumeration")
```

- [ ] **Create analysis package and stubs**

```powershell
New-Item -ItemType Directory -Force src\analysis
New-Item -ItemType File src\analysis\__init__.py
```

- [ ] **Create `src/analysis/topology_sweep.py` with full contents**

```python
"""Stub: topology sweep across all 5 entanglement topologies for N=3..6. Month 3."""

raise NotImplementedError(
    "Month 3: topology sweep — run all 5 topologies (GHZ, W, ring, star, FC) "
    "for N in {3, 4, 5, 6} and compute quantum advantage heatmap"
)
```

- [ ] **Create `src/analysis/noise_sweep.py` with full contents**

```python
"""Stub: depolarizing noise sweep using Qiskit Aer. Month 4."""

raise NotImplementedError(
    "Month 4: noise sweep — AerSimulator with depolarizing channel, "
    "sweep p from 0.0 to 0.05 in steps of 0.005, one surface per topology"
)
```

---

## Task 10: results/.gitkeep

**Files:** Create `results/.gitkeep`

- [ ] **Create results directory and gitkeep**

```powershell
New-Item -ItemType Directory -Force results
New-Item -ItemType File results\.gitkeep
```

---

## Task 11: Full Pytest Suite

- [ ] **Run the complete test suite and verify all 14 tests pass**

```powershell
conda run -n entangled-equilibria pytest -v
```

Expected output:
```
tests/test_ewl.py::test_dove_is_identity PASSED
tests/test_ewl.py::test_hawk_is_i_sigma_x PASSED
tests/test_ewl.py::test_J_is_unitary PASSED
tests/test_payoffs.py::test_dove_dove PASSED
tests/test_payoffs.py::test_hawk_dove PASSED
tests/test_payoffs.py::test_dove_hawk PASSED
tests/test_payoffs.py::test_hawk_hawk PASSED
tests/test_two_player.py::test_classical_dove_dove PASSED
tests/test_two_player.py::test_classical_dove_hawk PASSED
tests/test_two_player.py::test_classical_hawk_dove PASSED
tests/test_two_player.py::test_classical_hawk_hawk PASSED
tests/test_two_player.py::test_q_q_yields_cooperative_payoff PASSED
tests/test_two_player.py::test_nash_hawk_deviation_does_not_improve PASSED
tests/test_two_player.py::test_nash_dove_deviation_does_not_improve PASSED

14 passed
```

If any test fails, do not proceed to the commit. Diagnose with `pytest -v --tb=short`.

---

## Task 12: Final Commit

- [ ] **Stage all remaining files and commit**

```powershell
git add src/circuits/topologies.py src/game/nash.py src/analysis/__init__.py src/analysis/topology_sweep.py src/analysis/noise_sweep.py results/.gitkeep
git commit -m "feat: scaffold repo and pass Month-1 two-player EWL validation"
```

Expected: commit succeeds, `git log --oneline -3` shows three new commits from this session.

---

## Diagnostic Reference

If `test_q_q_yields_cooperative_payoff` fails:
- **Payoff << 2.0 (e.g., ~0.5):** GAMMA is wrong. Check `config.py` — must be `math.pi / 2`.
- **Payoff ≈ 0.5 even with correct GAMMA:** J sign is wrong. In `ewl.py::J_matrix`, the term must be `+1j * s * xx`, not `-1j * s * xx`.
- **Payoff ≈ 2.0 but assertion tolerance fails:** Tighten with `atol=1e-4` temporarily to diagnose, then investigate the source of numerical drift.

If Nash property tests fail (payoff > 2.0 + 1e-6):
- This means HAWK or DOVE gives a higher payoff than Q against a Q-playing opponent.
- The most likely cause is a qubit ordering error — player 0 and player 1 are swapped in the circuit append order. Check `qc.append(UnitaryGate(U(*s0)), [0])` vs `[1]`.
