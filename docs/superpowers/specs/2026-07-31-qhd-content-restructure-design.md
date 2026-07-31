# QHD Paper Content Restructure Design

**Date:** 2026-07-31 (v3 — revised after engineering review: TQE manuscript shell migration added, entangler-family vocabulary adopted, hardware-evidence decision rule defined, general-$\gamma$ cooperative proposition added, notation and audit contracts strengthened, gates G1--G5 explicitly authorized)
**Status:** Approved architecture
**Target manuscript:** `paper/qhd.tex`

## 1. Purpose

Restructure the QHD paper into an accessible but mathematically detailed research narrative. The paper studies an $N$-player quantum Hawk--Dove trading game under multiple entangler families, simulated noise, and IBM hardware validation.

The restructuring will not simplify the science by removing mathematics. It will simplify the reading experience by introducing concepts in dependency order, defining every quantity before use, separating distinct scientific questions, and making the theory, simulation, and hardware evidence form one continuous argument.

The paper will be rewritten collaboratively, one section at a time, with subsections drafted in dependency order and reviewed at the five authorized gates (Section 11). Each section must be reviewed for readability, mathematical correctness, citation support, flow, and consistency before work moves to the next section.

## 2. Target Venue and Format

**Venue:** IEEE Transactions on Quantum Engineering (IEEE TQE).

Consequences, fixed for the whole program:

- **Manuscript shell migration (first execution task).** The manuscript currently uses `\documentclass[conference]{IEEEtran}` and the repository contains a competing entry point (`paper/main.tex`, still built by `paper/README.md`, which also still names IEEE QCE). Before any prose is rewritten: diff `main.tex` against `qhd.tex` and resolve any divergence explicitly (verified content must not silently disappear); migrate `qhd.tex` to the official TQE journal template from the IEEE Author Center; make `paper/qhd.tex` the canonical manuscript; convert `paper/main.tex` into a thin wrapper or remove it; update `paper/README.md` to name TQE and build `qhd.tex`.
- Length target: approximately 16--20 pages including appendices. TQE has no hard page limit, but clarity and correctness take priority over artificial compression; repetition and operational detail must be removed from the main narrative.
- Appendices remain in-paper (TQE style), not a separate supplement.
- TQE is open access; the reproducibility posture in Section 10 (archived artifacts with a DOI) matches the venue's expectations.
- All display math, matrices, and tables must fit a single column unless explicitly designed as a two-column (`figure*`/`table*`) float; column-width fit is checked at every compile gate.
- Abstract: single paragraph, approximately 150--250 words, structured as problem, approach, three pillars of evidence, and the headline quantitative findings. No citations, no undefined acronyms.

## 3. Agreed Reader, Scope, and Vocabulary

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

### 3.2 Comparison vocabulary (binding)

The five compared entanglers are not all graphs, so the paper adopts two-level vocabulary:

- **Entangler family** — the umbrella term for the five-way comparison: GHZ, W, ring, star, and complete. Every five-way statement says "entangler family," never "topology."
- **Graph topology** — reserved for the pairwise-graph families only (ring, star, complete), where an edge set $E(G)$ genuinely exists. Graph-position language (hub, leaf, orbit) applies only here.
- Because GHZ and W use a single global interpolation angle while pairwise families compose per-edge rotations, equal $\gamma$ does not mean equal total interaction strength across families. The paper defines a **normalized interaction-strength convention** in III-D and reports a sensitivity control under it in Section V, so family comparisons are not confounded by raw coupling budget.

### 3.3 Target-state naming (binding)

The quantity $P(0^N)$ is canonically named the **all-zero target-state population** (shorthand after first definition: *target-state population*). It must never be called "ground-state population" (the all-zero computational basis state is not a Hamiltonian ground state) and never "state fidelity" unless an actual full-state fidelity is computed.

### 3.4 Mathematical depth

All central mathematical definitions and derivations will remain in the main paper. Appendices will contain supporting reproducibility material, circuit expansions, secondary analyses, and full numerical tables rather than core proofs.

### 3.5 Literature depth

The final paper will target more than 50 peer-reviewed sources across the relevant research strands. Every citation must support a specific sentence or comparison. Bibliography size must not be increased through irrelevant padding.

