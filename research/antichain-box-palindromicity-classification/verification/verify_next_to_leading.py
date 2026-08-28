"""Independent finite checks for the near-extremal lattice-path formula.

The script enumerates complements of supports rather than using the
Ding--Dong transfer recurrence.  It verifies both the number of admissible
supports and every possible single-cell weight increment in a bounded
regression set.  Multiple increments and entries at least 3 are excluded by
the theoretical saturation argument in S4, not by this script.  The
all-parameter claim is proved in S4--S5; this script is only an independent
destructive check.
"""

from __future__ import annotations

from itertools import combinations

from scan_rectangular_boxes import predicted_next_to_leading


Cell = tuple[int, int]


def last_passage(
    rows: int, columns: int, zero_set: set[Cell], doubled: Cell | None = None
) -> int:
    values = [[0] * columns for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            cell = (row, column)
            weight = 0 if cell in zero_set else 1
            if cell == doubled:
                weight += 1
            values[row][column] = weight + max(
                values[row - 1][column] if row else 0,
                values[row][column - 1] if column else 0,
            )
    return values[-1][-1]


def direct_count(first: int, second: int, depth: int) -> tuple[int, int]:
    third = first + second - 1 - 2 * depth
    width = first * second - depth * (depth + 1)
    complement_size = first * second - (width - 1)
    cells = [(row, column) for row in range(first) for column in range(second)]

    supports = 0
    increments = 0
    for complement_tuple in combinations(cells, complement_size):
        complement = set(complement_tuple)
        if last_passage(first, second, complement) > third:
            continue
        supports += 1
        for cell in cells:
            if cell not in complement and last_passage(
                first, second, complement, cell
            ) <= third:
                increments += 1
    return supports, increments


def main() -> None:
    cases = [
        (3, 3, 1),
        (3, 7, 1),
        (4, 6, 1),
        (5, 7, 1),
        (5, 5, 2),
        (5, 6, 2),
    ]
    results = []
    for first, second, depth in cases:
        supports, increments = direct_count(first, second, depth)
        width = first * second - depth * (depth + 1)
        expected_supports = first * second + 2
        expected_total = predicted_next_to_leading(first, second, depth)
        assert supports == expected_supports
        assert supports + increments == expected_total
        results.append(
            (first, second, depth, supports, increments, expected_total)
        )
    print("near-extremal complement regression: PASS")
    print("(a, b, d, supports, increments, total):")
    for result in results:
        print(result)

    # Mandatory negative control for the retracted w + 4d support formula.
    first = second = 7
    depth = 3
    standard = {
        (row, column)
        for row in range(first)
        for column in range(second)
        if row + column <= 2 or row + column >= 10
    }
    omitted_support_complement = (standard - {(1, 1)}) | {(1, 2), (2, 1)}
    assert len(omitted_support_complement) == depth * (depth + 1) + 1
    assert last_passage(first, second, omitted_support_complement) == 7
    assert predicted_next_to_leading(7, 7, 3) == 75
    print("d=3 internal-gap negative control: PASS")


if __name__ == "__main__":
    main()
