# Project Status — one page (re-orient in 60 s)

**Last updated:** 2026-07-19 (dev @ 03d642d, pushed fork). Read first when returning cold.

## One question

Does two-player quantum Hawk–Dove advantage survive real **N-player**
networks — topology, noise, hardware? **Answer: yes, sharper edges.**

## Through-line (the actual result)

- **N=3:** GHZ cooperative profile is a genuine symmetric pure Nash equilibrium.
  Reproduced on ibm_fez at **0.9978 ideal** (job `d9br6l66hjac73fg3g7g`).
- **N=4,5:** equilibrium *breaks* (a unilateral Hawk deviation profits), but the
  cooperative payoff keeps a large measurable advantage (0.739/0.584 ideal
  0.75/0.60). Framed as a **fixed cooperative protocol**, not an equilibrium (G19).
- **The mechanism:** mean payoff is *first-order insensitive to single
  bit-flips* — a property of payoff geometry, not the device. That is why
  advantage decays ~7× slower than state fidelity.
- **Scaling:** set per-two-qubit-gate decay, not fitted depolarizing strength.
  In the registered five-model comparison, cz-exponential retention leads runs.

## Why a reviewer trusts the process (the moat)

- **Pre-registered predictions** committed before hardware runs, judged after.
- **Registered five-model comparison** — let a simpler baseline beat the
  depolarizing fit; reported honestly.
- **VERIFIED-FACTS.md:** every number traces to file:line.
- Honesty notes inside artifacts themselves.

## State of the paper (item 14)

Prithvi's prose **drafted**: intro, N=3 error-budget, robustness→fairness link,
conclusion. ~12 `\todo`s remain, most assigned to Aasa (payoff tensor,
zero-noise landscape, Month-4 port). **Head of the line:** the advantage-map
figure — data is ready (`results/n-scaling-advantage/2026-07-19T0901Z/plots/
advantage_vs_N.png` + `topology_heatmap.png`) but `main.tex:199` still needs
the `\includegraphics` + caption.

## Hardware runs (blocked — wait, don't act)

- **Item 3** (cross-day repeats): 1 of 3–5 done. Run 3 needs a different
  ibm_fez calibration stamp; item 16's `calibration_at_submit.json` records it.
- **Item 4** (five-model ranking) auto-accumulates on run 3.
- **Item 16** (env-block capture) self-validates on run 3's artifact.

## Recently closed (2026-07-19, commits cd5c094 + 03d642d)

- **Item 13** — 7 old-convention n-scaling dirs retired-with-note (`RETIRED.md`
  each + `results/README`); advantage map regenerated fixed-mode V=4/C=3
  (`2026-07-19T0901Z`); gamma-sweep accepted from same-day pytest regen; 2
  nash-mode pytest artifacts deleted; hardware figures point at the 2-run
  aggregate. Resolves F3.
- **Item 17** — all 5 G-defects disposed: `results/` un-ignored (G1),
  `graphify-out/` untracked (G12), `.venv-win/` deleted (G4+G5), conda
  convention swept (G10, PYTHONPATH=src prefix stripped from 25 lines), 3
  `.sh` helpers repointed to conda. Resolves G1–G5, G10, G12.
- **Item 18** — CI + N=4/N=5 NE regression guard validated on Actions
  (run 29670675020: 512 passed, 3 skipped). Resolves G9.

## Open, unblocked

- **Item 19** (repo presentation) — partially done 2026-07-19 (`results/
  topology/` committed, the force-add fix). Remainder: `results/README`
  wording + coverage-gap scope.
- **Decisions (yours):** item 15 phase-2 `.gitattributes`. Items 6 / 8 / 12
  closed 2026-07-19 — never scoped, nothing traces to them, not blocking.
- **Item 9** (W-topology hardware + wiring-permutation controls) — open.

## Waiting on Aasa (out of the picture until first draft)

- **Item 10** (T9 learning rule) — sign-off; fairness paragraph hedged as
  exploratory.
- Aasa's 3 paper sections: payoff tensor, zero-noise landscape, Month-4 port.
  If he stays out, these become Prithvi's after the first draft exists.

## Key files

- Paper: `paper/main.tex` · status/owners: `paper/README.md`
- Work queue: `ITEMS.md` (index) · `TODOS.md` (deferred detail)
- Provenance: `docs/VERIFIED-FACTS.md` · findings: `docs/findings/`
- Preregistrations: `results/hardware-scaling/preregistration*.json`
