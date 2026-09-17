"""Exact controls for the path-A generalized gap separator in S17."""

from __future__ import annotations

import argparse
import importlib.util
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
S11_CONTROL = HERE / "verify_unique_path_boundary.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def order(block):
    return 1 + sum(block)


def coefficient(polynomial, degree):
    return polynomial[degree] if degree < len(polynomial) else 0


def profile_two(block):
    return sum(length >= 2 for length in block)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=24)
    args = parser.parse_args()

    s11 = load_module("s11_control", S11_CONTROL)
    s7 = s11.load_module("s7_control", s11.S7_CONTROL)
    probe = s7.load_probe()
    buckets = defaultdict(list)

    for total_order in range(8, args.max_order + 1):
        for raw in probe.descriptions(total_order):
            description = s11.orient_unique_minimum(raw)
            if description is None:
                continue
            alpha, beta, left, middle, right = description
            delta = order(right) - order(left)
            if len(left) != 2 or delta < 2:
                continue
            key = (
                order(left),
                order(middle),
                order(right),
                alpha + beta,
                left,
                tuple(sorted(left + middle + right, reverse=True)),
            )
            buckets[(total_order, key)].append(description)

    checked = 0
    first_coefficient = 0
    second_coefficient = 0
    swapped_degree_case = 0

    for descriptions in buckets.values():
        for first in descriptions:
            alpha, beta, left, middle, right = first
            delta = order(right) - order(left)
            if alpha != delta + 1 or beta < 2:
                continue
            if sorted(right + (1,)) != sorted(left + (delta + 1,)):
                continue

            for second in descriptions:
                alpha_prime, beta_prime, left_prime, middle_prime, right_prime = second
                if (
                    alpha_prime != beta + delta
                    or beta_prime != 1
                    or left_prime != left
                ):
                    continue

                difference = s7.add(
                    s11.path_remainder(s7, first),
                    s7.negate(s11.path_remainder(s7, second)),
                )
                q = len(middle)
                m_prime = len(right_prime)
                c_two = profile_two(right)
                c_two_prime = profile_two(right_prime)
                u_two = profile_two(middle + right)

                expected_two = (2 - m_prime) * (m_prime - q - 1)
                assert coefficient(difference, 2) == expected_two

                if expected_two:
                    first_coefficient += 1
                elif m_prime == 2:
                    expected_three = (q - 1) * (c_two_prime - c_two) - q
                    assert coefficient(difference, 3) == expected_three
                    assert expected_three != 0
                    second_coefficient += 1
                else:
                    assert m_prime == q + 1
                    assert len(middle_prime) == 1
                    expected_three = (
                        (q - 1) * (u_two - c_two - c_two_prime) - 1
                    )
                    assert coefficient(difference, 3) == expected_three
                    if q == 2:
                        # The singleton middle arm in the second layout is the
                        # sum of the two first-layout middle arms.  In the
                        # common four-arm multiset it must therefore be one of
                        # the two right arms, which makes the bracket <= 0.
                        assert u_two - c_two - c_two_prime <= 0
                    assert expected_three != 0
                    swapped_degree_case += 1

                assert any(difference)
                checked += 1

    assert checked > 0
    print(
        "PASS "
        f"generalized_gap_pairs={checked} "
        f"x2_separated={first_coefficient} "
        f"x3_fixed_degree={second_coefficient} "
        f"x3_swapped_degree={swapped_degree_case}"
    )


if __name__ == "__main__":
    main()
