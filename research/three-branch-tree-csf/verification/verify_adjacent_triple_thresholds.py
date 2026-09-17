"""Exact controls for the S10 adjacent-triple endpoint thresholds."""

from __future__ import annotations

import argparse
import importlib.util
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
S4_CONTROL = HERE / "verify_first_event_dichotomy.py"


def load_control():
    spec = importlib.util.spec_from_file_location("s4_control", S4_CONTROL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {S4_CONTROL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add(control, first, second):
    result = dict(first)
    control.add_scaled(result, second, 1)
    return result


def inverse_times(control, s4, arms, expansion, degree):
    pruning = s4.pruning_product(control, arms, degree)
    result = [dict(expansion)]
    for current_degree in range(1, degree + 1):
        coefficient = {}
        for pruning_degree in range(1, current_degree + 1):
            control.add_scaled(
                coefficient,
                s4.multiply(
                    pruning[pruning_degree],
                    result[current_degree - pruning_degree],
                ),
                -1,
            )
        result.append(coefficient)
    return result


def signature(expansion):
    return tuple(sorted(expansion.items()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=16)
    args = parser.parse_args()

    s4 = load_control()
    control = s4.load_control()
    probe = control.load_probe()
    checked = 0
    buckets = defaultdict(list)

    for order in range(8, args.max_order + 1):
        for description in probe.descriptions(order):
            alpha, beta, left, middle, right = description
            if alpha != 1 or beta != 1 or sum(left) != sum(right):
                continue
            endpoint_order = 1 + sum(left)
            middle_order = 1 + sum(middle)
            degree = min(endpoint_order - 2, middle_order - 1)
            left_expansion = s4.spider_expansion(control, left)
            right_expansion = s4.spider_expansion(control, right)
            endpoint_sum = add(control, left_expansion, right_expansion)
            left_series = inverse_times(
                control, s4, left, left_expansion, degree
            )
            right_series = inverse_times(
                control, s4, right, right_expansion, degree
            )
            combined_series = [
                add(control, left_series[index], right_series[index])
                for index in range(degree + 1)
            ]

            for index in range(1, degree + 1):
                partition = tuple(sorted((endpoint_order, index), reverse=True))
                observed = combined_series[index].get(partition, 0)
                threshold = sum(length >= index for length in left + right)
                expected = (-1) ** (endpoint_order + index - 1) * threshold
                assert observed == expected, (description, index, observed, expected)

            key = (
                endpoint_order,
                tuple(sorted(left + middle + right, reverse=True)),
                signature(endpoint_sum),
                tuple(signature(value) for value in combined_series[1:]),
            )
            buckets[(order, key)].append(description)
            checked += 1

    collisions = [values for values in buckets.values() if len(values) > 1]
    assert not collisions, collisions[:1]
    print(f"PASS checked_descriptions={checked} recovery_collisions=0")


if __name__ == "__main__":
    main()
