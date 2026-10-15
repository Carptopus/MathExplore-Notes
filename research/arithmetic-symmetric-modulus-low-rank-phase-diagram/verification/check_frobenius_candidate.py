"""Exact algebra checks for the MATH-DIR-0112 Frobenius candidate.

This checks the symbolic reductions used in S2, including the second branch
of the fixed-e min-max.  It does not prove the global matrix upper bound.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    d, e, z, a, b, lam = sp.symbols("d e z a b lam", positive=True, real=True)
    D = sp.diag(d, e)
    H = sp.Matrix([[0, -z], [-z, 0]])
    T = sp.Matrix([[2 * a, b], [-b, 0]])
    block = (D + H).row_join(T).col_join(T.T.row_join(D - H))

    m_plus = sp.Matrix([[d + 2 * a, b + z], [b + z, e]])
    m_minus = sp.Matrix([[d - 2 * a, b - z], [b - z, e]])
    factor_gap = sp.expand(
        block.charpoly(lam).as_expr()
        - m_plus.charpoly(lam).as_expr() * m_minus.charpoly(lam).as_expr()
    )
    assert factor_gap == 0

    d_star = b**2 / e + a**2 * e / b**2
    z_star = a * e / b
    assert sp.factor(m_plus.det().subs({d: d_star, z: z_star})) == 0
    assert sp.factor(m_minus.det().subs({d: d_star, z: z_star})) == 0

    # Destructive regression: the intersection formula is not valid after
    # ae>b^2.  Here the correct second branch has d=2a=1 at z=b, whereas the
    # unrestricted intersection would give 25/24.
    branch_subs = {
        a: sp.Rational(1, 2),
        b: sp.sqrt(3) / 2,
        e: sp.Integer(2),
        d: sp.Integer(1),
        z: sp.sqrt(3) / 2,
    }
    plus_branch = m_plus.subs(branch_subs)
    minus_branch = m_minus.subs(branch_subs)
    assert plus_branch.det() == 1
    assert minus_branch.det() == 0
    assert plus_branch[0, 0] > 0 and plus_branch[1, 1] > 0
    assert minus_branch[0, 0] == 0 and minus_branch[1, 1] > 0
    old_intersection = d_star.subs(branch_subs)
    assert old_intersection == sp.Rational(25, 24) > branch_subs[d]

    r, t = sp.symbols("r t", positive=True, real=True)
    c = 1 - r
    denominator_sq = sp.expand((1 / t + r * t) ** 2 + (c * t) ** 2)
    expected = 1 / t**2 + 2 * r + (r**2 + c**2) * t**2
    assert sp.simplify(denominator_sq - expected) == 0

    s = sp.sqrt(r**2 + (1 - r) ** 2)
    assert sp.expand(s**2 - r**2 - (1 - r) ** 2) == 0
    ratio_sq = (1 + r**2) / (r + s)
    derivative_numerator = sp.factor(
        sp.together(sp.diff(ratio_sq, r)).as_numer_denom()[0]
    )
    assert sp.simplify(
        derivative_numerator
        - (r - 1) * (2 * r**2 + r * s - r + s - 1)
    ) == 0

    elimination = sp.factor(
        (2 * r**3 - 3 * r**2 + 1) ** 2
        - (r**2 - 1) ** 2 * (2 * r**2 - 2 * r + 1)
    )
    assert elimination == 2 * r * (r - 1) ** 2 * (r**3 - 3 * r**2 - r + 1)

    roots = [
        root
        for root in sp.nroots(r**3 - 3 * r**2 - r + 1, n=40)
        if abs(sp.im(root)) < sp.Rational(1, 10) ** 30 and 0 < sp.re(root) < 1
    ]
    assert len(roots) == 1
    rho = sp.re(roots[0])
    candidate = sp.sqrt(ratio_sq.subs(r, rho))
    print(f"rho={sp.N(rho, 16)}")
    print(f"C2_candidate={sp.N(candidate, 16)}")
    print("PASS: exact Frobenius candidate identities")


if __name__ == "__main__":
    main()