### 3.6 Narrative balance

The paper will use a three-stage argument in which all three pillars are major contributions:

1. theory explains the mechanism;
2. simulation maps its behavior;
3. hardware tests whether the mechanism survives on a real device.

## 4. Central Research Question

> When the two-player quantum Hawk--Dove mechanism is extended to $N$ players, how do entangler family, player count, and noise jointly determine cooperative payoff, incentive compatibility, and player-level fairness, and which of those effects survive simulation controls and registered IBM hardware tests?

A secondary distinction will run through the paper:

> Which observed effects arise from the ideal entangler family, which arise from its compiled circuit implementation, and which are specific to the physical device?

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

## I-C. Why Player Count and Entangler Structure Matter

Explain why the choice of entangler is not a meaningful design decision for two players but becomes central for $N\geq3$, and preview the entangler-family versus graph-topology distinction.

## I-D. Research Questions

State four accessible questions:

1. How does the entangler family affect cooperative payoff?
2. When is the cooperative quantum profile an equilibrium?
3. Why can payoff remain stable while the quantum state degrades?
4. Does the entangler family create unequal benefits between players?

Hardware cross-cuts the questions rather than being a question of its own: each question is answered at up to three evidence levels — analytical prediction, simulation behavior, and hardware survival — and every result is labeled with the level it attains.

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

## II-C. Multiplayer Quantum Games and Entanglement Structure

Review $N$-player quantum games, multiplayer strategy spaces, GHZ and W-state games, computational scaling, graph-based entanglement, ring, star, and complete-network structures, including structure-dependent symmetry and circuit cost.

## II-D. Quantum Economics and Trading Applications

Review quantum finance, quantum market mechanisms, trading games, auctions or allocation mechanisms, and the closest two-player quantum trading work.

## II-E. Experimental Quantum Games, NISQ Validation, and Error Mitigation

Review experimental quantum games, superconducting hardware, observable estimation, the limitations of full-state fidelity as the sole performance measure, peer-reviewed readout-error mitigation, local gate folding, ZNE regression, uncertainty, and known failure modes.

## II-F. Research Gap and Paper Positioning

End with one precise gap:

> Existing work does not jointly study a fixed multiplayer economic game across entangler family, player count, equilibrium, fairness, circuit noise, and registered hardware validation.

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

## III-D. Entangler Families and Graph Symmetry

Formally define the GHZ, W, ring, star, and fully connected entanglers, using the two-level vocabulary of Section 3.2. Define graph automorphisms for the pairwise families and derive the equality of ideal payoffs for equivalent graph positions. Define the normalized interaction-strength convention that Section V's sensitivity control uses. Anchored by the entangler-family gallery (Figure F2 in Section 8).

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

Prove the benchmark at maximal entanglement:

\[
p(0^N)=1,
\qquad
\pi_j=\frac{V}{N},
\qquad
\Delta_{\mathrm{ana}}=\frac{C}{N}.
\]

For $V=4,C=3$: $\Delta_{\mathrm{ana}}=3/N$.

**General-$\gamma$ cooperative invariance (new proposition).** State and prove that for the GHZ entangler the cooperative output is invariant in $\gamma$:

\[
J_{\mathrm{GHZ}}^\dagger(\gamma)\,Q_N^{\otimes N}\,J_{\mathrm{GHZ}}(\gamma)\,|0^N\rangle=-\,|0^N\rangle
\quad\text{for every }\gamma .
\]

The proof is four lines: $J_{\mathrm{GHZ}}(\gamma)|0^N\rangle=\cos(\gamma/2)|0^N\rangle+i\sin(\gamma/2)|1^N\rangle$; $Q_N=U(0,\pi/N,\pi/N)$ multiplies the all-zero branch by $e^{iN\pi/N}=-1$ and the all-one branch by $e^{-iN\pi/N}=-1$ — the same phase — so the state is exactly $-J_{\mathrm{GHZ}}(\gamma)|0^N\rangle$ and the disentangler returns $|0^N\rangle$ up to global phase. Numerically confirmed for $N=2,\ldots,5$ and $\gamma\in\{0,0.2\pi,0.4\pi,0.5\pi\}$ (minimum $P(0^N)$ within $2\times10^{-16}$ of 1). This proposition is what makes III-G meaningful: $\gamma$ moves the deviation incentive while leaving the cooperative payoff exactly unchanged.

