"""Exact controls for the S7 three-leaf P/Q exchange separator."""

from __future__ import annotations

import argparse
import importlib.util
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


PROBE_PATH = Path(__file__).resolve().parent / "probe_three_branch_cut_profiles.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("three_branch_probe", PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PROBE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trim(poly: list[int]) -> tuple[int, ...]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def add(*polys: tuple[int, ...]) -> tuple[int, ...]:
    size = max((len(poly) for poly in polys), default=1)
    result = [0] * size
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            result[degree] += coefficient
    return trim(result)


def negate(poly: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-coefficient for coefficient in poly)


def multiply(first: tuple[int, ...], second: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * (len(first) + len(second) - 1)
    for first_degree, first_coefficient in enumerate(first):
        for second_degree, second_coefficient in enumerate(second):
            result[first_degree + second_degree] += (
                first_coefficient * second_coefficient
            )
    return trim(result)


def monomial(degree: int) -> tuple[int, ...]:
    return (0,) * degree + (1,)


def arm(length: int) -> tuple[int, ...]:
    return (0,) + (1,) * length


def elementary(arms: tuple[int, ...], degree: int) -> tuple[int, ...]:
    values = [(1,)] + [(0,)] * degree
    for length in arms:
        value = arm(length)
        for index in range(degree, 0, -1):
            values[index] = add(values[index], multiply(values[index - 1], value))
    return values[degree]


def three_leaf_formula(
    alpha: int,
    left: tuple[int, ...],
    middle: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    z = monomial(alpha)
    h = arm(alpha)
    left_one = elementary(left, 1)
    left_two = elementary(left, 2)
    middle_one = elementary(middle, 1)
    middle_two = elementary(middle, 2)
    return add(
        elementary(left, 3),
        elementary(middle, 3),
        elementary(right, 3),
        multiply(h, add(left_two, middle_two)),
        multiply(
            z,
            add(
                multiply(left_two, middle_one),
                multiply(left_one, middle_two),
            ),
        ),
    )


def double_spider_graph(alpha, left, middle):
    adjacency: list[list[int]] = []
    edges: list[tuple[int, int]] = []

    def vertex() -> int:
        adjacency.append([])
        return len(adjacency) - 1

    def edge(first: int, second: int) -> None:
        index = len(edges)
        edges.append((first, second))
        adjacency[first].append(index)
        adjacency[second].append(index)

    left_root = vertex()
    previous = left_root
    for _ in range(alpha):
        current = vertex()
        edge(previous, current)
        previous = current
    middle_root = previous
    for root, arms in ((left_root, left), (middle_root, middle)):
        for length in arms:
            previous = root
            for _ in range(length):
                current = vertex()
                edge(previous, current)
                previous = current
    return adjacency, edges


def spider_graph(arms):
    return double_spider_graph(0, (), arms)


def exact_three_leaf_polynomial(adjacency, edges):
    counts: Counter[int] = Counter()
    for edge_count in range(1, len(edges) + 1):
        for selected_tuple in combinations(range(len(edges)), edge_count):
            selected = set(selected_tuple)
            vertices = set()
            degrees = Counter()
            for edge_index in selected:
                first, second = edges[edge_index]
                vertices.update((first, second))
                degrees[first] += 1
                degrees[second] += 1
            start = next(iter(vertices))
            seen = {start}
            stack = [start]
            while stack:
                current = stack.pop()
                for edge_index in adjacency[current]:
                    if edge_index not in selected:
                        continue
                    first, second = edges[edge_index]
                    neighbour = second if first == current else first
                    if neighbour not in seen:
                        seen.add(neighbour)
                        stack.append(neighbour)
            if seen == vertices and sum(value == 1 for value in degrees.values()) == 3:
                counts[edge_count] += 1
    if not counts:
        return (0,)
    return tuple(counts.get(degree, 0) for degree in range(max(counts) + 1))


def path_profile(adjacency):
    counts = [0] * len(adjacency)
    for start in range(len(adjacency)):
        distances = [-1] * len(adjacency)
        distances[start] = 0
        queue = [start]
        for current in queue:
            for edge_index in adjacency[current]:
                first, second = EDGES[edge_index]
                neighbour = second if first == current else first
                if distances[neighbour] < 0:
                    distances[neighbour] = distances[current] + 1
                    queue.append(neighbour)
        for finish in range(start + 1, len(adjacency)):
            counts[distances[finish]] += 1
    return tuple(counts)


def tree_path_profile(probe, description):
    adjacency_with_edges, edges = probe.tree(description)
    adjacency = [[edge_index for _, edge_index in row] for row in adjacency_with_edges]
    global EDGES
    EDGES = edges
    return path_profile(adjacency)


def factor_rhs(alpha, left, p, q):
    z = monomial(alpha)
    one_minus_z = add((1,), negate(z))
    return multiply(
        multiply(multiply(z, one_minus_z), elementary(left, 2)),
        add(elementary(p, 1), negate(elementary(q, 1))),
    )


def subtract_counter(first: Counter, second: Counter):
    result = first.copy()
    result.subtract(second)
    return result if all(value >= 0 for value in result.values()) else None


def exchange_parts(first, second):
    alpha, _, left, middle, right = first
    _, _, other_left, other_middle, other_right = second
    if left != other_left:
        return None
    base_middle = Counter({alpha: len(left) - 1})
    base_right = Counter(alpha + length for length in left)
    p = subtract_counter(Counter(middle), base_middle)
    q = subtract_counter(Counter(right), base_right)
    if p is None or q is None:
        return None
    if Counter(other_middle) != base_middle + q:
        return None
    if Counter(other_right) != base_right + p:
        return None
    return tuple(sorted(p.elements(), reverse=True)), tuple(
        sorted(q.elements(), reverse=True)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=18)
    args = parser.parse_args()
    probe = load_probe()

    # Direct graph control for formula (18), including partial-trunk subtrees.
    direct_cases = (
        (1, (1, 1), (3, 1), (2, 2, 2, 1)),
        (2, (2, 1), (2, 1, 1), (3, 2)),
        (3, (1, 1, 1), (2,), (4, 1)),
    )
    for alpha, left, middle, right in direct_cases:
        first_graph = double_spider_graph(alpha, left, middle)
        second_graph = spider_graph(right)
        exact = add(
            exact_three_leaf_polynomial(*first_graph),
            exact_three_leaf_polynomial(*second_graph),
        )
        assert exact == three_leaf_formula(alpha, left, middle, right)

    collision_pairs = 0
    for order in range(8, args.max_order + 1):
        buckets = defaultdict(list)
        for description in probe.descriptions(order):
            alpha, _, left, middle, right = description
            left_order = 1 + sum(left)
            middle_order = 1 + sum(middle)
            right_order = 1 + sum(right)
            left_middle_order = left_order + middle_order + alpha - 1
            if not (
                left_order < right_order
                and alpha < right_order - left_order
                and left_middle_order == right_order
            ):
                continue
            key = (
                alpha,
                left,
                tuple(sorted(middle + right, reverse=True)),
                tree_path_profile(probe, description),
            )
            buckets[key].append(description)

        for values in buckets.values():
            for first_index, first in enumerate(values):
                for second in values[first_index + 1 :]:
                    parts = exchange_parts(first, second)
                    orientation = 1
                    if parts is None:
                        parts = exchange_parts(second, first)
                        orientation = -1
                    assert parts is not None
                    p, q = parts
                    source = first if orientation == 1 else second
                    target = second if orientation == 1 else first
                    alpha, _, left, middle, right = source
                    difference = add(
                        three_leaf_formula(alpha, left, middle, right),
                        negate(
                            three_leaf_formula(
                                target[0], target[2], target[3], target[4]
                            )
                        ),
                    )
                    assert difference == factor_rhs(alpha, left, p, q)
                    assert difference != (0,) or p == q
                    collision_pairs += 1

    print(
        "PASS direct_formula_cases=3 "
        f"classified_collision_pairs={collision_pairs} separated=true"
    )


if __name__ == "__main__":
    main()
