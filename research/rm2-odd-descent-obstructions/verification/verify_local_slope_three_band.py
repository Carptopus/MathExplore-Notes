"""Regression check for the local slope-three band classification.

This exhausts both dimension-sensitive rank/sign outer models.  In odd
dimension a maximal-rank quadratic form may have zero Walsh sum, whereas in
even dimension it may not.  The odd maximal-Pfaffian vector argument and even
scalar-Pfaffian parity remain mathematical lemmas, not computations here.
"""

from __future__ import annotations

import sys
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path


CURRENT = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT))

from verify_odd_descent_counterexample_family import (  # noqa: E402
    FANO_LINES,
    fixed_half_rank,
    is_fano_line,
    normalized_alphabet,
)


def admissible_half_ranks(
    m: int,
    values: tuple[int, ...],
    *,
    odd_dimension: bool,
) -> list[tuple[int, ...]]:
    """Apply Fano rank triangles and equality signs with the right zero range."""
    options = [
        range(m + 1) if odd_dimension and value == 0
        else range(m) if value == 0
        else (fixed_half_rank(m, value),)
        for value in values
    ]
    result: list[tuple[int, ...]] = []
    for ranks in product(*options):
        compatible = True
        for i, j, k in FANO_LINES:
            if (
                ranks[i] > ranks[j] + ranks[k]
                or ranks[j] > ranks[i] + ranks[k]
                or ranks[k] > ranks[i] + ranks[j]
            ):
                compatible = False
                break
            for largest, first, second in ((i, j, k), (j, i, k), (k, i, j)):
                if (
                    ranks[largest] == ranks[first] + ranks[second]
                    and values[largest]
                    and values[first]
                    and values[second]
                    and values[largest] * (1 << m)
                    != values[first] * values[second]
                ):
                    compatible = False
                    break
            if not compatible:
                break
        if compatible:
            result.append(tuple(ranks))
    return result


def reduced_signatures(
    m: int,
    c: int,
    *,
    odd_dimension: bool = False,
) -> set[tuple[int, ...]]:
    target = 3 * (1 << (m - 1)) + c
    result: set[tuple[int, ...]] = set()
    for multiset in combinations_with_replacement(normalized_alphabet(m), 7):
        if sum(multiset) != target:
            continue
        for values in set(permutations(multiset)):
            if admissible_half_ranks(m, values, odd_dimension=odd_dimension):
                result.add(values)
    return result


def main() -> None:
    for m in range(6, 10):
        large = 1 << (m - 1)
        offsets = range(-(large // 8) + 1, large // 8, 2)
        for odd_dimension in (False, True):
            for c in offsets:
                signatures = reduced_signatures(
                    m, c, odd_dimension=odd_dimension
                )
                if abs(c) > 7:
                    assert not signatures
                    continue

                assert signatures
                for values in signatures:
                    line = frozenset(
                        index for index, value in enumerate(values) if value == large
                    )
                    assert is_fano_line(line)
                    complement = set(range(7)) - line
                    assert (
                        sum(abs(values[index]) == 1 for index in complement) % 2 == 1
                    )

                if abs(c) == 7:
                    assert {tuple(sorted(values)) for values in signatures} == {
                        (-2, -2, -2, -1, large, large, large)
                        if c == -7
                        else (1, 2, 2, 2, large, large, large)
                    }

    print("PASS: even and odd expanding-band outer reductions agree for m=6,...,9")
    print("PASS: only offsets +-1,+-3,+-5,+-7 survive the outer reduction")
    print("PASS: odd maximal-rank zero-Walsh coordinates were included")


if __name__ == "__main__":
    main()
