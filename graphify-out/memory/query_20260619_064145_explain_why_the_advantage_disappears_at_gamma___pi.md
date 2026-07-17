---
type: "query"
date: "2026-06-19T06:41:45.056664+00:00"
question: "Explain why the advantage disappears at gamma = pi/2 for the ring"
contributor: "graphify"
source_nodes: ["Ring Topology", "Quantum Advantage Metric", "compute_advantage()", "J_N(gamma) X^N Entangler Formula", "Quantum Nash Equilibrium"]
---

# Q: Explain why the advantage disappears at gamma = pi/2 for the ring

## Answer

Expanded via graph vocab: [ring, gamma, advantage, payoff, equilibrium, nash, topology, entanglement, players, quantum, phase]. MECHANISM: EWL sandwich psi = Jdag(gamma)(U0..U3)J(gamma)|0000> (n_player.py:64). Ring J is pairwise entangler on cycle C_4: J=exp(i gamma/2 sum_edges X_i X_j), edges from nx.cycle_graph(4). gamma is entanglement knob: gamma=0->J=I (no entanglement), gamma=pi/2->MAXIMAL entanglement, each edge factor=(I+i X_iX_j)/sqrt2 (config.py:38). EVIDENCE: N=4 ring gamma-sweep (results/gamma-sweep/N4/results.csv, V=1000 C=550) shows per-player q-payoff sliding monotonically 250.0(0pi)->245.5(.1pi)->205.1(.2pi)->143.4(.3pi)->115.0(.4pi)->112.5(.5pi), landing EXACTLY on classical NE 112.5 at pi/2, advantage 137.5->132.95->92.57->30.87->2.50->0.000. So 'why at pi/2': pi/2 is the maximal-entanglement endpoint and for C_4 max entanglement is exactly where best symmetric quantum profile is dragged down to classical Hawk-Dove NE. TWO CORRECTIONS to prior results: (1) NOT a single-point resonance -- prior note said no N=4 gamma-sweep existed to tell spike vs range-wide; sweep now exists and shows smooth MONOTONE suppression terminating at pi/2, already ~gone by 0.4pi. (2) NOT a V=4,C=3 numeric coincidence -- this sweep uses V=1000,C=550 and STILL hits exactly 0.000 at pi/2, so the cancellation is STRUCTURAL (independent of V/C), not fine-tuned arithmetic. Structural reason: C_4 is bipartite 2-regular even cycle; at pi/2 the pairwise X_iX_j bit-flip interference around the closed even cycle is balanced and the cooperative amplitude that GHZ global X^N and odd cycles preserve gets cancelled by the Jdag un-entangling step -- max entanglement converts the quantum game back to classical. Caveat: q_is_nash=False throughout, all-Q is not an actual equilibrium for the ring at any gamma.

## Source Nodes

- Ring Topology
- Quantum Advantage Metric
- compute_advantage()
- J_N(gamma) X^N Entangler Formula
- Quantum Nash Equilibrium