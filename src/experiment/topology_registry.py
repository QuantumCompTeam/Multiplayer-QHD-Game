"""Resolve a friendly topology name to an Entangler callable.

Maps config-facing names (case-insensitive, with a few aliases) to the entangler
functions in circuits/topologies.py. All five topologies are implemented; an
unknown name raises ValueError (the sweep records it as a failed cell rather than
aborting the run). New topologies only need a line in _REGISTRY.
"""

from __future__ import annotations

from circuits.topologies import (
    Entangler,
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)

# Canonical name -> entangler.  Aliases are normalized in resolve().
_REGISTRY: dict[str, Entangler] = {
    "ghz": ghz_entangler,
    "ring": ring_entangler,
    "star": star_entangler,
    "fully-connected": fully_connected_entangler,
    "w": w_entangler,
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


def resolve(topology: str, N: int) -> Entangler:
    """Return the Entangler (N, gamma) -> matrix for `topology`.

    `N` is accepted for interface symmetry (some future topologies may need it);
    the current entanglers build their own graph from N internally.
    Raises ValueError for an unrecognized name.
    """
    key = canonical(topology)
    if key not in _REGISTRY:
        raise ValueError(
            f"unknown topology {topology!r}; known: {sorted(_REGISTRY)} "
            f"(aliases: {sorted(_ALIASES)})"
        )
    return _REGISTRY[key]
