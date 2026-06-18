"""Run the parameter sweep by calling game.nash.compute_advantage per cell.

Each cell is evaluated independently and wrapped so that one failing cell (an
unimplemented/unknown topology or an unexpected error) never aborts the whole
run — it is recorded with a status and message instead. Asymmetric topologies
(e.g. star) are fully supported: compute_advantage returns per-player vectors and
a `symmetric` flag, which the report surfaces.

This module adds NO game theory; compute_advantage is the single source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from experiment.config import Cell
from experiment.topology_registry import resolve
from game.nash import compute_advantage

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

    @property
    def advantage(self) -> float | None:
        return None if self.result is None else float(self.result["advantage"])

    @property
    def q_is_nash(self) -> bool | None:
        return None if self.result is None else bool(self.result["q_is_nash"])


def run_cell(cell: Cell) -> CellResult:
    """Evaluate a single cell, capturing all failure modes as a status."""
    try:
        entangler = resolve(cell.topology, cell.N)
        result = compute_advantage(
            N=cell.N,
            strategy_names=list(cell.strategy_names),
            V=cell.V,
            C=cell.C,
            entangler=entangler,
            gamma=cell.gamma,
        )
    except NotImplementedError as exc:
        return CellResult(cell, STATUS_NOT_IMPLEMENTED, message=str(exc))
    except Exception as exc:  # noqa: BLE001 — record, don't crash the whole sweep
        return CellResult(cell, STATUS_ERROR, message=f"{type(exc).__name__}: {exc}")
    return CellResult(cell, STATUS_OK, result=result)


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


def run_sweep(cells: list[Cell]) -> list[CellResult]:
    """Evaluate every cell in order and return their results."""
    return [run_cell(cell) for cell in cells]
