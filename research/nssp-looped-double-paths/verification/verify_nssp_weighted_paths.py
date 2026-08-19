# AI-assisted generation and review: OpenAI Codex. Responsible maintainer: Carptopus.
"""Verify the weighted-path nSSP ansatz over an exact prime field.

Full column rank modulo a prime proves that the corresponding integer
verification matrix has full column rank over Q (and hence over R).
"""

from __future__ import annotations

import argparse


PRIME = 1_000_003


def weighted_path(n: int, loop: int) -> list[list[int]]:
    """Return a symmetric double-path matrix with edge j weighted by j."""
    matrix = [[0] * n for _ in range(n)]
    for j in range(1, n):
        matrix[j - 1][j] = j
        matrix[j][j - 1] = j
    matrix[loop - 1][loop - 1] = 1
    return matrix


def verification_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """Linearize A X^T - X^T A on entries where A is zero."""
    n = len(matrix)
    variables = [
        (i, j) for i in range(n) for j in range(n) if matrix[i][j] == 0
    ]
    result: list[list[int]] = []
    for row in range(n):
        for column in range(n):
            equation: list[int] = []
            for i, j in variables:
                coefficient = matrix[row][j] if column == i else 0
                if row == j:
                    coefficient -= matrix[i][column]
                equation.append(coefficient)
            result.append(equation)
    return result


def rank_mod_prime(matrix: list[list[int]], prime: int = PRIME) -> int:
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        pivot_row = work[rank]
        for j in range(column, columns):
            pivot_row[j] = pivot_row[j] * inverse % prime
        for row in range(rank + 1, rows):
            coefficient = work[row][column]
            if coefficient:
                for j in range(column, columns):
                    work[row][j] = (
                        work[row][j] - coefficient * pivot_row[j]
                    ) % prime
        rank += 1
        if rank == columns:
            break
    return rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=24)
    args = parser.parse_args()
    if args.max_n < 2 or args.max_n % 2:
        raise SystemExit("--max-n must be an even integer at least 2")

    checked = 0
    for n in range(2, args.max_n + 1, 2):
        # Check every naturally labelled loop position.  Reversal preserves the
        # pattern but sends the fixed formula b_j=j to b_j=n-j, so reflection
        # representatives alone would not test the same labelled formula.
        for loop in range(1, n + 1):
            verification = verification_matrix(weighted_path(n, loop))
            expected = (n - 1) ** 2
            actual = rank_mod_prime(verification)
            if actual != expected:
                raise AssertionError(
                    f"rank failure at n={n}, loop={loop}: {actual}/{expected}"
                )
            checked += 1
    print(
        f"PASS: {checked} weighted single-loop patterns, "
        f"all naturally labelled positions for even n<= {args.max_n}, "
        f"prime={PRIME}"
    )


if __name__ == "__main__":
    main()
