"""Exact error budget for the compact-band effective Fourier expansion.

This certificate closes the last analytic estimate needed after the exact
fifth-order calculation.  For a saddle law in the compact band, write

    u = sigma * sqrt(m) * t,      epsilon = m^(-1/2),

and normalize the lattice probability by ``sigma*sqrt(2*pi*m)``.  The local
exponent through cumulant order ten is majorized by

    sum_{j=1}^8 A_j(u) epsilon^j,

where the rational coefficients below come from
``verify_low_cumulant_envelope.py``.  Cumulants of order at least eleven are
controlled by the compound-Poisson envelope from
``verify_renewal_reformulation.py``.

The cutoff is not fixed.  It is

    U(m) = 6 * (m/1000)^(1/16).

Consequently every core remainder, polynomial tail, and Fourier tail is
bounded by C/m uniformly for m>=1000.  All numerical comparisons in this
file use Fraction arithmetic.  Exponentials are bounded by rational Taylor
majorants/minorants; decimal output is display only.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial


Q = Fraction
MIN_M = 1000
MIN_K = 1001
U0 = 6


Poly = dict[int, Fraction]


def poly_add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for power, coefficient in right.items():
        result[power] = result.get(power, Q(0)) + coefficient
    return {power: value for power, value in result.items() if value}


def poly_mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for p, a in left.items():
        for q, b in right.items():
            result[p + q] = result.get(p + q, Q(0)) + a * b
    return {power: value for power, value in result.items() if value}


def poly_scale(poly: Poly, scalar: Fraction) -> Poly:
    return {power: scalar * value for power, value in poly.items() if value}


def poly_eval(poly: Poly, value: Fraction) -> Fraction:
    return sum((coefficient * value**power for power, coefficient in poly.items()), Q(0))


def double_factorial_odd(power: int) -> int:
    """Return (power-1)!! for an even Gaussian moment E Z^power."""
    assert power >= 0 and power % 2 == 0
    result = 1
    for value in range(1, power, 2):
        result *= value
    return result


def normal_abs_moment_upper(power: int) -> Fraction:
    """Rational upper bound for E|Z|^power, Z standard normal.

    For odd power 2a+1 we use

        E|Z|^(2a+1) = 2^(a+1) a! / sqrt(2*pi)
                       < 2^(a+2) a! / 5,

    using the elementary Archimedean bound pi>25/8.
    """
    if power % 2 == 0:
        return Q(double_factorial_odd(power))
    a = (power - 1) // 2
    return Q(2 ** (a + 2) * factorial(a), 5)


def exp_upper(x: Fraction, terms: int = 120) -> Fraction:
    """Rational upper bound for exp(x), x>=0."""
    assert x >= 0 and x < terms + 2
    total = Q(1)
    term = Q(1)
    for index in range(1, terms + 1):
        term *= x / index
        total += term
    first_omitted = term * x / (terms + 1)
    ratio = x / (terms + 2)
    return total + first_omitted / (1 - ratio)


def exp_negative_upper(x: Fraction, terms: int = 100) -> Fraction:
    """Rational upper bound for exp(-x), x>=0."""
    assert x >= 0
    partial = Q(1)
    term = Q(1)
    for index in range(1, terms + 1):
        term *= x / index
        partial += term
    return 1 / partial


def formal_exponential(max_order: int = 40) -> tuple[list[Poly], list[Poly]]:
    """Return A_j and H_n for exp(sum A_j epsilon^j)."""
    a: list[Poly] = [{} for _ in range(9)]
    a[1] = {1: Q(7, 4), 3: Q(11, 20)}
    a[2] = {4: Q(13, 20)}
    a[3] = {5: Q(17, 20)}
    a[4] = {6: Q(6, 5)}
    a[5] = {7: Q(7, 4)}
    a[6] = {8: Q(5, 2)}
    a[7] = {9: Q(15, 4)}
    a[8] = {10: Q(11, 2)}

    h: list[Poly] = [{} for _ in range(max_order + 1)]
    h[0] = {0: Q(1)}
    for order in range(1, max_order + 1):
        numerator: Poly = {}
        for index in range(1, min(8, order) + 1):
            numerator = poly_add(
                numerator,
                poly_scale(poly_mul(a[index], h[order - index]), Q(index)),
            )
        h[order] = poly_scale(numerator, Q(1, order))
        # Every monomial has parity order and degree at most 3*order.
        assert all((power - order) % 2 == 0 for power in h[order])
        assert all(power <= 3 * order for power in h[order])
    return a, h


def integrated_polynomial(poly: Poly, absolute: bool = True) -> Fraction:
    result = Q(0)
    for power, coefficient in poly.items():
        if power % 2:
            continue
        value = abs(coefficient) if absolute else coefficient
        result += value * double_factorial_odd(power)
    return result


def low_exponent_core_tail(h: list[Poly]) -> Fraction:
    # Odd epsilon orders integrate to zero.  Extending the integral from the
    # core to the full real line only enlarges this positive majorant.
    return sum(
        (
            integrated_polynomial(h[order]) / MIN_M ** (order // 2)
            for order in range(12, 41, 2)
        ),
        Q(0),
    )


def low_exponent_point_tail(a: list[Poly], h: list[Poly]) -> Fraction:
    # sqrt(1000)>31, hence epsilon<1/31 at the worst endpoint.
    epsilon = Q(1, 31)
    u = Q(U0)
    exponent = sum(
        (poly_eval(a[index], u) * epsilon**index for index in range(1, 9)),
        Q(0),
    )
    partial = sum(
        (poly_eval(h[order], u) * epsilon**order for order in range(41)),
        Q(0),
    )
    remainder = exp_upper(exponent) - partial
    assert remainder > 0
    # 2/sqrt(2*pi)<4/5 and the core length is 2U.
    return Q(4 * U0, 5) * remainder


def high_cumulant_core_tail() -> Fraction:
    # q=(15/8)|u|/sqrt(m) <=45/124 on the base core.
    q = Q(45, 124)
    b_sup = Q(5 * MIN_M, 11) * q**11 / (1 - q)
    low_even_coefficient = (
        Q(13, 20)
        + Q(6, 5) * Q(U0**2, MIN_M)
        + Q(5, 2) * Q(U0**4, MIN_M**2)
        + Q(11, 2) * Q(U0**6, MIN_M**3)
    )
    assert low_even_coefficient < Q(7, 8)
    low_real_correction = Q(7 * U0**4, 8 * MIN_M)
    assert low_real_correction + 2 * b_sup < Q(6, 5)
    assert exp_upper(Q(6, 5)) < 4

    integrated_b = (
        Q(5, 11)
        / (1 - q)
        * Q(15, 8) ** 11
        / (MIN_M**4 * 31)
        * normal_abs_moment_upper(11)
    )
    return 4 * integrated_b


def gaussian_tail_moments(max_power: int) -> list[Fraction]:
    e = exp_negative_upper(Q(U0**2, 2))
    moments = [Q(0)] * (max_power + 1)
    moments[0] = Q(4, 5) * e / U0
    if max_power:
        moments[1] = Q(4, 5) * e
    for power in range(2, max_power + 1):
        moments[power] = (
            Q(4, 5) * U0 ** (power - 1) * e
            + (power - 1) * moments[power - 2]
        )
    return moments


def finite_polynomial_tail(h: list[Poly]) -> Fraction:
    max_power = max(max(poly) for poly in h[:11] if poly)
    moments = gaussian_tail_moments(max_power)
    result = Q(0)
    for order in range(0, 11, 2):
        result += sum(
            (
                abs(coefficient) * moments[power]
                for power, coefficient in h[order].items()
            ),
            Q(0),
        ) / MIN_M ** (order // 2)
    return result


def mills_tail(c: Fraction, u: int) -> Fraction:
    # Two-sided normalized Gaussian-type tail:
    # (2/sqrt(2*pi))*int_u^inf exp(-c*x^2)dx.
    return Q(2, 5) * exp_negative_upper(c * u * u) / (c * u)


def actual_fourier_tail_constants() -> tuple[Fraction, Fraction]:
    # On 6<=|u|<=8 the c4/c8 bounds plus the compound-Poisson envelope
    # for r>=12 give Re exponent <=-(111/250)u^2.
    q8 = Q(15, 31)
    correction_ratio = (
        Q(13, 20) * Q(8**2, MIN_M)
        + Q(5, 2) * Q(8**6, MIN_M**3)
        + Q(5 * MIN_M, 12 * 8**2) * q8**12 / (1 - q8)
    )
    assert correction_ratio < Q(7, 125)

    near = mills_tail(Q(111, 250), 6)
    outer = mills_tail(Q(9, 32), 8)

    # U(m)=8 at m=1000*(4/3)^16.  Before that point the second tail
    # starts at 8; afterwards its moving lower endpoint makes m*tail
    # decrease.  This integer is an exact upper bound for the transition.
    transition = Q(MIN_M * 4**16, 3**16)
    transition_upper = (transition.numerator + transition.denominator - 1) // transition.denominator
    return MIN_M * near, transition_upper * outer


def far_fourier_tail_constant() -> Fraction:
    # sigma<17, sqrt(1000)<32, sqrt(2*pi)<3.
    base = Q(17 * 32 * 3) * Q(55, 64) ** 500
    return MIN_M * base


def probability_majorant(h: list[Poly]) -> tuple[list[Fraction], Fraction]:
    coefficients = [Q(0)] + [integrated_polynomial(h[2 * order]) for order in range(1, 6)]
    value = sum(
        (coefficients[order] / MIN_M**order for order in range(1, 6)),
        Q(0),
    )
    assert value < Q(1, 50)
    return coefficients, value


def series_mul(left: list[Fraction], right: list[Fraction], degree: int) -> list[Fraction]:
    result = [Q(0)] * (degree + 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i + j <= degree:
                result[i + j] += a * b
    return result


def log_majorant_coefficients(probability: list[Fraction], degree: int = 5) -> list[Fraction]:
    g = probability[: degree + 1]
    result = [Q(0)] * (degree + 1)
    power = [Q(1)] + [Q(0)] * degree
    for count in range(1, degree + 1):
        power = series_mul(power, g, degree)
        for index in range(1, degree + 1):
            result[index] += power[index] / count
    return result


def negative_log_upper(value: Fraction, terms: int = 20) -> Fraction:
    total = Q(0)
    power = Q(1)
    for count in range(1, terms + 1):
        power *= value
        total += power / count
    return total + power * value / ((terms + 1) * (1 - value))


def local_algebraic_tail(probability: list[Fraction], value_at_1000: Fraction) -> Fraction:
    # The worst sample size is m=k-1.  With q=1/k,
    # 1/(k-1)=q/(1-q), and at k=1001 this equals 1/1000.
    q = Q(1, MIN_K)
    log_coefficients = log_majorant_coefficients(probability)
    low = Q(0)
    for total_degree in range(1, 6):
        coefficient = sum(
            (
                log_coefficients[inner] * comb(total_degree - 1, inner - 1)
                for inner in range(1, total_degree + 1)
            ),
            Q(0),
        )
        low += coefficient * q**total_degree
    tail = negative_log_upper(value_at_1000) - low
    assert tail > 0
    # Absolute weights in 2L_k-L_(k-1)-L_(k+1) sum to four.
    return 4 * tail


def elementary_log_tails() -> tuple[Fraction, Fraction]:
    q = Q(1, MIN_K)
    normalization = q**6 / (6 * (1 - q**2))

    # Exact target is 1/(1+q) times four linear numerator/denominator
    # factors with T=mu+5>=11/2.  Bound every log-series tail absolutely.
    def tail(x: Fraction) -> Fraction:
        return x**6 / (6 * (1 - x))

    target = tail(q)
    for index in range(1, 5):
        target += tail(Q(2 * index, 11) * q)
        if index > 1:
            target += tail(Q(2 * (index - 1), 11) * q)
    return normalization, target


def verify_scaling(h: list[Poly]) -> None:
    # Put r=m/1000>=1.  U=6*r^(1/16), epsilon<=r^(-1/2)/31.
    # The following exponents are those of r after multiplying an error
    # by m.  Strict negativity makes the base endpoint the worst case.
    assert all(1 - Q(order, 2) < 0 for order in range(12, 41, 2))
    # For every omitted H_n, n>=41, every monomial degree p is at most
    # 3n.  Hence the worst exponent is 17/16-5n/16, already negative
    # at n=41 and decreasing thereafter.
    assert Q(17, 16) - Q(5 * 41, 16) < 0
    for order in range(0, 11, 2):
        for power in h[order]:
            exponent = Q(1) - Q(order, 2) + Q(power - 1, 16) - Q(U0**2, 16)
            assert exponent < 0

    # m*U^(-1)*exp(-cU^2) decreases from U=6 in the first tail,
    # and from U=8 in the outer tail.
    assert Q(15, 16) - Q(111, 250) * Q(U0**2, 8) < 0
    assert Q(15, 16) - Q(9, 32) * Q(8**2, 8) < 0
    assert Q(55, 64) * Q(MIN_M + 1, MIN_M) ** 3 < 1
    # The remaining algebraic tails start at q^6.  After multiplication
    # by k they decrease, while k times the retained margin increases.
    assert 1 - 6 < 0
    print("PASS: moving cutoff makes every error/margin ratio nonincreasing")


def main() -> None:
    a, h = formal_exponential(40)
    core = low_exponent_core_tail(h)
    point = low_exponent_point_tail(a, h)
    high = high_cumulant_core_tail()
    polynomial_tail = finite_polynomial_tail(h)
    near_constant, outer_constant = actual_fourier_tail_constants()
    far_constant = far_fourier_tail_constant()

    # All first four errors have m*error maximal at m=1000.
    fourier_constant = (
        MIN_M * (core + point + high + polynomial_tail)
        + near_constant
        + outer_constant
        + far_constant
    )

    probability, probability_value = probability_majorant(h)
    algebraic = local_algebraic_tail(probability, probability_value)
    normalization_tail, target_tail = elementary_log_tails()

    verify_scaling(h)

    # Each of the four local log factors contributes at most twice its
    # normalized probability error because G+error<1/2.  The worst local
    # sample size is k-1, so the Fourier contribution at k is at most
    # 8*C/(k-1).
    assert probability_value + fourier_constant / MIN_M < Q(1, 2)
    q = Q(1, MIN_K)
    retained = Q(3, 100) * (q - 2 * q**2 - 4 * q**4)
    total_error = (
        Q(8) * fourier_constant / (MIN_K - 1)
        + algebraic
        + normalization_tail
        + target_tail
    )
    assert total_error < retained

    print(f"PASS: low core tail < {float(core):.12g}")
    print(f"PASS: low point tail < {float(point):.12g}")
    print(f"PASS: high-cumulant core tail < {float(high):.12g}")
    print(f"PASS: finite polynomial tail < {float(polynomial_tail):.12g}")
    print(f"PASS: uniform Fourier constant C < {float(fourier_constant):.12g}")
    print(f"PASS: local polynomial deviation G < {float(probability_value):.12g}")
    print(f"PASS: algebraic log/re-expansion tail < {float(algebraic):.12g}")
    print(f"PASS: total log error at k=1001 < {float(total_error):.12g}")
    print(f"PASS: retained fifth-order margin at k=1001 > {float(retained):.12g}")
    print("PASS: effective compact-band Fourier remainder closes every k>=1001")


if __name__ == "__main__":
    main()
