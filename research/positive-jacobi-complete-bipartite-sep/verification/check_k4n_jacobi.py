"""Exact checks for the K_{4,n} positive Jacobi realization."""

from __future__ import annotations

import sympy as sp


n = sp.symbols("n", integer=True, positive=True)
m = 4
d = n + m - 1


def beta(j: sp.Expr) -> sp.Expr:
    return j**2 / 4


def polynomial_binomial_n_minus_one(j: int) -> sp.Expr:
    """Return binomial(n - 1, j) as a polynomial in n."""
    return sp.prod(n - 1 - k for k in range(j)) / sp.factorial(j)


def target_cross_coefficients() -> list[sp.Expr]:
    gamma_coefficients = [
        sp.binomial(2 * j, j)
        * sp.binomial(m - 1, j)
        * polynomial_binomial_n_minus_one(j)
        for j in range(m)
    ]
    cross_coefficients = [
        sp.factor(
            sum(
                sp.binomial(j, i)
                * gamma_coefficients[j]
                / sp.Integer(4) ** j
                for j in range(i, m)
            )
        )
        for i in range(m)
    ]
    return [
        sp.factor(
            cross_coefficients[i]
            * sp.prod(d - k for k in range(2 * i))
            / (cross_coefficients[0] * sp.Integer(4) ** i)
        )
        for i in range(m)
    ]


D = 5 * n**2 + 9 * n + 10

alpha = 3 * n * (3 * n**2 + 15 * n + 10) / (4 * D)
beta_tail = (
    2
    * (n + 1)
    * (8 * n**3 + 81 * n**2 + 164 * n + 80)
    / ((3 * n**2 + 15 * n + 10) * D)
)
gamma = (n + 2) * (13 * n + 11) / (4 * (3 * n**2 + 15 * n + 10))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(lhs: dict[int, sp.Expr], rhs: dict[int, sp.Expr], scale=1):
    out = dict(lhs)
    for shift, value in rhs.items():
        out[shift] = sp.expand(out.get(shift, 0) + scale * value)
    return {shift: value for shift, value in out.items() if value != 0}


def multiply_y(poly: dict[int, sp.Expr]):
    """Map P_{n+s} to P_{n+s+1}+((n+s)^2/4)P_{n+s-1}."""
    out: dict[int, sp.Expr] = {}
    for shift, value in poly.items():
        out[shift + 1] = out.get(shift + 1, 0) + value
        out[shift - 1] = out.get(shift - 1, 0) + value * beta(n + shift)
    return {shift: sp.expand(value) for shift, value in out.items()}


def append_edge(current, previous, weight_square):
    return add(multiply_y(current), previous, -weight_square)


def main() -> None:
    target = target_cross_coefficients()
    previous = {-1: sp.Integer(1)}  # P_{n-1}
    current = {0: sp.Integer(1)}  # P_n
    for weight in (alpha, beta_tail, gamma):
        previous, current = current, append_edge(current, previous, weight)

    expected = {m - 1 - 2 * i: target[i] for i in range(m)}
    require(set(current) == set(expected), "cross-basis support mismatch")
    for shift in expected:
        require(
            sp.factor(current[shift] - expected[shift]) == 0,
            f"cross-basis coefficient mismatch at shift {shift}",
        )

    # Positivity is coefficientwise transparent in the displayed factorizations.
    for expr in (alpha, beta_tail, gamma):
        numerator, denominator = sp.together(expr).as_numer_denom()
        numerator_coeffs = sp.Poly(numerator, n).all_coeffs()
        denominator_coeffs = sp.Poly(denominator, n).all_coeffs()
        require(
            all(c >= 0 for c in numerator_coeffs),
            f"negative numerator coefficient in {expr}",
        )
        require(
            any(c > 0 for c in numerator_coeffs),
            f"zero numerator in {expr}",
        )
        require(
            all(c >= 0 for c in denominator_coeffs),
            f"negative denominator coefficient in {expr}",
        )
        require(denominator.subs(n, 1) > 0, f"nonpositive denominator in {expr}")

    print("PASS: symbolic K_{4,n} Jacobi identity and positive tail weights")


if __name__ == "__main__":
    main()
