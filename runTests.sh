#!/bin/bash
# Run the test suite with the project's virtualenv interpreter.
# Calls .venv/bin/python directly — no shell activation needed, so this works
# from any shell (bash, fish, zsh). Extra args pass through, e.g.
#   ./runTests.sh -v
#   ./runTests.sh tests/test_topologies.py -k unitary
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then
    echo "error: .venv/bin/python not found — create the venv and install deps first." >&2
    exit 1
fi
exec .venv/bin/python -m pytest "$@"
