**Entangled Equilibria: manuscript review and journal-strengthening plan — 7 September 2026**

This review reads the complete canonical `paper/qhd.tex`, the claim ledger and literature audit, the Task 12 checkpoint, and the relevant payoff, strategy, circuit, noise, and hardware code. The manuscript is partway through its governed rewrite; findings about later sections concern the prose currently present, not a finished rewrite. No canonical manuscript, production implementation, bibliography, registration, or historical result was changed. The only executable addition is the sibling exploratory probe and its JSON output. No IBM jobs were submitted.

User constraint: approximately **600 seconds of IBM quantum usage remaining**. Usable backend and chain length remain to be established from account access and current calibration. The plan does not assume ibm_fez is still accessible or that all 600 seconds should be spent immediately.

**Assessment**

There is a credible experimental quantum-engineering paper here. The strengths are reproducible circuit constructions, negative results, matched implementation controls, per-player accounting, and prospective tests that can fail. The manuscript is not yet submission-ready: several headline conclusions exceed the evidence, and the main payoff-retention metric becomes less discriminating as N grows. More qubits alone would not resolve those issues.

The most promising thesis is: **cooperative welfare, unilateral incentive compatibility, and implementation fairness scale differently in multiplayer EWL games; phase selection can repair a restricted incentive failure, while unrestricted deviations reveal the mechanism's boundary.** The engineering and benchmarking emphasis fits the published [TQE scope](https://tqe.ieee.org/subject-areas/). Venue suitability is an assessment, not an acceptance prediction.

**1. Findings to resolve before further hardware use**

| Priority | Finding in current manuscript/code | Required change or evidence |
|---|---|---|
| Critical | Introduction/Related Work repeatedly position Khan et al. as two-player hardware work. The local literature audit already flags the problem. | Their Sections 5–6 include multiplayer trading and ion-trap experiments with N=3–6 on a different Prisoner's-Dilemma payoff model. Compare payoff rule, strategy restrictions, entangler families, hardware controls, and endpoints explicitly. |
| Critical | High analytic-baseline retention is presented as evidence of scalable useful quantum cooperation. | Include the exact uniform-random comparator, exploitability, fairness, and payoff sensitivity below. High mean retention alone cannot establish quantum-resource benefit. |
| Critical | The hardware section infers a full `{D,H,Q_N}` equilibrium from only unilateral Hawk circuits. `experiments/hardware_topology.py:DEVIATION_PROFILES` contains HQQ, QHQ, QQH. | Call the old result a Hawk-deviation test. Measure every player's Dove deviation too before claiming an empirical restricted-menu equilibrium under noise. |
| Major | The uniqueness implied by “Q scales as pi/N” overlooks other cooperative phase branches, including the identity. | Present `pi/N` as the chosen lowest positive branch, then analyze other branches as a separately named strategy family. |
| Major | `strategy_opt.py` calls local multistart optimization a global Nash certificate and claims vertex transitivity makes symmetric optimization exact. | A local optimizer gives a lower bound on maximum exploitability. Symmetry does not guarantee a globally optimal symmetric pure profile or exclude asymmetric equilibria. Use the quadratic-form oracle below; keep symmetric candidate searches explicitly constrained. |
| Major | Noise-induced ring circuit-order asymmetry and noiseless star hub/leaf asymmetry are merged into one causal conclusion. | Separate graph-role asymmetry, synthesis-order asymmetry, and physical-qubit heterogeneity. A star wiring control does not establish the cause of the ring's noise effect. |
| Major | Low all-zero population in ring/star is described as a damaged state despite their ideal outputs generally not being all-zero. | Compare each circuit with its own ideal distribution/state. Define target and fidelity convention explicitly. |
| Major | Later claims imply trusted mediation is eliminated. | EWL includes common preparation and a joint final J-dagger/readout; centralized execution also enforces the strategy menu. Document that trust and access model. No distributed market mechanism or security result has been demonstrated. |
| Major | Normalized interaction budget is defined in III-D but not actually tested. | Run the equal-raw-angle and equal-summed-angle controls separately from matched compiled gate-count controls. Neither equalizes every physical resource. |
| Major | The W-family restricted D/H circuit game is compared with classical terminology even though it can differ from the original classical action game at nonzero gamma. | Explicitly test classical embedding profile by profile. GHZ and the XX graph factors commute with local X actions; the specified W generator generally does not. Keep its circuit-relative comparator distinct from the original classical game. |
| Major | Hardware uncertainty remains limited by chain-matched calibration replication; N=6–7 remains unrepeated. | Prioritize fixed-chain repetitions and propagate raw-shot, calibration, and mitigation/fit uncertainty. Model misspecification is separate from shot uncertainty. |
| Minor | Abstract says all twelve topology cells have 97.9–99.6% retention, but ring N=4 has zero ideal advantage and undefined percentage. | Say eleven nonzero-baseline cells; report the ring cell separately. |
| Minor | Documentation/workflow states Qiskit 2.x changes the RXX sign. | IBM's [v1.2](https://quantum.cloud.ibm.com/docs/en/api/qiskit/1.2/qiskit.circuit.library.RXXGate) and [v2.0](https://eu-de.quantum.cloud.ibm.com/docs/en/api/qiskit/2.0/qiskit.circuit.library.RXXGate) documentation use the same negative sign. Preserve pins for reproducibility; do not justify them with an unverified convention change. |

