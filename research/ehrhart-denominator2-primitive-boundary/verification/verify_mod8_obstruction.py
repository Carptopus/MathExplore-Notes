#!/usr/bin/env python3
"""Independent integer checks for the denominator-2 triangle mod-8 lemma."""

from __future__ import annotations

import argparse
import math
from collections import Counter


def admissible(d: int, p: int) -> bool:
    return (
        d > 0
        and d % 2 == 1
        and p % 2 == 0
        and math.gcd(p, d) == 1
        and math.gcd(p - 1, d) == 1
    )


def n_by_slices(d: int, p: int) -> int:
    """Count odd-odd interior points using horizontal slices."""
    total = 0
    for y in range(1, d, 2):
        q, r = divmod(p * y, d)
        if r > y and q % 2 == 0:
            total += 1
    return total


def n_by_geometry(d: int, p: int) -> int:
    """Directly count odd-odd points using strict edge-side tests."""
    total = 0
    x_min = min(0, 1, p)
    x_max = max(0, 1, p)
    for x in range(x_min, x_max + 1):
        for y in range(1, d):
            if (
                x % 2 == 1
                and y % 2 == 1
                and d * x - p * y > 0
                and (p - 1) * y - d * (x - 1) > 0
            ):
                total += 1
    return total


def fiber_counts(d: int, p: int) -> Counter[int]:
    """Count positive odd triples by the residue of x+p*y modulo d."""
    counts: Counter[int] = Counter()
    for x in range(1, d, 2):
        for y in range(1, d - x, 2):
            z = d - x - y
            if z > 0 and z % 2 == 1:
                counts[(x + p * y) % d] += 1
    return counts


def verify(max_d: int, full_fiber_max_d: int, geometry_max_d: int) -> tuple[int, int, int]:
    slice_cases = 0
    fiber_cases = 0
    geometry_cases = 0
    for d in range(1, max_d + 1, 2):
        target_parity = ((d * d - 1) // 8) % 2
        # With the missing parity color fixed, even p is naturally periodic modulo 2d.
        for p in range(0, 2 * d, 2):
            if not admissible(d, p):
                continue
            n_value = n_by_slices(d, p)
            assert n_value % 2 == target_parity, (d, p, n_value)
            slice_cases += 1

            if d <= geometry_max_d:
                assert n_by_geometry(d, p) == n_value, (d, p, n_value)
                geometry_cases += 1

            if d <= full_fiber_max_d:
                counts = fiber_counts(d, p)
                assert counts[0] == n_value, (d, p, counts[0], n_value)
                assert all(counts[r] == counts[-r % d] for r in range(d)), (
                    d,
                    p,
                    counts,
                )
                assert sum(counts.values()) == (d * d - 1) // 8, (d, p)
                fiber_cases += 1

    # Each omitted primitive-edge condition has a concrete counterexample.
    assert n_by_slices(9, 6) % 2 != ((9 * 9 - 1) // 8) % 2
    assert n_by_slices(9, 4) % 2 != ((9 * 9 - 1) // 8) % 2
    return slice_cases, fiber_cases, geometry_cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-d", type=int, default=499)
    parser.add_argument("--full-fiber-max-d", type=int, default=129)
    parser.add_argument("--geometry-max-d", type=int, default=101)
    args = parser.parse_args()
    slice_cases, fiber_cases, geometry_cases = verify(
        args.max_d,
        args.full_fiber_max_d,
        args.geometry_max_d,
    )
    print(
        "PASS: "
        f"{slice_cases} admissible slice cases; "
        f"{fiber_cases} full fiber-symmetry cases; "
        f"{geometry_cases} direct geometry cases; "
        "2 negative controls."
    )


if __name__ == "__main__":
    main()
