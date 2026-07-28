# QHD Paper Narrative and Mathematical Redesign

**Date:** 2026-07-28  
**Canonical manuscript:** `paper/qhd.tex`  
**Status:** Approved design

## 1. Purpose

Redesign the QHD manuscript as a rigorous, readable, professional quantum-game-theory paper organized around one central claim: **entanglement topology is a mechanism-design variable in an $N$-player quantum Hawk--Dove trading game**.

The redesign must correct known figure inconsistencies, replace evidence-dump prose with a causal scientific narrative, add the missing mathematical framework and core proofs, rebuild the literature review around the actual research gap, and give every figure one clear evidentiary role followed by meaningful interpretation in the body.

There is no fixed page limit. Scientific completeness and readability take priority over compression, but the manuscript must still be focused rather than monograph-like.

## 2. Confirmed decisions

- Use `paper/qhd.tex` as the authoritative source and supersede the divergent `paper/main.tex` workflow.
- Use a rigorous but readable presentation.
- Organize the paper around topology as mechanism design.
- Reconstruct the narrative rather than surgically expanding the current structure.
- Keep full core proofs in the main manuscript; reserve appendices for secondary expansions and diagnostics.
- Redesign all figures under one visual system.
- Do not combine scientifically distinct results into A/B/C composite figures.
- Present figures sequentially: setup, figure, short caption, meaningful analysis, limitation, transition.
- Split the current Figure 6 into independent scaling, ZNE, and state-quality figures.
- Move secondary investigations, including the finite-round adaptation pilot and extended model diagnostics, to appendices.
- Preserve all negative results and caveats; improve placement and explanation rather than deleting inconvenient evidence.

## 3. Current problems to correct

### 3.1 Figure 4 discrepancy

Player 0 is present in the canonical data. For star topology at $N=4$, its circuit-relative advantage is numerically zero:

\[
\boldsymbol{\Delta}_{\mathrm{star},N=4}=(0,1,1,1).
\]

The red bar is currently invisible because it has zero height. This is a rendering problem, not a scientific-data error. The caption also incorrectly claims $N=2,\ldots,6$ although the asymmetric plot contains only $N=4,5,6$, and it calls the mean "dashed" although the mean is plotted as a green bar.

The redesigned figure must:

- show a baseline marker or explicit `0.00` annotation for Player 0 at $N=4$;
- state that the displayed asymmetric cases are $N=4,5,6$;
- describe the hub, leaf, and mean encodings accurately;
- explain in the body why zero hub advantage can coexist with a high mean.

### 3.2 Figure 6 overload

The current Figure 6 combines three different scientific roles:

- advantage scaling across three executions and two calibration epochs;
- a ZNE fold diagnostic from the registration-source execution only;
- ground-state probability across the cross-calibration aggregate.

These panels do not share one evidentiary population. They must become three independent figures:

1. hardware advantage versus $N$;
2. ZNE fold response and extrapolated intercept;
3. ground-state probability versus $N$.

Each figure receives setup and interpretation in the body. Captions identify the quantity, sample, uncertainty, and one headline observation; they do not contain the full argument.

### 3.3 Narrative failure

The current manuscript repeats the same findings across the abstract, contribution list, simulation section, hardware section, novelty section, and conclusion. Mathematical definitions are deferred or omitted while dense numerical claims appear early. Hardware procedure, results, mechanism, applications, and limitations are combined in one oversized section.

The redesign must remove this repetition and ensure every result answers a previously stated question.

### 3.4 Mathematical under-specification

The current manuscript does not adequately formalize:

- the $N$-player payoff tensor;
- the SU(2) strategy matrix;
- topology-specific entanglers;
- expected payoffs;
- restricted equilibrium;
- the two advantage metrics;
- player-level fairness;
- depolarizing channels;
- readout mitigation and weighted ZNE.

These definitions and the core proofs belong in the main paper.

## 4. Narrative architecture

## I. Introduction

Purpose: establish the mechanism-design problem and the research question.

Flow:

1. Introduce multiplayer Hawk--Dove as a coordination problem with adversarial incentives.
2. Explain why a two-player game has one entanglement relation while an $N$-player market admits multiple correlation graphs.
3. Motivate topology as a design choice rather than an implementation detail.
4. State the central research question:

\[
\textit{How do topology, player count, and noise determine payoff, equilibrium, and fairness?}
\]

