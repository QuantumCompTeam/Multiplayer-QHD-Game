#!/bin/bash
# Run the entanglement-γ sweep and write its results folder + insight plots.
# Uses the pinned conda env interpreter (works from any shell).
# Tune N / the γ range via the constants at the top of tests/test_gamma_sweep.py.
# Extra args pass through, e.g.  ./runGammaSweep.sh -v
cd "$(dirname "$0")" || exit 1
# -s so the "[gamma sweep] results written to ..." path is printed.
exec conda run -n entangled-equilibria --no-capture-output python -m pytest tests/test_gamma_sweep.py -s "$@"
