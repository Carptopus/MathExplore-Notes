"""Regression checks for six stable odd-descent endpoint families.

The uniform proof is in ../六个稳定端点异常族证明.md.  This program reuses
the audited Fano rank/sign helpers from the preceding case; it is a regression
check, not an independent implementation of the proof.
"""

from __future__ import annotations

import sys
from itertools import combinations_with_replacement, permutations
from pathlib import Path


CURRENT = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT))

from probe_fano_signature_atoms import (  # noqa: E402
    NET5,
    components_independent_mod_constants,
    polynomial_from_terms,
    signature,
)
from verify_odd_descent_counterexample_family import (  # noqa: E402
    admissible_half_ranks,
    is_fano_line,
    normalized_alphabet,
)


AFFINE_MASKS = {
    -5: (1, 2, 2),
    -3: (1, 2, 63),
    -1: (1, 28, 4),
    1: (4, 2, 63),
    3: (0, 2, 63),
    5: (0, 2, 2),
}

BASE_SIGNATURES = {
    -5: (-1, 2, -1, 2, -1, 2, -2),
    -3: (-1, 2, -1, 2, -1, 2, 0),
    -1: (-1, 2, 0, 2, 0, 2, 0),
    1: (0, 2, 0, 2, 1, 2, 0),
    3: (1, 2, 1, 2, 1, 2, 0),
    5: (1, 2, 1, 2, 1, 2, 2),
}


def witness_components(m: int, c: int) -> tuple[int, int, int]:
    assert m >= 2 and c in AFFINE_MASKS
    n = 2 * m + 1
    hyperbolic_pairs = [(5 + 2 * j, 6 + 2 * j) for j in range(m - 2)]
    masks = AFFINE_MASKS[c]
    return (
        polynomial_from_terms(n, NET5[0] + hyperbolic_pairs, affine=masks[0]),
        polynomial_from_terms(n, NET5[1], affine=masks[1]),
        polynomial_from_terms(n, NET5[2], affine=masks[2]),
    )


def expected_signature(m: int, c: int) -> tuple[int, ...]:
    base = BASE_SIGNATURES[c]
    factor = 1 << (m - 2)
    return tuple(value * factor if index in (1, 3, 5) else value for index, value in enumerate(base))


def reduced_even_signatures(m: int, c: int) -> set[tuple[int, ...]]:
    target = 3 * (1 << (m - 1)) + c
    result: set[tuple[int, ...]] = set()
    for multiset in combinations_with_replacement(normalized_alphabet(m), 7):
        if sum(multiset) != target:
            continue
        for values in set(permutations(multiset)):
            if admissible_half_ranks(m, values):
                result.add(values)
    return result


def main() -> None:
    for c in AFFINE_MASKS:
        for m in range(2, 7):
            components = witness_components(m, c)
            assert components_independent_mod_constants(components)
            values = signature(2 * m + 1, components)
            assert values == expected_signature(m, c)
            assert sum(values) == 3 * (1 << (m - 1)) + c

    for m in range(6, 11):
        large = 1 << (m - 1)
        for c in AFFINE_MASKS:
            signatures = reduced_even_signatures(m, c)
            assert signatures
            for values in signatures:
                low_rank_points = frozenset(
                    index for index, value in enumerate(values) if value == large
                )
                assert is_fano_line(low_rank_points)
                complement = set(range(7)) - low_rank_points
                assert sum(abs(values[index]) == 1 for index in complement) % 2 == 1

    damaged = list(witness_components(2, 5))
    damaged[2] ^= 1
    assert signature(5, tuple(damaged)) != expected_signature(2, 5)

    print("PASS: six explicit odd-dimensional families verified")
    print("PASS: even rank/sign reductions stabilize for m=6,...,10")
    print("PASS: every stable survivor violates maximal-Pfaffian parity")


if __name__ == "__main__":
    main()
