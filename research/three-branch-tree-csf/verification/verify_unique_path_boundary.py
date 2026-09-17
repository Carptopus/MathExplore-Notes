"""Exact controls for the S11 unique-minimum path endpoint theorem."""

from __future__ import annotations

import argparse
import importlib.util
from collections import Counter, defaultdict
from itertools import combinations
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
S7_CONTROL = HERE / "verify_three_leaf_separator.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plus_one(s7, polynomial):
    return s7.add((1,), polynomial)


def shift(s7, degree, polynomial):
    return s7.multiply(s7.monomial(degree), polynomial)


def arm_sum(s7, arms):
    return s7.elementary(arms, 1)


def path_remainder(s7, description):
    alpha, beta, left, middle, right = description
    a = arm_sum(s7, left)
    b = arm_sum(s7, middle)
    c = arm_sum(s7, right)
    z = s7.monomial(alpha)
    w = s7.monomial(beta)
    h = s7.arm(alpha)
    g = s7.arm(beta)
    return s7.add(
        s7.multiply(a, s7.add(h, s7.multiply(z, g))),
        s7.multiply(b, s7.add(h, g)),
        s7.multiply(c, s7.add(g, s7.multiply(w, h))),
        s7.multiply(s7.add(z, (-1,)), s7.multiply(a, b)),
        s7.multiply(
            s7.add(s7.multiply(z, w), (-1,)), s7.multiply(a, c)
        ),
        s7.multiply(s7.add(w, (-1,)), s7.multiply(b, c)),
    )


def three_leaf_formula(s7, description):
    alpha, beta, left, middle, right = description
    a = arm_sum(s7, left)
    b = arm_sum(s7, middle)
    c = arm_sum(s7, right)
    h_a = s7.add(s7.arm(alpha - 1), shift(s7, alpha, plus_one(s7, a)))
    h_c = s7.add(s7.arm(beta - 1), shift(s7, beta, plus_one(s7, c)))
    r_a = s7.add(
        s7.arm(alpha - 1),
        shift(s7, alpha, s7.add(plus_one(s7, b), h_c)),
    )
    r_c = s7.add(
        s7.arm(beta - 1),
        shift(s7, beta, s7.add(plus_one(s7, b), h_a)),
    )
    return s7.add(
        s7.elementary(left, 3),
        s7.elementary(middle, 3),
        s7.elementary(right, 3),
        s7.multiply(r_a, s7.elementary(left, 2)),
        s7.multiply(r_c, s7.elementary(right, 2)),
        s7.multiply(s7.add(h_a, h_c), s7.elementary(middle, 2)),
        s7.multiply(s7.multiply(h_a, h_c), b),
    )


def graph(description, probe):
    adjacency_with_edges, edges = probe.tree(description)
    adjacency = [[neighbour for neighbour, _ in row] for row in adjacency_with_edges]
    return adjacency, edges


def four_leaf_five_edge_formula(description, probe):
    adjacency, edges = graph(description, probe)
    value = 0
    for vertex, neighbours in enumerate(adjacency):
        degree = len(neighbours)
        if degree < 4:
            continue
        distance_two = set()
        for neighbour in neighbours:
            for second in adjacency[neighbour]:
                if second != vertex:
                    distance_two.add(second)
        value += comb(degree - 1, 3) * len(distance_two)
    branch_vertices = {vertex for vertex, neighbours in enumerate(adjacency) if len(neighbours) >= 3}
    for first, second in edges:
        if first in branch_vertices and second in branch_vertices:
            value += comb(len(adjacency[first]) - 1, 2) * comb(
                len(adjacency[second]) - 1, 2
            )
    return value


def exact_four_leaf_five_edge(description, probe):
    adjacency, edges = graph(description, probe)
    value = 0
    for selected_tuple in combinations(range(len(edges)), 5):
        selected = set(selected_tuple)
        degrees = Counter()
        vertices = set()
        selected_adjacency = defaultdict(list)
        for edge_index in selected:
            first, second = edges[edge_index]
            vertices.update((first, second))
            degrees[first] += 1
            degrees[second] += 1
            selected_adjacency[first].append(second)
            selected_adjacency[second].append(first)
        start = next(iter(vertices))
        seen = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            for neighbour in selected_adjacency[current]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        if seen == vertices and sum(value == 1 for value in degrees.values()) == 4:
            value += 1
    return value


def threshold(arms, level):
    return sum(length >= level for length in arms)


def coefficient(polynomial, degree):
    return polynomial[degree] if degree < len(polynomial) else 0


