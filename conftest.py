"""Pytest bootstrap: cap BLAS/OpenMP threads before any test imports NumPy.

The test suite runs the experiment sweep (see tests/test_config_experiment.py),
which does thousands of small statevector simulations at N up to 8. By default
NumPy's BLAS backend spawns one thread per core and busy-waits between calls, so
even this small-matrix work pegs every core to 100%. Importing cpu_limit here --
before pytest collects any test module that pulls in NumPy -- applies the same
core cap used by the entry-point scripts (single thread by default, since BLAS
multithreading is pure overhead for these tiny matrices; override with the
QHD_THREADS env var).

pyproject's [tool.pytest.ini_options] pythonpath=["src"] is applied before
conftest import, but we insert src/ explicitly too so this works regardless of
how pytest is invoked.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import cpu_limit  # noqa: E402,F401  (sets thread-pool env vars before NumPy loads)
