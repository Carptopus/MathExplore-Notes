"""Verify the exact four-core recursion for both rank-two Walsh signs.

This is the two-dimensional analogue of verify_rank4_full_core_recursion.py.
The core has four points, affine masks have size eight, one affine product
gives 12 masks, and two products already give every Boolean function.  A
five-valued relation kernel is retained so the output is filtered to genuine
three-dimensional subcodes.
"""

from __future__ import annotations

from itertools import product


U = tuple(product((0, 1), repeat=2))
FULL = 15


def values(coefficients: int, quadratic: bool) -> int:
    width = 4 if quadratic else 3
    mask = 0
    for point, u in enumerate(U):
        entries = (1, *u, u[0] * u[1])
        value = sum(
            ((coefficients >> index) & 1) * entry
            for index, entry in enumerate(entries[:width])
        ) % 2
        mask |= value << point
    return mask


AFFINE_BY_COEFFICIENT = {
    coefficients: values(coefficients, quadratic=False)
    for coefficients in range(1 << 3)
}
AFFINE = frozenset(AFFINE_BY_COEFFICIENT.values())
ONE_PRODUCT = frozenset(left & right for left in AFFINE for right in AFFINE)
TWO_PRODUCTS = frozenset(left ^ right for left in ONE_PRODUCT for right in ONE_PRODUCT)
QUADRATIC_BY_COEFFICIENT = {
    coefficients: values(coefficients, quadratic=True)
    for coefficients in range(1 << 4)
}
QUADRATIC = frozenset(QUADRATIC_BY_COEFFICIENT.values())

HYPERBOLIC = 0
for point, u in enumerate(U):
    HYPERBOLIC |= (u[0] * u[1]) << point
ONE_FIBRE = HYPERBOLIC
THREE_FIBRE = FULL ^ HYPERBOLIC

RELATION_SPACES = (
    frozenset((0,)),
    frozenset((0, 1)),
    frozenset((0, 2)),
    frozenset((0, 3)),
    frozenset((0, 1, 2, 3)),
)


def k0_relation(first: int, second: int) -> frozenset[int]:
    return frozenset(
        relation
        for relation in range(4)
        if ((first if relation & 1 else 0) ^ (second if relation & 2 else 0)) == 0
    )


def independent(
    relation_kernel: frozenset[int], f0: int, f1: int, f2: int
) -> bool:
    for relation in relation_kernel:
        if relation == 0:
            continue
        combination = (f1 if relation & 1 else 0) ^ (f2 if relation & 2 else 0)
        if combination in (0, f0):
            return False
    return True


def neutral_counts(
    fibre: int, relation_kernel: frozenset[int]
) -> tuple[set[int], set[int]]:
    all_counts: set[int] = set()
    independent_counts: set[int] = set()
    f0 = ((1 << 0) | (1 << 3)) if fibre == ONE_FIBRE else (1 << 3)
    for first_coefficients, first_mask in QUADRATIC_BY_COEFFICIENT.items():
        f1 = first_coefficients ^ 1
        for second_coefficients, second_mask in QUADRATIC_BY_COEFFICIENT.items():
            count = (fibre & first_mask & second_mask).bit_count()
            all_counts.add(count)
            f2 = second_coefficients ^ 1
            if independent(relation_kernel, f0, f1, f2):
                independent_counts.add(count)
    return all_counts, independent_counts


def main() -> None:
    assert len(U) == 4
    assert ONE_FIBRE.bit_count() == 1
    assert THREE_FIBRE.bit_count() == 3
    assert len(AFFINE) == 8
    assert len(ONE_PRODUCT) == 12
    assert len(TWO_PRODUCTS) == 16
    assert TWO_PRODUCTS == QUADRATIC == frozenset(range(16))

    observed: set[frozenset[int]] = set()
    for first, second in product(range(1 << 3), repeat=2):
        observed.add(k0_relation(first, second))
    assert observed == set(RELATION_SPACES)
    for first, second, third in product(RELATION_SPACES, repeat=3):
        assert (first & second) in RELATION_SPACES
        assert (first & second) & third == first & (second & third)

    all_relations = frozenset((0, 1, 2, 3))
    no_relations = frozenset((0,))
    one_all, one_independent = neutral_counts(ONE_FIBRE, all_relations)
    three_all, three_independent = neutral_counts(THREE_FIBRE, all_relations)
    _, three_automatic = neutral_counts(THREE_FIBRE, no_relations)
    assert one_all == one_independent == {0, 1}
    assert three_all == {0, 1, 2, 3}
    assert three_independent == {0, 1}
    assert three_automatic == {0, 1, 2, 3}

    # Destructive control: omitting the relation kernel falsely admits common
    # zero fibres of size two and three in the pure-core three-point stratum.
    assert {2, 3}.issubset(three_all - three_independent)

    print("PASS: four-core affine/product transfer classes stabilize after two products")
    print("PASS: the five relation kernels form the direct-sum intersection monoid")
    print("PASS: one- and three-point outputs enforce three-generator independence")
    print("CONCLUSION: both nonzero-Walsh rank-two signs admit one exact finite recursion")


if __name__ == "__main__":
    main()
