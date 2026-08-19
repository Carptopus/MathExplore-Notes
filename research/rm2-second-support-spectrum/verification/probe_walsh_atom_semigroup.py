"""Calibrate a low-dimensional Walsh-atom model for the second support spectrum.

This is a discovery/calibration program, not a proof for arbitrary n.  Every
state in the generated semigroup is nevertheless realizable: coordinatewise
multiplication of Walsh triples is induced by direct sums on disjoint variable
blocks.
"""

from __future__ import annotations

from itertools import combinations, product

from probe_recursive_slice_construction import necessary_support_weights


def basis_words(n: int) -> list[int]:
    monomials = [()]
    monomials.extend((index,) for index in range(n))
    monomials.extend(combinations(range(n), 2))
    result: list[int] = []
    for indices in monomials:
        word = 0
        for point in range(1 << n):
            value = 1
            for index in indices:
                value &= (point >> index) & 1
            word |= value << point
        result.append(word)
    return result


def span(basis: list[int]) -> list[int]:
    words = [0]
    for vector in basis:
        words += [word ^ vector for word in words]
    return words


def walsh_triples(n: int, require_independent: bool) -> set[tuple[int, int, int]]:
    words = span(basis_words(n))
    length = 1 << n
    result: set[tuple[int, int, int]] = set()
    for left in words:
        for right in words:
            if require_independent and (left == 0 or right == 0 or left == right):
                continue
            result.add(
                (
                    length - 2 * left.bit_count(),
                    length - 2 * right.bit_count(),
                    length - 2 * (left ^ right).bit_count(),
                )
            )
    return result


def multiply_states(
    left_states: set[tuple[int, int, int]],
    right_states: set[tuple[int, int, int]],
) -> set[tuple[int, int, int]]:
    return {
        tuple(left * right for left, right in zip(first, second, strict=True))
        for first in left_states
        for second in right_states
    }


def support_projection(n: int, states: set[tuple[int, int, int]]) -> set[int]:
    length = 1 << n
    return {
        length - (length + sum(state)) // 4
        for state in states
        if all(component != length for component in state)
    }


def normalized(states: set[tuple[int, int, int]], divisor: int) -> set[tuple[int, int, int]]:
    return {tuple(value // divisor for value in state) for state in states}


def normalized_projection(m: int, states: set[tuple[int, int, int]]) -> set[int]:
    central = 1 << m
    return {
        central + sum(state)
        for state in states
        if all(component != central for component in state)
    }


def normalized_necessary_values(m: int) -> set[int]:
    n = 2 * m
    scale = 1 << (m - 2)
    return {
        ((1 << n) - support) // scale
        for support in necessary_support_weights(n)
    }


def vectorial_bent_idle_signs() -> set[tuple[int, int, int]]:
    """Realize every sign triple with an explicit F_2^4 -> F_2^2 bent map."""

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

    affine_linear_words = []
    for mask in range(16):
        word = 0
        for point in range(16):
            word |= dot(mask, point) << point
        affine_linear_words.append(word)

    def walsh(word: int) -> int:
        return 16 - 2 * word.bit_count()

    result = set()
    for left_shift in affine_linear_words:
        for right_shift in affine_linear_words:
            shifted_left = left ^ left_shift
            shifted_right = right ^ right_shift
            triple = (
                walsh(shifted_left),
                walsh(shifted_right),
                walsh(shifted_left ^ shifted_right),
            )
            if all(abs(value) == 4 for value in triple):
                result.add(tuple(value // 4 for value in triple))
    return result


def main() -> None:
    two_variable_atoms = normalized(
        walsh_triples(2, require_independent=False), divisor=2
    )
    four_variable_core = normalized(
        walsh_triples(4, require_independent=True), divisor=4
    )
    vectorial_bent_signs = vectorial_bent_idle_signs()
    if vectorial_bent_signs != set(product((-1, 1), repeat=3)):
        raise AssertionError(("vectorial-bent-signs", sorted(vectorial_bent_signs)))

    levels = [four_variable_core]
    for _ in range(1, 9):
        levels.append(multiply_states(levels[-1], two_variable_atoms))

    for m in range(2, 9):
        observed = normalized_projection(m, levels[m - 2])
        expected = normalized_necessary_values(m)
        if observed != expected:
            raise AssertionError((m, sorted(expected - observed), sorted(observed - expected)))
        print(f"m={m}: two-variable-only model matches ({len(observed)} values)")

    original_m9 = normalized_projection(9, levels[7])
    expected_m9 = normalized_necessary_values(9)
    first_gap = expected_m9 - original_m9
    expected_gap = {491, 493, 499, 501, 523, 525, 531, 533}
    if first_gap != expected_gap:
        raise AssertionError(("original-model-gap", sorted(first_gap)))
    print("negative control: the two-variable-only model first misses eight m=9 values")

    for m in range(2, 11):
        cost = m - 2
        revised_states = set(levels[cost])
        for two_variable_cost in range(cost % 2, cost - 1, 2):
            revised_states.update(
                multiply_states(levels[two_variable_cost], vectorial_bent_signs)
            )
        observed = normalized_projection(m, revised_states)
        expected = normalized_necessary_values(m)
        if observed != expected:
            raise AssertionError((m, sorted(expected - observed), sorted(observed - expected)))
        print(f"m={m}: revised 2D/4D atom model matches ({len(observed)} values)")

    damaged_atoms = {
        state
        for state in walsh_triples(2, require_independent=False)
        if tuple(sorted(abs(value) for value in state)) != (2, 2, 4)
    }
    damaged_states = multiply_states(
        walsh_triples(4, require_independent=True), damaged_atoms
    )
    missing = necessary_support_weights(6) - support_projection(6, damaged_states)
    if missing != {34}:
        raise AssertionError(("negative-control", sorted(missing)))
    print("negative control: removing single-coordinate-growth atoms loses n=6 weight 34")
    print("PASS: revised Walsh-atom calibration and two destructive controls")


if __name__ == "__main__":
    main()
