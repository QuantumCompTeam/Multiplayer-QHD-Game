"""Month 3 RQ2: quantum advantage across entanglement topologies and N.

Sweeps topology in {GHZ, ring, star, fully-connected, W} x N in {2..6} and
reports, for each cell:
  - advantage  = mean (Q,...,Q) per-player payoff - mean classical NE payoff
  - whether (Q,...,Q) is a pure Nash equilibrium
  - whether ANY pure Nash equilibrium exists in {D,H,Q}^N

For asymmetric topologies (star) the advantage is the mean over players; the
per-player breakdown is saved to per_player.json.

All artifacts (CSV matrices, per-player JSON, heatmap, metadata) are written to
results/month3_topology_sweep/<UTC-timestamp>/.

Run from repo root:
  PYTHONPATH=src python scripts/topology_sweep.py
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import results_io  # noqa: E402
from circuits.topologies import (  # noqa: E402
    fully_connected_entangler,
    ghz_entangler,
    ring_entangler,
    star_entangler,
    w_entangler,
)
from config import C as DEFAULT_C, GAMMA, V as DEFAULT_V  # noqa: E402
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


def _write_matrix_csv(path, results: dict, fmt) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["topology"] + [f"N={N}" for N in N_VALUES])
        for name, _ in TOPOLOGIES:
            w.writerow([name] + [fmt(results[(name, N)]) for N in N_VALUES])


def _write_per_player_json(path, results: dict) -> None:
    out: dict = {}
    for name, _ in TOPOLOGIES:
        out[name] = {}
        for N in N_VALUES:
            r = results[(name, N)]
            out[name][str(N)] = {
                "advantage": r["advantage"],
                "q_payoff_vector": r["q_payoff_vector"],
                "classical_ne_payoff_vector": r["classical_ne_payoff_vector"],
                "advantage_vector": r["advantage_vector"],
                "symmetric": r["symmetric"],
                "q_is_nash": r["q_is_nash"],
                "all_pure_nash": [list(p) for p in r["all_pure_nash"]],
                "classical_nash_profiles": [
                    list(p) for p in r["classical_nash_profiles"]
                ],
            }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)


def write_heatmap(results: dict, path) -> None:
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
        plt.close(fig)
        print(f"  heatmap.png written")
    except Exception as e:  # noqa: BLE001
        print(f"  [heatmap skipped: {e}]")


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

    run_dir = results_io.new_run_dir("month3_topology_sweep")
    _write_matrix_csv(run_dir / "advantage_matrix.csv", results, _fmt_advantage)
    _write_matrix_csv(run_dir / "equilibrium_matrix.csv", results, _fmt_nash)
    _write_per_player_json(run_dir / "per_player.json", results)
    write_heatmap(results, run_dir / "heatmap.png")
    results_io.write_metadata(
        run_dir,
        "month3_topology_sweep",
        params={
            "N_values": N_VALUES,
            "topologies": [name for name, _ in TOPOLOGIES],
            "V": DEFAULT_V,
            "C": DEFAULT_C,
            "GAMMA": GAMMA,
            "strategy_set": ["D", "H", "Q"],
        },
    )
    print(f"\nResults written to {run_dir}")


if __name__ == "__main__":
    main()