## III-G. Incentive Compatibility and the Entanglement-Angle Boundary

Derive unilateral Dove and Hawk deviation payoffs. Establish the restricted-equilibrium boundary at $N=2,3$ versus $N\geq4$. Include the general-$\gamma$ relation so the reader sees how entanglement strength modifies incentive compatibility while (by the III-F invariance) the cooperative payoff is unchanged. The Dove deviation receives the same treatment as the Hawk deviation: a closed form verified numerically before publication, plus the non-binding inequality across the stated $(N,\gamma)$ scope — analytic non-bindingness at $\gamma=\pi/2$ is not assumed to extend elsewhere without a check.

## III-H. Circuit Realization, Noise Channels, and Hardware Estimators

Separate the four implementation layers:

1. ideal entangler family;
2. compiled gate-level circuit;
3. simulated noise;
4. physical-device noise.

Define one- and two-qubit depolarizing channels with strength $\eta$ and explain how two-qubit gate count and routing affect family comparisons.

Then define the hardware estimators applied in Section VI: assignment matrices, constrained probability reconstruction, gate-fold scales $s\in\{1,3,5\}$, weighted ZNE regression, extrapolated intercepts, and uncertainty conventions.

**Symbol discipline (binding):** $\eta$ is the depolarizing probability; $s$ is the ZNE fold scale; $\gamma$ is the entanglement angle; $\lambda$ is not used for any of these. No symbol is defined twice with different meanings.

**Independence assumption (binding):** the tensor-product assignment model $A=\bigotimes_jA_j$ assumes separable per-qubit readout errors and does not model correlated readout crosstalk (this limitation is already documented in `src/hardware/mitigation.py`). The assumption is stated directly beside the equation, and correlated readout error is listed among the excluded uncertainty/model components.

**Registered decision rule (binding, new):** one uncertainty convention is defined here and applied to *every* hardware sign or threshold claim in Section VI — the equilibrium gaps, the entanglement-angle sign change (including the marginal point near $0.4\pi$), the ring-$N{=}4$ special case, and the hub-versus-leaf separation. A positive point estimate is never sufficient: each claim states a one-sided interval at a declared level (or a registered non-inferiority margin) and passes or fails by that rule.

## III-I. Structural Robustness of the Payoff Observable

Prove why single-bit-flip outcomes preserve total welfare and why mean payoff can be more stable than the all-zero target-state population. Scope the result to the payoff observable and avoid implying preservation of the complete state.

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

## IV-C. Entangler-Family and Entanglement-Angle Effects

Predict how the entangler family can change output distributions, payoff gaps, equilibrium status, player symmetry, and exceptional interference cells. Use the general-$\gamma$ derivation plus the III-F invariance to predict that unilateral-deviation incentives move with entanglement strength while the cooperative payoff does not.

## IV-D. Robustness and Fairness Under Noise

Predict that mean payoff will decay more slowly than the all-zero target-state population because only all-Hawk probability reduces total welfare. Predict graph-orbit equality, hub-versus-leaf separation, invariance under player-to-qubit reassignment, and the difference between mean payoff and worst-player payoff.

## IV-E. Prediction Ledger for Simulation and Hardware

End with numbered predictions P1--P8. Later result subsections must cite these identifiers directly.

# V. Simulation Landscape

*(Consolidated from nine subsections to six.)*

## V-A. Simulation Design and Verification of the GHZ Scaling Law

Define player counts, entangler-family set, strategy menu, $\gamma$ range, noise range, simulation paths, comparison rules, and recorded estimands. Show that the implementation reproduces the analytical GHZ payoff and advantage before any new claims are made.

## V-B. Controlled Entangler-Family Intervention and Exceptional Cells

Hold $Q_N$, $V$, $C$, $N$, and $\gamma$ fixed while changing only the entangler. Describe the result as a controlled family comparison, not a strategy-optimization claim. Report the normalized interaction-strength sensitivity control from III-D so family effects are not confounded by raw coupling budget. Focus on ring $N=4$, star $N=6$, W-state differences, and family-specific equilibrium markers.

