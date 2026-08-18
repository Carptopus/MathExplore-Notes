"""Symbolic checks for the parameter-independent identities in HSF-E0496."""

from __future__ import annotations

from dataclasses import dataclass


Poly = frozenset[tuple[int, int]]
Laurent = frozenset[int]


def binary_polynomial_multiply(left: int, right: int) -> int:
    result = 0
    factor = left
    multiplier = right
    while multiplier:
        if multiplier & 1:
            result ^= factor
        factor <<= 1
        multiplier >>= 1
    return result


def binary_polynomial_remainder(dividend: int, divisor: int) -> int:
    if divisor == 0:
        raise ZeroDivisionError
    result = dividend
    divisor_degree = divisor.bit_length() - 1
    while result and result.bit_length() - 1 >= divisor_degree:
        result ^= divisor << (result.bit_length() - 1 - divisor_degree)
    return result


def binary_polynomial_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, binary_polynomial_remainder(left, right)
    return left


def binary_polynomial_multiply_mod(left: int, right: int, modulus: int) -> int:
    return binary_polynomial_remainder(
        binary_polynomial_multiply(left, right),
        modulus,
    )


def binary_polynomial_power_mod(value: int, exponent: int, modulus: int) -> int:
    result = 1
    factor = binary_polynomial_remainder(value, modulus)
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = binary_polynomial_multiply_mod(result, factor, modulus)
        factor = binary_polynomial_multiply_mod(factor, factor, modulus)
        remaining >>= 1
    return result


