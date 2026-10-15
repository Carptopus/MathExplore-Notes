"""Exact factorization guard for the complex Frobenius closure in S5."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    L, h, x, k = sp.symbols("L h x k", real=True)
    b_sq = 1 - h**2 - k**2 / (1 - x**2)
    alpha = L + h**2 - x**2
    beta = L - b_sq - k**2
    assert sp.factor((1 - x**2) * (1 - h**2 - b_sq) - k**2) == 0
    determinant = sp.factor(alpha * beta - k**2 * x**2)
    expected = (L + h**2 - 1) * (
        (1 - x**2) * alpha + k**2 * x**2
    ) / (1 - x**2)
    assert sp.factor(determinant - expected) == 0

    # If the second factor vanished for x<1, PSD would force alpha=0 and
    # kx=0.  The two possible branches make beta negative.
    beta_k_zero = sp.simplify(beta.subs({k: 0, L: x**2 - h**2}))
    assert beta_k_zero == x**2 - 1
    beta_x_zero = sp.simplify(beta.subs({x: 0, L: -h**2}))
    assert beta_x_zero == -1

    # At x=1 the normal-form domain forces k=0 and P_11 is the desired
    # boundary factor, so no division by 1-x^2 is used there.
    assert sp.expand(alpha.subs(x, 1) - (L + h**2 - 1)) == 0

    d, e, y = sp.symbols("d e y", real=True)
    first_linear = -h * (d + e) + x * (d - e)
    assert sp.expand(first_linear + (h - x) * d + (h + x) * e) == 0

    print("PASS: exact complex-k closure factorization")


if __name__ == "__main__":
    main()
