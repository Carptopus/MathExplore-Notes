"""Guard the analytic weighted-chain phase transition in MATH-DIR-0114/S4."""

from __future__ import annotations

import math

import sympy as sp


def symbolic_checks() -> None:
    p, t, x, y = sp.symbols("p t x y", positive=True)
    q = t ** (2 * p / (p + 1))
    h = (p - 1) / (2 * p)
    x_star = (1 + q) ** (-h)
    y_star = t ** (2 / (p + 1)) * (1 + q) ** h
    a = x + t**2 / y
    objective = a**p + y**p + x ** (-p)
    a_star = a.subs({x: x_star, y: y_star})
    # SymPy does not reliably combine symbolic positive real powers after the
    # direct derivative substitution.  Check the equivalent algebraic
    # identities from which both Euler equations follow.
    euler_identities = (
        x_star * y_star - t ** (2 / (p + 1)),
        a_star / x_star - (1 + q),
        x_star ** (2 * p) * (1 + q) ** (p - 1) - 1,
        y_star ** (p + 1) / (t**2 * x_star ** (-p - 1)) - 1,
    )
    if any(
        sp.simplify(sp.powsimp(identity, force=True)) != 0
        for identity in euler_identities
    ):
        raise AssertionError("Euler identities failed")
    expected = 2 * (1 + q) ** ((p + 1) / 2)
    objective_identities = (
        x_star**p * (1 + q) ** p / (1 + q) ** ((p + 1) / 2) - 1,
        y_star**p / (q * (1 + q) ** ((p - 1) / 2)) - 1,
        x_star ** (-p) / (1 + q) ** ((p - 1) / 2) - 1,
    )
    if any(
        sp.simplify(sp.powsimp(identity, force=True)) != 0
        for identity in objective_identities
    ):
        raise AssertionError("minimum formula failed")

    s = sp.symbols("s", real=True)
    et = sp.exp(s)
    numerator = (1 + et) ** p + 1 + et**p
    denominator = 2 * (1 + et ** (2 * p / (p + 1))) ** ((p + 1) / 2)
    f = sp.log(numerator / denominator)
    if sp.simplify(sp.diff(f, s).subs(s, 0)) != 0:
        raise AssertionError("even first derivative failed")
    second = sp.factor(sp.diff(f, s, 2).subs(s, 0))
    expected_second = p * (2 * p - 2**p) * (p - 1) / (
        4 * (2**p + 2) * (p + 1)
    )
    if sp.simplify(second - expected_second) != 0:
        raise AssertionError((second, expected_second))


def ratio_power(p: float, t: float) -> float:
    return ((1 + t) ** p + 1 + t**p) / (
        2 * (1 + t ** (2 * p / (p + 1))) ** ((p + 1) / 2)
    )


def trace_gap(p: float, t: float) -> float:
    q = t ** (2 * p / (p + 1))
    h = (p - 1) / (2 * p)
    x = (1 + q) ** (-h)
    y = t ** (2 / (p + 1)) * (1 + q) ** h
    return x + y - 1 / x - t * t / y


def numerical_controls() -> None:
    for p in (1.05, 1.2, 1.5, 1.8, 1.95):
        center = ratio_power(p, 1.0)
        nearby = ratio_power(p, math.exp(-0.08))
        if nearby <= center:
            raise AssertionError((p, nearby, center))
        delta = abs(trace_gap(p, math.exp(-0.08)))
        advantage = nearby - center
        # The slack cost tends to zero; verify strict decay over six decades.
        costs = [(delta / 2) ** p * d ** (1 - p) for d in (10, 10_000_000)]
        if not (costs[1] < costs[0] and advantage > 0):
            raise AssertionError("slack decay control failed")

    for p in (2.2, 3.0, 4.0, 8.0):
        center = ratio_power(p, 1.0)
        nearby = ratio_power(p, math.exp(-0.08))
        if nearby >= center:
            raise AssertionError((p, nearby, center))


if __name__ == "__main__":
    symbolic_checks()
    numerical_controls()
    print("VERIFIED: weighted-chain subquadratic dimension-amplification formulas")
