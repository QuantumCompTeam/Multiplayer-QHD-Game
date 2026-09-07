import math

import numpy as np
import pytest

from circuits.ewl import U, q_strategy
from circuits.n_player import build_ewl_circuit
from circuits.topologies import ghz_entangler, star_entangler, w_entangler
from game.best_response import best_response, quaternion_params
from game.compact_ghz import compact_payoffs
from game.payoffs import expected_payoff
from game.phase_branches import branch_predictions, counter_strategy, phase_strategy
from game.observable_payoffs import counts_summary, outcome_vector
from game.payoffs import outcome_payoff
from hardware.phase_validation import experiment_rows, judge


@pytest.mark.parametrize('n', range(2, 8))
@pytest.mark.parametrize('gamma', [0., .31*math.pi, math.pi/2])
def test_branches_against_dense(n, gamma):
    for m in {1, n//2}:
        base = [phase_strategy(n, m)]*n
        prediction = branch_predictions(n, m, gamma)
        for dev, target in [(base[0], prediction['cooperative']),
                            ((0.,0.,0.), prediction['dove']),
                            ((math.pi,0.,0.), prediction['hawk']),
                            (counter_strategy(n,m), 4.)]:
            profile = base.copy()
            profile[0] = dev
            payoff = expected_payoff(build_ewl_circuit(n, profile, gamma=gamma), n)
            assert payoff[0] == pytest.approx(target, abs=1e-10)
    assert phase_strategy(n,1) == q_strategy(n)


@pytest.mark.parametrize('n', [2,3,4,5,6,7,16,32,64,128])
def test_compact_arbitrary_profiles(n):
    rng = np.random.default_rng(87+n)
    profile = [tuple(rng.uniform(-math.pi,math.pi,3)) for _ in range(n)]
    got = compact_payoffs(profile, .37*math.pi)
    assert np.isfinite(got['payoff_vector']).all()
    if n <= 7:
        reference = expected_payoff(build_ewl_circuit(n, profile, gamma=.37*math.pi), n)
        np.testing.assert_allclose(got['payoff_vector'], reference, atol=1e-10)
    coop = compact_payoffs([phase_strategy(n,n//2)]*n)
    np.testing.assert_allclose(coop['payoff_vector'], 4/n, atol=1e-10)
    assert branch_predictions(n,n//2)['restricted_margin'] > 0


@pytest.mark.parametrize('entangler', [ghz_entangler, star_entangler, w_entangler])
def test_global_response_reconstructs_and_dominates_random_deviations(entangler):
    n = 3
    base = [(.71,.23,-.81), (.4,-.3,.2), (1.2,.9,.1)]
    def oracle(params):
        profile = base.copy()
        profile[1] = params
        return float(expected_payoff(build_ewl_circuit(n,profile,entangler=entangler),n)[1])
    response = best_response(oracle, oracle(base[1]))
    rng = np.random.default_rng(19)
    for _ in range(20):
        assert oracle(quaternion_params(rng.normal(size=4))) <= response.payoff+1e-10
    assert response.reconstruction_residual < 1e-10


def test_quaternion_sign_and_nonquadratic_rejection():
    q = np.array([1,2,3,4])/np.sqrt(30)
    target = np.array([[q[0]+1j*q[3], q[2]+1j*q[1]],
                       [-q[2]+1j*q[1],q[0]-1j*q[3]]])
    np.testing.assert_allclose(U(*quaternion_params(q)), target, atol=1e-12)
    with pytest.raises(ValueError, match='quadratic'):
        best_response(lambda p: float(abs(U(*p)[0,0])**4), 0.)


@pytest.mark.parametrize('n', range(2,8))
def test_streamed_original_and_uniform_sensitivity(n):
    counts = {format(i,f'0{n}b'): 2 for i in range(2**n)}
    for bits in counts:
        np.testing.assert_allclose(outcome_vector(bits),outcome_payoff(int(bits,2),n,4,3))
    for ell in [0.,.25,1.]:
        result = counts_summary(counts,ell)
        assert result['retention'] == pytest.approx(1-(1-ell)*2**(-n)-ell/4)
        assert result['spread'] == pytest.approx(0,abs=1e-12)


def test_hardware_design_covers_both_deviations_and_preserves_pilot_scope():
    rows = experiment_rows()
    assert len(rows)+2 == 70
    assert len(experiment_rows(common_menu=True))+2 == 92
    pilot = experiment_rows((3,),pilot=True)
    counts = [{'000':4096} for _ in pilot]
    result = judge(pilot,counts,pilot=True)
    assert not result['complete_D_H_coverage']
    assert not result['epsilon_equilibrium_supported']


def test_ideal_hardware_judge_and_profitable_deviation():
    rows = experiment_rows((4,))
    counts = []
    for row in rows:
        profile = [tuple(p) for p in row['strategies']]
        probabilities = build_ewl_circuit(4,profile)
        # N=4 candidate tests are deterministic; all rows can be rounded for this fixture.
        counts.append({format(i,'04b'):int(round(p*100000)) for i,p in enumerate(probabilities) if p>1e-8})
    assert judge(rows,counts)['epsilon_equilibrium_supported']
    bad = next(i for i,r in enumerate(rows) if r['kind']=='H' and r['player']==0)
    counts[bad] = {'0001':100000}
    assert not judge(rows,counts)['epsilon_equilibrium_supported']
