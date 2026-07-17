---
type: "query"
date: "2026-06-19T08:36:35.992985+00:00"
question: "Why is ring N=4 still zero if everything else is fixed?"
contributor: "graphify"
source_nodes: ["Ring Topology", "compute_advantage()", "q_strategy()", "Quantum Advantage Metric"]
---

# Q: Why is ring N=4 still zero if everything else is fixed?

## Answer

Because the config has strategy_mode: 'fixed', which deliberately keeps the GHZ-derived Q = q_strategy(N)=U(0,pi/N,pi/N) for EVERY topology. The cooperative/nash optimizer added in game.strategy_opt is only invoked by sweep.run_cell when strategy_mode != 'fixed' (the q_params=None default preserves legacy behavior byte-for-byte). So in fixed mode nothing changed: ring N=4 still uses the GHZ strategy, which on C_4 at gamma=pi/2 scores 0.25/player = classical all-Hawk NE 0.25 -> advantage 0.000. Other ring cells are nonzero because the GHZ-Q does not land exactly on the classical floor there (N=2:1.5, N=3:1.0, N=4:0.0, N=5:0.6, N=6:0.5). To make ring N=4 nonzero, set strategy_mode: cooperative (or nash) in experiments/config.yaml; then run_cell computes the ring's OWN optimal gate and N=4 reports +0.75 (payoff 1.0 vs classical 0.25), as verified by scripts/topology_optimal_strategy.py. The zero is the GHZ strategy's footprint, not a property of the C_4 topology; fixed mode keeps that footprint.

## Source Nodes

- Ring Topology
- compute_advantage()
- q_strategy()
- Quantum Advantage Metric