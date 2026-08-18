"""Symbolic proof check for the cubic Subiaco image power sum.

The calculation is performed in characteristic two over the rational function
field F_2(h), where h^2=c.  It uses only the quadratic pole relations and the
trace-hyperplane reciprocal-sum identities; no finite-field samples enter the
check.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import comb
from pathlib import Path


Laurent = frozenset[int]
Poly = dict[int, Laurent]


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


LAURENT_ZERO: Laurent = frozenset()
LAURENT_ONE: Laurent = frozenset({0})


def poly_clean(value: Poly) -> Poly:
    return {degree: coefficient for degree, coefficient in value.items() if coefficient}


def poly_add(*values: Poly) -> Poly:
    result: Poly = {}
    for value in values:
        for degree, coefficient in value.items():
            result[degree] = laurent_add(
                result.get(degree, LAURENT_ZERO), coefficient
            )
    return poly_clean(result)


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            degree = left_degree + right_degree
            coefficient = laurent_multiply(left_coefficient, right_coefficient)
            result[degree] = laurent_add(
                result.get(degree, LAURENT_ZERO), coefficient
            )
    return poly_clean(result)


def poly_power(value: Poly, exponent: int) -> Poly:
    result: Poly = {0: LAURENT_ONE}
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = poly_multiply(result, base)
        base = poly_multiply(base, base)
        remaining >>= 1
    return result


def poly_scale(value: Poly, coefficient: Laurent, degree_shift: int = 0) -> Poly:
    return poly_clean(
        {
            degree + degree_shift: laurent_multiply(old_coefficient, coefficient)
            for degree, old_coefficient in value.items()
        }
    )


def poly_frobenius_substitute(value: Poly) -> Poly:
    """Return value(z^2)."""

    return {2 * degree: coefficient for degree, coefficient in value.items()}


@dataclass(frozen=True)
class QuadraticElement:
    """base + root*coefficient, with root^2+root=h^relation_power."""

    base: Laurent
    coefficient: Laurent
    relation_power: int

    def __add__(self, other: "QuadraticElement") -> "QuadraticElement":
        if self.relation_power != other.relation_power:
            raise ValueError("quadratic relation mismatch")
        return QuadraticElement(
            laurent_add(self.base, other.base),
            laurent_add(self.coefficient, other.coefficient),
            self.relation_power,
        )

    def __mul__(self, other: "QuadraticElement") -> "QuadraticElement":
        if self.relation_power != other.relation_power:
            raise ValueError("quadratic relation mismatch")
        product = laurent_multiply(self.coefficient, other.coefficient)
        return QuadraticElement(
            laurent_add(
                laurent_multiply(self.base, other.base),
                laurent_shift(product, self.relation_power),
            ),
            laurent_add(
                laurent_multiply(self.base, other.coefficient),
                laurent_multiply(self.coefficient, other.base),
                product,
            ),
            self.relation_power,
        )

    def __pow__(self, exponent: int) -> "QuadraticElement":
        result = QuadraticElement(
            LAURENT_ONE, LAURENT_ZERO, self.relation_power
        )
        base = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * base
            base = base * base
            remaining >>= 1
        return result


def shifted_numerator_coefficients(
    numerator: Poly,
    relation_power: int,
    use_other_root: bool,
) -> dict[int, QuadraticElement]:
    root = QuadraticElement(
        LAURENT_ONE if use_other_root else LAURENT_ZERO,
        LAURENT_ONE,
        relation_power,
    )
    result: dict[int, QuadraticElement] = {}
    zero = QuadraticElement(LAURENT_ZERO, LAURENT_ZERO, relation_power)
    for degree, coefficient in numerator.items():
        for r_degree in range(degree + 1):
            if comb(degree, r_degree) % 2 == 0:
                continue
            contribution = root ** (degree - r_degree)
            contribution = QuadraticElement(
                laurent_multiply(contribution.base, coefficient),
                laurent_multiply(contribution.coefficient, coefficient),
                relation_power,
            )
            result[r_degree] = result.get(r_degree, zero) + contribution
    return result


def paired_partial_fraction_coefficients(
    numerator: Poly,
    pole_order: int,
    relation_power: int,
) -> dict[int, Laurent]:
    """Return paired coefficients of (z+r)^(-k) at r and r+1."""

    shifted = [
        shifted_numerator_coefficients(numerator, relation_power, other)
        for other in (False, True)
    ]
    result: dict[int, Laurent] = {}
    zero = QuadraticElement(LAURENT_ZERO, LAURENT_ZERO, relation_power)
    for pole_power in range(1, pole_order + 1):
        target_degree = pole_order - pole_power
        paired = zero
        for local in shifted:
            coefficient = zero
            for numerator_degree in range(target_degree + 1):
                series_degree = target_degree - numerator_degree
                if comb(pole_order + series_degree - 1, series_degree) % 2:
                    coefficient = coefficient + local.get(numerator_degree, zero)
            paired = paired + coefficient
        if paired.coefficient:
            raise AssertionError(
                f"paired pole coefficient retained quadratic part at k={pole_power}"
            )
        result[pole_power] = paired.base
    return result


# GF(4) element a+b*w encoded as a | (b << 1), with w^2+w+1=0.
def gf4_add(left: int, right: int) -> int:
    return left ^ right


def gf4_multiply(left: int, right: int) -> int:
    a0, a1 = left & 1, (left >> 1) & 1
    b0, b1 = right & 1, (right >> 1) & 1
    return (a0 * b0 ^ a1 * b1) | (
        (a0 * b1 ^ a1 * b0 ^ a1 * b1) << 1
    )


def trace_hyperplane_reciprocal_sums(maximum: int, first_sum: int) -> list[int]:
    """Power sums from prod(1+t/(z+a))=1+L(t)/L(a)."""

    elementary = [0] * (maximum + 1)
    for index in range(1, maximum + 1):
        if index & (index - 1) == 0:
            elementary[index] = first_sum
    power_sums = [0] * (maximum + 1)
    for index in range(1, maximum + 1):
        value = elementary[index] if index % 2 else 0
        for part in range(1, index):
            value = gf4_add(
                value,
                gf4_multiply(elementary[part], power_sums[index - part]),
            )
        power_sums[index] = value
    return power_sums


def accumulate_with_gf4(
    coefficients: dict[int, Laurent],
    sums: list[int],
) -> tuple[Laurent, Laurent]:
    base = LAURENT_ZERO
    omega = LAURENT_ZERO
    for index, coefficient in coefficients.items():
        scalar = sums[index]
        if scalar & 1:
            base = laurent_add(base, coefficient)
        if scalar & 2:
            omega = laurent_add(omega, coefficient)
    return base, omega


def binary_poly_multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def binary_poly_remainder(dividend: int, divisor: int) -> int:
    divisor_degree = divisor.bit_length() - 1
    while dividend and dividend.bit_length() - 1 >= divisor_degree:
        dividend ^= divisor << (dividend.bit_length() - 1 - divisor_degree)
    return dividend


def has_no_proper_monic_divisor(value: int) -> bool:
    degree = value.bit_length() - 1
    for divisor_degree in range(1, degree // 2 + 1):
        for lower_terms in range(1 << divisor_degree):
            divisor = (1 << divisor_degree) | lower_terms
            if binary_poly_remainder(value, divisor) == 0:
                return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    one: Laurent = LAURENT_ONE
    h2: Laurent = frozenset({2})
    u: Laurent = frozenset({0, 2, 4})

    e: Poly = {2: one, 1: one, 0: frozenset({-4})}
    q_numerator: Poly = {
        4: frozenset({4}),
        3: laurent_shift(u, 2),
        2: u,
        1: frozenset({-2}),
    }
    m_numerator = poly_add(
        q_numerator,
        poly_scale(poly_power(e, 2), laurent_multiply(u, h2), 1),
    )

    # R(z)^3 + c*z*R(z), where R=M/E^2.
    first_numerator = poly_add(
        poly_power(m_numerator, 3),
        poly_scale(
            poly_multiply(m_numerator, poly_power(e, 4)),
            h2,
            1,
        ),
    )
    first_coefficients = paired_partial_fraction_coefficients(
        first_numerator,
        pole_order=6,
        relation_power=-4,
    )

    # h*w*R(w^2)^2; E(w^2)=J(w)^2 and the denominator is J^8.
    second_numerator = poly_scale(
        poly_power(poly_frobenius_substitute(m_numerator), 2),
        frozenset({1}),
        1,
    )
    second_coefficients = paired_partial_fraction_coefficients(
        second_numerator,
        pole_order=8,
        relation_power=-2,
    )

    # If w=L(eta), then 1/L(eta)=w^2 and 1/L(eta^2)=w.
    # Encoding uses w=2 and w^2=w+1=3.
    first_sums = trace_hyperplane_reciprocal_sums(6, first_sum=2)
    second_sums = trace_hyperplane_reciprocal_sums(8, first_sum=3)
    first_value = accumulate_with_gf4(first_coefficients, first_sums)
    second_value = accumulate_with_gf4(second_coefficients, second_sums)
    total = (
        laurent_add(first_value[0], second_value[0]),
        laurent_add(first_value[1], second_value[1]),
    )

    expected = frozenset({3, 7, 9, 10, 11, 12, 16})
    if total[1]:
        raise AssertionError("cubic image sum retained an unexpected GF(4) part")
    if total[0] != expected:
        raise AssertionError(
            f"cubic image sum mismatch: got={sorted(total[0])}, "
            f"expected={sorted(expected)}"
        )

    factor_quadratic = 0b111  # h^2+h+1
    factor_cubic = 0b1011  # h^3+h+1
    factor_quintic = 0b110111  # h^5+h^4+h^2+h+1
    expected_bits = sum(1 << exponent for exponent in expected)
    factored_bits = 1 << 3
    for factor in (
        factor_quadratic,
        factor_cubic,
        factor_cubic,
        factor_quintic,
    ):
        factored_bits = binary_poly_multiply(factored_bits, factor)
    if factored_bits != expected_bits:
        raise AssertionError("cubic image sum factorization failed")
    if not has_no_proper_monic_divisor(factor_cubic):
        raise AssertionError("h^3+h+1 is reducible")
    if not has_no_proper_monic_divisor(factor_quintic):
        raise AssertionError("h^5+h^4+h^2+h+1 is reducible")

    payload = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0497-SUBIACO-CUBIC-IMAGE-SUM",
        "method": (
            "Exact characteristic-two Laurent-polynomial calculation over "
            "F_2(h), quadratic-pole pairing, and trace-hyperplane reciprocal sums"
        ),
        "finite_field_samples_used": False,
        "identity": "sum_I_y3=h^3+h^7+h^9+h^10+h^11+h^12+h^16",
        "factorization": (
            "h^3*(h^2+h+1)*(h^3+h+1)^2*"
            "(h^5+h^4+h^2+h+1)"
        ),
        "status": "PASS_SUBIACO_CUBIC_IMAGE_SUM",
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
