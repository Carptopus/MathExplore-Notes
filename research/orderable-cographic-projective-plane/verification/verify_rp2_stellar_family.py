"""Finite positive controls for the RP2 triangulation theorem candidate.

The proof is topological and infinite.  This script is only an independent
calibration: it repeatedly stellarly subdivides a face of the six-vertex RP2
triangulation and directly checks every bond for the first seven members.
All checks remain active under python -O.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


INITIAL_FACES = {
    frozenset(face)
    for face in (
        (0, 1, 3),
        (0, 1, 4),
        (0, 2, 4),
        (0, 2, 5),
        (0, 3, 5),
        (1, 2, 3),
        (1, 2, 5),
        (1, 4, 5),
        (2, 3, 4),
        (3, 4, 5),
    )
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def graph_from_faces(
    faces: set[frozenset[int]],
) -> tuple[tuple[int, ...], frozenset[tuple[int, int]], dict[int, set[int]]]:
    vertices = tuple(sorted(set().union(*faces)))
    edges = frozenset(
        edge(u, v) for face in faces for u, v in combinations(sorted(face), 2)
    )
    neighbors = {vertex: set() for vertex in vertices}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    return vertices, edges, neighbors


def connected(vertices: set[int], neighbors: dict[int, set[int]]) -> bool:
    if not vertices:
        return False
    seen = {next(iter(vertices))}
    frontier = list(seen)
    while frontier:
        current = frontier.pop()
        for following in neighbors[current] & vertices:
            if following not in seen:
                seen.add(following)
                frontier.append(following)
    return seen == vertices


def verify_triangulation(faces: set[frozenset[int]]) -> None:
    vertices, edges, neighbors = graph_from_faces(faces)
    incidences = Counter(
        edge(u, v) for face in faces for u, v in combinations(sorted(face), 2)
    )
    require(set(incidences) == set(edges), "face incidence misses an edge")
    require(set(incidences.values()) == {2}, ("nonmanifold edge", incidences))
    require(
        len(vertices) - len(edges) + len(faces) == 1,
        ("wrong Euler characteristic", len(vertices), len(edges), len(faces)),
    )
    for vertex in vertices:
        link_edges = [tuple(sorted(face - {vertex})) for face in faces if vertex in face]
        link_vertices = neighbors[vertex]
        link_neighbors = {item: set() for item in link_vertices}
        for left, right in link_edges:
            link_neighbors[left].add(right)
            link_neighbors[right].add(left)
        require(
            all(len(values) == 2 for values in link_neighbors.values()),
            ("link not 2-regular", vertex),
        )
        require(connected(set(link_vertices), link_neighbors), ("link disconnected", vertex))


def face_adjacencies(
    faces: set[frozenset[int]],
) -> frozenset[tuple[tuple[int, int], tuple[int, int]]]:
    selected = set()
    for face in faces:
        for center in face:
            left, right = sorted(face - {center})
            selected.add(tuple(sorted((edge(center, left), edge(center, right)))))
    return frozenset(selected)


def verify_three_connectivity(
    vertices: tuple[int, ...], neighbors: dict[int, set[int]]
) -> None:
    full = set(vertices)
    for removed_size in range(3):
        for removed in combinations(vertices, removed_size):
            remaining = full - set(removed)
            require(connected(remaining, neighbors), ("vertex cut", removed))


def verify_all_bonds(
    vertices: tuple[int, ...],
    edges: frozenset[tuple[int, int]],
    neighbors: dict[int, set[int]],
    selected: frozenset[tuple[tuple[int, int], tuple[int, int]]],
) -> int:
    root = vertices[0]
    all_vertices = set(vertices)
    bond_count = 0
    for mask in range(1 << (len(vertices) - 1)):
        side = {root}
        for index, vertex in enumerate(vertices[1:]):
            if mask & (1 << index):
                side.add(vertex)
        other = all_vertices - side
        if not other:
            continue
        if not connected(side, neighbors) or not connected(other, neighbors):
            continue
        bond_count += 1
        bond = {item for item in edges if (item[0] in side) != (item[1] in side)}
        boundary_neighbors = {item: set() for item in bond}
        for left, right in selected:
            if left in bond and right in bond:
                boundary_neighbors[left].add(right)
                boundary_neighbors[right].add(left)
        require(
            all(len(values) == 2 for values in boundary_neighbors.values()),
            ("bond boundary not 2-regular", side),
        )
        require(
            connected(set(bond), boundary_neighbors),
            ("bond boundary disconnected", side),
        )
    return bond_count


def subdivide_smallest_face(
    faces: set[frozenset[int]], new_vertex: int
) -> set[frozenset[int]]:
    chosen = min(faces, key=lambda face: tuple(sorted(face)))
    a, b, c = sorted(chosen)
    output = set(faces - {chosen})
    output.update(
        {
            frozenset((a, b, new_vertex)),
            frozenset((b, c, new_vertex)),
            frozenset((c, a, new_vertex)),
        }
    )
    return output


def main() -> None:
    faces = set(INITIAL_FACES)
    for new_vertex in range(6, 13):
        verify_triangulation(faces)
        vertices, edges, neighbors = graph_from_faces(faces)
        verify_three_connectivity(vertices, neighbors)
        require(len(edges) == 3 * len(vertices) - 3, "wrong RP2 edge count")
        require(len(edges) > 3 * len(vertices) - 6, "planar edge bound not violated")
        selected = face_adjacencies(faces)
        bonds = verify_all_bonds(vertices, edges, neighbors, selected)
        print(
            f"PASS n={len(vertices)} edges={len(edges)} faces={len(faces)} "
            f"bonds={bonds} face_adjacencies={len(selected)}"
        )
        faces = subdivide_smallest_face(faces, new_vertex)


if __name__ == "__main__":
    main()
