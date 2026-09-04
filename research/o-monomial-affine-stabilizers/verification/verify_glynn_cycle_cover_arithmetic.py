"""Exact arithmetic checks for the Glynn-I cycle-cover proof.

The general proof appears in the manuscript.  This script checks its parameter
identities, minimal zero-weight lengths, Kummer valuations, coefficient-gap claims,
and finite value-set polynomials for the first four admissible degrees.
"""

from __future__ import annotations

import math

from finite_field import BinaryField
from verify_bar_segre_value_polynomial import root_polynomial


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def predicted_first_index(degree: int) -> int:
    if degree % 4 == 1:
        return 1 << ((degree - 3) // 2)
    return 3 * (1 << ((degree - 3) // 2)) - 1


def valuation_two(value: int) -> int:
    require(value > 0, "2-adic valuation requires a positive integer")
    return (value & -value).bit_length() - 1


def first_zero_weight(degree: int) -> tuple[int, int]:
    h = (degree - 1) // 2
    a = 1 << h
    modulus = 2 * a * a - 1
    difference = 3 * (2 * a + 1)
    inverse = pow(difference, -1, modulus)
    for length in range(1, 4 * a):
        high_steps = (-length * inverse) % modulus
        if high_steps <= length:
            return length, high_steps
    raise AssertionError("search bound missed the first zero weight")


def expected_pair(degree: int) -> tuple[int, int]:
    h = (degree - 1) // 2
    a = 1 << h
    if h % 2 == 0:
        return a, (a - 1) // 3
    return 3 * a - 2, (7 * a - 5) // 3


def check_symbolic_arithmetic() -> None:
    for degree in range(5, 40, 2):
        h = (degree - 1) // 2
        a = 1 << h
        modulus = 2 * a * a - 1
        length, high_steps = expected_pair(degree)
        require(
            first_zero_weight(degree) == (length, high_steps),
            f"m={degree}: first zero-weight pair disagrees with the formula",
        )
        require(
            math.gcd(length, modulus) == 1,
            f"m={degree}: cycle length is not coprime to q-1",
        )
        choose = math.comb(length, high_steps)
        require(choose % length == 0, f"m={degree}: cycle count is not integral")
        require(
            valuation_two(choose) == valuation_two(length),
            f"m={degree}: Kummer valuation mismatch",
        )
        require(
            (modulus * (choose // length)) % 2 == 1,
            f"m={degree}: cycle-cover parity is even",
        )

        first = length // 2
        require(
            first == predicted_first_index(degree),
            f"m={degree}: first coefficient index mismatch",
        )
        require(
            math.gcd(first, modulus) == 1,
            f"m={degree}: first coefficient index is not coprime to q-1",
        )

        if degree % 4 == 1:
            exponent = 6 * a + 4
            difference = exponent - 1
            inverse = pow(difference, -1, modulus)
            for index in range(first + 1, 2 * first):
                symmetric_degree = 2 * index
                high_steps = (-symmetric_degree * inverse) % modulus
                require(
                    high_steps > symmetric_degree,
                    f"m={degree}, i={index}: forbidden coefficient gap failed",
                )
            require(
                math.comb(a * a - first, first) % 2 == 1,
                f"m={degree}: Lucas parity check failed",
            )


def check_finite_polynomials() -> None:
    for degree in (5, 7, 9, 11):
        field = BinaryField(degree)
        q = field.order
        exponent = 3 * (1 << ((degree + 1) // 2)) + 4
        image = {field.power(x, exponent) ^ x for x in range(q)}
        polynomial = root_polynomial(image, field)
        k = q // 2
        first = predicted_first_index(degree)
        require(
            all(polynomial[k - index] == 0 for index in range(1, first)),
            f"m={degree}: an earlier coefficient is nonzero",
        )
        require(
            polynomial[k - first] == 1,
            f"m={degree}: first predicted coefficient is not one",
        )
        if degree % 4 == 1:
            require(
                all(
                    polynomial[k - index] == 0
                    for index in range(first + 1, 2 * first)
                ),
                f"m={degree}: predicted coefficient gap failed",
            )


def check_negative_control() -> None:
    """Reject a deliberately shifted first-coefficient prediction at m=5."""
    degree = 5
    field = BinaryField(degree)
    q = field.order
    exponent = 3 * (1 << ((degree + 1) // 2)) + 4
    image = {field.power(x, exponent) ^ x for x in range(q)}
    polynomial = root_polynomial(image, field)
    k = q // 2
    first = predicted_first_index(degree)
    wrong_first = first - 1
    require(wrong_first > 0, "negative-control index is not positive")
    require(
        polynomial[k - wrong_first] != 1,
        "negative control accepted a deliberately shifted first index",
    )


def main() -> None:
    check_symbolic_arithmetic()
    check_finite_polynomials()
    check_negative_control()
    print("NEGATIVE_CONTROL_PASS: shifted first-index prediction was rejected")
    print("PASS: Glynn-I zero weights, cycle parity, gaps, and finite coefficients agree")


if __name__ == "__main__":
    main()
