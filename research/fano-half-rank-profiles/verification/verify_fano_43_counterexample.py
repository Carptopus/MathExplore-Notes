"""Exact certificate refuting the candidate Fano 4:3 half-rank inequality."""

from __future__ import annotations


ROWS = {
    "A": (0x7, 0x7, 0x7, 0x5),
    "B": (0xE, 0xF, 0xF, 0x0),
    "C": (0x4, 0x8, 0xC, 0x8),
    "D": (0xD, 0x0, 0x4, 0xD),
}

DOUBLE_LINE_ROWS = {
    "A": (0x1, 0x2, 0x0, 0x0),
    "B": (0x0, 0x0, 0x8, 0x4),
    "C": (0x7, 0x9, 0xE, 0x9),
    "D": (0x6, 0xB, 0x6, 0xD),
}

TRIPLE_LINE_ROWS = {
    "A": (0x01, 0x02, 0x04, 0x00, 0x00, 0x00),
    "B": (0x0B, 0x00, 0x2C, 0x3C, 0x2C, 0x1B),
    "C": (0x20, 0x39, 0x39, 0x2D, 0x19, 0x20),
    "D": (0x2A, 0x3B, 0x11, 0x11, 0x35, 0x3B),
}


def gf2_rank(rows: tuple[int, ...], width: int) -> int:
    work = list(rows)
    rank = 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(work)) if (work[index] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for index in range(len(work)):
            if index != rank and ((work[index] >> column) & 1):
                work[index] ^= work[rank]
        rank += 1
    return rank


def xor_rows(*matrices: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a ^ b ^ c for a, b, c in zip(*matrices)) if len(matrices) == 3 else tuple(
        a ^ b for a, b in zip(*matrices)
    )


def alternating_doubling(rows: tuple[int, ...]) -> tuple[int, ...]:
    """Return [[0,M],[M^T,0]] as bit-packed rows."""
    dimension = len(rows)
    top = tuple(row << dimension for row in rows)
    bottom = tuple(
        sum(((rows[i] >> j) & 1) << i for i in range(dimension))
        for j in range(dimension)
    )
    return top + bottom


def add(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a ^ b for a, b in zip(x, y))


def quadratic_value(polar_rows: tuple[int, ...], vector: int) -> int:
    value = 0
    dimension = len(polar_rows)
    for i in range(dimension):
        if not ((vector >> i) & 1):
            continue
        for j in range(i + 1, dimension):
            value ^= ((polar_rows[i] >> j) & 1) & ((vector >> j) & 1)
    return value


def main() -> None:
    assert xor_rows(ROWS["A"], ROWS["B"], ROWS["C"]) == ROWS["D"]
    point_ranks = tuple(gf2_rank(ROWS[name], 4) for name in "ABCD")
    direction_ranks = (
        gf2_rank(add(ROWS["A"], ROWS["B"]), 4),
        gf2_rank(add(ROWS["A"], ROWS["C"]), 4),
        gf2_rank(add(ROWS["B"], ROWS["C"]), 4),
    )
    assert point_ranks == (2, 2, 2, 2)
    assert direction_ranks == (3, 4, 4)

    doubled = {name: alternating_doubling(rows) for name, rows in ROWS.items()}
    for matrix in doubled.values():
        assert all(((matrix[i] >> i) & 1) == 0 for i in range(8))
        assert all(
            ((matrix[i] >> j) & 1) == ((matrix[j] >> i) & 1)
            for i in range(8)
            for j in range(8)
        )
    assert add(add(doubled["A"], doubled["B"]), doubled["C"]) == doubled["D"]
    assert tuple(gf2_rank(doubled[name], 8) for name in "ABCD") == (4, 4, 4, 4)

    u = add(doubled["A"], doubled["B"])
    v = add(doubled["A"], doubled["C"])
    z = doubled["A"]
    forms = (u, v, add(u, v), z, add(z, u), add(z, v), add(add(z, u), v))
    half_rank_profile = tuple(gf2_rank(form, 8) // 2 for form in forms)
    assert half_rank_profile == (3, 4, 4, 2, 2, 2, 2)
    assert 4 * sum(half_rank_profile[3:]) < 3 * sum(half_rank_profile[:3])

    histogram = [0] * 8
    for x in range(1 << 8):
        output = (
            quadratic_value(u, x)
            | (quadratic_value(v, x) << 1)
            | (quadratic_value(z, x) << 2)
        )
        histogram[output] += 1
    assert sum(histogram) == 256
    assert histogram[0] < 256

    print(f"point_ranks={point_ranks}")
    print(f"direction_ranks={direction_ranks}")
    print(f"half_rank_profile={half_rank_profile}")
    print(f"candidate_margin={4 * sum(half_rank_profile[3:]) - 3 * sum(half_rank_profile[:3])}")
    print(f"histogram={tuple(histogram)} support={256 - histogram[0]}")

    assert xor_rows(
        DOUBLE_LINE_ROWS["A"], DOUBLE_LINE_ROWS["B"], DOUBLE_LINE_ROWS["C"]
    ) == DOUBLE_LINE_ROWS["D"]
    assert tuple(gf2_rank(DOUBLE_LINE_ROWS[name], 4) for name in "ABCD") == (2, 2, 2, 2)
    assert (
        gf2_rank(add(DOUBLE_LINE_ROWS["A"], DOUBLE_LINE_ROWS["B"]), 4),
        gf2_rank(add(DOUBLE_LINE_ROWS["A"], DOUBLE_LINE_ROWS["C"]), 4),
        gf2_rank(add(DOUBLE_LINE_ROWS["B"], DOUBLE_LINE_ROWS["C"]), 4),
    ) == (4, 4, 4)
    doubled_line = {
        name: alternating_doubling(rows) for name, rows in DOUBLE_LINE_ROWS.items()
    }
    line_u = add(doubled_line["A"], doubled_line["B"])
    line_v = add(doubled_line["A"], doubled_line["C"])
    line_z = doubled_line["A"]
    double_line_profile = tuple(
        gf2_rank(form, 8) // 2
        for form in (
            line_u, line_v, add(line_u, line_v), line_z,
            add(line_z, line_u), add(line_z, line_v), add(add(line_z, line_u), line_v),
        )
    )
    assert double_line_profile == (4, 4, 4, 2, 2, 2, 2)
    print(f"double_line_profile={double_line_profile}")

    assert xor_rows(
        TRIPLE_LINE_ROWS["A"], TRIPLE_LINE_ROWS["B"], TRIPLE_LINE_ROWS["C"]
    ) == TRIPLE_LINE_ROWS["D"]
    assert tuple(gf2_rank(TRIPLE_LINE_ROWS[name], 6) for name in "ABCD") == (3, 3, 3, 3)
    assert (
        gf2_rank(add(TRIPLE_LINE_ROWS["A"], TRIPLE_LINE_ROWS["B"]), 6),
        gf2_rank(add(TRIPLE_LINE_ROWS["A"], TRIPLE_LINE_ROWS["C"]), 6),
        gf2_rank(add(TRIPLE_LINE_ROWS["B"], TRIPLE_LINE_ROWS["C"]), 6),
    ) == (6, 6, 6)
    tripled_line = {
        name: alternating_doubling(rows) for name, rows in TRIPLE_LINE_ROWS.items()
    }
    triple_u = add(tripled_line["A"], tripled_line["B"])
    triple_v = add(tripled_line["A"], tripled_line["C"])
    triple_z = tripled_line["A"]
    triple_line_profile = tuple(
        gf2_rank(form, 12) // 2
        for form in (
            triple_u, triple_v, add(triple_u, triple_v), triple_z,
            add(triple_z, triple_u), add(triple_z, triple_v),
            add(add(triple_z, triple_u), triple_v),
        )
    )
    assert triple_line_profile == (6, 6, 6, 3, 3, 3, 3)
    print(f"triple_line_profile={triple_line_profile}")
    print("PASS: explicit 4:3 counterexample and twice/triple-line-ray witnesses")


if __name__ == "__main__":
    main()
