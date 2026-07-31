# QHD Paper Content Restructure Design

**Date:** 2026-07-31 (v2 — revised after review: venue locked, subsections consolidated, figure specification and style guide added, approval gates batched, data availability added)
**Status:** Approved architecture
**Target manuscript:** `paper/qhd.tex`

## 1. Purpose

Restructure the QHD paper into an accessible but mathematically detailed research narrative. The paper studies an $N$-player quantum Hawk--Dove trading game under multiple entanglement topologies, simulated noise, and IBM hardware validation.

The restructuring will not simplify the science by removing mathematics. It will simplify the reading experience by introducing concepts in dependency order, defining every quantity before use, separating distinct scientific questions, and making the theory, simulation, and hardware evidence form one continuous argument.

The paper will be rewritten collaboratively, one section at a time, with subsections drafted in dependency order and reviewed in batches. Each section must be reviewed for readability, mathematical correctness, citation support, flow, and consistency before work moves to the next section.

## 2. Target Venue and Format

**Venue:** IEEE Transactions on Quantum Engineering (IEEE TQE).

Consequences, fixed for the whole program:

- Template: IEEEtran two-column, as currently used. No template migration.
- Length target: approximately 16--20 pages including appendices. TQE has no hard page limit, but clarity and correctness take priority over artificial compression; repetition and operational detail must be removed from the main narrative.
- Appendices remain in-paper (TQE style), not a separate supplement.
- TQE is open access; the reproducibility posture in Section 10 (archived artifacts with a DOI) matches the venue's expectations.
- All display math, matrices, and tables must fit a single column unless explicitly designed as a two-column (`figure*`/`table*`) float; column-width fit is checked at every compile gate.
- Abstract: single paragraph, approximately 150--250 words, structured as problem, approach, three pillars of evidence, and the headline quantitative findings. No citations, no undefined acronyms.

## 3. Agreed Reader and Scope

### 3.1 Target reader

The main reader is a mixed technical reader who is expected to know undergraduate linear algebra, probability, and basic quantum computing. The paper will not assume prior expertise in:

- quantum game theory;
- the Eisert--Wilkens--Lewenstein protocol;
- multiplayer Hawk--Dove games;
- graph-dependent entanglement;
- restricted equilibrium analysis;
- readout mitigation;
- zero-noise extrapolation;
- observable-specific noise robustness.

Every paper-specific metric and restricted claim must be defined explicitly.

### 3.2 Mathematical depth

All central mathematical definitions and derivations will remain in the main paper. Appendices will contain supporting reproducibility material, circuit expansions, secondary analyses, and full numerical tables rather than core proofs.

### 3.3 Literature depth

The final paper will target more than 50 peer-reviewed sources across the relevant research strands. Every citation must support a specific sentence or comparison. Bibliography size must not be increased through irrelevant padding.

### 3.4 Narrative balance

The paper will use a three-stage argument in which all three pillars are major contributions:

1. theory explains the mechanism;
2. simulation maps its behavior;
3. hardware tests whether the mechanism survives on a real device.

## 4. Central Research Question

> When the two-player quantum Hawk--Dove mechanism is extended to $N$ players, how do entanglement topology, player count, and noise jointly determine cooperative payoff, incentive compatibility, and player-level fairness, and which of those effects survive simulation controls and registered IBM hardware tests?

A secondary distinction will run through the paper:

> Which observed effects arise from the ideal entanglement graph, which arise from its compiled circuit implementation, and which are specific to the physical device?

## 5. Core Narrative Principle

The paper will use a concept-first progression:

\[
\text{intuitive problem}
\longrightarrow
\text{formal definition}
\longrightarrow
\text{analytical prediction}
\longrightarrow
\text{simulation map}
\longrightarrow
\text{hardware test}
\longrightarrow
\text{mechanism-design interpretation}.
\]

Every result subsection must answer a question that was introduced earlier. Every figure must have one primary scientific role. Every formula must be introduced after the reader understands why the quantity is needed.

