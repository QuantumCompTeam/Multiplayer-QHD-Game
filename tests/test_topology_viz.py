"""Tests for topology-graph definitions and the visualization layer.

Guards:
  - topology_graph returns the correct edges/kind for each topology (this is the
    SAME graph the entanglers consume, so it doubles as a refactor guard).
  - build_ewl_qc exposes the circuit and build_ewl_circuit is unchanged.
  - draw_topology_graph / draw_circuit produce non-empty output files.

The entangler-matrix correctness after the refactor is covered by the existing
tests/test_topologies.py (ring/star/fully-connected unitarity + N=2 reductions).
"""

from __future__ import annotations

import networkx as nx
import numpy as np
import pytest

from circuits.ewl import q_strategy
from circuits.n_player import build_ewl_circuit, build_ewl_qc
from circuits.topologies import ghz_entangler
from circuits.topology_graphs import topology_graph
from experiment.topology_viz import draw_circuit, draw_topology_graph
from qiskit.circuit import QuantumCircuit


def test_topology_graph_pairwise_edges() -> None:
    assert set(topology_graph("ring", 4).edges()) == {(0, 1), (1, 2), (2, 3), (0, 3)}
    # star: hub 0 connected to every spoke, spokes not to each other.
    star_edges = set(topology_graph("star", 4).edges())
    assert star_edges == {(0, 1), (0, 2), (0, 3)}
    assert topology_graph("fully-connected", 4).number_of_edges() == 6


def test_topology_graph_kinds() -> None:
    for name in ("ring", "star", "fully-connected"):
        assert topology_graph(name, 4).graph["kind"] == "pairwise"
    for name in ("ghz", "w"):
        g = topology_graph(name, 4)
        assert g.graph["kind"] == "global"
        assert g.number_of_nodes() == 4
        assert g.number_of_edges() == 0  # global: no pairwise edge set


def test_topology_graph_matches_nx_builders() -> None:
    # The graph drawn must have the same nodes/edges the entangler uses
    # (our graph also carries metadata attrs, so compare structure, not attrs).
    ring = topology_graph("ring", 5)
    assert set(ring.edges()) == set(nx.cycle_graph(5).edges())
    fc = topology_graph("fully-connected", 5)
    assert set(fc.edges()) == set(nx.complete_graph(5).edges())


def test_unknown_topology_raises() -> None:
    with pytest.raises(ValueError):
        topology_graph("banana", 3)


def test_build_ewl_qc_returns_circuit() -> None:
    qc = build_ewl_qc(3, [q_strategy(3)] * 3, entangler=ghz_entangler)
    assert isinstance(qc, QuantumCircuit)
    assert qc.num_qubits == 3


def test_build_ewl_circuit_unchanged() -> None:
    """Regression: GHZ (Q,Q,Q) collapses to all-Dove |000> with probability 1."""
    probs = build_ewl_circuit(3, [q_strategy(3)] * 3, entangler=ghz_entangler)
    assert probs.shape == (8,)
    assert np.isclose(probs.sum(), 1.0)
    assert np.isclose(probs[0], 1.0, atol=1e-9)


def test_draw_topology_graph_writes_png(tmp_path) -> None:
    for name in ("ring", "ghz"):  # one pairwise, one global
        fig = draw_topology_graph(name, 4)
        out = tmp_path / f"{name}.png"
        fig.savefig(out, dpi=80)
        assert out.exists() and out.stat().st_size > 0


def test_draw_circuit_produces_output(tmp_path) -> None:
    kind, obj = draw_circuit(3, entangler=ghz_entangler)
    assert kind in ("mpl", "text")
    if kind == "mpl":
        out = tmp_path / "circuit.png"
        obj.savefig(out, dpi=80)
        assert out.exists() and out.stat().st_size > 0
    else:
        assert isinstance(obj, str) and obj.strip()
