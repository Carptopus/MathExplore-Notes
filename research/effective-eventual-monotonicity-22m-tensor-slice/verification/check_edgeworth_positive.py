"""Certified positivity check for the first TR-16 Edgeworth coefficient.

The exact Gaussian/Hermite calculation reduces the coefficient to a one-
dimensional compact integral.  This script verifies that reduction symbolically
and encloses the remaining integral by outward-rounded interval Riemann sums.
"""

from __future__ import annotations

from mpmath import iv
import sympy as sp

from derive_edgeworth_coefficient import (
    W0,
    W1,
    W2,
    exact_edgeworth_polynomials,
)


INTERVALS = 20_000


def exact_inner_integrand() -> sp.Expr:
    first_polynomial, _ = exact_edgeworth_polynomials()
    x, t = sp.symbols("x t", real=True, nonnegative=True)
    radial_polynomial = sp.Integer(0)
    for exponents, coefficient in sp.Poly(
        first_polynomial, W0, W1, W2
    ).terms():
        if any(exponent % 2 for exponent in exponents):
            continue
        degree = sum(exponents)
        radial_moment = sp.prod(
            2 * index + 3 for index in range((degree + 2) // 2)
        )
        radial_polynomial += (
            coefficient
            * radial_moment
            * x ** exponents[0]
            * (1 - x**2) ** ((exponents[1] + exponents[2]) // 2)
            * (1 - t) ** (exponents[1] // 2)
            * t ** (exponents[2] // 2)
        )

    quadratic = (4 + t) * x**2 - (1 + t)
    crossing = sp.sqrt((1 + t) / (4 + t))
    primitive = sp.integrate(sp.expand(quadratic * radial_polynomial), x)
    return sp.factor(primitive.subs(x, 1) - 2 * primitive.subs(x, crossing))


def expected_inner_integrand() -> sp.Expr:
    t = sp.symbols("t", real=True, nonnegative=True)
    numerator = (
        96 * t**6 * sp.sqrt(t + 1)
        - 48 * t**6 * sp.sqrt(t + 4)
        + 1088 * t**5 * sp.sqrt(t + 1)
        - 472 * t**5 * sp.sqrt(t + 4)
        + 3360 * t**4 * sp.sqrt(t + 1)
        - 1098 * t**4 * sp.sqrt(t + 4)
        - 1488 * t**3 * sp.sqrt(t + 1)
        + 1413 * t**3 * sp.sqrt(t + 4)
        - 2896 * t**2 * sp.sqrt(t + 1)
        + 4604 * t**2 * sp.sqrt(t + 4)
        + 960 * t * sp.sqrt(t + 1)
        - 2832 * t * sp.sqrt(t + 4)
        - 192 * sp.sqrt(t + 4)
    )
    return numerator / (8 * (t + 4) ** sp.Rational(7, 2))


def interval_inner(t):
    return (
        96 * t**6 * iv.sqrt(t + 1)
        - 48 * t**6 * iv.sqrt(t + 4)
        + 1088 * t**5 * iv.sqrt(t + 1)
        - 472 * t**5 * iv.sqrt(t + 4)
        + 3360 * t**4 * iv.sqrt(t + 1)
        - 1098 * t**4 * iv.sqrt(t + 4)
        - 1488 * t**3 * iv.sqrt(t + 1)
        + 1413 * t**3 * iv.sqrt(t + 4)
        - 2896 * t**2 * iv.sqrt(t + 1)
        + 4604 * t**2 * iv.sqrt(t + 4)
        + 960 * t * iv.sqrt(t + 1)
        - 2832 * t * iv.sqrt(t + 4)
        - 192 * iv.sqrt(t + 4)
    ) / (8 * (t + 4) ** iv.mpf("3.5"))


def main() -> None:
    derived = exact_inner_integrand()
    expected = expected_inner_integrand()
    assert sp.simplify(derived - expected) == 0

    pi = iv.mpf(
        [
            "3.14159265358979323846264338327950288",
            "3.14159265358979323846264338327950289",
        ]
    )
    step = pi / (2 * INTERVALS)
    integral = iv.mpf([0, 0])
    for index in range(INTERVALS):
        phi = pi * iv.mpf([index, index + 1]) / (2 * INTERVALS)
        t = iv.sin(phi) ** 2
        integral += interval_inner(t) * step
    coefficient = 2 * integral / pi
    reported_lower = iv.mpf("0.0853526992029")
    reported_upper = iv.mpf("0.0864503864561")
    assert coefficient.a > iv.mpf(0).b
    assert reported_lower.b < coefficient.a
    assert coefficient.b < reported_upper.a

    print("PASS: symbolic sphere-to-one-dimensional reduction")
    print(
        "PASS: first Edgeworth coefficient in outward decimal enclosure "
        "[0.0853526992029, 0.0864503864561]"
    )


if __name__ == "__main__":
    main()
