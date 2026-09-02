"""Exact certificate that the compact-bulk fifth coefficient is positive.

The script reconstructs C5 in

    log(coefficient ratio / target weight)
        = M/k + C2/k^2 + C3/k^3 + C4/k^4 + C5/k^5 + O(k^-6)

and proves C5 > 0 on 1/2 <= mu <= 12 by rational Bernstein arithmetic.
It does not control the remaining O(k^-6) term.
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


def gaussian_integral(
    polynomial: sp.Expr, variable: sp.Symbol, variance: sp.Symbol
) -> sp.Expr:
    result = 0
    for (power,), coefficient in sp.Poly(sp.expand(polynomial), variable).terms():
        if power % 2 == 0:
            moment = sp.factorial2(power - 1) if power else 1
            result += coefficient * moment / variance ** (power // 2)
    return sp.factor(result)


def derive_fifth_coefficient() -> tuple[sp.Expr, sp.Symbol, sp.Symbol]:
    u, epsilon, displacement, variance = sp.symbols(
        "u epsilon displacement variance", real=True
    )
    inverse_k, mu = sp.symbols("inverse_k mu", real=True)
    cumulants = {order: sp.symbols(f"kappa_{order}") for order in range(3, 11)}

    exponent = -sp.I * displacement * u * epsilon
    for order in range(3, 11):
        exponent += (
            cumulants[order]
            * (sp.I * u) ** order
            / sp.factorial(order)
            * epsilon ** (order - 2)
        )
    expansion = sp.series(sp.exp(exponent), epsilon, 0, 11).removeO().expand()
    probability = {
        order: gaussian_integral(expansion.coeff(epsilon, 2 * order), u, variance)
        for order in range(1, 6)
    }
    placeholder = sum(
        probability[order] * inverse_k**order for order in range(1, 6)
    )
    logarithm = sp.series(
        sp.log(1 + placeholder), inverse_k, 0, 6
    ).removeO().expand()
    log_terms = {
        order: sp.factor(logarithm.coeff(inverse_k, order))
        for order in range(1, 6)
    }

    def local_log(offset: int, shift: sp.Expr) -> sp.Expr:
        sample_size = 1 / inverse_k + offset
        return -sp.log(sample_size) / 2 + sum(
            log_terms[order].subs(displacement, shift) / sample_size**order
            for order in range(1, 6)
        )

    a = mu + 1
    probability_ratio = sp.series(
        2 * local_log(0, 0)
        - local_log(-1, a)
        - local_log(1, -a),
        inverse_k,
        0,
        6,
    ).removeO().expand()
    probability_fifth = probability_ratio.coeff(inverse_k, 5)

    total_scaled = mu + 5
    target = 1 / (1 + inverse_k)
    for index in range(1, 5):
        target *= (total_scaled + index * inverse_k) / (
            total_scaled - (index - 1) * inverse_k
        )
    target_fifth = sp.series(
        sp.log(target), inverse_k, 0, 6
    ).removeO().expand().coeff(inverse_k, 5)
    return sp.factor(probability_fifth - target_fifth), mu, variance


def reduce_positive_polynomial() -> sp.Poly:
    coefficient, mu_symbol, variance_symbol = derive_fifth_coefficient()
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
    for order in range(3, 11):
        current = derivative(current)
        substitutions[sp.symbols(f"kappa_{order}")] = current

    numerator, denominator = sp.together(
        coefficient.subs(substitutions)
    ).as_numer_denom()
    base = 4 * f * z - 5 * f + 1
    constant = sp.factor(denominator / base**13)
    if constant != -5760:
        raise AssertionError(f"unexpected denominator factor: {constant}")
    # base=-f^2(1-z)^2 variance<0, hence -5760*base^13>0;
    # C5>0 is therefore equivalent to numerator>0.
    print("PASS: exact fifth-order saddlepoint reduction")
    return sp.Poly(sp.factor(numerator), f, z)


def verify_positive_strip(polynomial: sp.Poly) -> None:
    lower = lower_series(LOWER_ORDER)
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
    print("PASS: rational Bernstein certificate gives C5 > 0")


if __name__ == "__main__":
    verify_saddle_interval()
    positive_polynomial = reduce_positive_polynomial()
    verify_positive_strip(positive_polynomial)