def binary_polynomial_is_irreducible(value: int) -> bool:
    """Rabin's exact irreducibility test over F_2 for a monic polynomial."""

    degree = value.bit_length() - 1
    if degree <= 0 or not value & 1:
        return False
    prime_divisors = {
        divisor
        for divisor in range(2, degree + 1)
        if degree % divisor == 0
        and all(
            divisor % candidate
            for candidate in range(2, int(divisor**0.5) + 1)
        )
    }
    x_value = 0b10
    if binary_polynomial_power_mod(x_value, 1 << degree, value) != x_value:
        return False
    return all(
        binary_polynomial_gcd(
            value,
            binary_polynomial_power_mod(
                x_value,
                1 << (degree // prime),
                value,
            )
            ^ x_value,
        )
        == 1
        for prime in prime_divisors
    )


def poly_add(*values: Poly) -> Poly:
    result: set[tuple[int, int]] = set()
    for value in values:
        result.symmetric_difference_update(value)
    return frozenset(result)


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result: set[tuple[int, int]] = set()
    for left_x, left_c in left:
        for right_x, right_c in right:
            term = (left_x + right_x, left_c + right_c)
            if term in result:
                result.remove(term)
            else:
                result.add(term)
    return frozenset(result)


def poly_power(value: Poly, exponent: int) -> Poly:
    result: Poly = frozenset({(0, 0)})
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = poly_multiply(result, base)
        base = poly_multiply(base, base)
        remaining >>= 1
    return result


def poly_shift(value: Poly, x_power: int = 0, c_power: int = 0) -> Poly:
    return frozenset(
        (old_x + x_power, old_c + c_power) for old_x, old_c in value
    )


def laurent_add(*values: Laurent) -> Laurent:
    result: set[int] = set()
    for value in values:
        result.symmetric_difference_update(value)
    return frozenset(result)


def laurent_multiply(left: Laurent, right: Laurent) -> Laurent:
    result: set[int] = set()
    for left_power in left:
        for right_power in right:
            power = left_power + right_power
            if power in result:
                result.remove(power)
            else:
                result.add(power)
    return frozenset(result)


def laurent_shift(value: Laurent, power: int) -> Laurent:
    return frozenset(old_power + power for old_power in value)


@dataclass(frozen=True)
class QuadraticElement:
    """Element base+rho*coefficient with rho^2+rho=c^-2."""

    base: Laurent
    coefficient: Laurent

    def __add__(self, other: "QuadraticElement") -> "QuadraticElement":
        return QuadraticElement(
            laurent_add(self.base, other.base),
            laurent_add(self.coefficient, other.coefficient),
        )

    def __mul__(self, other: "QuadraticElement") -> "QuadraticElement":
        coefficient_product = laurent_multiply(
            self.coefficient,
            other.coefficient,
        )
        return QuadraticElement(
            laurent_add(
                laurent_multiply(self.base, other.base),
                laurent_shift(coefficient_product, -2),
            ),
            laurent_add(
                laurent_multiply(self.base, other.coefficient),
                laurent_multiply(self.coefficient, other.base),
                coefficient_product,
            ),
        )

    def __pow__(self, exponent: int) -> "QuadraticElement":
        result = QUAD_ONE
        base = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * base
            base = base * base
            remaining >>= 1
        return result


POLY_ONE: Poly = frozenset({(0, 0)})
POLY_X: Poly = frozenset({(1, 0)})
POLY_C: Poly = frozenset({(0, 1)})

LAURENT_ONE: Laurent = frozenset({0})
QUAD_ZERO = QuadraticElement(frozenset(), frozenset())
QUAD_ONE = QuadraticElement(LAURENT_ONE, frozenset())
RHO = QuadraticElement(frozenset(), LAURENT_ONE)


def coefficient(power: int) -> QuadraticElement:
    return QuadraticElement(frozenset({power}), frozenset())


def main() -> None:
    # If eta=c^2+c^5+c^(1/2) vanished and w=c^(-1/2), then
    # w^9+w^6+1=0.  These exact checks support the trace contradiction
    # written in the manuscript.
    eta_zero_polynomial = (1 << 9) | (1 << 6) | 1
    cubic_factor = (1 << 3) | (1 << 1) | 1
    sextic_factor = (1 << 6) | (1 << 4) | (1 << 2) | (1 << 1) | 1
    if binary_polynomial_multiply(cubic_factor, sextic_factor) != eta_zero_polynomial:
        raise AssertionError("eta-zero factorization failed")
    if not binary_polynomial_is_irreducible(cubic_factor):
        raise AssertionError("eta-zero cubic factor is not irreducible")
    if not binary_polynomial_is_irreducible(sextic_factor):
        raise AssertionError("eta-zero sextic factor is not irreducible")
    if sextic_factor & (1 << 5):
        raise AssertionError("eta-zero sextic trace coefficient is not zero")

    one = POLY_ONE
    x = POLY_X
    c = POLY_C
    c_squared = poly_power(c, 2)
    u = poly_add(one, c, c_squared)
    denominator = poly_add(poly_power(x, 2), poly_multiply(c, x), one)
    numerator_f = poly_multiply(
        c_squared,
        poly_add(
            poly_power(x, 4),
            x,
            poly_multiply(u, poly_add(poly_power(x, 3), poly_power(x, 2))),
        ),
    )
    numerator_g = poly_add(
        poly_multiply(poly_power(c, 4), poly_power(x, 4)),
        poly_multiply(
            poly_multiply(
                poly_power(c, 3),
                poly_add(one, poly_power(c, 2), poly_power(c, 4)),
            ),
            poly_power(x, 3),
        ),
        poly_multiply(
            poly_multiply(
                poly_power(c, 3),
                poly_add(one, poly_power(c, 2)),
            ),
            x,
        ),
    )
    p_value = poly_multiply(
        poly_multiply(c_squared, x),
        poly_add(x, c),
    )
    left = poly_add(
        poly_shift(numerator_g, c_power=-1),
        poly_multiply(u, numerator_f),
    )
    right = poly_add(poly_power(p_value, 2), poly_multiply(p_value, denominator))
    if left != right:
        raise AssertionError("Artin-Schreier rational numerator identity failed")

    # Partial-fraction coefficients for Q(z)/E(z)^2 in the proof of
    # sum B_c(F)=c(1+c+c^2).  Here rho^2+rho=c^-2.
    u_laurent = frozenset({0, 1, 2})
    rho_plus_one = RHO + QUAD_ONE

    def q_value(value: QuadraticElement) -> QuadraticElement:
        return (
            coefficient(2) * value**4
            + QuadraticElement(
                laurent_shift(u_laurent, 1),
                frozenset(),
            )
            * value**3
            + QuadraticElement(u_laurent, frozenset()) * value**2
            + coefficient(-1) * value
        )

    def q_derivative(value: QuadraticElement) -> QuadraticElement:
        return (
            QuadraticElement(laurent_shift(u_laurent, 1), frozenset())
            * value**2
            + coefficient(-1)
        )

    a_plus_c = q_derivative(RHO) + q_derivative(rho_plus_one)
    b_plus_d = q_value(RHO) + q_value(rho_plus_one)
    expected = QuadraticElement(frozenset({1, 2, 3}), frozenset())
    if a_plus_c != expected:
        raise AssertionError("first partial-fraction coefficient sum failed")
    if b_plus_d != expected:
        raise AssertionError("second partial-fraction coefficient sum failed")

    print("status=PASS_SYMBOLIC_IDENTITIES")
    print(
        "checked=subiaco_eta_nonzero_factorization,"
        "artin_schreier_numerator,hyperplane_partial_fractions"
    )


if __name__ == "__main__":
    main()