## V-C. Entanglement-Angle Transition

Separate payoff-gap behavior, equilibrium-status transition, and family-specific response.

## V-D. Player-Level Fairness in the Star Topology

Report the complete payoff vector, identify Player 0 as the hub, and show both payoff range and worst-player payoff. Make the zero hub advantage explicit.

## V-E. Noise Robustness and Circuit-Cost Controls

Compare restricted-equilibrium survival, circuit-relative payoff-gap survival, and analytic-baseline retention. Separate ideal family effects from compiled-circuit effects through natural-budget, gate-count, matched-count, and normalized-decay comparisons.

## V-F. Simulation Synthesis and Hardware Predictions

Map the simulation predictions to the hardware tests that follow.

# VI. Registered Hardware Validation

*(Consolidated from thirteen subsections to eight.)*

## VI-A. Experimental Protocol, Registration, and Uncertainty

Explain device use, registration, circuit-identity checks, simulator dry runs, physical-qubit selection, shot counts, and the difference between registered and exploratory analyses. Apply the estimators and the registered decision rule from Section III-H. Distinguish within-run, between-run, between-epoch, and excluded uncertainty sources (including correlated readout error, per III-H).

## VI-B. $N=3$ Validation: Output Distribution and Player Payoffs

Use one figure to answer whether the hardware produced the predicted cooperative output distribution, and a paired panel to answer whether the measured distribution preserved the predicted economic payoff.

## VI-C. Advantage Scaling and the ZNE Diagnostic

Present $N=3,4,5$ measured advantage across chain-matched calibration epochs, keeping scaling separate from state quality. Show fold-$s\in\{1,3,5\}$ data and the weighted extrapolation. State limitations and avoid treating every increased intercept as proof of successful mitigation.

## VI-D. State Quality Versus Payoff Robustness

Compare the all-zero target-state population with payoff-advantage retention and connect the result to the welfare identity.

## VI-E. Extension to $N=6,7$

Present the larger-$N$ run as an external scaling test. Preserve both the high payoff retention and the unresolved ZNE/model behavior.

## VI-F. Entangler Families, Equilibrium, and Entanglement Angle on Device

Compare each entangler family with its own ideal, treating ring $N=4$ separately because its ideal advantage is zero and its retention ratio is undefined.

**Hardware equilibrium evidence rule (new).** The restricted menu is $\{D,H,Q_N\}$, so a hardware equilibrium claim at GHZ $N=3$ requires $g_j(D)\geq0$ *and* $g_j(H)\geq0$ for every player — six gaps, not three. Before drafting: check the archived hardware artifacts for Dove-deviation executions. If the six gaps exist in the registered data, report all six under the III-H decision rule. If Dove-deviation circuits were never executed (no new IBM jobs are in scope), the claim is narrowed to exactly: "no profitable unilateral **Hawk** deviation was observed within the tested menu," and the Dove gap is labeled analytically predicted, hardware-untested. The manuscript must state which branch applies.

Show the sign change in deviation payoff across registered $\gamma$ values under the III-H decision rule, and explain the marginal point near $0.4\pi$ as marginal rather than resolved if its interval includes zero.

## VI-G. Wiring-Permutation Test of Graph-Position Fairness

Test whether the hub disadvantage follows the player label, physical qubit, or graph position, judged under the III-H decision rule.

## VI-H. Failed Predictions and Negative Results

Report failed absolute payoff predictions, calibration and chain confounding, failure of one-parameter models at larger $N$, ZNE limitations, and unresolved anomalies.

# VII. Discussion

*(Consolidated from ten subsections to six.)*

## VII-A. What the Entangler Family Actually Controls

Separate the family's effects on ideal interference, equilibrium status, payoff allocation, graph symmetry, and implementation cost. Interpret the natural-budget and matched-gate controls: mathematical structure effects versus routing and gate-cost effects. Matched gate count is a partial control, not a complete device-noise causal control, and the prose must say so.

## VII-B. Payoff, Equilibrium, and State Quality Are Three Different Claims

Explain why a high cooperative payoff at $N\geq4$ does not imply a self-enforcing equilibrium, and why observable robustness is not state preservation.

## VII-C. Mean Welfare Versus Player-Level Fairness

