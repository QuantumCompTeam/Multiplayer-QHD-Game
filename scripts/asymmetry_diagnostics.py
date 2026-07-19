"""Week-1 falsification diagnostics for the noise-induced per-player asymmetry finding.

Two tests (elevation-report validation plan):

  1. Wiring-permutation test
     Compose the SAME transpiled entangler onto permuted physical qubits and keep
     every player's strategy gate where it is. At the symmetric (Q,...,Q) profile
     all players apply an identical gate, so permuting the strategy layer is a
     no-op -- the entangler wiring is the only meaningful thing to permute.
     MECHANISM: the disadvantaged player follows the wiring (circuit position);
       the whole payoff vector permutes with it.
     SUSPECT:   the same player index loses regardless of wiring -> bookkeeping bug.

  2. State-level noise control
     Apply one global depolarizing channel to the ideal FINAL state instead of
     per-gate noise during the circuit. Measurement probabilities mix linearly:
     (1-p) * ideal + p * uniform. Because expected_payoff is linear and the
     noiseless (Q,...,Q) payoffs are player-symmetric for ring/GHZ/W, the
     per-player spread must collapse to ~0. If it survives, the "noise lives on
     the implementation, not the state" story is wrong -- stop and rethink.

Run from repo root:
  conda run -n entangled-equilibria python scripts/asymmetry_diagnostics.py             # ring N=5 p=0.02
  conda run -n entangled-equilibria python scripts/asymmetry_diagnostics.py w 5 0.02    # topology N p
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpu_limit  # noqa: E402,F401  (caps BLAS threads; MUST precede numpy import)

import numpy as np  # noqa: E402
from qiskit import QuantumCircuit, transpile  # noqa: E402
from qiskit.circuit.library import UnitaryGate  # noqa: E402
from qiskit_aer import AerSimulator  # noqa: E402

from circuits.ewl import U, q_strategy  # noqa: E402
from circuits.n_player import build_ewl_circuit  # noqa: E402
from circuits.noise import (  # noqa: E402
    _PINNED_BASIS,
    _transpiled_entangler,
    build_ewl_circuit_noisy,
    build_noise_model,
)
from config import C, GAMMA, V  # noqa: E402
from experiment.topology_registry import canonical, resolve  # noqa: E402
from game.payoffs import expected_payoff  # noqa: E402

# Report anchor: results/noise-robustness/2026-07-03T0213Z, N=5 ring p=0.02,
# per-player Q payoff vector (rounded to 4 dp in report.md).
ANCHOR = {("ring", 5, 0.02): [0.7969, 0.7949, 0.7886, 0.7828, 0.7819]}

VECTOR_TOL = 1e-6  # permuted run must reproduce the identity payoffs exactly


def run_noisy_wired(
    topology: str, N: int, p: float, perm: tuple[int, ...]
) -> np.ndarray:
    """Per-gate-noise run with the entangler composed onto permuted qubits.

    Reuses the production path's cached transpiled entangler and noise model
    (circuits.noise), so the gate set is identical to build_ewl_circuit_noisy;
    only the wire assignment changes. Entangler wire w acts on physical qubit
    perm[w], i.e. player perm[w] takes circuit role w.
    """
    j_t, jdag_t = _transpiled_entangler(canonical(topology), N, GAMMA)
    strategies = [q_strategy(N)] * N

    qc = QuantumCircuit(N)
    qc.compose(j_t, qubits=list(perm), inplace=True)
    for qubit, params in enumerate(strategies):
        qc.append(UnitaryGate(U(*params), label="U"), [qubit])
    qc.compose(jdag_t, qubits=list(perm), inplace=True)

    tqc = transpile(qc, basis_gates=_PINNED_BASIS, optimization_level=0)
    tqc.save_probabilities()
    sim = AerSimulator(method="density_matrix", noise_model=build_noise_model(p))
    probs = sim.run(tqc).result().data(0)["probabilities"]
    return expected_payoff(np.asarray(probs, dtype=np.float64), N, V, C)


def permutation_test(topology: str, N: int, p: float):
    """Cyclic shifts + reversal of the entangler wiring; loser must follow it."""
    identity = tuple(range(N))
    wirings = [tuple((i + s) % N for i in range(N)) for s in range(1, N)]
    wirings.append(tuple(range(N - 1, -1, -1)))

    payoffs_id = run_noisy_wired(topology, N, p, identity)
    loser_role = int(np.argmin(payoffs_id))
    print(f"  identity wiring payoffs: {np.round(payoffs_id, 6)}")
    print(f"  loser under identity wiring: player {loser_role} "
          f"(circuit role {loser_role})")

    follows_wiring, label_pinned, max_dev = True, True, 0.0
    for perm in wirings:
        payoffs = run_noisy_wired(topology, N, p, perm)
        expected = np.empty(N)
        expected[list(perm)] = payoffs_id  # role w's payoff moves to qubit perm[w]
        dev = float(np.max(np.abs(payoffs - expected)))
        max_dev = max(max_dev, dev)
        loser = int(np.argmin(payoffs))
        print(f"  wiring {perm}: loser=player {loser} "
              f"(expected {perm[loser_role]}), vector-permute dev={dev:.2e}")
        if loser != perm[loser_role] or dev > VECTOR_TOL:
            follows_wiring = False
        if loser != loser_role:
            label_pinned = False

    if follows_wiring:
        verdict = "MECHANISM: disadvantage follows circuit position"
    elif label_pinned:
        verdict = "SUSPECT: disadvantage follows player label -- check for a bug"
    else:
        verdict = ("INCONCLUSIVE: loser moves but not as the wiring predicts "
                   f"(max vector deviation {max_dev:.2e}) -- investigate")
    return verdict


def state_level_control(topology: str, N: int, p: float):
    """Global depolarizing on the ideal final state; spread must collapse."""
    strategies = [q_strategy(N)] * N
    probs_ideal = build_ewl_circuit(
        N, strategies, entangler=resolve(topology, N), gamma=GAMMA
    )
    probs_noisy = (1.0 - p) * probs_ideal + p / 2 ** N
    payoffs = expected_payoff(probs_noisy, N, V, C)
    spread = float(payoffs.max() - payoffs.min())
    print(f"  state-level payoffs: {np.round(payoffs, 6)}  spread={spread:.2e}")

    if spread < 1e-3:
        verdict = "CONFIRMS mechanism: asymmetry vanishes under state-level noise"
    else:
        verdict = ("ASYMMETRY SURVIVES uniform noise -- re-examine before "
                   "trusting the headline")
    return verdict, spread


def main() -> None:
    topology = sys.argv[1] if len(sys.argv) > 1 else "ring"
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    p = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02

    print(f"=== asymmetry diagnostics: topology={topology} N={N} p={p} "
          f"(V={V:g}, C={C:g}, gamma=pi/2) ===")

    # Anchor: production path must reproduce the locked report numbers.
    payoffs_prod = expected_payoff(
        build_ewl_circuit_noisy(
            N, [q_strategy(N)] * N, topology=topology, gamma=GAMMA, p=p
        ),
        N, V, C,
    )
    print(f"\nAnchor (build_ewl_circuit_noisy): {np.round(payoffs_prod, 6)}")
    key = (canonical(topology), N, p)
    if key in ANCHOR:
        ref = np.asarray(ANCHOR[key])
        ok = np.allclose(np.round(payoffs_prod, 4), ref, atol=1e-3)
        print(f"  vs report {ref.tolist()}: {'match' if ok else 'MISMATCH'}")
        if not ok:
            print("  Anchor mismatch -- diagnostics would not test the reported "
                  "finding. Aborting.")
            sys.exit(1)
    spread_gate = float(payoffs_prod.max() - payoffs_prod.min())
    print(f"  per-gate-noise spread: {spread_gate:.6f}")

    print("\nTest 1 -- wiring-permutation test")
    verdict1 = permutation_test(topology, N, p)

    print("\nTest 2 -- state-level noise control")
    verdict2, spread_state = state_level_control(topology, N, p)

    print("\n=== VERDICTS ===")
    print(f"Permutation test:    {verdict1}")
    print(f"State-level control: {verdict2}")
    print(f"(spread under per-gate noise {spread_gate:.6f} vs "
          f"state-level {spread_state:.2e})")


if __name__ == "__main__":
    main()
