"""Month 3 RQ2: quantum advantage across entanglement topologies and N.

Sweeps topology in {GHZ, ring, star, fully-connected, W} x N in {2..6} and
reports, for each cell:
  - advantage  = mean (Q,...,Q) per-player payoff - mean classical NE payoff
  - whether (Q,...,Q) is a pure Nash equilibrium
  - whether ANY pure Nash equilibrium exists in {D,H,Q}^N

For asymmetric topologies (star) the advantage is the mean over players; the
per-player breakdown is available from compute_advantage's *_vector keys.

Run from repo root:
  PYTHONPATH=src python scripts/topology_sweep.py
  PYTHONPATH=src python scripts/topology_sweep.py --heatmap   # also write PNG
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from circuits.topologies import (  # noqa: E402
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)
from game.nash import compute_advantage  # noqa: E402

TOPOLOGIES = [
    ("GHZ", ghz_entangler),
    ("ring", ring_entangler),
    ("star", star_entangler),
    ("full", fully_connected_entangler),
    ("W", w_entangler),
]
N_VALUES = [2, 3, 4, 5, 6]


def run_sweep() -> dict:
    """Return {(topology_name, N): compute_advantage result dict}."""
    results = {}
    for name, entangler in TOPOLOGIES:
        for N in N_VALUES:
            results[(name, N)] = compute_advantage(N=N, entangler=entangler)
    return results


def _fmt_advantage(r: dict) -> str:
    adv = r["advantage"]
    sym = "" if r["symmetric"] else "*"  # * marks asymmetric (mean reported)
    return f"{adv:+.3f}{sym}"


def _fmt_nash(r: dict) -> str:
    if r["q_is_nash"]:
        return "Q-NE"
    if r["all_pure_nash"]:
        return "NE"  # some pure NE exists, but not (Q,...,Q)
    return "-"  # no pure NE at all


def print_matrix(results: dict, title: str, fmt) -> None:
    print(f"\n{title}")
    header = "  topo  | " + " ".join(f"{('N='+str(N)):>9}" for N in N_VALUES)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for name, _ in TOPOLOGIES:
        row = " ".join(f"{fmt(results[(name, N)]):>9}" for N in N_VALUES)
        print(f"  {name:>5} | {row}")


def maybe_heatmap(results: dict, path: str = "topology_advantage_heatmap.png") -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")  # no display required
        import matplotlib.pyplot as plt
        import numpy as np

        data = np.array(
            [[results[(name, N)]["advantage"] for N in N_VALUES] for name, _ in TOPOLOGIES]
        )
        fig, ax = plt.subplots(figsize=(7, 4))
        im = ax.imshow(data, aspect="auto", cmap="viridis")
        ax.set_xticks(range(len(N_VALUES)), [f"N={N}" for N in N_VALUES])
        ax.set_yticks(range(len(TOPOLOGIES)), [name for name, _ in TOPOLOGIES])
        ax.set_title("Quantum advantage (mean per-player) by topology x N")
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center",
                        color="white", fontsize=8)
        fig.colorbar(im, ax=ax, label="advantage")
        fig.tight_layout()
        fig.savefig(path, dpi=120)
        print(f"\nHeatmap written to {path}")
    except Exception as e:  # noqa: BLE001
        print(f"\n[heatmap skipped: {e}]")


def main() -> None:
    print("=" * 70)
    print("  Month 3 RQ2 -- Topology x N Quantum Advantage Sweep")
    print("  advantage = mean (Q,..,Q) payoff - mean classical NE payoff")
    print("  '*' = asymmetric topology (mean over players reported)")
    print("=" * 70)

    results = run_sweep()
    print_matrix(results, "Advantage matrix:", _fmt_advantage)
    print_matrix(
        results,
        "Equilibrium structure  (Q-NE = (Q,..,Q) is Nash; NE = some pure NE; - = none):",
        _fmt_nash,
    )

    if "--heatmap" in sys.argv:
        maybe_heatmap(results)


if __name__ == "__main__":
    main()
