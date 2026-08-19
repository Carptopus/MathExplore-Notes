"""Verify the explicit low-dimensional Walsh atoms used by the proof draft.

This verifier evaluates all 16 inputs directly.  It does not import the atom
semigroup or the necessary-spectrum implementation.
"""

from __future__ import annotations


Term = tuple[int, ...]


def polynomial_word(terms: list[Term]) -> int:
    word = 0
    for point in range(16):
        value = 0
        for term in terms:
            monomial = 1
            for index in term:
                monomial &= (point >> index) & 1
            value ^= monomial
        word |= value << point
    return word


def linear_word(mask: int) -> int:
    word = 0
    for point in range(16):
        word |= ((mask & point).bit_count() & 1) << point
    return word


def walsh(word: int) -> int:
    return 16 - 2 * word.bit_count()


def triple(left: int, right: int) -> tuple[int, int, int]:
    return tuple(value // 4 for value in (walsh(left), walsh(right), walsh(left ^ right)))


def sign_pattern(values: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(0 if value == 0 else (1 if value > 0 else -1) for value in values)


def verify_base_common_zero_table() -> None:
    rows = {
        0: ([()], [(0,)]),
        1: ([(), (0, 1)], [(), (2, 3)]),
        2: ([(0,)], [(), (1, 2)]),
        3: ([(0, 1)], [(), (2, 3)]),
        4: ([(0,)], [(1,)]),
        5: ([(0, 1)], [(), (0,), (2, 3)]),
        6: ([(0,)], [(1, 2)]),
        7: ([(0, 1)], [(0,), (2, 3)]),
        8: ([(0,)], [(0, 1)]),
        9: ([(0, 1)], [(2, 3)]),
        10: ([(0, 1)], [(0, 2)]),
    }
    for expected, (left_terms, right_terms) in rows.items():
        left = polynomial_word(left_terms)
        right = polynomial_word(right_terms)
        if left == 0 or right == 0 or left == right:
            raise AssertionError(("dependent-base-pair", expected))
        observed = 16 - (left | right).bit_count()
        if observed != expected:
            raise AssertionError(("base-common-zeros", expected, observed))


def verify_core_rows() -> None:
    q = [(0, 3), (1, 2)]
    rows = {
        (1, 0, 0): (q, [(0,), (1,), (0, 3)]),
        (1, 1, 0): (q, q + [(0,)]),
        (1, 1, 1): (q, [(0, 2), (0, 3), (1, 3)]),
        (1, 1, 2): (q, q + [(0, 1)]),
        (1, 2, 0): (q, [(0,), (0, 3)]),
        (1, 2, 2): (q, [(0, 3)]),
    }
    expected_sign_counts = {
        (1, 0, 0): 2,
        (1, 1, 0): 4,
        (1, 1, 1): 8,
        (1, 1, 2): 8,
        (1, 2, 0): 4,
        (1, 2, 2): 4,
    }
    for absolute_type, (left_terms, right_terms) in rows.items():
        left = polynomial_word(left_terms)
        right = polynomial_word(right_terms)
        if tuple(abs(value) for value in triple(left, right)) != absolute_type:
            raise AssertionError((absolute_type, triple(left, right)))
        signs = set()
        for left_mask in range(32):
            left_affine = linear_word(left_mask & 15) ^ (0xFFFF if left_mask & 16 else 0)
            for right_mask in range(32):
                right_affine = linear_word(right_mask & 15) ^ (0xFFFF if right_mask & 16 else 0)
                values = triple(left ^ left_affine, right ^ right_affine)
                if tuple(abs(value) for value in values) == absolute_type:
                    signs.add(sign_pattern(values))
        if len(signs) != expected_sign_counts[absolute_type]:
            raise AssertionError((absolute_type, sorted(signs)))
        if absolute_type == (1, 2, 2):
            if any(first * second * third != 1 for first, second, third in signs):
                raise AssertionError((absolute_type, sorted(signs)))


def verify_vectorial_bent_masks() -> None:
    def dot(left: int, right: int) -> int:
        return (left & right).bit_count() & 1

    def matrix_m(vector: int) -> int:
        low = vector & 1
        high = (vector >> 1) & 1
        return high | ((low ^ high) << 1)

    left = 0
    right = 0
    for point in range(16):
        x = point & 3
        y = point >> 2
        left |= dot(x, y) << point
        right |= dot(x, matrix_m(y)) << point

    masks = {
        (-1, -1, -1): (5, 15),
        (-1, -1, 1): (5, 5),
        (-1, 1, -1): (5, 2),
        (-1, 1, 1): (5, 0),
        (1, -1, -1): (0, 6),
        (1, -1, 1): (0, 5),
        (1, 1, -1): (0, 7),
        (1, 1, 1): (0, 0),
    }
    for expected, (left_mask, right_mask) in masks.items():
        observed = triple(
            left ^ linear_word(left_mask),
            right ^ linear_word(right_mask),
        )
        if observed != expected:
            raise AssertionError((expected, observed, left_mask, right_mask))


def main() -> None:
    verify_base_common_zero_table()
    verify_core_rows()
    verify_vectorial_bent_masks()
    print(
        "PASS: base common-zero table, explicit 4-variable core rows, "
        "and all eight idle-atom signs"
    )


if __name__ == "__main__":
    main()
