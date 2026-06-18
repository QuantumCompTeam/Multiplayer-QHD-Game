---
type: "query"
date: "2026-06-17T10:45:41.498208+00:00"
question: "Would pairwise entanglement be useful at this level; if yes how, if no why?"
contributor: "graphify"
source_nodes: ["make_pairwise_entangler()", "ghz_entangler()", "Entangler", "Month 2 Design Spec: N=3 GHZ Extension", "find_pure_nash()"]
---

# Q: Would pairwise entanglement be useful at this level; if yes how, if no why?

## Answer

Expanded via vocab: [pairwise, entangler, entangling, ghz, topology, ring, star, fully, connected, extension, formula]. Grounded in n3-ghz-extension-design.md. At N=2: NO distinction - one pair only, so pairwise == global GHZ (ghz_entangler(2)==J_matrix, spec 2.1/test). At N=3 (current level): pairwise becomes meaningful and IS the planned next step - make_pairwise_entangler(G) for ring/star/fully-connected is the Month-3 RQ2 topology comparison (spec 2.2, sec 8). Why useful: different entanglement graphs distribute correlations differently and can change WHICH profiles are Nash equilibria and the size of quantum advantage; the spec built full 27-profile Nash enumeration specifically 'because the complete pure-NE structure is needed for Month 3 topology comparison (RQ2)' (spec 2.3). Why NOT yet: Month 2 deliberately uses only symmetric all-to-all GHZ to establish the baseline (Q_N=U(0,pi/N,pi/N), advantage>0) before varying structure; make_pairwise_entangler is a NotImplementedError stub (topologies.py:62, spec sec 8). So: useful and intended at N>=3, scoped to Month 3, pluggable via the Entangler interface without touching build_ewl_circuit.

## Source Nodes

- make_pairwise_entangler()
- ghz_entangler()
- Entangler
- Month 2 Design Spec: N=3 GHZ Extension
- find_pure_nash()