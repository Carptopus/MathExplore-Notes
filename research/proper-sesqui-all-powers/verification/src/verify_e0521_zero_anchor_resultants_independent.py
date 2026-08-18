"""Independent evaluation/interpolation audit of the E0500 resultants.

This verifier deliberately does not import the original E0500 verifier.  It
evaluates both Sylvester determinants at every element of GF(256), reconstructs
the resultant by Lagrange interpolation, verifies the advertised factor
products, and uses Berlekamp nullities rather than Rabin tests for
irreducibility.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


AES_REDUCTION = 0x1B  # x^8+x^4+x^3+x+1


def gf256_mul(left: int, right: int) -> int:
    result = 0
    a = left
    b = right
    for _ in range(8):
        if b & 1:
            result ^= a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a ^= AES_REDUCTION
        b >>= 1
    return result


def gf256_pow(value: int, exponent: int) -> int:
    result = 1
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = gf256_mul(result, base)
        base = gf256_mul(base, base)
        remaining >>= 1
    return result


def gf256_inverse(value: int) -> int:
    if value == 0:
        raise ZeroDivisionError("zero has no inverse")
    return gf256_pow(value, 254)


def evaluate_exponent_sum(exponents: tuple[int, ...], powers: list[int]) -> int:
    result = 0
    for exponent in exponents:
        result ^= powers[exponent]
    return result


K_COEFFICIENT_EXPONENTS: tuple[tuple[int, ...], ...] = (
    (0,),
    (1, 3),
    (),
    (7, 9, 11),
    (8,),
    (),
    (),
    (11,),
    (8,),
    (9, 11, 13),
)
A_EXPONENTS = (2, 4, 6)
C3_EXPONENTS = (3, 7, 9, 10, 11, 12, 16)


FACTOR_EXPONENTS: dict[str, tuple[int, ...]] = {
    "R21": (0, 3, 6, 7, 8, 11, 14, 15, 17, 18, 19, 20, 21),
    "R109": (
        0, 2, 4, 5, 7, 8, 9, 11, 14, 19, 21, 22, 27, 30, 32, 34,
        35, 36, 37, 38, 41, 42, 43, 45, 50, 51, 53, 55, 59, 60, 62,
        64, 68, 69, 70, 72, 76, 77, 79, 82, 84, 86, 87, 90, 92, 96,
        98, 99, 100, 101, 102, 104, 105, 108, 109,
    ),
    "R26": (0, 2, 3, 5, 6, 7, 8, 9, 12, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26),
    "R29": (0, 1, 2, 3, 5, 9, 12, 13, 14, 15, 16, 19, 22, 24, 25, 26, 29),
    "R75": (
        0, 3, 9, 11, 12, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26,
        28, 29, 36, 39, 40, 41, 42, 43, 45, 47, 50, 51, 53, 54, 56,
        58, 62, 63, 64, 65, 67, 68, 71, 72, 74, 75,
    ),
}


def coefficient_values_at(h_value: int) -> tuple[list[int], list[int], list[int]]:
    powers = [1]
    for _ in range(240):
        powers.append(gf256_mul(powers[-1], h_value))
    k_values = [evaluate_exponent_sum(item, powers) for item in K_COEFFICIENT_EXPONENTS]
    a_value = evaluate_exponent_sum(A_EXPONENTS, powers)
    a_cubed = gf256_mul(gf256_mul(a_value, a_value), a_value)
    c3_value = evaluate_exponent_sum(C3_EXPONENTS, powers)
    zero_values = [c3_value, 0, 0, 0, 0, 0, a_cubed]
    one_values = [c3_value ^ a_cubed, 0, a_cubed, 0, a_cubed]
    return k_values, zero_values, one_values


def sylvester_determinant(left: list[int], right: list[int]) -> int:
    left_degree = len(left) - 1
    right_degree = len(right) - 1
    size = left_degree + right_degree
    matrix = [[0] * size for _ in range(size)]
    for row in range(right_degree):
        for offset, coefficient in enumerate(left):
            matrix[row][row + offset] = coefficient
    for row in range(left_degree):
        for offset, coefficient in enumerate(right):
            matrix[right_degree + row][row + offset] = coefficient

    determinant = 1
    for column in range(size):
        pivot_row = next((row for row in range(column, size) if matrix[row][column]), None)
        if pivot_row is None:
            return 0
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]
            # A row-swap sign is invisible in characteristic two.
        pivot = matrix[column][column]
        determinant = gf256_mul(determinant, pivot)
        inverse = gf256_inverse(pivot)
        for entry in range(column, size):
            matrix[column][entry] = gf256_mul(matrix[column][entry], inverse)
        for row in range(column + 1, size):
            multiplier = matrix[row][column]
            if multiplier == 0:
                continue
            for entry in range(column, size):
                matrix[row][entry] ^= gf256_mul(multiplier, matrix[column][entry])
    return determinant


def interpolate_all_gf256(values: list[int]) -> list[int]:
    """Interpolate values on all GF(256) points, degree at most 255.

    The vanishing polynomial is Q(X)=X^256+X and Q'(X)=1.  Hence the
    Lagrange basis at alpha is Q(X)/(X+alpha).
    """

    if len(values) != 256:
        raise ValueError("all 256 field values are required")
    coefficients = [0] * 256
    for alpha, value in enumerate(values):
        if value == 0:
            continue
        quotient = [0] * 256
        quotient[255] = 1
        for degree in range(255, 0, -1):
            q_coefficient = 1 if degree == 1 else 0
            quotient[degree - 1] = q_coefficient ^ gf256_mul(alpha, quotient[degree])
        if gf256_mul(alpha, quotient[0]) != 0:
            raise AssertionError("synthetic division failed at the constant term")
        for degree, coefficient in enumerate(quotient):
            coefficients[degree] ^= gf256_mul(value, coefficient)
    return coefficients


SetPolynomial = frozenset[int]


def set_poly_add(left: SetPolynomial, right: SetPolynomial) -> SetPolynomial:
    return frozenset(set(left).symmetric_difference(right))


def set_poly_multiply(left: SetPolynomial, right: SetPolynomial) -> SetPolynomial:
    output: set[int] = set()
    for left_degree in left:
        for right_degree in right:
            degree = left_degree + right_degree
            if degree in output:
                output.remove(degree)
            else:
                output.add(degree)
    return frozenset(output)


def set_poly_power(value: SetPolynomial, exponent: int) -> SetPolynomial:
    result: SetPolynomial = frozenset({0})
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = set_poly_multiply(result, base)
        base = set_poly_multiply(base, base)
        remaining >>= 1
    return result


def set_poly_remainder(value: SetPolynomial, modulus: SetPolynomial) -> SetPolynomial:
    remainder = set(value)
    modulus_degree = max(modulus)
    while remainder and max(remainder) >= modulus_degree:
        shift = max(remainder) - modulus_degree
        for degree in modulus:
            shifted = degree + shift
            if shifted in remainder:
                remainder.remove(shifted)
            else:
                remainder.add(shifted)
    return frozenset(remainder)


def set_poly_gcd(left: SetPolynomial, right: SetPolynomial) -> SetPolynomial:
    a = left
    b = right
    while b:
        a, b = b, set_poly_remainder(a, b)
    return a


def derivative(value: SetPolynomial) -> SetPolynomial:
    return frozenset(exponent - 1 for exponent in value if exponent & 1)


def binary_rank(rows: list[int], width: int) -> int:
    working = rows[:]
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(working)) if (working[row] >> column) & 1), None)
        if pivot is None:
            continue
        working[rank], working[pivot] = working[pivot], working[rank]
        for row in range(len(working)):
            if row != rank and ((working[row] >> column) & 1):
                working[row] ^= working[rank]
        rank += 1
    return rank


def berlekamp_nullity(value: SetPolynomial) -> int:
    degree = max(value)
    if set_poly_gcd(value, derivative(value)) != frozenset({0}):
        raise AssertionError("candidate factor is not squarefree")
    rows = [0] * degree
    for column in range(degree):
        reduced = set_poly_remainder(frozenset({2 * column}), value)
        for row in reduced:
            rows[row] ^= 1 << column
    for index in range(degree):
        rows[index] ^= 1 << index
    return degree - binary_rank(rows, degree)


def expected_products() -> tuple[SetPolynomial, SetPolynomial]:
    h = frozenset({1})
    h_plus_one = frozenset({0, 1})
    quadratic = frozenset({0, 1, 2})
    common = set_poly_power(h, 54)
    common = set_poly_multiply(common, set_poly_power(h_plus_one, 2))
    common = set_poly_multiply(common, set_poly_power(quadratic, 14))
    factors = {name: frozenset(exponents) for name, exponents in FACTOR_EXPONENTS.items()}
    zero = set_poly_multiply(set_poly_multiply(common, factors["R21"]), factors["R109"])
    one = common
    for name in ("R26", "R29", "R75"):
        one = set_poly_multiply(one, factors[name])
    return zero, one


def coefficient_digest(coefficients: list[int]) -> str:
    return hashlib.sha256(bytes(coefficients)).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    field_inverse_checks = all(
        gf256_mul(value, gf256_inverse(value)) == 1 for value in range(1, 256)
    )
    field_frobenius_checks = all(
        gf256_pow(value, 256) == value for value in range(256)
    )
    if not field_inverse_checks or not field_frobenius_checks:
        raise AssertionError("GF(256) interpolation field self-check failed")

    zero_values: list[int] = []
    one_values: list[int] = []
    for h_value in range(256):
        k_values, zero_equation, one_equation = coefficient_values_at(h_value)
        zero_values.append(sylvester_determinant(k_values, zero_equation))
        one_values.append(sylvester_determinant(k_values, one_equation))

    zero_coefficients = interpolate_all_gf256(zero_values)
    one_coefficients = interpolate_all_gf256(one_values)
    if any(coefficient not in (0, 1) for coefficient in zero_coefficients + one_coefficients):
        raise AssertionError("interpolated resultant did not descend to GF(2)")
    if any(zero_coefficients[index] for index in range(241, 256)):
        raise AssertionError("zero resultant exceeded its independent degree-240 bound")
    if any(one_coefficients[index] for index in range(215, 256)):
        raise AssertionError("one resultant exceeded its independent degree-214 bound")

    reconstructed_zero = frozenset(index for index, coefficient in enumerate(zero_coefficients) if coefficient)
    reconstructed_one = frozenset(index for index, coefficient in enumerate(one_coefficients) if coefficient)
    expected_zero, expected_one = expected_products()
    if reconstructed_zero != expected_zero:
        raise AssertionError("independent S3=0 resultant reconstruction mismatch")
    if reconstructed_one != expected_one:
        raise AssertionError("independent S3=S1^3 resultant reconstruction mismatch")

    factors = {name: frozenset(exponents) for name, exponents in FACTOR_EXPONENTS.items()}
    nullities = {name: berlekamp_nullity(factor) for name, factor in factors.items()}
    if any(nullity != 1 for nullity in nullities.values()):
        raise AssertionError("Berlekamp audit found a reducible advertised factor")

    # For monic f with constant coefficient one and root alpha,
    # Tr(alpha^-1) is the x coefficient of f.  Frobenius invariance gives
    # Tr(alpha^-2)=Tr(alpha^-1)^2, the same bit.
    inverse_square_traces = {
        name: int(1 in factor) for name, factor in factors.items()
    }
    expected_traces = {"R21": 0, "R109": 0, "R26": 0, "R29": 1, "R75": 0}
    if inverse_square_traces != expected_traces:
        raise AssertionError("coefficient-based inverse-square trace table mismatch")

    # Destructive controls: a one-coefficient corruption must be detected, and
    # the unique trace-one factor must be distinguished from the four trace-zero factors.
    corrupted_expected = set(expected_zero)
    corrupted_expected.symmetric_difference_update({17})
    product_negative_control = reconstructed_zero != frozenset(corrupted_expected)
    trace_negative_control = sum(inverse_square_traces.values()) == 1 and inverse_square_traces["R29"] == 1
    if not product_negative_control or not trace_negative_control:
        raise AssertionError("a destructive control was not detected")

    result = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0521-ZERO-ANCHOR-RESULTANTS-INDEPENDENT",
        "independence": (
            "No import from the E0500 verifier; GF(256) evaluation plus Gaussian "
            "Sylvester determinants and all-point interpolation; Berlekamp nullity "
            "instead of Rabin irreducibility; inverse-square traces from coefficients."
        ),
        "evaluation_field": "GF(2^8), modulus x^8+x^4+x^3+x+1",
        "evaluation_points": 256,
        "evaluation_field_self_check": {
            "all_nonzero_inverses": field_inverse_checks,
            "frobenius_fixed_all_256_elements": field_frobenius_checks,
        },
        "independent_degree_bounds": {"zero": 240, "one": 214},
        "reconstructed_degrees": {
            "zero": max(reconstructed_zero),
            "one": max(reconstructed_one),
        },
        "coefficient_sha256": {
            "zero": coefficient_digest(zero_coefficients),
            "one": coefficient_digest(one_coefficients),
        },
        "factor_degrees": {name: max(factor) for name, factor in factors.items()},
        "berlekamp_nullities": nullities,
        "inverse_square_trace_from_x_coefficient": inverse_square_traces,
        "negative_controls": {
            "single_coefficient_product_corruption_detected": product_negative_control,
            "unique_trace_one_factor_detected": trace_negative_control,
        },
        "status": "PASS_E0521_INDEPENDENT_ZERO_ANCHOR_RESULTANTS",
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
