"""Exact transform checks for the whitened TR-16 matrix walk."""

from __future__ import annotations

import sympy as sp

from derive_edgeworth_coefficient import (
    differential_symbol_to_hermite,
    exact_edgeworth_polynomials,
)


def main() -> None:
    s0, s1, s2, epsilon = sp.symbols("s0 s1 s2 epsilon", real=True)
    root3 = sp.sqrt(3)

    # Quadratic-form matrices for one increment K and the initial rank-one P.
    increment_form = sp.Matrix(
        (
            (s0 / (2 * root3) + s1 / 2, s2 / (2 * sp.sqrt(2)), 0, 0),
            (s2 / (2 * sp.sqrt(2)), s0 / (2 * root3) - s1 / 2, 0, 0),
            (0, 0, -s0 / root3, s2 / (2 * sp.sqrt(2))),
            (0, 0, s2 / (2 * sp.sqrt(2)), 0),
        )
    )
    initial_form = sp.Matrix(
        (
            (s0 / (2 * root3) + s1 / 2, s2 / (2 * sp.sqrt(2))),
            (s2 / (2 * sp.sqrt(2)), s0 / (2 * root3) - s1 / 2),
        )
    )

    d1 = sp.expand((1 - s0 / root3) ** 2 - s1**2 - s2**2 / 2)
    d2 = sp.expand(1 + 2 * s0 / root3 - s2**2 / 2)
    assert sp.simplify((sp.eye(4) - 2 * increment_form).det() - d1 * d2) == 0
    assert sp.simplify((sp.eye(2) - 2 * initial_form).det() - d1) == 0

    # The normalized sum has exact MGF
    # d1(epsilon*s)^(-(r+1)/2) d2(epsilon*s)^(-r/2), epsilon=r^(-1/2).
    d1_epsilon = d1.subs(
        {s0: epsilon * s0, s1: epsilon * s1, s2: epsilon * s2}
    )
    d2_epsilon = d2.subs(
        {s0: epsilon * s0, s1: epsilon * s1, s2: epsilon * s2}
    )
    log_transform = sp.expand(
        -sp.Rational(1, 2) * (epsilon**-2 + 1) * sp.log(d1_epsilon)
        -sp.Rational(1, 2) * epsilon**-2 * sp.log(d2_epsilon)
    )
    series = sp.series(log_transform, epsilon, 0, 5).removeO()
    gaussian_term = sp.expand(series).coeff(epsilon, 0)
    assert sp.simplify(
        gaussian_term - (s0**2 + s1**2 + s2**2) / 2
    ) == 0

    log_coefficients = [
        sp.expand(series).coeff(epsilon, order) for order in range(1, 5)
    ]
    l1, l2, l3, l4 = log_coefficients
    first_symbol = sp.expand(l2 + l1**2 / 2)
    second_symbol = sp.expand(
        l4 + l1 * l3 + l2**2 / 2 + l1**2 * l2 / 2 + l1**4 / 24
    )
    first_polynomial, second_polynomial = exact_edgeworth_polynomials()
    assert sp.simplify(
        differential_symbol_to_hermite(first_symbol) - first_polynomial
    ) == 0
    assert sp.simplify(
        differential_symbol_to_hermite(second_symbol) - second_polynomial
    ) == 0

    # Destructive control: omitting the initial rank-one factor changes the
    # epsilon coefficient and therefore the first finite-r correction.
    broken_log_transform = sp.expand(
        -sp.Rational(1, 2) * epsilon**-2 * sp.log(d1_epsilon)
        -sp.Rational(1, 2) * epsilon**-2 * sp.log(d2_epsilon)
    )
    assert sp.simplify(
        sp.expand(series).coeff(epsilon, 1)
        - sp.expand(sp.series(broken_log_transform, epsilon, 0, 2).removeO()).coeff(
            epsilon, 1
        )
    ) != 0

    print("PASS: exact increment and initial quadratic-form determinants")
    print("PASS: exact normalized MGF has identity Gaussian covariance")
    print("PASS: exact MGF reproduces the first two Edgeworth polynomials")
    print("PASS: initial-factor destructive control changes the first correction")


if __name__ == "__main__":
    main()
