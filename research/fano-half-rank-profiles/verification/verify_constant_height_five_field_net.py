"""Verify the sharp constant-height-five Fano profile.

Let K = F_32 and V = K direct-sum K.  For a in K define

    B_a((x, y), (x', y')) = Tr(a * (x*y' + x'*y)).

The trace pairing on K is nondegenerate, so every B_a with a nonzero is a
nondegenerate alternating form on the ten-dimensional F_2-space V.  Taking
a in the span of 1, alpha, alpha^2 therefore realizes the constant Fano
half-rank profile (5, 5, 5, 5, 5, 5, 5).  This script constructs the three
matrices and verifies all seven ranks exactly over F_2.
"""

from __future__ import annotations


MODULUS = 0b100101  # x^5 + x^2 + 1
FIELD_MASK = 0b11111


def gf32_multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & 0b100000:
            left ^= MODULUS
    return result & FIELD_MASK


def gf32_square(value: int) -> int:
    return gf32_multiply(value, value)


def gf32_trace(value: int) -> int:
    total = 0
    conjugate = value
    for _ in range(5):
        total ^= conjugate
        conjugate = gf32_square(conjugate)
    assert total in (0, 1)
    return total


def alternating_form_rows(parameter: int) -> tuple[int, ...]:
    rows = [0] * 10
    for left_coordinate in range(5):
        left = 1 << left_coordinate
        for right_coordinate in range(5):
            right = 1 << right_coordinate
            entry = gf32_trace(gf32_multiply(parameter, gf32_multiply(left, right)))
            if entry:
                rows[left_coordinate] |= 1 << (5 + right_coordinate)
                rows[5 + right_coordinate] |= 1 << left_coordinate
    return tuple(rows)


def binary_rank(rows: tuple[int, ...], dimension: int) -> int:
    reduced = list(rows)
    rank = 0
    for column in range(dimension):
        pivot = next(
            (row for row in range(rank, dimension) if (reduced[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        reduced[rank], reduced[pivot] = reduced[pivot], reduced[rank]
        for row in range(dimension):
            if row != rank and ((reduced[row] >> column) & 1):
                reduced[row] ^= reduced[rank]
        rank += 1
    return rank


def main() -> None:
    parameters = (1, 0b10, 0b100)
    assert len(set(parameters)) == 3
    forms = tuple(alternating_form_rows(parameter) for parameter in parameters)

    ranks = []
    for mask in range(1, 8):
        selected = tuple(forms[index] for index in range(3) if (mask >> index) & 1)
        rows = tuple(0 for _ in range(10))
        for form in selected:
            rows = tuple(left ^ right for left, right in zip(rows, form))
        ranks.append(binary_rank(rows, 10))

    assert ranks == [10] * 7
    print(f"parameters={parameters}")
    print(f"ranks={tuple(ranks)}")
    print("half_rank_profile=(5,5,5,5,5,5,5)")
    print("PASS: the finite-field trace construction is nondegenerate in all seven directions")


if __name__ == "__main__":
    main()
