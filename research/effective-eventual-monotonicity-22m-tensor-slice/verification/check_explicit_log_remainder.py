"""Exact series regression for the explicit S35 logarithmic remainder.

The analytic remainder inequalities are proved in S35.  Random samples are
only destructive controls for sign, branch, and scaling mistakes.
"""

from __future__ import annotations

import cmath
import math
import random

import sympy as sp


def truncate_total_degree(expression: sp.Expr, variables: tuple[sp.Symbol, ...], degree: int) -> sp.Expr:
    result = sp.Integer(0)
    for powers, coefficient in sp.Poly(sp.expand(expression), *variables).terms():
        if sum(powers) <= degree:
            result += coefficient * sp.prod(
                variable**power for variable, power in zip(variables, powers, strict=True)
            )
    return sp.expand(result)


def exact_truncations() -> tuple[sp.Expr, sp.Expr]:
    a, b, c, epsilon = sp.symbols("a b c epsilon", real=True)
    d1 = 1 - epsilon**2 * a**2 / 3 + epsilon**2 * b**2 + epsilon**2 * c**2 / 2 - 2 * sp.I * epsilon * a / sp.sqrt(3)
    d2 = 1 + epsilon**2 * c**2 / 2 + 2 * sp.I * epsilon * a / sp.sqrt(3)
    initial_series = sp.series(-sp.log(d1) / 2, epsilon, 0, 5).removeO().subs(epsilon, 1)
    increment_series = sp.series(-sp.log(d1 * d2) / 2, epsilon, 0, 7).removeO().subs(epsilon, 1)
    variables = (a, b, c)
    return (
        truncate_total_degree(initial_series, variables, 4),
        truncate_total_degree(increment_series, variables, 6),
    )


def evaluate(expression: sp.Expr, values: tuple[float, float, float]) -> complex:
    a, b, c = sorted(expression.free_symbols, key=lambda item: item.name)
    return complex(expression.evalf(30, subs={a: values[0], b: values[1], c: values[2]}))


def main() -> None:
    initial, increment = exact_truncations()
    a, b, c = sp.symbols("a b c", real=True)
    # The increment has no linear term and its quadratic term is exactly the
    # standard-Gaussian exponent.
    increment_poly = sp.Poly(increment, a, b, c)
    degree_two = sum(
        coefficient * a**powers[0] * b**powers[1] * c**powers[2]
        for powers, coefficient in increment_poly.terms()
        if sum(powers) == 2
    )
    assert sp.simplify(degree_two + (a * a + b * b + c * c) / 2) == 0

    initial_function = sp.lambdify((a, b, c), initial, "math")
    increment_function = sp.lambdify((a, b, c), increment, "math")
    rng = random.Random(3501)
    worst_initial = 0.0
    worst_increment = 0.0
    for _ in range(30_000):
        direction = [rng.gauss(0.0, 1.0) for _ in range(3)]
        norm = math.sqrt(sum(value * value for value in direction))
        radius = 0.25 * rng.random() ** (1.0 / 3.0)
        av, bv, cv = [radius * value / norm for value in direction]
        d1 = 1 - av * av / 3 + bv * bv + cv * cv / 2 - 2j * av / math.sqrt(3)
        d2 = 1 + cv * cv / 2 + 2j * av / math.sqrt(3)
        exact_initial = -0.5 * cmath.log(d1)
        exact_increment = -0.5 * cmath.log(d1 * d2)
        initial_error = abs(exact_initial - initial_function(av, bv, cv))
        increment_error = abs(exact_increment - increment_function(av, bv, cv))
        if radius > 0.0:
            worst_initial = max(worst_initial, initial_error / radius**5)
            worst_increment = max(worst_increment, increment_error / radius**7)
        assert initial_error <= 3.0 * radius**5 + 5.0e-15
        assert increment_error <= 4.0 * radius**7 + 5.0e-15

    print("PASS exact initial log expansion through total degree 4")
    print("PASS exact increment log expansion through total degree 6")
    print("PASS increment quadratic term is -|u|^2/2")
    print(
        "PASS destructive samples obey explicit remainder bounds "
        f"(worst ratios {worst_initial:.6g}, {worst_increment:.6g})"
    )


if __name__ == "__main__":
    main()
