"""Resolve a friendly topology name to its entangler (two views).

Maps config-facing names (case-insensitive, with a few aliases) to BOTH the dense
matrix entangler (circuits/topologies.py, used by the exact noiseless path) and the
gate-level circuit builder (circuits/gate_level.py, used by the Month-4 noisy path).
Keeping both in one registry is the single source of truth for "what topologies
exist" plus their aliases -- adding a topology means one line here, wired for both
paths, so the noiseless and noisy paths cannot drift (Month-4 spec D5/4A).

All five topologies are implemented; an unknown name raises ValueError (the sweep
records it as a failed cell rather than aborting the run).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from circuits.gate_level import (
    fully_connected_gate_circuit,
    ghz_gate_circuit,
    ring_gate_circuit,
    star_gate_circuit,
    w_gate_circuit,
)
from circuits.topologies import (
    Entangler,
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)
from qiskit.circuit import QuantumCircuit

# Gate-level builder signature: (N, gamma) -> QuantumCircuit.
GateCircuitBuilder = Callable[..., QuantumCircuit]


@dataclass(frozen=True)
class TopologyEntry:
    """Both views of one topology: dense matrix entangler + gate-level builder."""

    entangler: Entangler
    gate_circuit: GateCircuitBuilder


# Canonical name -> (matrix entangler, gate-circuit builder). Aliases in resolve().
_REGISTRY: dict[str, TopologyEntry] = {
    "ghz": TopologyEntry(ghz_entangler, ghz_gate_circuit),
    "ring": TopologyEntry(ring_entangler, ring_gate_circuit),
    "star": TopologyEntry(star_entangler, star_gate_circuit),
    "fully-connected": TopologyEntry(
        fully_connected_entangler, fully_connected_gate_circuit
    ),
    "w": TopologyEntry(w_entangler, w_gate_circuit),
}

# Friendly aliases accepted in the config (normalized to canonical keys).
_ALIASES = {
    "full": "fully-connected",
    "fully_connected": "fully-connected",
    "complete": "fully-connected",
}

KNOWN_TOPOLOGIES = tuple(_REGISTRY.keys())


def canonical(topology: str) -> str:
    key = topology.strip().lower()
    return _ALIASES.get(key, key)


def _entry(topology: str) -> TopologyEntry:
    key = canonical(topology)
    if key not in _REGISTRY:
        raise ValueError(
            f"unknown topology {topology!r}; known: {sorted(_REGISTRY)} "
            f"(aliases: {sorted(_ALIASES)})"
        )
    return _REGISTRY[key]


def resolve(topology: str, N: int) -> Entangler:
    """Return the dense matrix Entangler (N, gamma) -> matrix for `topology`.

    `N` is accepted for interface symmetry (some future topologies may need it);
    the current entanglers build their own graph from N internally.
    Raises ValueError for an unrecognized name.
    """
    return _entry(topology).entangler


def resolve_gate_circuit(
    topology: str, N: int, gamma: float
) -> QuantumCircuit:
    """Return the gate-level entangler QuantumCircuit for `topology` (noisy path).

    Same name/alias handling as resolve(); the two views share one registry so
    they cannot drift (Month-4 spec D5/4A). Raises ValueError for an unknown name.
    """
    return _entry(topology).gate_circuit(N, gamma)