def orient_unique_minimum(description):
    alpha, beta, left, middle, right = description
    left_order = 1 + sum(left)
    right_order = 1 + sum(right)
    if left_order < right_order:
        return description
    if right_order < left_order:
        return beta, alpha, right, middle, left
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=19)
    parser.add_argument("--exact-order", type=int, default=12)
    args = parser.parse_args()

    s7 = load_module("s7_control", S7_CONTROL)
    probe = s7.load_probe()
    checked = 0
    fixed_count_pairs = 0
    count_swap_pairs = 0
    buckets = defaultdict(list)

    for order in range(8, args.max_order + 1):
        for raw in probe.descriptions(order):
            description = orient_unique_minimum(raw)
            if description is None:
                continue
            alpha, beta, left, middle, right = description
            left_order = 1 + sum(left)
            middle_order = 1 + sum(middle)
            right_order = 1 + sum(right)
            if len(left) != 2 or not (alpha == 1 or right_order == left_order + 1):
                continue

            if order <= args.exact_order:
                adjacency_with_edges, edges = probe.tree(description)
                adjacency = [
                    [edge_index for _, edge_index in row]
                    for row in adjacency_with_edges
                ]
                exact_three = s7.exact_three_leaf_polynomial(adjacency, edges)
                assert exact_three == three_leaf_formula(s7, description)
                assert exact_four_leaf_five_edge(description, probe) == four_leaf_five_edge_formula(
                    description, probe
                )

            key = (
                alpha,
                beta,
                left_order,
                middle_order,
                right_order,
                tuple(sorted(left + middle + right, reverse=True)),
            )
            buckets[(order, key)].append(description)
            checked += 1

    recovery_buckets = defaultdict(list)
    for (order, key), descriptions in buckets.items():
        for description in descriptions:
            signature = (
                key,
                path_remainder(s7, description),
                three_leaf_formula(s7, description),
                four_leaf_five_edge_formula(description, probe),
            )
            recovery_buckets[(order, signature)].append(description)

        for first_index, first in enumerate(descriptions):
            for second in descriptions[first_index + 1 :]:
                if first[2] == second[2]:
                    continue
                q, m = len(first[3]), len(first[4])
                q_prime, m_prime = len(second[3]), len(second[4])
                if q == q_prime and m == m_prime:
                    levels = range(2, max(max(first[2] + first[3] + first[4]), max(second[2] + second[3] + second[4])) + 1)
                    first_level = next(
                        (
                            level
                            for level in levels
                            if any(
                                threshold(first[index], level)
                                != threshold(second[index], level)
                                for index in (2, 3, 4)
                            )
                        ),
                        None,
                    )
                    if first_level is None:
                        continue
                    rho = threshold(first[2], first_level) - threshold(second[2], first_level)
                    sigma = threshold(first[3], first_level) - threshold(second[3], first_level)
                    w_difference = s7.add(
                        path_remainder(s7, first),
                        s7.negate(path_remainder(s7, second)),
                    )
                    j_difference = s7.add(
                        three_leaf_formula(s7, first),
                        s7.negate(three_leaf_formula(s7, second)),
                    )
                    expected_w = -(m - 2) * rho + (q - m + 1) * sigma
                    expected_j = (1 - comb(m, 2)) * rho + (
                        comb(q + 1, 2) - comb(m, 2)
                    ) * sigma
                    assert coefficient(w_difference, first_level + 1) == expected_w
                    assert coefficient(j_difference, first_level + 2) == expected_j
                    fixed_count_pairs += 1
                elif first[0] == 1 and q_prime == m - 1 and m_prime == q + 1:
                    a2 = threshold(first[2], 2)
                    a2_prime = threshold(second[2], 2)
                    w_difference = s7.add(
                        path_remainder(s7, first),
                        s7.negate(path_remainder(s7, second)),
                    )
                    j_difference = s7.add(
                        three_leaf_formula(s7, first),
                        s7.negate(three_leaf_formula(s7, second)),
                    )
                    k_difference = four_leaf_five_edge_formula(first, probe) - four_leaf_five_edge_formula(second, probe)
                    # (35)--(36) are the result after imposing the path x^3
                    # identity.  Pairs already separated there need no later
                    # separator.
                    if coefficient(w_difference, 3) != 0:
                        continue
                    assert coefficient(j_difference, 4) == (
                        (a2 - a2_prime) * (q - 1) * (m - 2) // 2
                        - (m - q - 1)
                    )
                    assert k_difference == (
                        (a2 - a2_prime) * (m - 2) * (m + q) * (q - 1) // 6
                        + (m + q) * (q - m + 1) // 2
                    )
                    assert coefficient(w_difference, 2) == 0
                    count_swap_pairs += 1

    collisions = [
        values
        for values in recovery_buckets.values()
        if len({description[2] for description in values}) > 1
    ]
    assert not collisions, collisions[:1]
    print(
        "PASS "
        f"checked_descriptions={checked} "
        f"fixed_count_pairs={fixed_count_pairs} "
        f"count_swap_pairs={count_swap_pairs} "
        "recovery_collisions=0"
    )


if __name__ == "__main__":
    main()
