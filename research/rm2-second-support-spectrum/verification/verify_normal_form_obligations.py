"""Red-team the parameter inequalities used in the Walsh-atom normal-form proof.

The bounded loop is a falsification aid, not a proof for arbitrary m.  The
assertions mirror the symbolic cases stated in S3 and deliberately do not call
the construction probe's compatibility helpers.
"""

from __future__ import annotations

from itertools import product


def normalized_values(m: int) -> list[int]:
    return [0, -(1 << m)] + [
        sign * (1 << exponent)
        for exponent in range(m)
        for sign in (-1, 1)
    ]


def rank_options(m: int, value: int, *, odd_dimension: bool = False) -> set[int]:
    if value == -(1 << m):
        return {0}
    if value == 0:
        maximum_rank = 2 * m if odd_dimension else 2 * m - 2
        return set(range(0, maximum_rank + 1, 2))
    exponent = abs(value).bit_length() - 1
    return {2 * (m - exponent)}


def rank_compatible(
    m: int,
    values: tuple[int, int, int],
    *,
    odd_dimension: bool = False,
) -> bool:
    for ranks in product(
        *(rank_options(m, value, odd_dimension=odd_dimension) for value in values)
    ):
        if max(ranks) > sum(ranks) - max(ranks):
            continue
        valid = True
        for first, second, summed in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            if ranks[summed] != ranks[first] + ranks[second]:
                continue
            if not all(values[index] for index in (first, second, summed)):
                continue
            expected = values[first] * values[second] // (1 << m)
            if values[summed] != expected:
                valid = False
        if valid:
            return True
    return False


def rank_tuple_compatible(
    m: int,
    values: tuple[int, int, int],
    ranks: tuple[int, int, int],
    *,
    odd_dimension: bool,
) -> bool:
    if any(
        rank not in rank_options(m, value, odd_dimension=odd_dimension)
        for value, rank in zip(values, ranks, strict=True)
    ):
        return False
    if max(ranks) > sum(ranks) - max(ranks):
        return False
    for first, second, summed in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        if ranks[summed] != ranks[first] + ranks[second]:
            continue
        if not all(values[index] for index in (first, second, summed)):
            continue
        if values[summed] != values[first] * values[second] // (1 << m):
            return False
    return True


def lower_maximal_zero_ranks(
    m: int,
    values: tuple[int, int, int],
    ranks: tuple[int, int, int],
) -> tuple[int, int, int]:
    maximum = 2 * m
    lowered = list(ranks)
    maximal_zero_indices = [
        index
        for index, (value, rank) in enumerate(zip(values, ranks, strict=True))
        if value == 0 and rank == maximum
    ]
    if not maximal_zero_indices:
        return ranks
    if len(maximal_zero_indices) >= 2:
        for index in maximal_zero_indices:
            lowered[index] = maximum - 2
        return tuple(lowered)

    maximal_index = maximal_zero_indices[0]
    other_indices = [index for index in range(3) if index != maximal_index]
    first, second = (ranks[index] for index in other_indices)
    lowered[maximal_index] = maximum - 2
    if abs(first - second) <= maximum - 2:
        return tuple(lowered)

    rank_zero_index = next(
        index for index in other_indices if ranks[index] == 0
    )
    if values[rank_zero_index] != 0:
        raise AssertionError(("constant-extreme-should-have-negative-fiber", m, values, ranks))
    lowered[rank_zero_index] = 2
    return tuple(lowered)


def verify_maximal_zero_rank_lowering() -> int:
    checked = 0
    for m in range(2, 9):
        central = 1 << m
        for values in product(normalized_values(m), repeat=3):
            fibers = (
                central + values[0] + values[1] + values[2],
                central + values[0] - values[1] - values[2],
                central - values[0] + values[1] - values[2],
                central - values[0] - values[1] + values[2],
            )
            if any(value < 0 for value in fibers):
                continue
            for ranks in product(
                *(rank_options(m, value, odd_dimension=True) for value in values)
            ):
                if not rank_tuple_compatible(
                    m,
                    values,
                    ranks,
                    odd_dimension=True,
                ):
                    continue
                lowered = lower_maximal_zero_ranks(m, values, ranks)
                if not rank_tuple_compatible(
                    m,
                    values,
                    lowered,
                    odd_dimension=False,
                ):
                    raise AssertionError(
                        ("maximal-zero-rank-lowering", m, values, ranks, lowered)
                    )
                checked += 1
    return checked


def candidate_valid(
    m: int,
    values: tuple[int, int, int],
    *,
    odd_dimension: bool = False,
) -> bool:
    if not rank_compatible(m, values, odd_dimension=odd_dimension):
        return False
    central = 1 << m
    fibers = (
        central + values[0] + values[1] + values[2],
        central + values[0] - values[1] - values[2],
        central - values[0] + values[1] - values[2],
        central - values[0] - values[1] + values[2],
    )
    minimum = 1 << (m - 2)
    if any(value < 0 or (value and value < minimum) for value in fibers):
        return False
    return fibers[0] <= 5 * (1 << (m - 1))