Discuss payoff range, worst-player payoff, hub-versus-leaf asymmetry, and position-locked disadvantage.

## VII-D. What the Hardware Tests Establish and What the Failures Teach

Summarize the strongest differential and structural hardware conclusions without repeating the full numerical ledger. Discuss reduced noise models, calibration drift, chain dependence, ZNE overshoot, and the greater reliability of within-job differential tests.

## VII-E. Implications for Quantum Mechanism Design

Present possible market and allocation applications as interpretations rather than demonstrated deployments.

## VII-F. Limitations and Future Research

Collect all claim boundaries in one location. Cover continuous strategies, family-optimized strategies, correlated noise (including correlated readout), alternative hardware, larger $N$, fairness-aware objectives, more graph families, and predictive uncertainty.

# VIII. Conclusion

No subsection heads. Two paragraphs: (1) direct, brief answers to the four Introduction questions, each labeled with the evidence level it attained; (2) the closing design principle that an entangler family must be evaluated by cooperative payoff, incentive compatibility, noise resilience, fairness, and physical implementation cost.

## 7. Prose Style Guide

This guide is binding for every drafted subsection. It will be saved as `paper/STYLE-GUIDE.md` during Phase 1 and checked at every review gate.

### 7.1 Voice and tense

- First-person plural ("we define", "we measure"); never passive constructions that hide the agent ("it was decided").
- Present tense for mathematics and standing facts ("the identity implies"); past tense for completed experimental actions ("we executed 12 jobs").
- No hype adjectives: "novel", "remarkable", "groundbreaking", "surprisingly" are banned; let the numbers carry the weight.

### 7.2 Paragraph discipline

- Every paragraph opens with a topic sentence stating its claim; the rest of the paragraph supports only that claim.
- Maximum paragraph length approximately 180 words (about 12 lines in one column).
- No paragraph may contain more than two displayed equations without intervening explanatory prose.
- Every displayed equation is followed within two sentences by a plain-language reading of what it says.

### 7.3 Connective tissue (the fluidity mechanism)

- Every subsection opens by answering, in one sentence, "why does the reader need this now?" — linking back to the question or result that created the need.
- Every subsection closes with a one-sentence hand-off to what comes next.
- Every result subsection in Sections V and VI names the prediction identifier (P1--P8) it tests in its first paragraph.
- Cross-references use semantic phrasing ("the welfare identity, Eq. (7)") not bare pointers ("see (7)").

### 7.4 Terminology and notation

- One name per concept, from `paper/CLAIM-SOURCE-MAP.md`; synonyms are defects.
- Every symbol defined before first use; no symbol redefined with a different meaning. Canonical assignments: $\eta$ depolarizing probability, $s$ ZNE fold scale, $\gamma$ entanglement angle.
- "Entangler family" for the five-way comparison; "graph topology" only for ring, star, complete (Section 3.2).
- $P(0^N)$ is the "all-zero target-state population" (shorthand "target-state population"); "ground-state population" and unsupported "state fidelity" are banned (Section 3.3).
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

The current manuscript's seven figures are data plots only; there is no protocol schematic and no entangler-family diagram, which is why the reader cannot picture the mechanism. Figure work is executed as its own plan after Section III prose is approved, against this specification.

### 8.1 Principles (binding for every figure)

- **One figure, one claim.** Each figure's caption begins with its takeaway as a declarative sentence ("Hardware preserves the cooperative advantage at $N=3$"), then describes panels, then gives provenance. Never a bare label ("Results for $N=3$").
- **Vector only.** All plots regenerated as PDF; the four current PNGs (`advantage_vs_N`, `topology_heatmap`, `advantage_vs_gamma_N4`, `per_player_advantage_star`) are replaced by vector versions from the same pipelines.
- **One visual language.** A single color assignment per entangler family (GHZ, W, ring, star, complete) used identically in every figure; a single marker convention for ideal / simulated / hardware values; colorblind-safe palette; identical axis labels and units for the same quantity everywhere.
- **Column-fit legibility.** Minimum 8 pt effective font in every figure at final size; single-column width by default, `figure*` only for the two wide hardware aggregates.
- **Prediction linkage.** Every results figure states in its caption which prediction (P1--P8) it tests.

### 8.2 Required new figures

