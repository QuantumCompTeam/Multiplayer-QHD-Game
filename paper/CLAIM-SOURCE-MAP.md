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

## Evidence labels

- **Proposition:** proved in the main manuscript and covered by an executable regression check.
- **Computational result:** evaluated over a stated finite parameter range; not presented as a theorem.
- **Simulation result:** produced by the statevector or density-matrix pipeline.
- **Registered hardware result:** acceptance rule written before the execution.
- **Observational hardware result:** measured after execution without a preregistered pass rule.
- **Exploratory result:** provisional analysis that does not support a central claim.

### Label status convention

Every label in the tables below is a **proposal**, not a settled classification,
until the user confirms it at Gate G3. The distinction matters most for
**Proposition**: by the definition above it requires a proof in the main
manuscript *and* an executable regression check. No Section III derivation has
been drafted yet, so at present each proposed Proposition rests on its
regression check alone. A row is promoted from proposed to confirmed only when
(a) the derivation exists in `paper/qhd.tex` and (b) the user approves the label
at G3; a row whose derivation does not materialise is demoted to **Computational
result** over its stated finite range.

## Section III-A / III-B evidence (labels proposed, pending Gate G3)

| Section | Claim | Proposed evidence label | Test |
|---|---|---|---|
| III-B (Classical Equilibrium and Welfare Geometry) | At $V{=}4,\ C{=}3$, Hawk strictly dominates Dove for every $N$ against every fixed count of Hawk opponents | Proposition | `tests/test_paper_claims.py::test_hawk_strictly_dominates_dove_for_live_parameters` |
| III-A (Notation and the Classical $N$-Player Payoff Tensor) | Per-player payoff for every basis outcome matches the piecewise payoff tensor, Eq. (2) of `paper/qhd.tex`, exhaustively for $N=2,\ldots,7$ | Proposition | `tests/test_paper_claims.py::test_payoff_tensor_matches_piecewise_formula_exhaustively` |
| III-B (Classical Equilibrium and Welfare Geometry) | Total welfare is $V$ for every outcome except all-Hawk, where it is $V-C$ — stated and proved as `Proposition 1 (Outcome-level welfare)`, Eq. (3) of `paper/qhd.tex` | Proposition (proof in manuscript) | `tests/test_paper_claims.py::test_total_welfare_identity_for_every_basis_state` |
| III-B (Classical Equilibrium and Welfare Geometry) | Expected mean payoff depends only on the all-Hawk outcome probability, $\bar\pi = V/N - (C/N)p(1^N)$, Eq. (4) of `paper/qhd.tex` | Proposition (derived in manuscript) | `tests/test_paper_claims.py::test_expected_mean_depends_only_on_all_hawk_probability` |

**Gate G3 outcome (2026-08-01).** The user approved the labels as written. The
III-A and III-B rows above are now **confirmed**, not proposed: III-B carries
`Proposition 1 (Outcome-level welfare)` with its proof in `paper/qhd.tex`, and
III-A's payoff-tensor row is definitional plus exhaustively checked. The
III-F cooperative-invariance row is confirmed at Task 12 because its proof now
appears in `paper/qhd.tex` and its executable regressions pass. The remaining
III-G/I/J Proposition classifications stay contingent on their manuscript
derivations.

**Subsection naming.** These rows were written at Task 5 against the manuscript's
pre-rewrite subsection titles. Task 7 renamed the first subsection of
`\label{sec:model}` to "Notation and the Classical $N$-Player Payoff Tensor",
which is the spec's III-A, and the equilibrium/welfare claims belong to the
III-B that Task 8 will write. The section column above now uses the target
names, so the payoff-tensor row sits under III-A and the three
dominance/welfare rows under III-B.

