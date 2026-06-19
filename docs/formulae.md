# Formulae Reference — Multiplayer QHD (EWL Hawk–Dove)

Every formula the codebase implements, with the symbol meanings and the source
file that realizes it. Ordered along the data flow:
**strategy → entangler → circuit → outcome probabilities → payoff → Nash / advantage → strategy optimization.**

Conventions (`src/config.py`):
- `N` = number of players = number of qubits.
- `V` = resource value, `C` = conflict cost (Hawk–Dove is non-trivial when `C > V/2`).
- `γ` (GAMMA) = entanglement strength; `γ = π/2` is maximum entanglement.
- **Qubit / bit ordering** is Qiskit little-endian: in basis state index `i`,
  player `j` plays **Hawk** iff bit `j` of `i` is set, i.e. `(i >> j) & 1 == 1`; otherwise **Dove**.

---

## 1. Strategy unitary `U(θ, α, β)`

A player's move is a single-qubit SU(2) gate (`src/circuits/ewl.py`, `U`):

$$
U(\theta,\alpha,\beta)=
\begin{pmatrix}
e^{i\alpha}\cos\frac{\theta}{2} & i\,e^{i\beta}\sin\frac{\theta}{2}\\[6pt]
i\,e^{-i\beta}\sin\frac{\theta}{2} & e^{-i\alpha}\cos\frac{\theta}{2}
\end{pmatrix}
$$

A strategy is the triple `(θ, α, β)` ∈ ℝ³. Meaning of each component:

| symbol | range | name | meaning |
|---|---|---|---|
| `θ` | `[0, π]` | mixing / bit-flip angle | `cos(θ/2)` = amplitude to **stay**, `sin(θ/2)` = amplitude to **flip** Dove↔Hawk. `θ=0` keeps the cooperative basis; `θ=π` is a full flip. |
| `α` | `[−π, π]` | diagonal (stay) phase | relative phase between the \|0⟩ and \|1⟩ branches — the genuinely *quantum* dial. |
| `β` | `[−π, π]` | off-diagonal (flip) phase | phase attached to the flip branch. |

Named strategies:

$$
\text{Dove}=U(0,0,0)=I,\qquad
\text{Hawk}=U(\pi,0,0)=i\sigma_x,\qquad
Q_{\text{GHZ}}(N)=U\!\left(0,\tfrac{\pi}{N},\tfrac{\pi}{N}\right)
$$

`HAWK` carries an unobservable global phase `i` (measurement-invariant).

---

## 2. The `Q` strategy and its `π/N` scaling

`q_strategy(N) = U(0, π/N, π/N)` (`ewl.py`, `q_strategy`). It is **derived for the
GHZ entangler**: it is the phase-only gate that returns the post-entangler GHZ
state to `|0…0⟩` after `J†`. Derivation at `γ = π/2`:

$$
J_N(\pi/2)\,|0\dots0\rangle=\frac{|0\dots0\rangle+i\,|1\dots1\rangle}{\sqrt2}
$$

Applying `U(0,α,α)^{\otimes N}` multiplies the `|0…0⟩` branch by `e^{iNα}` and the
`|1…1⟩` branch by `e^{-iNα}`; choosing `Nα = π` gives both branches the common
phase `−1`, so `J_N^\dagger` recovers `|0…0⟩`. Hence

$$
\alpha=\frac{\pi}{N}\quad\Rightarrow\quad Q_N=U\!\left(0,\tfrac{\pi}{N},\tfrac{\pi}{N}\right).
$$

`N=2 → U(0,π/2,π/2)` (the classic EWL move). This collapse is GHZ-specific; on
other topologies `Q_GHZ` is generally **not** the right gate (see §7).

---

## 3. Entangling operators `J(γ)` per topology

All entanglers share the signature `(N, γ) → 2^N × 2^N` unitary and use the
sign convention `exp(+i·γ/2··)` (`src/circuits/topologies.py`).

**Two-qubit base case** (`ewl.py`, `J_matrix`):

$$
J(\gamma)=\exp\!\Big(i\tfrac{\gamma}{2}\,X\!\otimes\!X\Big)=\cos\tfrac{\gamma}{2}\,(I\otimes I)+i\sin\tfrac{\gamma}{2}\,(X\otimes X)
$$

**GHZ (global)** — single N-body term (`ghz_entangler`):

$$
J_N(\gamma)=\cos\tfrac{\gamma}{2}\,I^{\otimes N}+i\sin\tfrac{\gamma}{2}\,X^{\otimes N}
$$

`X^{⊗N}` has 1s on the anti-diagonal: `X^{⊗N}|i⟩ = |2^N-1-i⟩` (flips all bits).

