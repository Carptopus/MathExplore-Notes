"""Finite regression for the parameter-independent Subiaco bridge reductions.

The d=4,6,8 cases only verify formulas and catch implementation mistakes.  They
are not used as proof of the open joint-existence lemma in HSF-E0496.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from analyze_subiaco_hyperoval_bridge import (
    MODULI,
    absolute_trace,
    admissible_parameters,
    fibre_pairs,
    inverse,
    multiply,
    power,
    subiaco_clan_constants,
    subiaco_companion_value,
    subiaco_value,
)


def xor_sum(values: object) -> int:
    result = 0
    for value in values:  # type: ignore[union-attr]
        result ^= int(value)
    return result


def shifted_image(image: set[int], shift: int) -> set[int]:
    return {value ^ shift for value in image}


def trace_pair_ok(
    pairs: list[tuple[int, int]],
    scale: int,
    dimension: int,
    modulus: int,
) -> bool:
    return all(
        absolute_trace(
            multiply(scale, left ^ right, modulus, dimension),
            modulus,
            dimension,
        )
        == 1
        for left, right in pairs
    )


def verify_bridge_map(
    values: list[int],
    slope: int,
    scale: int,
    anchor_pair: tuple[int, int],
    dimension: int,
    modulus: int,
) -> dict[str, object]:
    order = 1 << dimension
    anchor, partner = anchor_pair
    base = values[anchor]
    difference = anchor ^ partner
    special_label_unscaled = multiply(slope, difference, modulus, dimension)
    special_label = multiply(scale, special_label_unscaled, modulus, dimension)
    slope_inverse = inverse(slope, modulus, dimension)

    labels_by_input: dict[int, int] = {
        0: special_label,
        slope_inverse: special_label,
    }
    for point in range(order):
        if point in anchor_pair:
            continue
        translated_value = values[point] ^ base
        coordinate = multiply(
            point ^ anchor,
            inverse(translated_value, modulus, dimension),
            modulus,
            dimension,
        )
        label = multiply(scale, translated_value, modulus, dimension)
        if coordinate in labels_by_input:
            raise AssertionError("bridge coordinate collision")
        labels_by_input[coordinate] = label

    label_fibres: dict[int, list[int]] = defaultdict(list)
    outputs = []
    for coordinate, label in labels_by_input.items():
        label_fibres[label].append(coordinate)
        outputs.append(multiply(coordinate, label, modulus, dimension))

    trace_ok = all(
        len(points) == 2
        and absolute_trace(
            multiply(label, points[0] ^ points[1], modulus, dimension),
            modulus,
            dimension,
        )
        == 1
        for label, points in label_fibres.items()
    )
    return {
        "domain_complete": sorted(labels_by_input) == list(range(order)),
        "two_to_one": len(label_fibres) == order // 2
        and all(len(points) == 2 for points in label_fibres.values()),
        "product_permutation": sorted(outputs) == list(range(order)),
        "fibre_trace": trace_ok,
        "label_count": len(label_fibres),
    }


def analyze_parameter(
    dimension: int,
    modulus: int,
    parameter: int,
) -> dict[str, object]:
    order = 1 << dimension
    parameter_squared = multiply(parameter, parameter, modulus, dimension)
    slope = 1 ^ parameter ^ parameter_squared
    trace_scale = inverse(parameter, modulus, dimension)

    oval = [
        subiaco_value(point, parameter, dimension, modulus)
        for point in range(order)
    ]
    companion = [
        subiaco_companion_value(point, parameter, dimension, modulus)
        for point in range(order)
    ]
    binomial = [
        oval[point] ^ multiply(slope, point, modulus, dimension)
        for point in range(order)
    ]
    pairs = fibre_pairs(binomial)
    if pairs is None:
        raise AssertionError("Subiaco main map is not two-to-one")

    _, kappa = subiaco_clan_constants(parameter, dimension, modulus)
    companion_slope = multiply(
        slope,
        inverse(kappa, modulus, dimension),
        modulus,
        dimension,
    )
    companion_binomial = [
        companion[point]
        ^ multiply(companion_slope, point, modulus, dimension)
        for point in range(order)
    ]
    companion_pairs = fibre_pairs(companion_binomial)
    if companion_pairs is None:
        raise AssertionError("Subiaco companion map is not two-to-one")

    image = set(binomial)
    expected_image_sum = multiply(parameter, slope, modulus, dimension)
    actual_image_sum = xor_sum(image)
    good_fibres: list[dict[str, object]] = []
    for left, right in pairs:
        base = binomial[left]
        difference = left ^ right
        special = multiply(slope, difference, modulus, dimension)
        translated = shifted_image(image, base)
        if special in translated:
            continue
        unscaled_labels = (translated - {0}) | {special}
        first_power_sum = xor_sum(unscaled_labels)
        inverse_power_sum = xor_sum(
            inverse(label, modulus, dimension) for label in unscaled_labels
        )
        third_power_sum = xor_sum(
            power(label, 3, modulus, dimension) for label in unscaled_labels
        )
        inverse_third_power_sum = xor_sum(
            power(inverse(label, modulus, dimension), 3, modulus, dimension)
            for label in unscaled_labels
        )
        certificate_exponent = None
        if first_power_sum and inverse_power_sum:
            certificate_exponent = 1
        elif third_power_sum and inverse_third_power_sum:
            certificate_exponent = 3
        good_fibres.append(
            {
                "pair": [left, right],
                "base": base,
                "difference": difference,
                "special": special,
                "first_power_sum": first_power_sum,
                "inverse_power_sum": inverse_power_sum,
                "j1_proper_certificate": bool(
                    first_power_sum and inverse_power_sum
                ),
                "third_power_sum": third_power_sum,
                "inverse_third_power_sum": inverse_third_power_sum,
                "power_sum_certificate_exponent": certificate_exponent,
            }
        )

    certified = [
        fibre for fibre in good_fibres if fibre["j1_proper_certificate"]
    ]
    power_sum_certified = [
        fibre
        for fibre in good_fibres
        if fibre["power_sum_certificate_exponent"] is not None
    ]
    bridge_check = None
    if certified:
        bridge_check = verify_bridge_map(
            binomial,
            slope,
            trace_scale,
            tuple(certified[0]["pair"]),  # type: ignore[arg-type]
            dimension,
            modulus,
        )

    expected_first_power_sums = all(
        fibre["first_power_sum"]
        == multiply(
            slope,
            parameter ^ int(fibre["difference"]),
            modulus,
            dimension,
        )
        for fibre in good_fibres
    )
    status = (
        actual_image_sum == expected_image_sum
        and trace_pair_ok(pairs, trace_scale, dimension, modulus)
        and trace_pair_ok(
            companion_pairs,
            trace_scale,
            dimension,
            modulus,
        )
        and expected_first_power_sums
        and bool(certified)
        and len(power_sum_certified) == len(good_fibres)
        and bridge_check is not None
        and all(bool(value) for key, value in bridge_check.items() if key != "label_count")
    )
    return {
        "parameter": parameter,
        "main_trace_identity": trace_pair_ok(
            pairs, trace_scale, dimension, modulus
        ),
        "companion_trace_identity": trace_pair_ok(
            companion_pairs, trace_scale, dimension, modulus
        ),
        "image_sum": actual_image_sum,
        "expected_image_sum": expected_image_sum,
        "image_sum_identity": actual_image_sum == expected_image_sum,
        "good_fibre_count": len(good_fibres),
        "j1_certified_good_fibre_count": len(certified),
        "inverse_sum_zero_good_fibre_count": len(good_fibres) - len(certified),
        "j3_rescued_good_fibre_count": sum(
            fibre["power_sum_certificate_exponent"] == 3
            for fibre in good_fibres
        ),
        "power_sum_uncertified_good_fibre_count": (
            len(good_fibres) - len(power_sum_certified)
        ),
        "first_certified_fibre": certified[0] if certified else None,
        "bridge_check": bridge_check,
        "status": "PASS_FORMULA_REGRESSION" if status else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimensions", nargs="+", type=int, default=[4, 6, 8])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cases = []
    for dimension in args.dimensions:
        modulus = MODULI[dimension]
        analyses = [
            analyze_parameter(dimension, modulus, parameter)
            for parameter in admissible_parameters(dimension, modulus)
        ]
        cases.append(
            {
                "dimension": dimension,
                "field_order": 1 << dimension,
                "modulus": modulus,
                "admissible_parameter_count": len(analyses),
                "pass_count": sum(
                    result["status"] == "PASS_FORMULA_REGRESSION"
                    for result in analyses
                ),
                "minimum_good_fibre_count": min(
                    int(result["good_fibre_count"]) for result in analyses
                ),
                "minimum_j1_certified_good_fibre_count": min(
                    int(result["j1_certified_good_fibre_count"])
                    for result in analyses
                ),
                "inverse_sum_zero_good_fibre_histogram": dict(
                    sorted(
                        Counter(
                            int(result["inverse_sum_zero_good_fibre_count"])
                            for result in analyses
                        ).items()
                    )
                ),
                "total_j3_rescued_good_fibre_count": sum(
                    int(result["j3_rescued_good_fibre_count"])
                    for result in analyses
                ),
                "maximum_power_sum_uncertified_good_fibre_count": max(
                    int(result["power_sum_uncertified_good_fibre_count"])
                    for result in analyses
                ),
                "first_parameter": analyses[0] if analyses else None,
                "status": (
                    "PASS_FORMULA_REGRESSION"
                    if all(
                        result["status"] == "PASS_FORMULA_REGRESSION"
                        for result in analyses
                    )
                    else "FAIL"
                ),
            }
        )

    payload = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0496-SUBIACO-GENERAL-REDUCTIONS",
        "claim_boundary": (
            "Finite d=4,6,8 regression only.  The all-even-dimensional joint "
            "existence lemma remains open."
        ),
        "cases": cases,
        "status": (
            "PASS_FORMULA_REGRESSION"
            if all(case["status"] == "PASS_FORMULA_REGRESSION" for case in cases)
            else "FAIL"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["status"] == "PASS_FORMULA_REGRESSION" else 1


if __name__ == "__main__":
    raise SystemExit(main())
