---
type: "query"
date: "2026-06-19T08:55:28.909348+00:00"
question: "Give the formulae for the topology-specific payoff-maximization (cooperative) strategy and the representation meaning"
contributor: "graphify"
source_nodes: ["U()", "q_strategy()", "compute_advantage()", "EWL quantum game protocol", "Quantum Advantage Metric"]
---

# Q: Give the formulae for the topology-specific payoff-maximization (cooperative) strategy and the representation meaning

## Answer

REPRESENTATION: a strategy is one SU(2) gate U(theta,alpha,beta) (ewl.py:20) = [[e^{i a} cos(t/2), i e^{i b} sin(t/2)],[i e^{-i b} sin(t/2), e^{-i a} cos(t/2)]]. theta in [0,pi] = mixing/bit-flip angle (cos(t/2) stay amplitude, sin(t/2) Dove<->Hawk flip; 0=Dove basis, pi=full flip/Hawk); alpha in [-pi,pi] = phase on diagonal/stay amplitudes (the quantum dial, Q uses alpha=pi/N); beta in [-pi,pi] = phase on off-diagonal/flip amplitudes. Named: Dove=U(0,0,0)=I, Hawk=U(pi,0,0)=i sigma_x, GHZ-Q=U(0,pi/N,pi/N). PAYOFF PIPELINE (n_player.py): |psi> = Jdag(gamma) (U_0 (x)...(x) U_{N-1}) J(gamma) |0..0>; p_i=|<i|psi>|^2; J(gamma) is the topology-specific entangler (only thing that varies). Benjamin-Hayden payoff (payoffs.py): k=#Hawks in outcome i -> k=0: V/N all; 0<k<N: Hawk V/k, Dove 0; k=N: (V-C)/N all. pi_j = sum_i p_i P[i,j]. COOPERATIVE OBJECTIVE (strategy_opt._symmetric_payoff): all players same gate, f(t,a,b) = (1/N) sum_j pi_j([U]^(x)N). Optimization (cooperative_strategy): (t*,a*,b*) = argmax_{t in[0,pi], a,b in[-pi,pi]} f, solved by multi-start Nelder-Mead (anchors GHZ-Q/Dove/Hawk + seeded random) then L-BFGS-B polish (non-convex). CLOSED FORM VALUE: sum_j pi_j = V - C*p_allHawk <= V so f <= V/N, equality iff p_allHawk=0; Dove achieves it for every topology (Jdag I J=I), so cooperative optimum f* = V/N for ALL topologies (matches report q_payoff). NASH CERTIFICATE (nash_gap): BR_p(s*) = max_{s'} pi_p(others=s*, player p=s'); nash_gap = max_p [BR_p(s*) - pi_p([s*]^N)]; <=1e-6 => symmetric Nash (continuous analogue of nash.py deviation_check). ADVANTAGE: f* - classical_NE = V/N - (V-C)/N = C/N for vertex-transitive topologies.

## Source Nodes

- U()
- q_strategy()
- compute_advantage()
- EWL quantum game protocol
- Quantum Advantage Metric