# Project Status — why the repo looks like this & what's left

**Written:** 2026-07-19 · **For:** Aasa Singh Bhui · **From:** Prithvi
**Scope:** Month-3 end (2026-06-23, commit `bf6818b`) → today (dev @ `304a3bd`)

Read this to understand *why* things are the way they are now and what's left.
Every claim traces to `docs/VERIFIED-FACTS.md` (the ground-truth ledger) or to
a commit hash. Nothing here is from memory.

---

## 1. The one-paragraph answer

The "19 changes" are the **19 numbered items in `ITEMS.md`** — a work index, not
arbitrary churn. They were driven by **20 verified defects** (`G1`–`G20` in
`docs/VERIFIED-FACTS.md`) that a fresh-eyes audit of the repo surfaced in
mid-July. Each item either fixes a defect, lands a finding, or disposes of a
decision. Nothing was renamed or reorganized for taste; every diff traces to a
G-number or a paper requirement. If you remember one thing: **the repo you left
in June had silent rot — stale claims, three competing ways to run the code, an
untrackable results tree, and hardware artifacts that couldn't reproduce
themselves. The last month was paying that down before the paper went out.**

---

## 2. Timeline: what happened, in order

### Phase A — Month-3 close & Month-4 noise (Jun 23 → Jul 5)

| Commit | What | Why |
|---|---|---|
| `bf6818b` | Month-3 hardening | Pinned the topology-sweep test suite, fixed README/pyproject drift. This is the baseline "good" state. |
| `8679e46` | Month-4 noise-analysis spec + TODOS | Opened the noise work (T1–T8). |
| `4beed82`…`cee54bd` | Gate-level entanglers, depolarizing runner, T8 exact W entangler | Built the Month-4 noise machinery. **T8 retired the "approximate W" label** — the W entangler is now exact. |
| `570e1c4` | **T9 adaptation & fairness pilot** | Your fairness line. Result: *independent best response does **not** restore per-player fairness under noise.* This is why item 10 is yours to sign off. |

### Phase B — Hardware (Jul 15 → 17)

| Commit | What | Why |
|---|---|---|
| `c0a141f` | **N=3 GHZ on ibm_fez, advantage 0.9978** | First real-hardware validation. Job `d9br6l66hjac73fg3g7g`. |
| `35f6c87` | N=3,4,5 hardware scaling + mitigation | The scaling result the paper is built on. |
| `7fa978d` | **Pre-register effective-p predictions** | Committed predictions *before* repeat runs. This is the process moat. |
| `17cc1d5`, `13e9bfd` | Repeat-run judge + competing baseline predictors | Locked the scoring rule before data returned. |
| `a936f17` | Repeat batch 2 | N=5 deficit reproduces; N=4 passes the conditional test. |

### Phase C — The audit (Jul 16 → 18)

This is where the "why did everything change" comes from.

| Commit | What | Why |
|---|---|---|
| `124c09d`, `2996528` | **Item 11: repo-wide stale-claim audit** | Found N≥4 Nash claims, robustness qualifiers, **V/C convention mismatches**, and p_eff framing that had drifted. 614 generated "QNE" occurrences marked to retire on regeneration. |
| `2dcad2a` | **`VERIFIED-FACTS.md` created** | The ground-truth ledger. Every number in the repo now traces to file:line. This is *the* reference doc. |
| `9a2b5e9` | Anchored-citation checker | Because 4-of-4 carried-over line citations were silently stale (G13). |
| `ca94831` | Item 16: environment provenance + calibration-at-submit | Hardware artifacts previously recorded *no* python/qiskit version and `dirty:true` (G15/G16) — unreproducible. Now they capture it. |
| `ed43cab`…`5065ab1` | Item 18: CI + N=4/N=5 NE regression guard | No test pinned the N=4/N=5 equilibrium break (G9). Now it does, on GitHub Actions. |

### Phase D — Sweep & paper (Jul 18 → 19)

| Commit | What | Why |
|---|---|---|
| `dff79a4`, `cd5c094` | **Item 17: interpreter-convention sweep** | The big one — see §3. |
| `03d642d` | **Item 13: retire old-convention runs + regenerate advantage map** | The other big one — see §4. |
| `403e29a`…`9dd49fd` | Paper: intro, error-budget, robustness→fairness, conclusion | Your sections are the ones still marked `\todo{Aasa: ...}`. |

---

## 3. Item 17 — the interpreter sweep (the change you'll notice most)

**What you see:** commands that used to read `PYTHONPATH=src python ...` now read
`conda run -n entangled-equilibria python ...`.

**Why.** The audit (A5 in `VERIFIED-FACTS.md`) found **three competing
interpreter conventions documented at once**:

1. `conda run -n entangled-equilibria` — 17 lines / 9 files *(the correct one)*
2. `.venv/bin/python` — 3 lines / 2 files
3. bare `PYTHONPATH=src python` — 25 lines / 13 files

The bare-`python` convention (G10) delegates the interpreter to whatever `PATH`
resolves. On this machine that's **Python 3.9.13 with qiskit 0.45.3**, which
violates the repo's own pins (`pyproject.toml` requires `>=3.10` and
`qiskit==1.3.2`). Under it, `src/` **does not import** — it dies at
`from typing import TypeAlias` (a 3.10 feature). So the README's own quickstart
didn't run.

Compounding it (G4/G5): a stray `.venv-win/` directory carried qiskit 2.2.3,
which `README.md:185` explicitly declares incompatible.

**The disposition (commits `dff79a4` + `cd5c094`):**
- Stripped the `PYTHONPATH=src` prefix from **25 lines across 13 files** → all
  now use the conda env.
