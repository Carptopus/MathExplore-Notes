"""Exact bounded controls for the S14 gap-exchange closure.

The script is a regression guard for the formulas and the exceptional
two-pair/one-triple allocation lemma.  It is not used as evidence for the
unbounded theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
S11_CONTROL = HERE / "verify_unique_path_boundary.py"
S12_CONTROL = HERE / "verify_scalar_profile_merge.py"
EVENT_CONTROL = HERE / "verify_equal_endpoint_extension.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def partitions_exact(total, parts, ceiling=None, current=()):
    if parts == 0:
        if total == 0:
            yield current
        return
    if total < parts:
        return
    ceiling = min(total - parts + 1, ceiling or total)
    for part in range(ceiling, 0, -1):
        yield from partitions_exact(
            total - part, parts - 1, part, current + (part,)
        )


def threshold(arms, level):
    return sum(length >= level for length in arms)


def coefficient(polynomial, degree):
    return polynomial[degree] if degree < len(polynomial) else 0


def event_signature(event, left, right):
    left_extended = tuple(sorted(left + (1,), reverse=True))
    return event.signature(
        event.add(event.spider_expansion(left_extended), event.spider_expansion(right))
    )


def gap_pair(first, second):
    alpha, beta, left, middle, right = first
    alpha2, beta2, left2, middle2, right2 = second
    return (
        alpha2 == beta + 1
        and beta2 == alpha - 1
        and 1 + sum(left) == 1 + sum(left2)
        and 1 + sum(middle) == 1 + sum(middle2)
        and 1 + sum(right) == 1 + sum(right2) == 2 + sum(left)
    )


def exceptional_allocation_check(max_arm_sum):
    """Check the elementary lemma used when q=2, m=3, b=c."""

    checked_pairs = 0
    for arm_sum in range(4, max_arm_sum + 1):
        buckets = defaultdict(list)
        for left in partitions_exact(arm_sum - 1, 2):
            for middle in partitions_exact(arm_sum, 2):
                for right in partitions_exact(arm_sum, 3):
                    buckets[tuple(sorted(left + middle + right))].append(
                        (left, middle, right)
                    )
        for descriptions in buckets.values():
            for first_index, first in enumerate(descriptions):
                for second in descriptions[first_index + 1 :]:
                    if first == second:
                        continue
                    level = next(
                        level
                        for level in range(2, arm_sum + 1)
                        if tuple(threshold(arms, level) for arms in first)
                        != tuple(threshold(arms, level) for arms in second)
                    )
                    assert threshold(first[0], level) != threshold(
                        second[0], level
                    ), (arm_sum, first, second, level)
                    checked_pairs += 1
    return checked_pairs


def tree_check(max_order):
    s11 = load_module("s11_for_s14", S11_CONTROL)
    s12 = load_module("s12_for_s14", S12_CONTROL)
    event = load_module("event_for_s14", EVENT_CONTROL)
    s7 = s11.load_module("s7_for_s14", s11.S7_CONTROL)
    probe = s7.load_probe()

    buckets = defaultdict(list)
    descriptions_checked = 0
    for order in range(8, max_order + 1):
        for raw in probe.descriptions(order):
            description = s11.orient_unique_minimum(raw)
            if description is None:
                continue
            alpha, beta, left, middle, right = description
            a = 1 + sum(left)
            b = 1 + sum(middle)
            c = 1 + sum(right)
            if len(left) != 2 or c != a + 1 or alpha < 2:
                continue
            key = (
                order,
                a,
                b,
                c,
                alpha + beta,
                tuple(sorted(left + middle + right)),
                tuple(sorted((len(left) + 1, len(middle) + 2, len(right) + 1))),
                s12.scalar_profile(a, b, c, alpha, beta),
                event_signature(event, left, right),
            )
            buckets[key].append(description)
            descriptions_checked += 1

    compared = 0
    same_event_pairs = 0
    for descriptions in buckets.values():
        for first_index, first in enumerate(descriptions):
            for second in descriptions[first_index + 1 :]:
                if gap_pair(first, second):
                    oriented_first, oriented_second = first, second
                elif gap_pair(second, first):
                    oriented_first, oriented_second = second, first
                else:
                    continue
                same_event_pairs += 1
                difference = s7.add(
                    s11.path_remainder(s7, oriented_first),
                    s7.negate(s11.path_remainder(s7, oriented_second)),
                )
                assert any(difference), (oriented_first, oriented_second)
                compared += 1

                alpha, beta, left, middle, right = oriented_first
                alpha2, beta2, left2, middle2, right2 = oriented_second
                r, s = alpha - 1, beta
                if r > s:
                    (
                        r,
                        s,
                        left,
                        middle,
                        right,
                        left2,
                        middle2,
                        right2,
                        difference,
                    ) = (
                        s,
                        r,
                        left2,
                        middle2,
                        right2,
                        left,
                        middle,
                        right,
                        s7.negate(difference),
                    )
                if r == s:
                    continue

                q, m = len(middle), len(right)
                first_level = next(
                    (
                        level
                        for level in range(2, max(max(left + middle + right), max(left2 + middle2 + right2)) + 1)
                        if any(
                            threshold(block, level) != threshold(block2, level)
                            for block, block2 in (
                                (left, left2),
                                (middle, middle2),
                                (right, right2),
                            )
                        )
                    ),
                    None,
                )

                # If all allocations agree, the scalar baseline starts here.
                if first_level is None or first_level >= r + 2:
                    assert coefficient(difference, r + 2) == q * (1 - m)
                    continue

                rho = threshold(left, first_level) - threshold(left2, first_level)
                sigma = threshold(middle, first_level) - threshold(
                    middle2, first_level
                )
                local_w = -(m - 2) * rho + (q - m + 1) * sigma
                if first_level <= r:
                    assert coefficient(difference, first_level + 1) == local_w
                elif first_level == r + 1:
                    assert coefficient(difference, r + 2) == local_w + q * (1 - m)

    return descriptions_checked, same_event_pairs, compared


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=19)
    parser.add_argument("--max-exceptional-arm-sum", type=int, default=30)
    args = parser.parse_args()
    exceptional_pairs = exceptional_allocation_check(args.max_exceptional_arm_sum)
    descriptions, event_pairs, compared = tree_check(args.max_order)
    print(
        "PASS "
        f"descriptions={descriptions} "
        f"event_gap_pairs={event_pairs} "
        f"path_separated={compared} "
        f"exceptional_pairs={exceptional_pairs} "
        f"exceptional_arm_sums_through={args.max_exceptional_arm_sum}"
    )


if __name__ == "__main__":
    main()