- **F1 — Protocol schematic** (new, Section III-C): the EWL pipeline as a circuit-style diagram — initial state, entangler $J_T(\gamma)$, local strategy gates $U_j$, disentangler, measurement, payoff evaluation. This is the figure the current paper most obviously lacks.
- **F2 — Entangler-family gallery** (new, Section III-D): the five entangler families drawn side by side with qubit labels, the graph-topology subset (ring, star, complete) visually distinguished from the global-interpolation families (GHZ, W), hub highlighted in the star, plus per-family two-qubit gate counts. Replaces a paragraph of prose description.

### 8.3 Redesign of existing figures

| Current figure | Disposition |
|---|---|
| `advantage_vs_N.png` | Regenerate as vector; add analytic $3/N$ curve overlay; caption keyed to P1. |
| `topology_heatmap.png` | Regenerate as vector; annotate the exceptional cells (ring $N=4$, star $N=6$) directly on the heatmap; caption keyed to the entangler-family predictions. |
| `advantage_vs_gamma_N4.png` | Regenerate as vector; mark the equilibrium-transition angle; caption keyed to the entanglement-angle prediction. |
| `per_player_advantage_star.png` | Regenerate as vector; show the full payoff vector with hub emphasized; caption keyed to the fairness prediction. |
| `hardware_n3_validation.pdf` | Restructure as a two-panel figure: measured vs predicted distribution; measured vs predicted payoffs (serves VI-B alone). |
| `hardware_scaling.pdf` | Keep as `figure*`; visually separate raw, mitigated, and extrapolated values; caption keyed to the scaling prediction. |
| `hardware_topology.pdf` | Keep as `figure*`; add per-family ideal reference lines; flag ring $N=4$ as undefined-retention explicitly. |

### 8.4 Caption standard

```text
Fig. N. <Takeaway sentence stating the claim.> <Panel description:
what is plotted, axes, error-bar meaning.> <Provenance: simulation
pipeline or device/job reference, and the prediction identifier tested.>
```

## 9. Supporting Appendices

### Appendix A. Gate-Level Circuit Constructions

Detailed family-specific decompositions and native-gate counts.

### Appendix B. Simulation Reproducibility

Parameter grids, artifact locations, software versions, validation checks, and supplementary configuration tables.

### Appendix C. Finite-Round Adaptation Pilot

Exploratory learning-rule results, update-rule sensitivity, and $N=5$ extensions.

### Appendix D. Noise-Model Residuals and Larger-$N$ Diagnostics

Full model residuals, registered judgments, $N=6,7$ diagnostics, ZNE overshoot, and uncertainty limitations.

### Appendix E. Hardware Registration and Provenance

Job identifiers, physical qubits, calibration records, registration artifacts, selection rules, recovery records, and claim-to-artifact provenance.

### Appendix F. Supplementary Player-Level and Topology Tables

Complete payoff vectors, deviation tables, fairness metrics, and family-specific numerical values.

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

### 10.2 Verification standard (strengthened)

Metadata verification alone does not establish that a source supports a claim. `paper/LITERATURE-AUDIT.md` records, for every source:

- BibTeX key, research strand, claim supported, publication, year, peer-review status, DOI/publisher URL (as before);
- **evidence access:** full text / abstract only;
- **locator:** page, section, theorem, figure, or quoted passage that supports the claim;
- **support type:** direct / contextual / criticism;
- **verification notes.**

Sources verified only through an abstract must not support detailed mathematical or methodological claims. **Staging:** the ~18 Section III sources are verified to the full standard before Section III drafting; remaining strands are audited strand-by-strand as their sections are drafted, so the audit does not serialize weeks of reading ahead of all prose.

### 10.3 Data and code availability

- Before submission, the simulation code, hardware raw counts, registration artifacts, and figure-generation pipelines are archived to Zenodo (or equivalent) and assigned a DOI.
- The manuscript carries explicit Data Availability and Code Availability statements citing that DOI.
- The registered-protocol claims in Section VI must be checkable against the archived registration artifacts, not only against Appendix E prose.

## 11. Collaborative Rewrite Process

The manuscript will be rewritten in dependency order, drafting one subsection at a time but **reviewing at five authorized gates**. This gate structure supersedes any per-subsection approval language: the gates are exactly

