"""Exact certificate for the compact-bulk second-order margin.

For the anti-diagonal saddlepoint expansion, write

    log(coefficient ratio / target weight)
        = M(mu)/k + C2(mu)/k^2 + O(k^-3).

This script proves C2(mu) > -2 M(mu) on 1/2 <= mu <= 12.  It uses
only rational polynomial arithmetic and Bernstein coefficients.  It does
not bound the remaining O(k^-3) term and therefore is not a proof of the
full conjecture.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

import sympy as sp


LEFT = Fraction(39, 100)
RIGHT = Fraction(193, 200)
LOWER_ORDER = 40


def convolve(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            result[i + j] += first * second
    return result


def shifted(poly: list[Fraction], amount: int) -> list[Fraction]:
    return [Fraction(0)] * amount + poly


def bernstein_coefficients(
    poly: list[Fraction], left: Fraction, right: Fraction, degree: int | None = None
) -> list[Fraction]:
    while poly and poly[-1] == 0:
        poly.pop()
    intrinsic = len(poly) - 1
    target = intrinsic if degree is None else degree
    if target < intrinsic:
        raise ValueError("Bernstein degree cannot be smaller than the polynomial degree")

    width = right - left
    power = [Fraction(0)] * (target + 1)
    for source_degree, coefficient in enumerate(poly):
        for new_degree in range(source_degree + 1):
            power[new_degree] += (
                coefficient
                * comb(source_degree, new_degree)
                * left ** (source_degree - new_degree)
                * width**new_degree
            )
    return [
        sum(
            (
                power[j] * Fraction(comb(i, j), comb(target, j))
                for j in range(i + 1)
            ),
            Fraction(0),
        )
        for i in range(target + 1)
    ]


def lower_series(order: int) -> list[Fraction]:
    return [Fraction(1, j + 5) for j in range(order + 1)]


def evaluate(poly: list[Fraction], value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def upper_value(value: Fraction, order: int) -> Fraction:
    lower = sum(
        (value**j * Fraction(1, j + 5) for j in range(order + 1)),
        Fraction(0),
    )
    return lower + value ** (order + 1) / Fraction(order + 6) / (1 - value)


# P(z,f) is defined by
#
#     C2 + 2 M = -f P(z,f) / (2(4fz-5f+1)^4).
#
# The denominator is positive, so P<0 proves the required inequality.
TERMS = [
    (320, 5, 5), (-1264, 5, 4), (1888, 5, 3), (-1264, 5, 2),
    (320, 5, 1), (-12288, 4, 5), (75120, 4, 4), (-182584, 4, 3),
    (220896, 4, 2), (-133144, 4, 1), (32000, 4, 0), (-12288, 3, 4),
    (59548, 3, 3), (-107615, 3, 2), (86026, 3, 1), (-25675, 3, 0),
    (-4608, 2, 3), (16541, 2, 2), (-19652, 2, 1), (7730, 2, 0),
    (-768, 1, 2), (1794, 1, 1), (-1035, 1, 0),
]


def verify_symbolic_reduction() -> None:
    z, f = sp.symbols("z f", positive=True)
    reciprocal = 1 / (1 - z)

    def derivative(expr: sp.Expr) -> sp.Expr:
        return sp.factor(
            z * sp.diff(expr, z)
            + (reciprocal - 5 * f) * sp.diff(expr, f)
        )

    mu = sp.factor((reciprocal - 5 * f) / f)
    variance = derivative(mu)
    kappa3 = derivative(variance)
    kappa4 = derivative(kappa3)
    displacement = mu + 1
    first = sp.factor(
        displacement**2 / variance + 1 - 16 / (mu + 5)
    )
    second = sp.factor(
        -(
            2 * kappa3**2 * displacement**2
            - 2 * kappa3 * displacement * variance**2
            - kappa4 * displacement**2 * variance
            + variance**4
        )
        / (2 * variance**4)
        - (mu + 1) * (mu + 9) / (2 * (mu + 5) ** 2)
    )
    polynomial = sum(
        coefficient * f**power * z**shift
        for coefficient, power, shift in TERMS
    ) - 48 * z + 52
    expected = -f * polynomial / (2 * (4 * f * z - 5 * f + 1) ** 4)
    assert sp.factor(second + 2 * first - expected) == 0
    print("PASS: exact second-order saddlepoint reduction")


def substituted_polynomial() -> list[Fraction]:
    lower = lower_series(LOWER_ORDER)
    powers = {1: lower}
    for power in range(2, 6):
        powers[power] = convolve(powers[power - 1], lower)
    result = [Fraction(0)] * (5 * LOWER_ORDER + 6)
    for coefficient, power, shift in TERMS:
        for index, value in enumerate(powers[power]):
            result[index + shift] += coefficient * value
    result[1] -= 48
    result[0] += 52
    return result


def verify_saddle_interval() -> None:
    # mu(z)=1/((1-z)f_5(z))-5 is strictly increasing.  The rational
    # lower/upper series bounds place mu=1/2 and mu=12 inside this interval.
    lower_at_left = evaluate(lower_series(40), LEFT)
    assert lower_at_left > Fraction(2, 11) / (1 - LEFT)
    assert upper_value(RIGHT, 160) < Fraction(1, 17) / (1 - RIGHT)
    print("PASS: compact mu-band lies in 39/100 <= z <= 193/200")


def verify_polynomial_sign() -> None:
    # The forty-term lower bound already makes P negative throughout the
    # saddle interval.
    base = substituted_polynomial()
    assert all(value < 0 for value in bernstein_coefficients(base, LEFT, RIGHT))

    # Let f=L+tR, 0<=t<=1, where
    # R=z^41/(46(1-z)) bounds the positive tail.  We prove P_f<0 on the
    # whole strip.  Multiplication by (1-z)^4 clears the positive denominator.
    lower = lower_series(LOWER_ORDER)
    lower_powers = {0: [Fraction(1)], 1: lower}
    for power in range(2, 6):
        lower_powers[power] = convolve(lower_powers[power - 1], lower)
    one_minus_z = {
        power: [Fraction((-1) ** j * comb(power, j)) for j in range(power + 1)]
        for power in range(5)
    }
    by_tail_power: list[list[Fraction]] = [[] for _ in range(5)]
    for coefficient, power, z_shift in TERMS:
        derivative_power = power - 1
        for tail_power in range(derivative_power + 1):
            poly = convolve(
                lower_powers[derivative_power - tail_power],
                one_minus_z[4 - tail_power],
            )
            poly = shifted(poly, z_shift + 41 * tail_power)
            factor = Fraction(
                coefficient
                * power
                * comb(derivative_power, tail_power),
                46**tail_power,
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
        for tail_index in range(5):
            coefficient = sum(
                (
                    z_bernstein[power][z_index]
                    * Fraction(comb(tail_index, power), comb(4, power))
                    for power in range(tail_index + 1)
                ),
                Fraction(0),
            )
            assert coefficient < 0

    print("PASS: rational Bernstein certificate gives C2 > -2 M")


if __name__ == "__main__":
    verify_symbolic_reduction()
    verify_saddle_interval()
    verify_polynomial_sign()
