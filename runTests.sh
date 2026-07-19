#!/bin/bash
# Run the test suite with the pinned conda env interpreter.
# Extra args pass through, e.g.
#   ./runTests.sh -v
#   ./runTests.sh tests/test_topologies.py -k unitary
cd "$(dirname "$0")" || exit 1
exec conda run -n entangled-equilibria --no-capture-output python -m pytest "$@"