**Source-scope constraint carried into III-A (from `paper/LITERATURE-AUDIT.md`).**
`benjamin2001` is verified only for the multiplayer quantum-game construction
with worked $N=3$ and $N=4$ cases; the audit records that no fully general
closed-form $2^N$ payoff-tensor formula appears in that paper. III-A therefore
credits Benjamin and Hayden for the $N$-player extension route and presents the
general closed form as this paper's own statement, rather than repeating the
pre-rewrite phrase "the payoff generalises as a Benjamin--Hayden tensor". The
same audit restricts `maynardsmith1973` (abstract-only) to the two-strategy
value-and-cost structure — never an equilibrium value, because its mixed ESS
needs $C>V$ and this paper runs $V>C$ — and restricts `broom1997`
(abstract-only) to "a general $N$-player symmetric matrix-game framework
exists". III-A cites both within exactly those limits.

## Section III-C evidence (drafted at Task 9)

| Section | Claim | Evidence label | Test |
|---|---|---|---|
| III-C (Quantum Strategies and the EWL Protocol) | The printed strategy matrix $U(\theta,\alpha,\beta)$, Eq. (5) of `paper/qhd.tex`, is the unitary the implementation applies | Computational result (200 random parameter triples) | `tests/test_paper_claims.py::test_strategy_unitary_matches_manuscript_matrix` |
| III-C (Quantum Strategies and the EWL Protocol) | $D=U(0,0,0)$ is the identity and $H=U(\pi,0,0)=i\sigma_x$ exactly, the leading $i$ being an unobservable global phase | Proposition (exact matrix identities) | `tests/test_paper_claims.py::test_named_strategies_match_manuscript_definitions` |
| III-C (Quantum Strategies and the EWL Protocol) | $Q_N=U(0,\pi/N,\pi/N)=\mathrm{diag}(e^{i\pi/N},e^{-i\pi/N})$ for $N=2,\ldots,8$, so the two-player $Q$ is the $N=2$ case rather than a universal strategy | Proposition (exact matrix identity) | `tests/test_paper_claims.py::test_q_strategy_is_the_pi_over_n_phase_gate` |
| III-C (Quantum Strategies and the EWL Protocol) | $J_T(0)=I$ for every entangler family, so $\gamma=0$ returns the classical game exactly | Computational result (five families, $N=3,4,5$) | `tests/test_paper_claims.py::test_entangler_reduces_to_identity_at_zero_angle` |

**Attribution correction applied at Task 9.** The pre-rewrite III-C read "with
maximal entanglement at $\gamma=\pi/2$~\cite{benjamin2001,chappell2012}".
`paper/LITERATURE-AUDIT.md` records that no $\gamma$ symbol and no $\pi/2$ value
appears anywhere in `benjamin2001` (it uses a fixed maximal entangler, not a
continuously parameterized one). The angle parameterization is therefore
attributed to `chappell2012` alone, with the symbol translation stated in the
text because that source names the same angle $\theta$. This is the third
misattribution inherited from the old manuscript and corrected against the
audit, after `nation2021` and the "Benjamin--Hayden tensor".

## Section III-D evidence (drafted at Task 10)

