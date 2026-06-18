"""Write sweep outputs: config snapshot, results.json, results.csv, report.md, plots/.

Pure formatting — no game theory. Reads CellResult objects (from sweep.py) and
the ExperimentConfig, and emits the requested output formats into a run directory.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from experiment.config import ExperimentConfig
from experiment.sweep import (
    STATUS_OK,
    CellResult,
    SweepSummary,
    summarize,
)


def _profile_str(profile: tuple[str, ...]) -> str:
    return "(" + ",".join(profile) + ")"


def _json_safe_result(result: dict[str, Any]) -> dict[str, Any]:
    """Convert a compute_advantage dict into JSON-serializable form.

    compute_advantage uses tuple profiles and (player, alt) tuple keys that JSON
    cannot represent directly, so flatten them into lists of plain records.
    """
    return {
        "q_payoff_per_player": result["q_payoff_per_player"],
        "q_payoff_vector": result["q_payoff_vector"],
        "classical_ne_payoff": result["classical_ne_payoff"],
        "classical_ne_payoff_vector": result["classical_ne_payoff_vector"],
        "advantage": result["advantage"],
        "advantage_vector": result["advantage_vector"],
        "symmetric": result["symmetric"],
        "q_is_nash": result["q_is_nash"],
        "all_pure_nash": [list(p) for p in result["all_pure_nash"]],
        "classical_nash_profiles": [list(p) for p in result["classical_nash_profiles"]],
        "deviation_check": [
            {
                "player": player,
                "alt": alt,
                "deviation_payoff": info["deviation_payoff"],
                "q_payoff": info["q_payoff"],
                "q_dominates": info["q_dominates"],
            }
            for (player, alt), info in sorted(result["deviation_check"].items())
        ],
    }


def _cell_record(r: CellResult) -> dict[str, Any]:
    """Flat record for a cell (used by JSON and CSV)."""
    rec: dict[str, Any] = {
        "N": r.cell.N,
        "topology": r.cell.topology,
        "strategy_names": ",".join(r.cell.strategy_names),
        "V": r.cell.V,
        "C": r.cell.C,
        "gamma": r.cell.gamma,
        "gamma_label": r.cell.gamma_label,
        "status": r.status,
        "advantage": r.advantage,
        "q_is_nash": r.q_is_nash,
        "symmetric": None if r.result is None else r.result["symmetric"],
        "q_payoff_per_player": None if r.result is None else r.result["q_payoff_per_player"],
        "classical_ne_payoff": None if r.result is None else r.result["classical_ne_payoff"],
        "message": r.message,
    }
    return rec


# --- config snapshot ----------------------------------------------------------


def _config_snapshot(config: ExperimentConfig, timestamp: str) -> dict[str, Any]:
    return {
        "experiment": {"name": config.name, "description": config.description},
        "generated_at": timestamp,
        "output": {"formats": config.formats},
        "cells": [
            {
                "N": c.N,
                "topology": c.topology,
                "strategy_names": list(c.strategy_names),
                "V": c.V,
                "C": c.C,
                "gamma": c.gamma,
                "gamma_label": c.gamma_label,
            }
            for c in config.cells
        ],
    }


# --- markdown report ----------------------------------------------------------


def _fmt(value: float | None) -> str:
    return "—" if value is None else f"{value:.6f}"


def _summary_table(results: list[CellResult]) -> list[str]:
    header = (
        "| N | topology | V | C | gamma | q_payoff | classical_ne | advantage "
        "| q_is_nash | symmetric | status |"
    )
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    rows = [header, sep]
    for r in results:
        qp = None if r.result is None else r.result["q_payoff_per_player"]
        cp = None if r.result is None else r.result["classical_ne_payoff"]
        nash = "—" if r.q_is_nash is None else ("yes" if r.q_is_nash else "**NO**")
        sym = "—" if r.result is None else ("yes" if r.result["symmetric"] else "no")
        rows.append(
            f"| {r.cell.N} | {r.cell.topology} | {r.cell.V:g} | {r.cell.C:g} "
            f"| {r.cell.gamma_label} | {_fmt(qp)} | {_fmt(cp)} | {_fmt(r.advantage)} "
            f"| {nash} | {sym} | {r.status} |"
        )
    return rows


def _findings(results: list[CellResult], summary: SweepSummary) -> list[str]:
    lines = ["## Findings", ""]
    lines.append(
        f"- Evaluated **{summary.total}** cells: {summary.ok} ran, "
        f"{summary.not_implemented} not-implemented, {summary.error} errored."
    )
    if summary.ok:
        lines.append(
            f"- Quantum advantage > 0 in **{summary.positive_advantage}/{summary.ok}** "
            f"computed cells."
        )
        lines.append(
            f"- (Q,...,Q) is a pure Nash equilibrium in "
            f"**{summary.q_nash}/{summary.ok}** computed cells."
        )

    # A non-positive advantage or non-Nash Q is an RQ1 *finding*, not a bug.
    if summary.nonpositive_cells:
        lines.append("")
        lines.append("**Cells with advantage <= 0 (RQ1 finding — investigate, do not paper over):**")
        for r in summary.nonpositive_cells:
            lines.append(
                f"  - N={r.cell.N}, {r.cell.topology}, gamma={r.cell.gamma_label}: "
                f"advantage = {_fmt(r.advantage)}"
            )
    if summary.non_nash_cells:
        lines.append("")
        lines.append("**Cells where (Q,...,Q) is NOT Nash (RQ1 finding):**")
        for r in summary.non_nash_cells:
            lines.append(f"  - N={r.cell.N}, {r.cell.topology}, gamma={r.cell.gamma_label}")

    # Make skipped coverage explicit so gaps never read as "covered".
    skipped = [r for r in results if r.status != STATUS_OK]
    if skipped:
        lines.append("")
        lines.append("**Skipped / not-run cells (coverage gaps):**")
        for r in skipped:
            lines.append(
                f"  - N={r.cell.N}, {r.cell.topology} — {r.status}: {r.message or '—'}"
            )
    lines.append("")
    return lines


def _cell_detail(r: CellResult) -> list[str]:
    assert r.result is not None
    res = r.result
    q = tuple("Q" for _ in range(r.cell.N))
    lines = [
        f"### N={r.cell.N} · {r.cell.topology} · gamma={r.cell.gamma_label} "
        f"(V={r.cell.V:g}, C={r.cell.C:g})",
        "",
        f"- {_profile_str(q)} mean per-player payoff: **{res['q_payoff_per_player']:.6f}**",
        f"- Classical NE mean payoff: **{res['classical_ne_payoff']:.6f}**",
        f"- Advantage (QNE − CNE, mean): **{res['advantage']:.6f}**",
        f"- {_profile_str(q)} is pure Nash: **{res['q_is_nash']}**",
        f"- Player-symmetric: **{res['symmetric']}**",
        "",
    ]
    if not res["symmetric"]:
        # For asymmetric topologies (e.g. star), the scalar means hide per-player
        # spread — show the full vectors so the asymmetry is visible.
        def _vec(v: list[float]) -> str:
            return "[" + ", ".join(f"{x:.4f}" for x in v) + "]"

        lines += [
            "**Per-player breakdown (asymmetric topology):**",
            "",
            f"- Q payoff vector: {_vec(res['q_payoff_vector'])}",
            f"- Classical NE payoff vector: {_vec(res['classical_ne_payoff_vector'])}",
            f"- Advantage vector: {_vec(res['advantage_vector'])}",
            "",
        ]
    lines += [
        "Classical pure NE in {D,H}^N: "
        + (
            ", ".join(_profile_str(p) for p in res["classical_nash_profiles"])
            or "(none found)"
        ),
        "",
        "All pure NE: "
        + (", ".join(_profile_str(p) for p in res["all_pure_nash"]) or "(none found)"),
        "",
        "Unilateral deviation table from (Q,...,Q):",
        "",
        "| deviator | alt | dev payoff | Q payoff | Q dominates |",
        "|---|---|---|---|---|",
    ]
    for (player, alt), info in sorted(res["deviation_check"].items()):
        dominates = "yes" if info["q_dominates"] else "**NO — NASH VIOLATED**"
        lines.append(
            f"| player {player} | {alt} | {info['deviation_payoff']:.6f} "
            f"| {info['q_payoff']:.6f} | {dominates} |"
        )
    lines.append("")
    return lines


def _render_markdown(
    config: ExperimentConfig,
    results: list[CellResult],
    timestamp: str,
    plot_files: list[str],
) -> str:
    summary = summarize(results)
    lines = [
        f"# Experiment report: {config.name}",
        "",
        config.description,
        "",
        f"_Generated: {timestamp}_",
        "",
        "## Parameters used",
        "",
        "```yaml",
        yaml.safe_dump(_config_snapshot(config, timestamp), sort_keys=False).rstrip(),
        "```",
        "",
        "## Summary",
        "",
    ]
    lines += _summary_table(results)
    lines.append("")
    lines += _findings(results, summary)

    if plot_files:
        lines.append("## Plots")
        lines.append("")
        for pf in plot_files:
            lines.append(f"![{pf}](plots/{pf})")
        lines.append("")

    lines.append("## Per-cell detail")
    lines.append("")
    ok_cells = [r for r in results if r.status == STATUS_OK]
    if ok_cells:
        for r in ok_cells:
            lines += _cell_detail(r)
    else:
        lines.append("_No cells ran successfully._")
        lines.append("")

    lines.append("## Data files")
    lines.append("")
    lines.append("- `results.json` — full structured results")
    lines.append("- `results.csv` — one row per cell")
    lines.append("- `config.snapshot.yaml` — exact parameters used")
    lines.append("")
    return "\n".join(lines)


# --- top-level writer ---------------------------------------------------------


def write_outputs(
    config: ExperimentConfig,
    results: list[CellResult],
    run_dir: str | Path,
    timestamp: str,
) -> Path:
    """Write all requested output formats into run_dir. Returns the run_dir path."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    # Always snapshot the exact parameters for reproducibility.
    with (run_dir / "config.snapshot.yaml").open("w") as fh:
        yaml.safe_dump(_config_snapshot(config, timestamp), fh, sort_keys=False)

    if "json" in config.formats:
        payload = {
            "experiment": {"name": config.name, "description": config.description},
            "generated_at": timestamp,
            "cells": [
                {
                    **_cell_record(r),
                    "detail": None
                    if r.result is None
                    else _json_safe_result(r.result),
                }
                for r in results
            ],
        }
        with (run_dir / "results.json").open("w") as fh:
            json.dump(payload, fh, indent=2)

    if "csv" in config.formats:
        fields = list(_cell_record(results[0]).keys()) if results else []
        with (run_dir / "results.csv").open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            for r in results:
                writer.writerow(_cell_record(r))

    plot_files: list[str] = []
    if "plots" in config.formats:
        # Imported lazily so md/json/csv-only runs don't require matplotlib.
        from experiment.plots import write_plots

        plot_files = write_plots(results, run_dir / "plots")

    if "md" in config.formats:
        md = _render_markdown(config, results, timestamp, plot_files)
        (run_dir / "report.md").write_text(md)

    return run_dir
