"""Exact certificate that the compact-bulk third coefficient is positive.

The coefficient C3 in

    log(coefficient ratio / target weight)
        = M/k + C2/k^2 + C3/k^3 + O(k^-4)

is reconstructed from the lattice saddlepoint expansion and then reduced to
a rational polynomial sign problem on the same compact saddle interval used
by verify_bulk_second_order_margin.py.
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
)


def gaussian_integral(poly: sp.Expr, variable: sp.Symbol, variance: sp.Symbol) -> sp.Expr:
    result = 0
    for (power,), coefficient in sp.Poly(sp.expand(poly), variable).terms():
        if power % 2 == 0:
            moment = sp.factorial2(power - 1) if power else 1
            result += coefficient * moment / variance ** (power // 2)
    return sp.factor(result)


def derive_third_coefficient() -> tuple[sp.Expr, sp.Symbol, sp.Symbol]:
    u, epsilon, displacement, variance = sp.symbols(
        "u epsilon displacement variance", real=True
    )
    inverse_k, mu = sp.symbols("inverse_k mu", real=True)
    cumulants = {order: sp.symbols(f"kappa_{order}") for order in range(3, 7)}

    exponent = -sp.I * displacement * u * epsilon
    for order in range(3, 7):
        exponent += (
            cumulants[order]
            * (sp.I * u) ** order
            / sp.factorial(order)
            * epsilon ** (order - 2)
        )
    expansion = sp.series(sp.exp(exponent), epsilon, 0, 7).removeO().expand()
    probability = {
        order: gaussian_integral(expansion.coeff(epsilon, 2 * order), u, variance)
        for order in range(1, 4)
    }
    log_terms = {
        1: probability[1],
        2: sp.factor(probability[2] - probability[1] ** 2 / 2),
        3: sp.factor(
            probability[3]
            - probability[1] * probability[2]
            + probability[1] ** 3 / 3
        ),
    }

    def local_log(offset: int, shift: sp.Expr) -> sp.Expr:
        sample_size = 1 / inverse_k + offset
        return -sp.log(sample_size) / 2 + sum(
            log_terms[order].subs(displacement, shift) / sample_size**order
            for order in range(1, 4)
        )

    a = mu + 1
    probability_ratio = sp.series(
        2 * local_log(0, 0)
        - local_log(-1, a)
        - local_log(1, -a),
        inverse_k,
        0,
        4,
    ).removeO().expand()
    probability_third = probability_ratio.coeff(inverse_k, 3)

    total_scaled = mu + 5
    target = 1 / (1 + inverse_k)
    for index in range(1, 5):
        target *= (total_scaled + index * inverse_k) / (
            total_scaled - (index - 1) * inverse_k
        )
    target_third = sp.series(
        sp.log(target), inverse_k, 0, 4
    ).removeO().expand().coeff(inverse_k, 3)
    return sp.factor(probability_third - target_third), mu, variance


def reduce_to_saddle_polynomial() -> tuple[sp.Poly, sp.Expr]:
    coefficient, mu_symbol, variance_symbol = derive_third_coefficient()
    z, f = sp.symbols("z f", positive=True)
    reciprocal = 1 / (1 - z)

    def derivative(expr: sp.Expr) -> sp.Expr:
        return sp.factor(
            z * sp.diff(expr, z)
            + (reciprocal - 5 * f) * sp.diff(expr, f)
        )

    mu = sp.factor((reciprocal - 5 * f) / f)
    variance = derivative(mu)
    substitutions: dict[sp.Symbol, sp.Expr] = {
        mu_symbol: mu,
        variance_symbol: variance,
    }
    current = variance
    for order in range(3, 7):
        current = derivative(current)
        substitutions[sp.symbols(f"kappa_{order}")] = current

    numerator, denominator = sp.together(
        sp.factor(coefficient.subs(substitutions))
    ).as_numer_denom()
    reduced = sp.factor(numerator / f**3)
    assert sp.factor(denominator - 24 * (4 * f * z - 5 * f + 1) ** 7) == 0
    return sp.Poly(reduced, f, z), denominator


def verify_negative_strip(polynomial: sp.Poly) -> None:
    lower = lower_series(LOWER_ORDER)
    lower_powers = {0: [Fraction(1)], 1: lower}
    for power in range(2, 8):
        lower_powers[power] = convolve(lower_powers[power - 1], lower)
    one_minus_z = {
        power: [Fraction((-1) ** j * comb(power, j)) for j in range(power + 1)]
        for power in range(8)
    }

    # Substitute f=L_40+t*z^41/(46(1-z)), multiply by (1-z)^7,
    # and certify negativity on (z,t) in [LEFT,RIGHT] x [0,1].
    by_tail_power: list[list[Fraction]] = [[] for _ in range(8)]
    for (f_power, z_power), coefficient in polynomial.terms():
        exact_coefficient = Fraction(int(coefficient))
        for tail_power in range(f_power + 1):
            poly = convolve(
                lower_powers[f_power - tail_power],
                one_minus_z[7 - tail_power],
            )
            poly = shifted(poly, z_power + 41 * tail_power)
            factor = (
                exact_coefficient
                * comb(f_power, tail_power)
                / 46**tail_power
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
        for tail_index in range(8):
            coefficient = sum(
                (
                    z_bernstein[power][z_index]
                    * Fraction(comb(tail_index, power), comb(7, power))
                    for power in range(tail_index + 1)
                ),
                Fraction(0),
            )
            assert coefficient < 0
    print("PASS: rational Bernstein certificate gives C3 > 0")


if __name__ == "__main__":
    saddle_polynomial, _ = reduce_to_saddle_polynomial()
    print("PASS: exact third-order saddlepoint reduction")
    verify_negative_strip(saddle_polynomial)
