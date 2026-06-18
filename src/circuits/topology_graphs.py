"""Graph definitions for the entanglement topologies — single source of truth.

`topology_graph(name, N)` returns the networkx graph that defines a topology, so
the SAME graph drives both the entangler (via make_pairwise_entangler) and the
visualization (no drift between what is computed and what is drawn).

Two kinds, recorded in graph.graph["kind"]:
  "pairwise"  -- ring / star / fully-connected: edges ARE the entangling pairs
                 exp(i*gamma/2 X_i X_j), one per edge.
  "global"    -- ghz / w: a single N-body entangler, NOT a sum of pairwise terms.
                 GHZ uses X^(x)N; W uses a |0..0><->|W> reflection. There is no
                 pairwise edge set, so the graph carries nodes only and is drawn
                 with a distinct "global" depiction (never as a complete graph,
                 which would conflate GHZ with fully-connected).
"""

from __future__ import annotations

import networkx as nx

# Friendly names this module understands (canonical, lower-case, hyphenated).
PAIRWISE_TOPOLOGIES = ("ring", "star", "fully-connected")
GLOBAL_TOPOLOGIES = ("ghz", "w")
KNOWN_TOPOLOGIES = PAIRWISE_TOPOLOGIES + GLOBAL_TOPOLOGIES

# Human-readable description of the entangler each topology applies.
_LABELS = {
    "ring": "pairwise on cycle C_N",
    "star": "pairwise on star (hub = qubit 0)",
    "fully-connected": "pairwise on complete graph K_N",
    "ghz": "global X^⊗N (single N-body term)",
    "w": "global W-state reflection",
}


def _pairwise_graph(name: str, N: int) -> nx.Graph:
    if name == "ring":
        return nx.cycle_graph(N)
    if name == "star":
        # nx.star_graph(k) has k+1 nodes (hub 0 + k spokes); use N-1 for N nodes.
        return nx.star_graph(N - 1)
    if name == "fully-connected":
        return nx.complete_graph(N)
    raise ValueError(f"no pairwise graph for {name!r}")


def topology_graph(name: str, N: int) -> nx.Graph:
    """Return the nx.Graph defining `name` at N qubits.

    For pairwise topologies the edges are the entangling pairs. For global
    topologies (ghz/w) the graph has N nodes and NO edges; kind == "global".

    graph.graph carries: "kind" ("pairwise"|"global"), "topology" (name),
    "label" (entangler description), "N".
    """
    key = name.strip().lower()
    if key in PAIRWISE_TOPOLOGIES:
        graph = _pairwise_graph(key, N)
        kind = "pairwise"
    elif key in GLOBAL_TOPOLOGIES:
        graph = nx.empty_graph(N)  # N nodes, no edges
        kind = "global"
    else:
        raise ValueError(
            f"unknown topology {name!r}; known: {KNOWN_TOPOLOGIES}"
        )
    graph.graph.update(
        {"kind": kind, "topology": key, "label": _LABELS[key], "N": N}
    )
    return graph
