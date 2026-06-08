# Design Spec: Entangled Equilibria — Scaffold + Month-1 Two-Player EWL Validation

**Date:** 2026-06-08
**Author:** Prithvi Raghu (circuits layer) + Claude
**Status:** Approved — ready for implementation plan

---

## 1. Goal

Build the minimal repo skeleton that makes the Month-1 checkpoint verifiable in isolation:
> *Q is a Nash equilibrium strategy with payoff (2, 2) for V=4, C=3.*

Everything beyond Month 1 is stubbed with signed `NotImplementedError` messages so
that the circuit layer (Prithvi) and the game-theory layer (Aasa) can develop in
parallel on separate modules without merge conflicts.

---

## 2. Environment

- **Conda env:** `entangled-equilibria`
- **Python invocation:** `conda run -n entangled-equilibria python` (or direct path
  `C:\Users\prith\anaconda3\envs\entangled-equilibria\python.exe`)
- **Pinned dependencies:**

  ```
  qiskit==1.3.2
  qiskit-aer==0.14.2
  nashpy==0.0.19
  networkx==3.3
  numpy==1.26.4
  scipy==1.13.1
  matplotlib==3.9.2
  pytest>=8.0
  mypy>=1.10
  ruff>=0.5
  ```

- **One-time install command:**
  ```powershell
  conda run -n entangled-equilibria pip install qiskit==1.3.2 qiskit-aer==0.14.2 nashpy==0.0.19 networkx==3.3 numpy==1.26.4 scipy==1.13.1 matplotlib==3.9.2 pytest mypy ruff
  ```

---

## 3. Repository Layout

```
src/
  config.py               # single source of truth: V, C, GAMMA, bit-ordering doc
  circuits/
    __init__.py
    ewl.py                # U(θ,α,β), J(γ,N), J_dag(γ,N), DOVE/HAWK/Q constants
    two_player.py         # run_two_player(s0, s1) → NDArray[float64] shape (4,)
    topologies.py         # stubs: ghz_entangler, w_entangler, pairwise_entangler
  game/
    __init__.py
    payoffs.py            # outcome_payoff, expected_payoff, index_to_bitstring
    nash.py               # stub: nash_equilibria
  analysis/
    __init__.py
    topology_sweep.py     # stub (Month 3)
    noise_sweep.py        # stub (Month 4)
tests/
  test_ewl.py
  test_payoffs.py
  test_two_player.py
results/
  .gitkeep
pyproject.toml
```

**Import resolution:** `pyproject.toml` sets `[tool.pytest.ini_options] pythonpath = ["src"]`.
No `pip install -e .` required. Tests import as `from circuits.ewl import U`.

**Dependency direction (acyclic):**
```
tests          → circuits.*, game.*
game.payoffs   → config
circuits.ewl   → config
circuits.two_player → circuits.ewl, config
analysis.*     → circuits.*, game.*   (Month 3+, currently stubs)
```

The `game/` and `circuits/` subtrees share no imports. They communicate only through
the ndarray returned by `run_two_player`. This is the parallel-development guarantee.

---

## 4. Interface Contract

This is the single agreed boundary between the circuit layer and the game-theory layer.
Both sides must preserve this contract when adding N-player variants.

**Producer — `circuits/two_player.py`:**
```python
StrategyParams = tuple[float, float, float]  # (theta, alpha, beta)

def run_two_player(
    s0: StrategyParams,
    s1: StrategyParams,
    *,
    gamma: float = GAMMA,
) -> npt.NDArray[np.float64]:
    """Return probability distribution over 2-qubit computational basis.

    Returns shape (4,) = (2**2,). probs[i] = P(measuring basis state |i>).
    Bit ordering: Qiskit little-endian — player j is Hawk iff (i >> j) & 1 == 1.
    sum(result) == 1.0 (exact statevector, no sampling).
    """
```

**Consumer — `game/payoffs.py`:**
```python
def expected_payoff(
    probs: npt.NDArray[np.float64],   # shape (2**N,) — direct output of run_*_player
    N: int,
    V: float,
    C: float,
) -> npt.NDArray[np.float64]:
    """Return expected per-player payoffs. result[j] = expected payoff for player j.

    Accepts the (2**N,) probability array produced by any run_*_player function.
    Shape is stable from N=2 through N=6 without breaking changes.
    """
```

**Shape stability:** when N-player circuits are added in Month 2+, they return
`shape (2**N,)`. `expected_payoff` accepts it unchanged. No interface evolution needed.

---

## 5. Bit-Ordering Convention

Defined once in `config.py` as a module-level documentation block (not a variable):

```
BIT ORDERING CONVENTION
=======================
All probability arrays follow Qiskit's statevector little-endian ordering.
Qubit j occupies bit position j (value 2**j) of the integer index.

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
```

`index_to_bitstring(i, N)` returns `format(i, f'0{N}b')`.
Example: `index_to_bitstring(1, 2)` → `"01"` (rightmost char = player 0).

---

