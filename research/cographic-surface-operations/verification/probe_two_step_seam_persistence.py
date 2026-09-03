"""Bounded falsification probe for seam persistence.

This searches only for a counterexample.  A NO_HIT result is finite calibration
and is never evidence for the general seam-persistence statement.
"""

from __future__ import annotations

import argparse
import sys
import sys
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from check_vertex_split_nonclosure import (  # noqa: E402
    link_cycle,
    separating_nonfacial_triangles,
    split_vertex,
)
from verify_nonorientable_triangle_sum_family import (  # noqa: E402
    INITIAL_FACES,
    Face,
    face_adjacencies,
    graph_from_faces,
    triangle_sum,
    verify_all_bonds,
    verify_closed_triangulation,
    verify_three_connectivity,
)


def vertex_splits(faces: set[Face]):
    for vertex in sorted(set().union(*faces)):
        cycle = link_cycle(faces, vertex)
        degree = len(cycle)
        for left_index, right_index in combinations(range(degree), 2):
            span = min(
                right_index - left_index,
                degree - right_index + left_index,
            )
            if span >= 2:
                yield split_vertex(faces, vertex, left_index, right_index)


def has_u(faces: set[Face]) -> bool:
    vertices, edges, neighbors = graph_from_faces(faces)
    try:
        verify_all_bonds(vertices, edges, neighbors, face_adjacencies(faces))
    except RuntimeError:
        return False
    return True


def canonical_faces(faces: set[Face]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(tuple(sorted(face)) for face in faces))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=400)
    args = parser.parse_args()
    if not 1 <= args.limit <= 500:
        raise SystemExit("limit must be between 1 and 500")

    base = triangle_sum(set(INITIAL_FACES), set(INITIAL_FACES))
    first_positive = [faces for faces in vertex_splits(base) if has_u(faces)]
    if len(first_positive) != 63:
        raise AssertionError(("unexpected first-step positive count", len(first_positive)))

    seen: set[tuple[tuple[int, ...], ...]] = set()
    tested = 0
    prime_seen = 0
    witness = None
    for first in first_positive:
        for second in vertex_splits(first):
            key = canonical_faces(second)
            if key in seen:
                continue
            seen.add(key)
            if separating_nonfacial_triangles(second):
                continue
            prime_seen += 1
            if tested >= args.limit:
                break
            verify_closed_triangulation(second, expected_chi=0)
            vertices, _, neighbors = graph_from_faces(second)
            verify_three_connectivity(vertices, neighbors)
            tested += 1
            if has_u(second):
                witness = key
                break
        if witness is not None or tested >= args.limit:
            break

    print(
        {
            "scope": "bounded counterexample probe only",
            "first_step_positive": len(first_positive),
            "unique_second_step_seen": len(seen),
            "prime_candidates_seen": prime_seen,
            "prime_candidates_u_tested": tested,
            "positive_prime_found": witness is not None,
        }
    )
    if witness is not None:
        print({"witness_faces": witness})
        print("FAIL: bounded diagnostic found a prime positive witness", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
