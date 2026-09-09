# Month 4 Design Spec: Depolarizing Noise Analysis (RQ3)

**Date:** 2026-07-01
**Author:** Prithvi Raghu (circuits layer) + Aasa Singh Bhui (analysis layer)
**Scope:** Month 4 checkpoint — sweep a depolarizing-noise parameter `p`, recompute
quantum advantage per `(N, topology, p)`, extract a per-topology noise threshold
`p*`, and produce 3D advantage surfaces. Answers RQ3.
**Status:** Reviewed (`/plan-eng-review` 2026-07-01) — ready for implementation

---

## 0. Review Decisions (eng review 2026-07-01)

Eight decisions taken; sections below are amended to match.

- **D1 — noise fidelity: Option B (gate-level).** Confirmed (was author's pick).
- **D2 (1A) — W via transpiled unitary, pinned + labelled approximate.** §2.2. Pin
  the transpiler basis + optimization_level so W is reproducible; label every W
  noise result "approximate"; faithful gate-level W is a TODO, not a Month-4 gate.
- **D3 (2A) — noise basis pinned to {u, cx}; 2q depolarizing on `cx` only.** §2.3,
  §2.5. Deterministic, version-independent; "edge cost = its cx-decomposition cost."
- **D4 (3A) — `noise_p > 0` requires `strategy_mode = "fixed"`.** §4.3, §8. Config
  validation raises otherwise; noise-aware strategy optimization is deferred.
- **D5 (4A) — one registry, two views.** §3, §4.1. `topology_registry` holds both
  the matrix entangler and the gate-circuit builder per topology and owns aliases;
  `gate_level.py` only supplies builder functions. No parallel resolver.
- **D6 (5A) — guard `expected_payoff`.** §4, §6. Assert shape `(2^N,)`, clamp
  within-atol negatives to 0, assert `sum ≈ 1`. Closes the 2026-06-16 audit gap.
- **D7 (7A) — add 8 gap tests.** §5. Including the `p*` extractor, `prob_fn`
  injection, the D4 validation guard, registry parity, and the D6 guard.
- **D8 (8A) — parametrized transpiled template is required, not optional.** §4.1,
  §9. Transpile one template per `(topology, N, gamma, p)` with `U` gates as
  `Parameter`s; the sweep rebinds per profile. Makes the N=2..6 run feasible.

---

## 1. Goal

Extend the working noiseless sweep (Months 1–3) with a **realistic depolarizing
noise channel** and answer RQ3:

> Under a depolarizing channel, which entanglement topology preserves quantum
> advantage best, and does GHZ collapse faster than W as noise increases?

**Month 4 is met if:** for every topology we can compute `advantage(N, topology, p)`
across a `p` grid, identify each topology's threshold `p*` (the smallest `p` at
which advantage ≤ 0, or at which `(Q,…,Q)` stops being the best response), and
render a 3D surface (N × p × advantage) per topology. The GHZ-vs-W ordering of
`p*` is the headline RQ3 result — **reported, not assumed**. If GHZ does *not*
degrade faster than W, that is a finding about RQ3, not a bug.

---

## 2. Design Decisions

### 2.1 Noise must be applied per-gate → a gate-level circuit path is required (the central decision)

**The blocker.** Every entangler in `circuits/topologies.py` returns a *dense
`2^N × 2^N` matrix* — `ghz_entangler` (X^⊗N formula), `w_entangler` (S_W
reflection), and the pairwise ring/star/FC entanglers (`_pairwise_matrix`
collapses all per-edge factors into one matrix). `n_player.build_ewl_qc` then
applies each as a **single monolithic `UnitaryGate` spanning all N qubits**.

A Qiskit `NoiseModel` attaches errors to *gates*. A monolithic N-qubit unitary is
**one gate**, so:
- attaching noise to it cannot distinguish topologies by gate count or depth, and
- **rejected alternative (Option C):** transpiling the dense unitary to a basis
  gate set is worse than useless here — a generic `2^N` unitary synthesizes to
  ≈the same gate count for *every* topology, so all topologies would look
  identically noise-sensitive. That erases the RQ3 signal. **Rejected.**

