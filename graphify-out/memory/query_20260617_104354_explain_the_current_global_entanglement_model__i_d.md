---
type: "query"
date: "2026-06-17T10:43:54.758404+00:00"
question: "Explain the current global entanglement model, I didn't understand how it is"
contributor: "graphify"
source_nodes: ["ghz_entangler()", "J_matrix()", "GAMMA (entanglement parameter)", "EWL quantum game protocol"]
---

# Q: Explain the current global entanglement model, I didn't understand how it is

## Answer

Expanded via vocab: [entangler, entangling, ghz, gamma, matrix, formula, qubit, qubits, tensor, identity]. The global entanglement model = ONE gate J_N(gamma) applied across all qubits at once (ghz_entangler, topologies.py:34). Two ingredients summed: (1) cos(gamma/2)*I = 'leave every qubit alone' (identity), (2) i*sin(gamma/2)*X^(x)N = 'flip ALL qubits together' (the all-bits-flip anti-diagonal). The state becomes a superposition of do-nothing + flip-everything. At gamma=pi/2 both weights are 1/sqrt2: |00..0> -> (|00..0> + i|11..1>)/sqrt2. That is global/GHZ because the only two possibilities are all-Dove or all-Hawk, perfectly correlated: measuring one qubit instantly determines all others. gamma is a dial: 0 = no entanglement (stays |00..0>, game is classical), pi/2 = maximal. It is global rather than pairwise because X^(x)N couples every qubit in a single term, not qubit-by-qubit. Reduces to 4x4 J_matrix (ewl.py:42) at N=2.

## Source Nodes

- ghz_entangler()
- J_matrix()
- GAMMA (entanglement parameter)
- EWL quantum game protocol