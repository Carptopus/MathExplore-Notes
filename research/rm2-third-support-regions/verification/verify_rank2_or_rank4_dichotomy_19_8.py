"""Verify the Fano arithmetic behind the 19/8 rank-two/rank-four dichotomy."""

from __future__ import annotations

from itertools import combinations_with_replacement, permutations


FANO_LINES = (
    (1, 2, 3),
    (1, 4, 5),
    (1, 6, 7),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 5, 6),
)


def polar_rank(normalized_walsh: int) -> int:
    exponent = abs(normalized_walsh).bit_length() - 1
    return 2 * (6 - exponent)


def violates_extremal_sign_line(signature: tuple[int, ...]) -> bool:
    for a, b, c in FANO_LINES:
        values = (signature[a - 1], signature[b - 1], signature[c - 1])
        ranks = tuple(polar_rank(value) for value in values)
        largest = max(ranks)
        if largest != sum(ranks) - largest:
            continue
        largest_index = ranks.index(largest)
        other_indices = [index for index in range(3) if index != largest_index]
        largest_sign = 1 if values[largest_index] > 0 else -1
        other_sign_product = 1
        for index in other_indices:
            other_sign_product *= 1 if values[index] > 0 else -1
        if largest_sign != other_sign_product:
            return True
    return False


def main() -> None:
    # The normalized rank-zero endpoints are excluded before enumeration:
    # +64 would mean a nonzero output combination is the zero function,
    # while -64 would make it the constant-one function and force Z(F)=0.
    # W_a / 2^(n-6) is zero or a signed dyadic power.  Once negative rank-two
    # (-32) and negative rank-four (-16) terms are excluded, fractional terms
    # cannot contribute to a sum of -45: two or more leave at most five integer
    # terms, whose total is greater than -45.  The remaining integer arithmetic
    # is checked here.
    allowed = tuple(sorted((0, -1, 1, -2, 2, -4, 4, -8, 8, 16, 32)))
    multisets = [
        values
        for values in combinations_with_replacement(allowed, 7)
        if sum(values) == -45
    ]
    assert multisets == [(-8, -8, -8, -8, -8, -4, -1)]

    labelled = set(permutations(multisets[0]))
    assert len(labelled) == 42
    assert all(violates_extremal_sign_line(signature) for signature in labelled)

    print("PASS: every 19/8 candidate has a negative rank-two or rank-four Walsh term")
    print("DETAIL: all 42 no-rank2/no-rank4 Fano labelings violate an extremal sign line")


if __name__ == "__main__":
    main()
