#!/usr/bin/env python3
"""Classify the exact zero faces of the S16 isoclinic B0 certificate.

The S16 constant term B0 has a tensor Bernstein representation with
nonnegative coefficients on the unit cube.  Consequently B0 can vanish only
on coordinate faces for which every Bernstein coefficient surviving on the
relative interior is zero.  This script computes those faces exactly and
returns the inclusion-maximal ones.
"""

from __future__ import annotations

from itertools import product
import json
from math import comb

import sympy as sp

from mi14_isoclinic_pair_sum_certificate import (
    build_reduced_power_sums,
    pair_sum_shift_coefficients,
)


def bernstein_coefficients(
    expression: sp.Expr,
    variables: tuple[sp.Symbol, ...],
    forced_degrees: tuple[int, ...] | None = None,
) -> tuple[tuple[int, ...], dict[tuple[int, ...], sp.Expr]]:
    product_variable, radius, mixing, phase_square = variables
    scaled_product = sp.symbols("scaled_product", real=True)
    polynomial = sp.Poly(
        sp.expand(expression.subs(product_variable, scaled_product / 2)),
        scaled_product,
        radius,
        mixing,
        phase_square,
    )
    natural_degrees = tuple(
        polynomial.degree(variable) for variable in polynomial.gens
    )
    degrees = natural_degrees if forced_degrees is None else forced_degrees
    if any(
        forced < natural
        for forced, natural in zip(degrees, natural_degrees)
    ):
        raise ValueError("forced Bernstein degree is below the natural degree")
    power_coefficients = {
        indices: polynomial.coeff_monomial(
            sp.prod(
                variable**degree
                for variable, degree in zip(polynomial.gens, indices)
            )
        )
        for indices in product(*(range(degree + 1) for degree in degrees))
    }
    coefficients: dict[tuple[int, ...], sp.Expr] = {}
    for target in product(*(range(degree + 1) for degree in degrees)):
        value = 0
        for source in product(*(range(index + 1) for index in target)):
            weight = sp.prod(
                sp.Rational(comb(target_index, source_index), comb(degree, source_index))
                for target_index, source_index, degree in zip(
                    target, source, degrees
                )
            )
            value += power_coefficients[source] * weight
        coefficients[target] = sp.factor(value)
    return degrees, coefficients


def face_surviving_indices(
    face: tuple[int | None, ...], degrees: tuple[int, ...]
):
    choices = []
    for value, degree in zip(face, degrees):
        if value is None:
            choices.append(range(degree + 1))
        elif value == 0:
            choices.append((0,))
        else:
            choices.append((degree,))
    return product(*choices)


def contains_face(
    outer: tuple[int | None, ...], inner: tuple[int | None, ...]
) -> bool:
    """Return whether the coordinate face ``outer`` contains ``inner``."""

    return all(
        outer_value is None or outer_value == inner_value
        for outer_value, inner_value in zip(outer, inner)
    )


def render_face(face: tuple[int | None, ...], names: tuple[str, ...]):
    fixed = {
        name: value
        for name, value in zip(names, face)
        if value is not None
    }
    return {
        "dimension": sum(value is None for value in face),
        "fixed": fixed,
    }