- Deleted `.venv-win/` entirely.
- Un-ignored `results/` (G1) and un-tracked `graphify-out/` (G12).
- Repointed the 3 `.sh` helpers to conda.

**Net for you:** the only supported way to run anything is
`conda run -n entangled-equilibria python ...`. That's the env that satisfies
every pin.

---

## 4. Item 13 — the V/C convention & the retired runs (the data change)

**What you see:** 7 directories under `results/n-scaling-advantage/` now carry a
`RETIRED.md`, and the advantage map was regenerated.

**Why.** The audit found the repo had silently run on **two different V/C
conventions** (F1 in `VERIFIED-FACTS.md`):

- **Old:** `V=1000, C=550` — 5 `gamma-sweep/` directories.
- **Live:** `V=4, C=3` — what `src/config.py:35-36` defines and the paper uses.

The 7 `n-scaling-advantage` runs from Jul 2–16 recorded **no V or C key at all**
in their metadata (Group 3, F1), so their convention **cannot be determined from
their own artifacts.** Only the committed run (`2026-06-18T0930Z`) records the
live convention. A stale advantage map could not be traced to a known
convention — a provenance hole.

**The disposition (commit `03d642d`):**
- 7 old-convention n-scaling dirs **retired-with-note** (each gets a
  `RETIRED.md`; `results/README.md` documents them). Not deleted — preserved as
  record, marked not-current.
- Advantage map **regenerated** fixed-mode at `V=4/C=3` →
  `results/n-scaling-advantage/2026-07-19T0901Z`. **This is the figure data the
  paper's `\includegraphics` at `main.tex:199` points at.**
- Gamma-sweep accepted from the same-day pytest regen; 2 stale nash-mode pytest
  artifacts deleted.

**Net for you:** when you write the advantage-map section, the only number set
to cite is `2026-07-19T0901Z`. Don't touch the retired dirs except to read their
`RETIRED.md`.

---

## 5. The other items, one line each

| Item | Status | The why |
|---|---|---|
| 3 | **blocked** | Cross-day repeats, 1 of 3–5 done. Needs a different ibm_fez calibration stamp. |
| 4 | **blocked** | Five-model ranking; auto-accumulates on run 3. |
| 5B | decided | No new noise model before run 3; submit under existing four registered models. |
| 6, 8, 12 | open | Parallel tracks, no scope recorded, not blocking the paper. |
| 9 | open | W-topology hardware + wiring-permutation controls (separates player-4 position into wiring vs hardware). |
| 10 | **you** | T9 learning-rule sign-off. Fairness paragraph hedged "exploratory." |
| 11 | done | Stale-claim audit. |
| 13 | done | §4 above. |
| 14 | open | The paper itself. |
| 15 | open | cp1252 locale; test fix done, phase-2 `.gitattributes` is your call. |
| 16 | done (code) | Env-provenance landed; self-validates on run 3. |
| 17 | done | §3 above. |
| 18 | done | CI + NE regression guard, validated on Actions (512 passed, 3 skipped). |
| 19 | partial | Repo presentation. `results/topology/` now committed; remainder is `results/README` wording + coverage-gap scope. |

---

## 6. What's left — and what's yours

### Blocked on hardware (wait, don't touch)
Items 3, 4, 16-validation — all gate on **run 3**, which needs a fresh ibm_fez
calibration stamp. Nothing to do until that lands.

### Blocked on you (Aasa)

**Item 10 — T9 learning rule.** The pilot (commit `570e1c4`, finding
`docs/findings/2026-07-05-t9-adaptation-fairness.md`) showed independent best
response does **not** restore per-player fairness under noise. The paper's
fairness paragraph is hedged as "exploratory" pending your sign-off on the
learning rule.

**Your sections** — the `\todo{Aasa: ...}` markers in `main.tex`:
1. **Payoff tensor definition** — k Hawks among N (`main.tex:172`,
   `docs/formulae.md`).
2. **Zero-noise landscape / advantage map** — figure + gamma-sweep
   (`main.tex:199`). **Data is ready** at
   `results/n-scaling-advantage/2026-07-19T0901Z/plots/` (`advantage_vs_N.png`,
   `topology_heatmap.png`); only the `\includegraphics` + caption assembly is
   left.

Plus one untagged `\todo` that was scoped to you in discussion:
3. **Month-4 noise findings port** — the corrected README §9 p* table
   (`main.tex:205`, marked `\todo{Port README \S9 Month-4 findings...}`; note
   this one is *not* tagged `Aasa:` in the source — confirm before you claim
   it, or it defaults to Prithvi).

If you stay out of the picture until the first draft exists, these become
Prithvi's after that draft.

### Open, unblocked, not yours unless you want them
- **Item 19** — `results/README` wording + coverage-gap scope.
- **Item 15 phase-2** — decide the `.gitattributes` line-ending policy.
- **Items 6/8/12** — scope, none started.

---

## 7. How to verify any of this yourself

```
# The ground-truth ledger — start here
docs/VERIFIED-FACTS.md        # G1–G20 defects + A–F evidence sections

# The work index
ITEMS.md                      # the "19 changes," each with status + pointer

# The one-page re-orient
docs/STATUS.md                # cold-read first

# The run commands, post-sweep
conda run -n entangled-equilibria python <script>
```

Every number in the paper traces to a `results/` artifact named in a `%`-comment
beside it in `main.tex`, and to `VERIFIED-FACTS.md`. If a claim ever disagrees
with the repo, the repo wins — file it as a new G-defect.