**Fragmentation rule.** Flow lives in paragraphs, not headers. A subsection exists only when it carries a distinct scientific question; consecutive short subsections that share one question must be merged into one subsection with strong topic sentences. The consolidated architecture below (46 subsection heads, down from ~60) is a ceiling, not a target — merging further during drafting is allowed, splitting requires a spec change.

## 6. Complete Section and Subsection Architecture

# I. Introduction

## I-A. The Multiplayer Coordination Problem

Introduce Hawk--Dove as a model of aggressive versus cooperative trading behavior. Explain why individually rational aggression can reduce total welfare.

## I-B. Why Quantum Correlations May Change the Game

Explain intuitively how the EWL protocol modifies strategic incentives through interference and correlation rather than external regulation.

## I-C. Why Player Count and Entanglement Topology Matter

Explain why topology is not a meaningful design choice for two players but becomes central for $N\geq3$.

## I-D. Research Questions

State four accessible questions:

1. How does topology affect cooperative payoff?
2. When is the cooperative quantum profile an equilibrium?
3. Why can payoff remain stable while the quantum state degrades?
4. Does topology create unequal benefits between players?

## I-E. Contributions and Paper Roadmap

State only three contribution classes:

1. mathematical mechanism;
2. simulation landscape;
3. registered hardware validation.

Do not place job IDs, calibration details, long percentage lists, model residuals, or secondary diagnostics in the Introduction.

# II. Conceptual Background and Related Work

