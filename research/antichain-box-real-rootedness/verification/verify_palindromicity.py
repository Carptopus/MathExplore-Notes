"""Exact calibration for the palindromicity and strict gamma claims.

This script is supporting evidence only. The general result is proved in the
manuscript; finite symbolic checks do not replace that proof.
"""

from __future__ import annotations

import json

import sympy as sp


x, t = sp.symbols("x t")


def antichain_determinant(m: int, n: int) -> sp.Expr:
    a = sum(
        sp.binomial(m, j) * sp.binomial(n, j) * x**j
        for j in range(min(m, n) + 1)
    )
    b = sum(
        sp.binomial(m + 1, j + 1) * sp.binomial(n - 1, j - 1) * x**j
        for j in range(1, min(m, n) + 1)
    )
    c = sum(
        sp.binomial(m - 1, j - 1) * sp.binomial(n + 1, j + 1) * x**j
        for j in range(1, min(m, n) + 1)
    )
    return sp.expand(a * a - b * c)


def is_palindromic(poly: sp.Expr) -> bool:
    coefficients = sp.Poly(poly, x).all_coeffs()
    return coefficients == list(reversed(coefficients))


def gamma_coefficients(poly: sp.Expr) -> list[int]:
    degree = sp.degree(poly, x)
    remainder = sp.Poly(poly, x)
    gamma: list[int] = []
    for j in range(degree // 2 + 1):
        coefficient = remainder.nth(j)
        gamma.append(int(coefficient))
        remainder -= sp.Poly(
            coefficient * x**j * (1 + x) ** (degree - 2 * j), x
        )
    assert remainder.is_zero
    return gamma


def main() -> None:
    identity_checks = []
    for r in range(1, 31):
        j = sp.jacobi(r, 0, 1, t)
        j_tilde = sp.jacobi(r, 1, 0, t)
        h = (t - 1) * sp.jacobi(r - 1, 2, 1, t)
        k = (t + 1) * sp.jacobi(r - 1, 1, 2, t)

        identity_1 = sp.expand(2 * (j - j_tilde) - (h - k)) == 0
        identity_2 = sp.expand(
            2 * r * (j + j_tilde) - (r + 2) * (h + k)
        ) == 0
        e = sp.expand(j**2 - sp.Rational(r + 2, 4 * r) * h**2)
        evenness = sp.expand(e.subs(t, -t) - e) == 0
        assert identity_1 and identity_2 and evenness
        identity_checks.append(r)

    classification_checks = []
    for m in range(1, 13):
        for n in range(1, 13):
            poly = antichain_determinant(m, n)
            observed = is_palindromic(poly)
            expected = abs(m - n) == 1
            assert observed == expected, (m, n, poly)
            classification_checks.append([m, n, observed])

    gamma_checks = []
    for r in range(1, 21):
        poly = antichain_determinant(r, r + 1)
        gamma = gamma_coefficients(poly)
        assert all(value > 0 for value in gamma)
        if r % 2 == 0:
            s = r // 2
            expected_signed_value = sp.binomial(2 * s, s) ** 2 / (s + 1)
        else:
            s = (r - 1) // 2
            expected_signed_value = (
                2 * (2 * s + 1) * sp.binomial(2 * s, s) ** 2 / (s + 1) ** 2
            )
        signed_value = sp.expand((-1) ** r * poly.subs(x, -1))
        assert signed_value == expected_signed_value
        assert signed_value > 0
        gamma_checks.append(
            {
                "r": r,
                "gamma": gamma,
                "signed_value_at_minus_one": int(signed_value),
            }
        )

    destructive_controls = []
    for r in range(1, 13):
        square = is_palindromic(antichain_determinant(r, r))
        gap_two = is_palindromic(antichain_determinant(r, r + 2))
        assert not square and not gap_two
        destructive_controls.append(
            {"r": r, "square": square, "gap_two": gap_two}
        )

    print(
        json.dumps(
            {
                "status": "PASS",
                "jacobi_identity_r": identity_checks,
                "classification_pairs": len(classification_checks),
                "gamma_cases": gamma_checks,
                "destructive_controls": destructive_controls,
                "boundary": (
                    "Finite exact calibration; not a proof of the general theorem."
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
