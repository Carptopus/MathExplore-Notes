"""Exact resultant verification for the HSF-E0500 zero-anchor theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


Laurent = frozenset[int]
LaurentPolynomial = dict[int, Laurent]


def laurent_add(*values: Laurent) -> Laurent:
    result: set[int] = set()
    for value in values:
        result.symmetric_difference_update(value)
    return frozenset(result)


def laurent_multiply(left: Laurent, right: Laurent) -> Laurent:
    result: set[int] = set()
    for left_power in left:
        for right_power in right:
            exponent = left_power + right_power
            if exponent in result:
                result.remove(exponent)
            else:
                result.add(exponent)
    return frozenset(result)


def laurent_polynomial_add(
    *values: LaurentPolynomial,
) -> LaurentPolynomial:
    result: LaurentPolynomial = {}
    for value in values:
        for degree, coefficient in value.items():
            result[degree] = laurent_add(
                result.get(degree, frozenset()), coefficient
            )
    return {degree: coefficient for degree, coefficient in result.items() if coefficient}


def laurent_polynomial_multiply(
    left: LaurentPolynomial,
    right: LaurentPolynomial,
) -> LaurentPolynomial:
    result: LaurentPolynomial = {}
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            degree = left_degree + right_degree
            coefficient = laurent_multiply(left_coefficient, right_coefficient)
            result[degree] = laurent_add(
                result.get(degree, frozenset()), coefficient
            )
    return {degree: coefficient for degree, coefficient in result.items() if coefficient}


def laurent_polynomial_power(
    value: LaurentPolynomial,
    exponent: int,
) -> LaurentPolynomial:
    result: LaurentPolynomial = {0: frozenset({0})}
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = laurent_polynomial_multiply(result, base)
        base = laurent_polynomial_multiply(base, base)
        remaining >>= 1
    return result


def laurent_polynomial_scale(
    value: LaurentPolynomial,
    coefficient: Laurent,
    degree_shift: int = 0,
) -> LaurentPolynomial:
    return {
        degree + degree_shift: laurent_multiply(old_coefficient, coefficient)
        for degree, old_coefficient in value.items()
        if laurent_multiply(old_coefficient, coefficient)
    }


def laurent_polynomial_substitute_square(
    value: LaurentPolynomial,
) -> LaurentPolynomial:
    return {2 * degree: coefficient for degree, coefficient in value.items()}


def derive_zero_anchor_polynomial() -> list[int]:
    """Derive h^7 B_c(cw^2) E(w^2)^2 / w from the Subiaco formula."""

    one: Laurent = frozenset({0})
    h_squared: Laurent = frozenset({2})
    u_value: Laurent = frozenset({0, 2, 4})
    e_value: LaurentPolynomial = {
        2: one,
        1: one,
        0: frozenset({-4}),
    }
    q_value: LaurentPolynomial = {
        4: frozenset({4}),
        3: frozenset({2, 4, 6}),
        2: u_value,
        1: frozenset({-2}),
    }
    # R(z)=M(z)/E(z)^2 and B_c(cz)=R(z)+h sqrt(z).
    m_value = laurent_polynomial_add(
        q_value,
        laurent_polynomial_scale(
            laurent_polynomial_power(e_value, 2),
            laurent_multiply(u_value, h_squared),
            degree_shift=1,
        ),
    )
    e_w_squared = laurent_polynomial_substitute_square(e_value)
    zero_numerator = laurent_polynomial_add(
        laurent_polynomial_substitute_square(m_value),
        laurent_polynomial_scale(
            laurent_polynomial_power(e_w_squared, 2),
            frozenset({1}),
            degree_shift=1,
        ),
    )
    if 0 in zero_numerator:
        raise AssertionError("zero-anchor numerator is not divisible by w")

    derived: list[int] = [0] * 10
    for degree, coefficient in zero_numerator.items():
        scaled = frozenset(exponent + 7 for exponent in coefficient)
        if min(scaled, default=0) < 0:
            raise AssertionError("h^7 did not clear the Laurent denominator")
        derived[degree - 1] = from_exponents(set(scaled))
    return derived


def polynomial_multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def polynomial_divmod(dividend: int, divisor: int) -> tuple[int, int]:
    quotient = 0
    divisor_degree = divisor.bit_length() - 1
    while dividend and dividend.bit_length() - 1 >= divisor_degree:
        shift = dividend.bit_length() - 1 - divisor_degree
        quotient ^= 1 << shift
        dividend ^= divisor << shift
    return quotient, dividend


def polynomial_remainder(dividend: int, divisor: int) -> int:
    return polynomial_divmod(dividend, divisor)[1]


def polynomial_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, polynomial_remainder(left, right)
    return left


def polynomial_power(value: int, exponent: int) -> int:
    result = 1
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = polynomial_multiply(result, base)
        base = polynomial_multiply(base, base)
        remaining >>= 1
    return result


def polynomial_power_mod(value: int, exponent: int, modulus: int) -> int:
    result = 1
    base = polynomial_remainder(value, modulus)
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = polynomial_remainder(
                polynomial_multiply(result, base), modulus
            )
        base = polynomial_remainder(polynomial_multiply(base, base), modulus)
        remaining >>= 1
    return result


def exact_divide(dividend: int, divisor: int) -> int:
    quotient, remainder = polynomial_divmod(dividend, divisor)
    if remainder:
        raise AssertionError("non-exact polynomial division")
    return quotient


def prime_divisors(value: int) -> list[int]:
    result: list[int] = []
    candidate = 2
    remaining = value
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            result.append(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        result.append(remaining)
    return result


def is_irreducible(value: int) -> bool:
    degree = value.bit_length() - 1
    x_value = polynomial_remainder(0b10, value)
    if polynomial_power_mod(x_value, 1 << degree, value) != x_value:
        return False
    for prime in prime_divisors(degree):
        test = polynomial_power_mod(x_value, 1 << (degree // prime), value)
        if polynomial_gcd(value, test ^ x_value) != 1:
            return False
    return True


def bareiss_determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    values = [row[:] for row in matrix]
    previous = 1
    for pivot_index in range(size - 1):
        if values[pivot_index][pivot_index] == 0:
            swap = next(
                row
                for row in range(pivot_index + 1, size)
                if values[row][pivot_index]
            )
            values[pivot_index], values[swap] = (
                values[swap],
                values[pivot_index],
            )
        pivot = values[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = polynomial_multiply(values[row][column], pivot)
                numerator ^= polynomial_multiply(
                    values[row][pivot_index],
                    values[pivot_index][column],
                )
                values[row][column] = exact_divide(numerator, previous)
            values[row][pivot_index] = 0
        previous = pivot
    return values[-1][-1]


def resultant(left: list[int], right: list[int]) -> int:
    left_degree = len(left) - 1
    right_degree = len(right) - 1
    size = left_degree + right_degree
    matrix = [[0] * size for _ in range(size)]
    for row in range(right_degree):
        for column, coefficient in enumerate(left):
            matrix[row][row + column] = coefficient
    for row in range(left_degree):
        for column, coefficient in enumerate(right):
            matrix[right_degree + row][row + column] = coefficient
    return bareiss_determinant(matrix)


def from_exponents(exponents: set[int]) -> int:
    return sum(1 << exponent for exponent in exponents)


def trace_inverse_square(modulus: int) -> int:
    degree = modulus.bit_length() - 1
    inverse = polynomial_power_mod(0b10, (1 << degree) - 2, modulus)
    value = polynomial_remainder(polynomial_multiply(inverse, inverse), modulus)
    trace = 0
    conjugate = value
    for _ in range(degree):
        trace ^= conjugate
        conjugate = polynomial_remainder(
            polynomial_multiply(conjugate, conjugate), modulus
        )
    return trace


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    a_value = from_exponents({2, 4, 6})
    c3_value = from_exponents({3, 7, 9, 10, 11, 12, 16})
    a_cubed = polynomial_power(a_value, 3)
    k_value = [0] * 10
    k_value[0] = 1
    k_value[1] = from_exponents({1, 3})
    k_value[3] = from_exponents({7, 9, 11})
    k_value[4] = 1 << 8
    k_value[7] = 1 << 11
    k_value[8] = 1 << 8
    k_value[9] = from_exponents({9, 11, 13})
    derived_k_value = derive_zero_anchor_polynomial()
    if derived_k_value != k_value:
        raise AssertionError("zero-anchor polynomial derivation mismatch")

    zero_equation = [c3_value, 0, 0, 0, 0, 0, a_cubed]
    one_equation = [
        c3_value ^ a_cubed,
        0,
        a_cubed,
        0,
        a_cubed,
    ]
    zero_resultant = resultant(k_value, zero_equation)
    one_resultant = resultant(k_value, one_equation)

    h_value = 0b10
    h_plus_one = 0b11
    quadratic = 0b111
    r21 = from_exponents({0, 3, 6, 7, 8, 11, 14, 15, 17, 18, 19, 20, 21})
    r109 = from_exponents({
        0, 2, 4, 5, 7, 8, 9, 11, 14, 19, 21, 22, 27, 30, 32, 34,
        35, 36, 37, 38, 41, 42, 43, 45, 50, 51, 53, 55, 59, 60, 62,
        64, 68, 69, 70, 72, 76, 77, 79, 82, 84, 86, 87, 90, 92, 96,
        98, 99, 100, 101, 102, 104, 105, 108, 109,
    })
    r26 = from_exponents({
        0, 2, 3, 5, 6, 7, 8, 9, 12, 15, 16, 18, 19, 20, 21, 23,
        24, 25, 26,
    })
    r29 = from_exponents({
        0, 1, 2, 3, 5, 9, 12, 13, 14, 15, 16, 19, 22, 24, 25, 26, 29,
    })
    r75 = from_exponents({
        0, 3, 9, 11, 12, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26,
        28, 29, 36, 39, 40, 41, 42, 43, 45, 47, 50, 51, 53, 54, 56,
        58, 62, 63, 64, 65, 67, 68, 71, 72, 74, 75,
    })

    common = polynomial_power(h_value, 54)
    common = polynomial_multiply(common, polynomial_power(h_plus_one, 2))
    common = polynomial_multiply(common, polynomial_power(quadratic, 14))
    expected_zero = polynomial_multiply(
        polynomial_multiply(common, r21), r109
    )
    expected_one = common
    for factor in (r26, r29, r75):
        expected_one = polynomial_multiply(expected_one, factor)
    if zero_resultant != expected_zero:
        raise AssertionError("S3=0 resultant factorization mismatch")
    if one_resultant != expected_one:
        raise AssertionError("S3=S1^3 resultant factorization mismatch")

    factors = {
        "R21": r21,
        "R109": r109,
        "R26": r26,
        "R29": r29,
        "R75": r75,
    }
    traces: dict[str, int] = {}
    for name, factor in factors.items():
        if not is_irreducible(factor):
            raise AssertionError(f"{name} is reducible")
        traces[name] = trace_inverse_square(factor)
    if traces != {"R21": 0, "R109": 0, "R26": 0, "R29": 1, "R75": 0}:
        raise AssertionError("unexpected inverse-square trace table")

    result = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0500-ZERO-ANCHOR-RESULTANTS",
        "finite_field_samples_used": False,
        "zero_anchor_polynomial_derived_from_subiaco_formula": True,
        "zero_resultant_degree": zero_resultant.bit_length() - 1,
        "one_resultant_degree": one_resultant.bit_length() - 1,
        "irreducible_factor_degrees": {
            name: factor.bit_length() - 1 for name, factor in factors.items()
        },
        "inverse_square_trace": traces,
        "factor_exponents": {
            name: [
                exponent
                for exponent in range(factor.bit_length())
                if (factor >> exponent) & 1
            ]
            for name, factor in factors.items()
        },
        "conclusion": (
            "For every admissible parameter, the zero-anchor fibre has "
            "S3 neither zero nor S1^3."
        ),
        "remaining_general_target": "zero-anchor external-line existence",
        "status": "PASS_ZERO_ANCHOR_MULTIPLIER_RESULTANTS",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
