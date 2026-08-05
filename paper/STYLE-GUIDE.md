# QHD Manuscript Style Guide

Binding for every drafted paragraph. Source of truth: spec Section 7 in
docs/superpowers/specs/2026-07-31-qhd-content-restructure-design.md.
Checked at every approval gate; violations are review blockers.

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
