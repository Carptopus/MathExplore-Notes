"""Verify the finite polar-net orbit certificates used for n=5 and n=6.

This script does not prove the general nonexistence statements.  It verifies
only the explicitly stated affine-orbit support sets and their slice sumsets.
"""

from __future__ import annotations

from itertools import combinations_with_replacement


QuadraticTerms = list[tuple[int, int]]


def truth_mask(
    n: int, quadratic_terms: QuadraticTerms, affine_mask: int = 0, constant: int = 0
) -> int:
    result = 0
    for x in range(1 << n):
        value = constant
        for i, j in quadratic_terms:
            value ^= ((x >> i) & 1) & ((x >> j) & 1)
        value ^= (x & affine_mask).bit_count() & 1
        result |= value << x
    return result


def affine_orbit_supports(n: int, polar_net: list[QuadraticTerms]) -> set[int]:
    component_masks: list[list[int]] = []
    for quadratic_terms in polar_net:
        component_masks.append(
            [
                truth_mask(n, quadratic_terms, affine_mask, constant)
                for constant in range(2)
                for affine_mask in range(1 << n)
            ]
        )

    supports: set[int] = set()
    for first in component_masks[0]:
        for second in component_masks[1]:
            partial_union = first | second
            for third in component_masks[2]:
                supports.add((partial_union | third).bit_count())
    return supports


def sumset(values: set[int]) -> set[int]:
    return {left + right for left in values for right in values}


def assert_independent_polar_components(
    n: int, polar_net: list[QuadraticTerms]
) -> None:
    """Check independence of the three quadratic homogeneous parts."""
    pair_positions = {
        pair: index for index, pair in enumerate(combinations_with_replacement(range(n), 2))
        if pair[0] < pair[1]
    }
    vectors = []
    for terms in polar_net:
        vector = 0
        for pair in terms:
            vector ^= 1 << pair_positions[tuple(sorted(pair))]
        vectors.append(vector)
    assert len(vectors) == 3
    assert all(vectors)
    assert len(set(vectors)) == 3
    assert vectors[0] ^ vectors[1] ^ vectors[2]


def rm2_nonzero_weights(n: int) -> set[int]:
    weights = {1 << (n - 1), 1 << n}
    for half_rank in range(1, n // 2 + 1):
        deviation = 1 << (n - half_rank - 1)
        weights.add((1 << (n - 1)) - deviation)
        weights.add((1 << (n - 1)) + deviation)
    return weights


def arithmetic_candidates(n: int) -> set[int]:
    minimum = 7 * (1 << (n - 4))
    half = 1 << (n - 1)
    length = 1 << n
    return {
        sum(weights) // 4
        for weights in combinations_with_replacement(rm2_nonzero_weights(n), 7)
        if sum(weights) % 4 == 0
        and sum(weights) // 4 <= length
        and (sum(weights) // 4 == minimum or sum(weights) // 4 >= half)
    }


def main() -> None:
    net4 = [
        [(0, 1), (0, 3), (1, 2)],
        [(0, 1)],
        [(0, 1), (0, 3)],
    ]
    expected4 = set(range(8, 17))

    net5 = [
        [(0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)],
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)],
        [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
    ]
    expected5 = {17, *range(19, 33)}

    net7 = [
        [(0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)],
        [
            (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4),
            (6, 0), (6, 1), (6, 2), (6, 3),
        ],
        [
            (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4),
            (5, 1), (5, 2), (5, 3), (5, 4), (6, 0), (6, 1), (6, 5),
        ],
    ]
    expected_orbit7 = {78, 82, 86, *range(88, 126, 2), 128}

    orbit4 = affine_orbit_supports(4, net4)
    orbit5 = affine_orbit_supports(5, net5)
    orbit7 = affine_orbit_supports(7, net7)

    assert_independent_polar_components(4, net4)
    assert_independent_polar_components(5, net5)
    assert_independent_polar_components(7, net7)

    assert orbit4 == expected4, (sorted(orbit4), sorted(expected4))
    assert orbit5 == expected5, (sorted(orbit5), sorted(expected5))
    assert orbit7 == expected_orbit7, (sorted(orbit7), sorted(expected_orbit7))
    assert sumset(orbit4) == set(range(16, 33))
    assert sumset(orbit5) == {34, *range(36, 65)}

    spectrum6 = {28, 32, 34, *range(36, 65)}
    constructed7 = {2 * value for value in spectrum6}
    expected7 = {56, 64, 68, *range(72, 129, 2)}
    assert constructed7 == expected7
    assert rm2_nonzero_weights(7) == {32, 48, 56, 64, 72, 80, 96, 128}

    lifted8 = {2 * value for value in expected7}
    constructed8 = lifted8 | sumset(orbit7)
    assert set(range(166, 253, 2)) <= constructed8
    assert 254 not in constructed8
    expected8 = {
        112, 128, 136, 144, 148, 152, 156, 160, 164,
        *range(166, 253, 2),
        256,
    }
    assert constructed8 == expected8

    expected9 = {2 * value for value in expected8}
    candidate_gap9 = arithmetic_candidates(9) - expected9
    assert candidate_gap9 == {
        260, 264, 268, 276, 280, 284, 292, 300, 308, 316, 324, 508
    }

    # Negative control: deleting one quadratic term changes the first certificate.
    damaged_net4 = [net4[0][:-1], net4[1], net4[2]]
    assert affine_orbit_supports(4, damaged_net4) != expected4
    damaged_net5 = [net5[0][:-1], net5[1], net5[2]]
    assert affine_orbit_supports(5, damaged_net5) != expected5
    damaged_net7 = [net7[0], net7[1], net7[2][:-1]]
    assert affine_orbit_supports(7, damaged_net7) != expected_orbit7

    print("PASS: n=5--n=9 finite slice-orbit and arithmetic certificates verified")


if __name__ == "__main__":
    main()
