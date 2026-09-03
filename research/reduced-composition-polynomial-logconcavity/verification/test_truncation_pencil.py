"""Exact checks for the allowed-weight truncation-column pencil.

This is a discovery and falsification tool, not a proof.  It checks the exact
Ardila--Doker merge recurrence and minimizes every adjacent log-concavity
defect over both the conjectured allowed interval and the deliberately larger
interval [0, 1].
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
from math import comb
from typing import Iterable, Sequence


def compositions(total: int) -> Iterable[tuple[int, ...]]:
    if total == 1:
        yield (1,)
        return
    for mask in range(1 << (total - 1)):
        parts: list[int] = []
        previous = 0
        for cut in range(1, total):
            if mask & (1 << (cut - 1)):
                parts.append(cut - previous)
                previous = cut
        parts.append(total - previous)
        yield tuple(parts)


def coefficients(parts: Sequence[int]) -> list[Fraction]:
    """Return the exact reduced composition-polynomial coefficients."""

    knots = [0]
    for part in parts:
        knots.append(knots[-1] + part)
    length = len(parts)
    size = knots[-1]
    result: list[Fraction] = []
    for index in range(size - length + 1):
        value = Fraction()
        for knot_index, knot in enumerate(knots):
            if knot > index:
                continue
            denominator = 1
            for other in knots:
                if other != knot:
                    denominator *= abs(other - knot)
            value += Fraction(
                (-1) ** knot_index
                * comb(length + index - knot - 1, length - 1),
                denominator,
            )
        result.append(value)
    return result


def padded_truncation_columns(
    refined_parts: Sequence[int],
) -> tuple[list[Fraction], list[Fraction]]:
    size = sum(refined_parts)
    target_length = size - (len(refined_parts) - 1) + 1
    left = coefficients(refined_parts[:-1])
    right = [Fraction()] * refined_parts[0] + coefficients(refined_parts[1:])
    left.extend([Fraction()] * (target_length - len(left)))
    right.extend([Fraction()] * (target_length - len(right)))
    return left, right


def merge(parts: Sequence[int], split: int) -> tuple[int, ...]:
    """Merge positions split-1 and split, where 1 <= split < len(parts)."""

    return (
        *parts[: split - 1],
        parts[split - 1] + parts[split],
        *parts[split + 1 :],
    )


def defect_quadratic(
    left: Sequence[Fraction], right: Sequence[Fraction], index: int
) -> tuple[Fraction, Fraction, Fraction]:
    delta = [a - b for a, b in zip(left, right, strict=True)]
    quadratic = delta[index] ** 2 - delta[index - 1] * delta[index + 1]
    linear = (
        2 * right[index] * delta[index]
        - right[index - 1] * delta[index + 1]
        - delta[index - 1] * right[index + 1]
    )
    constant = right[index] ** 2 - right[index - 1] * right[index + 1]
    return quadratic, linear, constant


def evaluate(poly: tuple[Fraction, Fraction, Fraction], value: Fraction) -> Fraction:
    quadratic, linear, constant = poly
    return quadratic * value * value + linear * value + constant


def interval_minimum(
    poly: tuple[Fraction, Fraction, Fraction],
    lower: Fraction,
    upper: Fraction,
) -> tuple[Fraction, Fraction]:
    candidates = [(evaluate(poly, lower), lower), (evaluate(poly, upper), upper)]
    quadratic, linear, _ = poly
    if quadratic > 0:
        vertex = -linear / (2 * quadratic)
        if lower <= vertex <= upper:
            candidates.append((evaluate(poly, vertex), vertex))
    return min(candidates)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-size", type=int, default=13)
    args = parser.parse_args()

    counts = {
        "refined_compositions": 0,
        "merge_identities": 0,
        "difference_identities": 0,
        "eulerian_operator_identities": 0,
        "defects": 0,
        "allowed_failures": 0,
        "convex": 0,
        "linear": 0,
        "concave": 0,
        "negative_global_minima": 0,
        "negative_global_outside_allowed": 0,
        "adjacent_column_minors": 0,
        "minor_identities": 0,
        "log_concavity_defects": 0,
    }
    first_allowed_failure: tuple[object, ...] | None = None
    first_negative_control: tuple[object, ...] | None = None

    for size in range(2, args.max_size + 1):
        for parts in compositions(size):
            if len(parts) < 2:
                continue
            counts["refined_compositions"] += 1
            left, right = padded_truncation_columns(parts)
            full = coefficients(parts)
            lower = Fraction(parts[0], size)
            upper = Fraction(size - parts[-1], size)

            expected_difference = [
                size
                * (
                    (full[index] if index < len(full) else Fraction())
                    - (full[index - 1] if 0 <= index - 1 < len(full) else Fraction())
                )
                for index in range(len(left))
            ]
            counts["difference_identities"] += 1
            if [a - b for a, b in zip(left, right, strict=True)] != expected_difference:
                raise AssertionError(f"difference identity failed: parts={parts}")

            # The endpoint-truncation columns are adjacent columns of one
            # order-len(parts)-1 refinement matrix.  Total nonnegativity
            # predicts these consecutive-row minors to be nonnegative.  The
            # following exact identity is the algebraic bridge from those
            # minors to log-concavity of the full refined column.
            order_minus_one = len(parts) - 1
            for index in range(len(left) - 1):
                minor = left[index] * right[index + 1] - left[index + 1] * right[index]
                counts["adjacent_column_minors"] += 1
                if minor < 0:
                    raise AssertionError(
                        f"negative adjacent-column minor: parts={parts}, index={index}"
                    )

                full_index = index
                previous = (
                    full[full_index - 1]
                    if 0 <= full_index - 1 < len(full)
                    else Fraction()
                )
                current = (
                    full[full_index]
                    if 0 <= full_index < len(full)
                    else Fraction()
                )
                following = (
                    full[full_index + 1]
                    if 0 <= full_index + 1 < len(full)
                    else Fraction()
                )
                defect = current * current - previous * following
                first_difference = current - previous
                next_difference = following - current
                expected_minor = size * (
                    order_minus_one * defect
                    - first_difference * next_difference
                )
                counts["minor_identities"] += 1
                if minor != expected_minor:
                    raise AssertionError(
                        f"minor identity failed: parts={parts}, index={index}"
                    )

                if 0 < full_index < len(full) - 1:
                    counts["log_concavity_defects"] += 1
                    if defect < 0:
                        raise AssertionError(
                            f"negative full-column defect: parts={parts}, index={index}"
                        )

            for split in range(1, len(parts)):
                weight = Fraction(sum(parts[:split]), size)
                reconstructed = [
                    weight * a + (1 - weight) * b
                    for a, b in zip(left, right, strict=True)
                ]
                expected = coefficients(merge(parts, split))
                counts["merge_identities"] += 1
                if reconstructed != expected:
                    raise AssertionError(
                        f"merge recurrence failed: parts={parts}, split={split}"
                    )
                parameter = sum(parts[:split])
                operator_result = [
                    (parameter - index)
                    * (full[index] if index < len(full) else Fraction())
                    + (len(parts) - 1 + index - parameter)
                    * (
                        full[index - 1]
                        if 0 <= index - 1 < len(full)
                        else Fraction()
                    )
                    for index in range(len(left))
                ]
                counts["eulerian_operator_identities"] += 1
                if operator_result != expected:
                    raise AssertionError(
                        f"Eulerian operator failed: parts={parts}, split={split}"
                    )

            for index in range(1, len(left) - 1):
                counts["defects"] += 1
                poly = defect_quadratic(left, right, index)
                if poly[0] > 0:
                    counts["convex"] += 1
                elif poly[0] == 0:
                    counts["linear"] += 1
                else:
                    counts["concave"] += 1

                allowed_value, allowed_at = interval_minimum(poly, lower, upper)
                if allowed_value < 0:
                    counts["allowed_failures"] += 1
                    if first_allowed_failure is None:
                        first_allowed_failure = (
                            parts,
                            index,
                            allowed_at,
                            allowed_value,
                            poly,
                        )

                global_value, global_at = interval_minimum(
                    poly, Fraction(), Fraction(1)
                )
                if global_value < 0:
                    counts["negative_global_minima"] += 1
                    if not lower <= global_at <= upper:
                        counts["negative_global_outside_allowed"] += 1
                    if first_negative_control is None:
                        first_negative_control = (
                            parts,
                            index,
                            global_at,
                            global_value,
                            (lower, upper),
                        )

    for key, value in counts.items():
        print(f"{key.upper()} {value}")
    print(f"FIRST_ALLOWED_FAILURE {first_allowed_failure}")
    print(f"FIRST_NEGATIVE_CONTROL {first_negative_control}")

    if counts["allowed_failures"]:
        raise SystemExit(1)
    if not counts["negative_global_minima"]:
        raise AssertionError("negative control did not distinguish [0,1]")
    if (
        counts["negative_global_minima"]
        != counts["negative_global_outside_allowed"]
    ):
        raise AssertionError("a negative global minimum entered the allowed interval")


if __name__ == "__main__":
    main()
