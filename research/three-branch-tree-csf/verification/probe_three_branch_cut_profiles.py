"""Exact small-order calibration for trees with exactly three branch vertices.

The script enumerates the canonical path-trunk descriptions used in S1 and
compares the multisets of component-size partitions obtained after deleting
one through ``max_cuts`` edges.  It is discovery/calibration code, not a proof.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations


Description = tuple[int, int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]


def partitions(total: int, minimum_length: int, ceiling: int | None = None):
    ceiling = total if ceiling is None else ceiling

    def visit(remainder: int, upper: int, current: list[int]):
        if remainder == 0:
            if len(current) >= minimum_length:
                yield tuple(current)
            return
        for part in range(min(upper, remainder), 0, -1):
            yield from visit(remainder - part, part, current + [part])

    yield from visit(total, ceiling, [])


def canonical(description: Description) -> Description:
    left_gap, right_gap, left, middle, right = description
    reflected = (right_gap, left_gap, right, middle, left)
    return min(description, reflected)


def descriptions(order: int):
    seen: set[Description] = set()
    for left_gap in range(1, order):
        for right_gap in range(1, order - left_gap):
            arm_total = order - (1 + left_gap + right_gap)
            if arm_total < 5:
                continue
            for left_total in range(2, arm_total):
                for middle_total in range(1, arm_total - left_total):
                    right_total = arm_total - left_total - middle_total
                    if right_total < 2:
                        continue
                    for left in partitions(left_total, 2):
                        for middle in partitions(middle_total, 1):
                            for right in partitions(right_total, 2):
                                seen.add(
                                    canonical(
                                        (
                                            left_gap,
                                            right_gap,
                                            left,
                                            middle,
                                            right,
                                        )
                                    )
                                )
    yield from sorted(seen)


def tree(description: Description):
    left_gap, right_gap, left, middle, right = description
    adjacency: list[list[tuple[int, int]]] = []
    edges: list[tuple[int, int]] = []

    def vertex() -> int:
        adjacency.append([])
        return len(adjacency) - 1

    def edge(first: int, second: int) -> None:
        index = len(edges)
        edges.append((first, second))
        adjacency[first].append((second, index))
        adjacency[second].append((first, index))

    left_vertex = vertex()
    previous = left_vertex
    for _ in range(left_gap):
        current = vertex()
        edge(previous, current)
        previous = current
    middle_vertex = previous
    for _ in range(right_gap):
        current = vertex()
        edge(previous, current)
        previous = current
    right_vertex = previous

    for root, arms in (
        (left_vertex, left),
        (middle_vertex, middle),
        (right_vertex, right),
    ):
        for length in arms:
            previous = root
            for _ in range(length):
                current = vertex()
                edge(previous, current)
                previous = current
    return adjacency, edges


def cut_profile(description: Description, max_cuts: int):
    adjacency, edges = tree(description)
    order = len(adjacency)
    profile = []
    for cut_count in range(1, max_cuts + 1):
        counts: Counter[tuple[int, ...]] = Counter()
        for cut_tuple in combinations(range(len(edges)), cut_count):
            cut = set(cut_tuple)
            seen = [False] * order
            sizes = []
            for start in range(order):
                if seen[start]:
                    continue
                seen[start] = True
                stack = [start]
                size = 0
                while stack:
                    current = stack.pop()
                    size += 1
                    for neighbour, edge_index in adjacency[current]:
                        if edge_index not in cut and not seen[neighbour]:
                            seen[neighbour] = True
                            stack.append(neighbour)
                sizes.append(size)
            counts[tuple(sorted(sizes, reverse=True))] += 1
        profile.append(tuple(sorted(counts.items())))
    return tuple(profile)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=16)
    parser.add_argument("--max-cuts", type=int, default=4)
    args = parser.parse_args()

    first_collision = None
    for order in range(8, args.max_order + 1):
        objects = list(descriptions(order))
        buckets: dict[object, list[Description]] = defaultdict(list)
        for description in objects:
            buckets[cut_profile(description, args.max_cuts)].append(description)
        collisions = [value for value in buckets.values() if len(value) > 1]
        print(
            f"n={order}: objects={len(objects)}, "
            f"collision_classes={len(collisions)}"
        )
        if collisions and first_collision is None:
            first_collision = collisions[0]

    if first_collision is not None:
        print("first collision:", first_collision)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
