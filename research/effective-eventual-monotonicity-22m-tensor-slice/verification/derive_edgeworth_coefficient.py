"""Derive and numerically evaluate the first Edgeworth correction to I_r/r.

This is a discovery calculation, not a rigorous asymptotic remainder bound.  The
cumulant polynomial is exact; only its final spherical integral is numerical.
"""

from __future__ import annotations

import math

import scipy.integrate
import sympy as sp


X, T, Y, Z, P1, P2 = sp.symbols("x t y z p1 p2", real=True)
GAUSSIANS = (X, T, Y, Z, P1, P2)
S0, S1, S2 = sp.symbols("s0 s1 s2", real=True)
W0, W1, W2 = sp.symbols("w0 w1 w2", real=True)


def gaussian_moment(poly: sp.Expr) -> sp.Expr:
    result = sp.Integer(0)
    for exponents, coefficient in sp.Poly(sp.expand(poly), *GAUSSIANS).terms():
        moment = sp.Integer(1)
        for exponent in exponents:
            if exponent % 2:
                moment = sp.Integer(0)
                break
            if exponent:
                moment *= sp.factorial2(exponent - 1)
        result += coefficient * moment
    return sp.simplify(result)


def hermite(index: int, variable: sp.Symbol) -> sp.Expr:
    return sp.hermite_prob(index, variable)


def differential_symbol_to_hermite(poly: sp.Expr) -> sp.Expr:
    result = sp.Integer(0)
    for exponents, coefficient in sp.Poly(sp.expand(poly), S0, S1, S2).terms():
        result += coefficient * sp.prod(
            hermite(index, variable)
            for index, variable in zip(exponents, (W0, W1, W2), strict=True)
        )
    return sp.expand(result)


def exact_edgeworth_polynomials() -> tuple[sp.Expr, sp.Expr]:
    # Whitened coordinates: matrix entries are
    # a=sqrt(3)w0+w1, b=sqrt(3)w0-w1, c=sqrt(2)w2.
    increment = (
        (X**2 + T**2 - 2 * Y**2) / (2 * sp.sqrt(3)),
        (X**2 - T**2) / 2,
        (X * T + Y * Z) / sp.sqrt(2),
    )
    initial = (
        (P1**2 + P2**2) / (2 * sp.sqrt(3)),
        (P1**2 - P2**2) / 2,
        P1 * P2 / sp.sqrt(2),
    )
    direction = (S0, S1, S2)
    linear_increment = sum(
        coefficient * coordinate
        for coefficient, coordinate in zip(direction, increment, strict=True)
    )
    linear_initial = sum(
        coefficient * coordinate
        for coefficient, coordinate in zip(direction, initial, strict=True)
    )

    increment_second = gaussian_moment(linear_increment**2)
    assert sp.simplify(increment_second - (S0**2 + S1**2 + S2**2)) == 0
    increment_third_moment = gaussian_moment(linear_increment**3)
    increment_fourth_moment = gaussian_moment(linear_increment**4)
    increment_fifth_moment = gaussian_moment(linear_increment**5)
    increment_sixth_moment = gaussian_moment(linear_increment**6)
    increment_third_cumulant = increment_third_moment
    increment_fourth_cumulant = sp.expand(
        increment_fourth_moment - 3 * increment_second**2
    )
    increment_fifth_cumulant = sp.expand(
        increment_fifth_moment
        - 10 * increment_third_moment * increment_second
    )
    increment_sixth_cumulant = sp.expand(
        increment_sixth_moment
        - 15 * increment_fourth_moment * increment_second
        - 10 * increment_third_moment**2
        + 30 * increment_second**3
    )

    initial_mean = gaussian_moment(linear_initial)
    centered_initial = sp.expand(linear_initial - initial_mean)
    initial_variance = sp.expand(
        gaussian_moment(centered_initial**2)
    )
    initial_third_cumulant = sp.expand(
        gaussian_moment(centered_initial**3)
    )
    initial_fourth_cumulant = sp.expand(
        gaussian_moment(centered_initial**4) - 3 * initial_variance**2
    )

    order_half = initial_mean + increment_third_cumulant / 6
    order_one = initial_variance / 2 + increment_fourth_cumulant / 24
    order_three_halves = (
        initial_third_cumulant / 6 + increment_fifth_cumulant / 120
    )
    order_two = initial_fourth_cumulant / 24 + increment_sixth_cumulant / 720
    first_correction_symbol = order_one + order_half**2 / 2
    second_correction_symbol = (
        order_two
        + order_half * order_three_halves
        + order_one**2 / 2
        + order_half**2 * order_one / 2
        + order_half**4 / 24
    )
    return (
        differential_symbol_to_hermite(first_correction_symbol),
        differential_symbol_to_hermite(second_correction_symbol),
    )