def carried_even_triple(values: tuple[int, int, int]) -> tuple[int, int, int]:
    odd = [value for value in values if abs(value) == 1]
    even = [value for value in values if abs(value) != 1]
    if not odd:
        return tuple(value // 2 for value in values)
    if len(odd) != 2 or len(even) != 1:
        raise AssertionError(("even-parity", values))
    remainder = even[0] // 2
    if odd[0] == -odd[1]:
        return (remainder, 0, 0)
    return (remainder, odd[0], 0)


def check_odd_budget(m: int, values: tuple[int, int, int]) -> str:
    if -(1 << m) in values:
        raise AssertionError(("constant-survived-odd-layer", m, values))
    full = [value for value in values if abs(value) == 1]
    if len(full) == 3:
        return "O3-three-full"
    if len(full) != 1:
        raise AssertionError(("odd-full-count", m, values))

    remainder = list(values)
    remainder.remove(full[0])
    nonzero = [value for value in remainder if value]
    if len(nonzero) == 2:
        exponents = sorted(abs(value).bit_length() - 1 for value in nonzero)
        a, b = exponents
        if a < 1 or a + b > m:
            raise AssertionError(("O1-rank-budget", m, values, exponents))
        difference = a + b - (m - 2)
        if difference <= 0:
            seed_sum = difference & 1
        else:
            seed_sum = difference
        if seed_sum not in (0, 1, 2):
            raise AssertionError(("O1-seed", m, values, seed_sum))
        seed_exponents = ((0, 0), (0, 1), (1, 1))[seed_sum]
        cost = (a - seed_exponents[0]) + (b - seed_exponents[1])
        if cost < 0 or cost > m - 2 or (m - 2 - cost) % 2:
            raise AssertionError(("O1-cost", m, values, cost))
        if seed_sum == 2 and (m - 2 - cost) == 0:
            sign_product = 1
            for value in values:
                sign_product *= 1 if value > 0 else -1
            if sign_product != 1:
                raise AssertionError(("O1-critical-sign", m, values))
        return "O1-two-nonzero"

    if len(nonzero) == 1:
        exponent = abs(nonzero[0]).bit_length() - 1
        difference = exponent - (m - 2)
        seed_exponent = (difference & 1) if difference <= 0 else difference
        if seed_exponent not in (0, 1):
            raise AssertionError(("O2-seed", m, values, seed_exponent))
        cost = exponent - seed_exponent
        if cost < 0 or cost > m - 2 or (m - 2 - cost) % 2:
            raise AssertionError(("O2-cost", m, values, cost))
        return "O2-one-zero"

    if len(nonzero) == 0:
        return "O3-two-zero"
    raise AssertionError(("odd-unclassified", m, values))


def main() -> None:
    lowering_checks = verify_maximal_zero_rank_lowering()
    if rank_tuple_compatible(2, (0, 0, 1), (4, 0, 4), odd_dimension=False):
        raise AssertionError("negative control accepted the obsolete unchanged ranks")
    if not rank_tuple_compatible(2, (0, 0, 1), (2, 2, 4), odd_dimension=False):
        raise AssertionError("replacement ranks for the audit counterexample failed")
    print(
        "maximal zero-Walsh rank lowering: "
        f"{lowering_checks} compatible witnesses checked; audit counterexample repaired"
    )
    category_counts: dict[str, int] = {}
    for m in range(3, 13):
        even_checked = 0
        odd_checked = 0
        for values in product(normalized_values(m), repeat=3):
            if not candidate_valid(m, values):
                continue
            target = (1 << m) + sum(values)
            if target % 2 == 0:
                carried = carried_even_triple(values)
                if not candidate_valid(m - 1, carried):
                    raise AssertionError(("even-carry", m, values, carried))
                even_checked += 1
            else:
                category = check_odd_budget(m, values)
                category_counts[category] = category_counts.get(category, 0) + 1
                odd_checked += 1
        print(f"m={m}: even triples={even_checked}, odd triples={odd_checked}, PASS")
    for m in range(2, 13):
        even_dimension_candidates = {
            values
            for values in product(normalized_values(m), repeat=3)
            if candidate_valid(m, values)
        }
        odd_dimension_candidates = {
            values
            for values in product(normalized_values(m), repeat=3)
            if candidate_valid(m, values, odd_dimension=True)
        }
        if odd_dimension_candidates != even_dimension_candidates:
            raise AssertionError(
                (
                    "odd-even-normalized-candidates",
                    m,
                    sorted(odd_dimension_candidates - even_dimension_candidates),
                    sorted(even_dimension_candidates - odd_dimension_candidates),
                )
            )
        print(
            f"m={m}: odd/even normalized candidate triples agree "
            f"({len(even_dimension_candidates)} triples)"
        )
    print(f"odd categories={category_counts}")
    print("PASS: normal-form parity, budget, critical-sign, and carry obligations")


if __name__ == "__main__":
    main()