5. State three concise contributions:
   - a formal topology-dependent $N$-player EWL game;
   - analytical and simulation results for payoff, equilibrium, fairness, and noise;
   - registered hardware validation of the predicted mechanisms.

The Introduction must not list every hardware percentage, job identifier, model residual, or secondary diagnostic.

## II. Related Work

Organize literature by research strand rather than citation chronology:

1. foundational quantum games and EWL;
2. quantum Hawk--Dove and quantum trading games;
3. multiplayer quantum games;
4. graph/topology-dependent entanglement;
5. quantum mechanism design and quantum economics;
6. asymmetric payoffs and fairness in network games;
7. NISQ game experiments;
8. readout mitigation and zero-noise extrapolation;
9. observable robustness versus state fidelity.

For each strand, state:

- what prior work establishes;
- which assumptions it uses;
- what remains unresolved;
- how the present paper addresses the missing combination.

The bibliography must be expanded through a targeted literature review. Every source must support a concrete claim, method, comparison, or gap; citation padding is prohibited.

## III. Formal Model

Recommended subsections:

1. Classical $N$-player Hawk--Dove game
2. Quantum strategies and the EWL protocol
3. Topology-dependent entanglers
4. Expected payoff, equilibrium, advantage, and fairness
5. Noise and mitigation model
6. Analytical propositions

No result quantity may be used before it is defined.

## IV. Analytical Predictions and Simulation Landscape

Each subsection follows:

> Question -> mathematical expectation -> figure or table -> interpretation -> limitation -> transition.

Order:

1. GHZ cooperative payoff and restricted equilibrium
2. Topology-dependent advantage landscape
3. Entanglement-angle dependence
4. Position-locked unfairness
5. Disagreement between robustness criteria

## V. Registered Hardware Validation

Mirror the predictions from Section IV:

1. protocol, registration, and safeguards;
2. payoff-advantage scaling;
3. ZNE diagnostic;
4. state-quality degradation;
5. topology retention;
6. restricted equilibrium on hardware;
7. wiring-permutation fairness test.

The three former Figure 6 panels are independent figures with explanatory text between them.

## VI. Discussion

Interpret, do not repeat:

- why mean payoff outlives state fidelity;
- topology as a mechanism-design choice;
- restricted equilibrium versus cooperative fixed profiles;
- fairness versus mean welfare;
- what the one-parameter noise models fail to predict;
- limitations, external validity, and application scope.

The standalone novelty section is removed. Novelty belongs in the Introduction and is synthesized in the Discussion.

## VII. Conclusion

Answer the research question directly in a short conclusion. Do not repeat the full result ledger.

## Appendices

- **Appendix A:** secondary derivations and topology-specific operator expansions;
- **Appendix B:** circuit constructions and additional topology details;
- **Appendix C:** finite-round adaptation pilot;
- **Appendix D:** competing noise models and extended diagnostics;
- **Appendix E:** registration, reproducibility, hardware tables, job IDs, qubit lists, and calibration detail.

## 5. Mathematical framework

### 5.1 Classical payoff tensor

Let the player set be $\mathcal P=\{1,\ldots,N\}$, classical action set $\mathcal A=\{D,H\}$, outcome $x\in\{0,1\}^N$, and Hawk count

\[
k(x)=\sum_{j=1}^{N}x_j.
\]

Define player $j$'s payoff by

\[
P_j(x)=
\begin{cases}
V/N, & k(x)=0,\\[2mm]
V/k(x), & 0<k(x)<N \text{ and } x_j=1,\\[2mm]
0, & 0<k(x)<N \text{ and } x_j=0,\\[2mm]
(V-C)/N, & k(x)=N.
\end{cases}
\]

### 5.2 SU(2) strategies

Define

\[
U(\theta,\alpha,\beta)=
\begin{pmatrix}
e^{i\alpha}\cos(\theta/2) & i e^{i\beta}\sin(\theta/2)\\
i e^{-i\beta}\sin(\theta/2) & e^{-i\alpha}\cos(\theta/2)
\end{pmatrix},
\]

then define $D$, $H$, and

\[
Q_N=U(0,\pi/N,\pi/N).
\]

The paper must distinguish the full SU(2) domain from the tested finite menu $\{D,H,Q_N\}$.

### 5.3 EWL protocol

For topology $T$,

\[
\lvert\psi_{\mathrm{out}}\rangle
=
J_T^\dagger
\left(\bigotimes_{j=1}^{N}U_j\right)
J_T\lvert0\rangle^{\otimes N},
\]

