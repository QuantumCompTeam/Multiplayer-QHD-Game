"""Helpers for writing labelled, reproducible result runs under results/.

Every run lives in results/<experiment>/<UTC-timestamp>/ and carries a
metadata.json recording the parameters, git commit, and creation time so the
run is self-describing and reproducible.

Stdlib only -- safe to import from scripts without extra dependencies.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Repo root = parent of src/ (this file is src/results_io.py).
_REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_ROOT = _REPO_ROOT / "results"

# Filesystem-safe UTC label, e.g. 2026-06-18T0930Z (no colons).
_TIMESTAMP_FMT = "%Y-%m-%dT%H%MZ"


def run_timestamp() -> str:
    """Return the current UTC timestamp label used for run-folder names."""
    return datetime.now(timezone.utc).strftime(_TIMESTAMP_FMT)


def _git_commit() -> dict[str, object]:
    """Best-effort current git commit + dirty flag; None if git is unavailable."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        return {"commit": commit, "dirty": bool(status.strip())}
    except Exception:  # noqa: BLE001 -- git missing / not a repo: record null
        return {"commit": None, "dirty": None}


def new_run_dir(experiment: str, timestamp: str | None = None) -> Path:
    """Create and return results/<experiment>/<timestamp>/.

    `timestamp` defaults to the current UTC label; pass an explicit value to
    group several artifacts from one logical run under the same folder.
    """
    ts = timestamp or run_timestamp()
    parent = RESULTS_ROOT / experiment
    parent.mkdir(parents=True, exist_ok=True)
    if timestamp is not None:
        run_dir = parent / ts
        run_dir.mkdir(exist_ok=True)
        return run_dir
    # Separate invocations in the same minute must not overwrite one another.
    # mkdir is atomic, so concurrent writers also receive distinct directories.
    suffix = 0
    while True:
        run_dir = parent / (ts if suffix == 0 else f"{ts}-{suffix:03d}")
        try:
            run_dir.mkdir()
            return run_dir
        except FileExistsError:
            suffix += 1


def write_metadata(run_dir: Path, experiment: str, params: dict) -> Path:
    """Write metadata.json (experiment, timestamp, git commit, params) into run_dir."""
    meta = {
        "experiment": experiment,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git": _git_commit(),
        "python": sys.version,
        "params": params,
    }
    path = run_dir / "metadata.json"
    path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return path
