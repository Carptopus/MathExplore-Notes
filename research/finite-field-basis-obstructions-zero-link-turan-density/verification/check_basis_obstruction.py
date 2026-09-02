"""Exact sanity checks for the finite-field basis obstruction.

This script is calibration evidence only.  The general theorem is proved
symbolically in the accompanying Markdown record.
"""

from itertools import combinations, permutations, product


def rank_f2(vectors: tuple[int, ...], dimension: int) -> int:
    rows = list(vectors)
    rank = 0
    for bit in range(dimension - 1, -1, -1):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] >> bit & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] >> bit & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def basis_edges_f2(dimension: int) -> set[tuple[int, ...]]:
    vertices = range(1, 1 << dimension)
    return {
        edge
        for edge in combinations(vertices, dimension)
        if rank_f2(edge, dimension) == dimension
    }


def weak_chromatic_number(vertices: tuple[int, ...], edges: set[tuple[int, ...]]) -> int:
    for colors in range(1, len(vertices) + 1):
        for assignment in product(range(colors), repeat=len(vertices)):
            color = dict(zip(vertices, assignment, strict=True))
            if all(len({color[v] for v in edge}) > 1 for edge in edges):
                return colors
    raise AssertionError("finite hypergraph must be colorable")


def contains_complete_3graph(edges: set[tuple[int, ...]], order: int) -> bool:
    vertices = sorted({v for edge in edges for v in edge})
    return any(
        all(tuple(sorted(edge)) in edges for edge in combinations(subset, 3))
        for subset in combinations(vertices, order)
    )


def has_homomorphism(
    source_vertices: tuple[int, ...],
    source_edges: set[tuple[int, ...]],
    target_vertices: tuple[int, ...],
    target_edges: set[tuple[int, ...]],
) -> bool:
    return any(
        all(tuple(sorted(mapping[source_vertices.index(v)] for v in edge)) in target_edges
            for edge in source_edges)
        for mapping in product(target_vertices, repeat=len(source_vertices))
    )


def main() -> None:
    edges = basis_edges_f2(3)
    all_triples = set(combinations(range(1, 8), 3))
    dependent = all_triples - edges

    assert len(edges) == 28
    assert len(dependent) == 7
    assert all(rank_f2(edge, 3) == 2 for edge in dependent)
    assert weak_chromatic_number(tuple(range(1, 8)), edges) == 3
    assert contains_complete_3graph(edges, 4)
    assert not contains_complete_3graph(edges, 5)

    # The Fano plane itself is not an obstruction: a relabelling sends all
    # seven Fano lines to basis triples.  This guards against mistaking
    # non-isomorphism for nonexistence of a hypergraph homomorphism.
    fano_lines = {
        tuple(sorted(edge))
        for edge in ((0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
                     (1, 4, 6), (2, 3, 6), (2, 4, 5))
    }
    fano_target = {tuple(v - 1 for v in edge) for edge in edges}
    assert any(
        all(tuple(sorted(permutation[v] for v in edge)) in fano_target
            for edge in fano_lines)
        for permutation in permutations(range(7))
    )

    # The six-edge suspension of K_4 is an obstruction.  It is deliberately
    # retained only as a boundary calibration: it reduces to the classical
    # graph three-colour obstruction and is not claimed as a new application.
    suspended_k4 = {
        tuple(sorted((0, a, b)))
        for a, b in combinations(range(1, 5), 2)
    }
    assert not has_homomorphism(
        tuple(range(5)), suspended_k4, tuple(range(1, 8)), edges
    )

    # A genuinely three-uniform six-vertex obstruction H_*: with vertices
    # c=0, A={1,2,3}, B={4,5}, take cAB, cB, and A.  Every link graph is
    # 3-colourable, so positivity is not inherited from a suspended
    # non-tripartite graph.
    h_star = {
        tuple(sorted((0, a, b)))
        for a in (1, 2, 3)
        for b in (4, 5)
    } | {(0, 4, 5), (1, 2, 3)}
    assert len(h_star) == 8
    assert not has_homomorphism(
        tuple(range(6)), h_star, tuple(range(1, 8)), edges
    )
    for vertex in range(6):
        link_edges = {
            tuple(v for v in edge if v != vertex)
            for edge in h_star
            if vertex in edge
        }
        link_vertices = tuple(v for v in range(6) if v != vertex)
        assert weak_chromatic_number(link_vertices, link_edges) <= 3
    h_star_dual = {
        tuple(sorted(set(range(6)) - set(edge)))
        for edge in h_star
    }
    assert len(h_star_dual) == 8
    assert not has_homomorphism(
        tuple(range(6)), h_star_dual, tuple(range(1, 8)), edges
    )
    for vertex in range(6):
        link_edges = {
            tuple(v for v in edge if v != vertex)
            for edge in h_star_dual
            if vertex in edge
        }
        link_vertices = tuple(v for v in range(6) if v != vertex)
        assert weak_chromatic_number(link_vertices, link_edges) <= 3

    print("PASS: B_2(3) has 28 basis triples and seven Fano-line nonedges")
    print("PASS: weak chromatic number is 3")
    print("PASS: K_4^(3) maps into B_2(3), while K_5^(3) does not")
    print("PASS: the Fano plane maps into B_2(3)")
    print("PASS: the six-edge suspension of K_4 does not map into B_2(3)")
    print("PASS: H_* has no homomorphism to B_2(3), while every link is 3-colourable")
    print("PASS: the same statements hold for the six-point dual H_*^*")


if __name__ == "__main__":
    main()
