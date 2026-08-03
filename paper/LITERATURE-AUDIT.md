# QHD Literature Audit

Task 4 consolidation of three read-only research lanes (quantum/entanglement,
classical/network game theory, noise/mitigation) plus the audit of the 8
pre-existing `paper/references.bib` entries. This file supersedes the four
source lane documents as the single point of truth for Gate G2 review; the
lane documents remain on disk as the underlying research trail and are not
modified by this consolidation.

Source lanes consolidated (read-only inputs, unmodified by this file):
- `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-4-existing-bib-audit.md`
- `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-4-quantum-entanglement-sources.md`
- `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-4-classical-network-sources.md`
- `.superpowers/sdd/2026-07-31-qhd-mathematical-framework-rewrite/task-4-noise-mitigation-sources.md`

## Column semantics

- **Evidence access:** `full text` / `abstract only`.
- **Locator:** page, section, theorem, figure, or quoted passage that supports the claim.
- **Support type:** `direct` / `contextual` / `criticism`.
- Sources with `abstract only` access must not support detailed mathematical or methodological claims. Every `abstract only` row below is restricted to a definitional/contextual claim only; none is used for an equation, theorem, or a quantitative methodological result.

---

## CRITICAL FINDING: `nation2021` is misattributed in the current manuscript

`paper/qhd.tex` lines 211 and 654 currently cite `nation2021` (Nation, Kang,
Sundaresan, Gambetta, "Scalable Mitigation of Measurement Errors on Quantum
Computers," PRX Quantum 2, 040326, 2021 — the M3 method) for **"tensored
confusion-matrix inversion (constrained least squares)."**

**This is incorrect.** M3's own abstract states its method "does not form the
full assignment matrix, or its inverse," and instead uses a matrix-free
preconditioned iterative solver operating in the subspace of observed
bitstrings. M3 is the scalable *alternative to* full tensored matrix
inversion — it exists specifically because tensored inversion becomes
intractable at scale. The description "tensored confusion-matrix inversion,
constrained least squares" matches the **prior art that M3 replaces**, not
M3 itself.

**Verified correct attribution (full text, both papers):**

- **`maciejewski2020`** (Maciejewski, Zimborás, Oszmaniec, *Quantum* 4, 257,
  2020) is the **direct** source for both halves of the claim:
  tensor-product ("tensored") confusion/assignment-matrix model for
  multi-qubit readout noise (Sec. 3.3.2, Eq. 15: `Λ^(K) = ⊗ᵢ Λᵢ`), and
  constrained-least-squares reconstruction of the corrected probability
  vector (Sec. 4.3, Eq. 25: `p*_exp = argmin_{pᵢ≥0, Σpᵢ=1} ‖Λ⁻¹p_exp,est − p‖²`).
- **`bravyi2021pra`** (Bravyi, Sheldon, Kandala, McKay, Gambetta, *Phys. Rev.
  A* 103, 042605, 2021) is **contextual** support for the tensored noise-model
  assumption (Sec. III, Eq. 5) and **direct** support for a separate strand,
  observable-specific error resilience (Sec. II, Eq. 2: mitigation applied to
  one observable's expectation value via matrix inversion + quasi-probability
  sampling, not a full-distribution constrained-least-squares reconstruction).
- **`nation2021`** should be re-cited, same BibTeX entry, for the corrected
  claim: a scalable, matrix-free alternative that explicitly avoids forming
  the full/tensored assignment matrix or its inverse. It must **not** be cited
  for "tensored confusion-matrix inversion (constrained least squares)."

**Action required (out of scope for this task):** the Section III prose that
will replace `paper/qhd.tex` lines 211 and 654 must either (a) cite
`maciejewski2020` (direct) + `bravyi2021pra` (contextual) for a
tensored-inversion/constrained-least-squares method description and reserve
`nation2021` for a separate sentence about the scalable matrix-free
alternative, or (b) if the project's own mitigation code actually runs
M3/mthree, reword the claim to match `nation2021`'s real method and cite
`maciejewski2020`/`bravyi2021pra` only for tensored-noise-model background.
This audit does not resolve which of (a)/(b) is correct — that requires
checking `src/` mitigation code, which is out of scope for Task 4. **No edit
to `paper/qhd.tex` was made by this task**; this is a flag for Section III
drafting.

---

## Discrepancy note: `eisert1999` evidence access reconciled across lanes

The existing-bibliography lane obtained full text of the arXiv preprint
(quant-ph/9806088) via PDF-to-text extraction and recorded a specific locator
(Eq. 7 and the Nash-equilibrium/Pareto-optimal sentence following Fig. 3, PRL
p. 3078). The independent quantum-entanglement lane's later attempt to
re-fetch the same PDF failed (encoded/compressed stream, no legible body
text) and fell back to `abstract only`. Both lanes confirm identical
Crossref metadata (title/authors/journal/volume/pages/DOI). Because the
existing-bibliography lane's extraction produced a specific, checkable
equation/quote locator rather than only the abstract, that lane's `full
text` verification is retained as authoritative for the row below; the
abstract-only fallback is recorded here for transparency but does not
override it.

---

## Audit table (27 unique verified sources after deduplication)

| BibTeX key | Research strand | Claim supported | Publication | Year | Peer reviewed | DOI or publisher URL | Evidence access | Locator | Support type | Verification status | Notes |
|---|---|---|---|---:|---|---|---|---|---|---|---|
| `khan2025` | Quantum advantage in trading (existing entry) | Demonstrates a quantum Nash-equilibrium advantage for a two-player trading (Chicken) model; separately reports an ion-trap hardware run predominantly for n=3–6 traders on a Prisoner's-Dilemma-style variant | Khan, Linke, Than, Baron, "Quantum Advantage in Trading: A Game-Theoretic Approach," *Quantum Economics and Finance* 2(1):40–51 | 2025 | yes (SAGE) | 10.1177/29767032251333418 | full text (arXiv 2501.17189) | Sec. 2.1/Fig. 1 caption (2-player Chicken model); Sec. 4.1 (payoff 33 vs. 11); Sec. 6 (ion-trap hardware, n=3–6, plus a passing 2-trader mixed-strategy mention) | direct | verified — locator caveat | Existing bib entry, re-confirmed. `qhd.tex` phrase "two-player trading game...on ion-trap hardware" should be checked: the *theoretical* model is 2-player, the *hardware* run is chiefly 3–6 players. |
| `eisert1999` | Eisert-Wilkens-Lewenstein quantum games (existing entry) | EWL quantization embeds SU(2) strategies and entangles the register before play; the maximally entangled point (γ=π/2) yields a strategy simultaneously Nash equilibrium and Pareto optimal | Eisert, Wilkens, Lewenstein, "Quantum Games and Quantum Strategies," *Physical Review Letters* 83(15):3077–3080 | 1999 | yes (APS) | 10.1103/PhysRevLett.83.3077 | full text (arXiv quant-ph/9806088, PDF-text extraction) | Eq. (7), Ĵ=exp(−iγD̂⊗D̂/2); Nash-equilibrium/Pareto-optimal sentence, paragraph after Fig. 3, PRL p. 3078 right column | direct | verified | Two-player operator only (N=2); cite only for the EWL protocol concept, not an N-player generalization. See discrepancy note above re: a second lane's abstract-only fallback. |
| `benjamin2001` | Multiplayer quantum games (existing entry) | N-player generalization of quantum games via entangling operator Ĵ=(1/√2)(Î^⊗N+iF̂^⊗N); identifies a "pure/coherent equilibrium" unique to ≥3-player quantum settings, where shared entanglement acts as a binding contract preventing profitable unilateral deviation (no classical or 2-player-quantum analogue) | Benjamin, Hayden, "Multiplayer quantum games," *Physical Review A* 64(3):030301 | 2001 | yes (APS, Rapid Communication) | 10.1103/PhysRevA.64.030301 | full text (arXiv quant-ph/0007038) | Entangling gate near Fig. 1(b); worked N=3,4 examples; "pure, or coherent equilibria" definition and contract-framing sentence in the section introducing S_U vs. S_TCP strategy sets | direct (multiplayer-equilibrium concept); contextual only for the joint "maximal entanglement at γ=π/2" phrasing | verified — locator caveat | No γ symbol or π/2 value appears in this paper (fixed maximal entangler, not continuously parameterized) — the γ=π/2 notation is carried by `chappell2012`, not this paper. No fully general closed-form 2^N payoff-tensor formula located (only N=3,4 worked cases). |
| `chappell2012` | GHZ and W multipartite entanglement / quantum-game equilibrium scope (existing entry) | Compares GHZ-type (entanglement angle θ, Eq. 4) and W-type (Eq. 5) entanglement in N-player quantum games in an EPR/simulation setting; no Hawk-Dove payoff matrix and no hardware section anywhere in the paper | Chappell, Iqbal, Abbott, "N-Player Quantum Games in an EPR Setting," *PLOS ONE* 7(5):e36404 | 2012 | yes | 10.1371/journal.pone.0036404 | full text (PLOS ONE, open access) | Eq. (4) GHZ state; Eq. (5) W state; Results subsections "GHZ-type state" / "W entangled state" | direct | verified | Games analysed: Prisoner's Dilemma, Chicken, minority game. Entanglement parameter is named θ, not γ; worth a symbol-translation footnote if Section III leans on this source for the γ=π/2 wording. |
| `varsamis2025` | N-player hardware scalability (existing entry) | Studied N-player entanglement operators and payoff-computation scalability on IBM hardware (Von Neumann entropy metric across entangling angles, simulator + real IBM system) | Varsamis et al., "Analysis of the Effect of Entanglement Operators and the Scalability of Players' Payoff Computation in N-Player Quantum Games," *Advanced Quantum Technologies* 8(11):e00375 | 2025 | yes (Wiley) | 10.1002/qute.202500375 | abstract only (Wiley full text HTTP 402; no open preprint located) | Abstract | contextual | verified (metadata); access-limited | Must not be used for a specific equation/fidelity/circuit-depth claim until full text is obtained; current high-level usage is compliant. |
| `temme2017` | Zero-noise extrapolation and local gate folding (existing entry) | Introduces zero-noise extrapolation via noise rescaling and Richardson extrapolation (theoretical origin of ZNE; term "gate folding" is not used verbatim) | Temme, Bravyi, Gambetta, "Error Mitigation for Short-Depth Quantum Circuits," *Physical Review Letters* 119(18):180509 | 2017 | yes (APS) | 10.1103/PhysRevLett.119.180509 | full text (arXiv 1612.02058) | Eq. (5) noise rescaling; Eqs. (3)–(4) Richardson extrapolation; Supplemental Material Sec. A.2 | contextual | verified | Continuous-time noise-rescaling method, not literally discrete unitary "gate folding" — see `giurgicatiron2020` for the literal digital gate/layer-folding terminology. |
| `kandala2019` | Zero-noise extrapolation, hardware demonstration (existing entry) | Applies pulse-stretch ZNE together with readout-error mitigation on real superconducting hardware | Kandala, Temme, Córcoles, Mezzacapo, Chow, Gambetta, "Error mitigation extends the computational reach of a noisy quantum processor," *Nature* 567(7749):491–495 | 2019 | yes | 10.1038/s41586-019-1040-7 | full text (arXiv 1805.04492) | Main text, 2nd paragraph; Eqs. (1)–(2); Fig. 1(c) | direct | verified | Pulse-stretching implementation, not discrete gate folding. |
| `nation2021` | Measurement-error mitigation — scalable, matrix-free alternative (existing entry; **claim corrected**) | Method explicitly does not form the full/tensored assignment matrix or its inverse; matrix-free preconditioned iterative solver in the subspace of observed bitstrings | Nation, Kang, Sundaresan, Gambetta, "Scalable Mitigation of Measurement Errors on Quantum Computers," *PRX Quantum* 2(4):040326 | 2021 | yes (APS, open access) | 10.1103/PRXQuantum.2.040326 | full text (arXiv 2108.12518) | Abstract ("does not form the full assignment matrix, or its inverse"; "matrix-free preconditioned iterative-solution method"); Sec. II "Subspace reduction," Eqs. (3)–(4) | direct (for the matrix-free/scalable claim only) | verified — **currently misattributed in `qhd.tex` lines 211, 654; see Critical Finding above** | Do not cite for tensored-inversion/constrained-least-squares — that claim belongs to `maciejewski2020` (direct) with `bravyi2021pra` (contextual). |
| `benjamin2001comment` | Quantum-game equilibrium scope and criticism | Direct rebuttal of EWL: extending the strategy space from EWL's restricted two-parameter set to the full SU(2) makes the claimed Nash equilibrium disappear (an ideal counter-strategy always exists); "no Nash equilibrium of the kind suggested by Eisert et al." in the full deterministic-quantum-strategy space | Benjamin, Hayden, "Comment on 'Quantum Games and Quantum Strategies'," *Physical Review Letters* 87(6):069801 | 2001 | yes (APS) | 10.1103/PhysRevLett.87.069801 | full text (arXiv quant-ph/0003036) | Counter-strategy construction ("An ideal counter strategy to Q̂ ... is iσ_x"); concluding sentence | criticism | verified | Maps directly onto `CLAIM-SOURCE-MAP.md`'s restricted-menu-equilibrium vs. full-SU(2)-equilibrium distinction. |
| `vanenk2002classical` | Quantum-game equilibrium scope and criticism | The "quantum" equilibrium of a quantized game is not intrinsically quantum-mechanical: the move set/payoff structure used to reach it can be reproduced by an equivalent classical/extended-strategy game — the quantum solution solves a different, enlarged game rather than uniquely resolving the original one | van Enk, Pike, "Classical rules in quantum games," *Physical Review A* 66(2):024306 | 2002 | yes (APS) | 10.1103/PhysRevA.66.024306 | full text (arXiv quant-ph/0203133) | "Neither the above description of the move Q nor the payout matrix is quantum mechanical..."; "Games...are defined by their rules, and if you change the rules, you change the game." | criticism | verified | — |
| `duer2000three` | GHZ and W multipartite entanglement | Under SLOCC, three-qubit pure states fall into exactly two inequivalent genuine-tripartite-entanglement classes (GHZ, W), not interconvertible even probabilistically; W uniquely maximizes residual bipartite entanglement after tracing out any one qubit | Dür, Vidal, Cirac, "Three qubits can be entangled in two inequivalent ways," *Physical Review A* 62(6):062314 | 2000 | yes (APS) | 10.1103/PhysRevA.62.062314 | full text (arXiv quant-ph/0005115) | Sec. III.B (product-term SLOCC invariant); Sec. III.D, Eq. (37) (3-tangle); Sec. IV.B (least entangled pair) | direct | verified | Foundational GHZ-vs-W classification underlying the manuscript's entangler-family terminology. |
| `hein2004multiparty` | Graph states and graph automorphisms in quantum networks | Graph states are multiparticle entangled states tied to a mathematical graph; local-unitary equivalence is explicitly distinguished from graph-isomorphism/automorphism equivalence (vertex permutations mapping edges to edges) | Hein, Eisert, Briegel, "Multiparty entanglement in graph states," *Physical Review A* 69(6):062311 | 2004 | yes (APS) | 10.1103/PhysRevA.69.062311 | full text (arXiv quant-ph/0307130) | Sec. II.2, note after Eq. (14); Abstract | direct | verified | Supports the graph-topology/entangler-family framing (ring/star/complete) in `CLAIM-SOURCE-MAP.md`. |
| `hansenne2022symmetries` | Graph states and graph automorphisms / permutation symmetry in quantum networks | Permutation symmetry of a multiparty state constrains network generation: a permutationally symmetric N-party state is producible from an (N−1)-partite-or-smaller-source network iff it is fully separable; no graph state on up to 12 vertices is producible from a bipartite-only-source network | Hansenne, Xu, Kraft, Gühne, "Symmetries in quantum networks lead to no-go theorems for entanglement distribution and to verification techniques," *Nature Communications* 13:496 | 2022 | yes | 10.1038/s41467-022-28006-3 | full text (open access) | Observation 2 (network no-go theorem); Observation 1 + "Certifying network links" (local-complementation inequality) | direct | verified | Strongest source for the permutation-symmetry/graph-automorphism half of the strand. |
| `marinatto2000quantum` | EWL quantum games / multiplayer quantum games (contextual scope limiter) | Introduces an alternative "density-matrix"/probabilistic quantization scheme, formally distinct from EWL's unitary parametrization; explicitly restricted to two players — contains no N-player content | Marinatto, Weber, "A quantum approach to static games of complete information," *Physics Letters A* 272(5-6):291–303 | 2000 | yes | 10.1016/S0375-9601(00)00441-2 | full text (arXiv quant-ph/0004081) | Sec. 6, Eq. (6.2); Sec. 4 Hilbert-space construction (2-player only) | contextual | verified | Must **not** be cited for any N-player claim — the paper itself has no N>2 content. |
| `maynardsmith1973` | Classical Hawk-Dove and evolutionary games | Canonical two-strategy (Hawk/Dove) symmetric conflict game and the ESS concept, payoffs parameterized by resource value V and injury cost C | Maynard Smith, Price, "The Logic of Animal Conflict," *Nature* 246(5427):15–18 | 1973 | yes | 10.1038/246015a0 | abstract only (paywalled; scanned-image mirrors with no text layer) | Abstract; pp. 15–18 (whole article, no page-specific quote confirmed) | contextual | verified (bibliographic fields only) | SCOPE FLAG: this paper's own mixed-ESS result requires C>V; this manuscript's convention (V=4, C=3, i.e. V>C) means the interior mixed ESS does **not** apply. Cite only for the 2-strategy structure/ESS concept, never for an equilibrium-value claim. |
| `broom1997` | Multiplayer/N-player Hawk-Dove payoff formulations | General N-player symmetric matrix-game framework (of which 2-strategy conflict games are an instance); multiplayer equilibrium behavior is structurally more complex than the 2-player case | Broom, Cannings, Vickers, "Multi-player matrix games," *Bulletin of Mathematical Biology* 59(5):931–952 | 1997 | yes | 10.1007/BF02460000 | abstract only (Springer/ScienceDirect/repository all unreachable) | Abstract; pp. 931–952 | contextual | verified (bibliographic fields only) | Does not itself name Hawk-Dove in the located abstract — supports "a general N-player matrix-game framework exists," not a Hawk-Dove-specific result. |
| `wood2015` | Multiplayer/N-player Hawk-Dove payoff formulations | Formulates and analyzes an explicit n-player Hawk-Dove game (payoff-irrelevant player labels) studying which conventions/property-rights outcomes are evolutionarily stable among many players | Wood, "Informal property rights as stable conventions in hawk-dove games with many players," *Journal of Evolutionary Economics* 25(4):849–873 | 2015 | yes | 10.1007/s00191-015-0412-x | abstract only (Springer paywalled; ResearchGate mirror 403) | Abstract; pp. 849–873 | contextual | verified (bibliographic fields only) | Most directly on-point "N-player Hawk-Dove" source found. Cannot confirm from the abstract whether results require the classical V<C mixed-ESS regime — do not cite for any equilibrium-value claim; safe only for "an N-player Hawk-Dove payoff formulation exists in the literature." |
| `nash1951` | Strict dominance, pure-strategy equilibrium, and welfare framing (extension: supports Section III's classical game-theoretic foundation, not one of the 12 brief-listed strands) | Establishes the equilibrium-point (Nash equilibrium) concept for finite games and proves existence via mixed strategies; pure-strategy equilibria are the relevant special case for a game where one strategy strictly dominates (this manuscript's V>C Hawk-Dove regime) | Nash, "Non-Cooperative Games," *Annals of Mathematics* 54(2):286–295 | 1951 | yes | 10.2307/1969529 | full text | pp. 286–287 (equilibrium-point statement/definition, existence theorem) | direct | verified | Does not itself use the term "strict dominance" (paired conceptually with `dawes1980`); supports the pure-strategy Hawk-Hawk equilibrium description. |
| `dawes1980` | Strict dominance, pure-strategy equilibrium, and welfare framing (extension) | Defines a "social dilemma": each player has a strictly dominant strategy that, if adopted by all, leaves every player worse off than mutual cooperation — the canonical welfare framing for a Pareto-dominated strict-dominance equilibrium | Dawes, "Social Dilemmas," *Annual Review of Psychology* 31:169–193 | 1980 | yes | 10.1146/annurev.ps.31.020180.001125 | abstract only (Annual Reviews paywalled; definition cross-confirmed via three independent secondary citations) | p. 169 (opening definition of "social dilemma") | contextual | verified | Matches this paper's V>C structure exactly (mutual-Hawk Pareto-dominated by mutual-Dove); a conceptual/welfare claim, not a derived equation, so abstract-only access is adequate. |
| `galeotti2010` | Network games and position-dependent fairness | Bayesian network-game framework in which each player's equilibrium action and payoff depend on their network position (degree/connectivity) under strategic substitutes/complements | Galeotti, Goyal, Jackson, Vega-Redondo, Yariv, "Network Games," *Review of Economic Studies* 77(1):218–244 | 2010 | yes | 10.1111/j.1467-937X.2009.00570.x | abstract only (Oxford Academic 403; EUI working-paper mirror too large to fetch) | Abstract | contextual | verified | — |
| `teixeira2021` | Network games and position-dependent fairness | In an N-player network game, a player's network position (degree) determines their strategic role and payoff; degree-based role assignment (e.g. low-degree players as proposers) increases fairness of outcomes relative to random assignment | Teixeira, Santos, Francisco, Santos, "Eliciting Fairness in N-Player Network Games through Degree-Based Role Assignment," *Complexity* 2021:6851477 | 2021 | yes | 10.1155/2021/6851477 | full text (open-access PDF; exact page/section not resolved by the fetch tool) | Article body — paraphrased passage on degree-based role assignment (not a confirmed verbatim quote) | direct | verified — quote is a paraphrase, not verbatim | Ties "N-player" + "network position" + "fairness" precisely to this strand. Recommend hand-verifying the exact sentence/page before quoting directly in manuscript prose. |
| `georgopoulos2021` | Depolarizing channels and quantum noise | Symmetric depolarizing channel (Kraus operators, uniform X/Y/Z error probability) as a standard model for NISQ gate infidelity, alongside SPAM and thermal-relaxation channels | Georgopoulos, Emary, Zuliani, "Modelling and simulating the noisy behaviour of near-term quantum computers," *Physical Review A* 104(6):062432 | 2021 | yes (APS) | 10.1103/PhysRevA.104.062432 | full text (arXiv 2101.02109) | Sec. II.1, Eq. (1) | direct | verified | Also models SPAM and thermal relaxation as separate channels. |
| `maciejewski2020` | Measurement-error mitigation — tensored confusion-matrix inversion, constrained least squares | (a) Tensor-product ("tensored") confusion/assignment matrix for independent per-qubit readout noise; (b) corrected probability vector via constrained least squares (nearest valid probability vector to the unconstrained matrix-inverted estimate) | Maciejewski, Zimborás, Oszmaniec, "Mitigation of Readout Noise in Near-Term Quantum Devices by Classical Post-Processing Based on Detector Tomography," *Quantum* 4:257 | 2020 | yes (open access) | 10.22331/q-2020-04-24-257 | full text | Sec. 3.3.2, Eq. (15); Sec. 4.3, Eq. (25) | direct | verified | **The correct primary source for the claim currently misattributed to `nation2021`** — see Critical Finding above. Also evaluates cross-qubit readout correlations (Sec. 6.2.2, Table 2). |
| `bravyi2021pra` | Measurement-error mitigation (contextual: tensor-product model) AND observable-specific error resilience (direct) | (a) Tensor-product assignment-matrix model for multiqubit readout noise; (b) mitigation applied directly to a specific observable's expectation value via matrix inversion + quasi-probability sampling, not full-distribution reconstruction | Bravyi, Sheldon, Kandala, McKay, Gambetta, "Mitigating measurement errors in multiqubit experiments," *Physical Review A* 103(4):042605 | 2021 | yes (APS) | 10.1103/PhysRevA.103.042605 | full text (arXiv 2006.14044) | Sec. III, Eq. (5); Sec. II, Eq. (2) | direct (observable-specific strand); contextual (tensored-model strand) | verified | Do NOT cite for constrained least squares — correction method here is direct inversion + quasi-probability sampling, not a constrained-least-squares projection. |
| `giurgicatiron2020` | Zero-noise extrapolation and local gate folding | Local ("gate/layer") folding scales noise by repeating a chosen gate subset in place, distinct from global circuit folding (which repeats the whole circuit) | Giurgica-Tiron, Hindy, LaRose, Mari, Zeng, "Digital zero noise extrapolation for quantum error mitigation," 2020 IEEE QCE, pp. 306–316 | 2020 | yes (IEEE, peer-reviewed proceedings) | 10.1109/QCE49297.2020.00045 | full text (arXiv 2005.10921) | Sec. II-A1, Eq. (1) global folding; Sec. II-A2, Eq. (5) local folding rule | direct | verified | The paper's own terminology, "gate (or layer) folding," matches the manuscript's phrase literally — unlike `temme2017`/`kandala2019`. |
| `cross2019` | Circuit compilation/routing cost effects relevant to NISQ topology-family comparisons (extension, not one of the 12 brief-listed strands) | Mapping a logical circuit onto NISQ hardware connectivity requires a transpiler SWAP-insertion routing pass; measured circuit quality (heavy-output probability) depends on this compilation overhead | Cross, Bishop, Sheldon, Nation, Gambetta, "Validating quantum computers using randomized model circuits," *Physical Review A* 100(3):032328 | 2019 | yes (APS) | 10.1103/PhysRevA.100.032328 | full text (arXiv 1811.12926) | Main text (SWAP-mapping discussion); Appendix A; Table 2 | direct | verified | Introduces quantum volume; supports comparing routing overhead across different topology families on real hardware. |
| `li2019sabre` | Circuit compilation/routing cost effects relevant to NISQ topology-family comparisons (extension) | Two-qubit gates are restricted to physically coupled qubit pairs; incompatible logical circuits require inserted SWAP gates (3 CNOTs each) whose count depends on circuit/topology structure; the SABRE heuristic substantially reduces this routing overhead versus the prior best heuristic | Li, Ding, Xie, "Tackling the Qubit Mapping Problem for NISQ-Era Quantum Devices," ASPLOS 2019, pp. 1001–1014 | 2019 | yes (ACM, peer-reviewed proceedings) | 10.1145/3297858.3304023 | full text (arXiv 1809.02573) | Sec. III.A, Fig. 3; Abstract | direct | verified | Confirms routing/SWAP overhead is topology- and circuit-structure dependent — relevant to comparing GHZ/W/ring/star/complete entangler families on real hardware connectivity. |

---

## Threshold accounting (brief requires ≥18 verified Section III sources "at the full locator standard")

- **Total unique verified sources after deduplication: 27** (8 pre-existing bib entries + 19 new).
- **Full-text evidence access (the full locator standard): 21** of 27.
- **Abstract-only evidence access (restricted to contextual/definitional claims only): 6** of 27 — `varsamis2025`, `maynardsmith1973`, `broom1997`, `wood2015`, `dawes1980`, `galeotti2010`.
- Of the 21 full-text sources, **18 map directly onto the 12 strands named in the brief's Step 3 list**; the remaining 3 full-text sources (`nash1951`, `cross2019`, `li2019sabre`) are additional, verified, on-topic sources for Section III that extend beyond the literal 12-strand list (classical-equilibrium foundations and hardware-topology routing cost, respectively) surfaced by the research lanes.
- **Threshold met**: 18 full-locator-standard sources map onto the brief's exact strand list, with 3 further full-text sources as margin, and no abstract-only source was used to pad the count. No shortfall to disclose.

## Deduplication log

- `eisert1999` (existing key) absorbs the quantum-entanglement lane's `eisert1999quantum` proposal — same DOI, same paper. Existing key retained; see discrepancy note above.
- `benjamin2001` (existing key) absorbs the quantum-entanglement lane's `benjamin2001multiplayer` proposal — same DOI, same paper. Existing key retained; locators merged.
- `temme2017`, `kandala2019`, `nation2021` (existing keys) were independently re-verified by the noise-mitigation lane against the same DOIs with no metadata discrepancies; existing keys retained, `nation2021`'s claim text corrected per the Critical Finding above.
- No other cross-lane duplicates were found.

## BibTeX-key uniqueness check

See `paper/SECTION-III-EXECUTION-LOG.md`, Task 4 entry, for the exact command and output.

## Gate G2

This source list (27 rows, strand/evidence-access/locator visible above) requires explicit user approval or removal before any row is cited in Section III manuscript prose. `paper/qhd.tex` was not edited by this task.