**Decision (Option B): build a parallel gate-level circuit for the noisy path.**
The noiseless path is unchanged (exact dense-matrix statevector — fast,
regression-stable, the source of truth at `p=0`). The noisy path uses an explicit
gate sequence so 1- and 2-qubit depolarizing errors attach per physical gate, and
topology gate count differs as the physics demands (ring O(N) edges, FC O(N²)
edges, etc.).

**Rejected alternative (Option A): uniform single-qubit channel** applied once per
qubit, structure-independent. It captures GHZ-vs-W *state* fragility but not
circuit-depth cost, and contradicts README §5.1 ("single- and two-qubit
depolarizing channels"). Kept only as an optional Phase-0 spike, not the
deliverable.

### 2.2 Gate-level entangler constructions

Each gate-level entangler is a `QuantumCircuit` whose unitary equals the existing
dense matrix at every `gamma` (validated by §5 test 2, global-phase-tolerant). The
noiseless dense matrices remain the **reference** the gate circuits are checked
against — this is the correctness anchor for the whole month.

- **Pairwise (ring / star / fully-connected):** one two-qubit rotation per edge
  `(i, j)` of `topology_graph(topology, N)`.
  **Sign convention (critical):** the project uses `exp(+i·γ/2·XᵢXⱼ)`, but Qiskit
  `RXXGate(θ) = exp(−i·θ/2·XᵢXⱼ)`. Use `RXXGate(−gamma)` per edge. Edges all
  commute, so order is irrelevant. Gate count = `|E|` (ring N, star N−1, FC
  N(N−1)/2) — this is the topology-distinguishing quantity for RQ3.

- **GHZ (global X^⊗N):** `exp(i·γ/2·X^⊗N)` is a global all-X rotation. Build via
  basis change `X^⊗N = H^⊗N Z^⊗N H^⊗N`:
  `H` on all qubits → CNOT ladder (0→1→…→N−1) → `RZ(−gamma)` on the last qubit →
  CNOT ladder back → `H` on all qubits. O(N) two-qubit gates. (Exact angle/sign
  validated by §5 test 2; the dense matrix is authoritative.)

- **W (D2/1A):** the `S_W` reflection has no compact native-gate form. **Phase-1
  treatment:** transpile the dense `w_entangler` unitary to the **pinned {u, cx}
  basis at the pinned `optimization_level` (§2.5)** and attach noise to the result.
  Pinning makes W's gate count deterministic and reproducible (it is otherwise a
  transpiler artifact). Every W noise result MUST be labelled **"approximate"** in
  reports, plots, and the paper — its gate count is synthesis-derived, not a
  physical W-prep circuit, so the GHZ-vs-W headline is reported as preliminary for
  W. A faithful gate-level W entangler is **out of scope** (§8) and tracked as a
  TODO; `w_entangler`'s gamma-interpolation semantics are also flagged for physics
  review in its docstring.

`J†` is `circuit.inverse()` of the entangler circuit (negated angles), so no
separate construction is needed.

### 2.3 Noise model

A single scalar knob `p` (the README sweep parameter), applied via
`qiskit_aer.noise.NoiseModel`. **Basis pinned to {u, cx} (D3/2A)** — the circuit
is transpiled to exactly this basis at the pinned `optimization_level` (§2.5), so
the noise model is well-defined and version-independent:

- 1-qubit gates: `depolarizing_error(p, 1)` on `u` (the per-player `U` strategy
  gates and the `H`/`RZ` of the GHZ construction all reduce to `u`).
- 2-qubit gates: `depolarizing_error(min(1.0, p * p2_ratio), 2)` on **`cx` only**.
  Every entangling rotation (`RXX` per edge, the GHZ CNOT ladder) decomposes to
  `cx` in the {u, cx} basis, so **"each pairwise edge's noise cost = its cx count"**
  is explicit and deterministic. `p2_ratio` defaults to `1.0`; exposed so a later
  run can model hardware where 2-qubit gates are noisier, without an interface
  change. Not a sweep axis in v1. **Do not** attach noise to `rxx` (Aer decomposes
  it anyway, so the attached error and simulated gates would diverge — 2B rejected).

