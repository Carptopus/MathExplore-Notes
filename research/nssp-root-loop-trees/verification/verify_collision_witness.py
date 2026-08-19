# AI-assisted generation and review: OpenAI Codex. Responsible maintainer: Carptopus.
"""Exact destructive controls for the deepest-collision witness in P5.

The controls use rational eigenvalues, construct the proposed commuting matrix
explicitly over Q, and verify every nSSP equation rather than only a rank loss.
"""

from __future__ import annotations

import json
from fractions import Fraction

from verify_recursive_tree_criterion import (
    build_matrix,
    children_from_parent,
    induced_matrix,
    matrix_multiply,
    subtree_vertex_sets,
)


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*matrix)]


def null_vector(matrix: list[list[Fraction]]) -> list[Fraction]:
    """Return one nonzero null vector of a singular rational matrix."""
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    pivots: list[int] = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][index] - factor * work[pivot_row][index]
                for index in range(columns)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = [column for column in range(columns) if column not in pivots]
    if not free:
        raise ValueError("matrix has trivial nullspace")
    vector = [Fraction(0)] * columns
    vector[free[-1]] = Fraction(1)
    for row, column in reversed(list(enumerate(pivots))):
        vector[column] = -sum(
            work[row][index] * vector[index]
            for index in free
        )
    return vector


def eigenvector(
    matrix: list[list[int]], eigenvalue: Fraction, left: bool = False
) -> list[Fraction]:
    work = [[Fraction(value) for value in row] for row in matrix]
    if left:
        work = transpose(work)
    for index in range(len(work)):
        work[index][index] -= eigenvalue
    vector = null_vector(work)
    if not vector[0]:
        raise ValueError("child root coordinate unexpectedly vanishes")
    return [value / vector[0] for value in vector]


def subtract(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [left[row][column] - right[row][column] for column in range(len(left))]
        for row in range(len(left))
    ]


def collision_witness(
    label: str,
    parent: tuple[int, ...],
    forward: tuple[int, ...],
    backward: tuple[int, ...],
    vertex: int,
    child_left: int,
    child_right: int,
    eigenvalue: int,
) -> dict[str, object]:
    integer_matrix = build_matrix(parent, forward, backward)
    matrix = [[Fraction(value) for value in row] for row in integer_matrix]
    children = children_from_parent(parent)
    vertex_sets = subtree_vertex_sets(children)
    count = len(matrix)

    right_vectors: list[list[Fraction]] = []
    left_vectors: list[list[Fraction]] = []
    for child in (child_left, child_right):
        block = induced_matrix(integer_matrix, vertex_sets[child])
        right_vectors.append(eigenvector(block, Fraction(eigenvalue)))
        left_vectors.append(eigenvector(block, Fraction(eigenvalue), left=True))

    p_left = matrix[vertex][child_left]
    p_right = matrix[vertex][child_right]
    q_left = matrix[child_left][vertex]
    q_right = matrix[child_right][vertex]
    right_scales = (p_right, -p_left)
    left_scales = (q_right, -q_left)

    u_plus = [Fraction(0)] * count
    w_plus = [Fraction(0)] * count
    signs = [Fraction(0)] * count
    for branch_index, child in enumerate((child_left, child_right)):
        vertices = vertex_sets[child]
        for local_index, global_index in enumerate(vertices):
            u_plus[global_index] = (
                right_scales[branch_index] * right_vectors[branch_index][local_index]
            )
            w_plus[global_index] = (
                left_scales[branch_index] * left_vectors[branch_index][local_index]
            )
            distance = 0
            cursor = global_index
            while cursor != child:
                cursor = parent[cursor - 1]
                distance += 1
            signs[global_index] = Fraction(1 if distance % 2 == 0 else -1)

    u_minus = [signs[index] * u_plus[index] for index in range(count)]
    w_minus = [signs[index] * w_plus[index] for index in range(count)]
    witness = [
        [
            u_plus[row] * w_plus[column]
            + u_minus[row] * w_minus[column]
            for column in range(count)
        ]
        for row in range(count)
    ]
    commutator = subtract(
        matrix_multiply(matrix, witness),
        matrix_multiply(witness, matrix),
    )
    prescribed_zeros = all(
        not witness[row][column]
        for row in range(count)
        for column in range(count)
        if matrix[row][column]
    )
    commutes = all(not value for row in commutator for value in row)
    nonzero_entries = [
        [row, column, str(witness[row][column])]
        for row in range(count)
        for column in range(count)
        if witness[row][column]
    ]
    return {
        "label": label,
        "eigenvalue": eigenvalue,
        "commutes_exactly": commutes,
        "zero_on_all_prescribed_positions": prescribed_zeros,
        "witness_nonzero": bool(nonzero_entries),
        "nonzero_witness_entries": nonzero_entries,
    }


def main() -> None:
    cases = [
        collision_witness(
            "nested_leaf_collision_lambda_0",
            (0, 1, 1),
            (1, 1, 1),
            (2, 3, -2),
            1,
            2,
            3,
            0,
        ),
        collision_witness(
            "nested_shared_factor_x2_minus_1_lambda_1",
            (0, 1, 2, 1, 4),
            (1, 1, 1, 1, 1),
            (2, 3, 1, -3, 1),
            1,
            2,
            4,
            1,
        ),
    ]
    print(json.dumps(cases, indent=2))


if __name__ == "__main__":
    main()
