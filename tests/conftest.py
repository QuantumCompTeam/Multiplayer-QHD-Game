"""Pytest session setup: apply the project's single-thread BLAS policy to all tests.

pytest imports conftest.py before any test module — exactly the "before numpy" window
that src/cpu_limit.py needs (it reads thread-pool env vars once, when numpy is first
imported). pyproject's pythonpath=["src"] normally puts src/ on the path, but we insert
it defensively here so the import works even if conftest is loaded first.

Without this, the test suite oversubscribes every CPU core on these tiny (<=2^N) matrices
(observed user 2m22s vs real 12s on one cell). cpu_limit caps to a single thread, which
the project benchmarked at ~2x faster for this workload. Override via QHD_THREADS.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpu_limit  # noqa: E402,F401  (import applies the BLAS thread cap as a side effect)

import pytest  # noqa: E402

CONFIG_PATH = Path(__file__).resolve().parents[1] / "experiments" / "config.yaml"


@pytest.fixture(scope="session")
def topology_folder() -> Path:
    """Build the shared results/topology/ folder from config.yaml, once per session.

    Individual `<topology>_N{n}_graph.png` + `ewl_circuit_N{n}.png` for the config's
    topologies × N values. NOT autouse, so quick unit-only runs stay fast; the heavy
    sweep tests depend on it so a full `pytest` always produces results/topology/.
    """
    import results_io
    from circuits.topology_graphs import KNOWN_TOPOLOGIES
    from experiment.config import load_config
    from experiment.topology_registry import canonical
    from experiment.topology_viz import write_topology_folder

    cfg = load_config(CONFIG_PATH)
    topos = sorted({canonical(c.topology) for c in cfg.cells} & set(KNOWN_TOPOLOGIES))
    ns = sorted({c.N for c in cfg.cells})
    topo_dir = results_io.RESULTS_ROOT / "topology"
    if topos and ns:
        write_topology_folder(topos, ns, topo_dir)
    return topo_dir
