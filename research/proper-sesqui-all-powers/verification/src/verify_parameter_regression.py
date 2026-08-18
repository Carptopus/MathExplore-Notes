"""Independent incidence-matrix verification for parameterised HSF(t) regression artifacts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


def histogram(values: list[int]) -> dict[str, int]:
    return {str(key): count for key, count in sorted(Counter(values).items())}


def verify_case(case: dict[str, object], expected_t: int) -> dict[str, object]:
    construction = case["construction"]
    array = construction["array"]
    blocks = [set(block) for block in construction["residual_blocks"]]
    t = expected_t
    rows = 2 * t - 1
    columns = 2 * t
    symbols = 4 * t - 2
    errors: list[str] = []
    if len(array) != rows or any(len(row) != columns for row in array):
        errors.append("dimensions disagree")
        return {"valid": False, "errors": errors}
    row_vectors = [[0] * symbols for _ in range(rows)]
    column_vectors = [[0] * symbols for _ in range(columns)]
    for row in range(rows):
        for column in range(columns):
            symbol = array[row][column]
            if not 0 <= symbol < symbols:
                errors.append("symbol outside range")
                continue
            row_vectors[row][symbol] += 1
            column_vectors[column][symbol] += 1
    if any(value not in (0, 1) for vector in row_vectors + column_vectors for value in vector):
        errors.append("row or column repeats a symbol")
    replication = [sum(vector[symbol] for vector in column_vectors) for symbol in range(symbols)]
    if replication != [t] * symbols:
        errors.append("replication disagrees")
    dot = lambda left, right: sum(a * b for a, b in zip(left, right))
    cc = [dot(left, right) for left, right in combinations(column_vectors, 2)]
    rc = [dot(row, column) for row in row_vectors for column in column_vectors]
    rr = [dot(left, right) for left, right in combinations(row_vectors, 2)]
    if cc != [t - 1] * len(cc):
        errors.append("CC disagrees")
    if rc != [t] * len(rc):
        errors.append("RC disagrees")
    if len(set(rr)) == 1:
        errors.append("RR is constant")
    symbol_supports = [
        {column for row in range(rows) for column in range(columns) if array[row][column] == symbol}
        for symbol in range(symbols)
    ]
    if symbol_supports != blocks:
        errors.append("array symbol supports do not return the residual design")
    return {
        "valid": not errors,
        "errors": errors,
        "t": t,
        "cc_histogram": histogram(cc),
        "rc_histogram": histogram(rc),
        "rr_histogram": histogram(rr),
        "residual_support_roundtrip": symbol_supports == blocks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    t4 = verify_case(payload["t4"], 4)
    t5 = verify_case(payload["t5"], 5)
    t5_classes = {
        class_id: verify_case({"construction": construction}, 5)
        for class_id, construction in payload["t5"]["feasible_class_regressions"].items()
    }
    result = {
        "valid": t4["valid"] and t5["valid"] and all(item["valid"] for item in t5_classes.values()),
        "t4": t4,
        "t5_primary": t5,
        "t5_feasible_classes": t5_classes,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
