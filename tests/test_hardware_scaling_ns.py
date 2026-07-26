"""Offline guards for the --ns / --chain-len extension (plan item 4, Task 10).

experiments/hardware_scaling.py runs the batch that item 3's cross-day repeats
re-execute and that results/hardware-scaling/preregistration.json is frozen
against. Task 10 threads `ns` and `chain_len` through it. The contract that
must not break:

  * the DEFAULTS reproduce the registered batch exactly, and
  * plan_from_job_circuits rebuilds the pub ORDER from `ns`, so recovering
    runs 1-3 with the default --ns must yield exactly the original labelling.

A silent error here would mislabel the series of an already-billed job, which
is the one failure mode that cannot be fixed by re-running.
"""

import importlib.util
from pathlib import Path

import pytest
from qiskit import ClassicalRegister, QuantumCircuit

_PATH = Path(__file__).resolve().parents[1] / "experiments" / "hardware_scaling.py"
_spec = importlib.util.spec_from_file_location("hardware_scaling", _PATH)
hs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hs)


def _pub(n_meas: int, width: int = 8, n_cz: int = 0) -> QuantumCircuit:
    """A stand-in pub: `n_meas` measures (physical j -> clbit j) and n_cz czs."""
    qc = QuantumCircuit(width)
    for _ in range(n_cz):
        qc.cz(0, 1)
    creg = ClassicalRegister(n_meas, "meas")
    qc.add_register(creg)
    for j in range(n_meas):
        qc.measure(j, creg[j])
    return qc


def _job_circuits(ns, chain_len):
    """The pub sequence build_batch emits, in order."""
    circuits = [_pub(chain_len), _pub(chain_len)]
    for N in ns:
        for _ in hs.FOLDS:
            circuits.append(_pub(N))
    return circuits


# ── the defaults are the registered batch ────────────────────────────────────


def test_module_defaults_are_the_registered_batch():
    """NS/CHAIN_LEN are what the frozen preregistration was built against."""
    assert hs.NS == (3, 4, 5)
    assert hs.CHAIN_LEN == 5
    assert hs.FOLDS == (1, 3, 5)


def test_default_recovery_reproduces_the_11_pub_labelling():
    plan = hs.plan_from_job_circuits(_job_circuits(hs.NS, hs.CHAIN_LEN))
    meta = plan["meta"]
    assert len(meta) == 11, "runs 1-3 are 11-pub jobs"
    assert [m["kind"] for m in meta[:2]] == ["cal0", "cal1"]
    assert [(m["N"], m["fold"]) for m in meta[2:]] == [
        (3, 1), (3, 3), (3, 5),
        (4, 1), (4, 3), (4, 5),
        (5, 1), (5, 3), (5, 5),
    ]


def test_default_ns_is_implicit():
    """Calling without ns must equal calling with the default explicitly."""
    circuits = _job_circuits(hs.NS, hs.CHAIN_LEN)
    implicit = hs.plan_from_job_circuits(circuits)["meta"]
    explicit = hs.plan_from_job_circuits(_job_circuits((3, 4, 5), 5),
                                         ns=(3, 4, 5))["meta"]
    assert implicit == explicit


# ── the extension ────────────────────────────────────────────────────────────


def test_n67_recovery_has_17_pubs_in_order():
    ns = (3, 4, 5, 6, 7)
    plan = hs.plan_from_job_circuits(_job_circuits(ns, 7), ns=ns)
    meta = plan["meta"]
    assert len(meta) == 2 + len(ns) * len(hs.FOLDS) == 17
    assert [(m["N"], m["fold"]) for m in meta[2:]] == [
        (N, f) for N in ns for f in hs.FOLDS
    ]


def test_recovering_with_the_wrong_ns_aborts_rather_than_mislabels():
    """A 17-pub job read back as 3,4,5 must exit, not silently truncate."""
    circuits = _job_circuits((3, 4, 5, 6, 7), 7)
    with pytest.raises(SystemExit):
        hs.plan_from_job_circuits(circuits, ns=(3, 4, 5))


def test_recovering_the_default_job_with_n67_aborts():
    circuits = _job_circuits((3, 4, 5), 5)
    with pytest.raises(SystemExit):
        hs.plan_from_job_circuits(circuits, ns=(3, 4, 5, 6, 7))


def test_chain_is_read_from_the_cal_pub():
    plan = hs.plan_from_job_circuits(_job_circuits(hs.NS, hs.CHAIN_LEN))
    assert plan["chain"] == [0, 1, 2, 3, 4]
    assert len(plan["chain"]) == hs.CHAIN_LEN


def test_cz_counts_are_attributed_per_series_pub():
    circuits = [_pub(5), _pub(5), _pub(3, n_cz=6), _pub(3, n_cz=18),
                _pub(3, n_cz=30), _pub(4, n_cz=9), _pub(4, n_cz=27),
                _pub(4, n_cz=45), _pub(5, n_cz=14), _pub(5, n_cz=42),
                _pub(5, n_cz=70)]
    meta = hs.plan_from_job_circuits(circuits)["meta"]
    assert [m["cz"] for m in meta[2:]] == [6, 18, 30, 9, 27, 45, 14, 42, 70]
