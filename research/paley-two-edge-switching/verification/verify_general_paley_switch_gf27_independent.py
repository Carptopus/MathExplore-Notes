"""Independent GF(27) audit for the general Paley switch.

Elements are encoded in GF(3)[z]/(z^3+2z+1).  The implementation is local to
this file and imports no project field or array helpers.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path


ORDER = 27


def coefficients(value: int) -> tuple[int, int, int]:
    return value % 3, (value // 3) % 3, (value // 9) % 3


def encode(values: tuple[int, int, int]) -> int:
    return sum((value % 3) * (3**index) for index, value in enumerate(values))


def add(left: int, right: int) -> int:
    return encode(tuple((a + b) % 3 for a, b in zip(coefficients(left), coefficients(right))))


def neg(value: int) -> int:
    return encode(tuple((-entry) % 3 for entry in coefficients(value)))


def sub(left: int, right: int) -> int:
    return add(left, neg(right))


def mul(left: int, right: int) -> int:
    product = [0] * 5
    for left_degree, left_value in enumerate(coefficients(left)):
        for right_degree, right_value in enumerate(coefficients(right)):
            product[left_degree + right_degree] += left_value * right_value
    # z^3 = z + 2 modulo z^3+2z+1.
    for degree in range(4, 2, -1):
        value = product[degree] % 3
        product[degree] = 0
        product[degree - 2] += value
        product[degree - 3] += 2 * value
    return encode(tuple(value % 3 for value in product[:3]))


def power(value: int, exponent: int) -> int:
    result = 1
    factor = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = mul(result, factor)
        factor = mul(factor, factor)
        remaining >>= 1
    return result


def inverse(value: int) -> int:
    if value == 0:
        raise ZeroDivisionError
    return power(value, ORDER - 2)


def chi(value: int) -> int:
    if value == 0:
        return 0
    result = power(value, (ORDER - 1) // 2)
    if result == 1:
        return 1
    if result == neg(1):
        return -1
    raise AssertionError("quadratic character did not return +/-1")


def field_sum(values: list[int] | set[int]) -> int:
    result = 0
    for value in values:
        result = add(result, value)
    return result


def admissible_pairs() -> list[tuple[int, int]]:
    return [
        (alpha, ratio)
        for alpha in range(1, ORDER)
        if chi(alpha) == -1 and chi(add(1, alpha)) == -1
        for ratio in range(1, ORDER)
        if ratio != 1
        and chi(ratio) == 1
        and chi(add(1, mul(alpha, ratio))) == 1
        and chi(add(ratio, alpha)) == 1
    ]


def switched_partner(alpha: int, ratio: int) -> list[int]:
    partner = [0] * ORDER
    for value in range(1, ORDER):
        if chi(value) != 1:
            continue
        other = mul(alpha, value)
        partner[value] = other
        partner[other] = value
    old_edges = ((1, alpha), (ratio, mul(alpha, ratio)))
    for left, right in old_edges:
        if partner[left] != right:
            raise AssertionError("old edge missing")
    for left, right in ((1, mul(alpha, ratio)), (ratio, alpha)):
        partner[left] = right
        partner[right] = left
    return partner


def cubic_sum(alpha: int) -> int:
    total = 0
    for ratio in range(ORDER):
        cubic = mul(mul(ratio, add(1, mul(alpha, ratio))), add(ratio, alpha))
        total += chi(cubic)
    return total


def count_for_alpha(alpha: int) -> int:
    return sum(
        chi(ratio) == 1
        and chi(add(1, mul(alpha, ratio))) == 1
        and chi(add(ratio, alpha)) == 1
        for ratio in range(ORDER)
    )


def construct_array(alpha: int, ratio: int) -> list[list[tuple[int, int]]]:
    partner = switched_partner(alpha, ratio)
    rows = []
    for shift in range(ORDER):
        row = []
        for column in range(ORDER):
            base = sub(column, shift)
            symbol = add(add(base, partner[base]), shift)
            label = 0 if chi(partner[base]) == 1 else 1
            row.append((symbol, label))
        row.append((shift, 0))
        rows.append(row)
    return rows


def audit_array(rows: list[list[tuple[int, int]]]) -> dict[str, object]:
    columns = [[rows[row][column] for row in range(ORDER)] for column in range(ORDER + 1)]
    if any(len(set(row)) != ORDER + 1 for row in rows):
        raise AssertionError("row repetition")
    if any(len(set(column)) != ORDER for column in columns):
        raise AssertionError("column repetition")
    replication = Counter(symbol for row in rows for symbol in row)
    if len(replication) != 2 * ORDER or set(replication.values()) != {14}:
        raise AssertionError("replication failure")
    row_sets = [set(row) for row in rows]
    column_sets = [set(column) for column in columns]
    cc = [len(left & right) for left, right in combinations(column_sets, 2)]
    rc = [len(row & column) for row in row_sets for column in column_sets]
    rr = [len(left & right) for left, right in combinations(row_sets, 2)]
    if set(cc) != {13} or set(rc) != {14} or len(set(rr)) < 2:
        raise AssertionError("CC, RC or proper RR failure")
    return {
        "parameters": {"v": 54, "r": 27, "c": 28, "e": 14, "cc": 13, "rc": 14},
        "rr_spectrum": dict(sorted(Counter(rr).items())),
    }


def main() -> None:
    # Field self-checks include inverses and the stated irreducible modulus model.
    if any(mul(value, inverse(value)) != 1 for value in range(1, ORDER)):
        raise AssertionError("GF(27) inverse self-check failed")
    if len({mul(value, value) for value in range(1, ORDER)}) != 13:
        raise AssertionError("GF(27) square-class size failed")

    alphas = [
        alpha
        for alpha in range(ORDER)
        if chi(alpha) == -1 and chi(add(1, alpha)) == -1
    ]
    if len(alphas) != (ORDER - 3) // 4:
        raise AssertionError("alpha count failed in GF(27)")
    alpha_records = []
    for alpha in alphas:
        observed = count_for_alpha(alpha)
        trace_sum = cubic_sum(alpha)
        predicted_numerator = ORDER - 3 + trace_sum - 4 * chi(sub(alpha, 1))
        if predicted_numerator % 8 or observed != predicted_numerator // 8:
            raise AssertionError("D2.1 failed in GF(27)")
        if abs(trace_sum) > 2 * math.sqrt(ORDER) + 1e-12:
            raise AssertionError("Hasse bound failed in GF(27)")
        alpha_records.append({"alpha": alpha, "T_alpha": trace_sum, "C_alpha": observed})

    pairs = admissible_pairs()
    if not pairs:
        raise AssertionError("GF(27) has no admissible pair")
    alpha, ratio = pairs[0]
    rows = construct_array(alpha, ratio)
    array_audit = audit_array(rows)

    output = {
        "experiment_id": "HSF-SWITCH-0002-D2-GF27-INDEPENDENT",
        "field": "GF(3)[z]/(z^3+2z+1)",
        "alpha_count": len(alphas),
        "admissible_pair_count": len(pairs),
        "first_pair": [alpha, ratio],
        "alpha_records": alpha_records,
        "array_audit": array_audit,
        "claim_boundary": (
            "This closes the first non-prime prime-power implementation check. "
            "It does not replace the general Hasse proof or the novelty audit."
        ),
    }
    output_path = Path(__file__).resolve().parent / "results" / "general-paley-switch-gf27.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
