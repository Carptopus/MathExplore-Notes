"""Bounded regression control for the S3 trunk-split rigidity identity."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations_with_replacement


def add(*polynomials: tuple[int, ...]) -> tuple[int, ...]:
    degree = max((len(poly) for poly in polynomials), default=0)
    result = [0] * degree
    for polynomial in polynomials:
        for index, coefficient in enumerate(polynomial):
            result[index] += coefficient
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def shift(polynomial: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return (0,) * amount + polynomial


def interval_sum(length: int) -> tuple[int, ...]:
    return (0,) + (1,) * length if length > 0 else ()


def rooted_distance(arms: tuple[int, ...]) -> tuple[int, ...]:
    result = [1]
    for length in arms:
        if len(result) <= length:
            result.extend([0] * (length + 1 - len(result)))
        for distance in range(1, length + 1):
            result[distance] += 1
    return tuple(result)


def h_polynomial(
    left: tuple[int, ...],
    right: tuple[int, ...],
    trunk_length: int,
    left_gap: int,
) -> tuple[int, ...]:
    right_gap = trunk_length - left_gap
    return add(
        shift(rooted_distance(left), left_gap),
        shift(rooted_distance(right), right_gap),
        interval_sum(left_gap - 1),
        interval_sum(right_gap - 1),
    )


def main() -> None:
    endpoints = [
        arms
        for count in range(2, 5)
        for arms in combinations_with_replacement(range(1, 6), count)
    ]
    checked = 0
    for left in endpoints:
        for right in endpoints:
            for trunk_length in range(2, 13):
                buckets: dict[tuple[int, ...], list[int]] = defaultdict(list)
                for left_gap in range(1, trunk_length):
                    buckets[
                        h_polynomial(left, right, trunk_length, left_gap)
                    ].append(left_gap)
                for positions in buckets.values():
                    if len(positions) == 1:
                        continue
                    expected = (
                        left == right
                        and len(positions) == 2
                        and sum(positions) == trunk_length
                    )
                    if not expected:
                        raise AssertionError(
                            (left, right, trunk_length, positions)
                        )
                checked += 1
    print(f"PASS checked_block_pairs={checked}")


if __name__ == "__main__":
    main()
