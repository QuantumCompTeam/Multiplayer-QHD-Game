# VERIFIED FACTS

**Generated:** 2026-07-18
**Branch:** dev
**HEAD at generation:** b3469f020dd2beb0ea92fc3c8366ff57467b428c
**Working tree at generation:** clean (`git status --porcelain` returned empty)
**Status:** untracked until committed separately. This file snapshots the
repository immediately before its own commit; a reader who finds HEAD elsewhere
is looking at a later state.

**Provenance rule:** every value below was extracted from this repository at
that commit, by reading a file or running the command shown. Nothing is
recalled, inferred, or carried over from any prior conversation or handoff
document. Where a value could not be extracted it reads NOT IN REPO, with the
locations checked.

**Interpreter provenance, by script family:**

| family | interpreter | used for |
| --- | --- | --- |
| game-theory computations (D2, D5) | conda `entangled-equilibria`, python 3.10.20 | `compute_advantage` sweeps |
| stdlib extraction scripts (B, C, F) | bare PATH python 3.9.13 | `json` / `glob` reads only, no repo code imported |
| `.venv-win` version report (A1) | `.venv-win` python 3.9.13 | reporting its own package versions |
| everything else | `grep`, `find`, `cat`, `awk`, `git` | no interpreter |

The stdlib scripts run under an interpreter that cannot import `src/` (A7).
This is acceptable because they read JSON only. No value in this file depends on
repo code executed under anything but the conda env.

## Citation format

Every file:line citation carries a short literal anchor from the cited line,
written as `path:line (anchor)`. Line numbers drift silently when files are
edited, so the anchor lets a reader grep for the true current location and tell
immediately whether the number moved, or whether the claim is dead because the
anchor is gone. Four of four file:line citations carried over from a previous
draft failed re-derivation in a single session, one broken by a commit made
hours earlier, which is what this format exists to prevent. Command citations
and commit-hash citations carry no anchor because they do not drift.

For rows whose cited content is a single numeric JSON value, the value printed
in the table is itself the anchor. Multi-value blocks cite the exact first and
last value line, brackets excluded.

---

## A. Environment and interpreter conventions

### A1. Three Python environments are reachable from this repo

All three measured 2026-07-18 on the same five fields.

| field | conda `entangled-equilibria` | `.venv-win/` | bare `python` on PATH |
| --- | --- | --- | --- |
| python | 3.10.20 | 3.9.13 | 3.9.13 |
| qiskit | 1.3.2 | 2.2.3 | 0.45.3 |
| qiskit-aer | 0.14.2 | 0.17.2 | 0.13.3 |
| qiskit-ibm-runtime | 0.36.1 | 0.43.1 | not installed |
| numpy | 1.26.4 | 2.0.2 | 1.26.4 |

Commands, all run 2026-07-18:

    conda run -n entangled-equilibria python -c "import qiskit, qiskit_aer, qiskit_ibm_runtime, numpy, sys; print('python', sys.version.split()[0]); print('qiskit', qiskit.__version__); print('qiskit-aer', qiskit_aer.__version__); print('qiskit-ibm-runtime', qiskit_ibm_runtime.__version__); print('numpy', numpy.__version__)"

    ./.venv-win/Scripts/python.exe -c "...same body..."

    python -c "import sys; print(sys.version.split()[0], sys.executable)"
    python -c "import importlib
    for m in ['qiskit','qiskit_aer','qiskit_ibm_runtime','numpy']:
        try: print(m, importlib.import_module(m).__version__)
        except Exception as e: print(m, 'NOT INSTALLED (' + type(e).__name__ + ')')"

The `.venv-win` command emitted two DeprecationWarnings, that qiskit deprecates
Python 3.9 as of its 2.1.0 release and qiskit-ibm-runtime as of its 0.41.0
release.

**Machine-specific caveat.** The third column is not a property of this
repository. The bare interpreter is whatever PATH resolves `python` to, which on
the machine used on 2026-07-18 was `C:\Program Files\Python39\python.exe`, the
same base interpreter `.venv-win` was built from
(.venv-win/pyvenv.cfg:1 (`home = C:\Program Files\Python39`),
.venv-win/pyvenv.cfg:3 (`version = 3.9.13`)) though not that venv, carrying a
different qiskit. A different machine running the identical documented command
would get a different interpreter and different versions. The repo does not pin
a third stack. It pins nothing for this convention. See G10.

Only the conda env satisfies pyproject.toml:6 (`"qiskit==1.3.2",`). Both 3.9.13
interpreters violate pyproject.toml:4 (`requires-python = ">=3.10"`).

### A2. `.venv-win/pyvenv.cfg`, full contents

    1  home = C:\Program Files\Python39
    2  include-system-site-packages = false
    3  version = 3.9.13

Source: `cat -n .venv-win/pyvenv.cfg`

### A3. pyproject.toml pins

| constraint | source |
| --- | --- |
| requires-python | pyproject.toml:4 (`requires-python = ">=3.10"`) |
| qiskit | pyproject.toml:6 (`"qiskit==1.3.2",`) |
| qiskit-aer | pyproject.toml:7 (`"qiskit-aer==0.14.2",`) |
| nashpy | pyproject.toml:8 (`"nashpy==0.0.19",`) |
| networkx | pyproject.toml:9 (`"networkx==3.3",`) |
| numpy | pyproject.toml:10 (`"numpy==1.26.4",`) |
| scipy | pyproject.toml:11 (`"scipy==1.13.1",`) |
| matplotlib | pyproject.toml:12 (`"matplotlib==3.9.2",`) |
| pyyaml | pyproject.toml:13 (`"pyyaml>=6.0",`) |
| pylatexenc | pyproject.toml:14 (`"pylatexenc>=2.10",`) |
| dev extras | pyproject.toml:18 (`dev = ["pytest>=8.0", "mypy>=1.10", "ruff>=0.5"]`) |

Source: `grep -n -E "requires-python|qiskit|nashpy|networkx|numpy|scipy|matplotlib|pyyaml|pylatexenc|pytest>|mypy>|ruff>" pyproject.toml`

A3 is the pin table. The interpreter sweep is A5, not here. Any prompt citing
A3 for the sweep is stale; see the note at the end of A5.

### A4. No environment lockfile and no build entry point exist

Of Makefile, makefile, justfile, Justfile, noxfile.py, tasks.py,
environment.yml, environment.yaml, requirements.txt, requirements-dev.txt,
poetry.lock, uv.lock, setup.py, setup.cfg, and pyproject.toml, only
pyproject.toml exists. The other fourteen return "No such file or directory".

Source: `ls Makefile makefile justfile Justfile noxfile.py tasks.py environment.yml environment.yaml requirements.txt requirements-dev.txt poetry.lock uv.lock setup.py setup.cfg pyproject.toml`

There is no file from which the conda env `entangled-equilibria` can be
recreated.

### A5. Three competing interpreter conventions are documented

Sources:

    grep -rn "conda run -n entangled-equilibria" --include=*.md --include=*.py --include=*.yaml --include=*.toml --exclude-dir=.venv-win --exclude-dir=.git --exclude-dir=graphify-out .
    grep -rn "\.venv/bin/python" --include=*.md --include=*.py --include=*.yaml --include=*.toml --exclude-dir=.venv-win --exclude-dir=.git --exclude-dir=graphify-out .
    grep -rn "PYTHONPATH=src python" --include=*.md --include=*.py --include=*.yaml --include=*.toml --exclude-dir=.venv-win --exclude-dir=.git --exclude-dir=graphify-out .

plus, for the TODOS.md prose form no command above matches:

    grep -n -E "conda env|entangled-equilibria|hardware_scaling.py" TODOS.md

**Convention 1, `conda run -n entangled-equilibria`. Measured: 17 lines, 9 files.**

