"""Cap BLAS / OpenMP thread pools so the process doesn't saturate every core.

NumPy / SciPy (and Qiskit's quantum_info.Statevector, which is NumPy underneath)
sit on a BLAS backend that, by default, spawns one worker thread per CPU core.
Even this small-matrix workload then fans every matrix op out across all cores,
pinning the whole machine to 100%.

These thread-pool sizes are read ONCE, when NumPy is first imported, so this
module MUST be imported before numpy / scipy / qiskit / matplotlib (anything that
pulls in NumPy). Each entry-point script imports it as its very first project
import, right after the sys.path.insert that puts src/ on the path.

Policy (per project decision): default to a SINGLE thread. This project's
matrices are tiny (<=256x256), so BLAS multithreading is pure spin-wait overhead
-- benchmarked single-threaded is ~2x faster than 14 threads on the topology
sweep AND uses one core instead of pegging the whole machine. Override with the
QHD_THREADS env var (e.g. QHD_THREADS=4) if a future larger-N run benefits. Any
individual thread var already set in the environment is respected.
"""

from __future__ import annotations

import os

# Thread vars for the common BLAS / OpenMP backends (OpenBLAS, MKL, BLIS,
# Accelerate/vecLib, NumExpr, plain OpenMP). We set them all so the cap holds
# regardless of which backend NumPy was built against.
_THREAD_VARS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
)


def _default_threads() -> int:
    """Single-threaded by default: fastest and coolest for this workload."""
    return 1


def _resolve_threads() -> int:
    override = os.environ.get("QHD_THREADS")
    if override:
        try:
            return max(1, int(override))
        except ValueError:
            pass  # malformed override -> fall back to the default policy
    return _default_threads()


def apply() -> int:
    """Set the thread-pool env vars (without clobbering ones already set).

    Returns the thread count chosen, for logging/tests.
    """
    n = _resolve_threads()
    for var in _THREAD_VARS:
        os.environ.setdefault(var, str(n))  # don't override a user's explicit value
    return n


THREADS = apply()
