# AI-assisted generation and review: OpenAI Codex. Responsible maintainer: Carptopus.
"""Dependency-free exact check of the minimal arbitrary-diagonal counterexample."""

from __future__ import annotations

from fractions import Fraction


A = (
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
)

X = (
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
)


def multiply(left: tuple[tuple[int, ...], ...], right: tuple[tuple[int, ...], ...]):
    size = len(left)
    return tuple(
        tuple(
            sum(left[row][index] * right[index][column] for index in range(size))
            for column in range(size)
        )
        for row in range(size)
    )


def transpose(matrix: tuple[tuple[int, ...], ...]):
    size = len(matrix)
    return tuple(
        tuple(matrix[column][row] for column in range(size))
        for row in range(size)
    )


def add(*matrices: tuple[tuple[int, ...], ...]):
    size = len(matrices[0])
    return tuple(
        tuple(sum(matrix[row][column] for matrix in matrices) for column in range(size))
        for row in range(size)
    )


def scale(value: int, matrix: tuple[tuple[int, ...], ...]):
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def identity(size: int):
    return tuple(
        tuple(int(row == column) for column in range(size))
        for row in range(size)
    )


def verification_matrix(matrix: tuple[tuple[int, ...], ...]):
    size = len(matrix)
    variables = [
        (row, column)
        for row in range(size)
        for column in range(size)
        if matrix[row][column] == 0
    ]
    equations = []
    for row in range(size):
        for column in range(size):
            equation = []
            for variable_row, variable_column in variables:
                coefficient = matrix[row][variable_column] if column == variable_row else 0
                if row == variable_column:
                    coefficient -= matrix[variable_row][column]
                equation.append(coefficient)
            equations.append(equation)
    return equations, variables


def rank_over_q(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][index] - factor * work[rank][index]
                for index in range(columns)
            ]
        rank += 1
    return rank


def main() -> None:
    size = len(A)
    reconstructed = add(multiply(A, A), scale(-1, A), scale(-1, identity(size)))
    assert reconstructed == X
    assert transpose(X) == X
    assert multiply(A, transpose(X)) == multiply(transpose(X), A)
    assert all(
        A[row][column] == 0 or X[row][column] == 0
        for row in range(size)
        for column in range(size)
    )
    assert any(entry != 0 for row in X for entry in row)

    # Root the path 0--1--2 at vertex 0. Every vertex has at most one child,
    # so the pairwise-coprimality hypothesis is vacuous at every vertex.
    children = ((1,), (2,), ())
    assert all(len(child_set) <= 1 for child_set in children)

    verification, variables = verification_matrix(A)
    assert variables == [(0, 2), (1, 1), (2, 0)]
    assert rank_over_q(verification) == 2 < len(variables)

    diagonal_control = (
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 2),
    )
    edge_product_control = (
        (1, 1, 0),
        (1, 0, 1),
        (0, 2, 1),
    )
    for control in (diagonal_control, edge_product_control):
        control_verification, control_variables = verification_matrix(control)
        assert rank_over_q(control_verification) == len(control_variables) == 3

    print("PASS: exact 3x3 path counterexample")
    print("A*X = X*A, A o X = 0, X != 0, recursive coprimality vacuous")
    print("counterexample rank 2/3; diagonal and edge-product controls rank 3/3")


if __name__ == "__main__":
    main()
