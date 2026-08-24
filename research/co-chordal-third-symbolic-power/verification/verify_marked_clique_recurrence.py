"""Finite destructive check of the marked-clique induction identities.

The mathematical proof is in the accompanying manuscript. This script does
not prove it; it checks every state M_d(H,F) with d=3,4,5, n<=max_n,
and |F|=5-d (subfamilies are represented by repetitions/removals elsewhere)
against the exact left/right split formulas and B subset A condition.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import networkx as nx

from scan_s3_chordal_capacity import bounded_compositions


Exponent = tuple[int, ...]
Clique = tuple[int, ...]


def is_clique(graph: nx.Graph, vertices) -> bool:
    vertices = tuple(vertices)
    return all(graph.has_edge(a, b) for a, b in itertools.combinations(vertices, 2))


def all_nonempty_cliques(graph: nx.Graph) -> list[Clique]:
    nodes = tuple(sorted(graph.nodes()))
    return [
        subset
        for size in range(1, len(nodes) + 1)
        for subset in itertools.combinations(nodes, size)
        if is_clique(graph, subset)
    ]


def maximal_cliques(graph: nx.Graph) -> list[Clique]:
    return [tuple(sorted(clique)) for clique in nx.find_cliques(graph)]


def state_generators(
    graph: nx.Graph,
    marked: tuple[Clique, ...],
    degree: int,
    ambient_n: int,
) -> set[Exponent]:
    vertices = set(graph.nodes())
    maximal = maximal_cliques(graph)
    return {
        exponent
        for exponent in bounded_compositions(degree, ambient_n)
        if all(exponent[v] == 0 for v in range(ambient_n) if v not in vertices)
        and all(sum(exponent[v] for v in clique) <= 2 for clique in maximal)
        and all(sum(exponent[v] for v in clique) <= 1 for clique in marked)
    }


def simplicial_vertices(graph: nx.Graph) -> list[int]:
    return [
        vertex
        for vertex in graph.nodes()
        if is_clique(graph, [vertex, *graph.neighbors(vertex)])
    ]


def normalized_marked(items) -> tuple[Clique, ...]:
    return tuple(sorted({tuple(sorted(item)) for item in items if item}))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    checked_states = 0
    failures = []
    for atlas_index, graph in enumerate(nx.graph_atlas_g()):
        n = graph.number_of_nodes()
        if n < 2 or n > args.max_n or not nx.is_chordal(graph):
            continue
        if graph.number_of_edges() == n * (n - 1) // 2:
            continue
        cliques = all_nonempty_cliques(graph)
        for degree in (3, 4, 5):
            max_mark_count = 5 - degree
            families = itertools.chain.from_iterable(
                itertools.combinations(cliques, mark_count)
                for mark_count in range(max_mark_count + 1)
            )
            for marked_raw in families:
                marked = normalized_marked(marked_raw)
                simplicial = simplicial_vertices(graph)
                candidates = [
                    vertex
                    for vertex in simplicial
                    if sum(vertex in clique for clique in marked) <= 1
                ]
                if not candidates:
                    failures.append({"kind": "no_vertex", "atlas_index": atlas_index, "degree": degree, "marked": marked})
                    break
                vertex = min(candidates)
                unique_maximal = [clique for clique in maximal_cliques(graph) if vertex in clique]
                if len(unique_maximal) != 1:
                    failures.append({"kind": "not_unique_maximal", "atlas_index": atlas_index, "degree": degree, "vertex": vertex})
                    break
                q_clique = unique_maximal[0]
                generators = state_generators(graph, marked, degree, n)
                actual_b = {a for a in generators if a[vertex] == 0}
                actual_a = {
                    tuple(value - (1 if i == vertex else 0) for i, value in enumerate(a))
                    for a in generators
                    if a[vertex] >= 1
                }

                graph_b = graph.copy()
                graph_b.remove_node(vertex)
                marked_b = normalized_marked(
                    tuple(v for v in clique if v != vertex) for clique in marked
                )
                expected_b = state_generators(graph_b, marked_b, degree, n)

                containing = [clique for clique in marked if vertex in clique]
                if not containing:
                    expected_a = state_generators(
                        graph,
                        normalized_marked((*marked, q_clique)),
                        degree - 1,
                        n,
                    )
                else:
                    s_clique = set(containing[0])
                    graph_a = graph.subgraph(set(graph.nodes()) - s_clique).copy()
                    marked_a = [
                        tuple(v for v in clique if v not in s_clique)
                        for clique in marked
                        if clique != containing[0]
                    ]
                    marked_a.append(tuple(v for v in q_clique if v not in s_clique))
                    expected_a = state_generators(
                        graph_a,
                        normalized_marked(marked_a),
                        degree - 1,
                        n,
                    )

                inclusion = all(
                    any(all(c[i] <= b[i] for i in range(n)) for c in actual_a)
                    for b in actual_b
                )
                checked_states += 1
                if actual_a != expected_a or actual_b != expected_b or not inclusion:
                    failures.append(
                        {
                            "kind": "split_identity",
                            "atlas_index": atlas_index,
                            "degree": degree,
                            "marked": marked,
                            "vertex": vertex,
                            "actual_a": len(actual_a),
                            "expected_a": len(expected_a),
                            "actual_b": len(actual_b),
                            "expected_b": len(expected_b),
                            "inclusion": inclusion,
                        }
                    )
                    break
            if failures:
                break
        if failures:
            break

    result = {
        "scope": "all noncomplete nonisomorphic chordal atlas graphs through max_n; exact d=3,4,5 marked-clique split identities",
        "max_n": args.max_n,
        "checked_states": checked_states,
        "failure_count": len(failures),
        "first_failure": failures[0] if failures else None,
        "claim_boundary": "finite destructive verification of proof identities; not a proof of the general theorem",
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
