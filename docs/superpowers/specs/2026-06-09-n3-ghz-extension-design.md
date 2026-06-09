# Month 2 Design Spec: N=3 GHZ Extension, Payoff Tensor, Nash Advantage

**Date:** 2026-06-09
**Scope:** Month 2 checkpoint — extend to N=3, confirm quantum advantage (RQ1)
**Status:** Approved

---

## 1. Goal

Extend the working 2-player EWL circuit (Month 1) to N=3 using the GHZ entangler
(J_N formula), build the 3-player payoff tensor over strategies {D, H, Q}, enumerate
all pure Nash equilibria in that discrete set, and compute the quantum advantage at
N=3. This is the first joint test of the circuit layer and the game-theory layer.

**Month 2 is met if:** the (Q,Q,Q) pure Nash equilibrium exists and the advantage
(Q-profile payoff minus best classical symmetric payoff) is strictly greater than 0.
If advantage ≤ 0 or (Q,Q,Q) is not Nash, execution stops and the finding is reported
— it is a research finding about RQ1, not a bug to paper over.

---

## 2. Design Decisions

### 2.1 GHZ Entangler: X^⊗N Formula (Option A)

The EWL J operator is a game-theoretic entangler, not a state-preparation gate.
The correct N-player generalisation is:

```
J_N(γ) = cos(γ/2) · I^⊗N + i·sin(γ/2) · X^⊗N
```

`X^⊗N` maps every basis vector |i⟩ to |2^N − 1 − i⟩ (anti-diagonal matrix).

At γ=π/2 and N=2 this yields exactly the existing `J_matrix(GAMMA)` in `ewl.py`
(same formula: `cos(γ/2)·I₄ + i·sin(γ/2)·X⊗X`), preserving Month-1 Nash results.

At γ=π/2 and N=3, `J₃|000⟩ = (|000⟩ + i|111⟩)/√2` — a GHZ-type state with
a relative phase `i` on |111⟩. This is NOT the real-valued GHZ state (|000⟩ + |111⟩)/√2;
that would be produced by the H+CNOT circuit, which is a state-preparation gate, not
the EWL J operator. Tests must assert the complex-valued form.

**Rejected alternative (Option B):** H on q0 + CNOT ladder. Creates the real-valued
GHZ state but does not reduce to `J_matrix` at N=2 (differs by relative phase i on
|11⟩). Nash property not guaranteed by the same argument. Rejected.

**Authority:** Benjamin & Hayden (2001), Flitney & Abbott (2002) use the X^⊗N formula
as the standard N-player EWL entangler.

### 2.2 Entangler Interface Contract

`build_ewl_circuit` accepts a uniform callable of signature:

```python
Entangler: TypeAlias = Callable[[int, float], npt.NDArray[np.complex128]]
#                               (N, gamma) -> 2^N × 2^N unitary matrix
```

Graph-defined topologies (ring, star, fully-connected) in Month 3 are handled by a
factory `make_pairwise_entangler(G: nx.Graph) -> Entangler` that returns a closure
of this exact signature. `n_player.py` never needs to know about NetworkX graphs.
`ghz_entangler` and `w_entangler` (Month 3) fit natively without a factory.

The closure mechanism is intentional: it is the contract mechanism that makes the
interface stable through Month 6.

### 2.3 Nash Computation: Direct Best-Response, Full Enumeration

Nashpy (already pinned at 0.0.19) is built for 2-player normal-form games.
For N=3 we use a direct best-response check over the full 3×3×3 payoff tensor.

**Scope:** pure-strategy enumeration over the discrete set {D, H, Q}. This is NOT
continuous SU(2) Nash analysis (mixed strategies over all of SU(2)); that is
explicitly future work per the README and is out of scope for all months.

A profile `p` is a pure Nash equilibrium iff for every player `i`, no unilateral
deviation raises player `i`'s payoff: `payoff(p)[i] >= payoff(p')[i]` for all `p'`
differing from `p` only in player `i`'s strategy.

Full enumeration (all 27 profiles) is used because: (a) it is the same computational
cost as a targeted check, (b) the complete pure-NE structure is needed for Month 3's
topology comparison (RQ2), and (c) it makes the paper's claim stronger — Q is
Pareto-optimal among all pure Nash equilibria, not merely "a" Nash equilibrium.

### 2.4 (Q,Q,Q) Payoff Is a Reported Result, Not a Test Assertion

The hypothesis from 2-player analogy is (Q,Q,Q) → payoff V/2 = 2.0 per player.
This is NOT tested or assumed — it is the RQ1 finding, read from `compute_advantage`
output in Phase 3. The simulation confirms or refutes it. If it differs from 2.0,
that is a research result to investigate, not a bug.

---

## 3. Files

