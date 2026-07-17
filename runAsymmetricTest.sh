#!/bin/bash
# Run ONLY the asymmetric per-player advantage test (hub vs leaf on the star).
# Calls .venv/bin/python directly — no shell activation needed, works from any shell.
# Extra args pass through, e.g.  ./runAsymmetricTest.sh -v   or   ./runAsymmetricTest.sh -k star
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then
    echo "error: .venv/bin/python not found — create the venv and install deps first." >&2
    exit 1
fi
# -s so any per-player prints surface; -v for one line per case.
exec .venv/bin/python -m pytest tests/test_asymmetric_advantage.py -s -v "$@"
