"""Exact controls for the S12 scalar trunk-profile classification."""

from __future__ import annotations

import argparse
import importlib.util
from collections import Counter, defaultdict
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


def scalar_profile(a, b, c, alpha, beta):
    d = a + b + alpha - 1
    e = b + c + beta - 1
    counts = Counter()
    for lower, upper in (
        (a, a + alpha - 1),
        (c, c + beta - 1),
        (d, d + beta - 1),
        (e, e + alpha - 1),
    ):
        for value in range(lower, upper + 1):
            counts[value] += 1
    return tuple(sorted(counts.items()))


def is_allowed_exchange(first, second):
    a, b, c, alpha, beta = first
    a2, b2, c2, alpha2, beta2 = second
    if a != a2:
        return False
    gap_exchange = (
        b2 == b
        and c2 == c == a + 1
        and alpha2 == beta + 1
        and beta2 == alpha - 1
    )
    cd_exchange = (
        alpha == alpha2 == 1
        and beta2 == beta
        and b2 == c - a
        and c2 == a + b
    )
    return gap_exchange or cd_exchange


def scalar_check(max_order):
    buckets = defaultdict(list)
    checked = 0
    for order in range(8, max_order + 1):
        for a in range(3, order):
            for b in range(2, order):
                for c in range(a + 1, order):
                    remainder = order + 2 - a - b - c
                    for alpha in range(1, remainder):
                        beta = remainder - alpha
                        if beta < 1 or not (alpha == 1 or c == a + 1):
                            continue
                        description = (a, b, c, alpha, beta)
                        key = (
                            order,
                            a,
                            alpha + beta,
                            scalar_profile(*description),
                        )
                        buckets[key].append(description)
                        checked += 1

    collisions = 0
    for descriptions in buckets.values():
        assert len(descriptions) <= 2, descriptions
        if len(descriptions) == 2:
            first, second = descriptions
            if not is_allowed_exchange(first, second):
                assert is_allowed_exchange(second, first), descriptions
            collisions += 1
    return checked, collisions


def tree_check(max_order):
    s11 = load_module("s11_control", S11_CONTROL)
    s7 = s11.load_module("s7_for_s12", s11.S7_CONTROL)
    probe = s7.load_probe()
    buckets = defaultdict(list)
    checked = 0

    for order in range(8, max_order + 1):
        for raw in probe.descriptions(order):
            description = s11.orient_unique_minimum(raw)
            if description is None:
                continue
            alpha, beta, left, middle, right = description
            a = 1 + sum(left)
            b = 1 + sum(middle)
            c = 1 + sum(right)
            if len(left) != 2 or not (alpha == 1 or c == a + 1):
                continue
            degree_profile = tuple(
                sorted((len(left) + 1, len(middle) + 2, len(right) + 1))
            )
            key = (
                order,
                a,
                alpha + beta,
                tuple(sorted(left + middle + right, reverse=True)),
                degree_profile,
                scalar_profile(a, b, c, alpha, beta),
                s11.path_remainder(s7, description),
                s11.three_leaf_formula(s7, description),
                s11.four_leaf_five_edge_formula(description, probe),
            )
            buckets[key].append(description)
            checked += 1

    collisions = [values for values in buckets.values() if len(values) > 1]
    assert not collisions, collisions[:1]
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-scalar-order", type=int, default=80)
    parser.add_argument("--max-tree-order", type=int, default=19)
    args = parser.parse_args()
    scalar_descriptions, scalar_collisions = scalar_check(args.max_scalar_order)
    tree_descriptions = tree_check(args.max_tree_order)
    print(
        "PASS "
        f"scalar_descriptions={scalar_descriptions} "
        f"classified_scalar_collisions={scalar_collisions} "
        f"tree_descriptions={tree_descriptions} "
        "cross_layout_collisions=0"
    )


if __name__ == "__main__":
    main()

