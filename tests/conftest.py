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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpu_limit  # noqa: E402,F401  (import applies the BLAS thread cap as a side effect)