`qiskit-aer==0.14.2` is **already pinned** in `pyproject.toml` — no new
dependency.

### 2.4 `p` grid

`p ∈ {0.000, 0.005, 0.010, …, 0.050}` — 11 points, step 0.005 (README §5.1:
"0.0 to 0.05"). Configurable as a sweep axis (§4.3). `p = 0.0` is always included
and **must** reproduce the noiseless result exactly (§6 guard 1).

### 2.5 Simulation backend

`AerSimulator(method="density_matrix")`. Build the gate-level circuit, append
`save_probabilities()`, `transpile(qc, basis_gates=["u", "cx"],
optimization_level=1)` (**both pinned, D3/2A** — pinning the basis and level is
what makes the noise model and W's gate count reproducible across Qiskit
versions), run once, read `result.data(0)["probabilities"]` → shape `(2^N,)`, same
contract as `build_ewl_circuit`. No shot sampling (exact density-matrix
probabilities), so results are deterministic — consistent with the project's "no
QASM sampling" guard. See §4.1 (D8/8A): the transpile happens once per cell on a
parametrized template, not per profile.

### 2.6 Advantage and Nash under noise are recomputed, not re-derived

`expected_payoff` already consumes any `(2^N,)` probability vector, so the
game-theory layer is **unchanged**. Under noise, `(Q,…,Q)` may stop being Nash and
advantage may go negative — these are read from the noisy tensor exactly as in
Month 3. No formula changes.

---

## 3. Files

| File | Status | Responsibility |
|---|---|---|
| `src/circuits/gate_level.py` | NEW | Gate-level entangler builder functions only (D5/4A): `pairwise_gate_circuit`, `ghz_gate_circuit`, `w_gate_circuit` (transpiled-unitary fallback). No resolver — the registry owns name→builder. |
| `src/experiment/topology_registry.py` | MODIFIED | (D5/4A) `_REGISTRY` entry per topology carries BOTH the matrix entangler and the gate-circuit builder; add `resolve_gate_circuit(topology, N, gamma)` reusing `canonical()`. Single source of truth for "what topologies exist" + aliases. |
| `src/circuits/noise.py` | NEW | `build_noise_model(p, p2_ratio)`; parametrized template builder + bind-and-run (D8/8A); `build_ewl_circuit_noisy(N, strategies, *, topology, gamma, p, p2_ratio)` → probs `(2^N,)` |
| `src/circuits/n_player.py` | UNCHANGED | Noiseless path stays the `p=0` source of truth |
| `src/game/nash.py` | MODIFIED | `build_payoff_tensor` / `compute_advantage` gain optional `prob_fn` injection (see §4.2); `p=0`/`prob_fn=None` byte-identical to today |
| `src/game/payoffs.py` | MODIFIED | (D6/5A) `expected_payoff` input guard: shape, negative-clamp, normalization |
| `src/experiment/config.py` | MODIFIED | `Cell` gains `noise_p: float = 0.0`; `expand_cells` adds `noise_p` as a sweep axis |
| `src/experiment/sweep.py` | MODIFIED | `run_cell` builds a noisy `prob_fn` when `cell.noise_p > 0` and passes it to `compute_advantage` |
| `src/experiment/plots.py` | MODIFIED | 3D surface (N × p × advantage) per topology; `p*` extraction |
| `src/experiment/report.py` | MODIFIED | `noise_p` column; per-topology `p*` findings table |
| `experiments/config.yaml` | MODIFIED | Add documented `noise.p` axis (default `[0.0]` → existing behavior) |
| `experiments/noise-sweep.yaml` | NEW | Ready-to-run Month-4 config (the RQ3 run) |
| `tests/test_noise.py` | NEW | `p=0` equivalence, gate-vs-dense unitary, normalization, decay sanity, harness end-to-end |

---

## 4. Module Specifications

### 4.1 `src/circuits/noise.py`

