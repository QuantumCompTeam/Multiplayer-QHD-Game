#!/bin/bash
# Run ONLY the asymmetric per-player advantage test (hub vs leaf on the star).
# Uses the pinned conda env interpreter (works from any shell).
# Extra args pass through, e.g.  ./runAsymmetricTest.sh -v   or   ./runAsymmetricTest.sh -k star
cd "$(dirname "$0")" || exit 1
# -s so any per-player prints surface; -v for one line per case.
exec conda run -n entangled-equilibria --no-capture-output python -m pytest tests/test_asymmetric_advantage.py -s -v "$@"
