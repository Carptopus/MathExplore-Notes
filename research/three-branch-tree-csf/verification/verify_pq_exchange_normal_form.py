"""Bounded control for the S6 P/Q exchange normal form."""

from __future__ import annotations

import argparse
import importlib.util
from collections import Counter, defaultdict, deque
from pathlib import Path


PROBE_PATH = Path(__file__).resolve().parent / "probe_three_branch_cut_profiles.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("three_branch_probe", PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PROBE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def path_profile(adjacency):
    counts = [0] * len(adjacency)
    for start in range(len(adjacency)):
        distances = [-1] * len(adjacency)
        distances[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour, _ in adjacency[current]:
                if distances[neighbour] < 0:
                    distances[neighbour] = distances[current] + 1
                    queue.append(neighbour)
        for finish in range(start + 1, len(adjacency)):
            counts[distances[finish]] += 1
    return tuple(counts)


def subtract(first: Counter, second: Counter):
    result = first.copy()
    result.subtract(second)
    return result if all(value >= 0 for value in result.values()) else None


def exchange_holds(first, second):
    alpha, _, left, middle, right = first
    _, _, other_left, other_middle, other_right = second
    if left != other_left:
        return False

    base_middle = Counter({alpha: len(left) - 1})
    base_right = Counter(alpha + length for length in left)
    p = subtract(Counter(middle), base_middle)
    q = subtract(Counter(right), base_right)
    if p is None or q is None:
        return False
    expected_middle = base_middle + q
    expected_right = base_right + p
    return (
        Counter(other_middle) == expected_middle
        and Counter(other_right) == expected_right
        and sum(p.elements()) == sum(q.elements())
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=18)
    args = parser.parse_args()
    probe = load_probe()

    collision_pairs = 0
    cases = 0
    for order in range(8, args.max_order + 1):
        buckets = defaultdict(list)
        for description in probe.descriptions(order):
            alpha, beta, left, middle, right = description
            left_order = 1 + sum(left)
            middle_order = 1 + sum(middle)
            right_order = 1 + sum(right)
            left_middle_order = left_order + middle_order + alpha - 1
            if not (
                left_order < right_order
                and alpha < right_order - left_order
                and left_middle_order == right_order
            ):
                continue
            adjacency, _ = probe.tree(description)
            key = (
                alpha,
                left,
                tuple(sorted(middle + right, reverse=True)),
                path_profile(adjacency),
            )
            buckets[key].append(description)
            cases += 1

        for values in buckets.values():
            for first_index, first in enumerate(values):
                for second in values[first_index + 1 :]:
                    if not (
                        exchange_holds(first, second)
                        or exchange_holds(second, first)
                    ):
                        raise AssertionError((first, second))
                    collision_pairs += 1
        print(f"n={order}: PASS")

    print(
        f"PASS cases={cases} classified_collision_pairs={collision_pairs}"
    )


if __name__ == "__main__":
    main()
