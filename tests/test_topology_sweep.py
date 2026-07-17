"""Regression + structure tests for the Month 3 topology sweep script.

The advantage ENGINE (`game.nash.compute_advantage`) is already covered by
`test_nash_advantage.py` / `test_asymmetric_advantage.py`. These tests pin the
SWEEP SCRIPT itself — its (topology x N) grid, the headline matrix numbers, and
the CSV / JSON / heatmap writers — so the Month 3 deliverable cannot silently
regress. `scripts/` is importable here because pyproject sets
`pythonpath = ["src", "scripts"]`.

The grid is capped at N<=4: it still exercises the asymmetric star (N=4) while
keeping the 3^N classical-profile enumeration fast.
"""

from __future__ import annotations

import csv
import json

import numpy as np
import pytest

import topology_sweep as ts

_N_VALUES = [2, 3, 4]
_LABELS = [label for label, _ in ts.TOPOLOGIES]  # GHZ, ring, star, full, W


@pytest.fixture(scope="module")
def small_sweep():
    """Run the real `run_sweep()` over a reduced N grid (restored afterwards)."""
    original = ts.N_VALUES
    ts.N_VALUES = _N_VALUES
    try:
        yield ts.run_sweep()
    finally:
        ts.N_VALUES = original


# --------------------------------------------------------------------------
# Grid structure / invariants
# --------------------------------------------------------------------------
def test_grid_is_complete(small_sweep):
    """Every (topology, N) cell is present and is a full compute_advantage dict."""
    assert set(small_sweep) == {(label, N) for label in _LABELS for N in _N_VALUES}
    for r in small_sweep.values():
        for key in ("advantage", "advantage_vector", "q_payoff_vector",
                    "classical_ne_payoff_vector", "symmetric", "q_is_nash"):
            assert key in r


def test_per_cell_vectors_consistent(small_sweep):
    """Per cell: vector length == N, scalar == mean(vector), q == classical + adv."""
    for (label, N), r in small_sweep.items():
        adv = np.asarray(r["advantage_vector"], dtype=float)
        q = np.asarray(r["q_payoff_vector"], dtype=float)
        cne = np.asarray(r["classical_ne_payoff_vector"], dtype=float)
        assert adv.shape == (N,), f"{label} N={N}: advantage_vector wrong length"
        np.testing.assert_allclose(r["advantage"], adv.mean(), atol=1e-9,
                                   err_msg=f"{label} N={N}: scalar != mean(vector)")
        np.testing.assert_allclose(q, cne + adv, atol=1e-9,
                                   err_msg=f"{label} N={N}: q != classical + advantage")


# --------------------------------------------------------------------------
# Headline regression pins (guard the Month 3 numbers)
# --------------------------------------------------------------------------
def test_ghz_n3_advantage_is_one(small_sweep):
    """GHZ N=3: advantage = 1.0, (Q,Q,Q) is Nash, symmetric across players."""
    r = small_sweep[("GHZ", 3)]
    np.testing.assert_allclose(r["advantage"], 1.0, atol=1e-6)
    assert r["q_is_nash"] is True
    assert r["symmetric"] is True


def test_star_n4_per_player_split(small_sweep):
    """Star N=4: per-player advantage [0,1,1,1] (hub sacrificed), mean 0.75, asymmetric."""
    r = small_sweep[("star", 4)]
    np.testing.assert_allclose(r["advantage_vector"], [0.0, 1.0, 1.0, 1.0], atol=1e-6)
    np.testing.assert_allclose(r["advantage"], 0.75, atol=1e-6)
    assert r["symmetric"] is False


@pytest.mark.parametrize("label", ["GHZ", "ring", "full", "W"])
def test_vertex_transitive_topologies_are_symmetric(small_sweep, label):
    """Vertex-transitive topologies give a uniform per-player vector at N=4."""
    r = small_sweep[(label, 4)]
    assert r["symmetric"] is True
    adv = r["advantage_vector"]
    np.testing.assert_allclose(adv, [adv[0]] * len(adv), atol=1e-6)


# --------------------------------------------------------------------------
# Artifact writers
# --------------------------------------------------------------------------
def test_write_matrix_csv(small_sweep, tmp_path):
    """CSV has a header + one row per topology, each with len(N_VALUES) values."""
    ts.N_VALUES = _N_VALUES
    try:
        path = tmp_path / "advantage_matrix.csv"
        ts._write_matrix_csv(path, small_sweep, ts._fmt_advantage)
        rows = list(csv.reader(path.open(encoding="utf-8")))
    finally:
        ts.N_VALUES = [2, 3, 4, 5, 6]
    assert rows[0] == ["topology"] + [f"N={N}" for N in _N_VALUES]
    assert [row[0] for row in rows[1:]] == _LABELS
    for row in rows[1:]:
        assert len(row) == 1 + len(_N_VALUES)


def test_write_per_player_json(small_sweep, tmp_path):
    """JSON is valid, nested [label][str(N)], with vectors of length N."""
    ts.N_VALUES = _N_VALUES
    try:
        path = tmp_path / "per_player.json"
        ts._write_per_player_json(path, small_sweep)
    finally:
        ts.N_VALUES = [2, 3, 4, 5, 6]
    out = json.loads(path.read_text(encoding="utf-8"))
    assert set(out) == set(_LABELS)
    for label in _LABELS:
        assert set(out[label]) == {str(N) for N in _N_VALUES}
        for N in _N_VALUES:
            assert len(out[label][str(N)]["advantage_vector"]) == N


def test_write_heatmap(small_sweep, tmp_path):
    """Heatmap PNG is written and non-empty."""
    pytest.importorskip("matplotlib")
    ts.N_VALUES = _N_VALUES
    try:
        path = tmp_path / "heatmap.png"
        ts.write_heatmap(small_sweep, path)
    finally:
        ts.N_VALUES = [2, 3, 4, 5, 6]
    assert path.exists() and path.stat().st_size > 0


# --------------------------------------------------------------------------
# Formatters
# --------------------------------------------------------------------------
def test_fmt_advantage_marks_asymmetric_only():
    assert ts._fmt_advantage({"advantage": 0.75, "symmetric": False}).endswith("*")
    assert not ts._fmt_advantage({"advantage": 1.0, "symmetric": True}).endswith("*")


def test_fmt_nash_states():
    assert ts._fmt_nash({"q_is_nash": True, "all_pure_nash": [("Q", "Q")]}) == "Q-NE"
    assert ts._fmt_nash({"q_is_nash": False, "all_pure_nash": [("H", "H")]}) == "NE"
    assert ts._fmt_nash({"q_is_nash": False, "all_pure_nash": []}) == "-"
