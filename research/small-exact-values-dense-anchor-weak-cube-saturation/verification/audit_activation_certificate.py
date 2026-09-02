"""Independent graph-level audit of a sequential Q_3 certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import networkx as nx


def edge(item: list[int]) -> tuple[int, int]:
    return tuple(sorted((int(item[0]), int(item[1]))))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text(encoding="utf-8"))
    n = int(data["n"])
    current = {edge(item) for item in data["initial_edges"]}
    cube = nx.cubical_graph()
    initial_graph = nx.Graph()
    initial_graph.add_nodes_from(range(n))
    initial_graph.add_edges_from(current)
    initial_contains_cube = nx.algorithms.isomorphism.GraphMatcher(
        initial_graph, cube
    ).subgraph_is_monomorphic()
    assert not initial_contains_cube

    for expected_step, item in enumerate(data["steps"], start=1):
        assert int(item["step"]) == expected_step
        added = edge(item["added_edge"])
        cube_edges = {edge(value) for value in item["cube_edges_after_addition"]}
        assert added not in current
        assert added in cube_edges
        assert cube_edges - {added} <= current
        graph = nx.Graph()
        graph.add_edges_from(cube_edges)
        assert graph.number_of_nodes() == 8
        assert graph.number_of_edges() == 12
        assert nx.is_isomorphic(graph, cube)
        current.add(added)

    expected = {tuple(pair) for pair in __import__("itertools").combinations(range(n), 2)}
    assert current == expected
    print(
        json.dumps(
            {
                "certificate": str(args.certificate),
                "steps": len(data["steps"]),
                "final_edges": len(current),
                "initial_q3_free": not initial_contains_cube,
                "verified": True,
            }
        )
    )


if __name__ == "__main__":
    main()