| Section | Claim | Evidence label | Test |
|---|---|---|---|
| III-D (Entangler Families and Graph Symmetry) | $J_{\mathrm{GHZ}}(\gamma)=\cos(\gamma/2)I^{\otimes N}+i\sin(\gamma/2)X^{\otimes N}$, Eq. (9) of `paper/qhd.tex`, is the operator the implementation applies | Computational result (exact matrix identity, $N=2,\ldots,6$, five $\gamma$ values) | `tests/test_paper_claims.py::test_ghz_entangler_matches_manuscript_formula` |
| III-D | $J_G(\gamma)=\prod_{(r,s)\in E(G)}\exp(i\tfrac{\gamma}{2}X_rX_s)$, Eq. (10), with the $+i$ sign convention; the $-i$ convention is checked to disagree | Computational result (matrix exponential taken independently of the implementation's closed form; ring/star/complete, $N=3,4,5$) | `tests/test_paper_claims.py::test_graph_entangler_is_the_product_of_per_edge_exponentials` |
| III-D | The printed edge sets and, for $N\ge3$, the counts $m_{C_N}=N$, $m_{S_N}=N-1$, $m_{K_N}=N(N-1)/2$; at $N=2$, $C_2$ is the single-edge degeneracy with $m_{C_2}=1$; hub at qubit $0$ (manuscript player $1$); GHZ and W carry no edge set | Computational result (exact set equality, $N=3,\ldots,7$, plus the manuscript/implementation $N=2$ cycle guard) | `tests/test_paper_claims.py::test_graph_topology_edge_sets_match_manuscript`; `tests/test_paper_claims.py::test_manuscript_scopes_cycle_edge_count_at_n2` |
| III-D | $S_W$ of Eq. (11) is a Hermitian involution and $J_W(\gamma)=\cos(\gamma/2)I^{\otimes N}+i\sin(\gamma/2)S_W=\exp(i\gamma S_W/2)$, Eq. (12) | Computational result (exact matrix identity, $N=2,\ldots,6$, five $\gamma$ values) | `tests/test_paper_claims.py::test_w_entangler_matches_manuscript_involution` |
| III-D | $R_\sigma J_G(\gamma)R_\sigma^{\dagger}=J_{\sigma(G)}(\gamma)$, Eq. (14), for **every** permutation, not only automorphisms — this reaches the star hub relocation that the leaf-SWAP check cannot | Proposition (all $\sigma\in S_N$; ring/star/complete, $N=3,4,5$) | `tests/test_paper_claims.py::test_graph_entangler_permutation_covariance` |
| III-D | $R_\sigma J_{\mathrm{GHZ}}R_\sigma^{\dagger}=J_{\mathrm{GHZ}}$ and $R_\sigma J_WR_\sigma^{\dagger}=J_W$ for all $\sigma$: the global families are invariant under the full symmetric group | Proposition (all $\sigma\in S_N$, $N=3,4,5$) | `tests/test_paper_claims.py::test_global_entanglers_are_invariant_under_every_permutation` |
| III-D | `Proposition 2 (Relabeling covariance of payoffs)`, Eq. (15): $\sum_xp_{\sigma(G)}(x)P_{\sigma(j)}(x)=\sum_xp_G(x)P_j(x)$ under a symmetric profile, hence equal expected payoffs within an automorphism orbit | Proposition (proof in manuscript; all $\sigma\in S_N$, ring/star/complete, $N=3,4,5$, $\gamma=\pi/2$, $V{=}4,C{=}3$) | `tests/test_paper_claims.py::test_payoff_vector_relabeling_covariance` |

**Reused, not duplicated, at Task 10.** Unitarity of every family and the
$C_3=K_3$ identity are already covered and are referenced rather than
re-implemented: `tests/test_topologies.py::test_pairwise_unitary`,
`tests/test_topologies.py::test_ghz_n2_is_unitary`,
`tests/test_topologies.py::test_ghz_n3_is_unitary`,
`tests/test_topologies.py::test_w_unitary`,
`tests/test_topologies.py::test_ring_equals_fully_connected_n3`, and
`tests/test_topologies.py::test_pairwise_n2_matches_j_matrix` (the $N=2$
single-edge degeneracy III-D states). $J_T(0)=I$ for all five families is
covered by `tests/test_paper_claims.py::test_entangler_reduces_to_identity_at_zero_angle`
from Task 9. The star leaf-orbit consequences are covered by
`tests/test_paper_claims.py::test_star_payoff_vector_respects_leaf_orbit`,
`tests/test_paper_claims.py::test_star_entangler_invariant_under_leaf_swap`, and
`tests/test_asymmetric_advantage.py::test_star_leaves_share_one_advantage`.

**GAP — the normalized interaction-strength convention is a definition, not an
implementation.** III-D defines
$J^{\mathrm{n}}_G(\gamma)=\prod_{(r,s)\in E(G)}\exp(i\tfrac{\gamma}{2m_G}X_rX_s)$
as Eq. (13). No such normalization exists anywhere in `src/`: every family is
called at the same raw `gamma` by `src/circuits/topologies.py`,
`src/circuits/gate_level.py`, and `src/experiment/topology_registry.py`, with no
per-edge or per-family scaling (verified 2026-08-01 by direct inspection and by
a repository-wide grep for `normali[sz]`, `per-edge`, `/ len(edges)`, and
`number_of_edges`, which returns only unrelated hits in
`src/experiment/config.py`, `src/experiment/topology_registry.py`, and
`src/game/payoffs.py`). Consequently **every reported entangler-family comparison is computed
under the unnormalized equal-$\gamma$ setting**, and the manuscript says so
explicitly. The sensitivity control that Eq. (13) is defined for has not been
run; Section V must not be written as though it had been. Closing this gap
requires (a) a normalized entangler in `src/circuits/topologies.py`, (b) a sweep
under it, and (c) a Section V paragraph reporting the comparison. Until then,
any star-versus-complete family difference reported at equal raw $\gamma$
confounds correlation structure with coupling budget, and the manuscript states
that limitation rather than hiding it.

**Star hub-choice limitation, partially lifted at Task 10.** The Task 6 note
below records that `star_entangler(N, gamma)` exposes no hub-selection parameter,
so the hub-relocation half of the operator-level covariance check could not be
built from that constructor alone.
`tests/test_paper_claims.py::test_graph_entangler_permutation_covariance` lifts
this by going through `make_pairwise_entangler` on an explicitly relabelled
`networkx` graph, which does construct "the star with the relocated hub" and
verifies $R_\sigma J_{S_N}R_\sigma^{\dagger}=J_{\sigma(S_N)}$ for every $\sigma$.
The limitation on `star_entangler` itself is unchanged: it still hard-codes
hub $=$ qubit $0$.

## Section III-E metric contracts (definitions, not experimental results)

The rows below register the meanings consumed by Sections IV--VII. They are
manuscript definitions and reporting contracts, not simulation or hardware
results, and therefore carry no result-level evidence label.

| Metric or test | Definitional contract | Contract check |
|---|---|---|
| expected payoff and payoff vector | $\pi_j(\boldsymbol U;T)=\sum_xp_T(x\mid\boldsymbol U)P_j(x)$ and $\boldsymbol\pi=(\pi_1,\ldots,\pi_N)$; the vector is primary evidence | `tests/test_paper_structure.py::test_section_iii_e_defines_expected_payoff_and_primary_vector` |
| restricted-menu equilibrium | $g_j(a)=\pi_j(Q_N^{\otimes N})-\pi_j(a,Q_{N,-j})$ for $a\in\{D,H\}$; pass iff $g_j(a)\geq0$ for both deviations and every player | `tests/test_paper_structure.py::test_section_iii_e_requires_both_deviations_for_every_player` |
| analytic-baseline advantage | $\Delta_{\mathrm{ana}}(\boldsymbol U;T)=\bar\pi(\boldsymbol U;T)-(V-C)/N$ | `tests/test_paper_structure.py::test_section_iii_e_keeps_advantage_metrics_distinct` |
| circuit-relative payoff gap | fixed-profile mean payoff minus the highest-mean pure restricted $\{D,H\}^N$ circuit equilibrium under the same entangler family and, where applicable, the same implementation and noise path | `tests/test_paper_structure.py::test_section_iii_e_keeps_advantage_metrics_distinct` |
| all-zero target-state population | $P(0^N)=p_T(0^N\mid\boldsymbol U)$; one basis-state population, explicitly not state fidelity | `tests/test_paper_structure.py::test_section_iii_e_defines_all_zero_population_as_not_fidelity` |
| fairness range and player floor | $S_\pi=\max_j\pi_j-\min_j\pi_j$ and $F_\pi=\min_j\pi_j$; neither scalar replaces $\boldsymbol\pi$ | `tests/test_paper_structure.py::test_section_iii_e_defines_vector_first_fairness_summaries` |

The interaction-strength normalization of Eq. (13) remains only a definition:
it is still unimplemented and its sensitivity control remains unrun. No III-E
metric contract changes that limitation.

## Section III-F evidence (drafted at Task 12)

| Section | Claim | Evidence label | Test |
|---|---|---|---|
| III-F (GHZ Cooperative Benchmark) | For the GHZ profile $Q_N^{\otimes N}$, `Proposition 3 (Cooperative invariance in the entanglement angle)` proves for every $\gamma$ that $J_{\mathrm{GHZ}}^\dagger Q_N^{\otimes N}J_{\mathrm{GHZ}}\lvert0^N\rangle=-\lvert0^N\rangle$, because both GHZ branches acquire the same $N$-fold phase $-1$. Hence $p(0^N)=1$, $\pi_j=V/N$, and $\Delta_{\mathrm{ana}}=C/N$; at $V{=}4,C{=}3$ and $\gamma=\pi/2$, $\pi_j=4/N$ and $\Delta_{\mathrm{ana}}=3/N$. | Proposition (analytic proof in manuscript; finite-grid numerical regressions are corroborating evidence) | Manuscript contract: `tests/test_paper_claims.py::test_ghz_cooperative_benchmark_manuscript_contract`. Numerical regressions: `tests/test_paper_claims.py::test_ghz_cooperative_output_invariant_in_gamma` ($N=2,\ldots,7$, $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$); `tests/test_paper_claims.py::test_ghz_q_profile_returns_all_dove` ($N=2,\ldots,8$, $\gamma=\pi/2$); `tests/test_paper_claims.py::test_ghz_q_profile_payoff_and_analytic_advantage` ($N=2,\ldots,8$, $V{=}4,C{=}3$). |

The universal quantifier over $\gamma$ is established by the analytic phase-cancellation proof, not inferred from the finite grid. The numerical tests independently regress the implementation over their exact ranges and do not replace the proof.

## Section III-G / III-I / III-J evidence (remaining derivations pending)

The evidence labels below retain the Gate G3 classification decisions, but a
Proposition label is earned only when the corresponding main-text derivation
exists. Task 12 does not promote any deviation, equilibrium-boundary, or
fairness claim.

| Section | Claim | Evidence label | Test |
|---|---|---|---|
| III-G (Hawk deviation, maximal entanglement) | Closed form $\pi_{\text{dev}} = 4\cos^2(\pi/N)$ for a lone Hawk deviation against $(Q_N,\ldots,Q_N)$ at $\gamma=\pi/2$, $N=2,\ldots,8$, $V{=}4,\ C{=}3$ | Computational result today; Proposition proposed but contingent — see the note below | `tests/test_paper_claims.py::test_hawk_deviation_matches_closed_form_at_maximal_entanglement` |
| III-G (Dove deviation) | A lone Dove deviation never exceeds $V/N$, checked across $N=2,\ldots,7$ and $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$ (non-bindingness does not follow automatically from the $\gamma=\pi/2$ analytic case) | Computational result | `tests/test_paper_claims.py::test_dove_deviation_is_non_binding` |
| III-G (Restricted-menu equilibrium boundary) | $(Q_N,\ldots,Q_N)$ is a restricted-menu Nash equilibrium at $N=2,3$ and not at $N=4,5$ under the GHZ entangler, $V{=}4,\ C{=}3$ | Proposition | Reused, not duplicated — see `tests/test_ne_guard.py::test_registered_values_reproduce`, `tests/test_ne_guard.py::test_candidate_identities`, `tests/test_ne_guard.py::test_boundary_inequality_agreement`, `tests/test_ne_guard.py::test_g9_hawk_breaks_q_at_n4_n5` |
| III-I (Star-orbit payoff covariance) | Under the star topology's leaf-permutation automorphism (hub = qubit 0), the two leaf payoffs coincide at $N=3$ under the symmetric $Q_3$ profile; the hub is not asserted equal to the leaves | Proposition | `tests/test_paper_claims.py::test_star_payoff_vector_respects_leaf_orbit` |
| III-I (Star-orbit operator-level covariance) | Conjugating the star entangler unitary ($N{=}4,\ \gamma=\pi/2$) by the SWAP of the two non-hub leaf qubits (1,2) leaves the operator invariant | Proposition | `tests/test_paper_claims.py::test_star_entangler_invariant_under_leaf_swap` |
| III-I (Star-orbit, per-player asymmetry) | Star leaves share one advantage value, checked at $N=3,4,5$ | Proposition (follows from the leaf-permutation automorphism) | Reused, not duplicated — `tests/test_asymmetric_advantage.py::test_star_leaves_share_one_advantage` |
| III-I (Star-orbit, per-player asymmetry) | The star is genuinely non-uniform (hub $\neq$ leaves), checked at $N=4,5$ only | Computational result | Reused, not duplicated — `tests/test_asymmetric_advantage.py::test_star_is_asymmetric_for_n_ge_4` |
| III-I (Star-orbit, per-player asymmetry) | Scalar advantage is the mean of the per-player advantage vector, and $q = \text{classical} + \text{advantage}$ per player, checked at $N=3,4,5$ | Proposition (definitional identity in `compute_advantage`) | Reused, not duplicated — `tests/test_asymmetric_advantage.py::test_star_scalar_is_mean_and_vectors_consistent` |
| III-I (Star-orbit, per-player asymmetry) | The pinned star $N{=}4$ per-player advantage split is $[0,1,1,1]$ with scalar mean $0.75$ | Computational result (single pinned point) | Reused, not duplicated — `tests/test_asymmetric_advantage.py::test_star_n4_known_per_player_split` |
| III-J (Single unilateral-deviation welfare invariance) | Total welfare of a lone Hawk deviation from all-Dove equals the all-Dove total welfare $V$, for every deviating player and $N=2,\ldots,8$, $V{=}4,\ C{=}3$ | Proposition | `tests/test_paper_claims.py::test_single_bit_flip_preserves_total_welfare` |

**Note — the Hawk-deviation closed form is not yet proven in this repository.**
`tests/test_paper_claims.py::test_hawk_deviation_matches_closed_form_at_maximal_entanglement`
verifies $\pi_{\text{dev}} = 4\cos^2(\pi/N)$ numerically for $N=2,\ldots,8$. The
same quantity appears in `tests/test_ne_guard.py::test_candidate_identities` in
the algebraically identical form $2+2\cos(2\pi/N)$, and the docstring of
`tests/test_ne_guard.py::test_boundary_inequality_agreement` describes that
identity as holding "as computed, not proven". Numerical agreement across a
finite $N$ grid is therefore the only evidence that exists today. This row may
be promoted to Proposition only if Section III-G supplies the derivation;
otherwise it stays a computational result over $N=2,\ldots,8$ and the
manuscript must not call it a proposition. Task 12 supplies only the cooperative
invariance proof and does not change this status.

**Limitation — star hub-choice not exposed.** `star_entangler(N, gamma)` (`src/circuits/topologies.py`) hard-codes hub = qubit 0 via `nx.star_graph(N-1)` in `src/circuits/topology_graphs.py` and takes no hub-selection parameter. The operator-level covariance check above therefore verifies only leaf-exchange invariance (conjugation by SWAP on two non-hub leaves fixes the operator); the complementary claim — that conjugating by a hub-leaf SWAP yields "the star with the relocated hub" — cannot be constructed from this entangler alone and is not tested. Confirmed by inspection of `topology_graphs.py::_pairwise_graph` (2026-08-01).

**Reused-test coverage (not duplicated in `tests/test_paper_claims.py`):** unitarity and $C_3=K_3$ identities — `tests/test_topologies.py` (`test_pairwise_unitary`, `test_ghz_n2_is_unitary`, `test_ghz_n3_is_unitary`, `test_ring_equals_fully_connected_n3`); equilibrium boundary — `tests/test_ne_guard.py` (node IDs above); per-player star asymmetry — `tests/test_asymmetric_advantage.py` (node IDs above); noise/hardware-mitigation pipelines — `tests/test_hardware_mitigation.py`, `tests/test_noise.py` (unaffected by this task, out of scope for III-F/G/I/J).