| source |
| --- |
| docs/findings/2026-07-16-preregistered-peff-scaling-predictions.md:105 (`conda run -n entangled-equilibria python scripts/preregister_peff.py`) |
| docs/findings/2026-07-16-topology-vs-implementation-controls.md:147 (`conda run -n entangled-equilibria python scripts/topology_noise_controls.py`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:9 (`All commands use `conda run -n entangled-equilibria`.`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:41 (`conda run -n entangled-equilibria pip install qiskit==1.3.2`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:47 (`conda run -n entangled-equilibria python -c "import qiskit; print(qiskit.__version__)"`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:94 (`conda run -n entangled-equilibria pytest --collect-only`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:297 (`conda run -n entangled-equilibria pytest tests/test_ewl.py -v`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:452 (`conda run -n entangled-equilibria pytest tests/test_payoffs.py -v`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:613 (`conda run -n entangled-equilibria pytest tests/test_two_player.py -v`) |
| docs/superpowers/plans/2026-06-08-ewl-scaffold.md:765 (`conda run -n entangled-equilibria pytest -v`) |
| docs/superpowers/specs/2026-06-08-ewl-scaffold-design.md:23 (`**Python invocation:** `conda run -n entangled-equilibria python``) |
| docs/superpowers/specs/2026-06-08-ewl-scaffold-design.md:42 (`conda run -n entangled-equilibria pip install qiskit==1.3.2`) |
| scripts/judge_repeat_run.py:27 (`conda run -n entangled-equilibria python scripts/judge_repeat_run.py`) |
| scripts/n3_advantage.py:17 (`conda run -n entangled-equilibria python scripts/n3_advantage.py`) |
| scripts/preregister_peff.py:30 (`conda run -n entangled-equilibria python scripts/preregister_peff.py`) |
| scripts/topology_noise_controls.py:38 (`conda run -n entangled-equilibria python scripts/topology_noise_controls.py`) |
| TODOS.md:75 (`conda run -n entangled-equilibria python scripts/judge_repeat_run.py`) |

Anchors at :41 and :42 are prefixes; both lines continue with the full pip
dependency list.

A tenth location states the env in prose rather than as a command:
TODOS.md:43 (`**What:** Re-run `python experiments/hardware_scaling.py --hardware` (conda env`),
continuing to TODOS.md:44 (`` `entangled-equilibria`) on 3-5 different days.``).
This is the only place the hardware entry point is tied to an environment.

**Post-snapshot status (2026-07-19):** The counts and `live`
classifications below describe the b3469f0 snapshot. Commits dff79a4 and
cd5c094 replaced all 26 live non-conda command lines with the pinned
`conda run -n entangled-equilibria python` invocation. For changed rows,
the citation now anchors the current replacement.

**Convention 2, `.venv/bin/python`. Measured at snapshot: 3 lines, 2 files.**

| source | classification |
| --- | --- |
| results/README.md:61 (`conda run -n entangled-equilibria python scripts/run_experiment.py`) | live at snapshot; replaced by item 17 |
| results/README.md:62 (`conda run -n entangled-equilibria python scripts/topology_sweep.py`) | live at snapshot; replaced by item 17 |
| docs/findings/2026-07-17-item11-stale-claim-audit.md:456 (`Regeneration commands use `.venv/bin/python` vs the pinned`) | dated record, exempt |

No `.venv/` directory exists in the repo root.

**Convention 3, bare `PYTHONPATH=src python`. Measured at snapshot: 25 lines, 13 files.**

| source | classification |
| --- | --- |
| README.md:200 (`conda run -n entangled-equilibria python scripts/run_experiment.py --config experiments/noise-sweep.yaml`) | live at snapshot; replaced by item 17 |
| README.md:218 (`conda run -n entangled-equilibria python scripts/run_experiment.py`) | live at snapshot; replaced by item 17 |
| README.md:220 (`conda run -n entangled-equilibria python scripts/run_experiment.py --config experiments/config.yaml`) | live at snapshot; replaced by item 17 |
| README.md:250 (`conda run -n entangled-equilibria python scripts/draw_topology.py --topology star --N 5`) | live at snapshot; replaced by item 17 |
| README.md:251 (`conda run -n entangled-equilibria python scripts/draw_topology.py --topology ghz --N 4 --what both`) | live at snapshot; replaced by item 17 |
| README.md:252 (`conda run -n entangled-equilibria python scripts/draw_topology.py --topology full --N 6 --out /tmp/diag`) | live at snapshot; replaced by item 17 |
| scripts/draw_topology.py:4 (`conda run -n entangled-equilibria python scripts/draw_topology.py --topology star --N 5`) | live at snapshot; replaced by item 17 |
| scripts/draw_topology.py:5 (`conda run -n entangled-equilibria python scripts/draw_topology.py --topology ghz --N 4 --what both`) | live at snapshot; replaced by item 17 |
| scripts/draw_topology.py:6 (`conda run -n entangled-equilibria python scripts/draw_topology.py --topology ring --N 6 --out /tmp/diag`) | live at snapshot; replaced by item 17 |
| scripts/asymmetry_diagnostics.py:23 (`conda run -n entangled-equilibria python scripts/asymmetry_diagnostics.py             # ring N=5 p=0.02`) | live at snapshot; replaced by item 17 |
| scripts/asymmetry_diagnostics.py:24 (`conda run -n entangled-equilibria python scripts/asymmetry_diagnostics.py w 5 0.02`) | live at snapshot; replaced by item 17 |
| scripts/plot_hardware_scaling.py:18 (`conda run -n entangled-equilibria python scripts/plot_hardware_scaling.py            # all runs`) | live at snapshot; replaced by item 17 |
| scripts/plot_hardware_scaling.py:19 (`conda run -n entangled-equilibria python scripts/plot_hardware_scaling.py <run_dir> [<run_dir>..]`) | live at snapshot; replaced by item 17 |
| scripts/run_experiment.py:4 (`conda run -n entangled-equilibria python scripts/run_experiment.py`) | live at snapshot; replaced by item 17 |
| scripts/run_experiment.py:5 (`conda run -n entangled-equilibria python scripts/run_experiment.py --config path/to.yaml`) | live at snapshot; replaced by item 17 |
| scripts/t9_adaptation_pilot.py:29 (`conda run -n entangled-equilibria python scripts/t9_adaptation_pilot.py               # w 4, p in {0, 0.02, 0.05}`) | live at snapshot; replaced by item 17 |
| scripts/t9_adaptation_pilot.py:30 (`conda run -n entangled-equilibria python scripts/t9_adaptation_pilot.py ring 4 0.02`) | live at snapshot; replaced by item 17 |
| scripts/topology_optimal_strategy.py:17 (`conda run -n entangled-equilibria python scripts/topology_optimal_strategy.py            # ring, N=2..4`) | live at snapshot; replaced by item 17 |
| scripts/topology_optimal_strategy.py:18 (`conda run -n entangled-equilibria python scripts/topology_optimal_strategy.py ring 2 5`) | live at snapshot; replaced by item 17 |
| scripts/plot_hardware_result.py:14 (`conda run -n entangled-equilibria python scripts/plot_hardware_result.py \`) | live at snapshot; replaced by item 17 |
| scripts/topology_sweep.py:16 (`conda run -n entangled-equilibria python scripts/topology_sweep.py`) | live at snapshot; replaced by item 17 |
| experiments/config.yaml:6 (`#     conda run -n entangled-equilibria python scripts/run_experiment.py`) | live at snapshot; replaced by item 17 |
| experiments/noise-sweep.yaml:4 (`#   conda run -n entangled-equilibria python scripts/run_experiment.py --config experiments/noise-sweep.yaml`) | live at snapshot; replaced by item 17 |
| TODOS.md:84 (`conda run -n entangled-equilibria python scripts/plot_hardware_scaling.py`) | live at snapshot; replaced by item 17 |
| docs/superpowers/plans/2026-07-02-w-entangler-gate-level.md:375 (`PYTHONPATH=src python scripts/run_experiment.py --config experiments/noise-sweep.yaml`) | dated record, exempt |

At the snapshot, convention 3 resolved on this machine to python 3.9.13 with
qiskit 0.45.3 (see A1), which satisfied neither pyproject.toml:4
(`requires-python = ">=3.10"`) nor pyproject.toml:6 (`"qiskit==1.3.2",`).

### A5.1 Sweep classification rule

**The rule, in general form, for every documentation sweep in this repo, not
just this one.**

A file is exempt from a sweep if it records what was true at a point in time,
because rewriting it falsifies a record rather than fixing a defect. Everything
else is live and gets swept.

The test is what the file is for, not where it lives and not what filetype it
is. Docstrings inside `.py` files and comments inside `.yaml` files are
documentation that happens to be colocated with code; they prescribe behaviour
to a reader today, so they are live. A forward-looking work list is live even
with no date in its name. A findings document or a dated plan is a record even
though it is prose in `docs/`.

Applied to the interpreter conventions on 2026-07-18, this exempts exactly two
lines: docs/findings/2026-07-17-item11-stale-claim-audit.md:456 and
docs/superpowers/plans/2026-07-02-w-entangler-gate-level.md:375. A secondary
reason applies to the first, that it describes the convention as a defect rather
than prescribing it, but the record-integrity reason is primary and does not
depend on reading intent.

### A5.2 Counts, measured and target, kept separate

**Measured, from the printed commands.** Non-conda conventions combined:
**28 lines across 15 files.** Convention 2 contributes 3 lines / 2 files;
convention 3 contributes 25 lines / 13 files; no file appears in both.
Source: `grep -rln -E "\.venv/bin/python|PYTHONPATH=src python" --include=*.md --include=*.py --include=*.yaml --include=*.toml --exclude-dir=.venv-win --exclude-dir=.git --exclude-dir=graphify-out . | wc -l`
and the same with `-rn ... | wc -l`.

**Sweep target. This is a judgment made 2026-07-18, not a measurement, and item
17 may overrule it without re-deriving anything.** 26 lines across 13 files,
being the measured 28 minus the 2 dated-record lines exempted by A5.1.

**Execution breakdown of the 26, for whoever runs item 17:**

| number | meaning |
| --- | --- |
| 26 lines / 13 files | sweep target |
| 2 lines | subsumed: results/README.md:45 and :46, rewritten in full by item 17 deliverable (d), not by the mechanical pass |
| 24 lines / 12 files | mechanical pass |

Recorded so nobody executing item 17 double-edits those two lines or concludes a
line was missed.

**Note for item 17.** 15 of the 24 mechanical lines sit in source files, 13 in
`scripts/*.py` docstrings and 2 in `experiments/*.yaml` comments. Those edits
must be text-only with zero behaviour change; run the test suite afterward as a
no-op check.

**Exclusion declared.** All three convention commands carry
`--exclude-dir=graphify-out`. `graphify-out/` is generated knowledge-graph
output (top-level contents `graph.json`, `graph.html`, `GRAPH_REPORT.md`,
`manifest.json`, `cost.json`, `cache/`, `memory/`; source `ls graphify-out/`),
ignored at .gitignore:55 (`graphify-out/`). It is excluded because its contents
are tool-generated summaries of the repo rather than repo documentation, so
counting them would inflate the convention counts with restatements. Stated so
every count beside a command is reproducible from that command as printed. Note
that 62 files under it are tracked despite the ignore
(`git ls-files -- graphify-out | wc -l`). See G12.

**Stale downstream reference.** Any prompt citing "section A3" or "the 17
sources" for the interpreter sweep is stale on both halves. The sweep is A5, and
17 is convention 1's line count, which is the correct convention and not part of
the sweep.

### A6. What references `.venv-win/`

Two references exist, both created 2026-07-18 in this session:
.gitignore:10 (`.venv-win/`), introduced by commit b3469f0, and
TODOS.md:23 (`` `fake_provider` files under `.venv-win/`.``), introduced by
commit b608375.

Source: `grep -rn "venv-win" --exclude-dir=.venv-win --exclude-dir=.git .`

No commit on any branch created the directory.
`git log --all -i --oneline --grep=venv` returns exactly one commit, fc71749
"Fix: Deleted venv directory", which concerns a different directory.

No requirements or lock file exists inside `.venv-win/`; the only file at its
root is pyvenv.cfg.
Source: `ls .venv-win/*.txt .venv-win/*.lock .venv-win/*.cfg`

The purpose of `.venv-win/` is NOT IN REPO. Locations checked: all tracked files
via the grep above, all branch history via the git log grep, and the venv root
for a dependency manifest.

### A7. Whether the documented bare-python commands can run

At the snapshot commit, they could not run on this machine, and the cause was
not qiskit.

    PYTHONPATH=src python -c "import game.nash; print('ok')"

failed at src/game/nash.py:24
(`from typing import Any, Callable, TypeAlias`) with
`ImportError: cannot import name 'TypeAlias' from 'typing'`.

At the snapshot commit, the representative README quickstart entry point used
bare `PYTHONPATH=src python`. Running that historical command in `--help` form
so it touched no hardware and wrote nothing to results/:

    PYTHONPATH=src python scripts/run_experiment.py --help

failed with the same root cause, through this import chain:
scripts/run_experiment.py:30 (`from experiment import load_config, run_sweep, write_outputs  # noqa: E402`)
to src/experiment/__init__.py:16 (`from experiment.report import write_outputs`)
to src/experiment/report.py:17 (`from experiment.sweep import (`)
to src/experiment/sweep.py:18 (`from circuits.noise import build_ewl_circuit_noisy`)
to src/circuits/noise.py:36 (`from circuits.ewl import U, StrategyParams`)
to src/circuits/ewl.py:8 (`from typing import TypeAlias`).

`typing.TypeAlias` requires Python 3.10. The failure occurred at import time,
before any qiskit code executed, and would have occurred identically regardless
of which qiskit version the bare interpreter carried. src/ genuinely requires
the version declared at pyproject.toml:4 (`requires-python = ">=3.10"`).

**Post-snapshot status:** item 17 replaced that quickstart with README.md:218
(`conda run -n entangled-equilibria python scripts/run_experiment.py`). The
import failure above remains a record of the removed bare-Python convention; it
is not a claim about the current quickstart.

---

## B. Hardware runs, backends, job ids, and what the artifacts record

### B0. Extraction limitations, stated

**Job id pattern.** Job ids were enumerated with the pattern `d9[a-z0-9]{18}`.
An id not beginning with `d9` would not be matched. This is accepted rather than
widened, because the pattern is cross-checked against two authoritative sources
that do not depend on it: results/hardware-scaling/pending_jobs.txt, which lists
every submission, and the `job_id` fields of each result.json. A job id present
in neither of those and not starting with `d9` would be missed by this
extraction.

**Git-hash false positives.** The same pattern matches substrings of git commit
hashes stored in the artifacts. One such match, `d9452fef157fde02eff8`, is a
fragment of the commit hash at
results/hardware-scaling/2026-07-17T014458Z/result.json:5
(`"commit": "cd8318b76d9452fef157fde02eff8f452512e8e4",`) and is excluded. It is
not a job id.

**Interpreter.** Values in this section were read with `grep`, `find`, and
`cat`, no interpreter involved. The JSON structure probes described in B4 ran
under the bare PATH interpreter (python 3.9.13, see A1), which is acceptable
because they use only the `json` stdlib module and read no repo code.

### B1. Every file in the hardware run directories

Source: `find results/hardware-scaling results/hardware-n3 -type f | sort`

Each of the three run directories contains exactly five files:
`calibration.json`, `result.json`, and three under `plots/` (`caption.md`, a
`.pdf`, a `.png`).

Four additional files sit at results/hardware-scaling/ root: `pending_jobs.txt`,
`preregistration.json`, `preregistration-baselines.json`,
`repeat-judgments.json`.

**No log, launch-info, or environment-capture file exists in any hardware run
directory.** The `launch-info.txt` / `run.log` / `run.err` pattern used
elsewhere in results/ is absent here.

### B2. `results/hardware-n3/2026-07-16T013912Z`

| field | value | source |
| --- | --- | --- |
| experiment | hardware-n3-ghz | result.json:2 (`"experiment": "hardware-n3-ghz",`) |
| created_utc | 2026-07-16T01:39:12.716554+00:00 | result.json:3 (`"created_utc": "2026-07-16T01:39:12.716554+00:00",`) |
| git commit | d5b4b1259ba7c9bccdc0a6d60b78cd13f31d4ea8 | result.json:5 (`"commit": "d5b4b1259ba7c9bccdc0a6d60b78cd13f31d4ea8",`) |
| git dirty | true | result.json:6 (`"dirty": true`) |
| backend | ibm_fez | result.json:8 (`"backend": "ibm_fez",`), calibration.json:2 (`"backend": "ibm_fez",`) |
| job_id | d9br6l66hjac73fg3g7g | result.json:9 (`"job_id": "d9br6l66hjac73fg3g7g",`), calibration.json:3 (same) |
| shots | 4096 | result.json:10 (`"shots": 4096,`) |
| N | 3 | result.json:11 (`"N": 3,`) |
| qubit chain | key is `physical_qubits_logical_order`, not `chain` | calibration.json:4 (`"physical_qubits_logical_order": [`) |
| calibration_last_update | 2026-07-15 18:24:06+05:30 | calibration.json:9 (`"calibration_last_update": "2026-07-15 18:24:06+05:30",`) |
| distinct_calibration_vs_previous_runs | NOT IN REPO. That field exists only in repeat-judgments.json, which does not cover this run. | |
| is_registration_source | NOT IN REPO, same reason. | |
| python / qiskit / qiskit-ibm-runtime version | NOT IN REPO. See B4. | |

This run uses a different qubit-chain key and a different calibration epoch from
the two scaling runs, and is a separate experiment.

### B3. The first two hardware-scaling runs

(Run 3 `2026-07-25T035623Z` is covered in section C; the two 2026-07-25 batches
are in B3.1.)

| field | run 1 | run 2 |
| --- | --- | --- |
| directory | results/hardware-scaling/2026-07-16T074134Z | results/hardware-scaling/2026-07-17T014458Z |
| experiment | hardware-scaling-n345, result.json:2 (`"experiment": "hardware-scaling-n345",`) | hardware-scaling-n345, result.json:2 (same) |
| created_utc | 2026-07-16T07:41:34.466740+00:00, result.json:3 | 2026-07-17T01:44:58.964811+00:00, result.json:3 |
| git commit | 9248bb230e7d2c96f2733cf6b22e50138ab1cfee, result.json:5 | cd8318b76d9452fef157fde02eff8f452512e8e4, result.json:5 |
| git dirty | true, result.json:6 (`"dirty": true`) | true, result.json:6 (`"dirty": true`) |
| job_id | d9c8fpn550hc73dl1tcg, result.json:9 (`"job_id": "d9c8fpn550hc73dl1tcg",`) | d9cohq1htsac739c1iu0, result.json:9 (`"job_id": "d9cohq1htsac739c1iu0",`) |
| backend | ibm_fez, result.json:10, calibration.json:2 | ibm_fez, result.json:10, calibration.json:2 |
| **recovered** | **true**, result.json:11 (`"recovered": true`) | **key absent** |
| shots | 4096, result.json:13 (`"shots": 4096,`) | 4096, result.json:12 (`"shots": 4096,`) |
| calibration_last_update | 2026-07-16 08:30:13+05:30, calibration.json:3 | 2026-07-16 08:30:13+05:30, calibration.json:3 |
| chain | key `chain`, calibration.json:4 (`"chain": [`) | key `chain`, calibration.json:4 (`"chain": [`) |
| python / qiskit / runtime | NOT IN REPO. See B4. | NOT IN REPO. See B4. |

**The two calibration_last_update values are identical**, byte for byte, despite
the runs being 18 hours apart in submission time. See G15 for why this may be
mechanical rather than meaningful.

**Run 1 was recovered, run 2 was not.** Run 1 carries `"recovered": true`; run
2's job object has no such key. Per experiments/hardware_scaling.py, the
`--from-job` mode reconstructs the plan from the submitted job's own circuits
rather than polling a live submission. What this implies about run 1's execution
path is not determined here; the fact recorded is the flag's presence and
absence.

### B3.1 The 2026-07-25 runs (topology batch and N=3..7 extension)

| field | topology batch | N=3..7 extension |
| --- | --- | --- |
| directory | results/hardware-topology/2026-07-25T114621Z | results/hardware-scaling/2026-07-25T180549Z |
| experiment | hardware-topology, result.json:2 (`"experiment": "hardware-topology",`) | **hardware-scaling-n345**, result.json:2 (`"experiment": "hardware-scaling-n345",`) — see the mislabel note below |
| created_utc | 2026-07-25T11:46:21.848162+00:00, result.json:3 | 2026-07-25T18:05:49.016021+00:00, result.json:3 |
| job_id | d9ia1pd0k0jc738jaqgg, result.json:22 (`"job_id": "d9ia1pd0k0jc738jaqgg",`) | d9if010gk0ls73f4avkg, result.json:23 (`"job_id": "d9if010gk0ls73f4avkg",`) |
| shots | 4096, result.json:25 (`"shots": 4096,`) | 4096, result.json:26 (`"shots": 4096,`) |
| calibration_last_update at submit | 2026-07-25 16:05:46+05:30, calibration_at_submit.json:3 | 2026-07-25 22:32:49+05:30, calibration_at_submit.json:3 |
| pubs | 49 | 17 |

**`experiment` is mislabelled on the extension run.** It records
`"hardware-scaling-n345"` while the run covers N=3..7. The string is a literal
in `experiments/hardware_scaling.py`'s `save_run` payload and was not
parameterised when `--ns` was added. The `pub_meta` block carries the true N
values, so nothing downstream is wrong, but a consumer keying off `experiment`
alone would misread the run's scope. Not corrected here: editing the artifact
after the fact would be worse than the label.

**ibm_fez recalibrated three times on 2026-07-25**: 08:15:48 (topology
registration), 16:05:46 (topology submission), 22:32:49 (extension submission),
all +05:30. The topology batch was registered under the first and executed
under the second, and its qubit selector moved the pinned set as a result —
this is the confound recorded in
`docs/findings/2026-07-25-topology-hardware-run1.md`. The extension pinned its
chain explicitly and so was unaffected despite a further recalibration:
judgments-n67.json:28 (`"chain_matches": true,`).

### B4. What the artifacts do not record

**No environment metadata exists in any hardware artifact.** A case-insensitive
search across all five JSON files in the three run directories for the keys
`python`, `qiskit`, `version`, `runtime`, `env`, `environment`, and `packages`
returns **zero hits**.

Source:

    grep -rn -i -E "\"python\"|\"qiskit\"|\"version\"|\"runtime\"|\"env\"|\"environment\"|\"packages\"" results/hardware-n3/2026-07-16T013912Z/ results/hardware-scaling/2026-07-16T074134Z/ results/hardware-scaling/2026-07-17T014458Z/ --include=*.json | wc -l

**Which qiskit or qiskit-ibm-runtime version submitted any job: NOT IN REPO.**
Locations checked: all five JSON files per run directory (B1), pending_jobs.txt
(B5), and the absence of any log or launch-info file (B1). Simulation runs do
record a python version; confirmed in F2.

All three runs record a git commit with `dirty: true`, meaning the working tree
had uncommitted changes at run time, so the commit alone does not identify the
code that ran. See G16.

**The in-repo template for the missing environment block.**
results/hardware-scaling/preregistration.json:11-17 records
`"python": "3.10.20"` (:12), `"qiskit": "1.3.2"` (:13),
`"qiskit_aer": "0.14.2"` (:14), `"numpy": "1.26.4"` (:15),
`"scipy": "1.13.1"` (:16), matching the conda env measured in A1 exactly.

**This does not weaken the finding above.** `preregistration.json` is written by
`scripts/preregister_peff.py` running locally; it is not a hardware artifact and
records the environment of the fit, not of any job submission. What it shows is
that the project already has the pattern, applied in one place and not the
other. Item 16 should copy this block into the hardware save path rather than
design one. Cross-referenced from C1 and G16.

### B5. pending_jobs.txt

Source: `cat -n results/hardware-scaling/pending_jobs.txt`

    1  2026-07-16T07:27:34.364857+00:00  ibm_fez  d9c8fpn550hc73dl1tcg
    2  2026-07-16T17:44:34.029154+00:00  ibm_fez  d9chh0qneu4c739lvgb0
    3  2026-07-17T01:44:08.624953+00:00  ibm_fez  d9cohq1htsac739c1iu0

Three columns: submission timestamp, backend, job id. **No version column.**

Line 1's submission timestamp, 07:27:34Z, precedes run 1's result.json
`created_utc` of 07:41:34Z by 14 minutes, consistent with a submission followed
by a result write.

### B6. Every job id in the repo

Four genuine job ids exist. All four appear in five or more files.
**No job id appears in only one place.**

Source per id:
`grep -rn "<id>" --exclude-dir=.venv-win --exclude-dir=.git --exclude-dir=graphify-out -I .`

**d9br6l66hjac73fg3g7g**, N=3 run. 5 occurrences, 5 files:
experiments/fetch_result.py:8, experiments/hardware_scaling.py:83,
paper/main.tex:215, results/hardware-n3/2026-07-16T013912Z/calibration.json:3,
results/hardware-n3/2026-07-16T013912Z/result.json:9.

**d9c8fpn550hc73dl1tcg**, run 1. 12 occurrences, 11 files:
docs/findings/2026-07-16-preregistered-peff-scaling-predictions.md:4,
docs/findings/2026-07-17-item11-stale-claim-audit.md:69 and :407,
paper/main.tex:232,
results/hardware-scaling/2026-07-16T074134Z/plots/caption.md:1,
results/hardware-scaling/2026-07-16T074134Z/result.json:9,
results/hardware-scaling/2026-07-17T014458Z/plots/caption.md:1,
results/hardware-scaling/pending_jobs.txt:1,
results/hardware-scaling/preregistration.json:6,
results/hardware-scaling/repeat-judgments.json:12,
scripts/preregister_peff.py:4, TODOS.md:51.

Run 2's caption cites run 1's job id, consistent with the scaling plot
aggregating all runs.

**d9chh0qneu4c739lvgb0.** Measured: appears at
results/hardware-scaling/pending_jobs.txt:2
(`2026-07-16T17:44:34.029154+00:00	ibm_fez	d9chh0qneu4c739lvgb0`), and in no
`result.json` in the repository. 8 occurrences, 6 files:
docs/findings/2026-07-16-preregistered-baseline-competitors.md:12 and :103,
docs/findings/2026-07-17-run2-repeat-judgment.md:89,
results/hardware-scaling/pending_jobs.txt:2,
results/hardware-scaling/preregistration-baselines.json:4,
scripts/preregister_baselines.py:30 and :175, TODOS.md:53.

Interpretation, not measurement: TODOS.md:53
(`d9chh0qneu4c739lvgb0 failed backend-side (error 9603, RF hardware, during`)
records it as a backend-side failure with 0 quantum seconds billed. That is a
work-log entry written by the project, not a provider-issued artifact; no error
record from IBM exists in the repo. At registration time it was still queued,
per docs/findings/2026-07-16-preregistered-baseline-competitors.md:12.

**d9cohq1htsac739c1iu0**, run 2. 5 occurrences, 5 files:
docs/findings/2026-07-17-run2-repeat-judgment.md:16,
results/hardware-scaling/2026-07-17T014458Z/result.json:9,
results/hardware-scaling/pending_jobs.txt:3,
results/hardware-scaling/repeat-judgments.json:281, TODOS.md:52.

**d8nvd2bqv2lc7389d9e0: NOT IN REPO.**
`grep -rn "d8nvd2bqv2lc7389d9e0" . | wc -l` returns **0**, searching every file
including ignored directories and binaries. This job id is unknown to this
repository. It does not begin with `d9` and so would also be missed by the
enumeration pattern in B0; the zero-hit literal search above does not depend on
that pattern and is the authoritative check.

---

## C. Run outcomes from repeat-judgments.json, both runs, all N

Single source for every value in this section:
`results/hardware-scaling/repeat-judgments.json`, generated
2026-07-25T03:57:31.164219+00:00 (repeat-judgments.json:2
(`"generated_utc": "2026-07-25T03:57:31.164219+00:00",`)).

Registration status is stated per subsection and sourced to
`results/hardware-scaling/preregistration.json` or
`results/hardware-scaling/preregistration-baselines.json`. Both were read only
and neither was modified.

Run 1 is `2026-07-16T074134Z` (repeat-judgments.json:11
(`"run": "2026-07-16T074134Z",`)). Run 2 is `2026-07-17T014458Z`
(repeat-judgments.json:280 (`"run": "2026-07-17T014458Z",`)). Run 3 is
`2026-07-25T035623Z` (repeat-judgments.json:549
(`"run": "2026-07-25T035623Z",`)).

**Distinct calibration days is 2, not 3.** Run 2 carries
`"distinct_calibration_vs_previous_runs": false` — it shares run 1's
calibration stamp, so runs 1 and 2 are ONE calibration day. Run 3 is the first
genuinely distinct one. The registered target is 3–5 distinct days, so this is
2 of 3–5. Any cross-day uncertainty estimate must use this count, not the
number of runs.

### C1. p_eff

| value | number | source |
| --- | --- | --- |
| registered central | 0.001837649512845019 | preregistration.json:48 (`"central": 0.001837649512845019,`), echoed at repeat-judgments.json:6 |
| registered sigma | 0.00032952732404180015 | preregistration.json:49 (`"sigma": 0.00032952732404180015,`) |
| registration timestamp | 2026-07-16T17:04:36.363760+00:00 | preregistration.json:2 (`"registered_utc": "2026-07-16T17:04:36.363760+00:00",`) |
| run 1 refit | 0.001837649512845019 | repeat-judgments.json:25 |
| run 2 refit | 0.0016456338927582697 | repeat-judgments.json:294 |

Run 1's refit equals the registered central value exactly because run 1 is the
registration source (preregistration.json:5
(`"dir": "results/hardware-scaling/2026-07-16T074134Z",`), and
repeat-judgments.json:24 (`"is_registration_source": true,`)).

The environment under which this registration was computed is recorded at
preregistration.json:11-17; see B4.

**Registration status: preregistered.** The central value and its uncertainty
were committed before any repeat run landed (preregistration.json:3
(`N=4,5 advantages are predictions committed BEFORE any repeat batch run.`)).

### C2. Conditional primary test

**Run 1**

| N | field | value | source |
| --- | --- | --- | --- |
| 4 | predicted_conditional | 0.7426904519741249 | repeat-judgments.json:28 |
| 4 | measured | 0.7384272699895833 | repeat-judgments.json:29 |
| 4 | delta | -0.004263181984541564 | repeat-judgments.json:30 |
| 4 | z | -2.14483755652589 | repeat-judgments.json:31 |
| 4 | sigma_predictive | 0.0019876479557020027 | repeat-judgments.json:32 |
| 4 | pass_95 | false | repeat-judgments.json:33 (`"pass_95": false`) |
| 5 | predicted_conditional | 0.5931700156036097 | repeat-judgments.json:36 |
| 5 | measured | 0.5831190172535277 | repeat-judgments.json:37 |
| 5 | delta | -0.010050998350082052 | repeat-judgments.json:38 |
| 5 | z | -5.166738914507109 | repeat-judgments.json:39 |
| 5 | sigma_predictive | 0.0019453273169776348 | repeat-judgments.json:40 |
| 5 | pass_95 | false | repeat-judgments.json:41 (`"pass_95": false`) |

**Run 2**

| N | field | value | source |
| --- | --- | --- | --- |
| 4 | predicted_conditional | 0.7434293298233563 | repeat-judgments.json:297 |
| 4 | measured | 0.7415761349129972 | repeat-judgments.json:298 |
| 4 | delta | -0.0018531949103590684 | repeat-judgments.json:299 |
| 4 | z | -0.9323557046622736 | repeat-judgments.json:300 |
| 4 | sigma_predictive | 0.0019876479557020027 | repeat-judgments.json:301 |
| 4 | pass_95 | **true** | repeat-judgments.json:302 (`"pass_95": true`) |
| 5 | predicted_conditional | 0.5938528682272297 | repeat-judgments.json:305 |
| 5 | measured | 0.5846250840823848 | repeat-judgments.json:306 |
| 5 | delta | -0.00922778414484493 | repeat-judgments.json:307 |
| 5 | z | -4.743563751102674 | repeat-judgments.json:308 |
| 5 | sigma_predictive | 0.0019453273169776348 | repeat-judgments.json:309 |
| 5 | pass_95 | false | repeat-judgments.json:310 (`"pass_95": false`) |

`sigma_predictive` is identical across both runs at each N, consistent with the
shared-yardstick design.

**Registration status: preregistered.** The test is defined at
preregistration.json:43
(`"conditional (primary, drift-robust)": "for each repeat run: refit p_eff on that run's N=3 mitigated fold-1 payoff;`),
which specifies refitting p_eff on each run's N=3 and judging that run's N=4 and
N=5 against 95% predictive intervals recentred on the refit prediction using the
same sigma_predictive.

### C3. n5_deficit block

| field | run 1 | run 2 |
| --- | --- | --- |
| delta | -0.010050998350082052, repeat-judgments.json:45 | -0.00922778414484493, repeat-judgments.json:314 |
| z | -5.166738914507109, repeat-judgments.json:46 | -4.743563751102674, repeat-judgments.json:315 |
| registered_run1_delta | -0.010050998350082052, repeat-judgments.json:47 | -0.010050998350082052, repeat-judgments.json:316 |
| registered_run1_z | -5.166738914507109, repeat-judgments.json:48 | -5.166738914507109, repeat-judgments.json:317 |
| same_sign_as_run1 | true, repeat-judgments.json:49 | true, repeat-judgments.json:318 |

The run-1 reference values match preregistration.json's `source_run_comparison`
for N=5 exactly: preregistration.json:219 (`"delta": -0.010050998350082052,`)
and preregistration.json:220 (`"z": -5.166738914507109`), held under
`source_run_comparison["5"]["mitigated_fold1"]` (preregistration.json:216
(`"mitigated_fold1": {`)). The judge reads its references from the registration
rather than recomputing them.

**Registration status: split.** The run-1 reference values are preregistered,
held in preregistration.json's `source_run_comparison` block
(preregistration.json:186 (`"source_run_comparison": {`)). **The
sign-reproduction criterion is not.** See G17.

### C4. Five-model comparison

| model | run 1 score_z2 | run 2 score_z2 |
| --- | --- | --- |
| p_eff_primary | 31.29551915456605, repeat-judgments.json:154 | 23.37068422079156, repeat-judgments.json:423 |
| cz_exponential | 10.032095975636892, repeat-judgments.json:155 | 7.399852402490573, repeat-judgments.json:424 |
| device_model_anchored | 38.862284568361446, repeat-judgments.json:156 | 27.563697136876158, repeat-judgments.json:425 |
| constant_retention | 46.03168503448163, repeat-judgments.json:157 | 34.410774522717176, repeat-judgments.json:426 |
| transpiled_count_corrected | 29.93261198678005, repeat-judgments.json:158 | 22.25480363450175, repeat-judgments.json:427 |

`ranking_best_first` is identical in both runs (repeat-judgments.json:160
(`"ranking_best_first": [`) and :429 (same)):

    cz_exponential, transpiled_count_corrected, p_eff_primary,
    device_model_anchored, constant_retention

**Registration status: preregistered, explicitly secondary.** The four
competitor models are defined at preregistration-baselines.json:10-13,
registered 2026-07-16T18:25:30.397235+00:00 (preregistration-baselines.json:2
(`"registered_utc": "2026-07-16T18:25:30.397235+00:00",`)), before batch 2
returned (preregistration-baselines.json:4
(`"pending_job_not_yet_returned": "d9chh0qneu4c739lvgb0",`)). The scoring rule
is registered at preregistration-baselines.json:21
(`"score": "z4^2 + z5^2 per run, cumulative across repeats; lower is better;`).

That file states its own subordinate status at preregistration-baselines.json:3
(`SECONDARY to the primary p_eff registration (preregistration.json, untouched).`)
and at :20 that the shared sigma yields
`model-comparison scores, not per-competitor calibrated intervals`. The scores
rank models against each other; they are not calibrated pass/fail tests.

### C5. Per-player advantages, N=5

**Run 1 raw**, value lines repeat-judgments.json:247-251:
0.5713216145833333, 0.5723795572916668, 0.5779947916666668, 0.5823893229166666,
0.6146158854166668.
worst 0.5713216145833333 (:253), spread 0.04329427083333337 (:254),
any_player_below_classical false (:255 (`"any_player_below_classical": false`)).

**Run 1 mitigated**, value lines repeat-judgments.json:266-270:
0.5685539934051271, 0.5795399989045174, 0.5719522204521466, 0.5732905905982917,
0.6222582829075554.
worst 0.5685539934051271 (:272), spread 0.053704289502428115 (:273),
any_player_below_classical false (:274).

**Run 2 raw**, value lines repeat-judgments.json:516-520:
0.5722493489583333, 0.5657389322916666, 0.5721679687500001, 0.5882812500000001,
0.6275878906249999.
worst 0.5657389322916666 (:522), spread 0.06184895833333326 (:523),
any_player_below_classical false (:524).

**Run 2 mitigated**, value lines repeat-judgments.json:535-539:
0.5660502563047922, 0.5686312446217308, 0.5693112326199914, 0.5841782080462852,
0.634954478819125.
worst 0.5660502563047922 (:541), spread 0.06890422251433281 (:542),
any_player_below_classical false (:543).

Index 4 holds the maximum in all four vectors. `any_player_below_classical` is
false in every block at every N in both runs.

**Registration status: not preregistered.** See G18.

---

## D. Game theory and the Nash claim

### D1. V and C

The live convention is **V=4, C=3**, consistent across all four sources.

| source | value |
| --- | --- |
| src/config.py:35 (`V: float = 4.0  # resource value`) | V = 4.0 |
| src/config.py:36 (`C: float = 3.0  # conflict cost (C > V/2 ensures Hawk-Dove dynamics are non-trivial)`) | C = 3.0 |
| experiments/config.yaml:70 (`V: 4`) | V = 4 |
| experiments/config.yaml:73 (`C: 3`) | C = 3 |
| experiments/noise-sweep.yaml:37 (`V: 4.0`) | V = 4.0 |
| experiments/noise-sweep.yaml:38 (`C: 3.0`) | C = 3.0 |

`src/config.py` is the single definition; the game modules import from it under
aliases rather than redefining, at
src/game/nash.py:32 (`from config import C as DEFAULT_C, GAMMA, V as DEFAULT_V`),
src/game/payoffs.py:16 (`from config import C as DEFAULT_C, V as DEFAULT_V`),
and src/game/strategy_opt.py:47
(`from config import C as DEFAULT_C, GAMMA, V as DEFAULT_V`).

### D2. Pure quantum NE at N=3, 4, 5, and the deviations that break it

Values produced by running the repository's own code under the conda env, with
default GHZ entangler and default V=4, C=3:

    PYTHONPATH=src conda run -n entangled-equilibria python <script>

| N | q_is_nash | Q payoff per player | classical NE payoff | advantage |
| --- | --- | --- | --- | --- |
| 3 | **True** | 1.3333333333333333 | 0.33333333333333331 | 1 |
| 4 | **False** | 1 | 0.25 | 0.75 |
| 5 | **False** | 0.80000000000000004 | 0.20000000000000001 | 0.60000000000000009 |

Unilateral deviation payoffs from the all-Q profile. Every player's values are
identical at each N, consistent with GHZ being vertex-transitive.

| N | deviate to Dove | deviate to Hawk | Hawk beats Q payoff? |
| --- | --- | --- | --- |
| 3 | 0.58333333333333348 | 1 | no, 1 < 1.3333333333333333 |
| 4 | 0.62500000000000022 | **2.0000000000000009** | **yes**, 2.0 > 1 |
| 5 | 0.5927050983124843 | **2.6180339887498949** | **yes**, 2.618 > 0.8 |

Each `deviation_check` entry is keyed `(player, alt)` and carries the key
`deviation_payoff`; the values above are those entries.

### D3. The code that computes it

| element | source |
| --- | --- |
| pure-NE search | src/game/nash.py:103 (`def find_pure_nash(`) |
| deviation substitution | src/game/nash.py:129 (`deviation[player] = alt`) |
| deviation payoff lookup | src/game/nash.py:130 (`dev_payoff = tensor[tuple(deviation)][player]`) |
| advantage entry point | src/game/nash.py:142 (`def compute_advantage(`) |
| NE membership test | src/game/nash.py:249 (`q_is_nash = q_profile in all_nash`) |
| deviation table assembly | src/game/nash.py:263 (`deviation_check[(player, alt)] = {`) |
| returned NE flag | src/game/nash.py:277 (`"q_is_nash": q_is_nash,`) |
| returned deviation table | src/game/nash.py:280 (`"deviation_check": deviation_check,`) |

### D4. What the test suite actually pins

**Three tests assert `q_is_nash is True`. All three are N=3.**

| source | what it covers |
| --- | --- |
| tests/test_nash_advantage.py:19 (`assert r["q_is_nash"] is True`) | GHZ N=3, via `compute_advantage(N=3)` at :18 |
| tests/test_topology_sweep.py:71 (`assert r["q_is_nash"] is True`) | GHZ N=3, docstring at :68 |
| tests/test_experiment.py:58 (`assert res.q_is_nash is True`) | a sweep cell asserting advantage 1.0 at :57, the N=3 GHZ signature |

**No test asserts `q_is_nash is False` at N=4 or N=5 for any topology.**

The closest case is tests/test_asymmetric_advantage.py:89
(`r = compute_advantage(N=4, V=_V, C=_C, entangler=ghz_entangler)`), which calls
GHZ at N=4 but asserts only symmetry at :90 (`assert r["symmetric"] is True`)
and uniformity of the advantage vector at :92. It does not touch `q_is_nash`.

Other `q_is_nash` occurrences in tests are not NE assertions on computed runs:
tests/test_noise.py:173 is a comment, tests/test_topology_sweep.py:47 is a key
list, and tests/test_topology_sweep.py:147-149 assert a formatting helper
against hand-built dicts.

See G9.

### D5. Raw sweep, N=2 to N=8

| N | q_is_nash | q_payoff_per_player | classical_ne_payoff | advantage | deviate to Dove | deviate to Hawk |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | True | 2 | 0.5 | 1.5 | 0.5 | 1.6872297554945904e-32 |
| 3 | True | 1.3333333333333333 | 0.33333333333333331 | 1 | 0.58333333333333348 | 1 |
| 4 | False | 1 | 0.25 | 0.75 | 0.62500000000000022 | 2.0000000000000009 |
| 5 | False | 0.80000000000000004 | 0.20000000000000001 | 0.60000000000000009 | 0.5927050983124843 | 2.6180339887498949 |
| 6 | False | 0.66666666666666663 | 0.16666666666666666 | 0.5 | 0.5416666666666663 | 2.9999999999999973 |
| 7 | False | 0.57142857142857129 | 0.14285714285714282 | 0.42857142857142849 | 0.49074781468401435 | 3.2469796037174672 |
| 8 | False | 0.49999999999999978 | 0.125 | 0.37499999999999978 | 0.44508252147247762 | 3.4142135623730949 |

**Candidate identities, as computed. Not proven, not fitted.**

| identity | holds for N=2..8 as computed |
| --- | --- |
| q_payoff_per_player == V/N, i.e. 4/N | **yes** |
| classical_ne_payoff == 1/N | **yes** |
| advantage == (V-1)/N, i.e. 3/N | **yes** |
| deviation to Hawk == 2 + 2*cos(2*pi/N) | **yes** |

All four hold within 1e-12 at every N from 2 to 8. None holds under exact float
equality, which is expected: these are outputs of floating-point circuit
simulation, not closed-form arithmetic. The fourth subsumes the phi^2 value at
N=5 as the special case 2 + 2*cos(2*pi/5) = phi^2 = 2.6180339887498949, phi
being the golden ratio, which does match under exact float equality.

**Equilibrium boundary.** Measured `q_is_nash` agrees with the inequality
`2 + 2*cos(2*pi/N) <= V/N` at every N from 2 to 8, with no disagreement.
Recorded as: the inequality is consistent with q_is_nash for N=2..8 as computed.
Not proven. No derivation is given here; that belongs to item 14 if anywhere.

The Dove deviation never binds: it is below the Q payoff at every N in the
sweep, so the Hawk deviation alone determines the boundary in this range.

---

## E. Repository and git state

### E1. Git state

**This section snapshots the repository immediately before this file's own
commit.** A reader who finds HEAD at a different commit than the one recorded
here is looking at a later state; that is expected, not a defect.

| fact | value | source |
| --- | --- | --- |
| branch | `dev` | `git rev-parse --abbrev-ref HEAD` |
| HEAD | b3469f020dd2beb0ea92fc3c8366ff57467b428c | `git rev-parse HEAD` |
| working tree | clean, zero entries | `git status --porcelain` returned empty |
| ahead of origin/main | 6 commits | `git rev-list --count origin/main..HEAD` |
| **behind origin/main** | **1 commit** | `git rev-list --count HEAD..origin/main` |

**The branch has diverged.** `dev` is both ahead and behind. The commit
`origin/main` holds that `dev` lacks is 195e122, 2026-07-17 22:08:54 +0530,
"Merge pull request #14 from Prithvi8706/dev"
(`git log --format="%h %ci %s" HEAD..origin/main`). Any statement that `dev` is
"6 ahead" without the behind count implies a fast-forward merge that is not
available.

**Freshness of the comparison.** `origin/main` is a local remote-tracking ref.
It was last updated by a fetch at 2026-07-18 08:20 (`ls -la .git/FETCH_HEAD`).
The counts above are relative to that ref as of that fetch. No fetch was
performed while writing this file.

The 6 commits ahead, newest first
(`git log --format="%h %s" origin/main..HEAD`):

    b3469f0  chore: gitignore local env and tool directories
    b608375  todos: log item-11 marrakesh backend-attribution residue
    3a41813  findings: run-2 repeat judgment prose record + player-4 position effect cross-reference
    9e8ef50  Merge branch 'dev' of https://github.com/QuantumCompTeam/Multiplayer-QHD-Game into dev
    2996528  item-11: repo-wide stale-claim audit ...
    56b18b8  Merge pull request #13 from Prithvi8706/dev

b3469f0 and b608375 were both made during this session and are responsible for
four of the citation failures recorded in G13.

### E2. Tracking under results/ and graphify-out/

| fact | value | source |
| --- | --- | --- |
| tracked files under results/ | 50, 4.2M | `git ls-files -- results \| wc -l` |
| ignored-but-present under results/ | 126, 3.1M | `git ls-files --others --ignored --exclude-standard -- results \| wc -l` |
| tracked files under graphify-out/ | 62 | `git ls-files -- graphify-out \| wc -l` |

Both directories are blanket-ignored, results/ at .gitignore:52 (`results/`) and
graphify-out/ at .gitignore:55 (`graphify-out/`), yet both carry tracked
content. See G1 and G12.

### E3. Run directories, committed and not

**Committed, meaning at least one tracked file: 11 directories.**

    results/hardware-n3/2026-07-16T013912Z
    results/hardware-scaling/2026-07-16T074134Z
    results/hardware-scaling/2026-07-17T014458Z
    results/noise-robustness/2026-07-02T1212Z
    results/noise-robustness/2026-07-03T0213Z
    results/n-scaling-advantage/2026-06-18T0930Z
    results/t9-pilot/precise-2026-07-04T0401Z-p0.05
    results/t9-pilot/precise-2026-07-04T0433Z-p0
    results/t9-pilot/precise-cycle-2026-07-04T0509Z-p0.02
    results/t9-pilot/precise-cycle-2026-07-04T0509Z-p0.02-rev
    results/topology-controls/2026-07-16T172737Z

Plus five tracked files not inside a run directory: results/README.md,
results/hardware-scaling/pending_jobs.txt,
results/hardware-scaling/preregistration.json,
results/hardware-scaling/preregistration-baselines.json,
results/hardware-scaling/repeat-judgments.json.

**Zero tracked files: 22 directories.**

    results/gamma-sweep/N2, N3, N4, N5, N6                            (5)
    results/n-scaling-advantage/2026-07-02T0444Z, 0525Z, 0538Z,
      1247Z, 1757Z, and 2026-07-16T0736Z, 0738Z                       (7)
    results/t9-pilot/2026-07-04T0326Z, 0329Z, 0331Z, 0334Z            (4)
    results/topology/ewl, fully-connected, ghz, ring, star, w         (6)

Source for both lists: `git ls-files -- results` compared against
`git ls-files --others --ignored --exclude-standard -- results`, reduced to two
path components.

**Partially tracked: 2 directories.** Both hold one tracked file and three
untracked ones.

    results/t9-pilot/precise-cycle-2026-07-04T0509Z-p0.02       tracked=1 untracked=3
    results/t9-pilot/precise-cycle-2026-07-04T0509Z-p0.02-rev   tracked=1 untracked=3

In each, `results.json` is tracked while `run.log`, `run.err`, and
`launch-info.txt` beside it are not. The other two `precise-*` directories
contain only `results.json` and are therefore complete rather than partial.

Of the 8 `n-scaling-advantage` runs, exactly one is committed. This bears on
item 13; see F3.

### E4. "QNE" occurrences

| scope | occurrences | command |
| --- | --- | --- |
| generated `results/**/report.md` | **614** | `grep -ro "QNE" results --include=report.md \| wc -l` |
| docs/ | 17 | `grep -ro "QNE" docs -I \| wc -l` |
| src/ | **0** | `grep -ro "QNE" src --include=*.py \| wc -l` |
| repo-wide, text files only | 631 | `grep -ro "QNE" --exclude-dir=.venv-win --exclude-dir=.git -I . \| wc -l` |

614 + 17 = 631, so the term survives only in generated reports and in docs; the
source tree is clean. This confirms the claim in commit 2996528's message that
614 generated occurrences would retire on regeneration, and locates them.

### E5. "marrakesh" occurrences

Two lines in source:

| source |
| --- |
| experiments/hand_built_j.py:8 (`Prototype for cutting the ibm_marrakesh CZ count (35 QSD -> 6) without changing`) |
| experiments/hardware_n3_ghz.py:62 (`decomposition (6 two-qubit gates on ibm_marrakesh vs 35 for generic QSD);`) |

Six further hits fall inside a single contiguous TODOS.md entry, the item-11
residue log, spanning TODOS.md:5 to TODOS.md:23. Citing first and last:
TODOS.md:5 (`## Item-11 residue: ibm_marrakesh attribution on the N=3 gate counts`)
and TODOS.md:23 (`` `fake_provider` files under `.venv-win/`.``). The hits
within it are at :5, :8, :10, :12, :17, :21; they are one entry, not six
independent references.

`docs/` has zero hits. All remaining hits are vendored qiskit `fake_provider`
files under `.venv-win/`.

Source: `grep -rn "marrakesh" --exclude-dir=.venv-win --exclude-dir=.git -I .`

These raw locations are recorded here; the defect they represent is G6.

---

## F. Artifact conventions, the V/C question, and directory inventory

### F1. V/C inventory across every run directory

Source: scratchpad script reading `params.V` and `params.C` from every
`results/*/*/metadata.json`, falling back to `config.snapshot.yaml` where
metadata lacks them, and listing directories with neither. Run under the bare
PATH interpreter (stdlib `json` and `glob` only).

**Group 1: old convention, V=1000.0 C=550.0. Count 5.**

    results/gamma-sweep/N2
    results/gamma-sweep/N3
    results/gamma-sweep/N4
    results/gamma-sweep/N5
    results/gamma-sweep/N6

**This is 5, not 12.** Recorded as measured. No reconciliation to any prior
figure was attempted.

**Group 2: live convention, V=4.0 C=3.0, matching D1. Count 3.**

    results/n-scaling-advantage/2026-06-18T0930Z
    results/noise-robustness/2026-07-02T1212Z
    results/noise-robustness/2026-07-03T0213Z

**Group 2b: any other V/C pair. Count 0.**

**Group 3: no V or C record. Count 25**, in two kinds.

Seven have a `metadata.json` with a `params` block carrying no V or C key:

    results/n-scaling-advantage/2026-07-02T0444Z
    results/n-scaling-advantage/2026-07-02T0525Z
    results/n-scaling-advantage/2026-07-02T0538Z
    results/n-scaling-advantage/2026-07-02T1247Z
    results/n-scaling-advantage/2026-07-02T1757Z
    results/n-scaling-advantage/2026-07-16T0736Z
    results/n-scaling-advantage/2026-07-16T0738Z

Eighteen have no `metadata.json` at all: the three hardware run directories,
eight t9-pilot directories, results/topology-controls/2026-07-16T172737Z, and
the six results/topology/ subdirectories.

**Total: 5 + 3 + 0 + 25 = 33 run directories.**

### F2. What simulation artifacts record that hardware artifacts do not

A committed simulation run records five provenance fields:

| field | source |
| --- | --- |
| experiment | results/n-scaling-advantage/2026-06-18T0930Z/metadata.json:2 (`"experiment": "n-scaling-advantage",`) |
| created_utc | :3 (`"created_utc": "2026-06-18T09:30:50.316418+00:00",`) |
| git commit | :5 (`"commit": "f0ccdcb7623ff4f51a67f9c4637d944b05745e16",`) |
| git dirty | :6 (`"dirty": true`) |
| **python** | :8 (`"python": "3.14.5 (main, May 10 2026, 18:26:20) [GCC 16.1.1 20260430]",`) |

plus a `params` block from :9 onward. B4's forward reference is confirmed, with
three qualifications.

**One.** The python versions differ between simulation runs and neither matches
the canonical env. See G20.

**Two.** No simulation artifact records a qiskit version. The provenance gap is
narrower for simulation than for hardware, not closed.

**Three.** Not all simulation artifacts carry provenance.
results/topology-controls/2026-07-16T172737Z/results.json records
:2 (`"experiment": "topology-noise-controls",`),
:3 (`"created_utc": "2026-07-16T17:27:37.023705+00:00",`), and
:5 (`"seed": 20260716,`), but no git block and no python version.

The strongest provenance in the repo remains
results/hardware-scaling/preregistration.json:11-17, cited in B4, which records
five package versions. That file is written by the local registration script,
not by a run.

### F3. Consequence for item 13, as measurement

**Directories whose V/C convention cannot be determined from their own
artifact: 25** (Group 3 above).

Of those, the seven `n-scaling-advantage` directories are the ones item 13
touches, since item 13 concerns the advantage map. **Seven of the eight
`n-scaling-advantage` runs record no V or C key.** The single exception is
results/n-scaling-advantage/2026-06-18T0930Z, which records V=4.0 C=3.0 and is
also the only one of the eight that is committed (E3).

**Measured consequence.** If the stale advantage map was produced at V=1000
C=550, it did not come from the one committed `n-scaling-advantage` run, whose
metadata records the live convention. It would have to have come from one of the
seven uncommitted runs, none of which records its convention. Those seven cannot
be classified as retire-or-regenerate from their artifacts alone; classifying
them requires re-running or an external record.

**G20 further constrains what "regenerate" can mean here.** The committed
comparison run was produced under python 3.14.5 on Linux, an interpreter not
present on this machine, so regenerating under the canonical env will not
reproduce it byte-for-byte.

No disposition is recommended here. Item 13 decides.

---

## G. Open defects, recorded not resolved

Ids are stable. Where evidence lives in another section it is cross-referenced
rather than duplicated.

**G1. Resolved after this snapshot: `results/` was blanket-ignored while
50 files under it were tracked.** At b3469f0, `.gitignore` line 52 read
`results/`; `git ls-files -- results | wc -l` returned 50, against 126
ignored-but-present (E2). Item 17 removed the ignore rule in cd5c094. Current
.gitignore:52 (`# (results/ is intentionally NOT ignored.)`) and
results/README.md:3 (`Generated experiment outputs, committed to git as part of the research record.`)
now agree. The former `git add -f` consequence is no longer the current rule.

**G2. results/README.md documents two experiments that do not exist.**
results/README.md:23 (`### \`month2_n3_advantage/\``) and
results/README.md:29 (`### \`month3_topology_sweep/\``). Neither directory is
present; the 33 run directories that do exist (F1) are documented nowhere in
that file. *Consequence:* the only file describing the results layout describes
a layout the repo does not have.

**G3. Three interpreter conventions are documented simultaneously.**
Measured (A5): convention 1 `conda run -n entangled-equilibria` 17 lines / 9
files; convention 2 `.venv/bin/python` 3 lines / 2 files; convention 3 bare
`PYTHONPATH=src python` 25 lines / 13 files. A handoff figure of "1 source, 9
conda, 8 bare" fails re-derivation and appears to have counted files for one
convention and lines for another. *Consequence:* a reader following the repo's
own documentation gets one of three different environments; see G10 for what
convention 3 resolves to.

**G4. The pinned Python floor is violated by two of the three reachable
interpreters.** pyproject.toml:4 (`requires-python = ">=3.10"`) against
.venv-win/pyvenv.cfg:3 (`version = 3.9.13`) and the bare PATH interpreter, also
3.9.13 (A1). *Consequence:* `src/` cannot import under either, failing at
src/game/nash.py:24 (`from typing import Any, Callable, TypeAlias`); see A7.
(G11 was assigned to this defect during derivation and is folded here; the id
G11 is retired and should not be cited.)

**G5. The pinned qiskit version is violated by `.venv-win`.**
pyproject.toml:6 (`"qiskit==1.3.2",`) against `.venv-win` qiskit 2.2.3 (A1).
README.md:185 (`# Unpinned installs pull qiskit 2.x, which is incompatible with this code`)
states 2.x is incompatible. *Consequence:* an environment the repo declares
incompatible is present and undocumented; its purpose is NOT IN REPO (A6).

**G6. Two docstrings attribute N=3 gate counts to `ibm_marrakesh` while every
artifact records `ibm_fez`.** Raw locations in E5. Every hardware artifact
records ibm_fez (B2, B3). *Consequence:* unresolved. The files do not settle
whether the counts were genuinely measured against marrakesh during early
prototyping, in which case the attribution is correct and predates the move to
fez, or whether the name is stale. Settling it requires the early transpile
record. Logged at TODOS.md:5 to :23; owned by no item in the current sequence.

**G7. A cross-reference in the run-2 findings doc is stale.**
docs/findings/2026-07-17-run2-repeat-judgment.md:89
(`submissions. The first submission of this batch, job d9chh0qneu4c739lvgb0,`)
and the sentence following it cite "TODOS.md L38-42" for the failed-submission
history. That content now sits around TODOS.md:52
(`d9chh0qneu4c739lvgb0 failed backend-side (error 9603, RF hardware, during`),
shifted by commit b608375 which inserted 20 lines above it. *Consequence:* the
citation was correct when written and points at unrelated content now. One
instance of G13.

**G8. RESOLVED — not a defect; the original reading was wrong.**
`n_repeats_judged` counts *repeats*, i.e. array entries other than the
registration source run, not the array length. At two entries it read 1; after
run 3 it reads 2 with three entries (repeat-judgments.json:8
(`"n_repeats_judged": 2,`)), and exactly one entry carries
`"is_registration_source": true`. The field has now been consistent at two
different array sizes, which is what distinguishes a convention from an
off-by-one. *Consequence:* none. Consumers wanting the array length should read
`len(judgments)`.

**G9. The NE claim is not pinned by any test at N=4 or N=5.**
Three tests assert `q_is_nash is True`, all at N=3 (D4). No test asserts it
False at any N. The closest, tests/test_asymmetric_advantage.py:89
(`r = compute_advantage(N=4, V=_V, C=_C, entangler=ghz_entangler)`), asserts
only symmetry. *Consequence:* a regression in the N=4 or N=5 equilibrium
behaviour would not fail the suite, and that behaviour is what G19 rests on.

**G10. The bare-python convention delegates interpreter selection to PATH,
which the repo never specifies.** 25 lines across 13 files (A5) prescribe
`PYTHONPATH=src python` with no interpreter named anywhere. *Consequence:* the
resulting environment is a property of the reader's machine, not the repo.
Measured locally on 2026-07-18 it resolves to python 3.9.13 with qiskit 0.45.3,
under which README.md's primary quickstart does not run (A7). This is evidence
of what the delegation produces, not a claim about all machines.

**G11. Retired.** Folded into G4 during derivation. Do not cite.

**G12. `graphify-out/` is blanket-ignored yet 62 files under it are tracked.**
.gitignore:55 (`graphify-out/`); `git ls-files -- graphify-out | wc -l` returns
62 (E2). *Consequence:* same class as G1, but the remedies likely differ.
`results/` becomes visible under the option (i) ruling; `graphify-out/` is
tool-generated and probably should not be tracked at all. Disposition belongs to
item 17 or item 19, not decided here.

**G13. Line-number citations in this repo decay faster than they are read.**
Four of four file:line citations carried from a prior draft into this session
failed re-derivation: TODOS.md:55, TODOS.md:60, and TODOS.md:23, all broken by
commit b608375, and .gitignore:47, broken by commit b3469f0. Both commits were
made hours before the citations were checked. Every failure still pointed at
real, plausible-looking content in the correct file, giving no signal it was the
wrong content. *Consequence:* this is a property of the repository's
documentation practice, not of one document. G7 is one instance. The anchored
citation format used in this file is the mitigation applied here and has not
been applied to the rest of the repo.

**G14. `distinct_calibration_vs_previous_runs` is vacuously true for the first
judged run.** Computed as `cal_stamp not in seen_cals`
(scripts/judge_repeat_run.py:162 (`distinct = cal_stamp is not None and cal_stamp not in seen_cals`)),
with `seen_cals` initialised empty at :228 (`seen_cals: list = []`) and appended
only after each run is judged at :232
(`seen_cals.append(cal["calibration_last_update"])`). Run 1 reports true
(repeat-judgments.json:16) while carrying a stamp identical to run 2's (:15 and
:284). *Consequence:* run 2's `false` is the only informative value of the two;
the field name invites reading run 1's `true` as evidence of a distinct
calibration.

**G15. Calibration metadata is captured at result-write time, not submission
time.** `analyze_and_save` calls it at experiments/hardware_scaling.py:653
(`cal = chain_calibration(backend, plan["chain"])`), which fetches live
properties at :585 (`props = backend.properties()`) and records
`str(props.last_update_date)` at :588. Both the live path and the recovery path
reach it through `analyze_and_save`, the latter at :697. Run 1 carries
`"recovered": true` (results/hardware-scaling/2026-07-16T074134Z/result.json:11).
*Consequence:* the recorded stamp describes backend state at analysis time and
may not identify the calibration the job ran under. The cross-day repeat design
counts calibration days from this field.

**G16. No hardware run is reproducible from its own artifact.** All three record
`"dirty": true` (results/hardware-n3/2026-07-16T013912Z/result.json:6,
results/hardware-scaling/2026-07-16T074134Z/result.json:6,
results/hardware-scaling/2026-07-17T014458Z/result.json:6), so the recorded
commit does not identify the code; and no hardware artifact records any python,
qiskit, or runtime version, a probe returning zero hits (B4). *Consequence:*
neither code nor environment behind any hardware result is recoverable. The
in-repo template to copy is
results/hardware-scaling/preregistration.json:11-17 (B4).

**G17. The N=5 deficit sign-reproduction criterion sits outside the
registration.** Scope fact, not a defect. `registered_tests`
(results/hardware-scaling/preregistration.json:42 (`"registered_tests": {`))
names exactly two, at :43 and :44. Neither is a deficit-sign test, though the
reference values it uses are registered at :219 and :220 (C3). *Consequence:*
"the N=5 deficit reproduced" is a real measured result with registered
references, but calling it a preregistered test would overstate what the
registration covers.

**G18. Per-player advantage reporting sits outside the registration.** Scope
fact, not a defect. `grep -c "per_player"` returns 0 for both registration files
(C5). *Consequence:* per-player results are reportable as observations, not as
preregistered outcomes.

**G19. The Q profile is not an equilibrium at the N where both hardware runs
sit.** Open framing question for item 14. Requires the collaborator who owns the
game-theory layer. (Q,...,Q) is a pure NE only at N=3; the Hawk deviation pays
2.0000000000000009 against a Q payoff of 1 at N=4, and 2.6180339887498949
against 0.80000000000000004 at N=5 (D2, D5). The equilibrium boundary is
characterised rather than merely observed: measured `q_is_nash` agrees with
`2 + 2*cos(2*pi/N) <= V/N` at every N from 2 to 8 (D5), placing the transition
between N=3 and N=4 at V=4. The artifacts already carry an honesty note
(results/hardware-scaling/2026-07-17T014458Z/result.json, `note` field:
`(Q,..,Q) is a pure NE only at N=3 (Month-3 finding).`). *Consequence:* the
conditional primary test (C2), the n5_deficit analysis (C3), the per-player
results (C5), and item 9's plan all rest on a non-equilibrium profile. Item 14
must state explicitly whether the Q profile is presented as an equilibrium
prediction or as a fixed cooperative protocol under study.

**G20. Committed simulation artifacts were produced by interpreters no longer
present on this machine, including a different operating system.**
results/n-scaling-advantage/2026-06-18T0930Z/metadata.json:8
(`"python": "3.14.5 (main, May 10 2026, 18:26:20) [GCC 16.1.1 20260430]",`) is
python 3.14.5 on Linux/GCC.
results/noise-robustness/2026-07-02T1212Z/metadata.json:8
(`"python": "3.12.7 | packaged by Anaconda, Inc. | (main, Oct  4 2024, 13:17:27) [MSC v.1929 64 bit (AMD64)]",`)
is python 3.12.7 Anaconda on Windows. Neither matches the canonical conda env's
3.10.20 (A1), and neither of those two interpreters is among the three reachable
stacks recorded there. *Consequence:* regenerating any of these artifacts under
the canonical env will not reproduce them byte-for-byte, which bears directly on
item 13's retire-versus-regenerate decision (F3). No simulation artifact records
a qiskit version, so the gap is narrowed rather than closed.

### Ownership across the current sequence

- **Item 17 resolves:** G1, G2, G3, G4, G5, G10, G12 (G12's disposition possibly
  deferred to item 19).
- **Item 16 resolves:** G15, G16.
- **Item 18 resolves:** G9, via the N=4/N=5 NE regression guard.
- **Sequence step 2 resolves:** G7.
- **Unowned by any item:** G6, G8, G13, G14.
- **Scope facts item 14 must respect rather than fix:** G17, G18, G19. G20
  constrains item 13.