| File | Status | Responsibility |
|---|---|---|
| `src/circuits/topologies.py` | NEW | `ghz_entangler(N, gamma)` using X^⊗N formula; `Entangler` type alias |
| `src/circuits/n_player.py` | NEW | `build_ewl_circuit(N, strategies, *, entangler, gamma)` |
| `src/circuits/two_player.py` | MODIFIED | Thin wrapper delegating to `build_ewl_circuit(2, [s0, s1])` |
| `src/circuits/ewl.py` | UNCHANGED | `J_matrix`, `make_J_gate`, `make_J_dag_gate`, strategy constants retained |
| `src/game/nash.py` | NEW | Payoff tensor construction, pure-NE enumeration, advantage computation |
| `src/game/payoffs.py` | UNCHANGED | Already handles arbitrary N; no changes |
| `src/config.py` | UNCHANGED | `GAMMA = pi/2` is the single source of truth |
| `tests/test_topologies.py` | NEW | Validates ghz_entangler correctness and N=2 equivalence |
| `tests/test_n_player.py` | NEW | Validates circuit correctness at N=2 and N=3 |
| `tests/test_two_player.py` | UNCHANGED | Must pass without modification after refactor |

---

## 4. Module Specifications

### 4.1 `src/circuits/topologies.py`

**Public API:**

```python
Entangler: TypeAlias = Callable[[int, float], npt.NDArray[np.complex128]]

def ghz_entangler(N: int, gamma: float = GAMMA) -> npt.NDArray[np.complex128]:
    """J_N(gamma) = cos(gamma/2)*I^⊗N + i*sin(gamma/2)*X^⊗N.

    Reduces to J_matrix(gamma) in ewl.py exactly for N=2.
    At gamma=pi/2, N=3: J₃|000⟩ = (|000⟩ + i|111⟩)/√2.
    """
```

**Not implemented (Month 3 stubs with NotImplementedError):**
- `w_entangler(N, gamma)` — W-state construction
- `make_pairwise_entangler(G)` — closure factory for ring/star/FC topologies

**Implementation detail:** X^⊗N is built as a (2^N × 2^N) matrix with
`anti_diag[i, 2^N - 1 - i] = 1` for all i. This is the anti-identity and equals
the N-fold tensor product of Pauli-X.

### 4.2 `src/circuits/n_player.py`

**Public API:**

```python
def build_ewl_circuit(
    N: int,
    strategies: list[StrategyParams],
    *,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
) -> npt.NDArray[np.float64]:
    """N-qubit EWL circuit: J → (U_0 ⊗ ... ⊗ U_{N-1}) → J† → statevector.

    Returns exact outcome probabilities, shape (2^N,). No sampling.
    Bit ordering: Qiskit little-endian. Matches payoffs.expected_payoff input.
    """
```

**Circuit construction:**
1. Call `entangler(N, gamma)` → J matrix (2^N × 2^N)
2. Wrap as `UnitaryGate(J, label="J")` applied to qubits `[0, ..., N-1]`
3. For each player `j`: `UnitaryGate(U(*strategies[j]))` applied to qubit `j`
4. Wrap `J.conj().T` as `UnitaryGate(Jdag, label="Jdag")` applied to `[0, ..., N-1]`
5. Return `np.asarray(Statevector(qc).probabilities(), dtype=np.float64)`

### 4.3 `src/circuits/two_player.py` (refactored)

**Public interface unchanged.** `run_two_player(s0, s1, *, gamma=GAMMA)` signature
is identical. Implementation delegates entirely to `build_ewl_circuit(2, [s0, s1], gamma=gamma)`.

The old direct Qiskit circuit construction, `make_J_gate`, and `make_J_dag_gate`
imports are removed from this file. `ewl.py` retains those functions — they are not
deleted, as they may be used directly in future analysis code.

### 4.4 `src/game/nash.py`

**Public API:**

```python
STRATEGY_NAMES: list[str] = ["D", "H", "Q"]

def build_payoff_tensor(
    N: int,
    strategy_names: list[str] = STRATEGY_NAMES,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
) -> dict[tuple[str, ...], npt.NDArray[np.float64]]:
    """Build the N-player payoff tensor over all strategy profiles.

    Pure-strategy enumeration over a discrete strategy set only.
    Continuous / mixed-strategy Nash analysis over SU(2) is future work.

    Returns: dict mapping profile tuple -> shape (N,) per-player payoffs.
    Number of entries: len(strategy_names)^N.
    """

def find_pure_nash(
    tensor: dict[tuple[str, ...], npt.NDArray[np.float64]],
    N: int,
    strategy_names: list[str] = STRATEGY_NAMES,
) -> list[tuple[str, ...]]:
    """Find all pure Nash equilibria by direct best-response check.

    A profile p is a pure NE iff for every player i and every alternative
    strategy s, payoff(p)[i] >= payoff(p_with_s_for_i)[i].
    """

def compute_advantage(
    N: int = 3,
    strategy_names: list[str] = STRATEGY_NAMES,
    V: float = DEFAULT_V,
    C: float = DEFAULT_C,
    entangler: Entangler = ghz_entangler,
    gamma: float = GAMMA,
) -> dict[str, object]:
    """Compute quantum advantage for (Q,...,Q) vs best classical symmetric profile.

    Returns dict with keys:
      q_payoff_per_player   : float — (Q,...,Q) per-player payoff (simulation result)
      best_classical_payoff : float — max per-player payoff over all-classical
                              symmetric profiles (D...D and H...H)
      advantage             : float — q_payoff - best_classical_payoff
      q_is_nash             : bool  — whether (Q,...,Q) is in find_pure_nash output
      all_pure_nash         : list[tuple] — all pure NE profiles found
      deviation_check       : dict — for each (player_i, alt_strategy), the payoff
                              from deviating vs the Q-profile payoff; confirms
                              no deviation beats q_payoff_per_player
    """
```

