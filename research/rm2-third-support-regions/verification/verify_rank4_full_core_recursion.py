"""Verify the 16-core lift that closes both signs of the rank-four stratum.

The six-slice recursion uses the fact that quadratic core functions restrict
surjectively to the six-point quadric H.  Its ten-point complement does not
have that freedom.  The exact repair is still finite:

* keep masks on all 16 core points;
* replace arbitrary sign masks by sums of r affine products, where r is the
  exact block sign-control rank;
* keep the relation kernel of the two non-core functions;
* enumerate the two 11-dimensional quadratic core twists and retain only
  choices that make the three generators independent.

This script verifies the finite function classes, their restriction to the
old six-point state, the relation-kernel monoid, and the indispensable
independence filter on the six- and ten-point rank-four fibres.
"""

from __future__ import annotations

from itertools import product


U = tuple(product((0, 1), repeat=4))
FULL = (1 << 16) - 1


def monomials(u: tuple[int, int, int, int]) -> tuple[int, ...]:
    return (
        1,
        *u,
        *(u[i] * u[j] for i in range(4) for j in range(i + 1, 4)),
    )


def evaluation_mask(coefficients: int, degree_two: bool = True) -> int:
    width = 11 if degree_two else 5
    mask = 0
    for point, u in enumerate(U):
        value = sum(
            ((coefficients >> index) & 1) * entry
            for index, entry in enumerate(monomials(u)[:width])
        ) % 2
        mask |= value << point
    return mask


AFFINE_BY_COEFFICIENT = {
    coefficients: evaluation_mask(coefficients, degree_two=False)
    for coefficients in range(1 << 5)
}
AFFINE = frozenset(AFFINE_BY_COEFFICIENT.values())
ONE_PRODUCT = frozenset(left & right for left in AFFINE for right in AFFINE)
TWO_PRODUCTS = frozenset(left ^ right for left in ONE_PRODUCT for right in ONE_PRODUCT)
THREE_PRODUCTS = frozenset(left ^ right for left in TWO_PRODUCTS for right in ONE_PRODUCT)
QUADRATIC_BY_COEFFICIENT = {
    coefficients: evaluation_mask(coefficients) for coefficients in range(1 << 11)
}
QUADRATIC = frozenset(QUADRATIC_BY_COEFFICIENT.values())


HYPERBOLIC = 0
for point, u in enumerate(U):
    HYPERBOLIC |= (u[0] * u[1] ^ u[2] * u[3]) << point
SIX_FIBRE = HYPERBOLIC
TEN_FIBRE = FULL ^ HYPERBOLIC
SIX_POINTS = tuple(point for point in range(16) if SIX_FIBRE & (1 << point))


def restrict_to_six(mask: int) -> int:
    result = 0
    for target, source in enumerate(SIX_POINTS):
        result |= ((mask >> source) & 1) << target
    return result


RELATION_SPACES = (
    frozenset((0,)),
    frozenset((0, 1)),
    frozenset((0, 2)),
    frozenset((0, 3)),
    frozenset((0, 1, 2, 3)),
)


def k0_relation(first_coefficients: int, second_coefficients: int) -> frozenset[int]:
    return frozenset(
        relation
        for relation in range(4)
        if (
            ((first_coefficients if relation & 1 else 0)
             ^ (second_coefficients if relation & 2 else 0))
            == 0
        )
    )


def independent_after_core_choice(
    relation_kernel: frozenset[int],
    f0: int,
    f1_core: int,
    f2_core: int,
) -> bool:
    for relation in relation_kernel:
        if relation == 0:
            continue
        core_combination = (
            (f1_core if relation & 1 else 0)
            ^ (f2_core if relation & 2 else 0)
        )
        if core_combination in (0, f0):
            return False
    return True


