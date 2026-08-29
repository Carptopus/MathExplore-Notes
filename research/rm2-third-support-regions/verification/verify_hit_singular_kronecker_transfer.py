"""Verify six-slice hit states for singular odd Kronecker pencil blocks."""

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


def product_sign_rank(k: int) -> int:
    # On a slice where all three Walsh sums are nonzero, impose
    # p_k=0, s_0=0 and sum_i(p_i+s_i)=0.  Use
    # p_0,...,p_(k-1),s_1,...,s_(k-1) as free x-linear variables and eliminate
    # s_k.  The product-sign exponent is bilinear in these variables and the
    # 2k y-linear variables r_0,...,r_(k-1),t_0,...,t_(k-1).
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

            exponent_1 = sum(p[i] * r[i] for i in range(k)) % 2
            exponent_2 = sum(s[i + 1] * t[i] for i in range(k)) % 2
            partial = [0] * (k + 1)
            for i in range(1, k + 1):
                partial[i] = partial[i - 1] ^ r[i - 1] ^ t[i - 1]
            exponent_12 = sum(
                (p[i] ^ s[i]) * partial[i] for i in range(k + 1)
            ) % 2
            matrix[x_index][y_index] = exponent_1 ^ exponent_2 ^ exponent_12

    return rank_f2(matrix)


def main() -> None:
    points = core_points()
    affine = affine_masks(points)
    assert len(affine) == 32

    # Each of the three nonzero masks is the zero set of one affine boundary
    # coefficient.  The three coefficients are independent: choose p_k, s_0,
    # and then p_0 to prescribe their sum.  Hence every triple in A^3 occurs.
    zero_masks = {63 ^ mask for mask in affine}
    assert zero_masks == affine
    mask_triples = list(product(zero_masks, repeat=3))
    assert len(mask_triples) == 32**3

    product_masks = {left & right for left in affine for right in affine}
    assert len(product_masks) == 58
    assert [product_sign_rank(k) for k in range(1, 7)] == [0, 1, 2, 3, 4, 5]

    # k=1 has fixed positive product sign on the common nonzero set.  k=2 has
    # one affine-product exponent.  Its restriction is arbitrary on every
    # proper common mask; for the full six-point mask exactly the six 5-subsets
    # are absent.  k>=3 has at least two independent products, which realize
    # all Boolean functions on the common mask.
    for first, second, third in mask_triples:
        common = first & second & third
        restricted_products = {candidate & common for candidate in product_masks}
        all_subsets = {mask for mask in range(64) if mask & ~common == 0}
        if common == 63:
            assert len(restricted_products) == 58
        else:
            assert restricted_products == all_subsets

    count_k1 = len(mask_triples)
    count_long = sum(
        1 << (first & second & third).bit_count()
        for first, second, third in mask_triples
    )
    count_k2 = count_long - 6
    assert count_k1 == 32768
    assert count_k2 == 66425
    assert count_long == 66431

    # Destructive controls: length one has no sign-control product; length two
    # cannot realize a five-point exponent when all three masks are full.
    five_point = 63 ^ 1
    assert product_sign_rank(1) == 0
    assert five_point not in product_masks
    assert five_point in {
        first ^ second for first in product_masks for second in product_masks
    }

    print("PASS: three singular-block nonzero masks range independently over 32 affine masks")
    print("PASS: product-sign control rank is k-1")
    print(f"PASS: K1 has {count_k1} normalized hit states")
    print(f"PASS: K2 has {count_k2} normalized hit states")
    print(f"PASS: every Kk, k>=3, has {count_long} normalized hit states")
    print("PASS: short-block destructive controls verified")


if __name__ == "__main__":
    main()
