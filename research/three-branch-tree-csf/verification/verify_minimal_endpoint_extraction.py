"""Exact control for the minimal-endpoint extraction lemma.

For every canonical three-branch description through ``max_order``, compute
the power-sum expansion of the trunk alternating sum directly from edge
subsets, differentiate at the predicted degree, and compare with the sum of
the chromatic symmetric functions of the minimum-order endpoint spiders.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


PROBE = Path(__file__).resolve().parent / "probe_three_branch_cut_profiles.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("three_branch_probe", PROBE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PROBE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def component_partition(adjacency, kept_edges):
    seen = set()
    sizes = []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            for neighbour, edge_index in adjacency[current]:
                if edge_index in kept_edges and neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return tuple(sorted(sizes, reverse=True))


def power_sum_expansion(adjacency, allowed_edges, forbidden_full_set=()):
    edges = tuple(allowed_edges)
    forbidden = set(forbidden_full_set)
    result = {}
    for mask in range(1 << len(edges)):
        kept = {edges[index] for index in range(len(edges)) if mask >> index & 1}
        if forbidden and forbidden <= kept:
            continue
        partition = component_partition(adjacency, kept)
        result[partition] = result.get(partition, 0) + (-1) ** len(kept)
    return {partition: value for partition, value in result.items() if value}


def derivative(expansion, part):
    result = {}
    for partition, coefficient in expansion.items():
        multiplicity = partition.count(part)
        if not multiplicity:
            continue
        reduced = list(partition)
        reduced.remove(part)
        key = tuple(reduced)
        result[key] = result.get(key, 0) + coefficient * multiplicity
    return {partition: value for partition, value in result.items() if value}


def component_vertices(adjacency, cut_edge, start):
    seen = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbour, edge_index in adjacency[current]:
            if edge_index != cut_edge and neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return seen


def induced_expansion(adjacency, vertices):
    ordered = sorted(vertices)
    vertex_map = {vertex: index for index, vertex in enumerate(ordered)}
    original_edges = sorted(
        {
            edge_index
            for vertex in vertices
            for neighbour, edge_index in adjacency[vertex]
            if neighbour in vertices
        }
    )
    edge_map = {edge: index for index, edge in enumerate(original_edges)}
    induced = [[] for _ in ordered]
    for vertex in ordered:
        for neighbour, edge_index in adjacency[vertex]:
            if neighbour in vertices and vertex < neighbour:
                first = vertex_map[vertex]
                second = vertex_map[neighbour]
                new_edge = edge_map[edge_index]
                induced[first].append((second, new_edge))
                induced[second].append((first, new_edge))
    return power_sum_expansion(induced, range(len(original_edges)))


def add_scaled(target, source, scale):
    for partition, coefficient in source.items():
        target[partition] = target.get(partition, 0) + scale * coefficient
        if not target[partition]:
            del target[partition]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=12)
    args = parser.parse_args()
    probe = load_probe()

    checked = 0
    for order in range(8, args.max_order + 1):
        for description in probe.descriptions(order):
            adjacency, edges = probe.tree(description)
            trunk_edges = description[0] + description[1]
            alternating = power_sum_expansion(
                adjacency,
                range(len(edges)),
                range(trunk_edges),
            )

            left = component_vertices(adjacency, 0, 0)
            right_center = trunk_edges
            right = component_vertices(
                adjacency,
                trunk_edges - 1,
                right_center,
            )
            minimum = min(len(left), len(right))
            derivative_order = order - minimum
            actual = derivative(alternating, derivative_order)

            expected = {}
            sign = (-1) ** (derivative_order - 1)
            for endpoint in (left, right):
                if len(endpoint) == minimum:
                    add_scaled(
                        expected,
                        induced_expansion(adjacency, endpoint),
                        sign,
                    )
            if actual != expected:
                raise AssertionError(
                    f"failed for n={order}, description={description}: "
                    f"actual={actual}, expected={expected}"
                )
            checked += 1
        print(f"n={order}: PASS")
    print(f"checked_descriptions={checked}")


if __name__ == "__main__":
    main()
