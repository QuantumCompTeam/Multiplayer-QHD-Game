---
type: "query"
date: "2026-06-18T17:33:37.013612+00:00"
question: "Why did we get a 0 payoff for ring config at N=4?"
contributor: "graphify"
source_nodes: ["Ring Topology", "build_ewl_circuit()", "expected_payoff()", "build_payoff_tensor()", "Entanglement Topology", "config.py"]
---

# Q: Why did we get a 0 payoff for ring config at N=4?

## Answer

Expanded from original query via graph vocab tokens: [ring, config, payoff, payoffs, zero, topology, topologies, entanglement, player, gamma, qubits, star]. The '0' is zero quantum ADVANTAGE, not zero payoff. advantage = q_payoff_per_player - classical_ne_payoff (nash.py:207). For the ring (cycle graph C_N, topology_graphs.py:38) at N=4 the Q-profile (Q,Q,Q,Q) payoff (0.25/player) exactly equals the classical all-Hawk NE payoff (0.25/player), so advantage=0.000 (results/month3_topology_sweep/2026-06-18T0857Z/per_player.json, gamma=pi/2, V=4, C=3). Two breaks: (1) q_is_nash=false, the symmetric all-Q Q-NE reverts to a classical NE; (2) the pure-Nash set degenerates to 5 profiles = all-Hawk plus the four paired patterns [Q,Q,H,H],[H,Q,Q,H],[Q,H,H,Q],[H,H,Q,Q] = the 2-colourings of C_4 (its bipartite structure). Unique to N=4: N=2 ring is a single edge (adv 1.5), N=3 ring=C3=K3=fully-connected (adv 1.0), N=4 is the first sparse even cycle distinct from K_N (adv 0.0), N=5 odd cycle recovers 0.6, N=6 even cycle recovers 0.5 - so NOT a generic even-cycle effect, a resonance peculiar to C_4 at gamma=pi/2. Caveat: snapshot at gamma=pi/2 only; no N=4 gamma-sweep folder exists. A gamma sweep at N=4 would show whether the zero is a single-point resonance or range-wide suppression.

## Source Nodes

- Ring Topology
- build_ewl_circuit()
- expected_payoff()
- build_payoff_tensor()
- Entanglement Topology
- config.py