---
type: "query"
date: "2026-06-19T08:50:00.078359+00:00"
question: "Read the latest n-scaling-advantage output and explain what it means"
contributor: "graphify"
source_nodes: ["Quantum Advantage Metric", "Ring Topology", "compute_advantage()", "Quantum Nash Equilibrium"]
---

# Q: Read the latest n-scaling-advantage output and explain what it means

## Answer

Latest run results/n-scaling-advantage/2026-06-19T0845Z, strategy_mode=cooperative (the new per-topology optimizer), 25 cells = 5 topologies x N=2..6, V=1000 C=550 gamma=pi/2. MEANING: each cell plays the topology's OWN payoff-maximizing symmetric quantum strategy instead of the fixed GHZ one. HEADLINE: ring N=4 advantage is now 137.5 (identical to ghz/star/fully-connected), NOT 0 -- the fixed-mode artifact is gone end-to-end through the pipeline. THREE PATTERNS: (1) The four vertex-transitive topologies (ghz, ring, star, fully-connected) are IDENTICAL at every N: q_payoff = V/N exactly (cooperative ceiling, total payoff cannot exceed V), classical_ne = (V-C)/N (all-Hawk equilibrium sharing reduced pot V-C=450), so advantage = V/N - (V-C)/N = C/N = 275,183,137.5,110,91.7 for N=2..6. Interpretation: quantum cooperation reaches split-V instead of all-Hawk split-(V-C), reclaiming exactly the conflict cost C per player; advantage shrinks as 1/N. (2) W is the outlier (adv 137.5,91.7,68.75,55,45.8): same q_payoff V/N but HIGHER classical baseline (362.5 vs 225 at N=2) because the W entangler's classical D/H game already beats all-Hawk, leaving less conflict cost to reclaim. (3) q_is_nash is NO in 20/25 cells (only N=2 four-symmetric + N=5 ghz are Nash): the cooperative optimum is REACHABLE but NOT self-enforcing -- Benjamin-Hayden: not a stable equilibrium vs unrestricted SU(2) deviations. star shows symmetric=no at N>=4 (hub vs leaf payoffs differ; mean still V/N). ONE-LINE: cooperative mode reaches ceiling V/N everywhere so advantage = C/N for the symmetric topologies (ring N=4 included), but it is a payoff you can reach, not one that is self-stabilizing.

## Source Nodes

- Quantum Advantage Metric
- Ring Topology
- compute_advantage()
- Quantum Nash Equilibrium