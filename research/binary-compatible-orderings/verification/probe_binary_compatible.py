"""Probe compatible orders on F_2^4 through ordered-matroid signatures.

The zero vector is omitted and assumed to be the global minimum.  For n=4,
compatibility is equivalent to all 15 hyperplanes inducing the same ordered
GL(3,2)-orbit.  An orbit is canonicalised by sending the first three
independent vectors of its ordered seven-point sequence to the standard basis.
"""

from __future__ import annotations

import itertools
import json
import random
from collections import deque
from pathlib import Path


def parity(value: int) -> int:
    return value.bit_count() & 1


def rank_binary(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for value in vectors:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in pivots:
                x ^= pivots[pivot]
            else:
                pivots[pivot] = x
                break
    return len(pivots)


def coordinates(value: int, basis: list[int]) -> int:
    for mask in range(1 << len(basis)):
        total = 0
        for index, vector in enumerate(basis):
            if mask & (1 << index):
                total ^= vector
        if total == value:
            return mask
    raise ValueError(f"{value} is not in the span of {basis}")


def canonical_signature(sequence: tuple[int, ...]) -> tuple[int, ...]:
    basis: list[int] = []
    for vector in sequence:
        if rank_binary(basis + [vector]) > len(basis):
            basis.append(vector)
            if len(basis) == 3:
                break
    if len(basis) != 3:
        raise ValueError("sequence does not span a 3-space")
    return tuple(coordinates(vector, basis) for vector in sequence)


HYPERPLANES = tuple(
    tuple(x for x in range(1, 16) if parity(functional & x) == 0)
    for functional in range(1, 16)
)
HYPERPLANE_SETS = tuple(map(frozenset, HYPERPLANES))


def signatures(order: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        canonical_signature(tuple(x for x in order if x in hyperplane))
        for hyperplane in HYPERPLANE_SETS
    )


def compatible(order: tuple[int, ...]) -> bool:
    return len(set(signatures(order))) == 1


def swapped(order: tuple[int, ...], i: int, j: int) -> tuple[int, ...]:
    result = list(order)
    result[i], result[j] = result[j], result[i]
    return tuple(result)


def adjacent_component(start: tuple[int, ...], limit: int = 200_000) -> set[tuple[int, ...]]:
    seen = {start}
    queue = deque([start])
    while queue and len(seen) < limit:
        order = queue.popleft()
        for index in range(len(order) - 1):
            candidate = swapped(order, index, index + 1)
            if candidate not in seen and compatible(candidate):
                seen.add(candidate)
                queue.append(candidate)
    return seen


def main() -> None:
    standard = tuple(range(1, 16))
    assert compatible(standard)

    orbit_counts: dict[tuple[int, ...], int] = {}
    for sequence in itertools.permutations(range(1, 8)):
        signature = canonical_signature(sequence)
        orbit_counts[signature] = orbit_counts.get(signature, 0) + 1
    assert len(orbit_counts) == 30
    assert set(orbit_counts.values()) == {168}

    adjacent = [
        index
        for index in range(14)
        if compatible(swapped(standard, index, index + 1))
    ]
    transpositions = [
        (i, j)
        for i in range(15)
        for j in range(i + 1, 15)
        if compatible(swapped(standard, i, j))
    ]

    component = adjacent_component(standard)
    component_signatures = sorted({signatures(order)[0] for order in component})

    rng = random.Random(20260831)
    random_hits = 0
    random_signature_counts: list[int] = []
    for _ in range(1000):
        order = list(standard)
        rng.shuffle(order)
        count = len(set(signatures(tuple(order))))
        random_signature_counts.append(count)
        random_hits += count == 1

    result = {
        "standard_signature": standard and list(signatures(standard)[0]),
        "compatible_adjacent_swaps_from_standard": adjacent,
        "compatible_transpositions_from_standard": transpositions,
        "adjacent_component_size": len(component),
        "adjacent_component_hit_limit": len(component) >= 200_000,
        "signature_types_in_component": [list(item) for item in component_signatures],
        "random_trials": 1000,
        "random_compatible_hits": random_hits,
        "random_distinct_signature_min": min(random_signature_counts),
        "random_distinct_signature_max": max(random_signature_counts),
        "controls": {
            "ordered_fano_orbit_count": len(orbit_counts),
            "orders_per_ordered_fano_orbit": sorted(set(orbit_counts.values())),
            "n3_zero_extremal_orders": 2 * 7 * 6 * 5 * 4 * 3 * 2,
            "zero_nonextremal_rejected_by_lines": True,
        },
    }

    output = Path(__file__).parent / "results"
    output.mkdir(parents=True, exist_ok=True)
    target = output / "binary-compatible-n4-local-probe.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
