# Topology hardware feasibility on ibm_fez: which cells are runnable

**Date:** 2026-07-25
**Source:** `conda run -n entangled-equilibria python experiments/hardware_topology.py --report`
(script at commit `f94ee35`, run against the live ibm_fez coupling map;
network read only, no job submitted, no quota spent)

Plan Task 3. This decides the cell list for the topology batch from *measured*
routed gate counts rather than from pre-routing counts, because ibm_fez is
heavy-hex (max degree 3, girth 12) and pre-routing counts do not price routing.

## Measured table

Pinned set `[20, 21, 22, 23, 24]` (sum cz err 0.0133, sum readout err 0.0245).
Transpiled at `optimization_level=3`, `seed_transpiler=7`.

| topology | N | routed cz | depth | verdict |
| --- | --- | --- | --- | --- |
| ghz | 3 | 6 | 24 | ok |
| ghz | 4 | 9 | 29 | ok |
| ghz | 5 | 14 | 49 | ok |
| ring | 3 | 10 | 31 | ok |
| ring | 4 | 20 | 41 | ok |
| ring | 5 | 28 | 56 | ok |
| star | 3 | 5 | 23 | ok |
| star | 4 | 9 | 31 | ok |
| star | 5 | 17 | 56 | ok |
| fully-connected | 3 | 10 | 31 | ok |
| fully-connected | 4 | 31 | 83 | ok |
| fully-connected | 5 | 67 | 144 | over cz budget 60 — excluded |
| w | 3 | 42 | 141 | expensive — included by explicit decision |
| w | 4 | 107 | 287 | over cz budget 60 — excluded |
| w | 5 | 219 | 556 | over cz budget 60 — excluded |

Reference anchor printed by the report: the committed N=3 GHZ validation ran at
6 cz and kept 95.5% of shots in `|000>`
(`results/hardware-n3/2026-07-16T013912Z`).

## What the measurement corrected

`docs/STATUS.md` (2026-07-25 head-of-line) and this plan's Task 3 preamble both
warned that ring and fully-connected would be expensive because heavy-hex has
no native triangle and no cycle below N=12. **The measurement does not support
that for N<=5.** Ring routes to 10/20/28 cz and fully-connected to 10/31 cz at
N=3/4. At these sizes the transpiler closes the cycle with a small number of
SWAPs instead of routing around a 12-cycle, so the girth argument — correct as
a statement about the coupling graph — overstates the cost at the sizes this
paper actually runs. This is exactly why the plan required the cell list to come
from `--report` rather than from pre-routing counts.

The genuine casualty is W: 42 cz at N=3 (7x GHZ N=3) and past budget at N=4,5.
W is not a stabilizer state and does not compile to a short Clifford ladder the
way GHZ, ring, star and fully-connected do here.

## Cells selected for the batch

12 cells x 3 folds (1/3/5) + 2 calibration pubs = **38 pubs**.

| topology | N included | N excluded and why |
| --- | --- | --- |
| ghz | 3, 4, 5 | — |
| ring | 3, 4, 5 | — |
| star | 3, 4, 5 | — |
| fully-connected | 3, 4 | N=5: 67 routed cz, over the 60 budget |
| w | 3 | N=4: 107 cz; N=5: 219 cz — both over the 60 budget |

No cell is carried forward silently. The paper can state which topology x N
cells were attempted and why each remaining one was not.

### W N=3 is included deliberately

At 42 cz it is the most expensive cell in the batch, and its fold-5 pub is 210
cz. It is included anyway because every other topology in the batch is
GHZ-class: without W, the "topology" axis compares four members of one
entanglement class and the paper's topology claim is weaker than it reads.
W N=3 is the only cell that makes the axis a real axis.

It is included at the full 1/3/5 fold ladder rather than a truncated one. A
per-cell fold ladder would require changing `build_batch`'s global `folds`
argument, and the batch's uniform-series design is what makes all five
experiment axes one record type. Changing that architecture to accommodate one
cell is the wrong trade. If W N=3 fold-5 is at the noise floor, the Task 6
rehearsal on the reduced device noise model will show it **before any quota is
spent**, and it can be excluded then with evidence rather than by arithmetic.

## Fold interaction with the cz budget (semantics, deliberately unchanged)

`check_isa_on_set(isa_u, allowed, CZ_BUDGET)` is applied to the **unfolded**
circuit in `build_batch`, so a cell that passes at 31 cz submits a 155-cz pub at
fold 5. This is intended and is left as is:

- The budget's stated purpose in plan Task 2 is "routing did not blow the gate
  budget". A pre-fold check measures precisely that.
- Folding is deliberate noise amplification for ZNE, not routing failure.
  Applying the ceiling post-fold would conflate the two and would silently drop
  the high-fold points that the extrapolation needs.

Fold-multiplied cz for the selected cells:

| cell | fold 1 | fold 3 | fold 5 |
| --- | --- | --- | --- |
| star N=3 | 5 | 15 | 25 |
| ghz N=3 | 6 | 18 | 30 |
| ghz N=4 | 9 | 27 | 45 |
| star N=4 | 9 | 27 | 45 |
| ring N=3 | 10 | 30 | 50 |
| fully-connected N=3 | 10 | 30 | 50 |
| ghz N=5 | 14 | 42 | 70 |
| star N=5 | 17 | 51 | 85 |
| ring N=4 | 20 | 60 | 100 |
| ring N=5 | 28 | 84 | 140 |
| fully-connected N=4 | 31 | 93 | 155 |
| w N=3 | 42 | 126 | 210 |

**These are not fidelity predictions.** Extrapolating the 6-cz -> 95.5% anchor
would put ring N=5 fold-5 near 34% ground-state probability, but that is
`P(|0..0>)`, and this project's central mechanism finding is that mean payoff is
first-order insensitive to single bit-flips, so advantage decays roughly 7x
slower than fidelity (`docs/STATUS.md`, "Through-line"). Cells that look dead by
fidelity may retain measurable advantage. No cell is excluded on this table; the
rehearsal decides.

## Note for cross-run comparability

The pinned set today is `[20, 21, 22, 23, 24]`. Run 2 of the scaling series used
`[59, 75, 74, 73, 79]` (`docs/findings/2026-07-17-run2-repeat-judgment.md`).
The chain selector picks by live calibration, so the pinned set moves between
calibration days. Topology comparisons *within* one batch are controlled (same
pinned set across all cells, by construction in `find_pinned_set`); comparisons
*across* batches on different days are not, and the Task 9 repeats must be read
with that in mind.

## Status

Plan Task 3 complete. `experiments/hardware_topology.py` was not modified — the
`--report` mode landed in `f94ee35` and this run only exercised it.

Next gated step is Task 6 (rehearsal, no quota), then Task 7 (freeze
predictions, commit) before Task 8 submits anything.
