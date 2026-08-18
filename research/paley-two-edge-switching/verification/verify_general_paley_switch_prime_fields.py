"""Prime-field calibration of the conditional general Paley switch.

The script imports neither the Loop C constructor nor the symbolic verifier.  It
enumerates every admissible (alpha, r) pair for a small frozen prime set, checks
the switched involution and row-block identities for every pair, and performs a
direct cell-by-cell array audit for one deterministic witness per prime.

The finite scan is a regression test only.  It does not prove existence for an
infinite family or establish novelty.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path


PRIMES = (7, 11, 19, 23, 31, 43, 47, 59)


def quadratic_character(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    residue = pow(value, (prime - 1) // 2, prime)
    if residue == 1:
        return 1
    if residue == prime - 1:
        return -1
    raise AssertionError("Euler criterion did not return +/-1")


def admissible_pairs(prime: int) -> list[tuple[int, int]]:
    result = []
    for alpha in range(1, prime):
        if quadratic_character(alpha, prime) != -1:
            continue
        if quadratic_character(1 + alpha, prime) != -1:
            continue
        for ratio in range(2, prime):
            if quadratic_character(ratio, prime) != 1:
                continue
            if quadratic_character(1 + alpha * ratio, prime) != 1:
                continue
            if quadratic_character(ratio + alpha, prime) != 1:
                continue
            result.append((alpha, ratio))
    return result


def switched_involution(prime: int, alpha: int, ratio: int) -> list[int]:
    squares = {
        value for value in range(1, prime) if quadratic_character(value, prime) == 1
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
            raise AssertionError("requested old edge is absent")
    for left, right in new_edges:
        partner[left] = right
        partner[right] = left
    return partner


def moment_defect(block: set[int], prime: int) -> int:
    size = len(block) % prime
    first = sum(block) % prime
    second = sum(value * value for value in block) % prime
    return (size * second - first * first) % prime


def direct_difference_histogram(block: set[int], prime: int) -> Counter[int]:
    return Counter(
        (left - right) % prime
        for left in block
        for right in block
        if left != right
    )


def audit_pair(prime: int, alpha: int, ratio: int) -> dict[str, object]:
    partner = switched_involution(prime, alpha, ratio)
    if any(partner[partner[value]] != value for value in range(prime)):
        raise AssertionError("switched map is not an involution")
    if sorted(partner) != list(range(prime)):
        raise AssertionError("switched map is not a permutation")

    fibres: dict[int, list[int]] = {}
    for value in range(prime):
        edge_sum = (value + partner[value]) % prime
        fibres.setdefault(edge_sum, []).append(value)
    if sorted(len(fibre) for fibre in fibres.values()) != [1] + [2] * ((prime - 1) // 2):
        raise AssertionError("edge-sum map does not have one singleton and two-point fibres")
    if fibres.get(0) != [0]:
        raise AssertionError("zero is not the unique singleton fibre")
    for edge_sum, fibre in fibres.items():
        if edge_sum == 0:
            continue
        if sorted(quadratic_character(value, prime) for value in fibre) != [-1, 1]:
            raise AssertionError("a nonzero fibre does not cross square classes")

    block = set(fibres)
    expected_block = {
        0,
        *(
            value
            for value in range(1, prime)
            if quadratic_character(value, prime) == -1
        ),
    }
    expected_block.remove((1 + alpha) % prime)
    expected_block.remove((ratio * (1 + alpha)) % prime)
    expected_block.add((1 + alpha * ratio) % prime)
    expected_block.add((ratio + alpha) % prime)
    if block != expected_block:
        raise AssertionError("edge-sum image is not the predicted two-element replacement")

    defect = moment_defect(block, prime)
    predicted_defect = (-alpha * (ratio - 1) * (ratio - 1)) % prime
    if defect != predicted_defect or defect == 0:
        raise AssertionError("moment defect is wrong or zero")

    histogram = direct_difference_histogram(block, prime)
    nonzero_counts = {histogram[value] for value in range(1, prime)}
    if len(nonzero_counts) == 1:
        raise AssertionError("switched block remained a difference set")
    return {
        "alpha": alpha,
        "r": ratio,
        "block": sorted(block),
        "moment_defect": defect,
        "difference_multiplicities": sorted(nonzero_counts),
    }


def construct_array(prime: int, alpha: int, ratio: int) -> list[list[tuple[int, int]]]:
    partner = switched_involution(prime, alpha, ratio)
    rows: list[list[tuple[int, int]]] = []
    for shift in range(prime):
        row = []
        for column in range(prime):
            base = (column - shift) % prime
            symbol = (base + partner[base] + shift) % prime
            label = 0 if quadratic_character(partner[base], prime) == 1 else 1
            row.append((symbol, label))
        row.append((shift, 0))
        rows.append(row)
    return rows


def constant_value(values: list[int], label: str) -> int:
    distinct = set(values)
    if len(distinct) != 1:
        raise AssertionError(f"{label} is not constant: {sorted(distinct)}")
    return next(iter(distinct))


def audit_array(prime: int, rows: list[list[tuple[int, int]]]) -> dict[str, object]:
    row_count = prime
    column_count = prime + 1
    treatment_count = 2 * prime
    replication = (prime + 1) // 2

    if len(rows) != row_count or any(len(row) != column_count for row in rows):
        raise AssertionError("array dimensions are wrong")
    if any(len(set(row)) != column_count for row in rows):
        raise AssertionError("a row repeats a symbol")

    columns = [[rows[row][column] for row in range(row_count)] for column in range(column_count)]
    if any(len(set(column)) != row_count for column in columns):
        raise AssertionError("a column repeats a symbol")

    occurrences = Counter(symbol for row in rows for symbol in row)
    if len(occurrences) != treatment_count or set(occurrences.values()) != {replication}:
        raise AssertionError("replication is wrong")

    row_supports = [set(row) for row in rows]
    column_supports = [set(column) for column in columns]
    cc_values = [
        len(column_supports[left] & column_supports[right])
        for left, right in combinations(range(column_count), 2)
    ]
    rc_values = [
        len(row_supports[row] & column_supports[column])
        for row in range(row_count)
        for column in range(column_count)
    ]
    rr_values = [
        len(row_supports[left] & row_supports[right])
        for left, right in combinations(range(row_count), 2)
    ]
    cc = constant_value(cc_values, "CC")
    rc = constant_value(rc_values, "RC")
    if cc != (prime - 1) // 2 or rc != replication:
        raise AssertionError("CC or RC has the wrong value")
    if len(set(rr_values)) < 2:
        raise AssertionError("RR is constant")
    return {
        "v": treatment_count,
        "r": row_count,
        "c": column_count,
        "e": replication,
        "lambda_cc": cc,
        "lambda_rc": rc,
        "rr_spectrum": dict(sorted(Counter(rr_values).items())),
    }


def main() -> None:
    records = []
    for prime in PRIMES:
        pairs = admissible_pairs(prime)
        pair_audits = [audit_pair(prime, alpha, ratio) for alpha, ratio in pairs]
        array_audit = None
        if pairs:
            alpha, ratio = pairs[0]
            array_audit = audit_array(prime, construct_array(prime, alpha, ratio))
        records.append(
            {
                "q": prime,
                "q_mod_24": prime % 24,
                "admissible_pair_count": len(pairs),
                "first_pair": list(pairs[0]) if pairs else None,
                "all_pair_identities_passed": len(pair_audits) == len(pairs),
                "array_audit": array_audit,
            }
        )

    output = {
        "experiment_id": "HSF-SWITCH-0002-D1-PRIME-CALIBRATION",
        "records": records,
        "claim_boundary": (
            "The frozen prime scan calibrates the conditional lemma and exhibits "
            "cases outside 19 mod 24. It is not an infinite-family proof and says "
            "nothing about unscanned prime powers or novelty."
        ),
    }
    output_path = Path(__file__).resolve().parent / "results" / "general-paley-switch-primes.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