\[
p_T(x\mid U_1,\ldots,U_N)
=
\left|\langle x\mid\psi_{\mathrm{out}}\rangle\right|^2,
\]

and

\[
\pi_j(U_1,\ldots,U_N;T)
=
\sum_{x\in\{0,1\}^N}
p_T(x\mid U_1,\ldots,U_N)P_j(x).
\]

The paper must define the GHZ global entangler, graph-based pairwise entanglers for ring, star, and fully connected graphs, and the W-state preparation separately. The operator convention must match the implementation exactly.

### 5.4 Equilibrium, advantage, and fairness

Restricted equilibrium:

\[
\pi_j(Q_N,\ldots,Q_N)
\ge
\pi_j(a,Q_{N,-j})
\qquad
\forall j,\quad a\in\{D,H,Q_N\}.
\]

Deviation gap:

\[
g_j(a)
=
\pi_j(Q_N^{\otimes N})-
\pi_j(a,Q_{N,-j}).
\]

Define circuit-relative and analytic-baseline advantage as separate quantities matching their implemented comparators. The manuscript must explain why they answer different questions and can cross zero at different noise levels.

Represent fairness with

\[
\boldsymbol{\pi}=(\pi_1,\ldots,\pi_N)
\]

and an explicit spread such as

\[
S_\pi=\max_j\pi_j-\min_j\pi_j.
\]

### 5.5 Noise and mitigation

The main model must include:

- exact one- and two-qubit depolarizing-channel definitions;
- the distinction between density-matrix and device-noise simulations;
- readout-confusion-matrix inversion;
- local folding factors $\lambda\in\{1,3,5\}$;
- weighted linear ZNE and the extrapolated intercept;
- retention and state-fidelity definitions.

### 5.6 Core main-text proofs

The following proofs remain in the main body.

#### Proposition 1: total-welfare identity

Prove outcome by outcome that

\[
\sum_{j=1}^{N}P_j(x)=
V-C\,\mathbf 1_{\{x=1^N\}},
\]

and therefore

\[
\bar\pi
=
\frac{V}{N}-\frac{C}{N}\Pr(1^N).
\]

#### Proposition 2: GHZ cooperative profile

Derive the GHZ amplitude evolution, the $Q_N$ phase cancellation, the cooperative output, and

\[
p(0^N)=1,
\qquad
\pi_j=\frac{V}{N}.
\]

For $V=4,C=3$, derive the analytic-baseline advantage $3/N$ using the paper's exact baseline convention.

#### Proposition 3: restricted-deviation condition

Derive the unilateral deviation gaps for $D$ and $H$ wherever analytically supportable. The observed expression

\[
\pi_j(H,Q_{N,-j})=2+2\cos(2\pi/N)
\]

must not be called a theorem unless a valid derivation is supplied and independently checked. Otherwise it remains a computationally verified identity over the tested range.

#### Proposition 4: bit-flip insensitivity

Show that a single flip from $0^N$ produces a one-Hawk outcome $e_j$ and that

\[
\sum_{\ell=1}^{N}P_\ell(0^N)
=
\sum_{\ell=1}^{N}P_\ell(e_j)
=V.
\]

State this as an observable-specific property, not immunity to arbitrary depolarizing noise.

#### Proposition 5: permutation covariance and position locking

For register permutation $R_\sigma$, establish

\[
R_\sigma J_G R_\sigma^\dagger=J_{\sigma(G)}
\]

and the corresponding payoff-vector permutation. Use this to formalize why wiring permutation moves the measured vector with graph position rather than eliminating the hub disadvantage.

Every proof must be followed by a short physical or mechanism-design interpretation.

## 6. Figure and prose system

### 6.1 Global rules

- one primary claim per figure;
- no scientifically heterogeneous A/B/C composite figures;
- consistent type scale, line weight, palette, marker system, and notation;
- direct labels where clearer than legends;
- explicit annotation of exact zeros and exceptional points;
- short captions containing quantity, sample, uncertainty, and one observation;
- substantive interpretation in the body;
- preserved uncertainty definitions and source provenance;
- legibility at final column width.

### 6.2 Result-subsection template

1. State the question or registered prediction.
2. Define the quantity if not already defined.
3. Explain the sample and comparison.
4. Present one figure.
5. Interpret the pattern and mechanism.
6. State uncertainty and scope.
7. Transition to the next question.

