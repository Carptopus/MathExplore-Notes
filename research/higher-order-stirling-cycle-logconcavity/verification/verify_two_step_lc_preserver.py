"""Exact certificate for the two-step log-concavity mechanism.

The script proves the algebraic part of the following statement.  Let

    q_n(k) = A(n,k) q_{n-1}(k) + B(n,k) q_{n-1}(k-1),

where

    A(n,k) = (n-k)(n+4k-1)/(n+4k),
    B(n,k) = 5k/(n+4k).

For k >= 2 and d=n-k >= 3, the two-step map from row n-2 to row n
preserves log-concavity at k.  Boundary strips d=1,2 are checked
directly.  The final section verifies the rational comparison which
turns this auxiliary log-concavity into the original r=5 inequality in
the whole wedge k >= 2d, using the already certified d<=18 strips at the
finite boundary exceptions.

All calculations are over exact SymPy rationals.  No numerical sampling
is used as proof.
"""

from __future__ import annotations

import sympy as sp


n, k, d = sp.symbols("n k d", integer=True)
w, h = sp.symbols("w h", positive=True)
K, D, S, U = sp.symbols("K D S U", nonnegative=True, integer=True)


def ab(nn: sp.Expr, kk: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    denominator = nn + 4 * kk
    return (
        (nn - kk) * (nn + 4 * kk - 1) / denominator,
        5 * kk / denominator,
    )


def two_step(nn: sp.Expr, kk: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    a, b = ab(nn, kk)
    a0, b0 = ab(nn - 1, kk)
    a1, b1 = ab(nn - 1, kk - 1)
    return tuple(
        map(sp.factor, (a * a0, a * b0 + b * a1, b * b1))
    )


def assert_nonnegative_coefficients(expr: sp.Expr, *variables: sp.Symbol) -> None:
    polynomial = sp.Poly(sp.expand(expr), *variables)
    negatives = [(monomial, coefficient) for monomial, coefficient in polynomial.terms()
                 if coefficient < 0]
    assert not negatives, negatives[:5]
    assert polynomial.as_expr() != 0


def verify_two_step_preserver() -> None:
    alpha_minus, beta_minus, gamma_minus = two_step(n, k - 1)
    alpha, beta, gamma = two_step(n, k)
    alpha_plus, beta_plus, gamma_plus = two_step(n, k + 1)

    # For an input LC sequence, write its four local adjacent ratios as
    # u >= v >= w >= t.  The output defect is minimized at u=v and t=w.
    # Put v=w+h, h>=0.  After scaling x_{k-2}=1, the worst defect is F.
    v = w + h
    center = alpha * v * w + beta * v + gamma
    left = alpha_minus * v + beta_minus + gamma_minus / v
    right = v * (alpha_plus * w**2 + beta_plus * w + gamma_plus)
    defect = sp.factor(center**2 - left * right)

    numerator, denominator = sp.together(defect.subs(n, k + d)).as_numer_denom()
    expected_denominator = (
        (d + 5 * k) ** 2
        * (d + 5 * k - 9)
        * (d + 5 * k - 5) ** 2
        * (d + 5 * k - 4)
        * (d + 5 * k - 1)
        * (d + 5 * k + 4)
    )
    assert sp.factor(denominator - expected_denominator) == 0

    polynomial = sp.Poly(sp.expand(numerator), h, w)
    coefficients = {monomial: coefficient for monomial, coefficient in polynomial.terms()}
    assert set(coefficients) == {
        (2, 2), (2, 1), (2, 0),
        (1, 3), (1, 2), (1, 1), (1, 0),
        (0, 4), (0, 3), (0, 2), (0, 1), (0, 0),
    }

    # On k=K+2, d=D+3, every coefficient except the linear w term of
    # the h-free part is coefficientwise nonnegative.
    for monomial, coefficient in coefficients.items():
        if monomial == (0, 1):
            continue
        shifted = coefficient.subs(
            {k: K + 2, d: D + 3}, simultaneous=True
        )
        assert_nonnegative_coefficients(shifted, K, D)

    c0 = coefficients[(0, 0)]
    c1 = coefficients[(0, 1)]
    c2 = coefficients[(0, 2)]
    negative_discriminant = sp.factor(4 * c0 * c2 - c1**2)
    shifted_discriminant = negative_discriminant.subs(
        {k: K + 2, d: D + 3}, simultaneous=True
    )
    assert_nonnegative_coefficients(shifted_discriminant, K, D)

    print("PASS: exact two-step map preserves log-concavity for k>=2, d>=3")


def normalized_coefficient(dd: int, kk: sp.Expr) -> sp.Expr:
    z = sp.symbols("z")
    generating = sum(sp.Rational(5, j + 5) * z**j for j in range(dd + 2))
    return sp.factor(
        sp.factorial(dd)
        * sp.series(generating**kk, z, 0, dd + 1).removeO().coeff(z, dd)
    )


def verify_boundary_strips() -> None:
    expected = {
        1: 5 * (33 * k + 2) / sp.Integer(252),
        2: 25 * (1155 * k**3 + 2426 * k**2 + 1435 * k + 168)
        / sp.Integer(63504),
    }
    for dd in (1, 2):
        defect = sp.factor(
            normalized_coefficient(dd, k) ** 2
            - normalized_coefficient(dd + 1, k - 1)
            * normalized_coefficient(dd - 1, k + 1)
        )
        assert sp.factor(defect - expected[dd]) == 0
        assert_nonnegative_coefficients(expected[dd].as_numer_denom()[0], k)
    print("PASS: exact boundary defects for d=1,2 are strictly positive")


def verify_original_wedge_comparison() -> None:
    total = 5 * k + d
    target_weight = d / (d + 1) * k / (k + 1)
    for i in range(1, 5):
        target_weight *= (total + i) / (total - i + 1)
    numerator = sp.factor(sp.together(1 - target_weight).as_numer_denom()[0])

    # Strictly inside the wedge: k=2d+1+S, d=1+U.
    interior = numerator.subs(
        {d: U + 1, k: 2 * (U + 1) + 1 + S}, simultaneous=True
    )
    assert_nonnegative_coefficients(interior, S, U)

    # Boundary k=2d is automatic from d>=12.  The remaining d<=11
    # cases are included in the independent all-k certificate d<=18.
    boundary = numerator.subs(
        {d: U + 12, k: 2 * (U + 12)}, simultaneous=True
    )
    assert_nonnegative_coefficients(boundary, U)

    # Low-density wedge: d=12k+S, k=K+3.  The cases k=1 and k=2 are
    # already trivial / independently proved for all n.
    low_density = numerator.subs(
        {k: K + 3, d: 12 * (K + 3) + S}, simultaneous=True
    )
    assert_nonnegative_coefficients(low_density, K, S)
    print(
        "PASS: auxiliary LC implies the original r=5 inequality "
        "for k>=2d and for d>=12k (k>=3)"
    )


if __name__ == "__main__":
    verify_two_step_preserver()
    verify_boundary_strips()
    verify_original_wedge_comparison()
