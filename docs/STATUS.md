# Project Status — one page (re-orient in 60 s)

**Last updated:** 2026-07-19 (dev @ dff79a4, pushed to fork). Read this first when returning cold.

## The one question
Does the two-player quantum Hawk–Dove advantage survive real **N-player**
networks — topology, noise, hardware? **Answer: yes, with sharper edges.**

## The through-line (the actual result)
- **N=3:** GHZ cooperative profile is a genuine symmetric pure Nash equilibrium.
  Reproduced on ibm_fez at **0.9978 of ideal** (job `d9br6l66hjac73fg3g7g`).
- **N=4,5:** the equilibrium *breaks* (a unilateral Hawk deviation profits), but
  the cooperative payoff keeps a large measurable advantage (0.739/0.584 of ideal
  0.75/0.60). Framed as a **fixed cooperative protocol**, not an equilibrium (G19).
- **The mechanism:** the mean payoff is *first-order insensitive to single
  bit-flips* — a property of the payoff geometry, not the device. That is why the
  advantage decays several times slower than state fidelity.
- **Scaling:** set by per-two-qubit-gate decay, not a fitted depolarizing strength.
  In the registered five-model comparison, cz-exponential retention leads both runs.

## Why a reviewer trusts it (the process is the moat)
- **Pre-registered predictions** committed before hardware runs, then judged.
- **Registered five-model comparison** that let a simpler baseline beat the
  depolarizing fit — reported honestly.
- **VERIFIED-FACTS.md:** every number traces to file:line.
- Honesty notes inside the artifacts themselves.

## State of the paper (item 14)
Prithvi's prose **drafted**: intro, N=3 error-budget, robustness→fairness link,
conclusion. 13 `\todo`s remain = figures, captions, and **Aasa's sections**
(payoff tensor, zero-noise landscape, Month-4 port).

## The 3 things that finish it
1. **Item 3 — cross-day hardware repeats.** 1 of 3–5 calibration days. *Blocked
   on ibm_fez recalibrating.* Run 3 must land on a genuinely different stamp
   (item 16's submit-time stamp now records it).
2. **Aasa's paper sections** (3 of the 13 `\todo`s).
3. **Item 13 — retire-vs-regenerate the 7 uncommitted V/C runs** (needed for the
   advantage-map figure).

## Open decisions (yours)
- Item 15 phase-2 `.gitattributes` · Item 6 / 8 / 12 / 19 (scope, none started).

## Waiting on a rerun
- Item 16 (env-block capture) self-validates on run 3's artifact.
- Item 4 (five-model ranking) accumulates per repeat.

## Item 17 status
Interpreter-convention sweep **done** (G2, G3). Remaining: G1, G4, G5, G10, G12
— tracking/provenance dispositions (G12 → item 19), not sweep lines.

## Key files
- Paper: `paper/main.tex` · status/owners: `paper/README.md`
- Work queue: `ITEMS.md` (index) · `TODOS.md` (deferred detail)
- Provenance: `docs/VERIFIED-FACTS.md` · findings: `docs/findings/`
- Preregistrations: `results/hardware-scaling/preregistration*.json`
