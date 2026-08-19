"""Probe a slice-recursive construction for the RM_2(2,n) second support spectrum."""

from __future__ import annotations

from itertools import combinations, product


def basis_words(n: int, degree: int) -> list[int]:
    monomials = [()]
    if degree >= 1:
        monomials.extend((i,) for i in range(n))
    if degree >= 2:
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


def polar_rank_options(n: int, walsh_value: int) -> set[int]:
    if walsh_value == -(1 << n):
        return {0}
    if walsh_value == 0:
        maximum_rank = 2 * (n // 2)
        # In even dimension a full-rank quadratic has nonzero Walsh transform
        # at every affine frequency.  In odd dimension the maximal alternating
        # rank still has a one-dimensional radical, so zero remains possible.
        if n % 2 == 0:
            maximum_rank -= 2
        return set(range(0, maximum_rank + 1, 2))
    for polar_rank in range(2, 2 * (n // 2) + 1, 2):
        if abs(walsh_value) == 1 << (n - polar_rank // 2):
            return {polar_rank}
    return set()


def rank_and_sign_compatible(
    n: int,
    walsh_values: tuple[int, int, int],
    polar_ranks: tuple[int, int, int],
) -> bool:
    left, right, total = polar_ranks
    if left > right + total or right > left + total or total > left + right:
        return False
    for first, second, summed in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        if polar_ranks[summed] != polar_ranks[first] + polar_ranks[second]:
            continue
        if not all(walsh_values[index] for index in (first, second, summed)):
            continue
        expected = walsh_values[first] * walsh_values[second] // (1 << n)
        if walsh_values[summed] != expected:
            return False
    return True


def necessary_support_weights(n: int) -> set[int]:
    """Weights surviving current Walsh, rank, sign, and Warning obstructions."""
    walsh_values = {0, -(1 << n)}
    for polar_rank in range(2, 2 * (n // 2) + 1, 2):
        amplitude = 1 << (n - polar_rank // 2)
        walsh_values.update((amplitude, -amplitude))
    minimum_fiber = 1 << max(0, n - 4)
    minimum_support = 3 * (1 << (n - 3))
    result: set[int] = set()
    for left, right, total in product(walsh_values, repeat=3):
        numerators = (
            (1 << n) + left + right + total,
            (1 << n) + left - right - total,
            (1 << n) - left + right - total,
            (1 << n) - left - right + total,
        )
        if any(value % 4 for value in numerators):
            continue
        fibers = tuple(value // 4 for value in numerators)
        if any(value < 0 or (value and value < minimum_fiber) for value in fibers):
            continue
        rank_choices = product(
            polar_rank_options(n, left),
            polar_rank_options(n, right),
            polar_rank_options(n, total),
        )
        if not any(
            rank_and_sign_compatible(n, (left, right, total), ranks)
            for ranks in rank_choices
        ):
            continue
        support = (1 << n) - fibers[0]
        if support >= minimum_support:
            result.add(support)
    return result


def initial_representatives(n: int) -> dict[int, tuple[int, int]]:
    words = span(basis_words(n, 2))
    target = necessary_support_weights(n)
    representatives: dict[int, tuple[int, int]] = {}
    for left_index in range(1, len(words)):
        left = words[left_index]
        for right_index in range(left_index + 1, len(words)):
            right = words[right_index]
            weight = (left | right).bit_count()
            if weight in target and weight not in representatives:
                representatives[weight] = (left, right)
                if representatives.keys() >= target:
                    return representatives
    return representatives


def lift_representatives(
    n: int, representatives: dict[int, tuple[int, int]]
) -> dict[int, tuple[int, int]]:
    """Lift n-variable pairs to n+1 variables by affine slice differences."""
    affine_words = span(basis_words(n, 1))
    half_length = 1 << n
    next_n = n + 1
    target = necessary_support_weights(next_n)
    lifted: dict[int, tuple[int, int]] = {}
    for left, right in representatives.values():
        low_support = (left | right).bit_count()
        for left_shift in affine_words:
            upper_left = left ^ left_shift
            for right_shift in affine_words:
                upper_right = right ^ right_shift
                weight = low_support + (upper_left | upper_right).bit_count()
                if weight in target and weight not in lifted:
                    new_left = left | (upper_left << half_length)
                    new_right = right | (upper_right << half_length)
                    lifted[weight] = (new_left, new_right)
                    if lifted.keys() >= target:
                        return lifted
    return lifted


def main() -> None:
    n = 4
    representatives = initial_representatives(n)
    for current_n in range(4, 11):
        target = necessary_support_weights(current_n)
        missing = sorted(target - representatives.keys())
        print(
            f"n={current_n}: reached={len(representatives)}/{len(target)}, "
            f"necessary_weights={sorted(target)}, missing={missing}"
        )
        if missing or current_n == 10:
            break
        representatives = lift_representatives(current_n, representatives)


if __name__ == "__main__":
    main()
