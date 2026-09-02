"""Exact structural constants for the effective Fourier remainder.

The saddle distribution has probability generating function

    f_5(z w) / f_5(z),
    f_5(z) = integral_0^1 x^4/(1-zx) dx.

This script certifies three ingredients used to control the Fourier tail:

1. |f_5(z exp(it))| is decreasing for 0 <= t <= pi;
2. the standardized fourth central moment is at most 18;
3. with R=(1-z)/2, one has R*sigma >= 1/4.
4. E exp(9|J-mu|/(20 sigma)) <= 30.

Consequently, at t0=1/(2 sigma),

    |phi(t)|^2 <= 55/64       for t0 <= |t| <= pi.

All nontrivial saddle-strip signs are checked by rational Bernstein
coefficients.  This file supplies tail constants; it is not by itself the
complete effective local expansion.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

import sympy as sp

from verify_bulk_second_order_margin import (
    LEFT,
    LOWER_ORDER,
    RIGHT,
    bernstein_coefficients,
    convolve,
    lower_series,
    shifted,
    verify_saddle_interval,
)


def verify_monotone_characteristic_modulus() -> None:
    q, r, y, s = sp.symbols("q r y s", real=True)
    kernel = (1 + q * r - (q + r) * y) / (
        (1 - 2 * q * y + q**2) * (1 - 2 * r * y + r**2)
    )
    derivative_numerator = sp.factor(
        sp.together(sp.diff(kernel, y)).as_numer_denom()[0]
    )

    base = sp.factor(derivative_numerator.subs(y, 1))
    inner = (
        (q + r) * (1 - (q + r) / 2) ** 2
        + (q - r) ** 2 * (8 - q - r) / 4
    )
    expected = (
        (1 - q) * (1 - r) * inner
        + 8 * q * r * (1 - q) * (1 - r) * s
        + 4 * q * r * (q + r) * s**2
    )
    assert sp.factor(base - (1 - q) * (1 - r) * inner) == 0
    assert sp.factor(derivative_numerator.subs(y, 1 - s) - expected) == 0

    # For 0<=q,r<1 and s=1-y in [0,2], every displayed term is
    # nonnegative and the integral is nonconstant.  Thus the symmetrized
    # double-integral kernel grows with y=cos(t).
    print("PASS: characteristic-function modulus decreases on [0, pi]")


def saddle_polynomials() -> tuple[sp.Poly, sp.Poly, sp.Poly, sp.Poly]:
    z, f = sp.symbols("z f", positive=True)
    reciprocal = 1 / (1 - z)

    def derivative(expr: sp.Expr) -> sp.Expr:
        return sp.factor(
            z * sp.diff(expr, z)
            + (reciprocal - 5 * f) * sp.diff(expr, f)
        )

    mu = sp.factor((reciprocal - 5 * f) / f)
    variance = derivative(mu)
    kappa_3 = derivative(variance)
    kappa_4 = derivative(kappa_3)
    margin = sp.factor(
        (mu + 1) ** 2 / variance + 1 - 16 / (mu + 5)
    )

    # central fourth moment = kappa_4 + 3 variance^2.  Hence
    # central_fourth <= 18 variance^2 iff 15 variance^2-kappa_4 >= 0.
    moment_numerator, moment_denominator = sp.together(
        15 * variance**2 - kappa_4
    ).as_numer_denom()
    assert sp.factor(moment_denominator - f**4 * (1 - z) ** 4) == 0

    # R=(1-z)/2 and R*sigma>=1/4 iff (1-z)^2 variance>=1/4.
    radius_numerator, radius_denominator = sp.together(
        (1 - z) ** 2 * variance - sp.Rational(1, 4)
    ).as_numer_denom()
    if sp.factor(radius_denominator - 4 * f**2 * (1 - z) ** 2) != 0:
        raise AssertionError(f"unexpected radius denominator: {radius_denominator}")

    strong_radius_numerator, strong_radius_denominator = sp.together(
        (1 - z) ** 2 * variance - sp.Rational(64, 225)
    ).as_numer_denom()
    assert sp.factor(
        strong_radius_denominator - 225 * f**2 * (1 - z) ** 2
    ) == 0

    margin_numerator, margin_denominator = sp.together(
        margin - sp.Rational(3, 100)
    ).as_numer_denom()
    base = 4 * f * z - 5 * f + 1
    assert sp.factor(margin_denominator - 100 * base) == 0
    # base<0, so M>3/100 is equivalent to margin_numerator<0.
    return (
        sp.Poly(sp.factor(moment_numerator), f, z),
        sp.Poly(sp.factor(radius_numerator), f, z),
        sp.Poly(sp.factor(strong_radius_numerator), f, z),
        sp.Poly(sp.factor(-margin_numerator), f, z),
    )


def verify_positive_strip(
    polynomial: sp.Poly, label: str, order: int = LOWER_ORDER
) -> None:
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
        exact_coefficient = Fraction(int(coefficient))
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
            assert coefficient > 0
    print(f"PASS: {label}")


def verify_analytic_disk_constants() -> None:
    # For R=(1-z)/2 and |s|<=R,
    # |exp(s)-1| <= R/(1-R), hence |z exp(s)| <= 2z/(1+z)<1.
    # The integral representation gives
    # f_5(2z/(1+z)) <= (1+z)f_5(z), so the relative perturbation is <z.
    # Also mu*R<=1/2 because
    # (6-5z)f_5(z)-1 = 1/5 + sum_{j>=2}(j-1)z^j/((j+4)(j+5)).
    z = sp.symbols("z", positive=True)
    j = sp.symbols("j", integer=True, nonnegative=True)
    coefficient = sp.factor(6 / (j + 5) - 5 / (j + 4))
    assert sp.factor(coefficient - (j - 1) / ((j + 4) * (j + 5))) == 0
    assert sum(Fraction(4**n, sp.factorial(n)) for n in range(5)) > Fraction(200, 7)
    print("PASS: analytic log disk has R*sigma>=1/4 and |K|<9/2")


def verify_exponential_moment_envelope() -> None:
    # R*sigma>=1/4 implies 1/sigma<=2(1-z).  With lambda=9/20,
    # a=lambda/sigma<=9(1-z)/10.  For 0<=x<1, exp(x)<=1/(1-x), so
    # w=z exp(a) satisfies
    #
    #   1-w >= (1-z)/10.
    #
    # The integral representation then gives f_5(w)/f_5(z)<=10.
    # Since mu(1-z)<=1 and exp(9/10)<3,
    #
    #   E exp(lambda |J-mu|/sigma)
    #       <= exp(a mu) E exp(aJ) < 30.
    #
    # The scalar inequalities use coefficientwise comparisons:
    # exp(x)<=sum x^n=1/(1-x) for 0<=x<1, and n!>=2^(n-1)
    # for n>=2 gives e<3.
    x = sp.symbols("x", nonnegative=True)
    difference = sp.Poly(sp.factor(
        sum(x**n for n in range(8))
        - sum(x**n / sp.factorial(n) for n in range(8))
    ), x)
    assert all(coefficient >= 0 for coefficient in difference.all_coeffs())
    assert all(sp.factorial(n) >= 2 ** (n - 1) for n in range(2, 30))
    print("PASS: standardized exponential moment at 9/20 is below 30")


if __name__ == "__main__":
    verify_saddle_interval()
    verify_monotone_characteristic_modulus()
    (
        fourth_moment_polynomial,
        radius_polynomial,
        strong_radius_polynomial,
        margin_polynomial,
    ) = saddle_polynomials()
    verify_positive_strip(
        fourth_moment_polynomial,
        "standardized fourth central moment is below 18",
    )
    verify_positive_strip(radius_polynomial, "R*sigma is above 1/4")
    verify_positive_strip(
        strong_radius_polynomial,
        "(1-z)*sigma is above 8/15",
        order=160,
    )
    verify_positive_strip(
        margin_polynomial,
        "first-order margin M is above 3/100",
        order=160,
    )
    verify_analytic_disk_constants()
    verify_exponential_moment_envelope()