def neutral_zero_counts(
    fibre: int, relation_kernel: frozenset[int]
) -> tuple[set[int], set[int]]:
    # q_i are the chosen core quadratics; f_i=1+q_i.  The first returned set
    # ignores generator independence and the second enforces it.
    all_counts: set[int] = set()
    independent_counts: set[int] = set()
    q0_small = fibre == SIX_FIBRE
    f0 = ((1 << 0) | (1 << 5) | (1 << 10)) if q0_small else ((1 << 5) | (1 << 10))
    for first_coefficients, first_mask in QUADRATIC_BY_COEFFICIENT.items():
        f1_core = first_coefficients ^ (1 << 0)
        for second_coefficients, second_mask in QUADRATIC_BY_COEFFICIENT.items():
            count = (fibre & first_mask & second_mask).bit_count()
            all_counts.add(count)
            f2_core = second_coefficients ^ (1 << 0)
            if independent_after_core_choice(relation_kernel, f0, f1_core, f2_core):
                independent_counts.add(count)
    return all_counts, independent_counts


def verify_function_classes() -> None:
    assert len(U) == 16
    assert SIX_FIBRE.bit_count() == 6
    assert TEN_FIBRE.bit_count() == 10
    assert len(AFFINE) == 32
    assert len(ONE_PRODUCT) == 172
    assert len(TWO_PRODUCTS) == 1600
    assert len(THREE_PRODUCTS) == 2048
    assert THREE_PRODUCTS == QUADRATIC

    # Restriction recovers exactly the old six-point transition classes:
    # affine masks, one-product masks, then all 64 functions after two
    # products.  This is the required regression to ROUND 10.
    assert len({restrict_to_six(mask) for mask in AFFINE}) == 32
    assert len({restrict_to_six(mask) for mask in ONE_PRODUCT}) == 58
    assert {restrict_to_six(mask) for mask in TWO_PRODUCTS} == set(range(64))
    assert {restrict_to_six(mask) for mask in THREE_PRODUCTS} == set(range(64))


def verify_relation_kernel() -> None:
    observed: set[frozenset[int]] = set()
    for first, second in product(range(1 << 5), repeat=2):
        relation = k0_relation(first, second)
        observed.add(relation)
        first_mask = AFFINE_BY_COEFFICIENT[first]
        second_mask = AFFINE_BY_COEFFICIENT[second]

        # The affine evaluation map is injective.  Hence the K0 relation
        # kernel can be recovered from its two nonzero masks alone.
        inferred = {0}
        if first_mask == 0:
            inferred.add(1)
        if second_mask == 0:
            inferred.add(2)
        if first_mask == second_mask:
            inferred.add(3)
        assert relation == frozenset(inferred)
    assert observed == set(RELATION_SPACES)

    # Direct sums intersect relation kernels.  Intersection is associative
    # and stays inside the five subspaces of F_2^2.
    for first, second, third in product(RELATION_SPACES, repeat=3):
        assert (first & second) in RELATION_SPACES
        assert (first & second) & third == first & (second & third)


def verify_core_output_and_independence() -> None:
    no_relations = frozenset((0,))
    all_relations = frozenset((0, 1, 2, 3))

    six_all, six_independent = neutral_zero_counts(SIX_FIBRE, all_relations)
    ten_all, ten_independent = neutral_zero_counts(TEN_FIBRE, all_relations)
    assert six_all == set(range(7))
    assert six_independent == set(range(7))
    assert ten_all == set(range(11))
    assert ten_independent == set(range(9))

    # If the non-core parts of f1,f2 are already independent, no core filter
    # remains and all ten intersection sizes return.
    _, ten_automatic = neutral_zero_counts(TEN_FIBRE, no_relations)
    assert ten_automatic == set(range(11))

    # Destructive control: omitting the relation state would falsely admit 9
    # and 10 in the pure-core ten-point case.
    assert {9, 10}.issubset(ten_all - ten_independent)


def main() -> None:
    verify_function_classes()
    verify_relation_kernel()
    verify_core_output_and_independence()

    print("PASS: 16-core affine/product/quadratic transfer classes verified")
    print("PASS: restriction to the six-point recursion exactly recovers ROUND 10")
    print("PASS: the five relation kernels form the direct-sum intersection monoid")
    print("PASS: six- and ten-point core outputs enforce generator independence")
    print("CONCLUSION: both nonzero-Walsh rank-four signs admit one exact finite recursion")


if __name__ == "__main__":
    main()
