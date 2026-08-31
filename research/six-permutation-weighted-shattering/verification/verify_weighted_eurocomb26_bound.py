"""Exact certificate for the weighted EUROCOMB'25 order-26 template."""

from __future__ import annotations

import itertools
from fractions import Fraction


# Table 2 of Cerna--Kielak--Volec, EUROCOMB'25, pp. 247--248.  Their tuple
# notation records the rank map x -> pi(x), not the labels in increasing rank.
RANK_MAPS = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
    [3, 2, 1, 22, 23, 21, 25, 24, 26, 11, 10, 17, 16, 15, 14, 13, 12, 20, 19, 18, 4, 6, 5, 8, 9, 7],
    [19, 20, 18, 22, 21, 23, 9, 8, 7, 14, 17, 12, 16, 10, 13, 11, 15, 2, 1, 3, 5, 4, 6, 26, 25, 24],
    [19, 18, 20, 6, 5, 4, 25, 26, 24, 17, 14, 15, 11, 16, 12, 13, 10, 2, 3, 1, 23, 22, 21, 8, 7, 9],
    [18, 21, 20, 16, 11, 14, 6, 10, 7, 4, 25, 24, 2, 23, 1, 26, 3, 17, 22, 19, 13, 15, 12, 9, 5, 8],
    [21, 18, 19, 11, 16, 13, 9, 5, 8, 25, 4, 1, 23, 3, 26, 2, 24, 22, 17, 20, 15, 12, 14, 6, 10, 7],
]

INTEGER_WEIGHTS = [
    12, 7, 7, 8, 9, 14, 9, 9, 9, 16, 16, 9, 12,
    10, 6, 6, 8, 7, 7, 12, 8, 14, 8, 9, 9, 9,
]


def count_by_rank_maps() -> list[tuple[int, int, int]]:
    good = []
    for triple in itertools.combinations(range(26), 3):
        orders = {
            tuple(sorted(triple, key=lambda x, rank_map=rank_map: rank_map[x]))
            for rank_map in RANK_MAPS
        }
        if len(orders) == 6:
            good.append(triple)
    return good


def count_by_equivalent_order_lists() -> list[tuple[int, int, int]]:
    """Round-trip the rank maps through their equivalent order-list form."""
    order_lists = [
        sorted(range(26), key=lambda x, rank_map=rank_map: rank_map[x])
        for rank_map in RANK_MAPS
    ]
    positions = [
        {label: position for position, label in enumerate(order_list)}
        for order_list in order_lists
    ]
    good = []
    for triple in itertools.combinations(range(26), 3):
        orders = {
            tuple(sorted(triple, key=position.__getitem__))
            for position in positions
        }
        if len(orders) == 6:
            good.append(triple)
    return good


def main() -> None:
    expected = list(range(1, 27))
    assert len(RANK_MAPS) == 6
    assert all(sorted(rank_map) == expected for rank_map in RANK_MAPS)

    rank_map_good = count_by_rank_maps()
    order_list_good = count_by_equivalent_order_lists()
    assert rank_map_good == order_list_good
    assert len(rank_map_good) == 1446

    total = sum(INTEGER_WEIGHTS)
    weights = [Fraction(value, total) for value in INTEGER_WEIGHTS]
    distinct_block_term = 6 * sum(
        weights[a] * weights[b] * weights[c]
        for a, b, c in rank_map_good
    )
    same_block_term = sum(weight**3 for weight in weights)
    density = distinct_block_term / (1 - same_block_term)
    published_uniform_density = Fraction(
        6 * len(rank_map_good), 26 * (26**2 - 1)
    )

    assert total == 250
    assert distinct_block_term == Fraction(773031, 1562500)
    assert same_block_term == Fraction(7387, 3906250)
    assert density == Fraction(1288385, 2599242)
    assert published_uniform_density == Fraction(482, 975)
    assert density - published_uniform_density == Fraction(1113577, 844753650)
    assert density > published_uniform_density

    print(f"template shattered triples: {len(rank_map_good)}/2600")
    print(f"integer weights: {INTEGER_WEIGHTS}; total={total}")
    print(f"A={distinct_block_term}, B={same_block_term}")
    print(f"weighted recursive density={density}={float(density):.12f}")
    print(
        "improvement over 482/975: "
        f"{density - published_uniform_density}="
        f"{float(density - published_uniform_density):.12f}"
    )
    print("exact EUROCOMB'25 weighted certificate passed")


if __name__ == "__main__":
    main()