**Pairwise (graph) topologies** — ring, star, fully-connected (`make_pairwise_entangler`,
`_pairwise_matrix`). For edge set `E` of the topology graph (all `XᵢXⱼ` commute, so
the product is order-independent and exact):

$$
J_G(\gamma)=\prod_{(i,j)\in E}\exp\!\Big(i\tfrac{\gamma}{2}\,X_i X_j\Big)
=\prod_{(i,j)\in E}\Big(\cos\tfrac{\gamma}{2}\,I+i\sin\tfrac{\gamma}{2}\,X_iX_j\Big)
$$

Edge sets (`src/circuits/topology_graphs.py`):
- **ring** = cycle `C_N`: `E = {(0,1),(1,2),…,(N−1,0)}`
- **star** = `K_{1,N−1}` (hub = qubit 0): `E = {(0,1),(0,2),…,(0,N−1)}`
- **fully-connected** = `K_N`: `E = {(i,j) : i<j}`, `|E| = N(N−1)/2`

All pairwise topologies reduce to `J_matrix(γ)` at `N=2` (single edge).

**W-state (global)** — reflection about the W state (`w_entangler`). With
`|W⟩ = (1/√N) Σⱼ |2^j⟩` and the Hermitian involution
`S_W = I − |0⟩⟨0| − |W⟩⟨W| + |0⟩⟨W| + |W⟩⟨0|`:

$$
J_W(\gamma)=\cos\tfrac{\gamma}{2}\,I+i\sin\tfrac{\gamma}{2}\,S_W,
\qquad
J_W(\pi/2)\,|0\dots0\rangle=\frac{|0\dots0\rangle+i\,|W\rangle}{\sqrt2}
$$

---

## 4. EWL circuit and outcome probabilities

For a profile of `N` gates `U_0,…,U_{N−1}` (`src/circuits/n_player.py`, `build_ewl_circuit`):

$$
|\psi\rangle = J^{\dagger}(\gamma)\,\big(U_0\otimes U_1\otimes\cdots\otimes U_{N-1}\big)\,J(\gamma)\,|0\dots0\rangle
$$

$$
p_i=\big|\langle i|\psi\rangle\big|^2,\qquad \sum_{i=0}^{2^N-1}p_i=1
$$

`J` is the only topology-dependent factor. Note `U=Dove=I` for all players gives
`J^\dagger J|0…0⟩ = |0…0⟩` (the all-Dove outcome) for **every** topology.

---

## 5. Hawk–Dove payoffs (Benjamin–Hayden)

For outcome index `i` with `k = popcount(i)` Hawks, the per-player payoff matrix
`P[i,j]` (`src/game/payoffs.py`, `outcome_payoff` / `_payoff_matrix`):

$$
P_{i,j}=
\begin{cases}
\dfrac{V}{N} & k=0\ \text{(all Dove)}\\[6pt]
\dfrac{V}{k} & \text{player }j\text{ is Hawk},\ 0<k<N\\[6pt]
0 & \text{player }j\text{ is Dove},\ 0<k<N\\[6pt]
\dfrac{V-C}{k}=\dfrac{V-C}{N} & k=N\ \text{(all Hawk)}
\end{cases}
$$

Expected per-player payoff from a probability vector (`expected_payoff`):

$$
\pi_j=\sum_{i} p_i\,P_{i,j}\qquad(\text{vectorized as } \pi = p\cdot P)
$$

**Total-payoff bound** (used repeatedly below). Summing over players, every
outcome contributes total `V` except all-Hawk which contributes `V−C`:

$$
\sum_j \pi_j = V - C\,p_{\text{all-Hawk}} \;\le\; V
\quad\Longrightarrow\quad
\frac{1}{N}\sum_j \pi_j \le \frac{V}{N}.
$$

---

## 6. Nash analysis and quantum advantage

Discrete pure-strategy analysis over a finite set (default `{D,H,Q}`) (`src/game/nash.py`).

**Pure Nash** (`find_pure_nash`): profile `p` is a Nash equilibrium iff no player
gains by switching, within tolerance `1e-9`:

$$
\forall i,\ \forall s\in\text{strategies}:\quad \pi_i(p)\ \ge\ \pi_i(p_{-i},s)-10^{-9}.
$$

**Quantum advantage** (`compute_advantage`): with `Q_N` the quantum strategy
(GHZ `q_strategy(N)` in fixed mode, or a topology-optimized gate otherwise),

$$
\text{advantage}=\underbrace{\overline{\pi}\big((Q_N)^{\otimes N}\big)}_{\text{quantum per-player}}
\;-\;\underbrace{\overline{\pi}(\text{best classical NE})}_{\text{classical baseline}}
$$

