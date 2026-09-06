"""Exact symbolic check for the K_{5,n} positive Jacobi realization."""

from __future__ import annotations

import sympy as sp


n = sp.symbols("n", integer=True, positive=True)
m = 5
d = n + m - 1


def polynomial_binomial_n_minus_one(j: int) -> sp.Expr:
    """Return binomial(n - 1, j) as a polynomial in n."""
    return sp.prod(n - 1 - k for k in range(j)) / sp.factorial(j)


def target_cross_coefficients() -> list[sp.Expr]:
    gamma = [
        sp.binomial(2 * j, j)
        * sp.binomial(m - 1, j)
        * polynomial_binomial_n_minus_one(j)
        for j in range(m)
    ]
    cross = [
        sp.factor(
            sum(
                sp.binomial(j, i) * gamma[j] / sp.Integer(4) ** j
                for j in range(i, m)
            )
        )
        for i in range(m)
    ]
    coefficients = []
    for i in range(m):
        falling = sp.prod(d - k for k in range(2 * i))
        coefficients.append(
            sp.factor(cross[i] * falling / (cross[0] * sp.Integer(4) ** i))
        )
    return coefficients


p4 = 10 * n**4 + 127 * n**3 + 527 * n**2 + 875 * n + 420
q4 = 35 * n**4 + 290 * n**3 + 841 * n**2 + 1066 * n + 840
r7 = (
    1070 * n**7
    + 24299 * n**6
    + 224862 * n**5
    + 1117182 * n**4
    + 3217969 * n**3
    + 5307310 * n**2
    + 4518240 * n
    + 1461600
)
s10 = (
    18000 * n**10
    + 596320 * n**9
    + 8583924 * n**8
    + 70987556 * n**7
    + 373829392 * n**6
    + 1306384332 * n**5
    + 3048698627 * n**4
    + 4643902725 * n**3
    + 4356607140 * n**2
    + 2235394800 * n
    + 472651200
)

tail_weights = [
    2 * n * p4 / q4,
    3 * (n + 1) * r7 / (4 * p4 * q4),
    (n + 2) * s10 / (p4 * r7),
    (n + 3) * (457 * n**2 + 2378 * n + 2632) * p4 / (4 * r7),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(
    lhs: dict[int, sp.Expr], rhs: dict[int, sp.Expr], scale: sp.Expr = sp.Integer(1)
) -> dict[int, sp.Expr]:
    out = dict(lhs)
    for shift, value in rhs.items():
        out[shift] = sp.factor(out.get(shift, 0) + scale * value)
    return {shift: value for shift, value in out.items() if value != 0}


def multiply_y(poly: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    """Use y P_{n+s}=P_{n+s+1}+((n+s)^2/4)P_{n+s-1}."""
    out: dict[int, sp.Expr] = {}
    for shift, value in poly.items():
        out[shift + 1] = out.get(shift + 1, 0) + value
        out[shift - 1] = out.get(shift - 1, 0) + value * (n + shift) ** 2 / 4
    return {shift: sp.factor(value) for shift, value in out.items()}


def append_edge(
    current: dict[int, sp.Expr],
    previous: dict[int, sp.Expr],
    weight_square: sp.Expr,
) -> dict[int, sp.Expr]:
    return add(multiply_y(current), previous, -weight_square)


def require_positive_coefficient_polynomial(expr: sp.Expr) -> None:
    coeffs = sp.Poly(sp.expand(expr), n).all_coeffs()
    require(
        bool(coeffs) and all(coefficient >= 0 for coefficient in coeffs),
        f"negative coefficient in {expr}",
    )
    require(any(coefficient > 0 for coefficient in coeffs), f"zero polynomial: {expr}")


def main() -> None:
    target = target_cross_coefficients()

    previous = {-1: sp.Integer(1)}  # P_{n-1}
    current = {0: sp.Integer(1)}  # P_n
    for weight in tail_weights:
        previous, current = current, append_edge(current, previous, weight)

    expected = {m - 1 - 2 * i: target[i] for i in range(m)}
    require(set(current) == set(expected), "cross-basis support mismatch")
    for shift in expected:
        require(
            sp.factor(current[shift] - expected[shift]) == 0,
            f"cross-basis coefficient mismatch at shift {shift}",
        )

    for polynomial in (p4, q4, r7, s10, 457 * n**2 + 2378 * n + 2632):
        require_positive_coefficient_polynomial(polynomial)
    for weight in tail_weights:
        numerator, denominator = sp.together(weight).as_numer_denom()
        require_positive_coefficient_polynomial(numerator)
        require_positive_coefficient_polynomial(denominator)

    print("PASS: symbolic K_{5,n} Jacobi identity and positive tail weights")


if __name__ == "__main__":
    main()
