"""Independent exact verifier for the F_2^4 compatible-order classification.

Unlike the discovery search, this verifier never canonicalises coordinates in
a hyperplane.  It represents an ordered Fano plane solely by the seven triples
of positions whose vectors sum to zero, then checks those line-position masks
on every hyperplane prefix.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


def parity(value: int) -> int:
    return value.bit_count() % 2


def rank(vectors: tuple[int, ...]) -> int:
    rows = list(vectors)
    result = 0
    for bit in reversed(range(4)):
        pivot = next((i for i in range(result, len(rows)) if rows[i] & (1 << bit)), None)
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        for i in range(len(rows)):
            if i != result and rows[i] & (1 << bit):
                rows[i] ^= rows[result]
        result += 1
    return result


def line_code(sequence: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (i, j, k)
        for i in range(len(sequence))
        for j in range(i + 1, len(sequence))
        for k in range(j + 1, len(sequence))
        if sequence[i] ^ sequence[j] ^ sequence[k] == 0
    )


def all_fano_codes() -> tuple[tuple[tuple[int, int, int], ...], ...]:
    codes = {line_code(sequence) for sequence in itertools.permutations(range(1, 8))}
    assert len(codes) == 30
    assert all(len(code) == 7 for code in codes)
    return tuple(sorted(codes))


HYPERPLANES = tuple(
    frozenset(x for x in range(1, 16) if parity(a & x) == 0)
    for a in range(1, 16)
)


def classify(code: tuple[tuple[int, int, int], ...]) -> tuple[list[tuple[int, ...]], int]:
    target_prefixes = [
        tuple(triple for triple in code if triple[2] < length)
        for length in range(8)
    ]
    containing = [
        tuple(i for i, hyperplane in enumerate(HYPERPLANES) if x in hyperplane)
        for x in range(16)
    ]
    induced: list[tuple[int, ...]] = [tuple() for _ in HYPERPLANES]
    solutions: list[tuple[int, ...]] = []
    nodes = 0

    def visit(order: tuple[int, ...], remaining: frozenset[int], current_rank: int) -> None:
        nonlocal nodes
        nodes += 1
        if not remaining:
            solutions.append(order)
            return
        candidates = sorted(x for x in remaining if x < (1 << current_rank))
        if current_rank < 4 and (1 << current_rank) in remaining:
            candidates.append(1 << current_rank)
        for x in candidates:
            changed = []
            valid = True
            for index in containing[x]:
                old = induced[index]
                new = old + (x,)
                changed.append((index, old))
                induced[index] = new
                if line_code(new) != target_prefixes[len(new)]:
                    valid = False
                    break
            if valid:
                visit(
                    order + (x,),
                    remaining - {x},
                    current_rank + int(current_rank < 4 and x == (1 << current_rank)),
                )
            for index, old in reversed(changed):
                induced[index] = old

    visit(tuple(), frozenset(range(1, 16)), 0)
    return solutions, nodes


def canonicalise(sequence: tuple[int, ...]) -> tuple[int, ...]:
    basis: list[int] = []
    for value in sequence:
        if rank(tuple(basis + [value])) > len(basis):
            basis.append(value)
            if len(basis) == 4:
                break
    result = []
    for value in sequence:
        for mask in range(16):
            total = 0
            for i, vector in enumerate(basis):
                if mask & (1 << i):
                    total ^= vector
            if total == value:
                result.append(mask)
                break
        else:
            raise AssertionError("coordinate reconstruction failed")
    return tuple(result)


def main() -> None:
    records = []
    solutions = []
    for code in all_fano_codes():
        found, nodes = classify(code)
        records.append(
            {
                "line_position_code": [list(triple) for triple in code],
                "solution_count": len(found),
                "nodes": nodes,
                "solutions": [list(item) for item in found],
            }
        )
        solutions.extend(found)

    ascending = tuple(range(1, 16))
    layer_reversed = tuple(
        value
        for leading in range(4)
        for value in range((1 << (leading + 1)) - 1, (1 << leading) - 1, -1)
    )
    expected = {
        canonicalise(ascending),
        canonicalise(layer_reversed),
        canonicalise(tuple(reversed(ascending))),
        canonicalise(tuple(reversed(layer_reversed))),
    }
    assert set(solutions) == expected
    assert len(solutions) == 4

    result = {
        "method": "independent Fano line-position-prefix DFS",
        "fano_line_codes": 30,
        "canonical_gl4_orbit_count": len(solutions),
        "solutions": [list(item) for item in sorted(solutions)],
        "records": records,
    }
    target = Path(__file__).parent / "results" / "binary-compatible-n4-independent.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, indent=2))


if __name__ == "__main__":
    main()
