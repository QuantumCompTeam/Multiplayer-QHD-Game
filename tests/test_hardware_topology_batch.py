"""Offline tests for the topology batch plan and its analysis.

experiments/hardware_topology.py is a script, not a package module, so it is
loaded by path here (same approach the repo uses for other experiment entry
points). Nothing in this file touches the network or spends quota: the batch
plan's bookkeeping and the analysis arithmetic are proven correct before the
plan is ever used to build a real job.
"""

import importlib.util
import math
from pathlib import Path

import numpy as np
import pytest

_PATH = Path(__file__).resolve().parents[1] / "experiments" / "hardware_topology.py"
_spec = importlib.util.spec_from_file_location("hardware_topology", _PATH)
ht = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ht)

GAMMA = math.pi / 2


# ── series_meta: the uniform five-axis record ────────────────────────────────


def _meta(**over):
    base = dict(topology="ghz", N=3, fold=1, gamma=GAMMA, profile=["Q", "Q", "Q"],
                wiring=[0, 1, 2], fil=[59, 75, 74], cz=6)
    base.update(over)
    return ht.series_meta(**base)


def test_series_meta_carries_every_axis():
    meta = _meta()
    assert meta["kind"] == "series"
    for key in ("topology", "N", "fold", "gamma", "profile", "wiring", "fil", "cz"):
        assert key in meta, f"{key} missing from series meta"


def test_series_meta_rejects_wiring_of_wrong_length():
    with pytest.raises(ValueError, match="wiring"):
        _meta(wiring=[0, 1])


def test_series_meta_rejects_profile_of_wrong_length():
    with pytest.raises(ValueError, match="profile"):
        _meta(profile=["Q", "Q"])


def test_series_meta_is_json_safe():
    """The record goes straight into result.json; no numpy scalars allowed."""
    import json

    json.dumps(_meta(gamma=np.float64(GAMMA)))


# ── series_key: identity across folds ────────────────────────────────────────


def test_series_key_is_stable_and_excludes_fold():
    assert ht.series_key(_meta(fold=1)) == ht.series_key(_meta(fold=5))


def test_series_key_separates_profiles_wirings_topologies_and_gammas():
    keys = {
        ht.series_key(_meta()),
        ht.series_key(_meta(profile=["H", "Q", "Q"])),
        ht.series_key(_meta(profile=["Q", "H", "Q"])),
        ht.series_key(_meta(wiring=[1, 2, 0])),
        ht.series_key(_meta(topology="ring")),
        ht.series_key(_meta(gamma=math.pi / 4)),
    }
    assert len(keys) == 6, "series_key collapsed two distinct experiments"


# ── payoff_stats: must match the registered scaling estimator ────────────────


def test_payoff_stats_on_the_ideal_ground_state():
    """All-|0..0> is the ideal cooperative outcome: every player gets V/N."""
    N = 3
    probs = np.zeros(2**N)
    probs[0] = 1.0
    s = ht.payoff_stats(probs, N, shots=4096)
    assert s["mean"] == pytest.approx(4.0 / N)          # V/N at V=4
    assert s["per_player"] == pytest.approx([4.0 / N] * N)
    assert s["p_ground"] == pytest.approx(1.0)
    assert s["sigma"] == pytest.approx(0.0, abs=1e-12)  # deterministic outcome


def test_payoff_stats_single_bitflip_leaves_the_mean_at_v_over_n():
    """The paper's core mechanism: one Hawk still pays V total, so mean = V/N.

    This is the first-order insensitivity claim in Sec. IV-D. If this ever
    fails, the mechanism sentence in the paper is wrong, not the test.
    """
    N = 3
    for flipped in range(N):
        probs = np.zeros(2**N)
        probs[1 << flipped] = 1.0
        s = ht.payoff_stats(probs, N, shots=4096)
        assert s["mean"] == pytest.approx(4.0 / N), f"flip on player {flipped}"


def test_payoff_stats_all_hawk_is_the_only_mean_lowering_outcome():
    N = 3
    probs = np.zeros(2**N)
    probs[2**N - 1] = 1.0
    s = ht.payoff_stats(probs, N, shots=4096)
    assert s["mean"] == pytest.approx((4.0 - 3.0) / N)  # (V-C)/N at V=4, C=3


def test_payoff_stats_matches_the_scaling_scripts_estimator():
    """Byte-for-byte agreement with experiments/hardware_scaling.payoff_stats.

    The topology run and the scaling run must be comparable; a divergence in
    the estimator would silently make them not.
    """
    import importlib.util as ilu

    p = Path(__file__).resolve().parents[1] / "experiments" / "hardware_scaling.py"
    spec = ilu.spec_from_file_location("hardware_scaling", p)
    hs = ilu.module_from_spec(spec)
    spec.loader.exec_module(hs)

    rng = np.random.default_rng(20260725)
    for N in (3, 4):
        probs = rng.dirichlet(np.ones(2**N))
        a = ht.payoff_stats(probs, N, shots=4096)
        b = hs.payoff_stats(probs, N, shots=4096)
        assert a["mean"] == pytest.approx(b["mean"], abs=1e-15)
        assert a["sigma"] == pytest.approx(b["sigma"], abs=1e-15)
        assert a["per_player"] == pytest.approx(b["per_player"], abs=1e-15)


# ── analyze_batch: grouping, ZNE, per-player retention ───────────────────────


