from __future__ import annotations

import math

import sympy as sp


def require(condition: bool, message: str) -> None:
    """Fail explicitly even when Python is run with optimization enabled."""
    if not condition:
        raise RuntimeError(message)


def derivative_convolution(poly_p: sp.Expr, poly_q: sp.Expr, x: sp.Symbol, degree: int) -> sp.Expr:
    return sp.expand(
        sum(sp.diff(poly_p, x, k) * sp.diff(poly_q, x, degree - k) for k in range(degree + 1))
    )


def walsh_at_twice_x(poly_p: sp.Expr, poly_q: sp.Expr, x: sp.Symbol, degree: int) -> sp.Expr:
    y = sp.symbols("y")
    p_y = poly_p.subs(x, y)
    q_y = poly_q.subs(x, y)
    convolution = sum(
        sp.diff(p_y, y, k) * sp.diff(q_y, y, degree - k).subs(y, 0)
        for k in range(degree + 1)
    ) / math.factorial(degree)
    return sp.expand(math.factorial(degree) * convolution.subs(y, 2 * x))


def verify_degree(degree: int) -> None:
    x, t = sp.symbols("x t")
    a = sp.symbols(f"a0:{degree + 1}")
    b = sp.symbols(f"b0:{degree + 1}")
    poly_p = sum(a[i] * x**i for i in range(degree + 1))
    poly_q = sum(b[i] * x**i for i in range(degree + 1))

    direct = derivative_convolution(poly_p, poly_q, x, degree)
    walsh = walsh_at_twice_x(poly_p, poly_q, x, degree)
    require(
        sp.expand(direct - walsh) == 0,
        f"degree {degree}: derivative/Walsh identity failed",
    )

    shifted = sum(
        sp.diff(poly_p, x, k).subs(x, x + t)
        * sp.diff(poly_q, x, degree - k).subs(x, x - t)
        for k in range(degree + 1)
    )
    require(
        sp.expand(sp.diff(shifted, t)) == 0,
        f"degree {degree}: telescoping certificate failed",
    )

    # Grace apolar pairing for P(z+t) and Q(-t).
    z = sp.symbols("z")
    a_coeff = [
        sp.factorial(degree - k) * sp.diff(poly_p, x, k).subs(x, z) / sp.factorial(degree)
        for k in range(degree + 1)
    ]
    b_coeff = [
        (-1) ** j * sp.factorial(degree - j) * sp.diff(poly_q, x, j).subs(x, 0)
        / sp.factorial(degree)
        for j in range(degree + 1)
    ]
    apolar = sum(
        (-1) ** k * sp.binomial(degree, k) * a_coeff[k] * b_coeff[degree - k]
        for k in range(degree + 1)
    )
    walsh_numerator_at_z = sum(
        sp.diff(poly_p, x, k).subs(x, z) * sp.diff(poly_q, x, degree - k).subs(x, 0)
        for k in range(degree + 1)
    )
    require(
        sp.expand(
            apolar
            - (-1) ** degree * walsh_numerator_at_z / sp.factorial(degree)
        )
        == 0,
        f"degree {degree}: apolar-pairing certificate failed",
    )

    if degree >= 1:
        broken = sum(
            sp.diff(poly_p, x, k) * sp.diff(poly_q, x, degree - k)
            for k in range(degree)
        )
        require(
            sp.expand(direct - broken) != 0,
            f"degree {degree}: destructive control did not detect a deleted endpoint",
        )


def main() -> None:
    for degree in range(1, 9):
        verify_degree(degree)
    print(
        "PASS: derivative/Walsh identity for generic degrees 1..8, "
        "telescoping and apolar certificates, destructive control"
    )


if __name__ == "__main__":
    main()
