"""Best linear qubit chain on a device coupling graph.

The scaling experiment pins ONE 5-qubit linear chain and runs N=3/4/5 on its
prefixes, so the physical qubits are a controlled variable across the curve.
The chain is chosen by minimizing the summed calibration error along the path.
"""

from __future__ import annotations


def best_linear_chain(
    edges: list[tuple[int, int]],
    edge_err: dict[frozenset[int], float],
    node_err: dict[int, float],
    length: int,
) -> list[int]:
    """Return the simple path of `length` nodes minimizing summed error.

    Score = sum of edge_err over the path's length-1 edges
          + sum of node_err over the path's nodes.
    Edges are undirected (edge_err keyed by frozenset). A path and its reverse
    have equal score; the returned path is canonicalized so path[0] < path[-1].
    Raises ValueError if the graph has no simple path of that length.
    """
    adj: dict[int, set[int]] = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    best_path: list[int] | None = None
    best_score = float("inf")

    def extend(path: list[int], score: float) -> None:
        nonlocal best_path, best_score
        if len(path) == length:
            if score < best_score:
                best_score = score
                best_path = list(path)
            return
        for nxt in adj.get(path[-1], ()):
            if nxt in path:
                continue
            e = frozenset((path[-1], nxt))
            extend(path + [nxt], score + edge_err[e] + node_err[nxt])

    for start in sorted(adj):
        extend([start], node_err[start])

    if best_path is None:
        raise ValueError(f"no simple path of {length} nodes in coupling graph")
    if best_path[0] > best_path[-1]:
        best_path.reverse()
    return best_path
