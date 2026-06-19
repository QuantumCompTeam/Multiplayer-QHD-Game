"""Load and validate experiments/config.yaml into a typed, sweep-expanded config.

A "cell" is one concrete parameter combination evaluated by the sweep. The full
cell list is the cartesian product over every list-valued sweep/game field:
`sweep.N`, `sweep.topologies`, and `game.V`, `game.C`, `game.gamma` each become a
sweep axis when given a list (a scalar is a single fixed point). `strategy_names`
(the discrete action set) and `strategy_mode` (fixed|cooperative|nash) are
constant per run, not sweep axes. Required keys: `sweep.N` and `sweep.topologies`.

See experiments/config.yaml itself for the per-field documentation (valid values,
defaults, and which fields are sweep axes) — that file is the user-facing
reference; this module is the parser/validator behind it.
"""

from __future__ import annotations

import itertools
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Output formats the harness knows how to write (see report.py / plots.py).
VALID_FORMATS = ("md", "json", "csv", "plots")

# How "Q" is chosen per cell. "fixed": the GHZ-derived q_strategy(N) (legacy,
# default). "cooperative"/"nash": a topology-optimized gate from
# game.strategy_opt computed per (topology, N, gamma). See sweep.run_cell.
VALID_STRATEGY_MODES = ("fixed", "cooperative", "nash")


@dataclass(frozen=True)
class Cell:
    """One concrete parameter combination to evaluate."""

    N: int
    topology: str
    strategy_names: tuple[str, ...]
    V: float
    C: float
    gamma: float
    gamma_label: str  # original config text (e.g. "pi/2") for display
    strategy_mode: str = "fixed"  # fixed | cooperative | nash (constant per run)


@dataclass
class ExperimentConfig:
    name: str
    description: str
    cells: list[Cell]
    formats: list[str] = field(default_factory=lambda: list(VALID_FORMATS))


# --- gamma expression parsing -------------------------------------------------

_GAMMA_TOKEN = re.compile(r"^[\spi0-9./*]+$")


def parse_gamma(value: Any) -> float:
    """Parse a gamma value: a number, or a restricted expression of pi.

    Accepts ints/floats directly, or strings containing only `pi`, digits, `.`,
    `/`, `*`, and whitespace (e.g. "pi/2", "pi / 4", "2*pi"). Rejects anything
    else. This is a whitelist, NOT eval of arbitrary code.
    """
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        raise ValueError(f"gamma must be a number or pi-expression, got {value!r}")
    text = value.strip()
    if not _GAMMA_TOKEN.match(text):
        raise ValueError(
            f"gamma expression {value!r} may only contain pi, digits, '.', '/', '*'"
        )
    expr = text.replace("pi", "math.pi")
    try:
        result = eval(expr, {"__builtins__": {}}, {"math": math})  # noqa: S307
    except (SyntaxError, ZeroDivisionError, NameError) as exc:
        raise ValueError(f"could not parse gamma expression {value!r}: {exc}") from exc
    return float(result)


def _as_list(value: Any) -> list[Any]:
    """Normalize a scalar-or-list config field into a list (a sweep axis)."""
    if isinstance(value, list):
        return value
    return [value]


def _gamma_label(value: Any) -> str:
    return value if isinstance(value, str) else repr(value)


# --- loading ------------------------------------------------------------------


def expand_cells(raw: dict[str, Any]) -> list[Cell]:
    """Expand the cartesian product of all list-valued sweep/game fields."""
    sweep = raw.get("sweep", {})
    game = raw.get("game", {})

    n_values = _as_list(sweep["N"])
    topologies = _as_list(sweep["topologies"])
    strategy_names = tuple(sweep.get("strategy_names", ["D", "H", "Q"]))
    strategy_mode = str(sweep.get("strategy_mode", "fixed"))
    if strategy_mode not in VALID_STRATEGY_MODES:
        raise ValueError(
            f"unknown strategy_mode {strategy_mode!r}; valid: {VALID_STRATEGY_MODES}"
        )

    v_values = _as_list(game.get("V", 4.0))
    c_values = _as_list(game.get("C", 3.0))
    gamma_values = _as_list(game.get("gamma", "pi/2"))

    cells: list[Cell] = []
    for N, topo, V, C, gamma_raw in itertools.product(
        n_values, topologies, v_values, c_values, gamma_values
    ):
        cells.append(
            Cell(
                N=int(N),
                topology=str(topo),
                strategy_names=strategy_names,
                V=float(V),
                C=float(C),
                gamma=parse_gamma(gamma_raw),
                gamma_label=_gamma_label(gamma_raw),
                strategy_mode=strategy_mode,
            )
        )
    return cells


def load_config(path: str | Path) -> ExperimentConfig:
    """Load and validate a YAML experiment config into an ExperimentConfig."""
    path = Path(path)
    with path.open() as fh:
        raw = yaml.safe_load(fh)

    if not isinstance(raw, dict):
        raise ValueError(f"{path}: top-level YAML must be a mapping")
    if "sweep" not in raw or "N" not in raw["sweep"] or "topologies" not in raw["sweep"]:
        raise ValueError(f"{path}: config must define sweep.N and sweep.topologies")

    exp = raw.get("experiment", {})
    out = raw.get("output", {})

    formats = out.get("formats", list(VALID_FORMATS))
    bad = [f for f in formats if f not in VALID_FORMATS]
    if bad:
        raise ValueError(f"{path}: unknown output formats {bad}; valid: {VALID_FORMATS}")

    cells = expand_cells(raw)
    if not cells:
        raise ValueError(f"{path}: sweep expanded to zero cells")

    return ExperimentConfig(
        name=str(exp.get("name", path.stem)),
        description=str(exp.get("description", "")),
        cells=cells,
        formats=list(formats),
    )
