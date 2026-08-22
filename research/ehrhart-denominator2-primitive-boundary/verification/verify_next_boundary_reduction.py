from __future__ import annotations

from math import gcd

from analyze_realizability_spectrum import missing_color_count, missing_color_points


def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    def cross(
        origin: tuple[int, int],
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> int:
        return (first[0] - origin[0]) * (second[1] - origin[1]) - (
            first[1] - origin[1]
        ) * (second[0] - origin[0])

    lower: list[tuple[int, int]] = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)

    upper: list[tuple[int, int]] = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def pick_invariants(polygon: list[tuple[int, int]]) -> tuple[int, int, int]:
    area2 = abs(
        sum(
            polygon[index][0] * polygon[(index + 1) % len(polygon)][1]
            - polygon[index][1] * polygon[(index + 1) % len(polygon)][0]
            for index in range(len(polygon))
        )
    )
    boundary = sum(
        gcd(
            abs(polygon[(index + 1) % len(polygon)][0] - polygon[index][0]),
            abs(polygon[(index + 1) % len(polygon)][1] - polygon[index][1]),
        )
        for index in range(len(polygon))
    )
    interior = (area2 - boundary + 2) // 2
    return area2, boundary, interior


def admissible_parameters(determinant: int) -> list[int]:
    return [
        parameter
        for parameter in range(determinant)
        if gcd(parameter, determinant) == gcd(parameter - 1, determinant) == 1
    ]


def main() -> None:
    hits: list[tuple[int, int, list[int]]] = []
    for count in range(3, 11):
        determinant = 6 * count - 3
        witnesses = [
            parameter
            for parameter in admissible_parameters(determinant)
            if missing_color_count(determinant, parameter) == count
        ]
        if witnesses:
            hits.append((count, determinant, witnesses))

    assert hits == [(10, 57, [8, 50])]

    lifted_points = missing_color_points(57, 8)
    lattice_points = [((x - 1) // 2, (y - 1) // 2) for x, y in lifted_points]
    hull = convex_hull(lattice_points)
    assert hull == [(0, 0), (3, 24), (0, 3)]
    assert pick_invariants(hull) == (9, 9, 1)

    # The only line-hull endpoint left by the symbolic height argument is N=3.
    # Its normalized determinant D=15 has no target witness.
    assert all(missing_color_count(15, p) != 3 for p in admissible_parameters(15))

    print("PASS finite_one_interior_branch_hits=[(10,57,[8,50])]")
    print("PASS representative_hull=(area2=9,boundary=9,interior=1)")
    print("PASS line_hull_small_endpoint_N3_absent")


if __name__ == "__main__":
    main()
