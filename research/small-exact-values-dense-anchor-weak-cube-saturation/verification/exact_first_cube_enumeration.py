"""Complete K8/K9/K10 search after normalising the first Q3-e witness."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from probe_q3_weak_saturation import BASE_EDGES, closure, cube_masks


def is_two_connected(n: int, edge_set: list[tuple[int, int]]) -> bool:
    adjacency = [0] * n
    for a, b in edge_set:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    for removed in range(n):
        allowed = ((1 << n) - 1) ^ (1 << removed)
        start = (allowed & -allowed).bit_length() - 1
        reached = 1 << start
        frontier = reached
        while frontier:
            vertex_bit = frontier & -frontier
            frontier ^= vertex_bit
            vertex = vertex_bit.bit_length() - 1
            new = adjacency[vertex] & allowed & ~reached
            reached |= new
            frontier |= new
        if reached != allowed:
            return False
    return True


def solve(n: int, maximum_edges: int, structural_filter: bool) -> dict[str, object]:
    edges, cubes = cube_masks(n)
    edge_index = {edge: i for i, edge in enumerate(edges)}
    full = (1 << len(edges)) - 1

    missing_first = (0, 1)
    core = [edge for edge in BASE_EDGES if edge != missing_first]
    core_mask = sum(1 << edge_index[edge] for edge in core)
    optional = [
        edge
        for edge in edges
        if edge not in core and edge != missing_first
    ]

    enumerated_by_size: dict[int, int] = {}
    tested_by_size: dict[int, int] = {}
    for total_edges in range(len(core), maximum_edges + 1):
        extra_count = total_edges - len(core)
        enumerated = 0
        tested = 0
        for extra in itertools.combinations(optional, extra_count):
            enumerated += 1
            candidate_edges = core + list(extra)
            if structural_filter and not is_two_connected(n, candidate_edges):
                continue
            tested += 1
            mask = core_mask | sum(1 << edge_index[edge] for edge in extra)
            if closure(mask, cubes, full) == full:
                enumerated_by_size[total_edges] = enumerated
                tested_by_size[total_edges] = tested
                return {
                    "n": n,
                    "minimum": total_edges,
                    "normalisation": {
                        "first_cube": list(BASE_EDGES),
                        "first_missing_edge": missing_first,
                    },
                    "structural_filter": structural_filter,
                    "enumerated_by_size": enumerated_by_size,
                    "tested_by_size": tested_by_size,
                    "witness": candidate_edges,
                }
        enumerated_by_size[total_edges] = enumerated
        tested_by_size[total_edges] = tested
    return {
        "n": n,
        "minimum": None,
        "searched_through": maximum_edges,
        "structural_filter": structural_filter,
        "enumerated_by_size": enumerated_by_size,
        "tested_by_size": tested_by_size,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(8, 9, 10, 11), required=True)
    parser.add_argument("--maximum-edges", type=int, required=True)
    parser.add_argument("--structural-filter", action="store_true")
    args = parser.parse_args()
    result = solve(args.n, args.maximum_edges, args.structural_filter)
    output = Path(__file__).parent / "results" / f"exact-first-cube-n{args.n}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
