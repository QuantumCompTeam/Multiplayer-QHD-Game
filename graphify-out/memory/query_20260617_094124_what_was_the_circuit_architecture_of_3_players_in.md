---
type: "query"
date: "2026-06-17T09:41:24.817240+00:00"
question: "What was the circuit architecture of 3 players in this scenario?"
contributor: "graphify"
source_nodes: ["build_ewl_circuit()", "ghz_entangler()", "q_strategy()", "n3_advantage script", "test_n3_ddd_payoff()", "N-Player Payoff Tensor"]
---

# Q: What was the circuit architecture of 3 players in this scenario?

## Answer

Expanded via graph vocab to tokens: [ghz, three, ddd, entangler, circuit, player, build, ewl, extension, gamma, formula, sequence]. The N=3 circuit uses the SAME build_ewl_circuit(N=3, strategies, entangler=ghz_entangler, gamma=GAMMA) in src/circuits/n_player.py:32 - no separate 3-player function. Architecture: 3 qubits |000> -> J_3(gamma) GHZ entangler -> per-qubit strategy gates U(s0)xU(s1)xU(s2) -> J_3_dag -> Statevector probabilities (8-dim vector). ghz_entangler (topologies.py:34) builds J_3(gamma)=cos(gamma/2)*I^8 + i*sin(gamma/2)*X^3 where X^3 is 8x8 anti-diagonal. At gamma=pi/2: J_3|000>=(|000>+i|111>)/sqrt(2) (Option A, relative phase i). N=3 quantum Nash strategy is Q_3=U(0,pi/3,pi/3) from q_strategy(3). Driver: scripts/n3_advantage.py runs compute_advantage(N=3) for RQ1 (quantum vs classical NE). Tests: test_n3_ddd_payoff (all-Dove gives 4/3 per player).

## Source Nodes

- build_ewl_circuit()
- ghz_entangler()
- q_strategy()
- n3_advantage script
- test_n3_ddd_payoff()
- N-Player Payoff Tensor