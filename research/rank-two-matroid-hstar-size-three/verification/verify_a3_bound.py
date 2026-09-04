"""Exact checks for the a=3 rank-two matroid h*-real-rootedness proof."""

from __future__ import annotations

import math

import sympy as sp


u, n, v, x = sp.symbols("u n v x")


def require(condition: bool, message: str) -> None:
    """Fail explicitly even when Python is run with optimization enabled."""
    if not condition:
        raise RuntimeError(message)


def p_star_coefficients(a: int, ground_size: int) -> list[int]:
    result = [0] * (a + 1)
    for k in range(1, a + 1):
        for j in range(1, k + 1):
            if ground_size - k - 1 >= j - 1:
                result[j] += math.comb(k, j) * math.comb(
                    ground_size - k - 1, j - 1
                )
    return result


def partitions(total: int, largest: int | None = None):
    largest = min(total, total if largest is None else largest)
    if total == 0:
        yield ()
        return
    for first in range(largest, 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def connected_h_star(parts: tuple[int, ...]) -> sp.Poly:
    ground_size = sum(parts)
    coeffs = [math.comb(ground_size, 2 * j) for j in range(ground_size // 2 + 1)]
    for a in parts:
        correction = p_star_coefficients(a, ground_size)
        for j in range(1, len(correction)):
            if j < len(coeffs):
                coeffs[j] -= correction[j]
            else:
                require(correction[j] == 0, "correction exceeds the main degree")
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return sp.Poly(sum(c * x**j for j, c in enumerate(coeffs)), x)


def negative_root_multiplicity(polynomial: sp.Poly) -> int:
    """Count negative real roots with multiplicity via square-free factors."""
    return sum(
        exponent * factor.count_roots(-sp.oo, 0)
        for factor, exponent in polynomial.factor_list()[1]
    )


def verify_symbolic_certificate() -> None:
    p3 = sum(
        sp.binomial(k, j) * sp.binomial(n - k - 1, j - 1) * x**j
        for k in range(1, 4)
        for j in range(1, k + 1)
    )
    expected = 6 * x + (4 * n - 15) * x**2 + (n - 4) * (n - 5) * x**3 / 2
    require(sp.simplify(p3 - expected) == 0, "p*_{3,n} formula mismatch")

    taylor_five = sum(
        sp.prod(n / 2 - index for index in range(order))
        / sp.factorial(order)
        * (u / n) ** order
        for order in range(6)
    )
    p_scaled = (
        -6 * u
        + (4 - 15 / n) * u**2
        - sp.Rational(1, 2) * (1 - 9 / n + 20 / n**2) * u**3
    )
    a_coefficient = (29 * n - 114) / (8 * n)
    b_coefficient = 3 * (n - 4) * (3 * n - 14) / (16 * n**2)
    e_coefficient = (n - 6) * (n - 4) * (n - 2) / (128 * n**3)
    f_coefficient = (
        (n - 8) * (n - 6) * (n - 4) * (n - 2) / (1280 * n**4)
    )
    expected_upper = (
        3
        + sp.Rational(15, 2) * u
        - a_coefficient * u**2
        + b_coefficient * u**3
        + e_coefficient * u**4
        + f_coefficient * u**5
    )
    require(
        sp.simplify(3 * taylor_five - p_scaled - expected_upper) == 0,
        "upper Taylor certificate mismatch",
    )

    positivity = 239 * n**2 - 2748 * n + 7164
    require(
        sp.expand(positivity.subs(n, v + 9))
        == 239 * v**2 + 1554 * v + 1791,
        "shifted AM-GM positivity polynomial mismatch",
    )

    q_poly = (
        8703 * n**6
        - 265850 * n**5
        + 3132496 * n**4
        - 17387312 * n**3
        + 41723824 * n**2
        - 12090272 * n
        - 72328064
    )
    shifted = sp.Poly(sp.expand(q_poly.subs(n, v + 9)), v)
    require(
        all(coefficient > 0 for coefficient in shifted.all_coeffs()),
        "the shifted discriminant polynomial is not coefficient-positive",
    )

    c_coefficient = 7 * (5 * n - 18) / (8 * n)
    d_coefficient = (n - 4) * (7 * n - 38) / (16 * n**2)
    r_polynomial = (
        c_coefficient
        - d_coefficient * u
        + e_coefficient * u**2
        + f_coefficient * u**3
    )
    expected_lower = 3 - sp.Rational(9, 2) * u + u**2 * r_polynomial
    require(
        sp.simplify(3 * taylor_five + p_scaled - expected_lower) == 0,
        "lower Taylor certificate mismatch",
    )
    require(
        sp.simplify(c_coefficient - sp.Rational(21, 8) - 7 * (n - 9) / (4 * n))
        == 0,
        "C_n lower-bound certificate mismatch",
    )
    require(
        sp.simplify(
            sp.Rational(7, 16)
            - d_coefficient
            - (66 * n - 152) / (16 * n**2)
        )
        == 0,
        "D_n upper-bound certificate mismatch",
    )

    discriminant = sp.factor(sp.discriminant(r_polynomial - 1, u))
    expected_discriminant = -(
        (n - 6) * (n - 4) ** 2 * (n - 2) * q_poly
    ) / (104857600 * n**10)
    require(
        sp.simplify(discriminant - expected_discriminant) == 0,
        "discriminant certificate mismatch",
    )

    interval_minorant = (
        3
        - sp.Rational(9, 2) * u
        + sp.Rational(21, 8) * u**2
        - sp.Rational(7, 16) * u**3
    )
    stationary_minus = 2 - 2 * sp.sqrt(7) / 7
    stationary_plus = 2 + 2 * sp.sqrt(7) / 7
    require(
        sp.simplify(sp.diff(interval_minorant, u).subs(u, stationary_minus)) == 0
        and sp.simplify(sp.diff(interval_minorant, u).subs(u, stationary_plus))
        == 0,
        "interval minorant stationary points mismatch",
    )
    require(
        sp.simplify(
            interval_minorant.subs(u, stationary_minus)
            - (1 - sp.sqrt(7) / 7)
        )
        == 0
        and sp.simplify(
            interval_minorant.subs(u, stationary_plus)
            - (1 + sp.sqrt(7) / 7)
        )
        == 0,
        "interval minorant stationary values mismatch",
    )
    require(
        interval_minorant.subs(u, sp.Rational(37, 10))
        == sp.Rational(2009, 16000),
        "interval minorant endpoint mismatch",
    )
    require(
        (
            3
            - sp.Rational(9, 2) * u
            + u**2
        ).subs(u, sp.Rational(37, 10))
        == sp.Rational(1, 25),
        "large-u quadratic endpoint mismatch",
    )


def verify_nine_sturm_certificate() -> None:
    numerator = sp.Poly(
        u**9
        + 81 * u**8
        + 2916 * u**7
        - 594864 * u**6
        + 25627266 * u**5
        - 290698227 * u**4
        + 1249949232 * u**3
        - 1377495072 * u**2
        + 387420489 * u
        + 387420489,
        u,
    )
    p9 = -6 * u + (4 - sp.Rational(15, 9)) * u**2 - sp.Rational(1, 2) * (
        1 - sp.Rational(9, 9) + sp.Rational(20, 81)
    ) * u**3
    reconstructed = sp.Poly(
        sp.expand(43046721 * (9 * (1 + u / 9) ** 9 - p9**2)), u
    )
    require(reconstructed == numerator, "n=9 difference polynomial mismatch")

    sturm_chain = sp.sturm(numerator.as_expr(), u)
    require(
        [sp.degree(poly, u) for poly in sturm_chain]
        == [9, 8, 6, 5, 4, 3, 2, 1, 0],
        "unexpected n=9 Sturm-chain degree profile",
    )

    def sign(value: sp.Expr) -> int:
        return 1 if value > 0 else -1 if value < 0 else 0

    signs_at_zero = [sign(sp.Poly(poly, u).eval(0)) for poly in sturm_chain]
    signs_at_infinity = [sign(sp.LC(sp.Poly(poly, u))) for poly in sturm_chain]
    require(
        signs_at_zero == [1, 1, 0, -1, -1, 1, -1, -1, -1],
        "unexpected Sturm signs at zero",
    )
    require(
        signs_at_infinity == [1, 1, 1, -1, -1, -1, 1, 1, -1],
        "unexpected Sturm signs at positive infinity",
    )
    require(
        sp.count_roots(numerator, 0, sp.oo) == 0,
        "n=9 certificate polynomial has a positive root",
    )
    require(numerator.eval(0) > 0, "n=9 certificate is not positive at zero")

    # Negative control: the same positive-root test must reject a polynomial
    # with a known root in the (0, +infinity).
    require(
        sp.count_roots(sp.Poly(u - 1, u), 0, sp.oo) == 1,
        "positive-root negative control did not trigger",
    )


def verify_small_connected_cases() -> int:
    checked = 0
    for ground_size in range(3, 9):
        for parts in partitions(ground_size, 3):
            if len(parts) < 3:
                continue
            polynomial = connected_h_star(parts)
            degree = polynomial.degree()
            if degree:
                require(
                    negative_root_multiplicity(polynomial) == degree,
                    f"Sturm count does not place every root in (-infinity, 0) for {parts}",
                )
                roots = polynomial.all_roots()
                require(len(roots) == degree, f"root count mismatch for {parts}")
                require(
                    all(root.is_real and root < 0 for root in roots),
                    f"nonnegative or nonreal root for {parts}",
                )
            checked += 1
    return checked


def verify_disconnected_cases() -> int:
    expected = {
        (1, 1): [1],
        (1, 2): [1],
        (1, 3): [1],
        (2, 2): [1, 1],
        (2, 3): [1, 2],
        (3, 3): [1, 4, 1],
    }
    for (a, b), target in expected.items():
        dimension = a + b - 2
        coeffs = []
        for k in range(dimension + 1):
            coeffs.append(
                sum(
                    (-1) ** j
                    * math.comb(dimension + 1, j)
                    * math.comb(k - j + a - 1, a - 1)
                    * math.comb(k - j + b - 1, b - 1)
                    for j in range(k + 1)
                )
            )
        while len(coeffs) > 1 and coeffs[-1] == 0:
            coeffs.pop()
        require(coeffs == target, f"disconnected h* mismatch for {(a, b)}")
        polynomial = sp.Poly(sum(c * x**j for j, c in enumerate(coeffs)), x)
        if polynomial.degree():
            require(
                negative_root_multiplicity(polynomial) == polynomial.degree(),
                f"disconnected Sturm count failed for {(a, b)}",
            )
            roots = polynomial.all_roots()
            require(
                len(roots) == polynomial.degree(),
                f"disconnected root count mismatch for {(a, b)}",
            )
            require(
                all(root.is_real and root < 0 for root in roots),
                f"disconnected nonnegative or nonreal root for {(a, b)}",
            )
    return len(expected)


if __name__ == "__main__":
    verify_symbolic_certificate()
    verify_nine_sturm_certificate()
    small_count = verify_small_connected_cases()
    disconnected_count = verify_disconnected_cases()
    require(small_count == 31, f"expected 31 small connected cases, got {small_count}")
    require(
        disconnected_count == 6,
        f"expected 6 disconnected cases, got {disconnected_count}",
    )
    print(
        "PASS: symbolic certificate, n=9 Sturm certificate, "
        f"{small_count} small connected partitions, and "
        f"{disconnected_count} disconnected cases"
    )
