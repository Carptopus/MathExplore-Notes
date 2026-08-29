"""Bounded exact calibration of the proposed Fano half-rank profile semigroup."""

from __future__ import annotations

from collections import deque
from itertools import combinations, product


LINES = (
    (0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
    (1, 4, 6), (2, 3, 6), (2, 4, 5),
)


def fano_maps() -> tuple[tuple[int, ...], ...]:
    result = []
    for first in range(1, 8):
        for second in range(1, 8):
            if second == first:
                continue
            for third in range(1, 8):
                if third in (first, second, first ^ second):
                    continue
                result.append(tuple(
                    ((first if point & 1 else 0)
                     ^ (second if point & 2 else 0)
                     ^ (third if point & 4 else 0))
                    for point in range(1, 8)
                ))
    return tuple(result)


FANO_MAPS = fano_maps()


def orbit(profile: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        tuple(profile[mapping[point] - 1] for point in range(7))
        for mapping in FANO_MAPS
    }


def rank_four_atoms() -> set[tuple[int, ...]]:
    line_sets = {frozenset(line) for line in LINES}
    all_points = frozenset(range(7))
    result = {tuple(0 if point in line else 1 for point in range(7)) for line in LINES}
    result.add((1,) * 7)
    result.update(
        tuple(0 if point == zero else 1 for point in range(7))
        for zero in range(7)
    )
    for mask in range(1, 1 << 7):
        support = frozenset(point for point in range(7) if (mask >> point) & 1)
        if len(support) == 2 or (
            len(support) == 4 and all_points.difference(support) not in line_sets
        ):
            result.add(tuple(2 if point in support else 1 for point in range(7)))
    assert len(result) == 64
    return result


def known_actual_generators() -> set[tuple[int, ...]]:
    result = rank_four_atoms()
    for representative in (
        (1, 1, 2, 2, 3, 3, 2),
        (1, 2, 3, 2, 3, 3, 2),
        (4, 2, 2, 3, 2, 4, 4),
        (3, 4, 4, 2, 2, 2, 2),
        (4, 4, 4, 2, 2, 2, 2),
        (6, 6, 6, 3, 3, 3, 3),
    ):
        result.update(orbit(representative))
    for first, second in combinations(range(1, 8), 2):
        profile = [3] * 7
        profile[first - 1] = 5
        profile[second - 1] = 5
        profile[(first ^ second) - 1] = 6
        result.add(tuple(profile))
    return result


def triangle_feasible(profile: tuple[int, ...]) -> bool:
    return all(
        profile[left] + profile[right] >= profile[third]
        for line in LINES
        for left, right, third in (
            (line[0], line[1], line[2]),
            (line[0], line[2], line[1]),
            (line[1], line[2], line[0]),
        )
    )


def predicted_holes(bound: int) -> set[tuple[int, ...]]:
    result = {
        tuple(2 if point in line else 1 for point in range(7))
        for line in LINES
    }
    for distinguished in range(7):
        singleton = tuple(2 if point == distinguished else 1 for point in range(7))
        cuts = tuple(
            tuple(0 if point in line else 1 for point in range(7))
            for line in LINES if distinguished not in line
        )
        for coefficients in product(range(bound + 1), repeat=4):
            profile = tuple(
                singleton[point]
                + sum(coefficients[index] * cuts[index][point] for index in range(4))
                for point in range(7)
            )
            if max(profile) <= bound:
                result.add(profile)
    return result


def main(bound: int = 6) -> None:
    generators = tuple(
        profile for profile in known_actual_generators()
        if max(profile) <= bound
    )
    zero = (0,) * 7
    reachable = {zero}
    queue = deque([zero])
    while queue:
        current = queue.popleft()
        for generator in generators:
            successor = tuple(a + b for a, b in zip(current, generator))
            if max(successor) > bound or successor in reachable:
                continue
            reachable.add(successor)
            queue.append(successor)

    feasible = {
        profile for profile in product(range(bound + 1), repeat=7)
        if triangle_feasible(profile)
    }
    holes = feasible.difference(reachable)
    expected = predicted_holes(bound)
    unexpected = holes.difference(expected)
    overpredicted = expected.difference(holes)
    print(
        f"bound={bound} generators={len(generators)} feasible={len(feasible)} "
        f"reachable={len(reachable)} holes={len(holes)} predicted={len(expected)}"
    )
    print(f"unexpected={len(unexpected)} overpredicted={len(overpredicted)}")
    if unexpected:
        print("unexpected_samples=", sorted(unexpected)[:20])
    if overpredicted:
        print("overpredicted_samples=", sorted(overpredicted)[:20])
    assert not unexpected and not overpredicted


if __name__ == "__main__":
    main()
