---
type: "query"
date: "2026-06-18T09:41:59.407294+00:00"
question: "Explain what happened in the topology sweep and why it was effective"
contributor: "graphify"
source_nodes: ["compute_advantage()", "find_pure_nash()", "build_ewl_circuit()", "ghz_entangler()", "make_pairwise_entangler()"]
---

# Q: Explain what happened in the topology sweep and why it was effective

## Answer

The Month-3 RQ2 sweep ran compute_advantage(N) for every (topology, N) in {GHZ,ring,star,full,W} x {2,3,4,5,6} = 25 cells. Each cell: build 3^N strategy profiles over {D,H,Q}, run build_ewl_circuit with that topology's entangler, get exact Statevector probabilities -> per-player payoffs -> find_pure_nash (best-response enumeration) -> advantage = mean(Q,..,Q payoff) - mean(classical NE payoff). Effective because: (1) it isolated topology as the single independent variable while holding gamma=pi/2, V=4, C=3, strategy set fixed - clean controlled experiment; (2) exact statevector (no sampling noise) so differences are real physics not variance; (3) the pluggable Entangler interface meant zero circuit-code changes - only the J matrix swapped; (4) per-player reporting handled the asymmetric star correctly. KEY FINDINGS: advantage shrinks ~C/N for symmetric topos; the quantum Nash equilibrium SURVIVES past N=3 only for ring and W (GHZ and full lose all pure NE at N>=4), so topology determines equilibrium stability - the central RQ2 result. Ring N=4 anomaly: advantage 0.0 but a pure NE exists. W: distinct lower-advantage regime but pure NE at every N.

## Source Nodes

- compute_advantage()
- find_pure_nash()
- build_ewl_circuit()
- ghz_entangler()
- make_pairwise_entangler()