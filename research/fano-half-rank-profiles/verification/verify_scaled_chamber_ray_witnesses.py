"""Exact witnesses for the two scaled chamber-ray constructions.

The four-dimensional triple (12, 0, 22) realizes twice a single-zero
height-one profile.  The six-dimensional trace-pairing net over F_8 realizes
three times the constant height-one profile.  These are the sharp witnesses
required by Lemma 6.1 of the manuscript.
"""

from __future__ import annotations

from verify_realized_strengthened_fano_atoms import profile


MODULUS = 0b1011  # x^3 + x + 1
FIELD_MASK = 0b111


def gf8_multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & 0b1000:
            left ^= MODULUS
    return result & FIELD_MASK


def gf8_square(value: int) -> int:
    return gf8_multiply(value, value)


def gf8_trace(value: int) -> int:
    square = gf8_square(value)
    fourth = gf8_square(square)
    return (value ^ square ^ fourth) & 1


def trace_pairing_form(parameter: int) -> tuple[int, ...]:
    rows = [0] * 6
    basis = (1, 2, 4)
    for left, x in enumerate(basis):
        for right, y in enumerate(basis):
            value = gf8_trace(gf8_multiply(parameter, gf8_multiply(x, y)))
            if value:
                rows[left] |= 1 << (3 + right)
                rows[3 + right] |= 1 << left
    return tuple(rows)


def binary_rank(source: tuple[int, ...]) -> int:
    rows = list(source)
    rank = 0
    for column in range(len(rows)):
        pivot = next(
            (row for row in range(rank, len(rows)) if (rows[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(len(rows)):
            if row != rank and ((rows[row] >> column) & 1):
                rows[row] ^= rows[rank]
        rank += 1
    return rank


def main() -> None:
    doubled_single_zero = profile(12, 0, 22, 4)
    assert doubled_single_zero == (2, 0, 2, 2, 2, 2, 2)

    parameters = (1, 2, 4)
    forms = tuple(trace_pairing_form(parameter) for parameter in parameters)
    ranks = []
    for point in range(1, 8):
        rows = tuple(
            (forms[0][row] if point & 1 else 0)
            ^ (forms[1][row] if point & 2 else 0)
            ^ (forms[2][row] if point & 4 else 0)
            for row in range(6)
        )
        ranks.append(binary_rank(rows) // 2)
    assert tuple(ranks) == (3, 3, 3, 3, 3, 3, 3)

    print(f"doubled_single_zero={doubled_single_zero} masks=(12,0,22)")
    print(f"tripled_constant={tuple(ranks)} field_parameters={parameters}")
    print("PASS: both exceptional scaled chamber rays have sharp exact witnesses")


if __name__ == "__main__":
    main()