def _fake_plan_and_counts(shots=4096):
    """Two cal pubs + one GHZ N=3 series at folds 1/3/5, all ideal counts.

    Ideal counts make the expected analysis exactly computable by hand:
    perfect readout calibration (identity confusion matrices), every series pub
    entirely in |000>, so mitigated payoff = V/N and advantage = V/N - 1/N.
    """
    fil5 = [59, 75, 74, 73, 79]
    plan = {"pinned": fil5, "pubs": [], "meta": []}
    plan["meta"].append({"kind": "cal0", "fil": fil5})
    plan["meta"].append({"kind": "cal1", "fil": fil5})
    counts = [{"00000": shots}, {"11111": shots}]
    for f in (1, 3, 5):
        plan["meta"].append(ht.series_meta(
            topology="ghz", N=3, fold=f, gamma=GAMMA, profile=["Q", "Q", "Q"],
            wiring=[0, 1, 2], fil=fil5[:3], cz=6 * f))
        counts.append({"000": shots})
    return plan, counts


def test_analyze_batch_groups_folds_into_one_series():
    plan, counts = _fake_plan_and_counts()
    out = ht.analyze_batch(counts, plan, shots=4096)
    assert len(out["series"]) == 1
    entry = next(iter(out["series"].values()))
    assert sorted(entry["folds"]) == ["1", "3", "5"]


def test_analyze_batch_recovers_the_ideal_advantage():
    plan, counts = _fake_plan_and_counts()
    out = ht.analyze_batch(counts, plan, shots=4096)
    entry = next(iter(out["series"].values()))
    # ideal: cooperative payoff V/N = 4/3, classical baseline 1/N = 1/3
    assert entry["classical_ne_payoff"] == pytest.approx(1.0 / 3)
    assert entry["folds"]["1"]["mitigated"]["advantage"] == pytest.approx(1.0)
    assert entry["zne"]["advantage"] == pytest.approx(1.0, abs=1e-9)


def test_analyze_batch_keeps_per_player_vectors():
    """Items 6 and 7 read the per-player floor, not the mean -- it must survive."""
    plan, counts = _fake_plan_and_counts()
    out = ht.analyze_batch(counts, plan, shots=4096)
    entry = next(iter(out["series"].values()))
    assert entry["folds"]["1"]["mitigated"]["per_player"] == pytest.approx(
        [4.0 / 3] * 3)


def test_analyze_batch_separates_two_profiles_of_the_same_cell():
    """A deviation series must not be merged into the cooperative one."""
    plan, counts = _fake_plan_and_counts()
    plan["meta"].append(ht.series_meta(
        topology="ghz", N=3, fold=1, gamma=GAMMA, profile=["H", "Q", "Q"],
        wiring=[0, 1, 2], fil=[59, 75, 74], cz=6))
    counts.append({"001": 4096})
    out = ht.analyze_batch(counts, plan, shots=4096)
    assert len(out["series"]) == 2
    profiles = {"".join(s["profile"]) for s in out["series"].values()}
    assert profiles == {"QQQ", "HQQ"}


def test_analyze_batch_omits_zne_for_a_single_fold_series():
    """Deviation and gamma pubs run at fold 1 only; ZNE needs >=2 points."""
    plan, counts = _fake_plan_and_counts()
    plan["meta"].append(ht.series_meta(
        topology="ghz", N=3, fold=1, gamma=GAMMA, profile=["H", "Q", "Q"],
        wiring=[0, 1, 2], fil=[59, 75, 74], cz=6))
    counts.append({"001": 4096})
    out = ht.analyze_batch(counts, plan, shots=4096)
    dev = next(s for s in out["series"].values() if s["profile"] == ["H", "Q", "Q"])
    assert "zne" not in dev


# ── pinned-set guard ─────────────────────────────────────────────────────────
#
# Run 1 (job d9ia1pd0k0jc738jaqgg) was registered against pinned
# [20,21,22,23,24] but EXECUTED on [137,147,146,145,144]: ibm_fez recalibrated
# between the two, and find_pinned_set selects from live calibration. That made
# the registered per-cell prediction untestable. These tests pin the guard that
# stops it recurring.

_EDGES = [(20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (40, 41)]


def test_validate_pinned_chain_accepts_a_connected_path():
    ht.validate_pinned_chain(_EDGES, [20, 21, 22, 23, 24])  # must not raise


def test_validate_pinned_chain_accepts_the_reverse_direction():
    ht.validate_pinned_chain(_EDGES, [24, 23, 22, 21, 20])


def test_validate_pinned_chain_rejects_wrong_length():
    with pytest.raises(ValueError, match="PIN_LEN|length"):
        ht.validate_pinned_chain(_EDGES, [20, 21, 22])


def test_validate_pinned_chain_rejects_duplicates():
    with pytest.raises(ValueError, match="distinct"):
        ht.validate_pinned_chain(_EDGES, [20, 21, 22, 23, 23])


def test_validate_pinned_chain_rejects_a_broken_link():
    with pytest.raises(ValueError, match="not an edge"):
        ht.validate_pinned_chain(_EDGES, [20, 21, 22, 23, 41])


def test_validate_pinned_chain_rejects_out_of_order_path():
    """Adjacency must hold in the GIVEN order: the order is the chain."""
    with pytest.raises(ValueError, match="not an edge"):
        ht.validate_pinned_chain(_EDGES, [20, 22, 21, 23, 24])


def test_registered_pinned_set_matches_the_frozen_registration():
    """The committed registration is the source of truth for run comparability."""
    assert ht.registered_pinned_set() == [20, 21, 22, 23, 24]


def test_parse_pinned_arg_reads_a_comma_list():
    assert ht.parse_pinned_arg("137,147,146,145,144") == [137, 147, 146, 145, 144]


def test_parse_pinned_arg_rejects_wrong_length():
    with pytest.raises(ValueError, match="PIN_LEN|length"):
        ht.parse_pinned_arg("1,2,3")
