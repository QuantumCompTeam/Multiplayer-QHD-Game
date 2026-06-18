# Graph Report - .  (2026-06-17)

## Corpus Check
- Corpus is ~13,714 words - fits in a single context window. You may not need a graph.

## Summary
- 180 nodes · 299 edges · 12 communities (10 shown, 2 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 53 edges (avg confidence: 0.64)
- Token cost: 0 input · 121,324 output

## Community Hubs (Navigation)
- [[_COMMUNITY_EWL Strategies & J Gate|EWL Strategies & J Gate]]
- [[_COMMUNITY_N-Player Circuit & Nash Analysis|N-Player Circuit & Nash Analysis]]
- [[_COMMUNITY_Benjamin-Hayden Payoffs|Benjamin-Hayden Payoffs]]
- [[_COMMUNITY_Entangler Topologies|Entangler Topologies]]
- [[_COMMUNITY_Two-Player EWL & Literature|Two-Player EWL & Literature]]
- [[_COMMUNITY_Two-Player Validation Tests|Two-Player Validation Tests]]
- [[_COMMUNITY_Topology & N-Player Design|Topology & N-Player Design]]
- [[_COMMUNITY_N-Player Circuit Tests|N-Player Circuit Tests]]
- [[_COMMUNITY_N=3 Advantage Script|N=3 Advantage Script]]
- [[_COMMUNITY_Game Config|Game Config]]

## God Nodes (most connected - your core abstractions)
1. `build_ewl_circuit()` - 20 edges
2. `StrategyParams` - 19 edges
3. `ghz_entangler()` - 18 edges
4. `outcome_payoff()` - 16 edges
5. `expected_payoff()` - 16 edges
6. `Entangler` - 15 edges
7. `U()` - 15 edges
8. `run_two_player()` - 14 edges
9. `build_payoff_tensor()` - 13 edges
10. `_ep()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Quantum Advantage Metric` --references--> `compute_advantage()`  [INFERRED]
  README.md → src/game/nash.py
- `GHZ State Topology` --references--> `ghz_entangler()`  [INFERRED]
  README.md → src/circuits/topologies.py
- `SU(2) Strategy U(theta,alpha,beta)` --references--> `U()`  [INFERRED]
  README.md → src/circuits/ewl.py
- `N-Player Payoff Tensor` --references--> `expected_payoff()`  [INFERRED]
  docs/superpowers/specs/2026-06-09-n3-ghz-extension-design.md → src/game/payoffs.py
- `Pure Nash Best-Response Enumeration` --implements--> `find_pure_nash()`  [EXTRACTED]
  docs/superpowers/specs/2026-06-09-n3-ghz-extension-design.md → src/game/nash.py

## Hyperedges (group relationships)
- **N-player EWL circuit construction flow** — circuits_n_player_build_ewl_circuit, circuits_ewl_u, circuits_topologies_ghz_entangler, src_config_gamma [EXTRACTED 0.90]
- **Quantum advantage analysis pipeline** — game_nash_compute_advantage, game_nash_build_payoff_tensor, game_nash_find_pure_nash, game_payoffs_expected_payoff, circuits_n_player_build_ewl_circuit [EXTRACTED 0.90]
- **EWL named strategy constants and N-player generalization** — circuits_ewl_dove, circuits_ewl_hawk, circuits_ewl_q, circuits_ewl_q_strategy, game_nash_strategy_map [EXTRACTED 0.85]
- **N=2 backward-compatibility reduction guards** — tests_test_n_player_test_n2_qq_payoff, tests_test_ewl_test_q_strategy_n2_equals_q, tests_test_topologies_test_ghz_n2_matches_j_matrix [INFERRED 0.85]
- **Two-player (Q,Q)->(2,2) quantum Nash validation** — tests_test_two_player_test_q_q_yields_cooperative_payoff, tests_test_two_player_test_nash_hawk_deviation_does_not_improve, tests_test_two_player_test_nash_dove_deviation_does_not_improve [EXTRACTED 1.00]
- **Classical 2x2 Hawk-Dove payoff table coverage** — tests_test_payoffs_test_dove_dove, tests_test_payoffs_test_hawk_dove, tests_test_payoffs_test_dove_hawk, tests_test_payoffs_test_hawk_hawk [INFERRED 0.95]
- **EWL Protocol Design (6-step quantisation)** — readme_ewl_protocol, readme_su2_strategy, readme_q_strategy, readme_quantum_nash_equilibrium, specs_2026_06_08_ewl_scaffold_design_gamma_guard [INFERRED 0.85]
- **Five Entanglement Topologies** — readme_ghz_state, readme_w_state, readme_ring_topology, readme_star_topology, readme_fully_connected_topology [EXTRACTED 0.75]
- **N=3 GHZ Advantage Computation Pipeline** — specs_2026_06_09_n3_ghz_extension_design_jn_formula, specs_2026_06_09_n3_ghz_extension_design_payoff_tensor, specs_2026_06_09_n3_ghz_extension_design_pure_nash_enumeration, game_nash_compute_advantage [INFERRED 0.85]

## Communities (12 total, 2 thin omitted)

### Community 0 - "EWL Strategies & J Gate"
Cohesion: 0.08
Nodes (35): DOVE strategy, HAWK strategy, J_matrix(), make_J_dag_gate(), make_J_gate(), Q strategy (N=2 quantum Nash), q_strategy(), EWL protocol: strategy unitary U(theta, alpha, beta), entangling operators J and (+27 more)

### Community 1 - "N-Player Circuit & Nash Analysis"
Cohesion: 0.14
Nodes (30): Any, build_ewl_circuit(), General N-qubit EWL Hawk-Dove circuit.  Circuit sequence for N players:   |0...0, Run an N-player EWL circuit and return exact outcome probabilities.      N: numb, Entangler (type alias), build_payoff_tensor(), compute_advantage(), find_pure_nash() (+22 more)

### Community 2 - "Benjamin-Hayden Payoffs"
Cohesion: 0.11
Nodes (25): expected_payoff(), index_to_bitstring(), outcome_payoff(), N-player Hawk-Dove payoff functions (Benjamin-Hayden formula).  Interface contra, Return the Qiskit-convention bitstring for basis state index i with n qubits., Return per-player payoffs for basis state index i (Benjamin-Hayden formula)., Return expected per-player payoffs given a probability distribution.      probs:, Benjamin-Hayden Payoff Formula (+17 more)

### Community 3 - "Entangler Topologies"
Cohesion: 0.12
Nodes (20): ghz_entangler(), make_pairwise_entangler(), Entangling operators for N-qubit EWL circuits.  Each entangler has signature, J_N(gamma) = cos(gamma/2) * I^(x)N + i * sin(gamma/2) * X^(x)N.      X^(x)N is t, W-state EWL entangler. Implemented in Month 3., Factory for ring / star / fully-connected topologies. Implemented in Month 3., w_entangler(), object (+12 more)

### Community 4 - "Two-Player EWL & Literature"
Cohesion: 0.10
Nodes (21): Month-1 two-player EWL Hawk-Dove circuit.  Thin wrapper around build_ewl_circuit, Run the 2-player EWL circuit and return exact outcome probabilities.      s0: (t, run_two_player(), Carbon Trading Application, Eisert, Wilkens & Lewenstein (1999), Entangled Equilibria Project, EWL Quantisation Protocol, Hawk-Dove Game (+13 more)

### Community 5 - "Two-Player Validation Tests"
Cohesion: 0.18
Nodes (15): _ep(), float, float64, NDArray, Month-1 checkpoint: two-player EWL Hawk-Dove validation.  Proves three things:, (Q, Q) -> expected payoff (2.0, 2.0): the quantum Nash equilibrium.      Passes, Player 0 deviating to HAWK while player 1 stays on Q must not exceed 2.0., Player 0 deviating to DOVE while player 1 stays on Q must not exceed 2.0. (+7 more)

### Community 6 - "Topology & N-Player Design"
Cohesion: 0.21
Nodes (12): Benjamin & Hayden (2001), Depolarizing Noise Channel, Entanglement Topology, Flitney & Abbott (2002), Fully-Connected Topology, GHZ State Topology, N-Player Extension, Ring Topology (+4 more)

### Community 7 - "N-Player Circuit Tests"
Cohesion: 0.33
Nodes (5): Tests for build_ewl_circuit in n_player.py.  Two correctness guards before the N, build_ewl_circuit(2, [Q, Q]) must reproduce the Month-1 (Q,Q) -> (2,2) result., build_ewl_circuit(3, [D, D, D]) must give [4/3, 4/3, 4/3] per player.      Analy, test_n2_qq_payoff(), test_n3_ddd_payoff()

## Knowledge Gaps
- **11 isolated node(s):** `object`, `int`, `str`, `float`, `NDArray` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ghz_entangler()` connect `Entangler Topologies` to `EWL Strategies & J Gate`, `N-Player Circuit & Nash Analysis`, `Topology & N-Player Design`?**
  _High betweenness centrality (0.298) - this node is a cross-community bridge._
- **Why does `build_ewl_circuit()` connect `N-Player Circuit & Nash Analysis` to `EWL Strategies & J Gate`, `Benjamin-Hayden Payoffs`, `Entangler Topologies`, `Two-Player EWL & Literature`, `N-Player Circuit Tests`?**
  _High betweenness centrality (0.267) - this node is a cross-community bridge._
- **Why does `expected_payoff()` connect `Benjamin-Hayden Payoffs` to `N-Player Circuit & Nash Analysis`, `Two-Player EWL & Literature`, `Two-Player Validation Tests`, `N-Player Circuit Tests`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `build_ewl_circuit()` (e.g. with `UnitaryGate` and `expected_payoff()`) actually correct?**
  _`build_ewl_circuit()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `StrategyParams` (e.g. with `int` and `StrategyParams`) actually correct?**
  _`StrategyParams` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ghz_entangler()` (e.g. with `J_matrix()` and `GHZ State Topology`) actually correct?**
  _`ghz_entangler()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `expected_payoff()` (e.g. with `build_ewl_circuit()` and `N-Player Payoff Tensor`) actually correct?**
  _`expected_payoff()` has 2 INFERRED edges - model-reasoned connections that need verification._