The relevant prior work is [Khan et al., 2025, Sections 5–6](https://journals.sagepub.com/doi/full/10.1177/29767032251333418). The correction narrows the novelty claim; it does not erase the present project's implementation controls or incentive/fairness comparison.

On fidelity: under the squared fidelity convention, fidelity to a *specified pure output target* `|0^N>` is exactly `<0^N|rho|0^N>`. Full tomography is not necessary for that target overlap. Population does not certify fidelity to an intermediate GHZ state, coherences of an arbitrary target, or entanglement. The ledger's blanket “population is not fidelity” language should be refined through the manuscript workflow rather than treated as a physical theorem.

**2. A concrete new direction: cooperative phase branches**

These are review-derived results checked numerically against the repository, not preregistered hardware findings and not a claim of priority over the literature.

Define `Q_(N,m) = diag(exp(i alpha), exp(-i alpha))`, with `alpha=m*pi/N`. For any integer m and any gamma, both GHZ branches acquire `(-1)^m`, so

`J_GHZ† Q_(N,m)^(tensor N) J_GHZ |0^N> = (-1)^m |0^N>`.

Thus every such branch pays `V/N`. The existing `Q_N` is m=1, not the only cooperative phase. m=0 is Dove and demonstrates why cooperative output alone is insufficient.

For one deviating player, let `t = sin²(gamma) sin²(alpha)`. Direct evaluation gives

`pi_j(H,Q_-j) = V(1-t)` and `pi_j(D,Q_-j) = V/N - (C/N)t`.

Consequently, for V>0 and C>0, this branch is a restricted `{D,H,Q_(N,m)}` equilibrium exactly when

`sin²(gamma) sin²(alpha) >= 1 - 1/N`.

At maximal entanglement choose `m=floor(N/2)` and call the resulting phase `Qstar_N`. For even N, alpha=pi/2 and the Hawk payoff is zero. For odd N, alpha=pi/2-pi/(2N), and the Hawk payoff is `V sin²(pi/(2N)) < V/N`. The inequality follows for odd N>=3 from `sin(x)<x` and `pi²/(4N²)<1/N`. Dove also pays strictly less, since t>0. This establishes an ideal strict restricted-menu equilibrium for **every N>=2**. Mixtures over that same finite menu cannot improve on its best pure deviation, by linearity of expected payoff.

| N | Existing alpha/pi | Candidate alpha/pi | Cooperative payoff | Existing H payoff | Candidate H payoff | Candidate D payoff |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 1/3 | 1/3 | 1.333333 | 1.000000 | 1.000000 | 0.583333 |
| 4 | 1/4 | 1/2 | 1.000000 | 2.000000 | 0.000000 | 0.250000 |
| 5 | 1/5 | 2/5 | 0.800000 | 2.618034 | 0.381966 | 0.257295 |
| 6 | 1/6 | 1/2 | 0.666667 | 3.000000 | 0.000000 | 0.166667 |
| 7 | 1/7 | 3/7 | 0.571429 | 3.246980 | 0.198062 | 0.164078 |

This changes the interpretation of the old N>=4 result: **that particular phase branch fails**, rather than GHZ cooperation being inherently restricted to three players. Preserve the old result and its name. Add the new strategy explicitly; do not silently redefine `q_strategy(N)` or relabel existing hardware data.

The limitation is equally exact. Against any cooperative phase branch, the permitted full-SU(2) gate `U(pi,0,-alpha)` produces the outcome where the deviator alone is Hawk, with probability one, for every gamma. It pays V, giving gain `V(1-1/N)`. Neither the old nor the candidate phase profile is a full-SU(2) equilibrium. This does **not** rule out other pure or mixed equilibria of the broader game. The known strategy-space issue is contextualized by [Benjamin and Hayden's comment](https://arxiv.org/abs/quant-ph/0003036).

Two scaling limits remain even for the repaired restricted profile. Its raw incentive margin shrinks with N. Also its entanglement threshold approaches pi/2: for even N, `gamma_c=arccos(1/sqrt(N))`. Thus an all-N ideal existence result is not uniform noise robustness. For phase offsets delta_j from the cooperative branch, `p(1^N)=sin²(gamma) sin²(sum_j delta_j)`. A shared systematic offset accumulates as N*delta; independent zero-mean offsets accumulate differently. Add those sensitivity curves, rather than only depolarizing curves.

Verification: the sibling probe made **342 dense-oracle evaluations**, covering arbitrary strategy profiles and every m=0,...,N-1 for N=2,...,7 at gamma=0, 0.31*pi, pi/2. Largest phase-formula payoff discrepancy was **3.997e-15**. Values beyond this checked range follow the derivation, not larger hardware experiments. Literature novelty of the branch selection remains to be audited; compare [Koh, Kumar and Goh's multiplayer EWL analysis](https://arxiv.org/abs/2409.05708), which treats a different volunteer payoff rule, as well as existing multiplayer phase strategies.

**3. Make the robustness claim informative**

The manuscript's exact identity gives

`Delta_ana = (C/N)[1-p(1^N)]`, so `R_ana = Delta_ana/(C/N) = 1-p(1^N)`.

For independent uniform random bits, `R_ana=1-2^(-N)`: 87.5%, 93.75%, 96.875%, 98.4375%, and **99.21875%** at N=3,...,7. This classical randomization is not an equilibrium of the original dominance game. It is an essential diagnostic showing that near-perfect mean retention is not evidence of coherent cooperation, entanglement, or a computational advantage. Symmetry also makes its expected player payoffs equal, so adding the player floor alone does not replace incentive tests.

The payoff is insensitive to **all output error patterns with 1 through N-1 Hawks**, not merely one-bit flips. For independent final bit flips with probability epsilon from `|0^N>`, retention is `1-epsilon^N` while target population is `(1-epsilon)^N`. This is an output-channel calculation; a single fault inside the circuit can propagate to all N bits. Do not claim Nth-order protection against arbitrary gate noise.

Run a separately labeled sensitivity game that retains both endpoint payoffs but penalizes partial conflicts. For `ell in [0,1]`, define total loss

`L_ell(k)=C[(1-ell) 1_(k=N) + ell*k(k-1)/(N(N-1))]`.

Keep all-Dove at V/N, and for k>0 give each Hawk `(V-L_ell(k))/k` and each Dove zero. ell=0 is exactly the current game. ell=1 distributes cost by the fraction of Hawk pairs. V>C still ensures strict Hawk dominance in the classical game, so the analytic all-Hawk comparator remains `(V-C)/N`. The N=2 game is unchanged throughout this sensitivity family.

Compute ell=0, 0.25, 0.5, 1 from **existing raw outcome counts**. Recompute all metrics and, where claimed, equilibria for the altered payoff rule. Do not derive new payoff uncertainties from old scalar error bars. Resample counts and re-run mitigation/estimation. Treat this as retrospective sensitivity analysis. Under independent final flips the normalized retention becomes `1-(1-ell)epsilon^N-ell*epsilon²`; the uniform comparator at ell=1 is 75% for every N. This exposes exactly which robustness comes from the all-Hawk-only penalty. It is a sensitivity model, not a validated economic model.

Primary reporting should include raw per-player payoff vectors, simultaneous confidence bounds on both deviation gaps, normalized maximum regret, all-Hawk probability, the full Hawk-count histogram, and each family's own ideal-target comparison. Also report raw values alongside normalized values: the ideal per-player analytic gap is C/N and tends to zero.

**4. Demonstrate scalability without claiming more physical qubits than were used**

| Meaning of scalability | Proposed evidence | Honest boundary |
|---|---|---|
| Mathematical | All-N phase-branch and incentive-threshold derivations | Ideal restricted strategy model |
| Classical evaluation | N=8,16,32,64,128 benchmarks using compact GHZ/MPS evaluation | Simulation, not an N-qubit hardware demonstration |
| Physical execution | Repeated N=3–7 data, plus a larger N only if justified by runtime and routing | Native simultaneous players remain limited by usable physical qubits |
| Statistical | Shots and calibration repetitions required for a specified normalized regret/fairness precision | Fixed shots do not establish arbitrary-N precision |
| Protocol | Document preparation, player operations, joint decoding, menu enforcement, and trust | A centralized experiment is not a distributed trading network |

Current bottlenecks are concrete: dense J matrices in `src/circuits/n_player.py` use O(4^N) storage, `_payoff_matrix` in `src/game/payoffs.py` stores O(N*2^N), full profile enumeration grows as 3^N, density matrices use O(4^N), and `tensored_confusion` explicitly materializes a 2^N by 2^N assignment matrix. Increasing a configuration limit alone will not solve these.

For checking **one candidate** in `{D,H,Q}`, only `1+2N` profile evaluations are required, not enumeration of 3^N profiles. That shortcut does not enumerate all equilibria or compute a noisy circuit-relative comparator. Retain exhaustive search at small N; report analytic-baseline comparisons separately for large-N candidate checks.

The noiseless GHZ output has an especially useful exact representation. Put `A=tensor_j U_j|0>` and `B=tensor_j U_j|1>`, with c=cos(gamma/2), s=sin(gamma/2). Then

`psi_out = c² A + i*s*c B - i*s*c X^(tensor N) A + s² X^(tensor N) B`.

It is a sum of at most **four product states**, even for arbitrary non-identical local gates. Hence its Schmidt rank across every cut is at most four and it admits an exact MPS with bond dimension at most four. This is a direct derivation, independently checked against the dense oracle. It also rules out presenting this ideal GHZ evaluation problem as evidence of computational quantum speedup.

A production compact evaluator can contract the four branches directly. Compute p(0^N), p(1^N), and overlap products without a full distribution. For exact per-player rewards, use Hawk-count generating polynomials; equivalently `pi_j=(V/N)p(0^N)+V*E[1_(x_j=1)/k]-(C/N)p(1^N)`, where the middle term is zero at k=0. Branch-pair polynomial contractions yield polynomial work. The probe currently materializes small statevectors; it is a verification tool, **not yet the compact large-N implementation**.

For other families, benchmark the existing elementary circuits using MPS with measured bond dimensions, truncation error checks, runtime, and peak memory. Do not promise the GHZ bound for W or dense graph families or for arbitrary noisy circuits. Aer documents its [MPS method](https://qiskit.github.io/qiskit-aer/tutorials/7_matrix_product_state_method.html). Use noise trajectories with confidence intervals where density matrices become infeasible; label the resulting approximation.

For measurements, stream payoffs from observed bitstrings instead of constructing the complete probability table. Under independent assignment errors, the all-Hawk projector can be corrected with a product of per-qubit inverse-assignment weights; this avoids the dense matrix but can increase estimator variance and relies on that readout model. Calibration correlations need checks.

Circuit cutting is an optional *small feasibility experiment*. The [Qiskit cutting documentation](https://qiskit.github.io/qiskit-addon-cutting/explanation/) defines sampling overhead as `(sum |a_i|)^2`; independently cutting K CNOTs with the standard decomposition costs a factor `9^K`. Three such cuts already imply 729-fold variance overhead. Prefer a one- or two-cut comparison only if its actual statistical cost fits the reserve. Report a reconstructed observable, not an N-player state physically coexisting on fewer qubits.

Measurement/reset reuse is conditional on circuit causal structure, as in [DeCross et al.](https://arxiv.org/abs/2210.08039). The final EWL inverse generally couples player wires again. A valid reuse compilation must preserve the declared input/output and strategy-access model; early measurement cannot simply discard needed coherence. Symmetric-subspace compression similarly does not automatically preserve independent player actions. These are secondary directions, not the recommended main paper upgrade.

**5. Replace heuristic best-response certificates**

For fixed opponents, fixed pre/post channels, and one local gate occurrence, write `U(q)=q0 I+i(q1 X+q2 Y+q3 Z)`, with real unit vector q in R^4. The deviator's payoff is `q^T M_j q` for a real symmetric 4x4 matrix. Construct it with ten evaluations: four coordinate vectors and six normalized pair sums. Its largest eigenvalue gives the global best-response payoff; a maximizing eigenvector gives a witness gate. The general quadratic-form approach has precedent in [Landsburg's analysis](https://arxiv.org/abs/1110.1351); this implementation would adapt it to this project's player-payoff and fixed-channel oracle.

Return maximum gain, witness, numerical tolerance, and reconstruction residual. The probe checks 150 random unit quaternions across N=2–7 with maximum discrepancy 1.776e-15, and verifies the maximizing witnesses. This certifies a response to a fixed profile, not the global search for an equilibrium profile. Under hardware sampling, reconstruct M with confidence bounds and validate the selected witness on held-out measurements; a raw maximum eigenvalue of noisy estimates is biased upward.

The fixed-channel qualification matters: strategy-dependent transpilation, gate omission, pulse durations, or calibration response can break a single quadratic description of the *implemented noisy* strategy family. Freeze a common strategy-layer template and validate it before applying this certificate to noisy simulations. Arbitrary CPTP deviations, ancillas, coalitions, and adaptive multi-round strategies remain outside SU(2).

**6. Proposed use of the 600-second hardware budget**

IBM measures usage by QPU lock time, including relevant overhead, not solely circuit duration or queue waiting. Inspect estimates and consumed usage as documented in [Workload usage](https://quantum.cloud.ibm.com/docs/en/guides/estimate-job-run-time). The numbers below are planning ceilings, not guaranteed job runtimes. Validate runtime options against the installed runtime version; distinguish batch lifetime from charged execution usage.

| Allocation | Ceiling | Purpose |
|---|---:|---|
| Pilot | 60 s | Verify candidate phases, both deviations, and one unrestricted witness on a pinned chain; calibrate execution-cost estimates |
| Confirmatory epochs | 300 s total | Target three chain-matched calibration epochs, approximately 100 s each; reduce the design if estimates exceed this |
| Focused controls | 60 s | Circuit-order versus physical-placement comparison, or selected angle/phase-error controls |
| Reserve | 180 s | Failed jobs, a marginal endpoint, or one additional repeat; do not pre-spend |

Default confirmatory grid: GHZ N=3,4,5,6,7, on prefixes of one seven-qubit chain. Each epoch includes:

- Candidate cooperation and every player's H and D deviations: `sum_(N=3..7)(1+2N)=55` circuits.
- Old m=1 cooperation and one preregistered H witness for N=4,5,6,7: 8 circuits. One profitable deviation is sufficient to refute that profile.
- One preregistered unrestricted counter-strategy position per N: 5 circuits.
- Two tensor-readout calibration circuits: 2 circuits. This estimates independent readout errors, not full correlated readout.

Total: **70 circuits per epoch**, initially budgeted at 4096 shots each (286,720 shots). Use pilot/device-model power analysis to set the final shot allocation **before confirmation**. Avoid automatic ZNE on all 70 circuits: it triples circuit variants, adds fit assumptions, and does not replace better incentive measurements. Selected ZNE can be secondary.

The core phase comparison uses explicitly different restricted menus, `{D,H,Q_N}` and `{D,H,Qstar_N}`. If the main claim uses the common menu `{D,H,Q_N,Qstar_N}`, add every player's old-Q deviation against the new profile for N=4–7: 22 circuits, bringing the epoch to **92**. All phase-only alternatives are nonprofitable ideally, but that fact alone does not certify them on noisy hardware. If estimates do not fit, reduce N coverage to 3,4,5,7 or the prespecified secondary controls; retain both primary deviation types.

Primary acceptance should be finite-tolerance incentive compatibility: an upper simultaneous confidence bound on normalized maximum gain is at most a preregistered epsilon. Also report strict positive gap evidence where lower simultaneous bounds exceed zero. Set epsilon by scientific relevance and power analysis, not after seeing data. Bootstrap complete shot distributions, share the resampled cooperative endpoint across deviations, propagate calibration uncertainty, and account for the maximum across players/tests. List individual calibration epochs; three epochs are still limited evidence, not a reliable tail model of arbitrary device drift.

Before each submission: validate new strategies against the small-N dense oracle; freeze topology, gamma, chain, qubit ordering, gate template, transpiler seed and options, shots, metrics, and tests; record submission calibration; run the complete analysis on noiseless and device-model dress rehearsals; estimate usage; register and commit the specification before the confirmatory data. Record pilot data as pilot. If the selected chain is unavailable, stop or register an amended experiment before collecting data, rather than silently changing it. Credentials belong in the local IBM account configuration, not in a report or chat.

The hardware budget is best spent on **counterfactual strategy measurements and repeatability**, not an isolated N=10 point. If a larger point is later added, gate-level reference checks and scalable observable checks must replace exponential full-operator comparisons only under an explicit, tested validation contract. Current small-N safety checks remain intact.

**7. Implementation order and deliverables**

| Order | Work package / proposed files | Completion criterion |
|---|---|---|
| 1 | Review corrections and novelty matrix in a sidecar; then integrate at the existing rewrite gates | Every contribution distinguished from Khan, Benjamin–Hayden, Chappell, Varsamis, and Koh; hardware H-only claim corrected |
| 2 | `src/game/phase_branches.py`, branch-sweep script and independent formula tests | Old `q_strategy` unchanged; all-N proof reviewed; old/new restricted gaps and full-SU(2) witness agree with dense results |
| 3 | `src/game/best_response.py` using quaternion quadratic forms | Matrix reconstruction, maximizing witness, symmetry caveats, noisy-template restrictions checked; heuristic certification wording removed |
| 4 | `scripts/payoff_sensitivity.py` reanalyzing saved counts | ell-grid results, exact uniform baseline, all-player intervals, calibration-aware resampling; altered-game results separate |
| 5 | `src/game/observable_payoffs.py`, compact GHZ evaluator, `scripts/scalability_benchmark.py` | Dense overlap checks through N=7/8; N=16–128 timing/memory table without allocating full probabilities; no universal MPS scalability claim |
| 6 | Interaction-budget and schedule/placement controls using existing scripts | Same unitary under order variants, separate graph-role and gate-order effects, no equivalence claims from similar rates alone |
| 7 | Parameter-aware hardware manifest and judge built on existing hardware helpers | Offline complete dry run; concrete pub/shot/time report; frozen registration; repeatable recovery; then pilot and confirmatory execution |
| 8 | Manuscript synthesis and final evidence audit | Abstract, main text, figures, tables, claim map, and conclusion use the same estimands and the same evidence scope |

A reasonable division between the two authors is mathematical/game-theory work (branches, best responses, payoff sensitivity) and circuits/hardware work (compact execution, compilation controls, calibration epochs), with mutual review of the new theorem and preregistration. This is a proposed division of work, not delegated execution.

**8. Proposed limitations prose for author review**

“We study a specified N-player allocation game at V=4 and C=3, where Hawk strictly dominates Dove. The conflict cost in the primary model is incurred only at the all-Hawk outcome. Consequently, mean payoff depends only on that outcome's probability, and high analytic-baseline retention need not imply coherent cooperation, equitable outcomes, or strategic stability. Uniform independent randomization also approaches maximal normalized retention as N grows. The trading interpretations are illustrative; we do not validate an economic market model or establish superiority over classical mechanisms with comparable mediation and enforcement resources.

“Our equilibrium statements concern explicitly stated strategy menus. The GHZ cooperative profiles considered here admit profitable unrestricted SU(2) deviations; hardware Hawk-deviation tests alone do not certify resistance to Dove or other deviations. Centralized preparation, joint decoding, and enforcement of the permitted operation set remain protocol assumptions. We do not establish security against arbitrary channels, ancillary systems, coalitions, or adaptive players.

“Entangler-family comparisons depend on the chosen generators, interpolation strengths, synthesis, routing, and noise placement. In particular, the W construction is one specified operator, and graph-role asymmetry is distinct from implementation-induced asymmetry. Depolarizing noise is a controlled model rather than a complete description of the device. Mitigation introduces model dependence and uncertainty, and extrapolated values may fall outside physical payoff bounds.

“Native hardware results cover only the executed player counts and calibration epochs. Their uncertainty includes finite sampling and limited replication, and registered low-dimensional noise models did not extrapolate reliably. Compact simulation and all-N ideal derivations extend theoretical analysis rather than the number of simultaneously realized hardware players. Per-player ideal gains and incentive margins decrease with player count; scalable welfare evaluation therefore does not by itself establish scalable incentive certification.”

This text is a proposed sidecar draft, not inserted into the gated manuscript. Update its empirical phrasing after new experiments, preserving the original evidential status of historical results.

**9. Manuscript presentation**

The current paper repeats the same noise narrative, adaptation pilot, and registration history across Results, “Why the Advantage Outlives the State,” Novelty, and Conclusion. Keep one clear account of each result; move job details and the exploratory learning pilot to supplementary material where possible. The rewritten framework is careful but often explains the same displayed equation several times. A journal paper benefits more from a compact theorem, its scope, and a decisive test than from repeated signposting.

Suggested main figures: (1) protocol and family definitions; (2) old/new phase incentive boundary with unrestricted witness; (3) resource-normalized topology/fairness controls; (4) payoff-model sensitivity and the random comparator; (5) registered hardware deviations across calibration epochs; (6) classical evaluation cost and hardware resource scaling. The present advantage-vs-N plot and heatmap substantially duplicate one another.

A possible title after validation is **“Incentive Compatibility and Observable Robustness in Multiplayer Quantum Games: Theory and Hardware Tests.”** The extension should earn that title through the completed evidence. Neither the phase result nor a new manuscript title should be advertised as unprecedented until the expanded literature comparison is complete.
