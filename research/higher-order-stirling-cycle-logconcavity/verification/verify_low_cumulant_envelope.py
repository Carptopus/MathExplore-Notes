"""Rational low-cumulant envelope for the effective local Fourier proof.

On the compact saddle band this script proves

    (mu+1)/sigma < 7/4,
    sigma < 17,

and, for c_r=kappa_r/(r! sigma^r),

    c_3 < 11/20,  c_4 < 13/20,  c_5 < 17/20,
    c_6 < 6/5,    c_7 < 7/4,    c_8 < 5/2,
    c_9 < 15/4,   c_10 < 11/2.

All cumulants are positive by the compound-Poisson representation certified
in verify_renewal_reformulation.py.  Odd inequalities are squared only after
that positivity fact is established.  The strip checks use exact rational
Bernstein coefficients.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

import sympy as sp

from verify_bulk_second_order_margin import (
    LEFT,
    RIGHT,
    bernstein_coefficients,
    convolve,
    lower_series,
    shifted,
    verify_saddle_interval,
)


# Forty terms already give strictly positive rational Bernstein
# coefficients for all ten inequalities.  Eighty is retained only as a
# fallback so the verifier remains robust if a future algebraic rewrite
# changes coefficient conditioning without changing the theorem.
ORDER = 40


def positive_numerator(expression: sp.Expr, f: sp.Symbol, z: sp.Symbol) -> sp.Poly:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    coefficient, factors = sp.factor_list(denominator)
    sign = sp.sign(coefficient)
    for factor, power in factors:
        if factor == f:
            continue
        if factor == z - 1:
            sign *= (-1) ** power
            continue
        if factor == 1 - z:
            continue
        raise AssertionError(f"unexpected denominator factor: {factor}^{power}")
    assert sign != 0
    normalized = numerator if sign > 0 else -numerator
    return sp.Poly(sp.factor(normalized), f, z)


def saddle_inequalities() -> list[tuple[str, sp.Poly]]:
    z, f = sp.symbols("z f", positive=True)
    reciprocal = 1 / (1 - z)

    def derivative(expr: sp.Expr) -> sp.Expr:
        return sp.factor(
            z * sp.diff(expr, z)
            + (reciprocal - 5 * f) * sp.diff(expr, f)
        )

    mu = sp.factor((reciprocal - 5 * f) / f)
    variance = derivative(mu)
    cumulants = {2: variance}
    for order in range(3, 11):
        cumulants[order] = derivative(cumulants[order - 1])

    results = [
        (
            "(mu+1)/sigma < 7/4",
            positive_numerator(
                sp.Rational(49, 16) * variance - (mu + 1) ** 2,
                f,
                z,
            ),
        ),
        (
            "sigma < 17",
            positive_numerator(289 - variance, f, z),
        ),
    ]
    bounds = {
        3: sp.Rational(11, 20),
        4: sp.Rational(13, 20),
        5: sp.Rational(17, 20),
        6: sp.Rational(6, 5),
        7: sp.Rational(7, 4),
        8: sp.Rational(5, 2),
        9: sp.Rational(15, 4),
        10: sp.Rational(11, 2),
    }
    for order, bound in bounds.items():
        scaled = bound * sp.factorial(order)
        if order % 2:
            expression = scaled**2 * variance**order - cumulants[order] ** 2
        else:
            expression = (
                scaled * variance ** (order // 2) - cumulants[order]
            )
        results.append(
            (
                f"kappa_{order}/({order}! sigma^{order}) < {bound}",
                positive_numerator(expression, f, z),
            )
        )
    return results


def verify_positive_strip(polynomial: sp.Poly, order: int) -> bool:
    lower = lower_series(order)
    f_degree = polynomial.degree(0)
    lower_powers = {0: [Fraction(1)], 1: lower}
    for power in range(2, f_degree + 1):
        lower_powers[power] = convolve(lower_powers[power - 1], lower)
    one_minus_z = {
        power: [Fraction((-1) ** j * comb(power, j)) for j in range(power + 1)]
        for power in range(f_degree + 1)
    }
    by_tail_power: list[list[Fraction]] = [[] for _ in range(f_degree + 1)]
    for (f_power, z_power), coefficient in polynomial.terms():
        exact_coefficient = Fraction(int(coefficient.p), int(coefficient.q))
        for tail_power in range(f_power + 1):
            poly = convolve(
                lower_powers[f_power - tail_power],
                one_minus_z[f_degree - tail_power],
            )
            poly = shifted(poly, z_power + (order + 1) * tail_power)
            factor = (
                exact_coefficient
                * comb(f_power, tail_power)
                / (order + 6) ** tail_power
            )
            target = by_tail_power[tail_power]
            if len(target) < len(poly):
                target.extend([Fraction(0)] * (len(poly) - len(target)))
            for index, value in enumerate(poly):
                target[index] += factor * value

    z_degree = max(len(poly) for poly in by_tail_power) - 1
    z_bernstein = [
        bernstein_coefficients(poly, LEFT, RIGHT, z_degree)
        for poly in by_tail_power
    ]
    for z_index in range(z_degree + 1):
        for tail_index in range(f_degree + 1):
            coefficient = sum(
                (
                    z_bernstein[power][z_index]
                    * Fraction(comb(tail_index, power), comb(f_degree, power))
                    for power in range(tail_index + 1)
                ),
                Fraction(0),
            )
            if coefficient <= 0:
                return False
    return True


if __name__ == "__main__":
    verify_saddle_interval()
    for label, polynomial in saddle_inequalities():
        order = ORDER
        if not verify_positive_strip(polynomial, order):
            order = 80
            assert verify_positive_strip(polynomial, order), label
        print(f"PASS: {label} (series order {order})", flush=True)