## 6. EWL Circuit Design

### 6.1 Strategy Unitary U(θ, α, β)

Implements the README formula exactly:

```
U(θ,α,β) = [ e^(iα)·cos(θ/2)     i·e^(iβ)·sin(θ/2)  ]
            [ i·e^(-iβ)·sin(θ/2)  e^(-iα)·cos(θ/2)   ]
```

Returns `npt.NDArray[np.complex128]` of shape `(2, 2)`.

**Named strategy constants** (defined by calling `U`):
```python
DOVE: StrategyParams = (0.0, 0.0, 0.0)          # U(0,0,0) = Identity
HAWK: StrategyParams = (np.pi, 0.0, 0.0)         # U(π,0,0) = i·σX (global phase i)
Q:    StrategyParams = (0.0, np.pi/2, np.pi/2)   # the quantum Nash strategy
```

**Phase note for HAWK:** `U(π, 0, 0) = [[0, i], [i, 0]] = i·σX`. The global phase `i`
is unobservable in measurement outcomes. Tests assert `np.allclose(U(π,0,0), 1j*σX)`,
not equality to `σX`.

### 6.2 Entangling Operator J(γ, N=2)

Built as a `UnitaryGate` from its 4×4 matrix — NOT via `RXXGate` (wrong sign):

```
J(γ) = exp(i·γ/2 · X⊗X)
      = cos(γ/2)·(I⊗I) + i·sin(γ/2)·(X⊗X)
```

At `γ = π/2` (maximum entanglement):
```
J = (I⊗I + i·X⊗X) / √2
```

`J_dag` = `J.conj().T`, also wrapped as a `UnitaryGate`.

**GAMMA guard in config.py:**
```python
GAMMA: float = math.pi / 2
# CRITICAL: maximum entanglement requires gamma = pi/2.
# Symptom of wrong gamma: (Q,Q) payoff falls below (2,2) and Nash property fails.
# Do not change without re-running test_two_player.py.
```

### 6.3 Two-Player Circuit Sequence

`run_two_player(s0, s1, *, gamma=GAMMA)`:
1. `QuantumCircuit(2)` — initialised to |00⟩
2. `circuit.append(J_gate, [0, 1])`
3. `circuit.append(UnitaryGate(U(*s0)), [0])`
4. `circuit.append(UnitaryGate(U(*s1)), [1])`
5. `circuit.append(J_dag_gate, [0, 1])`
6. `return Statevector(circuit).probabilities()` → shape `(4,)`, exact, no sampling

---

## 7. Payoff Function Design

### 7.1 Benjamin-Hayden Formula

```
k = popcount(i)   # number of Hawks in outcome i

dove_payoff(k, N, V) = V/N   if k == 0
                     = 0.0   if k > 0

hawk_payoff(k, N, V, C) = V/k       if 0 < k < N   (Hawk faces Doves, takes all)
                        = (V-C)/k   if k == N       (all Hawks, conflict cost shared)
```

### 7.2 Verification Table (N=2, V=4, C=3)

| i | binary | k | dove | hawk | outcome_payoff result | test assertion |
|---|--------|---|------|------|-----------------------|----------------|
| 0 | 00 | 0 | 2.0 | — | [2.0, 2.0] | (D,D) → (2, 2) ✓ |
| 1 | 01 | 1 | 0.0 | 4.0 | [4.0, 0.0] | (H,D) → (4, 0) ✓ |
| 2 | 10 | 1 | 0.0 | 4.0 | [0.0, 4.0] | (D,H) → (0, 4) ✓ |
| 3 | 11 | 2 | — | 0.5 | [0.5, 0.5] | (H,H) → (0.5, 0.5) ✓ |

### 7.3 expected_payoff

```python
result = np.zeros(N)
for i in range(2**N):
    result += probs[i] * outcome_payoff(i, N, V, C)
return result
```

---

## 8. Stub Contracts

All stubs raise `NotImplementedError` with a milestone tag. Signatures are final.

**`circuits/topologies.py`:**
```python
def ghz_entangler(N: int, gamma: float) -> QuantumCircuit:
    """Return N-qubit GHZ entangling circuit parameterised by gamma. Month 3."""
    raise NotImplementedError("Month 3")

def w_entangler(N: int, gamma: float) -> QuantumCircuit:
    """Return N-qubit W-state entangling circuit. Month 3."""
    raise NotImplementedError("Month 3")

def pairwise_entangler(graph: nx.Graph, gamma: float) -> QuantumCircuit:
    """Return circuit applying Rxx(gamma) per edge of graph (ring/star/FC). Month 3.
    NOTE: Qiskit RXXGate(θ) = exp(-i·θ/2·X⊗X). Pass gamma directly; the sign
    convention differs from J — document carefully when implementing.
    """
    raise NotImplementedError("Month 3")
```

**`game/nash.py`:**
```python
def nash_equilibria(
    payoff_tensor: npt.NDArray[np.float64],
) -> list[tuple[npt.NDArray[np.float64], ...]]:
    """Compute Nash equilibria via Nashpy support enumeration. Month 2."""
    raise NotImplementedError("Month 2")
```

