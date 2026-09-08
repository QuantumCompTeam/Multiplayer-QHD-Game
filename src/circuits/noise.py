"""Depolarizing-noise EWL runner (Month 4).

The noiseless path returns exact statevector probabilities. Noise is a channel,
not a unitary, so it needs a density-matrix simulation with a per-gate error model.
This module builds the SAME J . U . J-dagger circuit as circuits/n_player, but as
elementary gates (circuits/gate_level), transpiles to the pinned {u, cx} basis, and
runs it on AerSimulator(density_matrix) under a depolarizing NoiseModel.

Design (Month-4 spec):
  - D3/2A: basis pinned to {u, cx}; 1-qubit depolarizing on `u`, 2-qubit on `cx`
    only. So "each entangling edge's noise cost = its cx-decomposition cost", and
    the model is deterministic and version-independent.
  - D8/8A: the expensive step is synthesizing the entangler to {u, cx}. That
    depends only on (topology, N, gamma), NOT on the strategy profile, so it is
    transpiled ONCE and cached; each of the 3^N profiles in a cell only pays for
    translating its tiny 1-qubit U layer. (Our U(theta,alpha,beta) is a custom
    SU(2) matrix, not a native parametrized gate, so the cache is on the transpiled
    entangler rather than qiskit Parameters -- same performance win, simpler.)

Contract: build_ewl_circuit_noisy returns probs of shape (2^N,), sum ~= 1, in the
same Qiskit little-endian order as build_ewl_circuit. At p=0 it reproduces the
exact statevector result (tests/test_noise.py::test_p0_equals_statevector).
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import numpy.typing as npt
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from circuits.ewl import U, StrategyParams
from config import GAMMA

_PINNED_BASIS = ["u", "cx"]


def build_noise_model(p: float, p2_ratio: float = 1.0) -> NoiseModel:
    """Depolarizing NoiseModel: prob `p` on 1-qubit `u`, `p*p2_ratio` on 2-qubit `cx`.

    Errors are only added when their probability is > 0, so build_noise_model(0.0)
    is an empty (noiseless) model and the density-matrix run then reproduces the
    exact statevector result. p2_ratio (default 1.0) lets a later run make 2-qubit
    gates noisier than 1-qubit ones without an interface change.
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"noise p must be in [0, 1], got {p}")
    if not np.isfinite(p2_ratio) or p2_ratio < 0:
        raise ValueError("p2_ratio must be finite and nonnegative")
    p2 = min(1.0, p * p2_ratio)
    nm = NoiseModel()
    if p > 0.0:
        nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), ["u"])
    if p2 > 0.0:
        nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    return nm


@lru_cache(maxsize=None)
def _transpiled_entangler(
    topology: str, N: int, gamma: float
) -> tuple[QuantumCircuit, QuantumCircuit]:
    """Return (J, J-dagger) as circuits pre-transpiled to {u, cx}. Cached (D8).

    Resolved through the shared topology registry (single source of truth, D5) so
    the noisy path uses exactly the topologies the noiseless path knows. Imported
    lazily to avoid an import-time circuits->experiment layering dependency.
    """
    from experiment.topology_registry import resolve_gate_circuit

    j_gates = resolve_gate_circuit(topology, N, gamma)
    j_t = transpile(j_gates, basis_gates=_PINNED_BASIS, optimization_level=1)
    return j_t, j_t.inverse()


def build_ewl_circuit_noisy(
    N: int,
    strategies: list[StrategyParams],
    *,
    topology: str,
    gamma: float = GAMMA,
    p: float,
    p2_ratio: float = 1.0,
) -> npt.NDArray[np.float64]:
    """Run the noisy EWL circuit and return outcome probabilities, shape (2^N,).

    J . (U_0 x ... x U_{N-1}) . J-dagger under a depolarizing channel. Bit ordering
    is Qiskit little-endian, identical to build_ewl_circuit. Raises ValueError for
    p outside [0, 1].
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"noise p must be in [0, 1], got {p}")

    if len(strategies) != N:
        raise ValueError(f"expected exactly {N} player strategies, got {len(strategies)}")
    j_t, jdag_t = _transpiled_entangler(topology, N, gamma)

    qc = QuantumCircuit(N)
    qc.compose(j_t, inplace=True)
    for qubit, params in enumerate(strategies):
        qc.append(UnitaryGate(U(*params), label="U"), [qubit])
    qc.compose(jdag_t, inplace=True)

    # Translate the U layer into {u, cx} so the 1-qubit depolarizing error attaches
    # to it; the J parts are already in basis (opt_level 0 leaves them alone).
    tqc = transpile(qc, basis_gates=_PINNED_BASIS, optimization_level=0)
    tqc.save_probabilities()

    sim = AerSimulator(
        method="density_matrix", noise_model=build_noise_model(p, p2_ratio)
    )
    result = sim.run(tqc).result()
    probs = result.data(0)["probabilities"]
    return np.asarray(probs, dtype=np.float64)
