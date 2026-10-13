"""Exact and destructive checks for the S42 effective low-frequency gate.

The proof of the inequalities is in S42.  This script freezes the homogeneous
logarithmic pieces, checks the constant ledger, and attacks branch or scaling
mistakes in the exponentiated bound.
"""

from __future__ import annotations

import cmath
import math
import random

import sympy as sp

from check_explicit_log_remainder import exact_truncations


def homogeneous(poly: sp.Expr, variables: tuple[sp.Symbol, ...], degree: int) -> sp.Expr:
    return sp.expand(
        sum(
            coefficient * sp.prod(v**power for v, power in zip(variables, powers, strict=True))
            for powers, coefficient in sp.Poly(poly, *variables).terms()
            if sum(powers) == degree
        )
    )


def corrections() -> tuple[tuple[sp.Symbol, ...], list[sp.Expr]]:
    initial, increment = exact_truncations()
    variables = tuple(sorted(initial.free_symbols | increment.free_symbols, key=lambda x: x.name))
    pieces = [
        homogeneous(initial, variables, j) + homogeneous(increment, variables, j + 2)
        for j in range(1, 5)
    ]
    return variables, pieces


def edgeworth_polynomial(pieces: list[sp.Expr], epsilon: sp.Symbol) -> sp.Expr:
    t = sp.symbols("t", real=True)
    exponent = sum(t**j * epsilon**j * piece for j, piece in enumerate(pieces, start=1))
    return sp.expand(sp.series(sp.exp(exponent), t, 0, 5).removeO().subs(t, 1))


def main() -> None:
    variables, pieces = corrections()
    a, b, c = variables
    epsilon = sp.symbols("epsilon", positive=True)

    # Freeze the four exact corrections and the fact that no other degrees occur.
    initial, increment = exact_truncations()
    rebuilt = -(a * a + b * b + c * c) / 2 + sum(pieces)
    assert sp.simplify(rebuilt - (initial + increment)) == 0
    polynomial = edgeworth_polynomial(pieces, epsilon)
    assert sp.Poly(polynomial, epsilon).degree() == 4

    # Constant ledger for q <= R^2/60 + 1/5000.
    r2_coefficient = (
        sp.Rational(2, 128)
        + sp.Rational(3, 4 * 128**2)
        + sp.Rational(5, 6 * 256**2)
        + sp.Rational(1, 128**3)
        + sp.Rational(5, 3 * 128**4)
    )
    constant = (
        sp.Rational(1, 6144)
        + sp.Rational(13, 9) / sp.sqrt(3) / 128**3
        + sp.Rational(41, 36) / 128**4
    )
    assert r2_coefficient < sp.Rational(1, 60)
    assert constant < sp.Rational(1, 5000)

    radial_integral = sp.simplify(
        2
        * sp.pi
        * sp.gamma(sp.Rational(7, 2))
        * sp.gamma(sp.Rational(1, 2))
        / sp.gamma(4)
    )
    assert sp.simplify(radial_integral - 5 * sp.pi**2 / 8) == 0
    plancherel_constant = sp.simplify(
        3 * sp.sqrt(radial_integral) / (2 * sp.pi) ** sp.Rational(3, 2)
    )
    assert sp.simplify(plancherel_constant - 3 * sp.sqrt(5) / (8 * sp.sqrt(sp.pi))) == 0

    piece_function = [sp.lambdify(variables, piece, "math") for piece in pieces]
    edgeworth_function = sp.lambdify((*variables, epsilon), polynomial, "math")
    rng = random.Random(4201)
    worst_ratio = 0.0
    # Ordinary binary64 loses the logarithm of d1,d2 after exponentiation by
    # about 10^12; the destructive control therefore stays below that purely
    # numerical regime.  The analytic inequalities have no such restriction.
    for r in (2**16, 10**6, 10**8):
        eps = r**-0.5
        radius_limit = r ** (1.0 / 16.0)
        for _ in range(4000):
            direction = [rng.gauss(0.0, 1.0) for _ in range(3)]
            norm = math.sqrt(sum(x * x for x in direction))
            radius = radius_limit * rng.random() ** (1.0 / 3.0)
            av, bv, cv = [radius * x / norm for x in direction]
            u0, u1, u2 = eps * av, eps * bv, eps * cv
            d1 = 1 - u0 * u0 / 3 + u1 * u1 + u2 * u2 / 2 - 2j * u0 / math.sqrt(3)
            d2 = 1 + u2 * u2 / 2 + 2j * u0 / math.sqrt(3)
            exact = d1 ** (-(r + 1) / 2) * d2 ** (-r / 2)
            approximation = math.exp(-radius * radius / 2) * edgeworth_function(
                av, bv, cv, eps
            )
            bracket = 7 * (1 + radius) ** 7 + (13 / 30) * 73**5 * (1 + radius) ** 30
            bound = eps**5 * math.exp(-23 * radius * radius / 94 + 1 / 5000) * bracket
            error = abs(exact - approximation)
            if bound > 0:
                worst_ratio = max(worst_ratio, error / bound)
            assert error <= bound + 2e-14, (
                f"r={r} radius={radius} error={error} bound={bound} "
                f"exact={exact} approximation={approximation}"
            )

            q = sum(
                eps**j * abs(function(av, bv, cv))
                for j, function in enumerate(piece_function, start=1)
            )
            assert q <= radius * radius / 60 + 1 / 5000 + 1e-12

    print("PASS exact logarithmic exponent splits into A1,...,A4")
    print("PASS explicit q envelope coefficient ledger")
    print("PASS weighted Plancherel radial integral and four-derivative constant")
    print(f"PASS destructive low-frequency exponentiation samples (worst ratio {worst_ratio:.3e})")


if __name__ == "__main__":
    main()
