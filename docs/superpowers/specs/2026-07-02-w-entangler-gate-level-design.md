# T8 Design Spec: Faithful Gate-Level W Entangler

Replaces the transpiled-dense-unitary W fallback (Month-4 spec D2/1A) with an
exact gate-level circuit for `J_W(gamma) = cos(gamma/2)*I + i*sin(gamma/2)*S_W`,
so the RQ3 GHZ-vs-W noise-robustness headline no longer rests on a synthesis
artifact and the "approximate" caveat can be dropped.

Status: awaiting user review (physics decision D-T8.1 made autonomously with
the recommended option; user was AFK — revisit if disagreed).

## 1. Decisions

### D-T8.1 Physics: keep the S_W reflection semantics

`w_entangler`'s docstring flagged the gamma-interpolation semantics (the
`|0...0> <-> |W>` reflection) for physics review. **Decision: keep them.**

- All Month-3 noiseless and Month-4 noisy W results remain valid as defined;
  T8 becomes purely a circuit-fidelity upgrade of the *noisy* path.
- The reflection mirrors the GHZ Option-A construction
  (`cos*I + i*sin*involution`), so GHZ-vs-W stays apples-to-apples.
- Rejected: redefining W to a standard Hamiltonian-style interaction
  (invalidates all existing W results, breaks the GHZ analogy); keeping both
  (doubles scope for an appendix nobody asked for).

### D-T8.2 Construction: conjugation, not direct synthesis

`S_W = I - |0><0| - |W><W| + |0><W| + |W><0|` acts as Pauli-X on the 2-dim
subspace `span{|0...0>, |W>}` and as identity on its orthogonal complement.
Conjugate that subspace into a computational one:

Let `T` be any unitary with `T|e_0> = |W>` and `T|0...0> = |0...0>`
(`|e_0> = |0...01>`, excitation on qubit 0, little-endian). Then

    T * S' * T^dag = S_W,   where S' swaps |0...0> <-> |e_0>, identity elsewhere,