def radial_moment(power: int) -> float:
    return (
        2.0 ** (power / 2)
        * math.gamma((power + 3) / 2)
        / math.gamma(1.5)
    )


def even_monomials(poly: sp.Expr) -> list[tuple[tuple[int, int, int], float]]:
    terms: list[tuple[tuple[int, int, int], float]] = []
    for exponents, coefficient in sp.Poly(poly, W0, W1, W2).terms():
        if any(exponent % 2 for exponent in exponents):
            continue
        terms.append((exponents, float(sp.N(coefficient, 30))))
    return terms


def evaluate_coefficient(poly: sp.Expr) -> tuple[float, float]:
    terms = even_monomials(poly)

    def radial_polynomial(u0: float, phi: float) -> float:
        radius = math.sqrt(max(0.0, 1.0 - u0 * u0))
        u1 = radius * math.cos(phi)
        u2 = radius * math.sin(phi)
        total = 0.0
        for exponents, coefficient in terms:
            degree = sum(exponents)
            total += (
                coefficient
                * radial_moment(degree + 2)
                * u0 ** exponents[0]
                * u1 ** exponents[1]
                * u2 ** exponents[2]
            )
        return total

    def phi_integral(u0: float) -> float:
        radius_squared = 1.0 - u0 * u0

        def integrand(phi: float) -> float:
            q_value = 3 * u0 * u0 - radius_squared * (
                math.cos(phi) ** 2 + 2 * math.sin(phi) ** 2
            )
            return abs(q_value) * radial_polynomial(u0, phi)

        points: list[float] = []
        u0_squared = u0 * u0
        if 0.25 < u0_squared < 0.4:
            crossing = math.asin(
                math.sqrt((4 * u0_squared - 1) / radius_squared)
            )
            points.append(crossing)
        value, error = scipy.integrate.quad(
            integrand,
            0.0,
            math.pi / 2,
            points=points or None,
            epsabs=2e-10,
            epsrel=2e-10,
            limit=160,
        )
        return 4 * value

    split_points = (0.0, 0.5, math.sqrt(0.4), 1.0)
    total = 0.0
    total_error = 0.0
    for lower, upper in zip(split_points[:-1], split_points[1:], strict=True):
        value, error = scipy.integrate.quad(
            phi_integral,
            lower,
            upper,
            epsabs=2e-8,
            epsrel=2e-8,
            limit=160,
        )
        total += value
        total_error += error
    # The normalized sphere integral is 2/(4*pi) times the positive-u0 half.
    return total / (2 * math.pi), total_error / (2 * math.pi)


def main() -> None:
    first_polynomial, second_polynomial = exact_edgeworth_polynomials()
    coefficient, quadrature_error = evaluate_coefficient(first_polynomial)
    second_coefficient, second_error = evaluate_coefficient(second_polynomial)
    limit_value, limit_error = evaluate_coefficient(sp.Integer(1))
    print("EXACT FIRST EDGEWORTH HERMITE POLYNOMIAL:")
    print(sp.sstr(first_polynomial))
    print(
        "EXACT SECOND EDGEWORTH HERMITE POLYNOMIAL: "
        f"{len(sp.Poly(second_polynomial, W0, W1, W2).terms())} terms"
    )
    print(f"DISCOVERY ONLY: Gaussian L1 limit={limit_value:.12f}")
    print(f"DISCOVERY ONLY: first 1/r coefficient={coefficient:.12f}")
    print(f"DISCOVERY ONLY: second 1/r^2 coefficient={second_coefficient:.12f}")
    print(
        "DISCOVERY ONLY: predicted adjacent r^-2 margin="
        f"{coefficient / limit_value:.12f}"
    )
    print(f"DISCOVERY ONLY: nested quadrature error estimate={quadrature_error:.3g}")
    print(f"DISCOVERY ONLY: second quadrature error estimate={second_error:.3g}")
    print(f"DISCOVERY ONLY: limit quadrature error estimate={limit_error:.3g}")
    print("NOT A PROOF: no explicit Edgeworth remainder bound")


if __name__ == "__main__":
    main()
