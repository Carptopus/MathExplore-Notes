"""Verify the finite rank-pattern exclusions used for n=8 and n=9.

The script exhausts every seven-word RM_2(2,n) weight multiset giving one of
the listed candidate support sizes.  Balanced quadratic words are branched
over every possible even polar rank.  It then applies only the rank-pattern
consequences proved in the accompanying research note.

This is an arithmetic certificate, not a substitute for the proofs of the
rank-geometry rules.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement, product


TARGETS = {
    8: {130, 132, 134, 138, 140, 142, 146, 150, 154, 158, 162},
    9: {260, 264, 268, 276, 280, 284, 292, 300, 308, 316, 324},
}


def weights_with_possible_ranks(n: int) -> list[tuple[int, tuple[int, ...]]]:
    """Return nonzero RM_2 weights and all compatible polar ranks."""
    half = 1 << (n - 1)
    entries = [
        # Balanced weight requires a nontrivial radical.  Hence the full even
        # rank n is excluded when n is even; range(0, n, 2) is exact in both
        # parities.
        (half, tuple(range(0, n, 2))),
        (1 << n, (0,)),
    ]
    for half_rank in range(1, n // 2 + 1):
        deviation = 1 << (n - half_rank - 1)
        entries.append((half - deviation, (2 * half_rank,)))
        entries.append((half + deviation, (2 * half_rank,)))
    return sorted(set(entries))


def rank_patterns(n: int, support: int) -> set[tuple[int, ...]]:
    """Enumerate all polar-rank multisets compatible with the weight average."""
    entries = weights_with_possible_ranks(n)
    patterns: set[tuple[int, ...]] = set()
    for indices in combinations_with_replacement(range(len(entries)), 7):
        if sum(entries[index][0] for index in indices) != 4 * support:
            continue
        for ranks in product(*(entries[index][1] for index in indices)):
            patterns.add(tuple(sorted(ranks)))
    return patterns


def arithmetic_candidates(n: int) -> set[int]:
    weights = sorted({weight for weight, _ in weights_with_possible_ranks(n)})
    minimum = 7 * (1 << (n - 4))
    half = 1 << (n - 1)
    length = 1 << n
    return {
        total // 4
        for choices in combinations_with_replacement(weights, 7)
        if (total := sum(choices)) % 4 == 0
        and total // 4 <= length
        and (total // 4 == minimum or total // 4 >= half)
    }


def may_have_polar_dimension_at_most_two(ranks: tuple[int, ...]) -> bool:
    """Test the necessary multiplicity pattern of a noninjective polar map.

    A linear map F_2^3 -> Alt(V) of rank at most two has a nonzero kernel.
    On the seven nonzero parameter points its multiset consists of one zero
    image and three image values, each repeated twice (with further merging
    possible).  The test deliberately gives this branch the benefit of doubt.
    """
    remaining = list(ranks)
    if 0 not in remaining:
        return False
    remaining.remove(0)
    return all(multiplicity % 2 == 0 for multiplicity in Counter(remaining).values())


def exclusion_reason(
    ranks: tuple[int, ...], *, use_maximal_pfaffian: bool = True
) -> str | None:
    rank_two = ranks.count(2)
    rank_four = ranks.count(4)
    rank_eight = ranks.count(8)
    rank_at_least_six = sum(rank >= 6 for rank in ranks)

    if rank_two >= 4 and rank_at_least_six:
        return "four rank-two points forbid rank at least six"

    # Six rank-two evaluations force the seventh Pfaffian evaluation to vanish.
    if rank_two >= 6 and any(rank >= 4 for rank in ranks):
        return "six rank-two points force the seventh rank at most two"

    # The remaining two rules use projective positions, so first separate the
    # noninjective polar-map multiplicity pattern instead of assuming injection.
    noninjective_pattern = may_have_polar_dimension_at_most_two(ranks)
    if 0 in ranks and not noninjective_pattern:
        return "a polar-map kernel point requires paired image multiplicities"
    if noninjective_pattern:
        return None

    if rank_two == 3 and rank_eight:
        if rank_at_least_six < 4:
            return "three rank-two points plus rank eight violate the line/basis split"
        if use_maximal_pfaffian and rank_eight < 2:
            return "maximal-Pfaffian update requires a second rank-eight point"

    if rank_two == 2 and rank_eight:
        if rank_four < 1 or rank_at_least_six < 3:
            return "two rank-two points plus rank eight violate the update-line bounds"

    return None


def main() -> None:
    expected8 = {
        112, 128, 136, 144, 148, 152, 156, 160, 164,
        *range(166, 253, 2),
        256,
    }
    expected9 = {2 * support for support in expected8}
    assert arithmetic_candidates(8) - expected8 == TARGETS[8] | {254}
    assert arithmetic_candidates(9) - expected9 == TARGETS[9] | {508}

    summaries: list[str] = []
    for n, targets in TARGETS.items():
        for support in sorted(targets):
            patterns = rank_patterns(n, support)
            assert patterns, (n, support, "no arithmetic patterns")
            unresolved = [pattern for pattern in patterns if exclusion_reason(pattern) is None]
            assert not unresolved, (n, support, unresolved)
            summaries.append(f"n={n}, s={support}: {len(patterns)} rank pattern(s) excluded")

    # Negative control: without the maximal-Pfaffian consequence requiring a
    # second rank-eight point, the final n=9 pattern would survive.
    residual_324 = (2, 2, 2, 6, 6, 6, 8)
    assert residual_324 in rank_patterns(9, 324)
    assert exclusion_reason(residual_324, use_maximal_pfaffian=False) is None
    assert exclusion_reason(residual_324) is not None

    print("PASS: exhaustive n=8 and n=9 rank-pattern exclusions verified")
    for summary in summaries:
        print(summary)


if __name__ == "__main__":
    main()
