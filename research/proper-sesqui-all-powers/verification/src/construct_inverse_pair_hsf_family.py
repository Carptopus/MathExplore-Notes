"""Construct the inverse-pair finite-field HSF family from the E0488 theorem."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from hsf_core import HSFParameters, analyze_array


DEFAULT_CASES = {
    3: 0b1011,       # x^3 + x + 1
    5: 0b100101,     # x^5 + x^2 + 1
    7: 0b10000011,   # x^7 + x + 1
}


def multiply(left: int, right: int, modulus: int, dimension: int) -> int:
    result = 0
    value = left
    factor = right
    while factor:
        if factor & 1:
            result ^= value
        factor >>= 1
        value <<= 1
        if value & (1 << dimension):
            value ^= modulus
    return result & ((1 << dimension) - 1)


def power(value: int, exponent: int, modulus: int, dimension: int) -> int:
    result = 1
    factor = value
    while exponent:
        if exponent & 1:
            result = multiply(result, factor, modulus, dimension)
        exponent >>= 1
        factor = multiply(factor, factor, modulus, dimension)
    return result


def inverse(value: int, modulus: int, dimension: int) -> int:
    if value == 0:
        raise ZeroDivisionError("zero has no multiplicative inverse")
    return power(value, (1 << dimension) - 2, modulus, dimension)


def absolute_trace(value: int, modulus: int, dimension: int) -> int:
    result = 0
    conjugate = value
    for _ in range(dimension):
        result ^= conjugate
        conjugate = multiply(conjugate, conjugate, modulus, dimension)
    if result not in (0, 1):
        raise ArithmeticError("the supplied modulus does not produce the expected binary trace")
    return result


def inverse_pair_map(value: int, modulus: int, dimension: int) -> int:
    if value in (0, 1):
        return 1
    denominator = multiply(value, value, modulus, dimension) ^ 1
    return multiply(value, inverse(denominator, modulus, dimension), modulus, dimension)


def build_case(dimension: int, modulus: int, include_array: bool) -> dict[str, object]:
    q = 1 << dimension
    t = q // 2
    trace = [absolute_trace(value, modulus, dimension) for value in range(q)]
    f = [inverse_pair_map(value, modulus, dimension) for value in range(q)]
    image = set(f)
    fibres = {value: [x for x, item in enumerate(f) if item == value] for value in image}
    expected_image = {1} | {value for value in range(1, q) if trace[value] == 0}
    g = [multiply(x, f[x], modulus, dimension) for x in range(1, q)]

    array: list[list[int]] = []
    for row_label in range(1, q):
        row = []
        for column_label in range(q):
            x = multiply(column_label, row_label, modulus, dimension)
            group = multiply(row_label, f[x], modulus, dimension)
            pair_bit = trace[multiply(column_label, group, modulus, dimension)]
            row.append(2 * (group - 1) + pair_bit)
        array.append(row)

    expected_columns = [
        {2 * (group - 1) + trace[multiply(column, group, modulus, dimension)] for group in range(1, q)}
        for column in range(q)
    ]
    actual_columns = [
        {array[row][column] for row in range(q - 1)}
        for column in range(q)
    ]
    row_group_sets = [{symbol // 2 + 1 for symbol in row} for row in array]
    row_group_intersections = [
        len(row_group_sets[left] & row_group_sets[right])
        for left in range(q - 1)
        for right in range(left + 1, q - 1)
    ]
    actual_group_histogram = Counter(row_group_intersections)
    ratio_formula = {}
    for ratio in range(2, q):
        predicted = (
            q // 4
            - 1
            + int(trace[ratio] == 0)
            + int(trace[inverse(ratio, modulus, dimension)] == 0)
        )
        ratio_formula[str(predicted)] = ratio_formula.get(str(predicted), 0) + 1

    fibre_pair_trace_ok = all(
        len(points) == 2
        and trace[multiply(points[0] ^ points[1], value, modulus, dimension)] == 1
        for value, points in fibres.items()
    )
    kloosterman_sum = sum(
        1 if trace[value ^ inverse(value, modulus, dimension)] == 0 else -1
        for value in range(1, q)
    )
    n00 = (q - 3 + kloosterman_sum) // 4
    n11 = (q + 1 + kloosterman_sum) // 4
    predicted_group_histogram = Counter({
        q // 4 - 1: (q - 1) * (n11 - 1) // 2,
        q // 4: (q - 1) * (q - 1 - kloosterman_sum) // 4,
        q // 4 + 1: (q - 1) * n00 // 2,
    })
    predicted_group_histogram += Counter()
    verification = analyze_array(HSFParameters(t), array)
    payload: dict[str, object] = {
        "dimension": dimension,
        "field_order": q,
        "modulus": modulus,
        "t": t,
        "inverse_pair_image": sorted(image),
        "inverse_pair_image_is_trace_zero_nonzero_plus_one": image == expected_image,
        "all_fibres_have_size_two": set(map(len, fibres.values())) == {2},
        "all_fibre_pair_traces_are_one": fibre_pair_trace_ok,
        "x_times_f_is_a_permutation_of_nonzero_field": set(g) == set(range(1, q)),
        "columns_equal_trace_sylvester_residual_blocks": actual_columns == expected_columns,
        "row_group_intersection_histogram": {
            str(value): count
            for value, count in sorted(actual_group_histogram.items())
        },
        "ratio_formula_histogram_excluding_identity": ratio_formula,
        "binary_kloosterman_sum": kloosterman_sum,
        "trace_inverse_counts": {"00": n00, "11": n11},
        "kloosterman_rr_histogram": {
            str(value): count
            for value, count in sorted(predicted_group_histogram.items())
            if count
        },
        "kloosterman_rr_histogram_matches_rows": (
            +predicted_group_histogram == +actual_group_histogram
        ),
        "verification": verification,
    }
    if include_array:
        payload["array"] = array
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimensions", type=int, nargs="+", default=[3, 5, 7])
    parser.add_argument("--include-array", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    missing = sorted(set(args.dimensions) - set(DEFAULT_CASES))
    if missing:
        raise ValueError(f"no audited irreducible modulus registered for dimensions {missing}")
    cases = [
        build_case(dimension, DEFAULT_CASES[dimension], args.include_array)
        for dimension in args.dimensions
    ]
    payload = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0488-INVERSE-PAIR-DIRECT-FAMILY",
        "formula": (
            "For q=2^d with odd d, f(0)=f(1)=1 and "
            "f(x)=1/(x+x^-1) otherwise; row r and column c receive group "
            "h=r*f(c*r) and pair bit Tr(c*h)."
        ),
        "cases": cases,
        "status": (
            "PASS_PROPER_FOR_ALL_TESTED_D_GE_5_AND_TRIPLE_BOUNDARY_D3"
            if all(
                case["verification"]["valid"] == (case["dimension"] >= 5)
                and all(
                    case[key]
                    for key in (
                        "inverse_pair_image_is_trace_zero_nonzero_plus_one",
                        "all_fibres_have_size_two",
                        "all_fibre_pair_traces_are_one",
                        "x_times_f_is_a_permutation_of_nonzero_field",
                        "columns_equal_trace_sylvester_residual_blocks",
                        "kloosterman_rr_histogram_matches_rows",
                    )
                )
                for case in cases
            )
            else "FAIL"
        ),
        "claim_boundary": (
            "The finite cases are regression evidence only. General existence follows only from "
            "the symbolic inverse-pair, permutation, margin, and Kloosterman-bound proof."
        ),
    }
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({
        "status": payload["status"],
        "cases": [
            {
                "d": case["dimension"],
                "t": case["t"],
                "valid": case["verification"]["valid"],
                "errors": case["verification"]["errors"],
                "rr_groups": case["row_group_intersection_histogram"],
            }
            for case in cases
        ],
    }, ensure_ascii=False))
    return 0 if payload["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
