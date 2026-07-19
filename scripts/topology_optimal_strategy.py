"""Per-topology OPTIMAL quantum strategy (topology-independent generalization).

The fixed strategy q_strategy(N) = U(0, pi/N, pi/N) is GHZ-specific. This script
computes each topology's OWN optimal symmetric SU(2) strategy directly from its
entangler, in two flavours (game.strategy_opt):

  cooperative -- the symmetric gate maximizing mean per-player payoff
  nash        -- a symmetric continuous Nash strategy (best-response fixed point),
                 certified by nash_gap (<= 1e-6 means genuine symmetric Nash)

For each (topology, N) it prints the optimized gate, its per-player payoff, the
resulting advantage over the classical NE, and the Nash certificate. This is the
tool that answers "does C_4 have a real quantum advantage under its OWN optimal
strategy, or was advantage=0 just an artifact of the GHZ strategy?"

Run from repo root:
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/topology_optimal_strategy.py            # ring, N=2..4
  PYTHONPATH=src conda run -n entangled-equilibria python scripts/topology_optimal_strategy.py ring 2 5   # topo, Nmin Nmax
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpu_limit  # noqa: E402,F401  (caps BLAS threads; MUST precede numpy import)
from config import C as DEFAULT_C, GAMMA, V as DEFAULT_V  # noqa: E402
from experiment.topology_registry import canonical, resolve  # noqa: E402
from game.nash import compute_advantage  # noqa: E402
from game.strategy_opt import cooperative_strategy, nash_strategy  # noqa: E402


def report(topology: str, n_lo: int, n_hi: int, V: float, C: float, gamma: float) -> None:
    caveat = canonical(topology) == "star"
    print(f"\n=== topology={topology}  V={V:g} C={C:g} gamma={gamma:.4f} ===")
    if caveat:
        print("  (star is not vertex-transitive: symmetric strategy is a "
              "constrained sub-optimum)")
    for N in range(n_lo, n_hi + 1):
        ent = resolve(topology, N)
        fixed = compute_advantage(N=N, V=V, C=C, entangler=ent, gamma=gamma)
        coop = cooperative_strategy(N, ent, gamma, V, C, symmetric_caveat=caveat)
        nash = nash_strategy(N, ent, gamma, V, C, symmetric_caveat=caveat)

        classical = fixed["classical_ne_payoff"]
        print(f"\n  N={N}  (classical NE payoff/player = {classical:.4f})")
        print(f"    fixed GHZ-Q     : payoff={fixed['q_payoff_per_player']:.4f}  "
              f"advantage={fixed['advantage']:+.4f}  q_is_nash={fixed['q_is_nash']}")
        print(f"    cooperative opt : payoff={coop.payoff_per_player:.4f}  "
              f"advantage={coop.payoff_per_player - classical:+.4f}  "
              f"params=({coop.params[0]:.3f},{coop.params[1]:.3f},{coop.params[2]:.3f})  "
              f"nash_gap={coop.nash_gap:.2e} is_nash={coop.is_nash}")
        print(f"    nash strategy   : payoff={nash.payoff_per_player:.4f}  "
              f"advantage={nash.payoff_per_player - classical:+.4f}  "
              f"params=({nash.params[0]:.3f},{nash.params[1]:.3f},{nash.params[2]:.3f})  "
              f"nash_gap={nash.nash_gap:.2e} is_nash={nash.is_nash} "
              f"converged={nash.converged}")


def main() -> None:
    topology = sys.argv[1] if len(sys.argv) > 1 else "ring"
    n_lo = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    n_hi = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    report(topology, n_lo, n_hi, DEFAULT_V, DEFAULT_C, GAMMA)


if __name__ == "__main__":
    main()
