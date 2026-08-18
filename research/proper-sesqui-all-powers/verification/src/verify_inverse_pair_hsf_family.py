"""Independently verify E0488 certificates without importing the constructor."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def degree(polynomial: int) -> int:
    return polynomial.bit_length() - 1


def remainder(dividend: int, divisor: int) -> int:
    while dividend and degree(dividend) >= degree(divisor):
        dividend ^= divisor << (degree(dividend) - degree(divisor))
    return dividend


def product(left: int, right: int, modulus: int) -> int:
    raw = 0
    while right:
        if right & 1:
            raw ^= left
        left <<= 1
        right >>= 1
    return remainder(raw, modulus)


def reciprocal(value: int, modulus: int, order: int) -> int:
    return next(candidate for candidate in range(1, order) if product(value, candidate, modulus) == 1)


def trace(value: int, modulus: int, dimension: int) -> int:
    total = 0
    item = value
    for _ in range(dimension):
        total ^= item
        item = product(item, item, modulus)
    if total not in (0, 1):
        raise AssertionError("non-binary trace")
    return total


def verify_case(case: dict[str, object]) -> dict[str, object]:
    dimension = int(case["dimension"])
    order = int(case["field_order"])
    modulus = int(case["modulus"])
    array = case.get("array")
    if array is None:
        raise ValueError("independent verification requires --include-array construction output")

    errors = []
    expected_rows = order - 1
    expected_columns = order
    expected_symbols = 2 * (order - 1)
    if len(array) != expected_rows or any(len(row) != expected_columns for row in array):
        errors.append("dimensions")

    symbol_counts = Counter(symbol for row in array for symbol in row)
    if set(symbol_counts) != set(range(expected_symbols)) or set(symbol_counts.values()) != {order // 2}:
        errors.append("replication")
    if any(len(set(row)) != expected_columns for row in array):
        errors.append("row_binary")
    columns = [
        {array[row][column] for row in range(expected_rows)}
        for column in range(expected_columns)
    ]
    if any(len(column) != expected_rows for column in columns):
        errors.append("column_binary")

    formula_mismatches = 0
    for r_index, row in enumerate(array):
        r = r_index + 1
        for c, symbol in enumerate(row):
            x = product(c, r, modulus)
            if x in (0, 1):
                f_value = 1
            else:
                f_value = reciprocal(x ^ reciprocal(x, modulus, order), modulus, order)
            h = product(r, f_value, modulus)
            b = trace(product(c, h, modulus), modulus, dimension)
            formula_mismatches += symbol != 2 * (h - 1) + b
    if formula_mismatches:
        errors.append("formula")

    expected_column_sets = [
        {
            2 * (h - 1) + trace(product(c, h, modulus), modulus, dimension)
            for h in range(1, order)
        }
        for c in range(order)
    ]
    if columns != expected_column_sets:
        errors.append("trace_residual_columns")

    cc = [
        len(columns[left] & columns[right])
        for left in range(order)
        for right in range(left + 1, order)
    ]
    row_sets = [set(row) for row in array]
    rc = [len(row & column) for row in row_sets for column in columns]
    rr = [
        len(row_sets[left] & row_sets[right])
        for left in range(expected_rows)
        for right in range(left + 1, expected_rows)
    ]
    if set(cc) != {order // 2 - 1}:
        errors.append("cc")
    if set(rc) != {order // 2}:
        errors.append("rc")
    should_be_proper = dimension >= 5
    if (len(set(rr)) > 1) != should_be_proper:
        errors.append("proper_boundary")

    traces = [trace(value, modulus, dimension) for value in range(order)]
    kloosterman_sum = sum(
        1 if traces[value ^ reciprocal(value, modulus, order)] == 0 else -1
        for value in range(1, order)
    )
    n00 = (order - 3 + kloosterman_sum) // 4
    n11 = (order + 1 + kloosterman_sum) // 4
    expected_rr_histogram = Counter({
        order // 2 - 2: (order - 1) * (n11 - 1) // 2,
        order // 2: (order - 1) * (order - 1 - kloosterman_sum) // 4,
        order // 2 + 2: (order - 1) * n00 // 2,
    })
    expected_rr_histogram += Counter()
    if +Counter(rr) != +expected_rr_histogram:
        errors.append("kloosterman_rr_histogram")

    return {
        "dimension": dimension,
        "t": order // 2,
        "formula_mismatches": formula_mismatches,
        "cc_histogram": dict(sorted(Counter(cc).items())),
        "rc_histogram": dict(sorted(Counter(rc).items())),
        "rr_histogram": dict(sorted(Counter(rr).items())),
        "binary_kloosterman_sum": kloosterman_sum,
        "kloosterman_rr_histogram": {
            key: count for key, count in sorted(expected_rr_histogram.items()) if count
        },
        "expected_proper": should_be_proper,
        "valid": not errors,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.input.read_text(encoding="utf-8"))
    cases = [verify_case(case) for case in source["cases"]]
    payload = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0488-INVERSE-PAIR-DIRECT-FAMILY-INDEPENDENT",
        "source": args.input.name,
        "cases": cases,
        "status": "PASS" if all(case["valid"] for case in cases) else "FAIL",
        "independence": (
            "Reimplements polynomial reduction, multiplication, reciprocal lookup, trace, "
            "the closed formula, all array margins, the binary Kloosterman count, its exact "
            "RR histogram, and the properness boundary without "
            "importing the constructor or project verification helpers."
        ),
    }
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
