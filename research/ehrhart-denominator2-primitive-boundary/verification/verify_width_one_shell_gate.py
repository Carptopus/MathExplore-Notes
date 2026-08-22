from __future__ import annotations

from math import gcd
from analyze_realizability_spectrum import (
    missing_color_count,
    missing_color_points,
)
from verify_next_boundary_reduction import (
    admissible_parameters,
    convex_hull,
    pick_invariants,
)


def normalized_area(triangle: list[tuple[int, int]]) -> int:
    anchor, first, second = triangle
    return abs(
        (first[0] - anchor[0]) * (second[1] - anchor[1])
        - (first[1] - anchor[1]) * (second[0] - anchor[0])
    )


def boundary_count(triangle: list[tuple[int, int]]) -> int:
    return sum(
        gcd(
            abs(triangle[(index + 1) % 3][0] - triangle[index][0]),
            abs(triangle[(index + 1) % 3][1] - triangle[index][1]),
        )
        for index in range(3)
    )


def lattice_points_in_triangle(
    triangle: list[tuple[int, int]], *, strict: bool
) -> set[tuple[int, int]]:
    def cross(
        first: tuple[int, int],
        second: tuple[int, int],
        point: tuple[int, int],
    ) -> int:
        return (second[0] - first[0]) * (point[1] - first[1]) - (
            second[1] - first[1]
        ) * (point[0] - first[0])

    result: set[tuple[int, int]] = set()
    minimum_x = min(point[0] for point in triangle)
    maximum_x = max(point[0] for point in triangle)
    minimum_y = min(point[1] for point in triangle)
    maximum_y = max(point[1] for point in triangle)
    threshold = 1 if strict else 0
    for x in range(minimum_x, maximum_x + 1):
        for y in range(minimum_y, maximum_y + 1):
            point = (x, y)
            if all(
                cross(triangle[index], triangle[(index + 1) % 3], point)
                >= threshold
                for index in range(3)
            ):
                result.add(point)
    return result


def verify_no_bounded_width_one_target(maximum_n: int) -> None:
    target_hits: list[tuple[int, int, int, int, int]] = []
    for count in range(3, maximum_n + 1):
        determinant = 6 * count - 3
        for parameter in admissible_parameters(determinant):
            if missing_color_count(determinant, parameter) != count:
                continue
            lifted = missing_color_points(determinant, parameter)
            lattice_points = [
                ((x - 1) // 2, (y - 1) // 2) for x, y in lifted
            ]
            hull = convex_hull(lattice_points)
            if len(hull) < 3:
                continue
            area, boundary, interior = pick_invariants(hull)
            target_hits.append((count, parameter, area, boundary, interior))

    assert target_hits == [(10, 8, 9, 9, 1), (10, 50, 9, 9, 1)]


def verify_sharp_family(maximum_k: int) -> None:
    for k in range(1, maximum_k + 1):
        triangle = [(-2, -1), (8 * k + 9, 3), (-1, 2)]
        count = 4 * k + 5
        determinant = 24 * k + 29

        assert normalized_area(triangle) == determinant == 6 * count - 1
        assert boundary_count(triangle) == 3
        assert {(x % 2, y % 2) for x, y in triangle} == {
            (0, 1),
            (1, 1),
            (1, 0),
        }

        interior = lattice_points_in_triangle(triangle, strict=True)
        even_even = {
            point for point in interior if point[0] % 2 == point[1] % 2 == 0
        }
        shell = convex_hull(sorted(even_even))
        shell_points = lattice_points_in_triangle(
            [shell[0], shell[1], shell[2]], strict=False
        ) if len(shell) == 3 else None

        assert len(interior) == 3 * count - 1
        assert len(even_even) == count
        assert shell == [(0, 0), (2 * k, 0), (6 * k + 6, 2), (0, 2)]

        # The exact trapezoid lattice set is easier to state directly than by
        # triangulating a quadrilateral through an arbitrary diagonal.
        expected_shell_points = {
            (x, y)
            for y, right in ((0, 2 * k), (1, 4 * k + 3), (2, 6 * k + 6))
            for x in range(0, right + 1)
        }
        assert expected_shell_points <= interior
        assert interior - expected_shell_points == {(-1, 0), (-1, 1)}
        assert shell_points is None


def verify_outer_vertex_formula() -> None:
    for half_length in range(1, 101):
        for horizontal_offset in range(-20, 21):
            incoming = (horizontal_offset, -1)
            outgoing = (2 * half_length - horizontal_offset, 1)
            determinant = (
                incoming[0] * outgoing[1]
                - incoming[1] * outgoing[0]
            )
            difference = (
                outgoing[0] - incoming[0],
                outgoing[1] - incoming[1],
            )
            integral = all(coordinate % determinant == 0 for coordinate in difference)
            assert integral == (half_length == 1)


def main() -> None:
    verify_no_bounded_width_one_target(maximum_n=200)
    verify_sharp_family(maximum_k=100)
    verify_outer_vertex_formula()
    print("PASS target calibration N=3..200 leaves only the N=10 one-interior hull")
    print("PASS sharp family k=1..100 has (0,N,3,3N-1), N=4k+5")
    print("PASS one-edge outer-hull integrality forces lattice base length 2")
    print("NOTE bounded checks calibrate but do not prove the candidate shell lemma")


if __name__ == "__main__":
    main()
