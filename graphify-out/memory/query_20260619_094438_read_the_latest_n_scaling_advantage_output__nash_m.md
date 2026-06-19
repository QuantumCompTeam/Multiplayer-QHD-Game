---
type: "query"
date: "2026-06-19T09:44:38.088154+00:00"
question: "Read the latest n-scaling-advantage output (nash mode) and explain what it means"
contributor: "graphify"
source_nodes: ["Quantum Nash Equilibrium", "Ring Topology", "Quantum Advantage Metric", "compute_advantage()"]
---

# Q: Read the latest n-scaling-advantage output (nash mode) and explain what it means

## Answer

Latest run results/n-scaling-advantage/2026-06-19T0939Z, strategy_mode=nash, 25 cells, V=1000 C=550 gamma=pi/2. MEANING: nash mode searches for a self-enforcing equilibrium strategy (best-response fixed point) rather than the best achievable payoff. HEADLINE: for symmetric topologies ghz/ring/fully-connected the nash advantage COLLAPSES to ~0 at every N (incl ring N=4=0), versus the cooperative run where the same cells showed advantage C/N (ring N=4=137.5). So the quantum advantage is ACHIEVABLE BUT NOT SELF-ENFORCING -- requiring equilibrium drags players back to classical conflict payoff (V-C)/N; the advantage evaporates. This reproduces Benjamin-Hayden across all topologies. CAVEAT 1: the 0.000000 cells are NON-equilibria, not stable zeros -- ring N=4 detail shows nash_gap=388 and is_nash=False, meaning the best-response search found NO quantum equilibrium and landed near the classical payoff (no symmetric pure-SU(2) Nash with advantage exists). CAVEAT 2: only 5/25 cells are CERTIFIED Nash (is_nash=True): star N=3 (advantage 0) and W N=3-6 (advantage NEGATIVE: -68.7,-43.4,-30.7,-25.4) -- W's genuinely stable quantum equilibrium pays LESS than classical (flagged advantage<=0 RQ1 finding). Outliers: star N=4 +103.1 (NOT Nash, asymmetric, exploratory), W N=2 +136 (not Nash). Findings: advantage>0 in 21/25 (most are numerically-negligible non-equilibrium values), q_is_nash 5/25. CONTRAST: cooperative answers 'best payoff' = V/N adv C/N; nash answers 'what is stable' = ~0 for symmetric topologies, <=classical for certified equilibria. Ring N=4=0 here is a GENUINE game-theoretic result (no stable advantage), uniform across ghz/ring/fully-connected, NOT the old GHZ-strategy-mismatch artifact.

## Source Nodes

- Quantum Nash Equilibrium
- Ring Topology
- Quantum Advantage Metric
- compute_advantage()