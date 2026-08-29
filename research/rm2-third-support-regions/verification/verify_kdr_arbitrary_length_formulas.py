"""Regression-check the arbitrary-length K/D/R sign-control factorizations.

The accompanying proof document derives closed bilinear factorizations for
all block lengths.  This script constructs the sign-control matrices directly
from the Walsh formulas and checks those factorizations exactly over F_2 for
representative lengths.  The finite range is a regression check; the proof is
the symbolic factorization, not extrapolation from these tests.
"""

from __future__ import annotations

import random


Matrix = list[list[int]]


def identity(size: int) -> Matrix:
    return [[int(row == column) for column in range(size)] for row in range(size)]


def transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def add(left: Matrix, right: Matrix) -> Matrix:
    return [[a ^ b for a, b in zip(row_left, row_right)] for row_left, row_right in zip(left, right)]


def multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum(left[row][index] * right[index][column] for index in range(len(right))) % 2
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def rank(matrix: Matrix) -> int:
    rows = [row[:] for row in matrix]
    result = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(result, len(rows)) if rows[row][column]), None)
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        for row in range(len(rows)):
            if row != result and rows[row][column]:
                rows[row] = [left ^ right for left, right in zip(rows[row], rows[result])]
        result += 1
    return result


def inverse(matrix: Matrix) -> Matrix:
    size = len(matrix)
    rows = [matrix[row][:] + identity(size)[row] for row in range(size)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if rows[row][column]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        for row in range(size):
            if row != column and rows[row][column]:
                rows[row] = [left ^ right for left, right in zip(rows[row], rows[column])]
    return [row[size:] for row in rows]


def outer(left: list[int], right: list[int]) -> Matrix:
    return [[a * b for b in right] for a in left]


def xor_into(target: Matrix, source: Matrix) -> None:
    for row in range(len(target)):
        for column in range(len(target[0])):
            target[row][column] ^= source[row][column]


def kronecker_direct(k: int) -> Matrix:
    x_dimension = 2 * k - 1
    y_dimension = 2 * k
    matrix = [[0] * y_dimension for _ in range(x_dimension)]
    for x_index in range(x_dimension):
        p = [0] * (k + 1)
        s = [0] * (k + 1)
        if x_index < k:
            p[x_index] = 1
        else:
            s[1 + x_index - k] = 1
        s[k] = (sum(p[:-1]) + sum(s[1:k])) % 2

        for y_index in range(y_dimension):
            r = [0] * k
            t = [0] * k
            if y_index < k:
                r[y_index] = 1
            else:
                t[y_index - k] = 1
            exponent_1 = sum(p[index] * r[index] for index in range(k)) % 2
            exponent_2 = sum(s[index + 1] * t[index] for index in range(k)) % 2
            partial = [0] * (k + 1)
            for index in range(1, k + 1):
                partial[index] = partial[index - 1] ^ r[index - 1] ^ t[index - 1]
            exponent_12 = sum(
                (p[index] ^ s[index]) * partial[index] for index in range(k + 1)
            ) % 2
            matrix[x_index][y_index] = exponent_1 ^ exponent_2 ^ exponent_12
    return matrix


def kronecker_factored(k: int) -> Matrix:
    matrix = [[0] * (2 * k) for _ in range(2 * k - 1)]
    for index in range(k - 1):
        left = [0] * (2 * k - 1)
        left[index] = 1
        left[k + index] = 1
        right = [0] * (2 * k)
        for position in range(index + 1, k):
            right[position] = 1
        for position in range(index, k - 1):
            right[k + position] = 1
        xor_into(matrix, outer(left, right))
    return matrix


def degenerate_direct(k: int) -> Matrix:
    nilpotent = [[0] * k for _ in range(k)]
    for index in range(k - 1):
        nilpotent[index][index + 1] = 1
    unit = identity(k)
    inverse_transpose = inverse(transpose(add(unit, nilpotent)))
    full = [[0] * (2 * k) for _ in range(2 * k)]
    for row in range(k):
        for column in range(k):
            full[row][column] = unit[row][column] ^ inverse_transpose[row][column]
            full[row][k + column] = inverse_transpose[row][column]
            full[k + row][column] = inverse_transpose[row][column]
            full[k + row][k + column] = nilpotent[row][column] ^ inverse_transpose[row][column]
    free_rows = list(range(k)) + list(range(k, 2 * k - 1))
    free_columns = list(range(k)) + list(range(k + 1, 2 * k))
    return [[full[row][column] for column in free_columns] for row in free_rows]


def degenerate_factored(k: int) -> Matrix:
    matrix = [[0] * (2 * k - 1) for _ in range(2 * k - 1)]
    for index in range(1, k):
        left = [0] * (2 * k - 1)
        left[index] = 1
        left[k + index - 1] = 1
        right = [0] * (2 * k - 1)
        for position in range(index):
            right[position] = 1
        for position in range(1, index + 1):
            right[k + position - 1] = 1
        xor_into(matrix, outer(left, right))
    return matrix


def random_regular_matrix(size: int, generator: random.Random) -> Matrix:
    unit = identity(size)
    while True:
        candidate = [[generator.randrange(2) for _ in range(size)] for _ in range(size)]
        try:
            inverse(candidate)
            inverse(add(unit, candidate))
        except ValueError:
            continue
        return candidate


def regular_direct(c_matrix: Matrix) -> Matrix:
    size = len(c_matrix)
    unit = identity(size)
    d_matrix = transpose(c_matrix)
    a_matrix = inverse(add(unit, d_matrix))
    b_matrix = inverse(d_matrix)
    return [
        [
            (unit[row][column] ^ a_matrix[row][column])
            if block_row == 0 and block_column == 0
            else a_matrix[row][column]
            if block_row != 1 or block_column != 1
            else b_matrix[row][column] ^ a_matrix[row][column]
            for block_column in range(2)
            for column in range(size)
        ]
        for block_row in range(2)
        for row in range(size)
    ]


def regular_factored(c_matrix: Matrix) -> Matrix:
    size = len(c_matrix)
    unit = identity(size)
    d_matrix = transpose(c_matrix)
    a_matrix = inverse(add(unit, d_matrix))
    d_inverse = inverse(d_matrix)
    left = d_matrix + unit
    right = [unit[row] + d_inverse[row] for row in range(size)]
    return multiply(multiply(left, a_matrix), right)


def main() -> None:
    for k in range(1, 13):
        assert kronecker_direct(k) == kronecker_factored(k)
        assert rank(kronecker_direct(k)) == k - 1
        assert degenerate_direct(k) == degenerate_factored(k)
        assert rank(degenerate_direct(k)) == k - 1

    generator = random.Random(20260829)
    for size in range(2, 13):
        for _ in range(4):
            c_matrix = random_regular_matrix(size, generator)
            assert regular_direct(c_matrix) == regular_factored(c_matrix)
            assert rank(regular_direct(c_matrix)) == size

    print("PASS: K_k closed factorization and rank k-1 verified for k=1,...,12")
    print("PASS: D_k closed factorization and rank k-1 verified for k=1,...,12")
    print("PASS: R_d factorization and rank d verified on 44 exact regular pencils")
    print("NOTE: arbitrary length follows from the documented symbolic identities")


if __name__ == "__main__":
    main()
