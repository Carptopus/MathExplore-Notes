"""Verify the proposed infinite obstruction to odd-dimensional descent.

The mathematical proof has two parts.

1.  An explicit five-variable quadratic map is enlarged by hyperbolic pairs.
    Its normalized seven-point Walsh aggregate in dimension 2m+1 is

        K_m = 3 * 2**(m-1) + 5.

2.  In even dimension 2m, m >= 5, the elementary rank/sign reduction for
    this same aggregate leaves two normalized signature multisets.  In both
    cases the three rank-two points form a Fano line and the complementary
    affine plane has an odd number of full-rank points.  The maximal
    Pfaffian restricted to that plane is affine, so this is impossible.

This script checks the explicit witness directly in the first relevant
dimensions and exhausts the finite dyadic reduction for m=5,...,12.  It is a
certificate for the case reduction, not a replacement for the uniform
algebraic lemmas in the research note.
"""

from __future__ import annotations

from itertools import combinations_with_replacement, permutations, product

from probe_fano_signature_atoms import (
    NET5,
    components_independent_mod_constants,
    polynomial_from_terms,
    signature,
)


def fano_lines() -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (a - 1, b - 1, (a ^ b) - 1)
        for a in range(1, 8)
        for b in range(a + 1, 8)
        if b < (a ^ b)
    )


FANO_LINES = fano_lines()


def witness_components(m: int) -> tuple[int, int, int]:
    """Return the explicit map in odd dimension n=2m+1."""
    assert m >= 2
    n = 2 * m + 1
    hyperbolic_pairs = [(5 + 2 * index, 6 + 2 * index) for index in range(m - 2)]
    return (
        polynomial_from_terms(n, NET5[0] + hyperbolic_pairs),
        polynomial_from_terms(n, NET5[1], affine=2),  # add x_0
        polynomial_from_terms(n, NET5[2], affine=2),  # add x_0
    )


def expected_witness_signature(m: int) -> tuple[int, ...]:
    large = 1 << (m - 1)
    return (1, large, 1, large, 1, large, 2)


def normalized_alphabet(m: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                -(1 << m),
                0,
                *(sign * (1 << exponent) for sign in (-1, 1) for exponent in range(m)),
            }
        )
    )


def fixed_half_rank(m: int, value: int) -> int:
    if value == -(1 << m):
        return 0
    return m - (abs(value).bit_length() - 1)


def admissible_half_ranks(m: int, values: tuple[int, ...]) -> list[tuple[int, ...]]:
    options = [
        range(m) if value == 0 else (fixed_half_rank(m, value),)
        for value in values
    ]
    result: list[tuple[int, ...]] = []
    for ranks in product(*options):
        compatible = True
        for i, j, k in FANO_LINES:
            if (
                ranks[i] > ranks[j] + ranks[k]
                or ranks[j] > ranks[i] + ranks[k]
                or ranks[k] > ranks[i] + ranks[j]
            ):
                compatible = False
                break
            for largest, first, second in ((i, j, k), (j, i, k), (k, i, j)):
                if (
                    ranks[largest] == ranks[first] + ranks[second]
                    and values[largest]
                    and values[first]
                    and values[second]
                    and values[largest] * (1 << m)
                    != values[first] * values[second]
                ):
                    compatible = False
                    break
            if not compatible:
                break
        if compatible:
            result.append(tuple(ranks))
    return result


def reduced_even_signatures(m: int) -> set[tuple[int, ...]]:
    target = 3 * (1 << (m - 1)) + 5
    result: set[tuple[int, ...]] = set()
    for multiset in combinations_with_replacement(normalized_alphabet(m), 7):
        if sum(multiset) != target:
            continue
        for values in set(permutations(multiset)):
            if admissible_half_ranks(m, values):
                result.add(values)
    return result


def is_fano_line(points: frozenset[int]) -> bool:
    return any(points == frozenset(line) for line in FANO_LINES)


def main() -> None:
    # Direct truth-table/Walsh checks of the explicit family.  Stopping at
    # m=6 keeps the certificate fast while exercising two nontrivial lifts.
    for m in range(2, 7):
        components = witness_components(m)
        assert components_independent_mod_constants(components)
        values = signature(2 * m + 1, components)
        assert values == expected_witness_signature(m)
        assert sum(values) == 3 * (1 << (m - 1)) + 5

    for m in range(5, 13):
        large = 1 << (m - 1)
        expected_multisets = {
            (0, 1, 2, 2, large, large, large),
            (1, 1, 1, 2, large, large, large),
        }
        signatures = reduced_even_signatures(m)
        assert len(signatures) == 112
        assert {tuple(sorted(values)) for values in signatures} == expected_multisets

        for values in signatures:
            rank_two_points = frozenset(
                index for index, value in enumerate(values) if value == large
            )
            assert is_fano_line(rank_two_points)
            complement = set(range(7)) - rank_two_points
            full_rank_count = sum(abs(values[index]) == 1 for index in complement)
            assert full_rank_count in (1, 3)

    # Destructive control: removing one base quadratic term breaks the family.
    damaged = [terms.copy() for terms in NET5]
    damaged[0].pop()
    m = 5
    n = 2 * m + 1
    pairs = [(5 + 2 * index, 6 + 2 * index) for index in range(m - 2)]
    damaged_components = (
        polynomial_from_terms(n, damaged[0] + pairs),
        polynomial_from_terms(n, damaged[1], affine=2),
        polynomial_from_terms(n, damaged[2], affine=2),
    )
    assert signature(n, damaged_components) != expected_witness_signature(m)

    print("PASS: explicit odd-dimensional witness family verified")
    print("PASS: rank/sign endpoint reduction is stable for m=5,...,12")
    print("PASS: every reduced even signature is killed by Pfaffian parity")


if __name__ == "__main__":
    main()
