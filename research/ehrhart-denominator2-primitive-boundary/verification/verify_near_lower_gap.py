from __future__ import annotations

import argparse
from math import gcd


def even_lift(d: int, p: int) -> int:
    p %= d
    return p if p % 2 == 0 else p + d


def slice_point(d: int, p: int, y: int) -> tuple[int, int] | None:
    """Find the unique possible lattice point on a horizontal open slice.

    This uses strict integer inequalities for the two triangle edges and does
    not call the residue criterion used by analyze_realizability_spectrum.py.
    """
    p = even_lift(d, p)
    x = (p * y) // d + 1
    if p * y < d * x < d + (p - 1) * y:
        return x, y
    return None


def triangle_points(d: int, p: int) -> list[tuple[int, int]]:
    return [point for y in range(1, d) if (point := slice_point(d, p, y)) is not None]


def missing_points(d: int, p: int) -> list[tuple[int, int]]:
    return [(x, y) for x, y in triangle_points(d, p) if x % 2 == y % 2 == 1]


def collinear(points: list[tuple[int, int]]) -> bool:
    if len(points) <= 2:
        return True
    (x0, y0), (x1, y1) = points[:2]
    return all((x - x0) * (y1 - y0) == (y - y0) * (x1 - x0) for x, y in points[2:])


def admissible(d: int, p: int) -> bool:
    return gcd(p, d) == gcd(p - 1, d) == 1


def verify_inverse_normalization(d: int, p: int, expected_n: int) -> None:
    """Check the parity data for P=(T(D,p)+(1,1))/2."""
    p = even_lift(d, p)
    if p % 2 != 0 or d % 2 != 1 or not admissible(d, p):
        raise AssertionError(("inverse normalization inputs", d, p))

    shifted_vertices = [(1, 1), (2, 1), (p + 1, d + 1)]
    colors = {(x % 2, y % 2) for x, y in shifted_vertices}
    if colors != {(1, 1), (0, 1), (1, 0)}:
        raise AssertionError(("boundary colors", d, p, colors))

    boundary_lengths = [
        gcd(1, 0),
        gcd(abs(p - 1), d),
        gcd(abs(p), d),
    ]
    if boundary_lengths != [1, 1, 1]:
        raise AssertionError(("primitive boundary", d, p, boundary_lengths))

    even_even_interior = sum(
        (x + 1) % 2 == 0 and (y + 1) % 2 == 0
        for x, y in triangle_points(d, p)
    )
    if even_even_interior != expected_n:
        raise AssertionError(("inverse normalization count", d, p, even_even_interior))


def verify_gap(max_d: int) -> tuple[int, int]:
    checked = 0
    low_region = 0
    for d in range(3, max_d + 1, 2):
        interior = (d - 1) // 2
        for p in range(d):
            if not admissible(d, p):
                continue
            checked += 1
            points = triangle_points(d, p)
            if len(points) != interior:
                raise AssertionError(("Pick count", d, p, len(points), interior))
            n = sum(x % 2 == y % 2 == 1 for x, y in points)
            if n >= 2 and interior <= 3 * n - 4:
                low_region += 1
                if interior not in {2 * n - 1, 2 * n}:
                    raise AssertionError(("gap theorem", d, p, n, interior))
                if not collinear(points):
                    raise AssertionError(("strip conclusion", d, p, n, interior))
    return checked, low_region


def verify_constructions(max_n: int) -> tuple[int, int]:
    bottom = 0
    boundary = 0
    for n in range(1, max_n + 1):
        for interior in (2 * n - 1, 2 * n):
            d = 2 * interior + 1
            if len(missing_points(d, 2)) != n:
                raise AssertionError(("p=2 construction", n, interior, d))
            verify_inverse_normalization(d, 2, n)
            bottom += 1

        if n % 4 in {2, 3}:
            interior = 3 * n - 3
            d = 2 * interior + 1
            if not admissible(d, 4) or len(missing_points(d, 4)) != n:
                raise AssertionError(("p=4 boundary construction", n, interior, d))
            verify_inverse_normalization(d, 4, n)
            boundary += 1
    return bottom, boundary


def negative_control(max_n: int) -> tuple[int, int, int, int]:
    """The false claim without the sharp boundary exception must fail."""
    for n in range(4, max_n + 1):
        if n % 4 not in {2, 3}:
            continue
        interior = 3 * n - 3
        d = 2 * interior + 1
        if len(missing_points(d, 4)) == n and interior not in {2 * n - 1, 2 * n}:
            return n, interior, d, 4
    raise AssertionError("negative control did not find the p=4 sharp-boundary family")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-d", type=int, default=501)
    parser.add_argument("--max-n", type=int, default=200)
    args = parser.parse_args()

    checked, low_region = verify_gap(args.max_d)
    bottom, boundary = verify_constructions(args.max_n)
    control = negative_control(args.max_n)
    print(f"PASS direct_triangle_instances={checked} low_region_instances={low_region}")
    print(f"PASS bottom_constructions={bottom} boundary_constructions={boundary}")
    print(f"PASS negative_control={control}")


if __name__ == "__main__":
    main()
