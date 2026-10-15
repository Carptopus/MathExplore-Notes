"""Guard the p>2 weighted-chain global maximum formulas in MATH-DIR-0114/S5."""

from __future__ import annotations

import math

import sympy as sp


def symbolic_checks() -> None:
    p, t = sp.symbols("p t", positive=True)
    a = 2 * p / (p + 1)
    b = (p + 1) / 2
    numerator = (1 + t) ** p + 1 + t**p
    ratio_power = numerator / (2 * (1 + t**a) ** b)
    logarithmic_derivative = sp.diff(sp.log(ratio_power), t) * t / p
    A = t * (1 + t) ** (p - 1) + t**p
    expected = A / numerator - t**a / (1 + t**a)
    if sp.simplify(logarithmic_derivative - expected) != 0:
        raise AssertionError("logarithmic derivative identity failed")

    if sp.simplify(a * b - p) != 0:
        raise AssertionError("ab=p failed")
    if sp.simplify((p - a) - p * (a - 1)) != 0:
        raise AssertionError("exponent conversion failed")

    r, z = sp.symbols("r z", positive=True)
    G = z ** (-1 / r) + z ** (1 + 1 / r) - z + 1 - (r + 1) ** (1 / r)
    if sp.simplify(sp.diff(G, z).subs(z, 1)) != 0:
        raise AssertionError("G'(1)=0 failed")
    expected_second = (1 / r) * (1 + 1 / r) * (
        z ** (-1 / r - 2) + z ** (1 / r - 1)
    )
    if sp.simplify(sp.diff(G, z, 2) - expected_second) != 0:
        raise AssertionError("G'' formula failed")


def logcosh(x: float) -> float:
    x = abs(x)
    return x + math.log1p(math.exp(-2 * x)) - math.log(2)


def normalized_log_ratio(p: float, s: float) -> float:
    """Return log(R_p(exp(s))^p / R_p(1)^p) stably."""
    x = abs(s)
    first = p * math.log(2) + p * logcosh(x / 2)
    second = math.log(2) + logcosh(p * x / 2)
    scale = max(first, second)
    log_numerator = scale + math.log(
        math.exp(first - scale) + math.exp(second - scale)
    )
    log_denominator = (p + 3) * math.log(2) / 2 + (
        (p + 1) / 2
    ) * logcosh(p * x / (p + 1))
    center = math.log(2**p + 2) - (p + 3) * math.log(2) / 2
    return log_numerator - log_denominator - center


def numerical_controls() -> None:
    for p in (2.001, 2.01, 2.1, 2.5, 3.0, 4.0, 8.0, 20.0, 100.0):
        previous = 0.0
        for s in (1e-4, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 12.0):
            value = normalized_log_ratio(p, s)
            if not value < 0:
                raise AssertionError((p, s, value))
            # Symmetry is built into the stable cosh representation; compare
            # against a direct evaluation where overflow is not a concern.
            if p * s < 500:
                t = math.exp(s)
                direct = ((1 + t) ** p + 1 + t**p) / (
                    2 * (1 + t ** (2 * p / (p + 1))) ** ((p + 1) / 2)
                )
                center = (2**p + 2) / 2 ** ((p + 3) / 2)
                if abs(math.log(direct / center) - value) > 2e-10:
                    raise AssertionError("stable/direct mismatch")
            if s <= 0.1 and value >= previous:
                raise AssertionError("local strict descent control failed")
            previous = value


if __name__ == "__main__":
    symbolic_checks()
    numerical_controls()
    print("VERIFIED: superquadratic weighted-chain global-maximum formulas")