### 6.3 Figure-specific redesign

- **Current Figure 1:** distinguish fixed-profile and topology-specific statements; directly indicate restricted-equilibrium cells.
- **Current Figure 2:** simplify the heatmap and label ring $N=4$ zero explicitly.
- **Current Figure 3:** simplify topology labeling and make the $\gamma$ transition the single visual message.
- **Current Figure 4:** expose Player 0's zero at $N=4$; correct scope and caption.
- **Current Figure 5:** separate outcome-distribution and player-payoff evidence.
- **Current Figure 6:** create independent scaling, ZNE, and ground-state-quality figures.
- **Current Figure 7:** create independent topology-retention, restricted-equilibrium-gap, and wiring-permutation figures.

## 7. Writing rules

Every result paragraph follows:

1. claim;
2. evidence;
3. interpretation;
4. scope;
5. transition.

Additional requirements:

- define before use;
- one main scientific claim per paragraph;
- separate proofs, simulations, and hardware observations linguistically;
- move job IDs, qubit lists, and calibration detail to tables or appendices while preserving uncertainty in the body;
- replace repeated numerical summaries with cross-references;
- use stable terms: `cooperative fixed profile`, `restricted-menu equilibrium`, `circuit-relative gap`, and `analytic-baseline advantage`;
- consolidate the adaptation pilot in one appendix;
- rewrite the abstract only after the body is stable;
- keep the conclusion short and answer-driven.

## 8. Source and data architecture

### 8.1 Manuscript ownership

`paper/qhd.tex` is canonical. Documentation and compatibility entry points must delegate to it rather than duplicate manuscript content.

### 8.2 Scientific-data boundary

Redesigned figures use canonical committed artifacts. Do not rerun changed present-day configurations in place of historical studies.

Each figure records:

- source result directory;
- exact JSON/CSV inputs;
- selection rules;
- aggregation method;
- uncertainty definition;
- output filename.

### 8.3 Plotting separation

Figure generation separates:

1. data extraction and validation;
2. scientific transformation;
3. rendering.

The pipeline must fail clearly if expected artifacts, cells, players, or runs are missing. It must not silently omit a zero-value player or unavailable topology.

## 9. Verification

### 9.1 Numerical

- verify redesigned points against canonical JSON/CSV artifacts;
- preserve Figure 6's same-chain and calibration-epoch rules;
- verify Figure 4's $N=4$ hub zero against the regression-pinned result;
- check displayed labels and percentages programmatically where practical.

### 9.2 Mathematical

Run and extend tests covering:

- payoff tensor;
- EWL construction;
- topology operators;
- GHZ $3/N$ advantage;
- restricted-equilibrium boundary;
- star $N=4$ asymmetry;
- continuous-strategy caveats;
- gate-level equivalence;
- depolarizing simulation;
- mitigation and ZNE.

Any new proof must receive an independent symbolic, numerical, or regression check. Unsupported analytic claims are downgraded to computational observations.

### 9.3 Publication

- clean build under the `qhd` job name;
- resolved bibliography and cross-references;
- no undefined citations or references;
- review LaTeX box warnings;
- inspect every rendered page;
- confirm caption-to-figure consistency;
- confirm claim-to-artifact provenance;
- confirm all figures remain legible at actual publication width.

## 10. Acceptance criteria

The redesign is complete when:

1. `paper/qhd.tex` is the single authoritative manuscript;
2. the paper follows the approved topology-as-mechanism-design narrative;
3. the classical and quantum games are mathematically self-contained;
4. the five central propositions are proved in the main body to the extent analytically valid;
5. all figures have one clear claim and no heterogeneous composite panels;
6. Figure 4 explicitly shows Player 0's zero at $N=4$;
7. the former Figure 6 panels are independent figures with meaningful prose between them;
8. the related-work section supports the actual research gap with relevant literature;
9. secondary studies are preserved in appendices without interrupting the main argument;
10. tests pass, the manuscript builds cleanly, and every rendered page is visually inspected;
11. no scientific claim is strengthened beyond its evidence.

## 11. Non-goals

- inventing new hardware data;
- rerunning historical experiments merely to restyle plots;
- claiming unrestricted SU(2) Nash equilibria where only a finite menu was tested;
- proving computational identities without a valid derivation;
- hiding negative results or model failures;
- adding formulas, citations, or figures that do not support the central argument;
- compressing the paper to an arbitrary page limit at the expense of readability.
