from __future__ import annotations

import argparse
import hashlib
from collections import deque
from itertools import combinations
from pathlib import Path

import networkx as nx


EXPECTED_GRAPH8_SHA256 = "0002354F1AB3344A2706626A037AD15367BF23A2163AA68F552C3A169CA9A036"
EXPECTED_ORDER_EIGHT_FAILURES = {"G?B@vG", "G?`crg", "G?aJeW", "GCQRTg"}
GRAPH8_OFFICIAL_URL = "https://users.cecs.anu.edu.au/~bdm/data/graph8c.g6"


def polynomial_add(*polynomials: list[int]) -> list[int]:
    size = max(map(len, polynomials))
    return [
        sum(poly[index] if index < len(poly) else 0 for poly in polynomials)
        for index in range(size)
    ]


def polynomial_multiply(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            result[left_degree + right_degree] += left_coefficient * right_coefficient
    return result


def family_formula(d: int, left_complete: int, right_triangle: int) -> list[int]:
    if d < 2:
        raise ValueError("the family is frozen for d >= 2")
    a2 = [0, 1, 2, 1]
    a3 = [0, 1, 3, 3, 1]
    cluster_sum = [0, 7, 7 + left_complete + right_triangle, 5, 1]
    internal_path = [0] + [d - degree for degree in range(1, d)]
    path_prefix = [0] + [1] * (d - 1)
    spanning = [0] * (d - 1) + polynomial_multiply(a2, a3)
    polynomial = polynomial_add(
        cluster_sum,
        internal_path,
        polynomial_multiply(polynomial_add(a2, a3), path_prefix),
        spanning,
    )
    return polynomial[1:]


def stated_closed_form(d: int, left_complete: int, right_triangle: int) -> list[int]:
    n = d + 6
    return (
        [n, n + 1 + left_complete + right_triangle, n + 3]
        + [n + 6 - degree for degree in range(4, d + 3)]
        + [11, 10, 5, 1]
    )


def build_family(d: int, left_complete: int, right_triangle: int) -> nx.Graph:
    graph = nx.Graph()
    path = list(range(d + 1))
    graph.add_edges_from(zip(path, path[1:]))
    u, v = path[0], path[-1]
    next_vertex = d + 1

    left_vertices = [next_vertex, next_vertex + 1, next_vertex + 2]
    next_vertex += 3
    graph.add_edges_from((u, vertex) for vertex in left_vertices)
    graph.add_edges_from(
        [(left_vertices[0], left_vertices[2]), (left_vertices[1], left_vertices[2])]
    )
    if left_complete:
        graph.add_edge(left_vertices[0], left_vertices[1])

    right_vertices = [next_vertex, next_vertex + 1]
    graph.add_edges_from((v, vertex) for vertex in right_vertices)
    if right_triangle:
        graph.add_edge(*right_vertices)
    return graph


def connected_set_coefficients_expansion(graph: nx.Graph) -> list[int]:
    """Enumerate connected masks by boundary expansion."""
    nodes = list(graph)
    index = {node: position for position, node in enumerate(nodes)}
    adjacency = [0] * len(nodes)
    for left, right in graph.edges():
        left_index, right_index = index[left], index[right]
        adjacency[left_index] |= 1 << right_index
        adjacency[right_index] |= 1 << left_index

    seen = bytearray(1 << len(nodes))
    queue: deque[int] = deque()
    coefficients = [0] * (len(nodes) + 1)
    for vertex in range(len(nodes)):
        mask = 1 << vertex
        seen[mask] = 1
        queue.append(mask)

    while queue:
        mask = queue.popleft()
        coefficients[mask.bit_count()] += 1
        boundary = 0
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            boundary |= adjacency[bit.bit_length() - 1]
            remaining -= bit
        boundary &= ~mask
        while boundary:
            bit = boundary & -boundary
            extended = mask | bit
            if not seen[extended]:
                seen[extended] = 1
                queue.append(extended)
            boundary -= bit
    return coefficients[1:]


def connected_set_coefficients_direct(graph: nx.Graph) -> list[int]:
    """Independent subset-by-subset induced-connectivity check."""
    nodes = list(graph)
    return [
        sum(nx.is_connected(graph.subgraph(subset)) for subset in combinations(nodes, size))
        for size in range(1, len(nodes) + 1)
    ]


def connected_set_coefficients_bitmask(graph: nx.Graph) -> list[int]:
    """Check every nonempty subset with an independent bitmask flood fill."""
    nodes = list(graph)
    index = {node: position for position, node in enumerate(nodes)}
    adjacency = [0] * len(nodes)
    for left, right in graph.edges():
        left_index, right_index = index[left], index[right]
        adjacency[left_index] |= 1 << right_index
        adjacency[right_index] |= 1 << left_index

    coefficients = [0] * (len(nodes) + 1)
    for mask in range(1, 1 << len(nodes)):
        reached = mask & -mask
        frontier = reached
        while frontier:
            bit = frontier & -frontier
            frontier -= bit
            neighbors = adjacency[bit.bit_length() - 1] & mask & ~reached
            reached |= neighbors
            frontier |= neighbors
        if reached == mask:
            coefficients[mask.bit_count()] += 1
    return coefficients[1:]


def is_unimodal(coefficients: list[int]) -> bool:
    descending = False
    for left, right in zip(coefficients, coefficients[1:]):
        if right < left:
            descending = True
        elif right > left and descending:
            return False
    return True


def verify_families() -> None:
    for d in range(2, 65):
        graphs = []
        for left_complete in (0, 1):
            for right_triangle in (0, 1):
                expected = stated_closed_form(d, left_complete, right_triangle)
                assert family_formula(d, left_complete, right_triangle) == expected
                assert expected[d + 1] == 10
                assert expected[d + 2] == 11
                assert not is_unimodal(expected)
                if d <= 8:
                    graph = build_family(d, left_complete, right_triangle)
                    graphs.append(graph)
                    assert graph.number_of_nodes() == d + 6
                    assert graph.number_of_edges() == d + 7 + left_complete + right_triangle
                    assert nx.is_connected(graph)
                    expansion = connected_set_coefficients_expansion(graph)
                    assert expansion == expected
                    if d <= 5:
                        direct = connected_set_coefficients_direct(graph)
                        assert direct == expected
        if graphs:
            assert all(
                not nx.is_isomorphic(graph, other)
                for index, graph in enumerate(graphs)
                for other in graphs[index + 1 :]
            )


def verify_orders_through_seven() -> None:
    atlas = nx.graph_atlas_g()
    for order in range(1, 8):
        for graph in atlas:
            if len(graph) != order or not nx.is_connected(graph):
                continue
            if graph.number_of_edges() < order:
                continue
            expansion = connected_set_coefficients_expansion(graph)
            direct = connected_set_coefficients_direct(graph)
            assert expansion == direct
            assert is_unimodal(expansion)


def verify_order_eight_catalog(path: Path) -> None:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest().upper()
    assert digest == EXPECTED_GRAPH8_SHA256, (digest, EXPECTED_GRAPH8_SHA256)
    lines = [line for line in raw.splitlines() if line and not line.startswith(b">>")]
    assert len(lines) == 11_117

    eligible = 0
    failures: dict[str, list[int]] = {}
    for line in lines:
        graph = nx.from_graph6_bytes(line)
        assert len(graph) == 8 and nx.is_connected(graph)
        if graph.number_of_edges() < 8:
            continue
        eligible += 1
        coefficients = connected_set_coefficients_expansion(graph)
        bitmask = connected_set_coefficients_bitmask(graph)
        assert bitmask == coefficients
        if not is_unimodal(coefficients):
            code = line.decode("ascii")
            direct = connected_set_coefficients_direct(graph)
            assert direct == coefficients
            failures[code] = coefficients

    assert eligible == 11_094
    assert set(failures) == EXPECTED_ORDER_EIGHT_FAILURES
    family_graphs = [
        build_family(2, left_complete, right_triangle)
        for left_complete in (0, 1)
        for right_triangle in (0, 1)
    ]
    for code in EXPECTED_ORDER_EIGHT_FAILURES:
        graph = nx.from_graph6_bytes(code.encode("ascii"))
        assert any(nx.is_isomorphic(graph, family) for family in family_graphs)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph8c",
        type=Path,
        help="McKay graph8c.g6 catalog with the frozen SHA-256",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    verify_families()
    verify_orders_through_seven()
    print("PASS: four pairwise nonisomorphic counterexample families for every n >= 8")
    print("PASS: closed form checked through d = 64; boundary expansion agrees through d = 8")
    print("PASS: independent subset enumeration agrees through d = 5")
    if args.graph8c is None:
        print("SKIP: order-eight full catalog (pass --graph8c PATH to enable)")
    else:
        verify_order_eight_catalog(args.graph8c)
        print("PASS: all 11,117 connected order-eight graphs checked by two algorithms; exactly four failures")
        print(f"SOURCE: {GRAPH8_OFFICIAL_URL}")


if __name__ == "__main__":
    main()


