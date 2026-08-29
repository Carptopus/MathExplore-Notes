"""Verify explicit alternating-net witnesses for 183 of the 190 atoms.

The seven omitted atoms are the labelled profiles with one entry two and six
entries one.  Their dimension-free nonrealizability is a proof obligation, not
something inferred from this finite program.
"""

from itertools import combinations


LINES = (
    (0,1,2), (0,3,4), (0,5,6), (1,3,5),
    (1,4,6), (2,3,6), (2,4,5),
)


def fano_maps():
    result = []
    for first in range(1, 8):
        for second in range(1, 8):
            if second == first:
                continue
            for third in range(1, 8):
                if third in (first, second, first ^ second):
                    continue
                result.append(tuple(
                    ((first if point & 1 else 0)
                     ^ (second if point & 2 else 0)
                     ^ (third if point & 4 else 0))
                    for point in range(1, 8)
                ))
    return tuple(result)


FANO_MAPS = fano_maps()


def orbit(profile):
    return {
        tuple(profile[mapping[point] - 1] for point in range(7))
        for mapping in FANO_MAPS
    }


def rows_from_edge_mask(mask, dimension):
    rows = [0] * dimension
    edge = 0
    for left in range(dimension):
        for right in range(left + 1, dimension):
            if (mask >> edge) & 1:
                rows[left] |= 1 << right
                rows[right] |= 1 << left
            edge += 1
    return tuple(rows)


def alternating_rank(mask, dimension):
    return alternating_rank_rows(rows_from_edge_mask(mask, dimension))


def alternating_rank_rows(source_rows):
    rows = list(source_rows)
    dimension = len(rows)
    rank = 0
    for column in range(dimension):
        pivot = next(
            (row for row in range(rank, dimension) if (rows[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(dimension):
            if row != rank and ((rows[row] >> column) & 1):
                rows[row] ^= rows[rank]
        rank += 1
    return rank


def profile(first, second, third, dimension):
    return tuple(
        alternating_rank(
            (first if point & 1 else 0)
            ^ (second if point & 2 else 0)
            ^ (third if point & 4 else 0),
            dimension,
        ) // 2
        for point in range(1, 8)
    )


def profile_rows(first, second, third):
    dimension = len(first)
    assert len(second) == dimension and len(third) == dimension
    forms = (first, second, third)
    return tuple(
        alternating_rank_rows(tuple(
            (forms[0][row] if point & 1 else 0)
            ^ (forms[1][row] if point & 2 else 0)
            ^ (forms[2][row] if point & 4 else 0)
            for row in range(dimension)
        )) // 2
        for point in range(1, 8)
    )


def rank_four_atoms():
    realized_profiles = set()
    for first in range(64):
        for second in range(64):
            for third in range(64):
                realized_profiles.add(profile(first, second, third, 4))

    line_sets = {frozenset(line) for line in LINES}
    all_points = frozenset(range(7))
    expected = set()
    for line in line_sets:
        expected.add(tuple(0 if point in line else 1 for point in range(7)))
    expected.add((1,) * 7)
    for zero in range(7):
        expected.add(tuple(0 if point == zero else 1 for point in range(7)))
    for mask in range(1, 1 << 7):
        support = frozenset(point for point in range(7) if (mask >> point) & 1)
        if (
            len(support) == 2
            or (
                len(support) == 4
                and all_points.difference(support) not in line_sets
            )
        ):
            expected.add(tuple(2 if point in support else 1 for point in range(7)))
    assert len(expected) == 64
    assert expected.issubset(realized_profiles)
    return expected


def main():
    realized = rank_four_atoms()

    rank_six_witnesses = (
        ((103, 3106, 27570), (1,1,2,2,3,3,2)),
        ((28885, 14727, 19520), (1,2,3,2,3,3,2)),
    )
    for masks, expected in rank_six_witnesses:
        actual = profile(*masks, 6)
        assert actual == expected
        realized.update(orbit(actual))

    rank_eight_masks = (0x216D14E, 0x5AA3A52, 0x6DD3144)
    rank_eight_profile = profile(*rank_eight_masks, 8)
    assert rank_eight_profile == (4,2,2,3,2,4,4)
    realized.update(orbit(rank_eight_profile))

    outside_rows = (
        (0xE74,0xCC0,0x5D9,0x2B4,0xBAD,0x6D9,0x5A7,0x37E,0x6D4,0x1B9,0x967,0x413),
        (0xA8C,0x894,0x203,0x461,0x662,0x458,0x8B8,0x443,0x000,0x015,0x8B8,0x443),
        (0x74E,0x0B9,0xB39,0x527,0xCE6,0x59E,0x091,0x972,0xEAD,0x505,0xB39,0x594),
        (0x3B6,0x4ED,0xCE3,0x3F2,0x129,0x71F,0xD8E,0xE4F,0x879,0x4A9,0xAE6,0x5C4),
    )
    for form in outside_rows:
        assert all(((form[row] >> row) & 1) == 0 for row in range(12))
        assert all(
            ((form[row] >> column) & 1) == ((form[column] >> row) & 1)
            for row in range(12) for column in range(12)
        )
        assert alternating_rank_rows(form) == 6
    assert all(
        outside_rows[0][row] ^ outside_rows[1][row]
        ^ outside_rows[2][row] ^ outside_rows[3][row] == 0
        for row in range(12)
    )
    first = tuple(outside_rows[0][row] ^ outside_rows[1][row] for row in range(12))
    second = tuple(outside_rows[0][row] ^ outside_rows[2][row] for row in range(12))
    offset = outside_rows[0]
    rank_twelve_profile = profile_rows(first, second, offset)
    assert sorted(rank_twelve_profile[:3]) == [5, 5, 6]
    assert rank_twelve_profile[3:] == (3, 3, 3, 3)
    realized.update(orbit(rank_twelve_profile))

    # The target orbit has one direction-six point determined by the two
    # direction-five points, hence exactly 21 labelled profiles.
    target_twelve = set()
    for left, right in combinations(range(1, 8), 2):
        item = [3] * 7
        item[left - 1] = 5
        item[right - 1] = 5
        item[(left ^ right) - 1] = 6
        target_twelve.add(tuple(item))
    assert orbit(rank_twelve_profile) == target_twelve
    assert len(realized) == 183

    missing_singletons = {
        tuple(2 if point == distinguished else 1 for point in range(7))
        for distinguished in range(7)
    }
    assert realized.isdisjoint(missing_singletons)
    print(
        "rank4_atoms=64 rank6_orbits=42+28 rank8_orbit=28 "
        "rank12_orbit=21"
    )
    print("PASS: 183 strengthened-cone Hilbert atoms have exact alternating-net witnesses")
    print("BOUNDARY: seven singleton-jump atoms require the separate Pfaffian obstruction")


if __name__ == "__main__":
    main()
