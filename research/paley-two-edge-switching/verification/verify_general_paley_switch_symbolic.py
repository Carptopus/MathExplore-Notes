"""Exact symbolic audit for the general two-edge Paley switch.

This verifier uses a tiny integer-coefficient polynomial implementation instead
of importing the Loop C construction.  It checks only identities that are valid
before any finite-field specialization; character conditions and existence are
deliberately outside its scope.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple


Exponent = Tuple[int, int, int]  # powers of alpha, r, x
Polynomial = Dict[Exponent, int]


def normalize(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def constant(value: int) -> Polynomial:
    return {} if value == 0 else {(0, 0, 0): value}


def variable(index: int) -> Polynomial:
    exponent = [0, 0, 0]
    exponent[index] = 1
    return {tuple(exponent): 1}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
    return normalize(result)


def negate(poly: Polynomial) -> Polynomial:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return add(left, negate(right))


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_monomial[index] + right_monomial[index] for index in range(3)
            )
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return normalize(result)


def power(poly: Polynomial, exponent: int) -> Polynomial:
    result = constant(1)
    base = poly
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        remaining >>= 1
    return result


def scale(poly: Polynomial, scalar: int) -> Polynomial:
    return normalize({monomial: scalar * coefficient for monomial, coefficient in poly.items()})


def main() -> None:
    one = constant(1)
    alpha = variable(0)
    ratio = variable(1)
    x = variable(2)

    old_first = multiply(multiply(x, add(one, alpha)), add(one, ratio))
    new_sum_left = multiply(x, add(one, multiply(alpha, ratio)))
    new_sum_right = multiply(x, add(ratio, alpha))
    new_first = add(new_sum_left, new_sum_right)

    old_second = multiply(
        power(x, 2),
        multiply(power(add(one, alpha), 2), add(one, power(ratio, 2))),
    )
    new_second = add(power(new_sum_left, 2), power(new_sum_right, 2))
    second_difference = subtract(new_second, old_second)
    expected_second_difference = scale(
        multiply(
            multiply(alpha, power(x, 2)),
            power(subtract(ratio, one), 2),
        ),
        -2,
    )

    sum_collision_difference = subtract(new_sum_left, new_sum_right)
    expected_collision_difference = multiply(
        multiply(x, subtract(one, alpha)), subtract(one, ratio)
    )

    checks = {
        "first_moment_preserved": subtract(new_first, old_first) == {},
        "second_moment_defect": second_difference == expected_second_difference,
        "new_sums_distinct_factorization": (
            sum_collision_difference == expected_collision_difference
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    output = {
        "experiment_id": "HSF-SWITCH-0002-D1-SYMBOLIC",
        "scope": "integer polynomial identities before finite-field specialization",
        "variable_order": ["alpha", "r", "x"],
        "checks": checks,
        "second_moment_defect": "-2*alpha*x^2*(r-1)^2",
        "new_sum_difference": "x*(1-alpha)*(1-r)",
        "claim_boundary": (
            "This proves the algebraic identities only. It does not prove that "
            "the quadratic-character conditions have solutions, that the Paley "
            "array interface closes, or that the result is novel."
        ),
    }
    output_path = Path(__file__).resolve().parent / "results" / "general-paley-switch-symbolic.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