```python
def noisy_template(
    topology: str, N: int, gamma: float, p: float, p2_ratio: float = 1.0,
) -> tuple[QuantumCircuit, list[Parameter], AerSimulator]:
    """(D8/8A) Build ONCE per cell: the transpiled, parametrized EWL circuit
    plus the configured density-matrix simulator.

    J_circuit · (U(θ_j,α_j,β_j) per player) · J_circuit† with the U-gate angles
    left as qiskit Parameters, transpiled to basis_gates=["u","cx"],
    optimization_level=1, with save_probabilities() appended. The simulator is
    AerSimulator(method="density_matrix", noise_model=build_noise_model(p,
    p2_ratio)). The entangler circuit comes from
    topology_registry.resolve_gate_circuit(topology, N, gamma); J† is its
    .inverse(). Cacheable on (topology, N, gamma, p, p2_ratio).
    """

def build_ewl_circuit_noisy(
    N: int,
    strategies: list[StrategyParams],
    *,
    topology: str,
    gamma: float = GAMMA,
    p: float,
    p2_ratio: float = 1.0,
) -> npt.NDArray[np.float64]:
    """Noisy EWL run → probs of shape (2^N,), sum ≈ 1. Bit ordering identical to
    build_ewl_circuit. Convenience wrapper: builds a noisy_template and binds
    `strategies` into it. The sweep uses noisy_template directly and rebinds per
    profile (D8) so the transpile cost is paid once per cell, not 3^N times.
    """
```

`build_noise_model(p, p2_ratio)` returns a `NoiseModel` per §2.3 (depolarizing on
`u` and `cx` only). The per-player `U` gates carry the angles as `Parameter`s so
one transpiled template serves every strategy profile in a cell.

### 4.2 `src/game/nash.py` (injection seam)

The only structural change. `build_payoff_tensor` currently hard-calls
`build_ewl_circuit` (line 83). Add an optional probability function:

```python
ProbFn: TypeAlias = Callable[[int, list[StrategyParams]], npt.NDArray[np.float64]]

def build_payoff_tensor(..., prob_fn: ProbFn | None = None) -> ...:
    run = prob_fn or (lambda n, params:
        build_ewl_circuit(n, params, entangler=entangler, gamma=gamma))
    # ... probs = run(N, params) ...
```

`compute_advantage` gains the same `prob_fn` passthrough. **`prob_fn=None` is
byte-identical to current behavior** — every Month-1..3 test and result is
preserved. The sweep layer (not nash) owns the topology→noisy-runner wiring, so
`nash.py` stays agnostic to whether a cell is noisy. This mirrors the existing
`q_params` injection pattern.

### 4.3 Harness wiring

- `Cell` gains `noise_p: float = 0.0`. `expand_cells` reads `noise.p` (scalar or
  list) and adds it to the cartesian product, exactly like `gamma`. Default
  `[0.0]` ⇒ existing configs and results are unchanged.
- **Validation (D4/3A):** `expand_cells`/`load_config` raises a clear `ValueError`
  if any cell has `noise_p > 0` and `strategy_mode != "fixed"`. Noise-aware
  strategy optimization is deferred (§8); mixing a noiseless-optimized `Q` with a
  noisy score is a silent inconsistency, so it is rejected loudly at config load.
- `run_cell`: when `cell.noise_p > 0`, build a `noisy_template` once for the cell
  (D8/8A) and construct `prob_fn = lambda n, params: <bind params into template
  and run>`, then pass it to `compute_advantage`. When `noise_p == 0`, pass
  `prob_fn=None` (exact path, byte-identical to today).

### 4.4 Plots and `p*` (`plots.py` / `report.py`)

- **3D surface:** for each topology, `matplotlib` surface over (N, p) coloured by
  mean advantage. One PNG per topology under `plots/noise/`.
- **`p*` extraction:** per `(N, topology)`, the smallest `p` where mean advantage
  ≤ 0 **or** `q_is_nash` flips to False; linearly interpolate between the two
  bracketing grid points. `None`/`>0.05` if advantage survives the whole grid.
  Rendered as a `p*` table in `report.md`, plus a GHZ-vs-W ordering statement in
  the Findings section.

---

## 5. Tests (`tests/test_noise.py`)

Original 5 (anchor + behavior):