where `\overline{\pi}` is the mean over players and the classical baseline is the
highest-mean pure NE of the restricted `{D,H}^N` game (most conservative choice).

**Clean cooperative result.** Combining the cooperative optimum `V/N` (§7) with
the classical all-Hawk NE `(V−C)/N` gives, for vertex-transitive topologies
(GHZ, ring, fully-connected):

$$
\text{advantage}=\frac{V}{N}-\frac{V-C}{N}=\frac{C}{N}.
$$

---

## 7. Topology-specific strategy optimization

`src/game/strategy_opt.py` finds each topology's **own** optimal symmetric gate
instead of reusing `Q_GHZ`. All players play the same `(θ,α,β)`.

**Symmetric objective** (`_symmetric_payoff`):

$$
f(\theta,\alpha,\beta)=\frac{1}{N}\sum_{j}\pi_j\!\Big(\big[U(\theta,\alpha,\beta)\big]^{\otimes N};\,J_G,\gamma\Big)
$$

### (A) Cooperative strategy (`cooperative_strategy`)

$$
(\theta^\*,\alpha^\*,\beta^\*)=\arg\max_{\substack{\theta\in[0,\pi]\\ \alpha,\beta\in[-\pi,\pi]}} f(\theta,\alpha,\beta)
$$

Solved by multi-start Nelder–Mead (anchors `Q_GHZ`, Dove, Hawk + seeded random
points) with an L-BFGS-B polish (the surface is non-convex). By the §5 bound the
optimum is

$$
f^\* = \frac{V}{N}\quad\text{for every topology}
$$

(achievable because all-Dove already attains it). It is the best *payoff*, not
necessarily an equilibrium.

### (B) Nash gap and Nash strategy

**Nash gap** (`nash_gap`) — the continuous analogue of the discrete deviation
check. For candidate `s` and each player position `p`, the best unilateral
deviation and the gap:

$$
\mathrm{BR}_p(s)=\max_{s'}\ \pi_p\big(\text{others}=s,\ \text{player }p=s'\big)
$$

$$
\boxed{\ \mathrm{nashgap}(s)=\max_{p}\Big[\mathrm{BR}_p(s)-\pi_p\big(s^{\otimes N}\big)\Big]\ }
\qquad
\mathrm{nashgap}(s)\le 10^{-6}\ \Rightarrow\ s\text{ is a symmetric Nash eq.}
$$

For vertex-transitive topologies only player `0` need be checked
(`check_all_players=False`); the star checks all positions.

**Nash strategy** (`nash_strategy`) — best-response fixed point. Iterate

$$
s_{k+1}=\mathrm{BR}(s_k)\quad\text{(others held at }s_k\text{)},
$$

converged when the **induced probability vectors** match (gauge-invariant):
`‖p(s_{k+1}^{⊗N}) − p(s_k^{⊗N})‖ < 10^{-8}`. A fixed point is a symmetric Nash;
by Benjamin–Hayden one may not exist in full SU(2), which the result reports
honestly (`is_nash=False`, `converged=False`).

---

## 8. Symbol summary

| symbol | meaning |
|---|---|
| `N` | players = qubits |
| `V`, `C` | resource value, conflict cost |
| `γ` | entanglement strength (`π/2` = max) |
| `θ, α, β` | strategy gate parameters (flip angle, stay phase, flip phase) |
| `J(γ)`, `J_G(γ)` | entangler (global / topology graph `G`) |
| `p_i` | probability of measuring basis state `i` |
| `k` | number of Hawks in an outcome (`popcount(i)`) |
| `π_j` | expected payoff to player `j` |
| `f(θ,α,β)` | mean per-player payoff of the symmetric profile |
| `nashgap(s)` | max unilateral deviation gain from `s` (≤1e-6 ⇒ Nash) |

## Source files

- `src/config.py` — `V`, `C`, `GAMMA`, bit-ordering convention
- `src/circuits/ewl.py` — `U`, `J_matrix`, `q_strategy`, `DOVE`/`HAWK`/`Q`
- `src/circuits/topologies.py` — `ghz_entangler`, pairwise/`make_pairwise_entangler`, `w_entangler`
- `src/circuits/topology_graphs.py` — ring/star/fully-connected edge sets
- `src/circuits/n_player.py` — `build_ewl_circuit` (the `J† U J` sandwich)
- `src/game/payoffs.py` — Benjamin–Hayden payoff matrix, `expected_payoff`
- `src/game/nash.py` — `find_pure_nash`, `compute_advantage`
- `src/game/strategy_opt.py` — `cooperative_strategy`, `nash_strategy`, `nash_gap`
