---
type: "query"
date: "2026-06-17T11:44:02.513705+00:00"
question: "Does the quantum payoff advantage (quantum NE payoff minus classical NE payoff) survive, grow, or diminish as N goes 2,3,4,5,6?"
contributor: "graphify"
source_nodes: ["compute_advantage()", "q_strategy()", "find_pure_nash()", "ghz_entangler()", "Quantum Advantage Metric"]
---

# Q: Does the quantum payoff advantage (quantum NE payoff minus classical NE payoff) survive, grow, or diminish as N goes 2,3,4,5,6?

## Answer

Computed live by running compute_advantage(N) for N=2..6 (GHZ X^N entangler, discrete {D,H,Q} set, V=4 C=3). Results: N=2 q=2.0 cNE=0.5 adv=1.5 Q_is_Nash=True; N=3 q=1.333 cNE=0.333 adv=1.0 Nash=True; N=4 q=1.0 cNE=0.25 adv=0.75 Nash=FALSE no pure NE; N=5 q=0.8 cNE=0.2 adv=0.6 Nash=FALSE; N=6 q=0.667 cNE=0.167 adv=0.5 Nash=FALSE. TWO findings: (1) the raw payoff gap DIMINISHES, scaling exactly as advantage=C/N (3/N: 1.5,1.0,0.75,0.6,0.5) - stays strictly positive but tends to 0. Both q_payoff=V/N and classical_ne=(V-C)/N shrink as 1/N; their difference is C/N. (2) MORE IMPORTANTLY the quantum Nash equilibrium only SURVIVES through N=3: at N>=4 (Q_N,...,Q_N) is NOT a pure Nash equilibrium and find_pure_nash returns NO pure NE in {D,H,Q}^N at all. So past N=3 the 'advantage' number is a bare payoff gap, not an enforceable-equilibrium advantage. CAVEATS: only the discrete {D,H,Q} strategy set + GHZ X^N entangler tested; continuous SU(2) Nash is out of scope/future work per spec and could restore equilibria; other topologies (ring/star/W, Month 3) untested. This extends beyond documented N=2,3.

## Source Nodes

- compute_advantage()
- q_strategy()
- find_pure_nash()
- ghz_entangler()
- Quantum Advantage Metric