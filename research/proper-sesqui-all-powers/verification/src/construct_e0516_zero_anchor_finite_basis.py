"""Construct the finite basis left by the E0516 Weil bound.

The discovery phase tests a bounded stream of field parameters.  It does not
enumerate HSF arrays or exhaust an entire field: roots of the fixed degree-9
and degree-10 polynomials are decided by gcd with X^(2^d)-X.  The emitted
witnesses are subsequently checked independently, so the proof does not rely
on how they were found.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

from verify_zero_anchor_multiplier_resultants import is_irreducible


class BinaryField:
    def __init__(self, degree: int, modulus: int) -> None:
        self.degree = degree
        self.modulus = modulus
        self.order = 1 << degree
        self.mask = self.order - 1

    def multiply(self, left: int, right: int) -> int:
        result = 0
        value = left
        multiplier = right
        while multiplier:
            if multiplier & 1:
                result ^= value
            multiplier >>= 1
            value <<= 1
            if value & self.order:
                value ^= self.modulus
        return result & self.mask

    def power(self, value: int, exponent: int) -> int:
        result = 1
        factor = value
        while exponent:
            if exponent & 1:
                result = self.multiply(result, factor)
            factor = self.multiply(factor, factor)
            exponent >>= 1
        return result

    def inverse(self, value: int) -> int:
        if value == 0:
            raise ZeroDivisionError
        return self.power(value, self.order - 2)

    def trace(self, value: int) -> int:
        result = 0
        conjugate = value
        for _ in range(self.degree):
            result ^= conjugate
            conjugate = self.multiply(conjugate, conjugate)
        if result not in (0, 1):
            raise AssertionError("absolute trace did not land in F_2")
        return result


Polynomial = list[int]


def trim(value: Polynomial) -> Polynomial:
    result = value[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    size = max(len(left), len(right))
    result = [0] * size
    for index in range(size):
        result[index] = (left[index] if index < len(left) else 0) ^ (
            right[index] if index < len(right) else 0
        )
    return trim(result)


def polynomial_multiply(
    field: BinaryField, left: Polynomial, right: Polynomial
) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            result[left_degree + right_degree] ^= field.multiply(
                left_coefficient, right_coefficient
            )
    return trim(result)


def polynomial_remainder(
    field: BinaryField, dividend: Polynomial, divisor: Polynomial
) -> Polynomial:
    result = trim(dividend)
    divisor = trim(divisor)
    inverse_leading = field.inverse(divisor[-1])
    while len(result) >= len(divisor) and result != [0]:
        shift = len(result) - len(divisor)
        scale = field.multiply(result[-1], inverse_leading)
        for index, coefficient in enumerate(divisor):
            result[index + shift] ^= field.multiply(scale, coefficient)
        result = trim(result)
    return result


def polynomial_monic(field: BinaryField, value: Polynomial) -> Polynomial:
    value = trim(value)
    if value == [0]:
        return value
    scale = field.inverse(value[-1])
    return trim([field.multiply(scale, coefficient) for coefficient in value])


def polynomial_gcd(
    field: BinaryField, left: Polynomial, right: Polynomial
) -> Polynomial:
    left = trim(left)
    right = trim(right)
    while right != [0]:
        left, right = right, polynomial_remainder(field, left, right)
    return polynomial_monic(field, left)


def x_to_field_order_mod(field: BinaryField, modulus: Polynomial) -> Polynomial:
    value = [0, 1]
    for _ in range(field.degree):
        value = polynomial_remainder(
            field, polynomial_multiply(field, value, value), modulus
        )
    return value


def field_root_factor(field: BinaryField, polynomial: Polynomial) -> Polynomial:
    x_to_q = x_to_field_order_mod(field, polynomial)
    return polynomial_gcd(field, polynomial, polynomial_add(x_to_q, [0, 1]))


def find_irreducible_modulus(degree: int) -> int:
    rng = random.Random(0xE0516000 + degree)
    for _ in range(10_000):
        middle = rng.getrandbits(degree - 1)
        candidate = (1 << degree) | (middle << 1) | 1
        if is_irreducible(candidate):
            return candidate
    raise RuntimeError(f"no irreducible modulus found for degree {degree}")


def parameter_polynomial(field: BinaryField, parameter: int) -> Polynomial:
    square = field.multiply(parameter, parameter)
    u_value = 1 ^ parameter ^ square
    result = [0] * 10
    result[0] = 1
    result[1] = 1 ^ parameter
    result[3] = field.multiply(square, u_value)
    result[4] = square
    result[7] = square
    result[8] = 1
    result[9] = u_value
    return trim(result)


def incidence_polynomial(
    field: BinaryField, parameter: int, partner: int
) -> Polynomial:
    square = field.multiply(parameter, parameter)
    u_value = 1 ^ parameter ^ square
    partner_square = field.multiply(partner, partner)
    result = [0] * 11
    result[0] = field.multiply(u_value, partner_square)
    result[1] = 1
    result[2] = 1 ^ parameter
    result[4] = field.multiply(
        field.multiply(square, u_value), 1 ^ partner_square
    )
    result[5] = square
    result[8] = square ^ field.multiply(u_value, partner_square)
    result[9] = 1
    result[10] = u_value
    return trim(result)


def evaluate(field: BinaryField, polynomial: Polynomial, value: int) -> int:
    result = 0
    for coefficient in reversed(polynomial):
        result = field.multiply(result, value) ^ coefficient
    return result


def candidate_stream(field: BinaryField):
    rng = random.Random(0xBAD1C1D3 + field.degree)
    yielded: set[int] = set()
    for candidate in range(2, min(field.order, 258)):
        yielded.add(candidate)
        yield candidate
    while True:
        candidate = rng.randrange(1, field.order)
        if candidate not in yielded:
            yielded.add(candidate)
            yield candidate


def find_witness(degree: int) -> dict[str, int]:
    modulus = find_irreducible_modulus(degree)
    field = BinaryField(degree, modulus)
    trials = 0
    for parameter in candidate_stream(field):
        trials += 1
        square = field.multiply(parameter, parameter)
        u_value = 1 ^ parameter ^ square
        if u_value == 0 or field.trace(field.inverse(parameter)) != 1:
            continue
        k_polynomial = parameter_polynomial(field, parameter)
        root_factor = field_root_factor(field, k_polynomial)
        if len(root_factor) != 2:
            continue
        partner = field.multiply(root_factor[0], field.inverse(root_factor[1]))
        if evaluate(field, k_polynomial, partner) != 0:
            raise AssertionError("linear root factor did not recover a K-root")
        l_polynomial = incidence_polynomial(field, parameter, partner)
        incidence_roots = field_root_factor(field, l_polynomial)
        if len(incidence_roots) == 1:
            return {
                "degree": degree,
                "modulus": modulus,
                "parameter_a": parameter,
                "partner_t": partner,
                "trials": trials,
            }
        if trials >= 100_000:
            break
    raise RuntimeError(f"no finite-basis witness found for d={degree}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    witnesses = [find_witness(degree) for degree in range(4, 34, 2)]
    result = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0516-ZERO-ANCHOR-FINITE-BASIS",
        "basis_degrees": list(range(4, 34, 2)),
        "method": "fixed-degree polynomial gcd with X^(2^d)-X",
        "parameter_search_used": True,
        "maximum_parameter_trials": max(witness["trials"] for witness in witnesses),
        "array_enumeration_used": False,
        "exhaustive_field_enumeration_used": False,
        "witnesses": witnesses,
        "status": "PASS_FINITE_BASIS_CONSTRUCTION",
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
