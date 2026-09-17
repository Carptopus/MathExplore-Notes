"""Guard the corrected equal-order endpoint-pair recovery lemma.

This script has two jobs:
1. reproduce the concrete counterexample to the discarded claim that the
   spider Lemma 3.2 Case-1 formula extends verbatim to a rooted path;
2. exhaustively check the complement-pairing uniqueness used when both
   equal-order endpoint blocks are rooted paths.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, combinations_with_replacement


def tree_from_arms(arms: tuple[int, ...], offset: int = 0) -> tuple[set[int], list[tuple[int, int]]]:
    vertices = {offset}
    edges: list[tuple[int, int]] = []
    next_vertex = offset + 1
    for length in arms:
        previous = offset
        for _ in range(length):
            current = next_vertex
            next_vertex += 1
            vertices.add(current)
            edges.append((previous, current))
            previous = current
    return vertices, edges


def component_sizes(vertices: set[int], edges: list[tuple[int, int]]) -> tuple[int, ...]:
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen: set[int] = set()
    sizes: list[int] = []
    for start in vertices:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            u = stack.pop()
            size += 1
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        sizes.append(size)
    return tuple(sorted(sizes, reverse=True))


def count_two_edge_cuts(arms: tuple[int, ...], target: tuple[int, ...]) -> int:
    vertices, edges = tree_from_arms(arms)
    count = 0
    for removed in combinations(range(len(edges)), 2):
        remaining = [edge for i, edge in enumerate(edges) if i not in removed]
        if component_sizes(vertices, remaining) == tuple(sorted(target, reverse=True)):
            count += 1
    return count


def old_case1_formula(forest_arms: tuple[tuple[int, ...], ...], i: int) -> int:
    counts = [sum(length >= i for length in arms) for arms in forest_arms]
    twice = sum(sum(length >= 2 * i for length in arms) for arms in forest_arms)
    return sum(x * (x - 1) // 2 for x in counts) + twice


def all_complement_pairings(values: tuple[int, ...], total: int) -> set[tuple[tuple[int, int], ...]]:
    if not values:
        return {()}
    first = values[0]
    results: set[tuple[tuple[int, int], ...]] = set()
    for index in range(1, len(values)):
        if first + values[index] != total:
            continue
        rest = values[1:index] + values[index + 1 :]
        pair = tuple(sorted((first, values[index])))
        for suffix in all_complement_pairings(rest, total):
            results.add(tuple(sorted((pair,) + suffix)))
    return results


def main() -> None:
    path_arms = (2, 7)
    spider_arms = (7, 1, 1)
    direct = count_two_edge_cuts(path_arms, (6, 2, 2)) + count_two_edge_cuts(
        spider_arms, (6, 2, 2)
    )
    formula = old_case1_formula((path_arms, spider_arms), 2)
    assert direct == 4, direct
    assert formula == 3, formula

    checked = 0
    for order in range(3, 25):
        arm_total = order - 1
        for values in combinations_with_replacement(range(1, arm_total), 4):
            if sum(values) != 2 * arm_total:
                continue
            pairings = all_complement_pairings(values, arm_total)
            if not pairings:
                continue
            checked += 1
            assert len(pairings) == 1, (order, values, pairings)

            # Multiplicity balance is the intrinsic existence criterion.
            counts = Counter(values)
            for value, multiplicity in counts.items():
                complement = arm_total - value
                if complement == value:
                    assert multiplicity % 2 == 0
                else:
                    assert multiplicity == counts[complement]

    print(
        "PASS verify_two_arm_extension_guard "
        f"counterexample_direct={direct} old_formula={formula} "
        f"complement_multisets={checked}"
    )


if __name__ == "__main__":
    main()