*(Consolidated from nine subsections to six. Each subsection synthesizes a strand against this paper's question; none may read as a standalone mini-survey.)*

## II-A. Classical Hawk--Dove, Network Games, and Mechanism Design

Cover classical payoff conflict, Nash equilibrium, welfare loss, multiplayer extensions, mechanism-design interpretations, and network games with position-dependent payoffs, centrality, asymmetric roles, distributive fairness, and worst-player outcomes.

## II-B. Quantum Game Theory and the EWL Protocol

Cover foundational quantum games, the EWL construction, quantum strategies, entanglement-assisted equilibria, and limitations and criticism of equilibrium claims.

## II-C. Multiplayer Quantum Games and Entanglement Topology

Review $N$-player quantum games, multiplayer strategy spaces, GHZ and W-state games, computational scaling, graph-based entanglement, ring, star, and complete-network structures, including topology-dependent symmetry and circuit cost.

## II-D. Quantum Economics and Trading Applications

Review quantum finance, quantum market mechanisms, trading games, auctions or allocation mechanisms, and the closest two-player quantum trading work.

## II-E. Experimental Quantum Games, NISQ Validation, and Error Mitigation

Review experimental quantum games, superconducting hardware, observable estimation, the limitations of full-state fidelity as the sole performance measure, peer-reviewed readout-error mitigation, local gate folding, ZNE regression, uncertainty, and known failure modes.

## II-F. Research Gap and Paper Positioning

End with one precise gap:

> Existing work does not jointly study a fixed multiplayer economic game across entanglement topology, player count, equilibrium, fairness, circuit noise, and registered hardware validation.

# III. Mathematical Framework

*(Consolidated from eleven subsections to ten: circuit realization and hardware estimators merge into one implementation-layer subsection.)*

## III-A. Notation and the Classical $N$-Player Payoff Tensor

Define players, actions, bitstrings, Hawk count, payoff vectors, mean payoff, and the complete piecewise payoff tensor:

\[
P_j(x)=
\begin{cases}
V/N, & k(x)=0,\\
V/k(x), & 0<k(x)<N,\;x_j=1,\\
0, & 0<k(x)<N,\;x_j=0,\\
(V-C)/N, & k(x)=N.
\end{cases}
\]

## III-B. Classical Equilibrium and Welfare Geometry

Derive the all-Hawk equilibrium for $V=4,C=3$. Prove:

\[
\sum_jP_j(x)=V-C\,\mathbf 1_{\{x=1^N\}},
\]

and therefore

\[
\overline{\pi}
=
\frac{V}{N}
-
\frac{C}{N}\Pr(1^N).
\]

This identity must later explain why mean payoff can survive substantial state degradation.

## III-C. Quantum Strategies and the EWL Protocol

Define the complete SU(2) strategy matrix, classical strategies, $Q_N$, entangling and disentangling operations, output state, and measurement probabilities. Anchored by the protocol schematic (Figure F1 in Section 8).

## III-D. Entanglement Topologies and Graph Symmetry

Formally define GHZ, W, ring, star, and fully connected entanglers. Define graph automorphisms and derive the equality of ideal payoffs for equivalent graph positions. Anchored by the topology gallery (Figure F2 in Section 8).

## III-E. Expected Payoff, Advantage, Equilibrium, and Fairness

Define:

- player payoff vector;
- mean payoff;
- analytic-baseline advantage;
- circuit-relative payoff gap;
- unilateral-deviation gap;
- restricted-menu equilibrium;
- payoff range;
- minimum-player payoff.

The vector remains primary evidence. Scalar fairness summaries must not replace player-level reporting.

## III-F. GHZ Cooperative Benchmark

Prove:

\[
p(0^N)=1,
\qquad
\pi_j=\frac{V}{N},
\qquad
\Delta_{\mathrm{ana}}=\frac{C}{N}.
\]

For $V=4,C=3$:

\[
\Delta_{\mathrm{ana}}=\frac{3}{N}.
\]

## III-G. Incentive Compatibility and the Entanglement-Angle Boundary

Derive unilateral Dove and Hawk deviation payoffs. Establish the restricted-equilibrium boundary at $N=2,3$ versus $N\geq4$. Include the general-$\gamma$ relation so the reader sees how entanglement can modify incentive compatibility without necessarily changing the cooperative payoff.

## III-H. Circuit Realization, Noise Channels, and Hardware Estimators

Separate the four implementation layers:

1. ideal entanglement topology;
2. compiled gate-level circuit;
3. simulated noise;
4. physical-device noise.

Define one- and two-qubit depolarizing channels and explain how two-qubit gate count and routing affect topology comparisons. Then define the hardware estimators applied in Section VI: assignment matrices, constrained probability reconstruction, gate-fold factors, weighted ZNE regression, extrapolated intercepts, and uncertainty conventions. This subsection defines estimators; it reports no results.

## III-I. Structural Robustness of the Payoff Observable

Prove why single-bit-flip outcomes preserve total welfare and why mean payoff can be more stable than ground-state population. Scope the result to the payoff observable and avoid implying preservation of the complete state.

## III-J. Player-Level Redistribution and Position-Locked Fairness

Show mathematically that mean robustness does not imply equal player benefit. Connect permutation covariance to hub-versus-leaf effects in the star topology.

# IV. Analytical Predictions

*(Consolidated from eight subsections to five. This section is short by design: it converts Section III results into the numbered predictions that structure Sections V and VI.)*

## IV-A. From Mathematical Results to Testable Predictions

State which claims are analytical, which require simulation, and which can be tested on hardware. Introduce a compact claim-to-evidence table.

## IV-B. GHZ Scaling and the Restricted-Equilibrium Boundary

State:

\[
\pi_j^{\mathrm{GHZ}}=\frac{V}{N},
\qquad
\Delta_{\mathrm{ana}}^{\mathrm{GHZ}}=\frac{C}{N}.
\]

Explain the difference between decreasing absolute advantage and constant multiplicative advantage over the classical payoff. Predict that the cooperative profile is incentive-compatible for $N=2,3$ and that a Hawk deviation becomes profitable for $N\geq4$.

## IV-C. Topology and Entanglement-Angle Effects

Predict how topology can change output distributions, payoff gaps, equilibrium status, player symmetry, and exceptional interference cells. Use the general-$\gamma$ derivation to predict changes in unilateral-deviation incentives as entanglement strength varies.

## IV-D. Robustness and Fairness Under Noise

Predict that mean payoff will decay more slowly than ground-state population because only all-Hawk probability reduces total welfare. Predict graph-orbit equality, hub-versus-leaf separation, invariance under player-to-qubit reassignment, and the difference between mean payoff and worst-player payoff.

## IV-E. Prediction Ledger for Simulation and Hardware

End with numbered predictions P1--P8. Later result subsections must cite these identifiers directly.

# V. Simulation Landscape

*(Consolidated from nine subsections to six.)*

## V-A. Simulation Design and Verification of the GHZ Scaling Law

Define player counts, topology set, strategy menu, $\gamma$ range, noise range, simulation paths, comparison rules, and recorded estimands. Show that the implementation reproduces the analytical GHZ payoff and advantage before any new claims are made.

## V-B. Controlled Topology Intervention and Exceptional Cells

Hold $Q_N$, $V$, $C$, $N$, and $\gamma$ fixed while changing only the entangler. Describe the result as a controlled topology comparison, not a strategy-optimization claim. Focus on ring $N=4$, star $N=6$, W-state differences, and topology-specific equilibrium markers.

## V-C. Entanglement-Angle Transition

Separate payoff-gap behavior, equilibrium-status transition, and topology-specific response.

## V-D. Player-Level Fairness in the Star Topology

Report the complete payoff vector, identify Player 0 as the hub, and show both payoff range and worst-player payoff. Make the zero hub advantage explicit.

## V-E. Noise Robustness and Circuit-Cost Controls

Compare restricted-equilibrium survival, circuit-relative payoff-gap survival, and analytic-baseline retention. Separate ideal topology effects from compiled-circuit effects through natural-budget, gate-count, matched-count, and normalized-decay comparisons.

## V-F. Simulation Synthesis and Hardware Predictions

Map the simulation predictions to the hardware tests that follow.

# VI. Registered Hardware Validation

*(Consolidated from thirteen subsections to eight.)*

## VI-A. Experimental Protocol, Registration, and Uncertainty

Explain device use, registration, circuit-identity checks, simulator dry runs, physical-qubit selection, shot counts, and the difference between registered and exploratory analyses. Apply the estimators from Section III-H. Distinguish within-run, between-run, between-epoch, and excluded uncertainty sources.

## VI-B. $N=3$ Validation: Output Distribution and Player Payoffs

Use one figure to answer whether the hardware produced the predicted cooperative output distribution, and a paired panel to answer whether the measured distribution preserved the predicted economic payoff.

## VI-C. Advantage Scaling and the ZNE Diagnostic

Present $N=3,4,5$ measured advantage across chain-matched calibration epochs, keeping scaling separate from state quality. Show fold-$1,3,5$ data and the weighted extrapolation. State limitations and avoid treating every increased intercept as proof of successful mitigation.

## VI-D. State Quality Versus Payoff Robustness

Compare ground-state population with payoff-advantage retention and connect the result to the welfare identity.

## VI-E. Extension to $N=6,7$

Present the larger-$N$ run as an external scaling test. Preserve both the high payoff retention and the unresolved ZNE/model behavior.

## VI-F. Topology, Equilibrium, and Entanglement Angle on Device

Compare each topology with its own ideal, treating ring $N=4$ separately because its ideal advantage is zero and its retention ratio is undefined. Present all three unilateral-deviation gaps at GHZ $N=3$, keeping the claim explicitly restricted to the tested strategy menu. Show the sign change in deviation payoff across registered $\gamma$ values and explain the marginal point near $0.4\pi$.

## VI-G. Wiring-Permutation Test of Graph-Position Fairness

Test whether the hub disadvantage follows the player label, physical qubit, or graph position.

## VI-H. Failed Predictions and Negative Results

Report failed absolute payoff predictions, calibration and chain confounding, failure of one-parameter models at larger $N$, ZNE limitations, and unresolved anomalies.

# VII. Discussion

*(Consolidated from ten subsections to six.)*

## VII-A. What Entanglement Topology Actually Controls

Separate topology's effects on ideal interference, equilibrium status, payoff allocation, graph symmetry, and implementation cost. Interpret the natural-budget and matched-gate controls: mathematical graph effects versus routing and gate-cost effects.

## VII-B. Payoff, Equilibrium, and State Quality Are Three Different Claims

Explain why a high cooperative payoff at $N\geq4$ does not imply a self-enforcing equilibrium, and why observable robustness is not state preservation.

## VII-C. Mean Welfare Versus Player-Level Fairness

Discuss payoff range, worst-player payoff, hub-versus-leaf asymmetry, and position-locked disadvantage.

## VII-D. What the Hardware Tests Establish and What the Failures Teach

Summarize the strongest differential and structural hardware conclusions without repeating the full numerical ledger. Discuss reduced noise models, calibration drift, chain dependence, ZNE overshoot, and the greater reliability of within-job differential tests.

## VII-E. Implications for Quantum Mechanism Design

Present possible market and allocation applications as interpretations rather than demonstrated deployments.

## VII-F. Limitations and Future Research

Collect all claim boundaries in one location. Cover continuous strategies, topology-optimized strategies, correlated noise, alternative hardware, larger $N$, fairness-aware objectives, more graph families, and predictive uncertainty.

# VIII. Conclusion

No subsection heads. Two paragraphs: (1) direct, brief answers to the four Introduction questions; (2) the closing design principle that entanglement topology must be evaluated by cooperative payoff, incentive compatibility, noise resilience, fairness, and physical implementation cost.

## 7. Prose Style Guide

This guide is binding for every drafted subsection. It will be saved as `paper/STYLE-GUIDE.md` during Phase 1 and checked at every review gate.

### 7.1 Voice and tense

- First-person plural ("we define", "we measure"); never passive constructions that hide the agent ("it was decided").
- Present tense for mathematics and standing facts ("the identity implies"); past tense for completed experimental actions ("we executed 12 jobs").
- No hype adjectives: "novel", "remarkable", "groundbreaking", "surprisingly" are banned; let the numbers carry the weight.

### 7.2 Paragraph discipline

- Every paragraph opens with a topic sentence stating its claim; the rest of the paragraph supports only that claim.
- Maximum paragraph length approximately 180 words (about 12 lines in one IEEEtran column).
- No paragraph may contain more than two displayed equations without intervening explanatory prose.
- Every displayed equation is followed within two sentences by a plain-language reading of what it says.

### 7.3 Connective tissue (the fluidity mechanism)

- Every subsection opens by answering, in one sentence, "why does the reader need this now?" — linking back to the question or result that created the need.
- Every subsection closes with a one-sentence hand-off to what comes next.
- Every result subsection in Sections V and VI names the prediction identifier (P1--P8) it tests in its first paragraph.
- Cross-references use semantic phrasing ("the welfare identity, Eq. (7)") not bare pointers ("see (7)").

### 7.4 Terminology and notation

- One name per concept, from `paper/CLAIM-SOURCE-MAP.md`; synonyms are defects.
- Every symbol defined before first use; no symbol redefined with a different meaning.
- Acronyms expanded at first use in the abstract and again at first use in the body (EWL, GHZ, ZNE, NISQ).
- The two advantage metrics are always named in full ("analytic-baseline advantage", "circuit-relative payoff gap"), never abbreviated to "advantage" alone where ambiguous.

### 7.5 The flow pass (mandatory, per section)

After all subsections of a section are drafted and individually correct, one dedicated flow pass over the whole section before its approval gate:

1. read the full section top to bottom in the rendered PDF, not the source;
2. rewrite subsection openings/closings so each answers the question the previous one raised;
3. verify the section reads as one author: consistent voice, tense, and terminology;
4. check every 7.1--7.4 rule; fix violations;
5. only then present the section for approval.

## 8. Figure Redesign Specification

The current manuscript's seven figures are data plots only; there is no protocol schematic and no topology diagram, which is why the reader cannot picture the mechanism. Figure work is executed as its own plan after Section III prose is approved, against this specification.

### 8.1 Principles (binding for every figure)

- **One figure, one claim.** Each figure's caption begins with its takeaway as a declarative sentence ("Hardware preserves the cooperative advantage at $N=3$"), then describes panels, then gives provenance. Never a bare label ("Results for $N=3$").
- **Vector only.** All plots regenerated as PDF; the four current PNGs (`advantage_vs_N`, `topology_heatmap`, `advantage_vs_gamma_N4`, `per_player_advantage_star`) are replaced by vector versions from the same pipelines.
- **One visual language.** A single color assignment per topology (GHZ, W, ring, star, complete) used identically in every figure; a single marker convention for ideal / simulated / hardware values; colorblind-safe palette; identical axis labels and units for the same quantity everywhere.
- **Column-fit legibility.** Minimum 8 pt effective font in every figure at final size; single-column width by default, `figure*` only for the two wide hardware aggregates.
- **Prediction linkage.** Every results figure states in its caption which prediction (P1--P8) it tests.

### 8.2 Required new figures

- **F1 — Protocol schematic** (new, Section III-C): the EWL pipeline as a circuit-style diagram — initial state, entangler $J_T(\gamma)$, local strategy gates $U_j$, disentangler, measurement, payoff evaluation. This is the figure the current paper most obviously lacks.
- **F2 — Topology gallery** (new, Section III-D): the five entanglement graphs drawn side by side with qubit labels, hub highlighted in the star, plus per-topology two-qubit gate counts. Replaces a paragraph of prose description.

### 8.3 Redesign of existing figures

| Current figure | Disposition |
|---|---|
| `advantage_vs_N.png` | Regenerate as vector; add analytic $3/N$ curve overlay; caption keyed to P1. |
| `topology_heatmap.png` | Regenerate as vector; annotate the exceptional cells (ring $N=4$, star $N=6$) directly on the heatmap; caption keyed to the topology predictions. |
| `advantage_vs_gamma_N4.png` | Regenerate as vector; mark the equilibrium-transition angle; caption keyed to the entanglement-angle prediction. |
| `per_player_advantage_star.png` | Regenerate as vector; show the full payoff vector with hub emphasized; caption keyed to the fairness prediction. |
| `hardware_n3_validation.pdf` | Restructure as a two-panel figure: measured vs predicted distribution; measured vs predicted payoffs (serves VI-B alone). |
| `hardware_scaling.pdf` | Keep as `figure*`; visually separate raw, mitigated, and extrapolated values; caption keyed to the scaling prediction. |
| `hardware_topology.pdf` | Keep as `figure*`; add per-topology ideal reference lines; flag ring $N=4$ as undefined-retention explicitly. |

### 8.4 Caption standard

```text
Fig. N. <Takeaway sentence stating the claim.> <Panel description:
what is plotted, axes, error-bar meaning.> <Provenance: simulation
pipeline or device/job reference, and the prediction identifier tested.>
```

## 9. Supporting Appendices

### Appendix A. Gate-Level Circuit Constructions

Detailed topology-specific decompositions and native-gate counts.

### Appendix B. Simulation Reproducibility

Parameter grids, artifact locations, software versions, validation checks, and supplementary configuration tables.

### Appendix C. Finite-Round Adaptation Pilot

Exploratory learning-rule results, update-rule sensitivity, and $N=5$ extensions.

### Appendix D. Noise-Model Residuals and Larger-$N$ Diagnostics

Full model residuals, registered judgments, $N=6,7$ diagnostics, ZNE overshoot, and uncertainty limitations.

### Appendix E. Hardware Registration and Provenance

Job identifiers, physical qubits, calibration records, registration artifacts, selection rules, recovery records, and claim-to-artifact provenance.

### Appendix F. Supplementary Player-Level and Topology Tables

Complete payoff vectors, deviation tables, fairness metrics, and topology-specific numerical values.

## 10. Reference Strategy and Data Availability

### 10.1 Reference strategy

The literature audit will seek peer-reviewed sources across:

1. evolutionary and classical Hawk--Dove games;
2. multiplayer and network games;
3. mechanism design and welfare;
4. foundational quantum game theory;
5. EWL protocol extensions and criticism;
6. multiplayer quantum games;
7. graph and multipartite entanglement;
8. GHZ and W-state properties;
9. quantum economics, finance, and trading;
10. network fairness and position-dependent outcomes;
11. experimental quantum games;
12. superconducting quantum hardware;
13. readout-error mitigation;
14. zero-noise extrapolation;
15. observable-specific error resilience;
16. experimental reproducibility and preregistration.

Each citation must be verified against an authoritative publisher, DOI record, or equivalent bibliographic source before inclusion.

### 10.2 Data and code availability (new requirement)

- Before submission, the simulation code, hardware raw counts, registration artifacts, and figure-generation pipelines are archived to Zenodo (or equivalent) and assigned a DOI.
- The manuscript carries explicit Data Availability and Code Availability statements citing that DOI.
- The registered-protocol claims in Section VI must be checkable against the archived registration artifacts, not only against Appendix E prose. This converts "we registered our predictions" from an assertion into a verifiable fact — a major credibility asset at review.

## 11. Collaborative Rewrite Process

The manuscript will be rewritten in dependency order, drafting one subsection at a time but **reviewing in batches** to preserve momentum and global judgment.

For each subsection draft:

1. agree on the exact purpose and claims;
2. list required definitions and formulas;
3. identify the peer-reviewed literature needed;
4. draft the subsection in accessible language following the style guide (Section 7);
5. verify every mathematical statement;
6. verify every numerical claim against its artifact;
7. check citation support;
8. compile the manuscript.

**Approval gates (batched):**

- one gate after the *first* drafted subsection of the program (style calibration — the user corrects voice and density once, early, instead of eleven times);
- one gate per completed section, after that section's flow pass (Section 7.5);
- individual gates are retained only for high-stakes subsections: III-G (incentive-compatibility derivation) and VI-H (failed predictions and negative results).

Recommended rewrite order:

1. terminology, metric definitions, and style guide;
2. Section III mathematical framework;
3. Section IV analytical predictions;
4. figure redesign (Section 8), which needs the P1--P8 ledger;
5. Section V simulation landscape;
6. Section VI hardware validation;
7. Section II literature synthesis;
8. Section VII discussion;
9. appendices and availability statements;
10. Section I Introduction;
11. Section VIII Conclusion;
12. abstract and keywords last.

## 12. Acceptance Criteria

The content restructure is successful when:

- a mixed technical reader can identify the problem before encountering the formalism;
- every symbol and metric is defined before use;
- every central mathematical claim is derived in the main text;
- proof, simulation, and hardware evidence are labeled distinctly;
- simulation and hardware subsections follow the same prediction order;
- one subsection has one primary scientific purpose, and no section exceeds the consolidated subsection count in Section 6;
- every drafted section has passed a flow pass against the style guide before approval;
- one figure has one primary scientific claim, every figure follows the Section 8 caption standard, and figures F1 and F2 exist;
- all figures are vector, colorblind-safe, and use the single shared visual language;
- the two advantage metrics are never conflated;
- restricted-menu equilibrium is never described as full-SU(2) equilibrium;
- mean payoff is never used as a substitute for player-level fairness;
- ideal topology effects are distinguished from compiled-circuit effects;
- failed predictions and negative results remain visible;
- secondary operational detail is moved to appendices;
- the bibliography contains more than 50 relevant, verified, peer-reviewed sources;
- the archived-artifact DOI exists and the Data/Code Availability statements cite it;
- the final paper fits approximately 16--20 IEEEtran pages without repeated result ledgers;
- Introduction questions, analytical predictions, simulation results, hardware tests, Discussion, and Conclusion align one-to-one.

## 13. Explicit Non-Goals for This Phase

This design phase does not:

- rewrite manuscript prose;
- generate figures (figure *specification* is Section 8; figure *execution* is a later plan);
- change scientific claims;
- add unverified citations;
- optimize strategies separately for each topology;
- convert restricted equilibrium claims into unrestricted equilibrium claims.