| # | Test | Assertion |
|---|---|---|
| 1 | `test_p0_equals_statevector` | For each topology, N∈{2,3}, profiles {(D,D..),(Q,Q..),(H,D..)}: `build_ewl_circuit_noisy(..., p=0.0)` ≈ `build_ewl_circuit(...)`, atol=1e-6. **The anchor.** |
| 2 | `test_gate_circuit_matches_dense` | `Operator(resolve_gate_circuit(t,N,γ))` ≈ dense `entangler(N,γ)` up to a global phase, for ghz + each pairwise topology **and W** (D7), N∈{2,3,4}. Validates §2.2 construction and the RXX sign flip. |
| 3 | `test_probs_normalized_under_noise` | For p∈{0.01,0.05}: probs ≥ 0 and `sum ≈ 1` (atol 1e-9). |
| 4 | `test_advantage_decays_with_noise` | GHZ N=3: `advantage(p=0.05) ≤ advantage(p=0) + 1e-9` (noise does not *increase* advantage). Sanity, not a pinned value. |
| 5 | `test_noise_axis_end_to_end` | A tiny `noise.p=[0.0,0.02]`, N=2, topology=ghz sweep runs; report contains a `noise_p` column and the run does not error. |

Added gap tests (D7/7A):

| # | Test | Assertion |
|---|---|---|
| 6 | `test_pstar_extraction` | **Pure-logic, feeds the published number.** Synthetic advantage-vs-p arrays: (a) crosses 0 between grid points → correct interpolated `p*`; (b) never crosses → `None`/`>p_max`; (c) `q_is_nash` flips True→False before advantage crosses → `p*` at the flip. |
| 7 | `test_prob_fn_injection` | `compute_advantage(prob_fn=stub)` where `stub` returns a hand-built distribution → payoffs/advantage computed from the stub, proving the seam is actually used (not just the default path). |
| 8 | `test_registry_parity` | For every name in `KNOWN_TOPOLOGIES`: `resolve(name,N)` and `resolve_gate_circuit(name,N,γ)` both succeed; aliases (`full`,`complete`,`fully_connected`) resolve in both. Locks D5 against drift. |
| 9 | `test_noise_p_sweep_axis` | `noise.p=[0.0,0.01,0.02]` expands to 3× the cells; scalar `noise.p` → 1×. Backward-compat: a config with no `noise` key expands identically to before. |
| 10 | `test_noise_requires_fixed_mode` | (D4) `load_config`/`expand_cells` with `noise.p=[0.02]` and `strategy_mode="nash"` raises `ValueError`; with `strategy_mode="fixed"` it does not. |
| 11 | `test_expected_payoff_guard` | (D6) wrong-shape probs → raises; `sum≠1` beyond atol → raises; a tiny negative within atol → clamped, payoff finite. |
| 12 | `test_build_noise_model` | `build_noise_model(0.0,…)` adds no error (or identity-equivalent); `build_noise_model(0.05,…)` attaches depolarizing to `u` and `cx` and to nothing else. |
| 13 | `test_noisy_invalid_p` | `build_ewl_circuit_noisy(..., p=-0.1)` and `p=1.5` raise a clear error (not a silent bad result). |

Keep N small; density-matrix sims are heavier than statevector. Tests 6–11 are
the correctness-critical set (published number, the new seam, the new validation,
the new guard); 12–13 are cheap parity/smoke.

---

## 6. Correctness Guards

1. **`p=0` ≡ noiseless.** The noisy path at `p=0` reproduces `build_ewl_circuit`
   to 1e-6 (test 1); the analysis layer at `prob_fn=None` is byte-identical.
2. **Gate circuits validated against dense matrices** (test 2) — the dense
   entanglers stay authoritative; the gate-level forms must match them.
3. `gamma` always from `config.GAMMA`; `V`, `C` from `config`. No literals.
4. Probabilities from density-matrix `save_probabilities()`. **`expected_payoff`
   guards its input (D6/5A):** asserts shape `(2^N,)`, clamps within-atol negatives
   to 0, asserts `sum ≈ 1` (atol 1e-9) — so any producer that violates the contract
   fails loudly instead of silently corrupting payoffs. No shot sampling.
5. The GHZ-vs-W `p*` ordering and any negative advantage are **reported findings**,
   never asserted to a specific value and never "fixed" to match a hypothesis.
6. W's noisy result is labelled approximate (§2.2) everywhere it is reported.

