"""Test one parameter-independent hyperoval-to-two-fibre construction criterion.

The finite cases are formula checks only.  A positive family claim requires a
separate proof for every admissible dimension.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from construct_inverse_pair_hsf_family import (
    absolute_trace,
    inverse,
    multiply,
    power,
)


MODULI = {
    4: 0b10011,       # x^4+x+1
    6: 0b1000011,     # x^6+x+1
    8: 0b100011011,   # x^8+x^4+x^3+x+1
}


def add(*values: int) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def subiaco_value(x: int, parameter: int, dimension: int, modulus: int) -> int:
    """Evaluate the standard Subiaco o-polynomial formula."""

    parameter_squared = multiply(parameter, parameter, modulus, dimension)
    x_squared = multiply(x, x, modulus, dimension)
    x_cubed = multiply(x_squared, x, modulus, dimension)
    x_fourth = multiply(x_squared, x_squared, modulus, dimension)
    coefficient = multiply(
        parameter_squared,
        add(1, parameter, parameter_squared),
        modulus,
        dimension,
    )
    numerator = add(
        multiply(parameter_squared, add(x_fourth, x), modulus, dimension),
        multiply(coefficient, add(x_cubed, x_squared), modulus, dimension),
    )
    denominator_base = add(
        x_squared,
        multiply(parameter, x, modulus, dimension),
        1,
    )
    denominator = multiply(denominator_base, denominator_base, modulus, dimension)
    if denominator == 0:
        raise ZeroDivisionError("Subiaco denominator vanished")
    rational = multiply(numerator, inverse(denominator, modulus, dimension), modulus, dimension)
    square_root = power(x, 1 << (dimension - 1), modulus, dimension)
    return rational ^ square_root


def subiaco_clan_constants(
    parameter: int,
    dimension: int,
    modulus: int,
) -> tuple[int, int]:
    parameter_squared = multiply(parameter, parameter, modulus, dimension)
    parameter_fifth = power(parameter, 5, modulus, dimension)
    parameter_root = power(parameter, 1 << (dimension - 1), modulus, dimension)
    common = add(parameter_squared, parameter_fifth, parameter_root)
    denominator = multiply(
        parameter,
        add(1, parameter, parameter_squared),
        modulus,
        dimension,
    )
    kappa = multiply(common, inverse(denominator, modulus, dimension), modulus, dimension)
    return common, kappa


def subiaco_companion_value(
    x: int,
    parameter: int,
    dimension: int,
    modulus: int,
) -> int:
    """Evaluate the companion diagonal function in the normalized Subiaco q-clan."""

    parameter_squared = multiply(parameter, parameter, modulus, dimension)
    parameter_cubed = multiply(parameter_squared, parameter, modulus, dimension)
    parameter_fourth = multiply(parameter_squared, parameter_squared, modulus, dimension)
    common, _ = subiaco_clan_constants(parameter, dimension, modulus)
    x_squared = multiply(x, x, modulus, dimension)
    x_cubed = multiply(x_squared, x, modulus, dimension)
    x_fourth = multiply(x_squared, x_squared, modulus, dimension)
    numerator = add(
        multiply(parameter_fourth, x_fourth, modulus, dimension),
        multiply(
            multiply(
                parameter_cubed,
                add(1, parameter_squared, parameter_fourth),
                modulus,
                dimension,
            ),
            x_cubed,
            modulus,
            dimension,
        ),
        multiply(
            multiply(
                parameter_cubed,
                add(1, parameter_squared),
                modulus,
                dimension,
            ),
            x,
            modulus,
            dimension,
        ),
    )
    denominator_base = add(
        x_squared,
        multiply(parameter, x, modulus, dimension),
        1,
    )
    denominator = multiply(
        common,
        multiply(denominator_base, denominator_base, modulus, dimension),
        modulus,
        dimension,
    )
    rational = multiply(numerator, inverse(denominator, modulus, dimension), modulus, dimension)
    parameter_root = power(parameter, 1 << (dimension - 1), modulus, dimension)
    square_root = power(x, 1 << (dimension - 1), modulus, dimension)
    root_term = multiply(
        multiply(parameter_root, inverse(common, modulus, dimension), modulus, dimension),
        square_root,
        modulus,
        dimension,
    )
    return rational ^ root_term


def is_in_gf4(value: int, dimension: int, modulus: int) -> bool:
    return power(value, 4, modulus, dimension) == value


def admissible_parameters(dimension: int, modulus: int) -> list[int]:
    result = []
    for parameter in range(1, 1 << dimension):
        if absolute_trace(inverse(parameter, modulus, dimension), modulus, dimension) != 1:
            continue
        if dimension % 4 == 2 and is_in_gf4(parameter, dimension, modulus):
            continue
        result.append(parameter)
    return result


def fibre_pairs(values: list[int]) -> list[tuple[int, int]] | None:
    fibres: dict[int, list[int]] = defaultdict(list)
    for point, value in enumerate(values):
        fibres[value].append(point)
    if any(len(points) != 2 for points in fibres.values()):
        return None
    return [tuple(points) for points in fibres.values()]


def intersection_histogram(image: set[int], dimension: int, modulus: int) -> Counter[int]:
    histogram: Counter[int] = Counter()
    for ratio in range(2, 1 << dimension):
        translated = {
            multiply(ratio, value, modulus, dimension)
            for value in image
        }
        histogram[len(image & translated)] += 1
    return histogram


def analyze_parameter(
    dimension: int,
    modulus: int,
    parameter: int,
) -> dict[str, object]:
    order = 1 << dimension
    oval = [subiaco_value(x, parameter, dimension, modulus) for x in range(order)]
    if sorted(oval) != list(range(order)):
        return {"parameter": parameter, "status": "FAIL_NOT_PERMUTATION"}

    for slope in range(1, order):
        binomial = [
            oval[z] ^ multiply(slope, z, modulus, dimension)
            for z in range(order)
        ]
        pairs = fibre_pairs(binomial)
        if pairs is None:
            return {
                "parameter": parameter,
                "slope": slope,
                "status": "FAIL_NOT_TWO_TO_ONE",
            }

        zero_pair = next(pair for pair in pairs if 0 in pair)
        zero_partner = zero_pair[0] ^ zero_pair[1]
        special_value = multiply(slope, zero_partner, modulus, dimension)
        image = set(binomial)
        if special_value in image:
            continue

        differences = [left ^ right for left, right in pairs]
        trace_scales = [
            scale
            for scale in range(1, order)
            if all(
                absolute_trace(
                    multiply(scale, difference, modulus, dimension),
                    modulus,
                    dimension,
                )
                == 1
                for difference in differences
            )
        ]
        if not trace_scales:
            continue

        scale = trace_scales[0]
        label_image = {
            multiply(scale, value, modulus, dimension)
            for value in image
            if value != 0
        }
        label_image.add(multiply(scale, special_value, modulus, dimension))
        histogram = intersection_histogram(label_image, dimension, modulus)
        companion = [
            subiaco_companion_value(z, parameter, dimension, modulus)
            for z in range(order)
        ]
        _, kappa = subiaco_clan_constants(parameter, dimension, modulus)
        companion_secant_ratios = {
            multiply(
                companion[left] ^ companion[right],
                inverse(left ^ right, modulus, dimension),
                modulus,
                dimension,
            )
            for left, right in pairs
        }
        clan_trace_values = {
            absolute_trace(
                multiply(
                    multiply(kappa, slope, modulus, dimension),
                    companion[left] ^ companion[right],
                    modulus,
                    dimension,
                ),
                modulus,
                dimension,
            )
            for left, right in pairs
        }
        return {
            "parameter": parameter,
            "slope": slope,
            "zero_partner": zero_partner,
            "special_value": special_value,
            "trace_scale": scale,
            "trace_scale_count": len(trace_scales),
            "expected_trace_scale": inverse(parameter, modulus, dimension),
            "subiaco_kappa": kappa,
            "companion_secant_ratio_count": len(companion_secant_ratios),
            "companion_secant_ratios": sorted(companion_secant_ratios),
            "clan_trace_values": sorted(clan_trace_values),
            "label_image": sorted(label_image),
            "multiplicative_intersection_histogram": dict(sorted(histogram.items())),
            "proper": len(histogram) > 1,
            "status": "PASS_BRIDGE_CRITERION",
        }

    return {"parameter": parameter, "status": "NO_BRIDGE_SLOPE"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimensions", nargs="+", type=int, default=[4, 6, 8])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cases = []
    for dimension in args.dimensions:
        modulus = MODULI[dimension]
        parameters = admissible_parameters(dimension, modulus)
        analyses = []
        for parameter in parameters:
            result = analyze_parameter(dimension, modulus, parameter)
            analyses.append(result)
        bridge_hits = [
            result
            for result in analyses
            if result["status"] == "PASS_BRIDGE_CRITERION"
        ]
        cases.append(
            {
                "dimension": dimension,
                "field_order": 1 << dimension,
                "modulus": modulus,
                "admissible_parameter_count": len(parameters),
                "tested_parameter_count": len(analyses),
                "bridge_parameter_count": len(bridge_hits),
                "bridge_parameters": [result["parameter"] for result in bridge_hits],
                "first_bridge": bridge_hits[0] if bridge_hits else None,
                "status": (
                    "PASS_FORMULA_SAMPLE"
                    if bridge_hits
                    else "NO_HIT_FORMULA_SAMPLE"
                ),
            }
        )

    payload = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0496-SUBIACO-HYPEROVAL-BRIDGE",
        "purpose": (
            "Test the predeclared Subiaco o-polynomial family against the exact "
            "two-fibre trace and properness criterion; finite samples are not a family proof."
        ),
        "cases": cases,
        "status": (
            "PASS_SAMPLE_HIT"
            if any(case["status"] == "PASS_FORMULA_SAMPLE" for case in cases)
            else "NO_HIT"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
