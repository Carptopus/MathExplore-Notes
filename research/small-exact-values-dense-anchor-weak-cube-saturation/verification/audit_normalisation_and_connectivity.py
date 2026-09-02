"""Independently audit the structural facts used by the exact search.

This checker does not call the bit-mask closure implementation.  It verifies
with NetworkX that the standard graph is Q3, that its automorphism group is
edge-transitive, and that deleting any one cube edge leaves a biconnected
graph.  These are exactly the facts behind first-witness normalisation and the
biconnectivity filter in ``exact_first_cube_enumeration.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx


def standard_cube() -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(8))
    graph.add_edges_from(
        (vertex, vertex ^ bit)
        for vertex in range(8)
        for bit in (1, 2, 4)
        if vertex < (vertex ^ bit)
    )
    return graph


def normalised_edge(edge: tuple[int, int]) -> tuple[int, int]:
    return tuple(sorted(edge))


def main() -> None:
    cube = standard_cube()
    canonical = nx.convert_node_labels_to_integers(nx.hypercube_graph(3))
    assert nx.is_isomorphic(cube, canonical)
    assert cube.number_of_nodes() == 8
    assert cube.number_of_edges() == 12
    assert set(dict(cube.degree()).values()) == {3}

    matcher = nx.algorithms.isomorphism.GraphMatcher(cube, cube)
    automorphisms = list(matcher.isomorphisms_iter())
    reference_edge = (0, 1)
    edge_orbit = {
        normalised_edge((mapping[reference_edge[0]], mapping[reference_edge[1]]))
        for mapping in automorphisms
    }
    all_edges = {normalised_edge(edge) for edge in cube.edges()}
    assert edge_orbit == all_edges

    deletion_checks: dict[str, bool] = {}
    for edge in sorted(all_edges):
        remainder = cube.copy()
        remainder.remove_edge(*edge)
        deletion_checks[f"{edge[0]}-{edge[1]}"] = nx.is_biconnected(remainder)
    assert all(deletion_checks.values())

    result = {
        "graph": "Q3",
        "vertices": cube.number_of_nodes(),
        "edges": cube.number_of_edges(),
        "automorphism_count": len(automorphisms),
        "reference_edge_orbit_size": len(edge_orbit),
        "edge_transitive": edge_orbit == all_edges,
        "all_single_edge_deletions_biconnected": all(deletion_checks.values()),
        "deletion_checks": deletion_checks,
    }
    output = Path(__file__).parent / "results" / "normalisation-connectivity-audit.json"
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
