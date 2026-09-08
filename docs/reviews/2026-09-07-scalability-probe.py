"""Exploratory review calculations; no production or manuscript changes.

Run with the entangled-equilibria Python interpreter. Writes sibling JSON.
Checks phase-branch predictions against the repository's dense EWL oracle.
"""
from pathlib import Path
import json
import math
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from circuits.ewl import U
from circuits.n_player import build_ewl_circuit
from game.payoffs import expected_payoff


def ghz_probs(gates, gamma):
    """Apply GHZ J and its inverse through four product-state terms."""
    a = np.array([1.0 + 0j])
    b = a.copy()
    for gate in reversed(gates):
        a = np.kron(a, gate[:, 0])
        b = np.kron(b, gate[:, 1])
    c, s = math.cos(gamma / 2), math.sin(gamma / 2)
    out = c*c*a + 1j*s*c*b - 1j*s*c*a[::-1] + s*s*b[::-1]
    return np.abs(out)**2


def main():
    rng = np.random.default_rng(90407)
    oracle_error = 0.0
    formula_error = 0.0
    oracle_cases = 0
    branch_cases = 0
    # Independent arbitrary-profile comparison, including non-maximal gamma.
    for n in range(2, 8):
        for gamma in (0.0, 0.31*math.pi, math.pi/2):
            params = [(float(rng.uniform(0, math.pi)),
                       float(rng.uniform(-math.pi, math.pi)),
                       float(rng.uniform(-math.pi, math.pi))) for _ in range(n)]
            actual = build_ewl_circuit(n, params, gamma=gamma)
            predicted = ghz_probs([U(*p) for p in params], gamma)
            oracle_error = max(oracle_error, float(np.max(np.abs(actual-predicted))))
            oracle_cases += 1
    for n in range(2, 8):
        for m in range(n):
            alpha = m*math.pi/n
            for gamma in (0.0, 0.31*math.pi, math.pi/2):
                base = [(0., alpha, alpha)]*n
                t = math.sin(gamma)**2 * math.sin(alpha)**2
                checks = [(base, 4/n)]
                for dev, target in [((0., 0., 0.), 4/n - 3*t/n),
                                    ((math.pi, 0., 0.), 4*(1-t)),
                                    ((math.pi, 0., -alpha), 4.)]:
                    profile = base.copy()
                    profile[0] = dev
                    checks.append((profile, target))
                for profile, target in checks:
                    probs = build_ewl_circuit(n, profile, gamma=gamma)
                    payoff = float(expected_payoff(probs, n)[0])
                    formula_error = max(formula_error, abs(payoff-target))
                    oracle_cases += 1
                branch_cases += 1
    rows = []
    for n in range(2, 13):
        alpha = (n//2)*math.pi/n
        h_old = 4*math.cos(math.pi/n)**2
        h_new = 4*math.cos(alpha)**2
        d_new = 4/n - 3*math.sin(alpha)**2/n
        rows.append(dict(N=n, m=n//2, alpha_over_pi=(n//2)/n,
                         cooperative=4/n, old_hawk=h_old, new_hawk=h_new,
                         new_dove=d_new,
                         new_restricted_margin=min(4/n-h_new, 4/n-d_new),
                         full_su2_gain=4-4/n,
                         uniform_retention=1-2.**(-n)))
    # Global single-player SU(2) response is a real 4x4 quadratic form.
    eye = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], complex)
    y = np.array([[0, -1j], [1j, 0]], complex)
    z = np.diag([1, -1]).astype(complex)
    basis = [eye, 1j*x, 1j*y, 1j*z]
    qform_error = 0.0
    eigen_gain = []
    for n in range(2, 8):
        alpha = (n//2)*math.pi/n
        gates = [U(0, alpha, alpha)]*n
        def f(q):
            candidate = gates.copy()
            candidate[0] = sum(q[k]*basis[k] for k in range(4))
            return float(expected_payoff(ghz_probs(candidate, math.pi/2), n)[0])
        M = np.zeros((4, 4))
        for a in range(4):
            M[a, a] = f(np.eye(4)[a])
        for a in range(4):
            for b in range(a+1, 4):
                M[a, b] = M[b, a] = f((np.eye(4)[a]+np.eye(4)[b])/math.sqrt(2)) - (M[a,a]+M[b,b])/2
        for _ in range(25):
            q = rng.normal(size=4)
            q /= np.linalg.norm(q)
            qform_error = max(qform_error, abs(f(q)-float(q@M@q)))
        vals, vecs = np.linalg.eigh(M)
        assert abs(f(vecs[:, -1])-vals[-1]) < 1e-10
        eigen_gain.append(dict(N=n, best_response=float(vals[-1]), gain=float(vals[-1]-4/n)))
    assert oracle_error < 1e-10
    assert formula_error < 1e-10
    assert qform_error < 1e-10
    assert all(r['new_restricted_margin'] > 0 for r in rows)
    result = dict(status="exploratory analytic checks, not preregistered hardware evidence",
                  oracle_cases=oracle_cases, branch_gamma_cases=branch_cases,
                  arbitrary_profile_max_probability_error=oracle_error,
                  branch_formula_max_payoff_error=formula_error,
                  quadratic_form_max_error=qform_error,
                  maximal_entanglement_rows=rows, eigenvalue_checks=eigen_gain)
    output = Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v, list)}, indent=2))
    print(output)


if __name__ == '__main__':
    main()
