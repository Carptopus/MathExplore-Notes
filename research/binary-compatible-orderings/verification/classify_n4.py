"""Exact GL(4,2)-orbit classification of compatible orders on F_2^4.

The zero vector is omitted and assumed extremal.  Global GL(4,2) symmetry is
broken by sending the first four independent vectors of an order to
1, 2, 4, 8.  For each of the 30 ordered Fano-plane orbit types, a prefix
automaton enforces that every hyperplane induces that same orbit type.
"""

from __future__ import annotations

import itertools
import json
import time
from collections import defaultdict
from pathlib import Path

from probe_binary_compatible import (
    HYPERPLANE_SETS,
    canonical_signature,
    compatible,
    rank_binary,
    signatures,
)


def fano_orbits() -> dict[tuple[int, ...], list[tuple[int, ...]]]:
    result: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for sequence in itertools.permutations(range(1, 8)):
        result[canonical_signature(sequence)].append(sequence)
    assert len(result) == 30
    assert {len(value) for value in result.values()} == {168}
    return dict(result)


def hyperplane_basis(hyperplane: frozenset[int]) -> list[int]:
    basis: list[int] = []
    for vector in sorted(hyperplane):
        if rank_binary(basis + [vector]) > len(basis):
            basis.append(vector)
    assert len(basis) == 3
    return basis


def mapped_vector(coordinates: int, basis: list[int]) -> int:
    value = 0
    for index, vector in enumerate(basis):
        if coordinates & (1 << index):
            value ^= vector
    return value


def prefix_sets_for_hyperplanes(
    sequences: list[tuple[int, ...]],
) -> list[list[set[tuple[int, ...]]]]:
    result = []
    for hyperplane in HYPERPLANE_SETS:
        basis = hyperplane_basis(hyperplane)
        mapped = [
            tuple(mapped_vector(vector, basis) for vector in sequence)
            for sequence in sequences
        ]
        result.append(
            [
                {sequence[:length] for sequence in mapped}
                for length in range(8)
            ]
        )
    return result


def classify_signature(
    target: tuple[int, ...], sequences: list[tuple[int, ...]]
) -> tuple[list[tuple[int, ...]], int]:
    allowed = prefix_sets_for_hyperplanes(sequences)
    hyperplane_sequences: list[tuple[int, ...]] = [tuple() for _ in range(15)]
    containing = [
        tuple(index for index, hyperplane in enumerate(HYPERPLANE_SETS) if x in hyperplane)
        for x in range(16)
    ]
    solutions: list[tuple[int, ...]] = []
    nodes = 0

    def visit(order: tuple[int, ...], remaining_mask: int, rank: int) -> None:
        nonlocal nodes
        nodes += 1
        if remaining_mask == 0:
            assert compatible(order)
            assert signatures(order)[0] == target
            solutions.append(order)
            return

        # Once the first r independent vectors have been normalised to
        # 1,2,...,2^(r-1), dependent vectors are exactly 1,...,2^r-1.
        candidates = [
            x
            for x in range(1, 1 << rank)
            if remaining_mask & (1 << x)
        ]
        if rank < 4:
            next_basis = 1 << rank
            if remaining_mask & (1 << next_basis):
                candidates.append(next_basis)

        for x in candidates:
            changed: list[tuple[int, tuple[int, ...]]] = []
            valid = True
            for index in containing[x]:
                old = hyperplane_sequences[index]
                new = old + (x,)
                changed.append((index, old))
                hyperplane_sequences[index] = new
                if new not in allowed[index][len(new)]:
                    valid = False
                    break
            if valid:
                visit(
                    order + (x,),
                    remaining_mask ^ (1 << x),
                    rank + int(rank < 4 and x == (1 << rank)),
                )
            for index, old in reversed(changed):
                hyperplane_sequences[index] = old

    visit(tuple(), sum(1 << x for x in range(1, 16)), 0)
    return solutions, nodes


def main() -> None:
    started = time.perf_counter()
    orbits = fano_orbits()
    records = []
    all_solutions: list[tuple[int, ...]] = []
    for target in sorted(orbits):
        target_started = time.perf_counter()
        solutions, nodes = classify_signature(target, orbits[target])
        elapsed = time.perf_counter() - target_started
        records.append(
            {
                "target_signature": list(target),
                "canonical_solution_count": len(solutions),
                "search_nodes": nodes,
                "solutions": [list(order) for order in solutions],
            }
        )
        all_solutions.extend(solutions)
        print(target, len(solutions), nodes, f"{elapsed:.3f}s", flush=True)

    gl4_order = (15 * 14 * 12 * 8)
    result = {
        "method": "complete prefix-automaton DFS with first-independent-basis GL(4,2) symmetry breaking",
        "ordered_fano_orbit_types": len(orbits),
        "canonical_gl4_orbit_count": len(all_solutions),
        "labelled_orders_with_zero_fixed_minimum": len(all_solutions) * gl4_order,
        "labelled_orders_with_zero_extremal": len(all_solutions) * gl4_order * 2,
        "gl4_order": gl4_order,
        "records": records,
    }
    output = Path(__file__).parent / "results"
    output.mkdir(parents=True, exist_ok=True)
    target = output / "binary-compatible-n4-classification.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, indent=2))


if __name__ == "__main__":
    main()
