---
type: "query"
date: "2026-06-18T10:55:53.772043+00:00"
question: "What is the command to run the testing suite?"
contributor: "graphify"
source_nodes: ["test_two_player.py", "test_n_player.py", "test_topologies.py"]
---

# Q: What is the command to run the testing suite?

## Answer

Expanded from original query via vocab: [test, tests, run, runs, validation, script, checkpoint, assertions, correctness, guards]. The run command is not a graph node; it comes from pyproject.toml [tool.pytest.ini_options] (pythonpath=['src'], testpaths=['tests']) and README Quick Start. Canonical: 'pytest' from repo root (zero flags needed due to the ini config). Variants: 'pytest tests/ -v' (README), 'conda run -n entangled-equilibria python -m pytest' (documented env), '.venv/bin/python -m pytest' (this machine, deps in project .venv). All run the same suite: test_two_player.py, test_n_player.py, test_topologies.py, test_ewl.py, test_payoffs.py, test_experiment.py, test_topology_viz.py.

## Source Nodes

- test_two_player.py
- test_n_player.py
- test_topologies.py