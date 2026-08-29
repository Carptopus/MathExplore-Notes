"""Verify six-slice hit states for a regular chain singular at one point."""

from __future__ import annotations

from itertools import product


def core_points() -> list[tuple[int, int, int, int]]:
    return [
        u
        for u in product((0, 1), repeat=4)
        if (u[0] * u[1] + u[2] * u[3]) % 2 == 1
    ]


def affine_masks(points: list[tuple[int, int, int, int]]) -> set[int]:
    result: set[int] = set()
    for coefficients in product((0, 1), repeat=5):
        mask = 0
        for index, u in enumerate(points):
            value = coefficients[0]
            value ^= sum(coefficients[i + 1] * u[i] for i in range(4)) % 2
            mask |= value << index
        result.add(mask)
    return result


def rank_f2(matrix: list[list[int]]) -> int:
    rows = [row[:] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(len(rows)):
            if index != rank and rows[index][column]:
                rows[index] = [a ^ b for a, b in zip(rows[index], rows[rank])]
        rank += 1
    return rank


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]


def inverse_f2(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    rows = [
        matrix[index][:] + [1 if index == column else 0 for column in range(size)]
        for index in range(size)
    ]
    for column in range(size):
        pivot = next(index for index in range(column, size) if rows[index][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        for index in range(size):
            if index != column and rows[index][column]:
                rows[index] = [a ^ b for a, b in zip(rows[index], rows[column])]
    return [row[size:] for row in rows]


def control_rank(k: int) -> int:
    # N has ones at (i,i+1).  For Q1=x^T y and Q2=x^T N y,
    # the product-sign control matrix with p2=r2=0 is
    # K=I+(I+N)^(-T), of rank k-1.
    nilpotent = [[0] * k for _ in range(k)]
    for index in range(k - 1):
        nilpotent[index][index + 1] = 1
    identity_plus = [
        [nilpotent[i][j] ^ (1 if i == j else 0) for j in range(k)]
        for i in range(k)
    ]
    inverse_transpose = inverse_f2(transpose(identity_plus))
    control = [
        [inverse_transpose[i][j] ^ (1 if i == j else 0) for j in range(k)]
        for i in range(k)
    ]
    return rank_f2(control)


def main() -> None:
    points = core_points()
    affine = affine_masks(points)
    assert len(affine) == 32

    product_masks = {left & right for left in affine for right in affine}
    assert len(product_masks) == 58
    assert set(range(64)) - product_masks == {
        63 ^ (1 << index) for index in range(6)
    }

    # The nonzero set M of the degenerate Walsh entry is the simultaneous zero
    # set of two affine boundary coefficients, hence exactly a product mask.
    possible_nonzero_masks = product_masks

    # On every proper product mask (size at most four), restricting one product
    # already gives every subset.  Only M=H retains the six missing 5-subsets.
    for mask in possible_nonzero_masks:
        restricted_products = {candidate & mask for candidate in product_masks}
        expected = {subset for subset in range(64) if subset & ~mask == 0}
        if mask == 63:
            assert restricted_products == product_masks
        else:
            assert restricted_products == expected

    assert [control_rank(k) for k in range(1, 7)] == [0, 1, 2, 3, 4, 5]

    # k=1: on M the degenerate quadratic is zero and Q1=Q1+Q2, so the product
    # sign is positive.  k=2: the exact exponent reduces on M to one product,
    # (p1_1+p2_0)(r1_0+r2_1).  Thus M=H misses precisely the six 5-subsets;
    # for proper M the restriction is already arbitrary.  k>=3: rank(K)>=2,
    # and two affine products realize all 64 exponent masks before restriction.
    all_masks = set(range(64))
    sum_of_two_products = {
        first ^ second for first in product_masks for second in product_masks
    }
    assert sum_of_two_products == all_masks

    count_k1 = len(possible_nonzero_masks)
    count_k2 = sum(
        1 if mask == 0 else len({candidate & mask for candidate in product_masks})
        for mask in possible_nonzero_masks
    )
    count_long = sum(1 << mask.bit_count() for mask in possible_nonzero_masks)
    assert count_k1 == 58
    assert count_k2 == count_long - 6

    # Destructive controls for the two exceptional short lengths.
    five_point = 63 ^ 1
    assert five_point not in product_masks
    assert five_point in sum_of_two_products
    assert control_rank(1) < 1
    assert control_rank(2) < 2

    print("PASS: degenerate nonzero masks are exactly the 58 affine-product masks")
    print(f"PASS: length 1 has {count_k1} states with positive product sign")
    print(f"PASS: length 2 has {count_k2} states; only six full-mask signs are absent")
    print(f"PASS: every length >=3 has {count_long} mask/sign states")
    print("PASS: control ranks and short-length destructive controls verified")


if __name__ == "__main__":
    main()
