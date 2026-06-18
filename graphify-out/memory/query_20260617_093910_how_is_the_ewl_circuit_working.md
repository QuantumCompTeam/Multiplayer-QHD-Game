---
type: "query"
date: "2026-06-17T09:39:10.566810+00:00"
question: "how is the EWL circuit working?"
contributor: "graphify"
source_nodes: ["build_ewl_circuit()", "U()", "ghz_entangler()", "GAMMA (entanglement parameter)", "EWL quantum game protocol", "StrategyParams"]
---

# Q: how is the EWL circuit working?

## Answer

Expanded from original query via graph vocab to tokens: [ewl, circuit, build, entangler, entangling, gate, unitary, strategy, gamma, protocol, sequence, qubit]. BFS traversal started at Entangler nodes (49 nodes). The EWL circuit is built in build_ewl_circuit() (src/circuits/n_player.py:32). Sequence: |0...0> -> J(gamma) entangler -> per-qubit strategy unitaries U(s_j) -> J_dag(gamma) -> Statevector probabilities. J(gamma)=exp(i*gamma/2 * X^N), gamma=pi/2 for max entanglement (GAMMA guard in config.py). U(theta,alpha,beta) is the 2x2 SU(2) strategy gate (src/circuits/ewl.py:20). Default entangler is ghz_entangler (topologies.py:34). Exact probabilities via Qiskit Statevector, no sampling. Bit ordering Qiskit little-endian: player j is Hawk iff (i>>j)&1==1.

## Source Nodes

- build_ewl_circuit()
- U()
- ghz_entangler()
- GAMMA (entanglement parameter)
- EWL quantum game protocol
- StrategyParams