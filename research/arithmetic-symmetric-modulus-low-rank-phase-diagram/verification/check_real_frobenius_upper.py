"""Symbolic regression checks for the real two-dimensional Frobenius proof.

The universal inequalities in S4 are proved in the accompanying mathematics;
this script guards the algebraic trace, determinant, and rationalization steps.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    h, x, L = sp.symbols("h x L", positive=True, real=True)
    alpha = L + h**2 - x**2
    u = h - x
    v = h + x

    quadratic = sp.Matrix(
        [
            [-u**2 / (4 * alpha), sp.Rational(1, 2) - u * v / (4 * alpha)],
            [sp.Rational(1, 2) - u * v / (4 * alpha), -v**2 / (4 * alpha)],
        ]
    )
    assert sp.factor(sp.trace(quadratic) + (h**2 + x**2) / (2 * alpha)) == 0
    assert sp.factor(quadratic.det() + L / (4 * alpha)) == 0

    spectral_sum = h**2 + x**2
    r = h * x
    radicand_1 = spectral_sum**2 + 4 * alpha * L
    radicand_2 = (2 * L + h**2 - x**2) ** 2 + 4 * r**2
    assert sp.expand(radicand_1 - radicand_2) == 0

    R = sp.sqrt(radicand_2)
    lambda_plus = (R - spectral_sum) / (4 * alpha)
    rationalized = sp.simplify(
        L / lambda_plus - (R + spectral_sum)
    )
    assert rationalized == 0

    S = sp.symbols("S", real=True)
    profile = S + sp.sqrt((2 - S) ** 2 + 4 * r**2)
    derivative = sp.diff(profile, S)
    expected_derivative = 1 - (2 - S) / sp.sqrt((2 - S) ** 2 + 4 * r**2)
    assert sp.simplify(derivative - expected_derivative) == 0

    # The h=1 or x=1 boundary is handled without dividing by alpha or
    # lambda_plus.  This identity certifies the squaring step in that branch.
    boundary_gap = sp.expand(
        (1 - r + r**2) ** 2 - (r**2 + (1 - r) ** 2)
    )
    assert sp.factor(boundary_gap - r**2 * (1 - r) ** 2) == 0

    print("PASS: exact real Frobenius upper-bound identities")


if __name__ == "__main__":
    main()