*regardless of what `T` does on the complement* (direct expansion of the
outer-product form). `S'` is an anti-controlled X: X on qubit 0, controlled on
qubits 1..N-1 all being |0>. Therefore, exactly:

    J_W(gamma) = exp(i*gamma/2 * S_W) = T * exp(i*gamma/2 * S') * T^dag

and `exp(i*gamma/2 * S')` splits over the control condition:

- controls satisfied (qubits 1..N-1 = 0): `cos(g/2)*I + i*sin(g/2)*X = RX(-gamma)` on qubit 0
- controls not satisfied: `e^{i*gamma/2} * I`

Factoring out the global phase `e^{i*gamma/2}`:

    exp(i*gamma/2 * S') = e^{i*gamma/2} * MCU,
    MCU = anti-controlled (ctrl_state = 0...0 on qubits 1..N-1) single-qubit
          gate U = e^{-i*gamma/2} * RX(-gamma) on qubit 0.

The `e^{-i*gamma/2}` inside `U` is a *relative* phase between the two control
branches and is required; the overall `e^{i*gamma/2}` is global and dropped
(density-matrix path is phase-invariant; tests use `Operator.equiv`).

Rejected: direct Givens-rotation synthesis of the 2-dim rotation (hand-rolls
what the transpiler does, no interpretability gain); status quo pinned
transpile (does not achieve T8).

### D-T8.3 The prep cascade T

Standard W-spreading cascade. For k = 0 .. N-2:

    CRy(theta_k)  control = qubit k,   target = qubit k+1
    CNOT          control = qubit k+1, target = qubit k

with `theta_k = 2 * arccos(1 / sqrt(N - k))`.

Properties (both required by D-T8.2, both unit-tested):

- `T|e_0> = |W>` with all-real amplitudes `+1/sqrt(N)` on every `|e_j>`,
  matching `_w_state` exactly. Amplitude left on qubit k after its block is
  `cos(theta_k/2) * prod_{m<k} sin(theta_m/2) = 1/sqrt(N)`.
- `T|0...0> = |0...0>`: every CRy is controlled on a qubit that is |0> in the
  all-zeros state, and every CNOT's control (qubit k+1) is |0> there too, so
  each gate acts as identity on |0...0>. This is what makes the conjugation
  argument exact with no correction terms.

Cost: N-1 blocks, each ~3 cx after {u, cx} transpile; T and T^dag together
~6(N-1) cx. The MCU has N-1 (negative) controls; Qiskit's decomposition at the
pinned basis/opt-level is deterministic (same pinning argument as Month-4
D3/2A). For N <= 5 this totals tens of cx vs hundreds for generic dense
5-qubit synthesis — and the count is physically interpretable: W-prep +
one collective interaction + un-prep.

## 2. Code changes

Single production file: `src/circuits/gate_level.py`.

- Add `_w_prep_cascade(N: int) -> QuantumCircuit` implementing D-T8.3.
- Rewrite `w_gate_circuit(N, gamma)` (same signature, same registry wiring):
  compose `T.inverse()`, then the MCU (build `U` as a 1-qubit circuit with
  `rx(-gamma)` and `global_phase = -gamma/2`, then
  `.to_gate().control(N-1, ctrl_state=0)` targeting qubit 0 with controls on
  qubits 1..N-1), then `T`. Remove the `UnitaryGate` + `transpile` fallback and
  the now-unused `_PINNED_BASIS` / `_PINNED_OPT_LEVEL` constants *if* nothing
  else in the module uses them; update the module docstring (W paragraph).
- **No changes** to `noise.py`, the registry, or the dense `w_entangler` (it
  stays the authoritative reference the gate circuit is tested against).
  `_transpiled_entangler` already transpiles whatever the registry returns to
  the pinned {u, cx} basis, cached per (topology, N, gamma); no Qiskit
  `Parameter` objects are involved, so parametrized-transpile issues cannot
  arise.

## 3. Tests (`tests/test_gate_level.py`)

Existing `test_gate_circuit_matches_dense` (w, N = 2..4, two gammas) becomes a
real guard instead of a tautology — it is the correctness anchor. Add:

1. **W equivalence at N=5** (the noise sweep's max N): `Operator.equiv`
   against dense `w_entangler`. `equiv` does not absorb the branch-relative
   phase, so it catches a missing `e^{-i*gamma/2}` in `U` or a wrong
   `ctrl_state`.
2. **Prep maps the excitation**: statevector of `_w_prep_cascade(N)` applied
   to `|e_0>` equals `_w_state(N)` (exact, not just up to phase — amplitudes
   must be real positive), N = 2..5.
3. **Prep fixes the vacuum**: applied to `|0...0>` returns `|0...0>` exactly,
   N = 2..5.

Success criterion for the implementation step: full test suite green,
including the untouched noise guards (`test_noise.py::test_p0_equals_statevector`
re-validates the noisy path end-to-end with the new W circuit at p=0).

## 4. Downstream updates (the point of T8)

W's gate count — hence its noise cost — changes, so **all W noise numbers
change**:

1. Re-run `experiments/noise-sweep.yaml` → new timestamped
   `results/noise-robustness/<ts>/`.
2. Re-read the RQ3 GHZ-vs-W ordering from the new run. The old conclusions
   (GHZ collapses first at N = 3, 4, 5) may move — report whatever the new
   data says; do not carry the old ordering forward.
3. Remove the "approximate" W labelling everywhere it was added under D2/1A:
   `gate_level.py` docstrings, `report.py` (column/footnotes),
   `experiments/noise-sweep.yaml` description, README Month-4 results section,
   `docs/formulae.md` if present there.
4. `TODOS.md`: delete the "Faithful gate-level W entangler" entry.
   Month-4 spec: tick T8 in Implementation Tasks; add a pointer to this spec
   next to D2.

## 5. Out of scope

- T9 (noise-aware strategy optimization) — unchanged, still blocked/deferred.
- Any change to the dense `w_entangler` or the noiseless path.
- Ancilla-assisted MCU decompositions (irrelevant at N <= 5; revisit only if
  the sweep ever extends past N ~ 8).

## 6. Failure modes

- **Wrong branch phase in U**: caught by test 1 (`equiv` is global-phase
  tolerant but branch-relative-phase strict).
- **Cascade angle/direction error**: caught by tests 2-3 independently of the
  conjugation logic, isolating prep bugs from MCU bugs.
- **Qiskit `.control(ctrl_state=0)` conventions** (which qubits are controls,
  bit ordering of ctrl_state): caught by test 1 at N >= 3 where control/target
  roles are asymmetric.
- **p=0 regression**: `test_p0_equals_statevector` pins the noisy path to the
  exact statevector result with the new circuit.
