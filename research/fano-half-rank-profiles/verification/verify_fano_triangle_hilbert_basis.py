"""Exact Hilbert-basis certificate for the integral Fano triangle cone.

This script assumes only the fourteen primitive rays independently certified
by ``verify_fano_triangle_extreme_rays.cpp``.  It constructs an exact pulling
triangulation from the facet incidences, enumerates every lattice residue in
the twelve fundamental parallelepipeds, and proves that the resulting Hilbert
basis has exactly 78 elements.  All ranks, determinants, adjugates, and lattice
divisibility checks use exact integer/rational arithmetic.
"""

from collections import Counter, deque
from functools import lru_cache
from itertools import product

import sympy as sp


LINES = (
    (0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
    (1, 4, 6), (2, 3, 6), (2, 4, 5),
)

RAYS = (
    (0,0,0,1,1,1,1), (0,1,1,0,0,1,1),
    (0,1,1,1,1,0,0), (1,0,1,0,1,0,1),
    (1,0,1,1,0,1,0), (1,1,0,0,1,1,0),
    (1,1,0,1,0,0,1), (1,1,2,1,2,2,1),
    (1,1,2,2,1,1,2), (1,2,1,1,2,1,2),
    (1,2,1,2,1,2,1), (2,1,1,1,1,2,2),
    (2,1,1,2,2,1,1), (2,2,2,1,1,1,1),
)


def inequalities():
    rows = []
    for coordinate in range(7):
        row = [0] * 7
        row[coordinate] = 1
        rows.append(tuple(row))
    for line in LINES:
        for distinguished in line:
            row = [0] * 7
            row[distinguished] = -1
            for point in line:
                if point != distinguished:
                    row[point] = 1
            rows.append(tuple(row))
    return tuple(rows)


INEQUALITIES = inequalities()


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def feasible(profile):
    return all(dot(row, profile) >= 0 for row in INEQUALITIES)


@lru_cache(maxsize=None)
def ray_rank(vertices):
    if not vertices:
        return 0
    return sp.Matrix([RAYS[index] for index in vertices]).rank()


def exact_facets():
    facets = set()
    for inequality in INEQUALITIES:
        vertices = tuple(
            index for index, ray in enumerate(RAYS)
            if dot(inequality, ray) == 0
        )
        if ray_rank(vertices) == 6:
            facets.add(vertices)
    assert len(facets) == 21
    assert Counter(map(len, facets)) == {7: 21}
    return tuple(sorted(facets))


FACETS = exact_facets()


@lru_cache(maxsize=None)
def pulling_triangulation(vertices):
    """Return the lexicographic pulling triangulation of one cone face."""
    vertices = tuple(sorted(vertices))
    cone_rank = ray_rank(vertices)
    if len(vertices) == cone_rank:
        return (vertices,)

    apex = vertices[0]
    vertex_set = set(vertices)
    candidates = set()
    for global_facet in FACETS:
        face = tuple(sorted(vertex_set.intersection(global_facet)))
        if apex not in face and ray_rank(face) == cone_rank - 1:
            candidates.add(face)
    boundary_facets = tuple(
        face for face in candidates
        if not any(set(face) < set(other) for other in candidates)
    )
    assert boundary_facets

    simplices = set()
    for facet in boundary_facets:
        for simplex in pulling_triangulation(facet):
            simplices.add(tuple(sorted((apex,) + simplex)))
    return tuple(sorted(simplices))


def simplex_matrix(simplex):
    return sp.Matrix.hstack(*(sp.Matrix(RAYS[index]) for index in simplex))


def residue_representatives(matrix):
    """Enumerate the exact half-open fundamental parallelepiped."""
    determinant = abs(int(matrix.det()))
    adjugate = matrix.adjugate()
    generators = tuple(
        tuple(int(adjugate[row, column]) % determinant for row in range(7))
        for column in range(7)
    )
    residues = {(0,) * 7}
    queue = deque(residues)
    while queue:
        current = queue.popleft()
        for generator in generators:
            successor = tuple(
                (left + right) % determinant
                for left, right in zip(current, generator)
            )
            if successor not in residues:
                residues.add(successor)
                queue.append(successor)
    assert len(residues) == determinant

    points = set()
    for residue in residues:
        numerator = matrix * sp.Matrix(residue)
        assert all(int(value) % determinant == 0 for value in numerator)
        points.add(tuple(int(value) // determinant for value in numerator))
    assert len(points) == determinant
    return points


def indecomposable(profile):
    ranges = tuple(range(value + 1) for value in profile)
    zero = (0,) * 7
    for left in product(*ranges):
        if left == zero or left == profile:
            continue
        right = tuple(value - part for value, part in zip(profile, left))
        if feasible(left) and feasible(right):
            return False
    return True


def expected_hilbert_basis():
    result = set(RAYS[:7])
    result.add((1,) * 7)
    for zero in range(7):
        result.add(tuple(0 if point == zero else 1 for point in range(7)))

    line_sets = {frozenset(line) for line in LINES}
    all_points = frozenset(range(7))
    for mask in range(1, 1 << 7):
        support = frozenset(point for point in range(7) if (mask >> point) & 1)
        allowed = (
            len(support) in (1, 2)
            or (len(support) == 3 and support in line_sets)
            or (
                len(support) == 4
                and all_points.difference(support) not in line_sets
            )
        )
        if allowed:
            result.add(tuple(2 if point in support else 1 for point in range(7)))
    return result


def main():
    simplices = pulling_triangulation(tuple(range(len(RAYS))))
    determinants = Counter(abs(int(simplex_matrix(simplex).det())) for simplex in simplices)
    assert len(simplices) == 12
    assert determinants == {16: 12}

    parallelepiped_points = set()
    for simplex in simplices:
        parallelepiped_points.update(residue_representatives(simplex_matrix(simplex)))

    candidates = parallelepiped_points.union(RAYS)
    candidates.discard((0,) * 7)
    hilbert_basis = {profile for profile in candidates if indecomposable(profile)}
    expected = expected_hilbert_basis()
    assert hilbert_basis == expected
    assert len(hilbert_basis) == 78

    # Every non-basis residue must reduce through smaller certified residues.
    reachable = {(0,) * 7}
    for total in range(1, max(map(sum, candidates)) + 1):
        for profile in sorted(item for item in candidates if sum(item) == total):
            if profile in hilbert_basis:
                reachable.add(profile)
                continue
            for atom in hilbert_basis:
                if not all(atom[i] <= profile[i] for i in range(7)):
                    continue
                residual = tuple(profile[i] - atom[i] for i in range(7))
                if residual in reachable:
                    reachable.add(profile)
                    break
    assert candidates.issubset(reachable)

    patterns = Counter(
        (max(profile), sum(value == 2 for value in profile), sum(value == 0 for value in profile))
        for profile in hilbert_basis
    )
    print(
        f"facets={len(FACETS)} simplices={len(simplices)} "
        f"determinants={dict(determinants)}"
    )
    print(
        f"parallelepiped_union={len(parallelepiped_points)} "
        f"candidate_union={len(candidates)} hilbert_basis={len(hilbert_basis)}"
    )
    print(f"basis_patterns={dict(sorted(patterns.items()))}")
    print("PASS: the 78-element Hilbert basis is complete")


if __name__ == "__main__":
    main()
