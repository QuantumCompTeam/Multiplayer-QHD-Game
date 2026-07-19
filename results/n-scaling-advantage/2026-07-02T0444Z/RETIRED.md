# RETIRED — old payoff convention (V=1000/C=550)

This run used the superseded payoff convention **V=1000, C=550**. It is a
truthful historical record and is retained for provenance, but its payoff
scale is NOT the current convention (V=4, C=3). Do not cite its numbers as
current-convention results.

**Why retired:** bounded config regression. `experiments/config.yaml` shipped
`V: 1000` / `C: 550` defaults between 2026-06-18 (last verified
current-convention run) and 2026-07-02 (first contaminated run). Fixed
2026-07-17 by the item-11 stale-claim audit. Nothing else about this run is
scientifically suspect — only the payoff scale is stale.

**Superseded by:** `results/n-scaling-advantage/2026-07-19T0901Z` — the
current-convention (V=4/C=3, strategy_mode=fixed) advantage map, regenerated
under item 13.

Reference: `docs/findings/2026-07-17-item11-stale-claim-audit.md` (item-13
handoff); `docs/VERIFIED-FACTS.md` F3.