def main() -> None:
    power_sums, variables = build_reduced_power_sums()
    b0 = pair_sum_shift_coefficients(power_sums)[0]
    degrees, coefficients = bernstein_coefficients(b0, variables)
    if any(value < 0 for value in coefficients.values()):
        raise RuntimeError("S16 B0 Bernstein representation has a negative coefficient")

    faces = tuple(product((None, 0, 1), repeat=len(degrees)))
    zero_faces = []
    for face in faces:
        surviving = tuple(face_surviving_indices(face, degrees))
        if all(coefficients[index] == 0 for index in surviving):
            zero_faces.append(face)

    maximal_zero_faces = [
        face
        for face in zero_faces
        if not any(
            other != face
            and contains_face(other, face)
            and sum(value is not None for value in other)
            < sum(value is not None for value in face)
            for other in zero_faces
        )
    ]
    zero_by_scaled_product_index = {
        str(index): sum(
            int(bool(value == 0))
            for target, value in coefficients.items()
            if target[0] == index
        )
        for index in range(degrees[0] + 1)
    }
    monomial_lower_bounds = {}
    for exponent in range(1, degrees[0] + 1):
        ratios = []
        for target, value in coefficients.items():
            scaled_index = target[0]
            if scaled_index < exponent:
                continue
            monomial_coefficient = sp.Rational(
                comb(scaled_index, exponent), comb(degrees[0], exponent)
            )
            ratios.append(sp.factor(value / monomial_coefficient))
        monomial_lower_bounds[str(exponent)] = str(min(ratios))
    product_variable, radius, mixing, _ = variables
    rank_one_factor = 48 * (radius * mixing) ** 2 * (
        1 + radius * mixing
    ) ** 2
    remainder_degrees, remainder_coefficients = bernstein_coefficients(
        sp.expand(b0 - rank_one_factor), variables
    )
    if remainder_degrees != degrees:
        raise RuntimeError("rank-one remainder changed the natural degree tuple")
    damped_rank_one_bounds = {}
    scaled_product_power_four = {
        target: (
            sp.Rational(comb(target[0], 4), comb(degrees[0], 4))
            if target[0] >= 4
            else sp.Integer(0)
        )
        for target in coefficients
    }
    for damping_exponent in range(1, degrees[0] + 1):
        _, damped_coefficients = bernstein_coefficients(
            sp.expand(
                (1 - product_variable) ** damping_exponent * rank_one_factor
            ),
            variables,
            degrees,
        )
        residual = {
            target: sp.factor(
                coefficients[target] - damped_coefficients[target]
            )
            for target in coefficients
        }
        ratios = [
            sp.factor(value / scaled_product_power_four[target])
            for target, value in residual.items()
            if scaled_product_power_four[target] != 0
        ]
        damped_rank_one_bounds[str(damping_exponent)] = {
            "residual_minimum": str(min(residual.values())),
            "residual_negative_count": sum(
                int(bool(value < 0)) for value in residual.values()
            ),
            "scaled_product_four_lower_bound": str(min(ratios)),
        }
    names = ("scaled_product", "radius", "mixing", "phase_square")
    rendered_zero_faces = [
        render_face(face, names)
        for face in sorted(
            maximal_zero_faces,
            key=lambda item: (
                -sum(value is None for value in item),
                tuple(-1 if value is None else value for value in item),
            ),
        )
    ]

    expected_zero_faces = {
        (("mixing", 0), ("scaled_product", 0)),
        (("radius", 0), ("scaled_product", 0)),
    }
    actual_zero_faces = {
        tuple(sorted(face["fixed"].items())) for face in rendered_zero_faces
    }
    if degrees != (10, 10, 4, 4):
        raise RuntimeError(f"unexpected B0 Bernstein degrees: {degrees}")
    if len(coefficients) != 3025:
        raise RuntimeError(f"unexpected B0 coefficient count: {len(coefficients)}")
    if sum(int(value == 0) for value in coefficients.values()) != 430:
        raise RuntimeError("unexpected B0 zero coefficient count")
    if actual_zero_faces != expected_zero_faces:
        raise RuntimeError(
            f"unexpected maximal zero faces: {sorted(actual_zero_faces)}"
        )
    if sp.sympify(monomial_lower_bounds["4"]) != 3:
        raise RuntimeError("scaled-product fourth-power lower bound drifted")

    expected_damped = {
        "6": {
            "residual_minimum": sp.Rational(-13, 210),
            "residual_negative_count": 1,
        },
        "7": {
            "residual_negative_count": 0,
            "scaled_product_four_lower_bound": sp.Rational(5, 2),
        },
        "8": {
            "residual_negative_count": 0,
            "scaled_product_four_lower_bound": sp.Integer(3),
        },
    }
    for exponent, expected in expected_damped.items():
        actual = damped_rank_one_bounds[exponent]
        for key, value in expected.items():
            actual_value = (
                sp.sympify(actual[key])
                if key != "residual_negative_count"
                else actual[key]
            )
            if actual_value != value:
                raise RuntimeError(
                    f"damping exponent {exponent} {key} drifted: "
                    f"{actual_value} != {value}"
                )

    payload = {
        "result": "PASS",
        "bernstein_degrees": degrees,
        "coefficient_count": len(coefficients),
        "zero_coefficient_count": sum(
            int(bool(value == 0)) for value in coefficients.values()
        ),
        "positive_coefficient_count": sum(
            int(bool(value > 0)) for value in coefficients.values()
        ),
        "zero_by_scaled_product_index": zero_by_scaled_product_index,
        "coefficientwise_lower_bounds_for_scaled_product_powers": (
            monomial_lower_bounds
        ),
        "rank_one_factor": "48*(radius*mixing)^2*(1+radius*mixing)^2",
        "after_subtracting_rank_one_factor": {
            "minimum": str(min(remainder_coefficients.values())),
            "negative_count": sum(
                int(bool(value < 0)) for value in remainder_coefficients.values()
            ),
            "zero_count": sum(
                int(bool(value == 0)) for value in remainder_coefficients.values()
            ),
        },
        "damped_rank_one_plus_scaled_product_four_bounds": (
            {
                "damping_factor": (
                    "(1-product)^K with product=pq; equivalently "
                    "(1-scaled_product/2)^K"
                ),
                "bounds": damped_rank_one_bounds,
            }
        ),
        "maximal_zero_faces": rendered_zero_faces,
        "interpretation": (
            "Because all tensor Bernstein coefficients are nonnegative, B0 is "
            "strictly positive away from the listed coordinate faces, and its "
            "zero set is exactly their union."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