- **G1** — baseline build, terminology table, style guide, and claim-scope contract;
- **G2** — Section III literature audit;
- **G3** — the first drafted subsection (III-A), as a style-calibration gate: the user corrects voice and density once, early;
- **G4** — the high-stakes III-G incentive-compatibility derivation;
- **G5** — the complete Section III after its flow pass.

Later phases define analogous per-section gates (one per section after its flow pass, plus individual gates for VI-H negative results and any subsection the user flags).

For each subsection draft:

1. agree on the exact purpose and claims;
2. list required definitions and formulas;
3. identify the peer-reviewed literature needed;
4. draft the subsection in accessible language following the style guide (Section 7);
5. verify every mathematical statement;
6. verify every numerical claim against its artifact;
7. check citation support;
8. compile the manuscript;
9. record commands, test results, warnings, page counts, evidence classifications, and approved exceptions in `paper/SECTION-III-EXECUTION-LOG.md` (and analogous logs for later phases).

Recommended rewrite order:

1. TQE manuscript shell migration and canonical entry point;
2. terminology, metric definitions, and style guide;
3. Section III mathematical framework;
4. Section IV analytical predictions;
5. figure redesign (Section 8), which needs the P1--P8 ledger;
6. Section V simulation landscape;
7. Section VI hardware validation;
8. Section II literature synthesis;
9. Section VII discussion;
10. appendices and availability statements;
11. Section I Introduction;
12. Section VIII Conclusion;
13. abstract and keywords last.

## 12. Acceptance Criteria

The content restructure is successful when:

- the manuscript builds from the official TQE journal shell with `paper/qhd.tex` as the single canonical entry point and `paper/README.md` updated to match;
- a mixed technical reader can identify the problem before encountering the formalism;
- every symbol and metric is defined before use, with $\eta$/$s$/$\gamma$ used per the canonical assignment and no symbol defined twice;
- every central mathematical claim is derived in the main text, including the general-$\gamma$ cooperative invariance proposition with proof and regression check;
- proof, simulation, and hardware evidence are labeled distinctly, and every hardware sign/threshold claim passes or fails by the single registered decision rule in III-H;
- the hardware equilibrium claim follows the VI-F evidence rule (six gaps, or the explicitly narrowed Hawk-only claim);
- simulation and hardware subsections follow the same prediction order;
- one subsection has one primary scientific purpose, and no section exceeds the consolidated subsection count in Section 6;
- every drafted section has passed a flow pass against the style guide before approval;
- one figure has one primary scientific claim, every figure follows the Section 8 caption standard, and figures F1 and F2 exist;
- all figures are vector, colorblind-safe, and use the single shared visual language;
- the two advantage metrics are never conflated;
- restricted-menu equilibrium is never described as full-SU(2) equilibrium;
- $P(0^N)$ is named per Section 3.3 everywhere, and "state fidelity" appears only where full-state fidelity is computed;
- the entangler-family / graph-topology vocabulary of Section 3.2 is used consistently, with the normalized interaction-strength control reported;
- mean payoff is never used as a substitute for player-level fairness;
- ideal family effects are distinguished from compiled-circuit effects;
- failed predictions and negative results remain visible;
- secondary operational detail is moved to appendices;
- the bibliography contains more than 50 relevant, verified, peer-reviewed sources meeting the Section 10.2 locator standard;
- the archived-artifact DOI exists and the Data/Code Availability statements cite it;
- `paper/SECTION-III-EXECUTION-LOG.md` (and successors) record every gate decision;
- the final paper fits approximately 16--20 TQE pages without repeated result ledgers;
- Introduction questions, analytical predictions, simulation results, hardware tests, Discussion, and Conclusion align one-to-one.

## 13. Explicit Non-Goals for This Program Phase

This design phase does not:

- rewrite manuscript prose;
- generate figures (figure *specification* is Section 8; figure *execution* is a later plan);
- change scientific claims;
- add unverified citations;
- run new IBM hardware jobs;
- claim unrestricted SU(2) equilibrium;
- optimize a different strategy for each entangler family;
- resolve continuous-strategy or mixed-strategy equilibria;
- treat matched gate count as a complete device-noise causal control.
