"""Independently verify the frozen q=11 Youden-completion certificate.

This verifier does not import the inverse-completion solver, the published
constructor, or HSF modules. It reconstructs the q=11, alpha=7, r=5 switched
array directly from the cell formula, checks the completed Youden rectangle,
applies the deletion transformation from the definition, compares both arrays
with the frozen certificate, and rejects a deliberately corrupted rectangle.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path


RESULT_DIR = Path(__file__).resolve().parent / "results"


def quadratic_character(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    return 1 if pow(value, (prime - 1) // 2, prime) == 1 else -1


def reconstruct_switched_array() -> list[list[int]]:
    """Rebuild the manuscript's q=11, alpha=7, r=5 array cell by cell."""
    prime, alpha, ratio = 11, 7, 5
    squares = {
        value
        for value in range(1, prime)
        if quadratic_character(value, prime) == 1
    }
    partner = [0] * prime
    for value in squares:
        other = alpha * value % prime
        partner[value] = other
        partner[other] = value

    old_edges = ((1, alpha % prime), (ratio, alpha * ratio % prime))
    new_edges = ((1, alpha * ratio % prime), (ratio, alpha % prime))
    for left, right in old_edges:
        if partner[left] != right or partner[right] != left:
            raise AssertionError("the prescribed Paley edge is absent")
    for left, right in new_edges:
        partner[left] = right
        partner[right] = left

    array: list[list[int]] = []
    for shift in range(prime):
        row: list[int] = []
        for column in range(prime):
            base = (column - shift) % prime
            symbol = (base + partner[base] + shift) % prime
            label = 0 if quadratic_character(partner[base], prime) == 1 else 1
            row.append(2 * symbol + label)
        row.append(2 * shift)
        array.append(row)
    return array


def verify_youden(rectangle: list[list[int]]) -> list[str]:
    errors: list[str] = []
    if len(rectangle) != 11 or any(len(row) != 23 for row in rectangle):
        return ["dimensions"]
    universe = set(range(23))
    if any(set(row) != universe for row in rectangle):
        errors.append("row permutation")
    columns = [set(rectangle[row][column] for row in range(11)) for column in range(23)]
    if any(len(column) != 11 for column in columns):
        errors.append("column binary")
    intersections = {
        len(columns[left] & columns[right])
        for left, right in combinations(range(23), 2)
    }
    if intersections != {5}:
        errors.append("column design")
    replication = Counter(value for row in rectangle for value in row)
    if set(replication) != universe or set(replication.values()) != {11}:
        errors.append("symbol replication")
    return errors


def delete_and_exchange(rectangle: list[list[int]], deleted: int) -> list[list[int]]:
    removed = {rectangle[row][deleted] for row in range(11)}
    surviving_symbols = sorted(set(range(23)) - removed)
    surviving_symbol_index = {
        symbol: index for index, symbol in enumerate(surviving_symbols)
    }
    surviving_columns = [column for column in range(23) if column != deleted]
    treatment_index = {
        column: index for index, column in enumerate(surviving_columns)
    }
    array = [[-1] * 12 for _ in range(11)]
    for row in range(11):
        for old_column in surviving_columns:
            symbol = rectangle[row][old_column]
            if symbol not in removed:
                target_column = surviving_symbol_index[symbol]
                if array[row][target_column] != -1:
                    raise AssertionError("two surviving cells map to one output cell")
                array[row][target_column] = treatment_index[old_column]
    if any(value < 0 for row in array for value in row):
        raise AssertionError("deletion left an empty output cell")
    return array


def verify_target(array: list[list[int]]) -> dict[str, object]:
    errors: list[str] = []
    if len(array) != 11 or any(len(row) != 12 for row in array):
        return {"errors": ["dimensions"]}
    rows = list(map(set, array))
    columns = [set(array[row][column] for row in range(11)) for column in range(12)]
    if any(len(row) != 12 for row in rows):
        errors.append("row binary")
    if any(len(column) != 11 for column in columns):
        errors.append("column binary")
    replication = Counter(value for row in array for value in row)
    if set(replication) != set(range(22)) or set(replication.values()) != {6}:
        errors.append("replication")
    cc = {
        len(columns[left] & columns[right])
        for left, right in combinations(range(12), 2)
    }
    rc = {
        len(rows[row] & columns[column])
        for row in range(11)
        for column in range(12)
    }
    rr = Counter(
        len(rows[left] & rows[right]) for left, right in combinations(range(11), 2)
    )
    if cc != {5}:
        errors.append("CC")
    if rc != {6}:
        errors.append("RC")
    if len(rr) < 2:
        errors.append("not proper")
    return {
        "errors": errors,
        "replication_values": sorted(set(replication.values())),
        "cc_values": sorted(cc),
        "rc_values": sorted(rc),
        "rr_spectrum": dict(sorted(rr.items())),
    }


def main() -> int:
    completion = json.loads(
        (RESULT_DIR / "audit-paley-switch-q11-youden-completion.json").read_text(
            encoding="utf-8"
        )
    )
    certificate = json.loads(
        (RESULT_DIR / "audit-paley-switch-q11-certificate.json").read_text(
            encoding="utf-8"
        )
    )
    rectangle = completion["youden_rectangle"]
    youden_errors = verify_youden(rectangle)
    recovered = delete_and_exchange(rectangle, 22)
    reconstructed = reconstruct_switched_array()
    formula_match = reconstructed == certificate["array"]
    roundtrip = recovered == reconstructed == certificate["array"]
    target = verify_target(recovered)

    corrupted = [row[:] for row in rectangle]
    corrupted[0][0] = corrupted[0][1]
    negative_control_detected = bool(verify_youden(corrupted))

    if (
        youden_errors
        or not formula_match
        or not roundtrip
        or target["errors"]
        or not negative_control_detected
    ):
        raise AssertionError("independent q=11 certificate audit failed")

    payload = {
        "experiment_id": "HSF-AUDIT-0003-E03-Q11-YOUDEN-INDEPENDENT",
        "checks": {
            "youden_11_by_23": True,
            "symmetric_2_23_11_5_column_design": True,
            "q11_alpha7_r5_cell_formula_matches_certificate": True,
            "delete_column_22_and_exchange_matches_formula": True,
            "proper_transposed_sesqui_22_6_5_6_11_by_12": True,
            "controlled_corruption_detected": True,
        },
        "target": target,
        "claim_boundary": (
            "This independently verifies one q=11 completion certificate. It does not "
            "prove that every switched array is Youden-completable or establish priority."
        ),
        "status": "PASS_Q11_COMPLETION_CERTIFICATE",
    }
    output = RESULT_DIR / "audit-paley-switch-q11-youden-independent.json"
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
