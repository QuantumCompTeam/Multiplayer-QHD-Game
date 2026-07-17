#!/bin/bash
# Run the entanglement-γ sweep and write its results folder + insight plots.
# Calls .venv/bin/python directly — no shell activation needed, works from any shell.
# Tune N / the γ range via the constants at the top of tests/test_gamma_sweep.py.
# Extra args pass through, e.g.  ./runGammaSweep.sh -v
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then
    echo "error: .venv/bin/python not found — create the venv and install deps first." >&2
    exit 1
fi
# -s so the "[gamma sweep] results written to ..." path is printed.
exec .venv/bin/python -m pytest tests/test_gamma_sweep.py -s "$@"
