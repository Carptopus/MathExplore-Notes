"""Exact structural certificate behind the M*(K6) ordering.

The ten frozen triangles form the six-vertex triangulation of the real
projective plane.  This checker verifies the surface links, the order-60
automorphism group, its three cut orbits, and one cyclic bond representative
per orbit.  It uses no optimizer and keeps all checks active under python -O.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
FACES = frozenset(
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
)

# Permutations are stored by images of 0,...,5.
GENERATOR_A = (0, 2, 3, 4, 5, 1)  # (1 2 3 4 5)
GENERATOR_B = (1, 2, 0, 5, 3, 4)  # (0 1 2)(3 5 4)
IDENTITY = VERTICES


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in VERTICES)


def generated_group() -> frozenset[tuple[int, ...]]:
    group = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        current = frontier.pop()
        for generator in (GENERATOR_A, GENERATOR_B):
            image = compose(current, generator)
            if image not in group:
                group.add(image)
                frontier.append(image)
    require(len(group) == 60, ("wrong automorphism-group order", len(group)))
    for permutation in group:
        image_faces = {
            frozenset(permutation[vertex] for vertex in face) for face in FACES
        }
        require(image_faces == FACES, ("face system not preserved", permutation))
    return frozenset(group)


def face_adjacencies() -> frozenset[tuple[tuple[int, int], tuple[int, int]]]:
    selected = set()
    for face in FACES:
        for center in face:
            others = sorted(face - {center})
            selected.add(tuple(sorted((edge(center, others[0]), edge(center, others[1])))))
    require(len(selected) == 30, ("wrong face-adjacency count", len(selected)))
    return frozenset(selected)


def verify_surface_links() -> None:
    incidences = Counter(
        edge(left, right)
        for face in FACES
        for left, right in combinations(sorted(face), 2)
    )
    require(set(incidences) == set(EDGES), "face system misses an edge")
    require(set(incidences.values()) == {2}, ("nonmanifold edge", incidences))
    require(6 - 15 + len(FACES) == 1, "wrong Euler characteristic")

    for vertex in VERTICES:
        link_edges = []
        for face in FACES:
            if vertex in face:
                link_edges.append(tuple(sorted(face - {vertex})))
        degrees = Counter(endpoint for item in link_edges for endpoint in item)
        require(len(link_edges) == 5, ("wrong link size", vertex, link_edges))
        require(set(degrees.values()) == {2}, ("link is not 2-regular", vertex))
        seen = {link_edges[0][0]}
        changed = True
        while changed:
            changed = False
            for left, right in link_edges:
                if left in seen and right not in seen:
                    seen.add(right)
                    changed = True
                if right in seen and left not in seen:
                    seen.add(left)
                    changed = True
        require(seen == set(VERTICES) - {vertex}, ("disconnected link", vertex))


def canonical_cut(side: frozenset[int]) -> frozenset[frozenset[int]]:
    complement = frozenset(set(VERTICES) - set(side))
    return frozenset((side, complement))


def cut_orbits(group: frozenset[tuple[int, ...]]) -> list[set[frozenset[frozenset[int]]]]:
    cuts = {
        canonical_cut(frozenset(side))
        for size in range(1, 4)
        for side in combinations(VERTICES, size)
    }
    orbits = []
    while cuts:
        seed = next(iter(cuts))
        orbit = {
            canonical_cut(frozenset(permutation[vertex] for vertex in next(iter(seed))))
            for permutation in group
        }
        orbits.append(orbit)
        cuts -= orbit
    require(sorted(map(len, orbits)) == [6, 10, 15], ("wrong cut orbits", orbits))
    return orbits


def induced_cycle(
    side: frozenset[int],
    selected: frozenset[tuple[tuple[int, int], tuple[int, int]]],
) -> tuple[tuple[int, int], ...]:
    bond = frozenset(
        edge(u, v) for u, v in EDGES if (u in side) != (v in side)
    )
    neighbors = {item: [] for item in bond}
    for left, right in selected:
        if left in bond and right in bond:
            neighbors[left].append(right)
            neighbors[right].append(left)
    require(all(len(values) == 2 for values in neighbors.values()), (side, neighbors))
    start = min(bond)
    order = []
    previous = None
    current = start
    while True:
        order.append(current)
        choices = sorted(neighbors[current])
        following = choices[0] if choices[0] != previous else choices[1]
        previous, current = current, following
        if current == start:
            break
        require(current not in order, ("premature closure", side, order))
    require(len(order) == len(bond), ("disconnected bond boundary", side, order))
    return tuple(order)


def main() -> None:
    verify_surface_links()
    selected = face_adjacencies()
    group = generated_group()
    orbits = cut_orbits(group)

    representatives = (frozenset({0}), frozenset({0, 1}), frozenset({0, 1, 2}))
    cycles = [induced_cycle(side, selected) for side in representatives]
    require([len(cycle) for cycle in cycles] == [5, 8, 9], "wrong representatives")

    print("PASS: ten faces form a closed six-vertex triangulation with chi=1")
    print("PASS: face angles reconstruct 30 global adjacency pairs")
    print("PASS: two explicit generators produce 60 face automorphisms")
    print(f"PASS: the 31 bonds form three cut orbits {sorted(map(len, orbits))}")
    print("PASS: representatives of sizes 5, 8, and 9 each induce one cycle")


if __name__ == "__main__":
    main()
