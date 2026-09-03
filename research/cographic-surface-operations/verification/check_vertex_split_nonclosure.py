"""Calibrate failure of U(T) under general vertex splitting.

Start from the nine-vertex Klein-bottle triangulation obtained by gluing two
six-vertex RP2 triangulations along a face.  Enumerate every nontrivial split of
one vertex along two nonconsecutive positions of its link.  For each resulting
triangulation, test every bond against the face-adjacency ordering and record
whether a separating nonfacial triangle remains.

This is finite calibration, not a classification theorem for vertex splits.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verify_nonorientable_triangle_sum_family import (  # noqa: E402
    INITIAL_FACES,
    Face,
    connected,
    face_adjacencies,
    graph_from_faces,
    triangle_sum,
    verify_all_bonds,
    verify_closed_triangulation,
    verify_three_connectivity,
)


def link_cycle(faces: set[Face], vertex: int) -> list[int]:
    link_neighbors: dict[int, set[int]] = {}
    for face in faces:
        if vertex not in face:
            continue
        left, right = tuple(face - {vertex})
        link_neighbors.setdefault(left, set()).add(right)
        link_neighbors.setdefault(right, set()).add(left)

    start = min(link_neighbors)
    cycle = [start]
    previous = None
    current = start
    while True:
        candidates = sorted(
            link_neighbors[current]
            - ({previous} if previous is not None else set())
        )
        following = candidates[0]
        if following == start:
            break
        cycle.append(following)
        previous, current = current, following
    if len(cycle) != len(link_neighbors):
        raise AssertionError((vertex, "link traversal incomplete"))
    return cycle


def split_vertex(
    faces: set[Face], vertex: int, left_index: int, right_index: int
) -> set[Face]:
    cycle = link_cycle(faces, vertex)
    left = cycle[left_index]
    right = cycle[right_index]
    moved_faces = {
        frozenset((vertex, cycle[index], cycle[(index + 1) % len(cycle)]))
        for index in range(left_index, right_index)
    }
    fresh_vertex = max(set().union(*faces)) + 1
    result = {
        frozenset(fresh_vertex if item == vertex else item for item in face)
        if face in moved_faces
        else face
        for face in faces
    }
    result.add(frozenset((vertex, fresh_vertex, left)))
    result.add(frozenset((vertex, fresh_vertex, right)))
    return result


def separating_nonfacial_triangles(faces: set[Face]) -> list[tuple[int, int, int]]:
    vertices_raw, edges, neighbors = graph_from_faces(faces)
    vertices = set(vertices_raw)
    edge_set = {frozenset(edge) for edge in edges}
    result = []
    for triangle in combinations(sorted(vertices), 3):
        triangle_set = frozenset(triangle)
        if triangle_set in faces:
            continue
        if not all(
            frozenset(edge) in edge_set for edge in combinations(triangle, 2)
        ):
            continue
        remainder = vertices - triangle_set
        remainder_neighbors = {
            item: neighbors[item] & remainder for item in remainder
        }
        if remainder and not connected(remainder, remainder_neighbors):
            result.append(triangle)
    return result


def canonical_labelled_faces(faces: set[Face]) -> tuple[tuple[int, ...], ...]:
    """Serialize current labels canonically; this is not graph isomorphism."""

    return tuple(sorted(tuple(sorted(face)) for face in faces))


def main() -> None:
    base = triangle_sum(set(INITIAL_FACES), set(INITIAL_FACES))
    base_vertices = sorted(set().union(*base))
    counts = {
        "positive_with_seam": 0,
        "positive_prime": 0,
        "negative_with_seam": 0,
        "negative_prime": 0,
    }
    first_failure = None
    unique_positive: set[tuple[tuple[int, ...], ...]] = set()
    unique_negative: set[tuple[tuple[int, ...], ...]] = set()

    for vertex in base_vertices:
        cycle = link_cycle(base, vertex)
        degree = len(cycle)
        for left_index, right_index in combinations(range(degree), 2):
            span = min(right_index - left_index, degree - right_index + left_index)
            if span < 2:
                continue
            split = split_vertex(base, vertex, left_index, right_index)
            verify_closed_triangulation(split, expected_chi=0)
            vertices, edges, neighbors = graph_from_faces(split)
            verify_three_connectivity(vertices, neighbors)
            try:
                verify_all_bonds(
                    vertices, edges, neighbors, face_adjacencies(split)
                )
                positive = True
            except RuntimeError as error:
                positive = False
                if first_failure is None:
                    first_failure = (
                        vertex,
                        cycle,
                        left_index,
                        right_index,
                        error,
                    )

            key = canonical_labelled_faces(split)
            (unique_positive if positive else unique_negative).add(key)

            has_seam = bool(separating_nonfacial_triangles(split))
            label = (
                ("positive_" if positive else "negative_")
                + ("with_seam" if has_seam else "prime")
            )
            counts[label] += 1

    expected = {
        "positive_with_seam": 63,
        "positive_prime": 0,
        "negative_with_seam": 0,
        "negative_prime": 27,
    }
    if counts != expected:
        raise AssertionError((counts, expected))
    unique_counts = {
        "positive": len(unique_positive),
        "negative": len(unique_negative),
        "total": len(unique_positive | unique_negative),
    }
    expected_unique = {"positive": 52, "negative": 26, "total": 78}
    if unique_counts != expected_unique:
        raise AssertionError((unique_counts, expected_unique))
    print(f"PASS split classification {counts}")
    print(f"PASS distinct labelled results {unique_counts}")
    print(f"PASS first negative witness {first_failure}")


if __name__ == "__main__":
    main()
