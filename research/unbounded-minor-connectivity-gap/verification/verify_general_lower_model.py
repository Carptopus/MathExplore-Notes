"""Verify the explicit floor(9t/2)-connected minor model in M12[I_t]."""

from __future__ import annotations

import argparse

import networkx as nx


Vertex = tuple[int, int]


def build_m12() -> nx.Graph:
    """Return the labelled 12-vertex Mader graph used in the manuscript."""
    graph = nx.Graph()
    graph.add_nodes_from(range(12))
    graph.add_edges_from(
        (u - 1, v - 1)
        for u, v in [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 7),
        ]
    )
    for axis in (5, 6):
        for cycle_vertex in (1, 2, 3, 4):
            graph.add_edge(axis - 1, cycle_vertex - 1)
    graph.add_edge(4, 5)
    for axis in (11, 12):
        for cycle_vertex in (7, 8, 9, 10):
            graph.add_edge(axis - 1, cycle_vertex - 1)
    graph.add_edge(10, 11)
    graph.add_edges_from((0, vertex - 1) for vertex in (8, 9, 10))
    graph.add_edges_from((6, vertex - 1) for vertex in (2, 3, 4))
    return graph


def independent_blowup(graph: nx.Graph, multiplicity: int) -> nx.Graph:
    result = nx.Graph()
    result.add_nodes_from(
        (vertex, clone)
        for vertex in graph.nodes()
        for clone in range(multiplicity)
    )
    for left, right in graph.edges():
        result.add_edges_from(
            ((left, left_clone), (right, right_clone))
            for left_clone in range(multiplicity)
            for right_clone in range(multiplicity)
        )
    return result


def quotient(graph: nx.Graph, branch_sets: list[set[Vertex]]) -> nx.Graph:
    """Return the full branch-set quotient after validating the model."""
    occupied: set[Vertex] = set()
    for index, branch_set in enumerate(branch_sets):
        if not branch_set:
            raise ValueError(f"branch set {index} is empty")
        if not occupied.isdisjoint(branch_set):
            raise ValueError(f"branch set {index} overlaps an earlier branch set")
        if not set(branch_set).issubset(graph):
            raise ValueError(f"branch set {index} contains a vertex outside the graph")
        if not nx.is_connected(graph.subgraph(branch_set)):
            raise ValueError(f"branch set {index} is disconnected")
        occupied.update(branch_set)

    result = nx.Graph()
    result.add_nodes_from(range(len(branch_sets)))
    for left_index, left in enumerate(branch_sets):
        for right_index in range(left_index + 1, len(branch_sets)):
            right = branch_sets[right_index]
            if any(graph.has_edge(u, v) for u in left for v in right):
                result.add_edge(left_index, right_index)
    return result


def branch_sets(t: int) -> list[set[Vertex]]:
    if t < 2:
        raise ValueError("the construction requires t >= 2")

    left_count = t // 2
    right_count = t - left_count
    result: list[set[Vertex]] = [
        {(0, i), (6, i), (7, i), (10, i), (11, i)}
        for i in range(left_count)
    ]
    result.extend({(1, i), (6, left_count + i)} for i in range(right_count))
    occupied = set().union(*result)
    result.extend(
        {(base, clone)}
        for base in range(6)
        for clone in range(t)
        if (base, clone) not in occupied
    )
    return result


def structural_connectivity(minor: nx.Graph, t: int) -> int:
    """Evaluate connectivity from the complement components in the proof."""
    complement = nx.complement(minor)
    orders = sorted(len(component) for component in nx.connected_components(complement))
    left_count = t // 2
    right_count = t - left_count
    expected_orders = sorted(
        [1] * t + [t, t, 2 * t - left_count, 2 * t - right_count]
    )
    if orders != expected_orders:
        raise AssertionError(
            f"unexpected complement-component orders: {orders} != {expected_orders}"
        )
    return minor.number_of_nodes() - max(orders)


def verify(t: int) -> tuple[int, int, int]:
    base = build_m12()
    if base.number_of_edges() != 32:
        raise AssertionError("the labelled M12 graph must have 32 edges")
    if sorted(dict(base.degree()).values()) != [5] * 10 + [7] * 2:
        raise AssertionError("the labelled M12 degree sequence is wrong")

    graph = independent_blowup(base, t)
    if graph.number_of_nodes() != 12 * t or graph.number_of_edges() != 32 * t * t:
        raise AssertionError("the independent blow-up has the wrong order or size")
    if min(dict(graph.degree()).values()) != 5 * t:
        raise AssertionError("the independent blow-up has the wrong minimum degree")

    model = branch_sets(t)
    minor = quotient(graph, model)
    expected_connectivity = (9 * t) // 2
    if len(model) != 6 * t or minor.number_of_nodes() != 6 * t:
        raise AssertionError("the branch-set model has the wrong order")
    if min(dict(minor.degree()).values()) != expected_connectivity:
        raise AssertionError("the quotient has the wrong minimum degree")
    if structural_connectivity(minor, t) != expected_connectivity:
        raise AssertionError("the complement calculation gives the wrong connectivity")
    if nx.node_connectivity(minor) != expected_connectivity:
        raise AssertionError("NetworkX connectivity disagrees with the structural calculation")
    return minor.number_of_nodes(), minor.number_of_edges(), expected_connectivity


def run_negative_controls() -> None:
    graph = independent_blowup(build_m12(), 2)
    controls = [
        ([{(0, 0), (6, 0)}], "disconnected"),
        ([{(0, 0)}, {(0, 0)}], "overlaps"),
    ]
    for model, expected_fragment in controls:
        try:
            quotient(graph, model)
        except ValueError as exc:
            if expected_fragment not in str(exc):
                raise AssertionError(f"unexpected negative-control failure: {exc}") from exc
        else:
            raise AssertionError(f"negative control did not reject {expected_fragment} model")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-t", type=int, default=2)
    parser.add_argument("--max-t", type=int, default=8)
    args = parser.parse_args()
    if args.min_t < 2 or args.max_t < args.min_t:
        raise ValueError("require 2 <= min-t <= max-t")

    run_negative_controls()
    print("negative_controls=PASS")
    for t in range(args.min_t, args.max_t + 1):
        vertices, edges, connectivity = verify(t)
        print(
            f"t={t} branch_sets={vertices} quotient_edges={edges} "
            f"connectivity={connectivity} expected={(9 * t) // 2}"
        )


if __name__ == "__main__":
    main()