**Nash enumeration logic (find_pure_nash):**
For each profile p in tensor:
  For each player i in range(N):
    For each alternative strategy s in strategy_names:
      Build p' = p with p'[i] = s
      If tensor[p'][i] > tensor[p][i] + 1e-9: p is not Nash; break
  If all players pass: p is a pure NE.

**Classical symmetric profiles** for the advantage baseline: only (D,...,D) and
(H,...,H). The mixed classical symmetric profile is not evaluated (future work).
For V=4, C=3, N=3: expected (D,D,D) payoff = 4/3 ≈ 1.333, (H,H,H) = 1/3 ≈ 0.333.
Best classical = 4/3. These are expected values only — the simulation is authoritative.

---

## 5. Tests

### 5.1 `tests/test_topologies.py` (NEW)

| Test | Assertion |
|---|---|
| `test_ghz_n2_matches_j_matrix` | `assert_allclose(ghz_entangler(2, GAMMA), J_matrix(GAMMA), atol=1e-12)` |
| `test_ghz_n3_state_from_zero` | `ghz_entangler(3, GAMMA) @ e_000` ≈ `(e_000 + 1j*e_111)/sqrt(2)`, atol=1e-10 |
| `test_ghz_n2_is_unitary` | `assert_allclose(J @ J.conj().T, I_4, atol=1e-12)` |
| `test_ghz_n3_is_unitary` | `assert_allclose(J @ J.conj().T, I_8, atol=1e-12)` |

Note: `e_000` is the 8-element basis vector with 1 at index 0; `e_111` has 1 at
index 7 (Qiskit little-endian: index 7 = 0b111 = all three players Hawk).

### 5.2 `tests/test_n_player.py` (NEW)

| Test | Assertion | Rationale |
|---|---|---|
| `test_n2_qq_payoff` | `expected_payoff(build_ewl_circuit(2,[Q,Q]), 2)` ≈ `[2.0, 2.0]`, atol=1e-6 | Reproduces Month-1 checkpoint via new code path |
| `test_n3_ddd_payoff` | `expected_payoff(build_ewl_circuit(3,[D,D,D]), 3)` ≈ `[4/3, 4/3, 4/3]`, atol=1e-6 | Deterministic: D⊗³ = I⊗³, J†J = I, outcome is \|000⟩ w.p. 1; outcome_payoff(0,3,4,3) = 4/3 each. FLAG and stop if actual value disagrees — do not adjust formula to match. |

### 5.3 `tests/test_two_player.py` (UNCHANGED)

All 6 existing tests must pass without modification after the `two_player.py` refactor.
This is the primary correctness guard for the refactor.

---

## 6. Correctness Guards (Baked Into All Code)

1. `gamma` always sourced from `config.GAMMA`. No literals in any new file.
2. All probability distributions from exact `Statevector.probabilities()`. No QASM sampling.
3. (Q,Q,Q) payoff is read from simulation output in Phase 3. It is NOT asserted in any test.
4. If `test_n3_ddd_payoff` actual value ≠ 4/3: execution stops, finding is reported.
5. If Month 2 advantage ≤ 0: execution stops, finding is reported as RQ1 evidence.

---

## 7. Build Order (Phase 2)

Failures surface early by building in dependency order:

1. `topologies.py` → `test_topologies.py` (run) — validates J_N formula and N=2 equivalence
2. `n_player.py` → refactor `two_player.py` → `test_two_player.py` (run) — must stay green
3. `test_n_player.py` (run) — validates N=3 circuit wiring
4. `nash.py` → advantage script (run) — reports RQ1 finding

---

## 8. Out of Scope (Month 2)

- `w_entangler`, `make_pairwise_entangler` — Month 3 (stub with `NotImplementedError`)
- Mixed-strategy / continuous SU(2) Nash analysis — future work per README
- Depolarizing noise — Month 4
- N > 3 — Month 3 topology sweep
- IBM hardware validation — Month 5