---

## 7. Build Order

1. `gate_level.py` → test 2 (gate-vs-dense). Validate constructions + RXX sign
   **before** any noise — failures surface at the cheapest point.
2. `noise.py` (`build_noise_model`, `build_ewl_circuit_noisy`) → tests 1, 3.
   The `p=0` anchor must pass before going further.
3. `nash.py` `prob_fn` injection → re-run full existing suite (must stay green) +
   test 4.
4. Harness: `Cell.noise_p`, `expand_cells`, `run_cell` wiring → test 5.
5. `plots.py` 3D surface + `report.py` `p*` table → visual check on a small run.
6. `experiments/noise-sweep.yaml`; run the RQ3 sweep; write `results/...`.
7. Docs: `formulae.md` (channel definition + gate constructions); flip README §9
   "Noise robustness surface" to Complete with measured `p*` numbers.

---

## 8. Out of Scope (Month 4)

- **Faithful gate-level W entangler** — Phase-1 uses the transpiled-unitary
  approximation with a documented caveat. A native W construction is future work.
- Real-backend calibration noise, coherent errors, amplitude-damping/thermal
  relaxation (T1/T2), and readout/measurement error. (Readout error is a cheap
  later add if a reviewer asks.)
- A `p2_ratio` sweep axis — single `p` knob in v1; ratio fixed at 1.0.
- **Noise-aware strategy optimization (D4/3A)** — `strategy_mode` cooperative/nash
  under noise. Deferred because it would run the per-cell optimizer on
  density-matrix sims (expensive) and needs its own design. Month 4 noise runs are
  `strategy_mode="fixed"` only, enforced by config validation.
- Mixed-strategy / continuous-SU(2) Nash under noise — still future work.
- IBM hardware runs — Month 5.

---

## 9. Performance Note

Density-matrix simulation is heavier than statevector, and `build_payoff_tensor`
evaluates all `|strategies|^N` profiles per cell (729 at N=6 with {D,H,Q}). With
an 11-point `p` grid × 5 topologies × N=2..6 this is a large run. Mitigations,
in order:
- Default the Month-4 config to the **comparison set that answers RQ3** — GHZ, W,
  ring — at N=2..5 first; run full {5 topologies × N=6} as a separate long job.
- **REQUIRED (D8/8A): the parametrized transpiled template (§4.1).** The entangler
  sub-circuit and gate structure are fixed per cell; only the per-player `U` angles
  change between the 3^N profiles. Transpile ONE template per `(topology, N, gamma,
  p)` with the `U` angles as `Parameter`s, then `assign_parameters` per profile —
  not `transpile` 3^N times. This is the difference between a feasible run and an
  hours-long one at N=5/6, so it is part of the design, not an optional pass.
- Reuse the existing `cpu_limit.py` cap and per-cell isolation in `run_sweep`;
  cells are independent and parallelizable.

The template reuse (first bullet) is required for the run to finish in reasonable
time; the rest are optimizations that correctness (sections 2–6) does not depend on.

---

## What already exists (reused, not rebuilt)

- `game/payoffs.expected_payoff` — consumes any `(2^N,)` prob vector unchanged.
- `nash.compute_advantage` — `q_params` injection pattern reused for `prob_fn`.
- `experiment` harness — "any list is a sweep axis" reused for `noise.p`.
- `circuits/topology_graphs.topology_graph` — edge sets reused for per-edge RXX.
- Dense entanglers in `circuits/topologies` — kept as the noiseless reference the
  gate-level circuits are validated against.
- `cpu_limit.py`, per-cell isolation in `run_sweep` — reused for the heavier sims.

## Failure modes (new codepaths)

| Codepath | Realistic failure | Test? | Handled? | Silent? |
|---|---|---|---|---|
| `build_ewl_circuit_noisy` | invalid `p` (<0,>1) | test 13 | raises | no |
| gate-level entangler | wrong RXX sign / GHZ angle | test 2 (vs dense) | n/a | no |
| `expected_payoff` | non-normalized noisy probs | test 11 | guard raises (D6) | no |
| `p*` extraction | off-by-one-grid interpolation | test 6 | n/a | **would be silent → test is the only guard** |
| registry | new topology added to one view only | test 8 | parity test | no |
| config | noise + non-fixed strategy | test 10 | validation raises (D4) | no |

