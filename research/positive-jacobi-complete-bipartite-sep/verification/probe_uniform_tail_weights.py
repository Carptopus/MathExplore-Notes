"""Exact Euclidean recovery for the seven frozen regression pairs only."""

from __future__ import annotations

from functools import cache

import sympy as sp


ALLOWED_PAIRS = ((3, 3), (3, 11), (4, 4), (4, 8), (5, 6), (6, 10), (8, 8))

y = sp.symbols("y")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


@cache
def cross_polynomial(dimension: int) -> sp.Poly:
    require(type(dimension) is int and 0 <= dimension <= 15, "Unsupported regression degree")
    if dimension == 0:
        return sp.Poly(1, y, domain=sp.QQ)
    if dimension == 1:
        return sp.Poly(y, y, domain=sp.QQ)
    previous = cross_polynomial(0)
    current = cross_polynomial(1)
    for degree in range(2, dimension + 1):
        previous, current = current, sp.Poly(
            y * current.as_expr()
            - sp.Rational((degree - 1) ** 2, 4) * previous.as_expr(),
            y,
            domain=sp.QQ,
        )
    return current


def centered_ehrhart(m: int, n: int) -> sp.Poly:
    require(type(m) is int and type(n) is int and (m, n) in ALLOWED_PAIRS, "Only frozen regression pairs are supported")
    dimension = m + n - 1
    cross_degree = m - 1
    gamma = [
        sp.binomial(2 * j, j)
        * sp.binomial(m - 1, j)
        * sp.binomial(n - 1, j)
        for j in range(cross_degree + 1)
    ]
    cross = [
        sum(
            sp.binomial(j, i) * gamma[j] / sp.Integer(4) ** j
            for j in range(i, cross_degree + 1)
        )
        for i in range(cross_degree + 1)
    ]
    expression = 0
    for i in range(cross_degree + 1):
        coefficient = (
            cross[i]
            * sp.factorial(dimension)
            / (
                cross[0]
                * sp.factorial(dimension - 2 * i)
                * sp.Integer(4) ** i
            )
        )
        expression += coefficient * cross_polynomial(dimension - 2 * i).as_expr()
    return sp.Poly(expression, y, domain=sp.QQ)


def recover_tail_weights(m: int, n: int) -> list[sp.Rational]:
    """Recover the unique zero-diagonal path tail extending P_n to Q_{m,n}."""
    require(type(m) is int and type(n) is int and (m, n) in ALLOWED_PAIRS, "Only frozen regression pairs are supported")
    target = centered_ehrhart(m, n)
    prefix = cross_polynomial(n)
    prefix_minor = cross_polynomial(n - 1)

    boundary = sp.rem(target * sp.invert(prefix_minor, prefix), prefix)
    first_weight = -boundary.LC()
    trailing_minor = sp.Poly(
        (-boundary / first_weight).as_expr(), y, domain=sp.QQ
    ).monic()
    trailing = sp.exquo(
        target + first_weight * prefix_minor * trailing_minor, prefix
    ).monic()

    weights = [first_weight]
    current, previous = trailing, trailing_minor
    for _ in range(1, m - 1):
        require(
            current.degree() == previous.degree() + 1,
            f"Euclid degree descent failed for (m,n)=({m},{n})",
        )
        remainder = sp.Poly(
            current.as_expr() - y * previous.as_expr(), y, domain=sp.QQ
        )
        weight = -remainder.LC()
        next_minor = sp.Poly(
            (-remainder / weight).as_expr(), y, domain=sp.QQ
        ).monic()
        weights.append(weight)
        current, previous = previous, next_minor
    require(
        current == sp.Poly(y, y, domain=sp.QQ)
        and previous == sp.Poly(1, y, domain=sp.QQ),
        f"terminal Euclid pair is not (y,1) for (m,n)=({m},{n})",
    )
    return weights
