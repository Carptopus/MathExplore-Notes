"""Exact polynomial control for the S9 adjacent-path factorization."""

from __future__ import annotations

import argparse
from itertools import combinations


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def add(*polys):
    size = max((len(poly) for poly in polys), default=1)
    result = [0] * size
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            result[degree] += coefficient
    return trim(result)


def negate(poly):
    return tuple(-coefficient for coefficient in poly)


def multiply(first, second):
    result = [0] * (len(first) + len(second) - 1)
    for first_degree, first_coefficient in enumerate(first):
        for second_degree, second_coefficient in enumerate(second):
            result[first_degree + second_degree] += (
                first_coefficient * second_coefficient
            )
    return trim(result)


def shift(poly, degree):
    return (0,) * degree + tuple(poly)


def arm(length):
    return (0,) + (1,) * length


def arm_sum(arms):
    return add(*(arm(length) for length in arms)) if arms else (0,)


def e2(arms):
    return add(
        *(
            multiply(arm(arms[first]), arm(arms[second]))
            for first, second in combinations(range(len(arms)), 2)
        )
    ) if len(arms) >= 2 else (0,)


def variable_part(left, middle, right, beta):
    left_sum = arm_sum(left)
    middle_sum = arm_sum(middle)
    right_sum = arm_sum(right)
    left_rooted = add((1,), left_sum)
    middle_rooted = add((1,), middle_sum)
    right_rooted = add((1,), right_sum)
    return add(
        e2(left),
        e2(middle),
        e2(right),
        shift(multiply(left_rooted, middle_rooted), 1),
        shift(multiply(middle_rooted, right_rooted), beta),
        shift(multiply(left_rooted, right_rooted), beta + 1),
    )


def rhs(first, second, union, right, beta):
    first_sum = arm_sum(first)
    second_sum = arm_sum(second)
    union_sum = arm_sum(union)
    right_rooted = add((1,), arm_sum(right))
    bracket = add(
        first_sum,
        second_sum,
        negate(union_sum),
        negate(shift(right_rooted, beta)),
    )
    return multiply(
        multiply(add(first_sum, negate(second_sum)), (1, -1)),
        bracket,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-arm-total", type=int, default=16)
    args = parser.parse_args()

    checks = 0
    for path_total in range(2, args.max_arm_total + 1):
        path_candidates = [
            tuple(sorted((first, path_total - first), reverse=True))
            for first in range(1, path_total // 2 + 1)
        ]
        for middle in ((1,), (2, 1), (3, 2, 1), (2, 2, 1, 1)):
            union = tuple(sorted(path_candidates[0] + middle, reverse=True))
            for right in ((1, 1), (3, 1), (2, 2, 1)):
                for beta in (2, 3, 5):
                    # Reallocate only when the required candidate arms occur in
                    # the fixed union multiset.
                    for first in path_candidates:
                        first_list = list(union)
                        if any(first_list.count(value) < first.count(value) for value in set(first)):
                            continue
                        for value in first:
                            first_list.remove(value)
                        first_middle = tuple(sorted(first_list, reverse=True))
                        for second in path_candidates:
                            second_list = list(union)
                            if any(
                                second_list.count(value) < second.count(value)
                                for value in set(second)
                            ):
                                continue
                            for value in second:
                                second_list.remove(value)
                            second_middle = tuple(sorted(second_list, reverse=True))
                            difference = add(
                                variable_part(first, first_middle, right, beta),
                                negate(
                                    variable_part(
                                        second, second_middle, right, beta
                                    )
                                ),
                            )
                            assert difference == rhs(
                                first, second, union, right, beta
                            )
                            if first != second:
                                assert difference != (0,)
                            checks += 1

    print(f"PASS polynomial_checks={checks} nontrivial_collisions=0")


if __name__ == "__main__":
    main()
