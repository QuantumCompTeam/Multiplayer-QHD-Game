---
type: "query"
date: "2026-06-17T10:42:18.357838+00:00"
question: "When extending to more qubits do I need to structure entanglements; are 3 qubits entangled in series or parallel?"
contributor: "graphify"
source_nodes: ["ghz_entangler()", "make_pairwise_entangler()", "Entangler", "build_ewl_circuit()"]
---

# Q: When extending to more qubits do I need to structure entanglements; are 3 qubits entangled in series or parallel?

## Answer

Expanded via vocab: [entangler, entangling, ghz, qubit, qubits, topology, pairwise, ring, star, tensor, formula, extension]. Neither series nor parallel-pairwise: the current GHZ entangler is a SINGLE global gate J_N applied to all N qubits simultaneously (topologies.py:34, ghz_entangler). J_N(gamma)=cos(gamma/2)*I + i*sin(gamma/2)*X^(x)N couples ALL qubits at once via the all-bits-flip X^(x)N term -> symmetric all-to-all GHZ-type correlation (|0..0>+i|1..1>)/sqrt2, no per-pair CNOT chain. So you do NOT manually wire entanglement; you swap the entangler matrix. Structuring entanglement by topology (ring/star/fully-connected pairwise, or W-state) is exactly the Month-3 extension point: make_pairwise_entangler(graph) (topologies.py:62, NotImplementedError stub) returns a closure of the same (N,gamma)->2^N x 2^N signature, and w_entangler (topologies.py:57) for W-states. build_ewl_circuit takes entangler as a pluggable param (n_player.py:36) so its interface never changes. The Entangler type alias (topologies.py:31) is the contract.

## Source Nodes

- ghz_entangler()
- make_pairwise_entangler()
- Entangler
- build_ewl_circuit()