**`analysis/topology_sweep.py`**, **`analysis/noise_sweep.py`:** module-level
`raise NotImplementedError` with Month 3 / Month 4 tags respectively.

---

## 9. Test Specifications

### `test_ewl.py`

| # | Assertion | Tolerance |
|---|-----------|-----------|
| 1 | `np.allclose(U(0, 0, 0), np.eye(2))` — DOVE is Identity | 1e-10 |
| 2 | `np.allclose(U(np.pi, 0, 0), 1j * sigma_x)` — HAWK is i·σX | 1e-10 |
| 3 | `np.allclose(J_matrix @ J_dag_matrix, np.eye(4))` — J is unitary | 1e-10 |

### `test_payoffs.py`

| # | Assertion | Notes |
|---|-----------|-------|
| 1 | `outcome_payoff(0, 2, 4, 3) ≈ [2., 2.]` | (D,D) |
| 2 | `outcome_payoff(1, 2, 4, 3) ≈ [4., 0.]` | (H,D): i=1, bit 0 set = player 0 Hawk |
| 3 | `outcome_payoff(2, 2, 4, 3) ≈ [0., 4.]` | (D,H): i=2, bit 1 set = player 1 Hawk |
| 4 | `outcome_payoff(3, 2, 4, 3) ≈ [0.5, 0.5]` | (H,H) |

All `atol=1e-10`.

### `test_two_player.py` — Month-1 Checkpoint

| # | Assertion | Tolerance | What it proves |
|---|-----------|-----------|----------------|
| 1 | `expected_payoff(run_two_player(DOVE,DOVE), 2,4,3) ≈ [2., 2.]` | 1e-6 | Classical sanity |
| 2 | `expected_payoff(run_two_player(DOVE,HAWK), 2,4,3) ≈ [0., 4.]` | 1e-6 | Classical sanity |
| 3 | `expected_payoff(run_two_player(HAWK,DOVE), 2,4,3) ≈ [4., 0.]` | 1e-6 | Classical sanity |
| 4 | `expected_payoff(run_two_player(HAWK,HAWK), 2,4,3) ≈ [0.5, 0.5]` | 1e-6 | Classical sanity |
| 5 | `expected_payoff(run_two_player(Q, Q), 2,4,3) ≈ [2., 2.]` | 1e-6 | **Month-1 checkpoint** |
| 6 | `expected_payoff(run_two_player(HAWK,Q), 2,4,3)[0] ≤ 2.0 + 1e-6` | — | Nash property: deviating to HAWK against Q does not improve player 0's payoff |
| 7 | `expected_payoff(run_two_player(DOVE,Q), 2,4,3)[0] ≤ 2.0 + 1e-6` | — | Nash property: deviating to DOVE against Q does not improve player 0's payoff |

Test 5 passes iff `GAMMA = π/2` and J is built correctly. Tests 6–7 confirm the
Nash equilibrium property: Q is a best response to Q for both classical deviations.

---

## 10. pyproject.toml

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

[tool.ruff.lint]
select = ["E", "F", "I"]
```

---

## 11. Build Order for Phase 2 (Execute)

Files are created in this order so failures surface at the earliest possible moment:

1. `pyproject.toml` — dependency declaration
2. `src/config.py` — constants imported by everything
3. `src/circuits/__init__.py`, `src/circuits/ewl.py` — strategy gates
4. `tests/test_ewl.py` — **run pytest** — verify gates before building circuit
5. `src/game/__init__.py`, `src/game/payoffs.py` — payoff functions
6. `tests/test_payoffs.py` — **run pytest** — verify payoffs before plugging into circuit
7. `src/circuits/two_player.py` — the full EWL circuit
8. `tests/test_two_player.py` — **run pytest** — Month-1 checkpoint
9. `src/circuits/topologies.py` — stubs
10. `src/game/nash.py` — stub
11. `src/analysis/__init__.py`, `src/analysis/topology_sweep.py`, `src/analysis/noise_sweep.py` — stubs
12. `results/.gitkeep`
13. Full `pytest` suite — final verification
14. Git commit: `feat: scaffold repo and pass Month-1 two-player EWL validation`

---

## 12. Open Questions for Future Months

- **Month 2:** N-player J operator generalisation — `J_N = exp(i·γ/2 · X^⊗N)`. Matrix is `(2^N × 2^N)`. For N>~10 this becomes impractical as a dense `UnitaryGate`; may need decomposition.
- **Month 3:** `pairwise_entangler` uses `RXXGate(gamma)` which has sign `exp(-i·γ/2·X⊗X)` — opposite to J. This must be documented explicitly in `topologies.py` and reconciled in the N-player circuit builder.
- **Month 4:** `qiskit-aer==0.14.2` is already pinned; the `AerSimulator` with depolarizing noise will be added to `noise_sweep.py` without touching the core circuit or payoff layers.
