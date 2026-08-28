"""Exact calibration for antichain polynomials of three-chain products.

The recurrence is Theorem A of Ding--Dong (arXiv:1905.06692).  This file is a
discovery/negative-control tool; its finite output is not used as a proof of the
all-parameter classification.
"""

from __future__ import annotations

from itertools import combinations_with_replacement


def _predecessors(ideal: tuple[int, ...]):
    candidate = [0] * len(ideal)

    def visit(index: int, lower: int):
        if index == len(ideal):
            yield tuple(candidate)
            return
        for value in range(lower, ideal[index] + 1):
            candidate[index] = value
            yield from visit(index + 1, value)

    yield from visit(0, 0)


def _add_shift(target: list[int], source: list[int], shift: int) -> None:
    required = len(source) + shift
    if len(target) < required:
        target.extend([0] * (required - len(target)))
    for degree, coefficient in enumerate(source):
        target[degree + shift] += coefficient


def antichain_polynomials(max_first: int, second: int, third: int):
    """Return N_[k]x[second]x[third] for 1 <= k <= max_first."""

    ideals = list(combinations_with_replacement(range(third + 1), second))
    ideal_index = {ideal: index for index, ideal in enumerate(ideals)}
    transitions: list[list[tuple[int, int]]] = []
    for ideal in ideals:
        row = []
        for predecessor in _predecessors(ideal):
            exponent = len(
                {
                    height
                    for height, old_height in zip(ideal, predecessor)
                    if height > old_height
                }
            )
            row.append((ideal_index[predecessor], exponent))
        transitions.append(row)

    vectors = [
        [0] * len({height for height in ideal if height > 0}) + [1]
        for ideal in ideals
    ]
    results = {}
    for first in range(1, max_first + 1):
        polynomial: list[int] = []
        for component in vectors:
            _add_shift(polynomial, component, 0)
        while polynomial and polynomial[-1] == 0:
            polynomial.pop()
        results[first] = polynomial

        if first == max_first:
            break
        next_vectors = []
        for row in transitions:
            component = []
            for predecessor_index, exponent in row:
                _add_shift(component, vectors[predecessor_index], exponent)
            next_vectors.append(component)
        vectors = next_vectors
    return results


def is_monic_candidate(first: int, second: int, third: int) -> bool:
    """Ding--Dong Lemma 2.3(a), for first <= second <= third."""

    return (
        first >= third - second + 1
        and (first - (third - second + 1)) % 2 == 0
    )


def predicted_next_to_leading(first: int, second: int, depth: int) -> int:
    """Conjectured/proved-by-lattice-count formula for the monic stratum.

    Here third = first + second - 1 - 2 * depth.  This function is kept
    separate from the transfer recurrence so the latter remains an independent
    finite regression check.
    """

    from math import comb

    if depth == 0:
        return (
            2 * comb(first + second, first)
            + first * first
            + second * second
            + first * second
            - 3 * first
            - 3 * second
        )
    return (
        first * first
        + second * second
        + first * second
        - 2 * depth * (first + second)
        + 2 * depth * depth
        - first
        - second
        + 2 * depth
        + 2
    )


def main() -> None:
    example = antichain_polynomials(4, 2, 3)[4]
    assert example == [1, 24, 120, 200, 120, 24, 1]

    palindromic = []
    for second in range(2, 6):
        for third in range(second, 11):
            candidates = [
                first
                for first in range(2, second + 1)
                if is_monic_candidate(first, second, third)
            ]
            if not candidates:
                continue
            polynomials = antichain_polynomials(max(candidates), second, third)
            for first in candidates:
                polynomial = polynomials[first]
                if polynomial == polynomial[::-1]:
                    palindromic.append((first, second, third))

    expected = [(2, r, r + 1) for r in range(2, 6)]
    assert palindromic == expected

    coefficient_checks = []
    for first, second, depth in [
        (3, 3, 0),
        (3, 7, 0),
        (3, 3, 1),
        (3, 7, 1),
        (4, 6, 1),
        (5, 7, 1),
        (5, 5, 2),
        (5, 6, 2),
    ]:
        third = first + second - 1 - 2 * depth
        polynomial = antichain_polynomials(first, second, third)[first]
        observed = polynomial[-2]
        predicted = predicted_next_to_leading(first, second, depth)
        assert observed == predicted, (first, second, depth, observed, predicted)
        coefficient_checks.append((first, second, depth, observed))

    print("calibration: PASS")
    print("palindromic triples:", palindromic)
    print("next-to-leading checks:", coefficient_checks)


if __name__ == "__main__":
    main()
