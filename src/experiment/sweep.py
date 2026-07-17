"""Run the parameter sweep by calling game.nash.compute_advantage per cell.

Each cell is evaluated independently and wrapped so that one failing cell (an
unimplemented/unknown topology or an unexpected error) never aborts the whole
run — it is recorded with a status and message instead. Asymmetric topologies
(e.g. star) are fully supported: compute_advantage returns per-player vectors and
a `symmetric` flag, which the report surfaces.

This module adds NO game theory; compute_advantage is the single source of truth.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from circuits.noise import build_ewl_circuit_noisy
from experiment.config import Cell
from experiment.topology_registry import canonical, resolve
from game.nash import ProbFn, compute_advantage
from game.strategy_opt import optimal_strategy

# Soft per-cell ceiling (seconds) for the nash optimizer, so no single cell pegs
# the CPU unbounded. Exceeding it returns the best candidate found so far.
NASH_TIME_BUDGET = 45.0

# Cell status values, in order of "things went well" -> "did not run".
STATUS_OK = "ok"
STATUS_NOT_IMPLEMENTED = "not-implemented"
STATUS_ERROR = "error"


@dataclass
class CellResult:
    """Outcome of evaluating one Cell.

    On success (status == "ok"), `result` holds the full compute_advantage dict.
    Otherwise `result` is None and `message` explains why the cell did not run.
    """

    cell: Cell
    status: str
    result: dict[str, Any] | None = None
    message: str = ""
    # Populated only when strategy_mode != "fixed": the topology-optimized "Q".
    strategy: dict[str, Any] | None = None

    @property
    def advantage(self) -> float | None:
        return None if self.result is None else float(self.result["advantage"])

    @property
    def q_is_nash(self) -> bool | None:
        return None if self.result is None else bool(self.result["q_is_nash"])


def run_cell(cell: Cell) -> CellResult:
    """Evaluate a single cell, capturing all failure modes as a status.

    When `cell.strategy_mode` is "cooperative" or "nash", the topology's own
    optimal symmetric gate is computed first (game.strategy_opt) and passed as
    `q_params`, so "Q" reflects the topology's best quantum play rather than the
    fixed GHZ-derived strategy. "fixed" (default) leaves the legacy behavior.

    When `cell.noise_p > 0`, every profile is evaluated on the depolarizing
    density-matrix path (circuits.noise) via the `prob_fn` seam; the transpiled
    entangler is cached per (topology, N, gamma) inside circuits.noise, so the
    3^N profiles of a cell share one synthesis (Month-4 D8). noise_p == 0 keeps
    the exact statevector path, byte-identical to before.
    """
    try:
        entangler = resolve(cell.topology, cell.N)
        prob_fn: ProbFn | None = None
        if cell.noise_p > 0.0:
            prob_fn = lambda n, params: build_ewl_circuit_noisy(  # noqa: E731
                n, params, topology=cell.topology, gamma=cell.gamma, p=cell.noise_p
            )
        q_params = None
        strategy: dict[str, Any] | None = None
        if cell.strategy_mode != "fixed":
            opt = optimal_strategy(
                cell.strategy_mode,
                N=cell.N,
                entangler=entangler,
                gamma=cell.gamma,
                V=cell.V,
                C=cell.C,
                symmetric_caveat=(canonical(cell.topology) == "star"),
                time_budget=NASH_TIME_BUDGET,
            )
            q_params = opt.params
            strategy = {
                "mode": opt.mode,
                "params": list(opt.params),
                "payoff_per_player": opt.payoff_per_player,
                "nash_gap": opt.nash_gap,
                "is_nash": opt.is_nash,
                "converged": opt.converged,
                "symmetric_caveat": opt.symmetric_caveat,
            }
        result = compute_advantage(
            N=cell.N,
            strategy_names=list(cell.strategy_names),
            V=cell.V,
            C=cell.C,
            entangler=entangler,
            gamma=cell.gamma,
            q_params=q_params,
            prob_fn=prob_fn,
        )
    except NotImplementedError as exc:
        return CellResult(cell, STATUS_NOT_IMPLEMENTED, message=str(exc))
    except Exception as exc:  # noqa: BLE001 — record, don't crash the whole sweep
        return CellResult(cell, STATUS_ERROR, message=f"{type(exc).__name__}: {exc}")
    return CellResult(cell, STATUS_OK, result=result, strategy=strategy)


@dataclass
class SweepSummary:
    """Aggregate counts derived from a list of CellResults (used by the report)."""

    total: int
    ok: int
    not_implemented: int
    error: int
    positive_advantage: int
    q_nash: int
    nonpositive_cells: list[CellResult] = field(default_factory=list)
    non_nash_cells: list[CellResult] = field(default_factory=list)


def summarize(results: list[CellResult]) -> SweepSummary:
    ok = [r for r in results if r.status == STATUS_OK]
    nonpositive = [r for r in ok if r.advantage is not None and r.advantage <= 0]
    non_nash = [r for r in ok if r.q_is_nash is False]
    return SweepSummary(
        total=len(results),
        ok=len(ok),
        not_implemented=sum(r.status == STATUS_NOT_IMPLEMENTED for r in results),
        error=sum(r.status == STATUS_ERROR for r in results),
        positive_advantage=sum(
            1 for r in ok if r.advantage is not None and r.advantage > 0
        ),
        q_nash=sum(1 for r in ok if r.q_is_nash),
        nonpositive_cells=nonpositive,
        non_nash_cells=non_nash,
    )


def run_sweep(
    cells: list[Cell],
    on_event: Callable[[str, dict[str, Any]], None] | None = None,
) -> list[CellResult]:
    """Evaluate every cell in order and return their results.

    `on_event(event, info)` is an optional progress hook called as each cell
    starts and finishes (events "start" and "done"). It exists so a CLI can
    stream per-cell progress — important for `strategy_mode` cooperative/nash,
    where a single cell's optimization can take many seconds and the run would
    otherwise look hung. Default None preserves the original silent behavior.
    """
    total = len(cells)
    results: list[CellResult] = []
    for idx, cell in enumerate(cells, start=1):
        if on_event is not None:
            on_event("start", {"index": idx, "total": total, "cell": cell})
        t0 = time.perf_counter()
        result = run_cell(cell)
        if on_event is not None:
            on_event(
                "done",
                {
                    "index": idx,
                    "total": total,
                    "cell": cell,
                    "result": result,
                    "elapsed": time.perf_counter() - t0,
                },
            )
        results.append(result)
    return results