No critical gaps (a failure that is untested AND unhandled AND silent): the only
silent path, `p*` extraction, is closed by test 6.

## NOT in scope (deferred, with rationale)

Spec §8 is authoritative. Summary: faithful gate-level W (research-grade),
noise-aware strategy optimization (expensive + needs own design), `p2_ratio` sweep
axis, mixed-strategy/SU(2) Nash under noise, IBM hardware (Month 5).

## Worktree parallelization

Two independent lanes after a shared foundation:

- **Lane 0 (foundation, sequential):** `gate_level.py` + `topology_registry`
  (D5) + `noise.py` (D8) → tests 1,2,8,12,13. Everything depends on this.
- **Lane A (analysis):** `nash.py` `prob_fn` + `payoffs.py` guard (D6) → tests 7,11.
- **Lane B (harness):** `config.py` (noise axis + D4 validation) + `sweep.py` +
  `plots.py` `p*` + `report.py` → tests 5,6,9,10.

Lanes A and B touch disjoint modules (`game/` vs `experiment/`) → parallel after
Lane 0 merges. Then integrate + run `experiments/noise-sweep.yaml`.

## Implementation Tasks

Synthesized from this review. P1 blocks the milestone; P2 same-branch; P3 follow-up.

- [x] **T1 (P1, CC: ~20min)** — pre-reqs — fix the cp1252 UTF-8 write bug + add `pyyaml` to `pyproject.toml`
  - Surfaced by: prior session — every report write crashes on Windows
  - Files: `src/experiment/topology_viz.py`, `src/experiment/report.py`, `pyproject.toml`
  - Verify: a noise sweep writes its report without `UnicodeEncodeError`
- [x] **T2 (P1, CC: ~30min)** — `gate_level.py` + registry (D5) — gate-level builders, dual-view registry
  - Verify: test 2 (gate vs dense, all 5 topologies) + test 8 (parity) pass
- [x] **T3 (P1, CC: ~30min)** — `noise.py` (D3 basis, D8 template) — noise model + parametrized template + runner
  - Verify: test 1 (p=0 anchor) + test 12 + test 13 pass
- [x] **T4 (P1, CC: ~15min)** — `nash.py` `prob_fn` + `payoffs.py` guard (D6)
  - Verify: full existing suite green (regression) + tests 7, 11
- [x] **T5 (P1, CC: ~20min)** — harness: `config` noise axis + D4 validation, `sweep` wiring
  - Verify: tests 5, 9, 10
- [x] **T6 (P1, CC: ~20min)** — `plots.py` p* extraction + 3D surface, `report.py` column
  - Verify: test 6 (the published-number guard)
- [x] **T7 (P2, CC: ~10min)** — `experiments/noise-sweep.yaml` + run + write `results/`, flip README §9
  - Done 2026-07-02: `results/noise-robustness/2026-07-02T1212Z/` (132/132 cells, 0 errors)
- [x] **T8 (P3)** — faithful gate-level W entangler (D2) — done, see
  `2026-07-02-w-entangler-gate-level-design.md`; the D2 "approximate" labelling
  is retired.
- [ ] **T9 (P3)** — TODO: noise-aware strategy optimization (D4)

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | 0 | — | not run |
| Automated second-opinion review | unavailable | Independent review | 0 | — | tool unavailable |
| Eng Review | `/plan-eng-review` | Architecture & tests (required) | 1 | CLEAR | 8 issues raised, 8 resolved, 0 critical gaps |
| Design Review | `/plan-design-review` | UI/UX gaps | 0 | — | n/a (no UI) |
| DX Review | `/plan-devex-review` | Developer experience gaps | 0 | — | n/a |

- **UNRESOLVED:** 0 — every issue (D1–D8) was decided.
- **OUTSIDE VOICE:** skipped because the review tool was unavailable; the fallback was not run for this focused specification.
- **VERDICT:** ENG CLEARED — ready to implement. Start with T1 (pre-reqs) so the first noise run doesn't crash on Windows.
