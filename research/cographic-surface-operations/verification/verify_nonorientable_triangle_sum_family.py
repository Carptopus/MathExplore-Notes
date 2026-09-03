"""Calibrate triangle-connected sums of projective-plane triangulations.

The general result is topological.  This finite check constructs the first five
nonorientable genera from the frozen six-vertex RP2 triangulation and directly
checks every bond against face adjacency.
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verify_rp2_stellar_family import (  # noqa: E402
    INITIAL_FACES,
    connected,
    face_adjacencies,
    graph_from_faces,
    verify_all_bonds,
    verify_three_connectivity,
)


Face = frozenset[int]


def verify_closed_triangulation(faces: set[Face], expected_chi: int) -> None:
    vertices, edges, neighbors = graph_from_faces(faces)
    incidences = Counter(
        tuple(sorted((u, v)))
        for face in faces
        for u, v in combinations(sorted(face), 2)
    )
    if set(incidences.values()) != {2}:
        raise AssertionError("Every edge must be in exactly two faces")
    if len(vertices) - len(edges) + len(faces) != expected_chi:
        raise AssertionError("Wrong Euler characteristic")
    for vertex in vertices:
        link_edges = [tuple(sorted(face - {vertex})) for face in faces if vertex in face]
        link_neighbors = {item: set() for item in neighbors[vertex]}
        for left, right in link_edges:
            link_neighbors[left].add(right)
            link_neighbors[right].add(left)
        if not all(len(values) == 2 for values in link_neighbors.values()):
            raise AssertionError((vertex, "link not 2-regular"))
        if not connected(set(link_neighbors), link_neighbors):
            raise AssertionError((vertex, "link disconnected"))


def triangle_sum(current: set[Face], fresh_copy: set[Face]) -> set[Face]:
    seam_current = min(current, key=lambda face: tuple(sorted(face)))
    seam_copy = frozenset((0, 1, 3))
    if seam_copy not in fresh_copy:
        raise AssertionError("Frozen RP2 seam missing")

    seam_vertices = sorted(seam_current)
    mapping = {0: seam_vertices[0], 1: seam_vertices[1], 3: seam_vertices[2]}
    next_vertex = max(set().union(*current)) + 1
    for old, new in zip((2, 4, 5), range(next_vertex, next_vertex + 3)):
        mapping[old] = new
    mapped = {frozenset(mapping[vertex] for vertex in face) for face in fresh_copy}
    mapped_seam = frozenset(mapping[vertex] for vertex in seam_copy)
    if mapped_seam != seam_current:
        raise AssertionError("Seams were not identified")
    return (current - {seam_current}) | (mapped - {mapped_seam})


def main() -> None:
    faces = set(INITIAL_FACES)
    for genus in range(1, 6):
        verify_closed_triangulation(faces, expected_chi=2 - genus)
        vertices, edges, neighbors = graph_from_faces(faces)
        verify_three_connectivity(vertices, neighbors)
        expected_edges = 3 * len(vertices) - 6 + 3 * genus
        if len(edges) != expected_edges:
            raise AssertionError((genus, "wrong edge count", len(edges)))
        selected = face_adjacencies(faces)
        bond_count = verify_all_bonds(vertices, edges, neighbors, selected)
        print(
            f"PASS h={genus} n={len(vertices)} m={len(edges)} "
            f"faces={len(faces)} bonds={bond_count}"
        )
        faces = triangle_sum(faces, set(INITIAL_FACES))


if __name__ == "__main__":
    main()
