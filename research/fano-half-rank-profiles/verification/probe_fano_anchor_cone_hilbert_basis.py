"""Exact discovery for the Fano triangle chamber h_0 >= h_i."""

from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
from itertools import product

import sympy as sp


LINES = (
    (0,1,2), (0,3,4), (0,5,6), (1,3,5),
    (1,4,6), (2,3,6), (2,4,5),
)

RAYS = (
    (1,0,1,0,1,0,1), (1,0,1,1,0,1,0), (1,0,1,1,1,1,1),
    (1,1,0,0,1,1,0), (1,1,0,1,0,0,1), (1,1,0,1,1,1,1),
    (1,1,1,0,1,1,1), (1,1,1,1,0,1,1), (1,1,1,1,1,0,1),
    (1,1,1,1,1,1,0), (1,1,1,1,1,1,1),
    (2,1,1,1,1,2,2), (2,1,1,1,2,2,2), (2,1,1,2,1,2,2),
    (2,1,1,2,2,1,1), (2,1,1,2,2,1,2), (2,1,1,2,2,2,1),
    (2,1,2,1,1,2,2), (2,1,2,1,2,2,1), (2,1,2,2,1,1,2),
    (2,1,2,2,2,1,1), (2,2,1,1,1,2,2), (2,2,1,1,2,1,2),
    (2,2,1,2,1,2,1), (2,2,1,2,2,1,1), (2,2,2,1,1,1,1),
    (2,2,2,1,1,1,2), (2,2,2,1,1,2,1), (2,2,2,1,2,1,1),
    (2,2,2,2,1,1,1),
)


def inequalities() -> tuple[tuple[int, ...], ...]:
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
    for point in range(1, 7):
        row = [0] * 7
        row[0] = 1
        row[point] = -1
        rows.append(tuple(row))
    return tuple(rows)


INEQUALITIES = inequalities()


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right))


def feasible(profile: tuple[int, ...]) -> bool:
    return all(dot(row, profile) >= 0 for row in INEQUALITIES)


@lru_cache(maxsize=None)
def ray_rank(vertices: tuple[int, ...]) -> int:
    return sp.Matrix([RAYS[index] for index in vertices]).rank() if vertices else 0


def exact_facets() -> tuple[tuple[int, ...], ...]:
    facets = set()
    for inequality in INEQUALITIES:
        vertices = tuple(index for index, ray in enumerate(RAYS) if dot(inequality, ray) == 0)
        if ray_rank(vertices) == 6:
            facets.add(vertices)
    return tuple(sorted(facets))


FACETS = exact_facets()


@lru_cache(maxsize=None)
def pulling(vertices: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    vertices = tuple(sorted(vertices))
    dimension = ray_rank(vertices)
    if len(vertices) == dimension:
        return (vertices,)
    apex = vertices[0]
    vertex_set = set(vertices)
    candidates = set()
    for facet in FACETS:
        face = tuple(sorted(vertex_set.intersection(facet)))
        if apex not in face and ray_rank(face) == dimension - 1:
            candidates.add(face)
    boundary = tuple(
        face for face in candidates
        if not any(set(face) < set(other) for other in candidates)
    )
    assert boundary, (vertices, dimension)
    result = set()
    for face in boundary:
        for simplex in pulling(face):
            result.add(tuple(sorted((apex,) + simplex)))
    return tuple(sorted(result))


def simplex_matrix(simplex: tuple[int, ...]) -> sp.Matrix:
    return sp.Matrix.hstack(*(sp.Matrix(RAYS[index]) for index in simplex))


def residues(matrix: sp.Matrix) -> set[tuple[int, ...]]:
    determinant = abs(int(matrix.det()))
    adjugate = matrix.adjugate()
    generators = tuple(
        tuple(int(adjugate[row, column]) % determinant for row in range(7))
        for column in range(7)
    )
    residue_group = {(0,) * 7}
    queue = deque(residue_group)
    while queue:
        current = queue.popleft()
        for generator in generators:
            successor = tuple((a + b) % determinant for a, b in zip(current, generator))
            if successor not in residue_group:
                residue_group.add(successor)
                queue.append(successor)
    assert len(residue_group) == determinant
    result = set()
    for residue in residue_group:
        numerator = matrix * sp.Matrix(residue)
        assert all(int(value) % determinant == 0 for value in numerator)
        result.add(tuple(int(value) // determinant for value in numerator))
    return result


def indecomposable(profile: tuple[int, ...]) -> bool:
    for left in product(*(range(value + 1) for value in profile)):
        if left == (0,) * 7 or left == profile:
            continue
        right = tuple(value - part for value, part in zip(profile, left))
        if feasible(left) and feasible(right):
            return False
    return True


def main() -> None:
    simplices = pulling(tuple(range(len(RAYS))))
    determinants = Counter(abs(int(simplex_matrix(simplex).det())) for simplex in simplices)
    points = set(RAYS)
    for simplex in simplices:
        points.update(residues(simplex_matrix(simplex)))
    points.discard((0,) * 7)
    basis = {profile for profile in points if indecomposable(profile)}
    print(
        f"inequalities={len(INEQUALITIES)} rays={len(RAYS)} facets={len(FACETS)} "
        f"simplices={len(simplices)} determinants={dict(sorted(determinants.items()))}"
    )
    print(f"candidate_union={len(points)} hilbert_basis={len(basis)}")
    print("basis_patterns=", Counter((max(x), sum(x), x[0]) for x in basis))
    for profile in sorted(basis, key=lambda item: (max(item), sum(item), item)):
        print("HB", *profile)


if __name__ == "__main__":
    main()
