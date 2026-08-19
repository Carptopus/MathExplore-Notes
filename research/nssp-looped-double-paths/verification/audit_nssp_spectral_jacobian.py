# AI-assisted generation and review: OpenAI Codex. Responsible maintainer: Carptopus.
"""Jacobian audit for the single-loop nSSP proof route."""

from __future__ import annotations

from verify_nssp_weighted_paths import (
    PRIME,
    rank_mod_prime,
    verification_matrix,
    weighted_path,
)


def add(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    return [
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    ]


def characteristic_polynomial(
    n: int, loop: int, loop_value: int, edge_weights: list[int]
) -> list[int]:
    """Continuant coefficients in ascending degree order."""
    previous = [1]
    current = [-loop_value if loop == 1 else 0, 1]
    for vertex in range(2, n + 1):
        diagonal = loop_value if vertex == loop else 0
        x_minus_diagonal = add([0] + current, [-diagonal * x for x in current])
        edge_term = [
            -(edge_weights[vertex - 2] ** 2) * x for x in previous
        ]
        following = add(x_minus_diagonal, edge_term)
        previous, current = current, following
    return current


def coefficient_jacobian(n: int, loop: int, weights: list[int]) -> list[list[int]]:
    base = characteristic_polynomial(n, loop, 1, weights)
    columns: list[list[int]] = []

    # The characteristic polynomial is affine in the unique diagonal entry.
    loop_plus = characteristic_polynomial(n, loop, 2, weights)
    columns.append([loop_plus[d] - base[d] for d in range(n)])

    # Each edge parameter occurs only through b_j^2, so the centered
    # difference at integer b_j is the exact derivative divided by one.
    for j, weight in enumerate(weights):
        plus = weights[:]
        minus = weights[:]
        plus[j] = weight + 1
        minus[j] = weight - 1
        poly_plus = characteristic_polynomial(n, loop, 1, plus)
        poly_minus = characteristic_polynomial(n, loop, 1, minus)
        derivative = [
            (poly_plus[d] - poly_minus[d]) // 2 for d in range(n)
        ]
        columns.append(derivative)

    return [[columns[column][row] for column in range(n)] for row in range(n)]


def compressed_moment_matrix(matrix: list[list[int]], loop: int) -> list[list[int]]:
    n = len(matrix)
    identity = [[int(row == column) for column in range(n)] for row in range(n)]
    powers = [identity]
    for _ in range(1, n):
        old = powers[-1]
        powers.append(
            [
                [
                    sum(old[row][k] * matrix[k][column] for k in range(n))
                    for column in range(n)
                ]
                for row in range(n)
            ]
        )
    rows = [
        [2 * powers[k][j][j + 1] for k in range(n)] for j in range(n - 1)
    ]
    rows.append([powers[k][loop - 1][loop - 1] for k in range(n)])
    return rows


def outer(vector: list[int]) -> list[list[int]]:
    return [[left * right for right in vector] for left in vector]


def matrix_add(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [left[row][column] + right[row][column] for column in range(len(left))]
        for row in range(len(left))
    ]


def matrix_multiply(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    n = len(left)
    return [
        [
            sum(left[row][k] * right[k][column] for k in range(n))
            for column in range(n)
        ]
        for row in range(n)
    ]


def assert_direct_nssp_witness(
    matrix: list[list[int]], witness: list[list[int]]
) -> None:
    n = len(matrix)
    if not any(witness[row][column] for row in range(n) for column in range(n)):
        raise AssertionError("the direct collision witness is zero")
    if any(
        matrix[row][column] * witness[row][column]
        for row in range(n)
        for column in range(n)
    ):
        raise AssertionError("the direct collision witness meets the matrix pattern")
    left = matrix_multiply(matrix, witness)
    right = matrix_multiply(witness, matrix)
    if left != right:
        raise AssertionError("the direct collision witness does not commute")


def main() -> None:
    checked = 0
    for n in range(2, 13):
        weights = list(range(1, n))
        for loop in range(1, n + 1):
            matrix = weighted_path(n, loop)
            full_rank = len(verification_matrix(matrix)[0])
            verification_rank = rank_mod_prime(verification_matrix(matrix))
            coefficient_rank = rank_mod_prime(coefficient_jacobian(n, loop, weights))
            moment_rank = rank_mod_prime(compressed_moment_matrix(matrix, loop))
            expected = n if (n % 2 == 0 or loop % 2 == 1) else n - 1
            if coefficient_rank != expected or moment_rank != expected:
                raise AssertionError(
                    f"n={n}, loop={loop}: coeff={coefficient_rank}, "
                    f"moment={moment_rank}, expected={expected}"
                )
            if (verification_rank == full_rank) != (expected == n):
                raise AssertionError(
                    f"verification mismatch at n={n}, loop={loop}: "
                    f"{verification_rank}/{full_rank}"
                )
            checked += 1

    # Mod-p collision calibration: P_8 with loop 3 and unit edges has a common
    # arm eigenvalue.  Mod-p rank loss is only a calibration signal; the direct
    # integer witnesses below provide the real-field nSSP failure certificates.
    n, loop = 8, 3
    unit_weights = [1] * (n - 1)
    collision = weighted_path(n, loop)
    for j in range(n - 1):
        collision[j][j + 1] = collision[j + 1][j] = 1
    if rank_mod_prime(coefficient_jacobian(n, loop, unit_weights)) == n:
        raise AssertionError("collision control unexpectedly has full coefficient rank")
    if rank_mod_prime(verification_matrix(collision)) == (n - 1) ** 2:
        raise AssertionError("collision control unexpectedly has full rank mod p")

    # Nonzero shared arm eigenvalue.  The vectors z and Sz have eigenvalues
    # +1 and -1; the sum of their rank-one projectors cancels every edge entry.
    nonzero_collision = weighted_path(5, 3)
    for j, weight in enumerate([1, 2, 3, 1]):
        nonzero_collision[j][j + 1] = weight
        nonzero_collision[j + 1][j] = weight
    z = [3, 3, 0, -2, -2]
    sz = [3, -3, 0, 2, -2]
    assert_direct_nssp_witness(
        nonzero_collision, matrix_add(outer(z), outer(sz))
    )

    # Zero shared arm eigenvalue.  A single rank-one projector already has
    # zero products on adjacent vertices because the zero mode is bipartite.
    zero_collision = weighted_path(7, 4)
    for j, weight in enumerate([1, 1, 2, 3, 1, 1]):
        zero_collision[j][j + 1] = weight
        zero_collision[j + 1][j] = weight
    zero_mode = [3, 0, -3, 0, 2, 0, -2]
    assert_direct_nssp_witness(zero_collision, outer(zero_mode))

    print(
        f"PASS: {checked} weighted cases, mod-p collision calibration, and two "
        f"direct spectral-projector witnesses; coefficient Jacobian, moment "
        f"Jacobian, and nSSP rank agree modulo {PRIME}"
    )


if __name__ == "__main__":
    main()
