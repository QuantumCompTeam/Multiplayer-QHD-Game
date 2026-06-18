"""Month 2 RQ1 result: quantum advantage at N=3 with GHZ entangler.

Runs compute_advantage(N=3) and prints:
  - (Q,Q,Q) per-player payoff  [Q = q_strategy(3) = U(0, pi/3, pi/3)]
  - classical Nash equilibrium payoff  [from restricted {D,H}^3 game]
  - advantage = quantum NE - classical NE
  - whether (Q,Q,Q) is a pure Nash equilibrium
  - all pure Nash equilibria in {D,H,Q}^3
  - classical pure NE profiles found in {D,H}^3
  - unilateral deviation table from (Q,Q,Q)

Month 2 checkpoint: advantage > 0 and (Q,Q,Q) is Nash.
If advantage <= 0 or q_is_nash is False, this is an RQ1 finding -- stop and
investigate rather than adjusting parameters to paper over the result.

Run from repo root:
  conda run -n entangled-equilibria python scripts/n3_advantage.py
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import results_io
from config import C as DEFAULT_C, GAMMA, V as DEFAULT_V
from game.nash import compute_advantage

N = 3
result = compute_advantage(N=N)

print("=" * 60)
print(f"  Month 2 — N={N} GHZ EWL Quantum Advantage (RQ1)")
print(f"  Q strategy: q_strategy({N}) = U(0, pi/{N}, pi/{N})")
print("=" * 60)

print(f"\n  (Q,Q,Q) per-player payoff  : {result['q_payoff_per_player']:.6f}")
print(f"  Classical NE payoff        : {result['classical_ne_payoff']:.6f}")
print(f"  Advantage (QNE - CNE)      : {result['advantage']:.6f}")
print(f"  (Q,Q,Q) is pure Nash       : {result['q_is_nash']}")

print(f"\n  Classical pure NE profiles in {{D,H}}^{N}:")
if result["classical_nash_profiles"]:
    for p in result["classical_nash_profiles"]:
        payoff = result["classical_ne_payoff"]
        print(f"    {p}  ->  {payoff:.6f} per player")
else:
    print("    (none found)")

print(f"\n  All pure Nash equilibria in {{D,H,Q}}^{N}:")
if result["all_pure_nash"]:
    for profile in result["all_pure_nash"]:
        print(f"    {profile}")
else:
    print("    (none found)")

print(f"\n  Unilateral deviation table from (Q,Q,Q):")
print(f"  {'Deviator':>10}  {'Alt':>4}  {'Dev payoff':>12}  {'Q payoff':>10}  {'Q dominates':>12}")
print(f"  {'-'*10}  {'-'*4}  {'-'*12}  {'-'*10}  {'-'*12}")
for (player, alt), info in sorted(result["deviation_check"].items()):
    print(
        f"  {'player ' + str(player):>10}  {alt:>4}  "
        f"{info['deviation_payoff']:>12.6f}  "
        f"{info['q_payoff']:>10.6f}  "
        f"{'YES' if info['q_dominates'] else 'NO -- NASH VIOLATED':>12}"
    )

print()

# Persist the full result (JSON-safe: tuple keys/profiles -> strings/lists).
run_dir = results_io.new_run_dir("month2_n3_advantage")
summary = {
    "N": N,
    "q_payoff_per_player": result["q_payoff_per_player"],
    "q_payoff_vector": result["q_payoff_vector"],
    "classical_ne_payoff": result["classical_ne_payoff"],
    "classical_ne_payoff_vector": result["classical_ne_payoff_vector"],
    "advantage": result["advantage"],
    "advantage_vector": result["advantage_vector"],
    "symmetric": result["symmetric"],
    "q_is_nash": result["q_is_nash"],
    "all_pure_nash": [list(p) for p in result["all_pure_nash"]],
    "classical_nash_profiles": [list(p) for p in result["classical_nash_profiles"]],
    "deviation_check": {
        f"player{player}_{alt}": info
        for (player, alt), info in result["deviation_check"].items()
    },
}
(run_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
results_io.write_metadata(
    run_dir,
    "month2_n3_advantage",
    params={"N": N, "V": DEFAULT_V, "C": DEFAULT_C, "GAMMA": GAMMA,
            "entangler": "ghz_entangler", "strategy_set": ["D", "H", "Q"]},
)
print(f"  Results written to {run_dir}\n")

if result["advantage"] <= 0:
    print("  CHECKPOINT FAILED: advantage <= 0.")
    print("  This is an RQ1 finding -- investigate before proceeding.")
    sys.exit(1)
elif not result["q_is_nash"]:
    print("  CHECKPOINT FAILED: (Q,Q,Q) is not a pure Nash equilibrium.")
    print("  This is an RQ1 finding -- investigate before proceeding.")
    sys.exit(1)
else:
    print("  CHECKPOINT PASSED: advantage > 0 and (Q,Q,Q) is a pure Nash equilibrium.")
    print("  Quantum advantage confirmed at N=3 (RQ1).")
