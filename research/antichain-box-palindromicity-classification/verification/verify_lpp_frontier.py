"""Frontier-DP regression for the corrected d >= 3 formula.

This route is independent of the plane-partition ideal-chain recurrence and of
the direct complement enumerator.  A row frontier records exact last-passage
values.  Binary mode counts admissible supports; ternary mode permits entries
0, 1, 2 and checks the bounded-entry near-top count in the first d=3 case.
The exclusion of entries at least 3 is a separate theorem in S4.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product

from scan_rectangular_boxes import predicted_next_to_leading


def frontier_count(
    first: int, second: int, depth: int, maximum_entry: int
) -> int:
    third = first + second - 1 - 2 * depth
    target_support = first * second - depth * (depth + 1) - 1
    row_patterns = [
        (values, sum(value > 0 for value in values))
        for values in product(range(maximum_entry + 1), repeat=second)
    ]

    @lru_cache(maxsize=None)
    def count(row: int, previous: tuple[int, ...], used: int) -> int:
        if row == first:
            return int(used == target_support)
        if used > target_support or used + (first - row) * second < target_support:
            return 0

        total = 0
        for values, positive_count in row_patterns:
            new_used = used + positive_count
            if (
                new_used > target_support
                or new_used + (first - row - 1) * second < target_support
            ):
                continue
            current = []
            for column, entry in enumerate(values):
                passage = entry + max(
                    previous[column], current[column - 1] if column else 0
                )
                if passage > third:
                    break
                current.append(passage)
            else:
                total += count(row + 1, tuple(current), new_used)
        return total

    return count(0, (0,) * second, 0)


def main() -> None:
    support_cases = [(7, 7, 3), (7, 8, 3), (7, 9, 3), (8, 9, 3)]
    for first, second, depth in support_cases:
        observed = frontier_count(first, second, depth, maximum_entry=1)
        assert observed == first * second + 2
        print("binary support:", (first, second, depth, observed))

    observed_coefficient = frontier_count(7, 7, 3, maximum_entry=2)
    assert observed_coefficient == predicted_next_to_leading(7, 7, 3) == 75
    print("d=3 near-top coefficient:", observed_coefficient)
    print("frontier regression: PASS")


if __name__ == "__main__":
    main()
