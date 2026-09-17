"""Exact bounded controls for the S16 event and fixed-layout closures.

The controls independently check the next-event power-sum identity and the
fixed-layout path factorization.  They are regression guards, not evidence for
the unbounded theorem.
"""

from __future__ import annotations

import argparse
import importlib.util
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
S4_CONTROL = HERE / "verify_first_event_dichotomy.py"
S11_CONTROL = HERE / "verify_unique_path_boundary.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def next_event_check(max_order):
    s4 = load_module("s4_for_s16", S4_CONTROL)
    control = s4.load_control()
    probe = control.load_probe()
    checked = 0

    for order in range(9, max_order + 1):
        for description in probe.descriptions(order):
            alpha, beta, left, middle, right = description
            left_order = 1 + sum(left)
            right_order = 1 + sum(right)
            if not (
                len(left) >= 3
                and len(right) == 2
                and left_order < right_order < left_order + alpha
            ):
                continue

            complement_order = right_order + 1
            adjacency, edges = probe.tree(description)
            alternating = control.power_sum_expansion(
                adjacency, range(len(edges)), range(alpha + beta)
            )
            pruning = s4.pruning_product(
                control,
                middle + right,
                complement_order - left_order,
            )
            prediction = {}
            for extension in range(
                complement_order - left_order + 1
            ):
                arms = left if extension == 0 else left + (extension,)
                control.add_scaled(
                    prediction,
                    s4.multiply(
                        s4.spider_expansion(control, arms),
                        pruning[
                            complement_order - left_order - extension
                        ],
                    ),
                    1,
                )

            actual = s4.normalized_derivative(
                control, alternating, order - complement_order
            )
            difference = s4.subtract(control, actual, prediction)

            expected = {}
            twig_count = len(left) + len(middle) + len(right)
            control.add_scaled(
                expected,
                s4.multiply(
                    {(1,): twig_count - 2},
                    s4.spider_expansion(control, right),
                ),
                1,
            )
            if beta >= 2:
                control.add_scaled(
                    expected,
                    s4.spider_expansion(control, right + (1,)),
                    1,
                )
            if complement_order == left_order + alpha:
                control.add_scaled(
                    expected,
                    s4.spider_expansion(control, left + (alpha,)),
                    -1,
                )
            if difference != expected:
                raise AssertionError((description, difference, expected))
            checked += 1
    return checked


def path_factor_check(max_order):
    s11 = load_module("s11_for_s16", S11_CONTROL)
    s7 = s11.load_module("s7_for_s16", s11.S7_CONTROL)
    probe = s7.load_probe()
    buckets = defaultdict(list)
    descriptions = 0

    for order in range(9, max_order + 1):
        for raw in probe.descriptions(order):
            alpha, beta, left, middle, right = raw
            left_order = 1 + sum(left)
            middle_order = 1 + sum(middle)
            right_order = 1 + sum(right)
            d_order = left_order + middle_order + alpha - 1
            if not (
                len(left) >= 2
                and len(right) == 2
                and left_order < right_order < d_order
            ):
                continue
            key = (
                order,
                alpha,
                beta,
                tuple(sorted(left)),
                1 + sum(middle),
                right_order,
                tuple(sorted(middle + right)),
            )
            buckets[key].append(raw)
            descriptions += 1

    checked_pairs = 0
    separated_pairs = 0
    for candidates in buckets.values():
        for first_index, first in enumerate(candidates):
            for second in candidates[first_index + 1 :]:
                alpha, beta, left, middle, right = first
                _, _, _, middle2, right2 = second
                if right == right2 and middle == middle2:
                    continue

                left_poly = s11.arm_sum(s7, left)
                union_poly = s11.arm_sum(s7, middle + right)
                right_poly = s11.arm_sum(s7, right)
                right_poly2 = s11.arm_sum(s7, right2)
                bracket = s7.add(
                    s7.multiply(s7.monomial(alpha), left_poly),
                    s7.arm(alpha),
                    union_poly,
                    s7.negate(right_poly),
                    s7.negate(right_poly2),
                )
                expected = s7.multiply(
                    s7.add(right_poly, s7.negate(right_poly2)),
                    s7.multiply(
                        s7.add(s7.monomial(beta), (-1,)), bracket
                    ),
                )
                actual = s7.add(
                    s11.path_remainder(s7, first),
                    s7.negate(s11.path_remainder(s7, second)),
                )
                if actual != expected:
                    raise AssertionError((first, second, actual, expected))
                if not any(actual):
                    raise AssertionError(("path collision", first, second))
                checked_pairs += 1
                separated_pairs += 1

    return descriptions, checked_pairs, separated_pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-event-order", type=int, default=15)
    parser.add_argument("--max-path-order", type=int, default=19)
    args = parser.parse_args()
    event_cases = next_event_check(args.max_event_order)
    descriptions, path_pairs, separated = path_factor_check(
        args.max_path_order
    )
    print(
        "PASS "
        f"next_event_cases={event_cases} "
        f"path_descriptions={descriptions} "
        f"path_pairs={path_pairs} "
        f"path_separated={separated}"
    )


if __name__ == "__main__":
    main()
