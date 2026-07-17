---
type: "query"
date: "2026-06-19T06:36:53.310392+00:00"
question: "The bipartite argument for the N=4 ring doesnt hold up because every star config is a proper bipartite graph and that is able to give a proper advantage?"
contributor: "graphify"
source_nodes: ["Ring Topology", "Star Topology", "build_payoff_tensor()", "Entanglement Topology", "Fully-Connected Topology"]
---

# Q: The bipartite argument for the N=4 ring doesnt hold up because every star config is a proper bipartite graph and that is able to give a proper advantage?

## Answer

CORRECT - bipartite argument fails on two counts. Expanded via graph vocab: [ring, star, topology, topologies, advantage, payoff, entanglement, ghz, connected, equilibrium, players, quantum]. (1) Star is bipartite (K_1,3) yet gives advantage 0.75 while ring C_4 gives 0.0 -- two bipartite graphs, opposite results, so bipartiteness cannot be the cause. Data: results/month3_topology_sweep/2026-06-18T0857Z/per_player.json gamma=pi/2 V=4 C=3: ring q_payoff=[0.25,0.25,0.25,0.25] adv 0.0; star q_payoff=[0.25,1.25,1.25,1.25] adv 0.75. (2) The prior note mislabeled the ring's 4 paired Nash profiles [Q,Q,H,H] etc as 2-colourings of C_4 -- they are contiguous QQ/HH domain-wall blocks with monochromatic edges, NOT proper 2-colourings; the actual 2-colourings [Q,H,Q,H]/[H,Q,H,Q] are ABSENT from the Nash set. Real distinction: ring zero = numerical resonance from vertex-transitive 2-regularity (uniform 0.25/player coincides with classical all-Hawk NE at gamma=pi/2; N=3->1.0, N=5->0.6, N=6->0.5 so peculiar to C_4). Star advantage = enabled by ASYMMETRY: hub sacrificed (0.25) while 3 leaves gain (1.25 each), mean=1.0 vs classical 0.25. Caveat: both have q_is_nash=false at N=4, off-equilibrium snapshots at gamma=pi/2 only.

## Source Nodes

- Ring Topology
- Star Topology
- build_payoff_tensor()
- Entanglement Topology
- Fully-Connected Topology