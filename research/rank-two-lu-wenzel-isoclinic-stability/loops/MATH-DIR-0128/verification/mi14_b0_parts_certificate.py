#!/usr/bin/env python3
"""Exact Bernstein search for the even and odd parts of the general B0 gate.

This imports the exact quotient-ring reduction from
``mi14_general_b0_reduction.py`` and writes

    B0 = E + imbalance * principal_difference * O.

The principal-angle product triangle is parameterized exactly by

    principal_product = radial * share,
    complement_product = radial * (1-share),

with ``radial, share in [0,1]``.  The unresolved singular wedge has
``product=pq in [0,6/13]`` by S6.  Tensor Bernstein coefficients are computed
with exact rationals.  A PASS for both parts proves B0 nonnegative; a FAIL is
only a failure of this unsplit certificate.
"""

from __future__ import annotations

import argparse
import json
import pickle
from math import comb
from pathlib import Path

import sympy as sp

from mi14_general_b0_reduction import (
    build_general_power_sums,
    constant_pair_gap,
)


def bernstein_statistics(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> dict[str, object]:
    polynomial = sp.Poly(sp.expand(expression), *variables)
    degrees = tuple(polynomial.degree(variable) for variable in variables)
    data: dict[tuple[int, ...], sp.Expr] = {
        monomial: coefficient for monomial, coefficient in polynomial.terms()
    }
    for axis, degree in enumerate(degrees):
        transformed: dict[tuple[int, ...], sp.Expr] = {}
        for indices, value in data.items():
            source = indices[axis]
            denominator = comb(degree, source)
            for target in range(source, degree + 1):
                output = list(indices)
                output[axis] = target
                key = tuple(output)
                transformed[key] = transformed.get(key, 0) + value * sp.Rational(
                    comb(target, source), denominator
                )
        data = transformed
    minimum = min(data.values())
    negative_count = sum(int(bool(value < 0)) for value in data.values())
    return {
        "degrees": list(degrees),
        "minimum": str(minimum),
        "negative_count": int(negative_count),
        "coefficient_count": len(data),
        "power_term_count": len(polynomial.terms()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=("even", "odd", "both"), required=True)
    parser.add_argument("--cache", type=Path)
    args = parser.parse_args()

    control_first, control_second = sp.symbols(
        "control_first control_second", real=True
    )
    positive_control = bernstein_statistics(
        1 + control_first * control_second,
        (control_first, control_second),
    )
    negative_control = bernstein_statistics(
        control_first - sp.Rational(1, 2),
        (control_first, control_second),
    )
    if (
        positive_control["minimum"] != "1"
        or positive_control["negative_count"] != 0
        or negative_control["minimum"] != "-1/2"
        or negative_control["negative_count"] != 1
    ):
        raise SystemExit("Bernstein transform controls failed")

    if args.cache is not None and args.cache.exists():
        with args.cache.open("rb") as handle:
            expression, source_variables = pickle.load(handle)
    else:
        powers, source_variables = build_general_power_sums()
        expression = constant_pair_gap(powers, source_variables)
        if args.cache is not None:
            args.cache.parent.mkdir(parents=True, exist_ok=True)
            with args.cache.open("wb") as handle:
                pickle.dump((expression, source_variables), handle)
    (
        product,
        imbalance,
        principal_product,
        complement_product,
        principal_difference,
        mixing,
        phase_square,
    ) = source_variables
    scaled_product, radial, share = sp.symbols(
        "scaled_product radial share", real=True
    )
    variables = (scaled_product, radial, share, mixing, phase_square)
    label_polynomial = sp.Poly(expression, imbalance, principal_difference)
    requested_parts = ("odd", "even") if args.part == "both" else (args.part,)
    results: dict[str, object] = {}
    passed = True
    for part_name in requested_parts:
        if part_name == "even":
            part = label_polynomial.coeff_monomial(1)
        else:
            part = label_polynomial.coeff_monomial(
                imbalance * principal_difference
            )
            quotient, remainder = sp.div(part, mixing)
            if remainder != 0:
                raise SystemExit("odd part lost its expected mixing factor")
            part = quotient
        boxed = sp.expand(
            part.subs(
                {
                    product: sp.Rational(6, 13) * scaled_product,
                    principal_product: radial * share,
                    complement_product: radial * (1 - share),
                }
            )
        )
        statistics = bernstein_statistics(boxed, variables)
        part_passed = statistics["negative_count"] == 0
        passed = passed and part_passed
        results[part_name] = {
            "result": "PASS" if part_passed else "FAIL",
            "removed_nonnegative_factor": (
                "mixing" if part_name == "odd" else "none"
            ),
            "bernstein": statistics,
        }
    print(
        json.dumps(
            {
                "result": "PASS" if passed else "FAIL",
                "part": args.part,
                "domain": (
                    "pq in [0,6/13], principal products in the exact triangle, "
                    "mixing and phase_square in [0,1]"
                ),
                "transform_controls": {
                    "positive": positive_control,
                    "negative": negative_control,
                },
                "parts": results,
                "interpretation": (
                    "PASS is an exact positivity certificate on the full unresolved box; "
                    "FAIL only rejects this unsplit Bernstein representation."
                ),
            },
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
