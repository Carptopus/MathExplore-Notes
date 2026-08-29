"""Verify the hit transfer set for a nondegenerate regular pencil block."""

from __future__ import annotations

from itertools import product


def core_points() -> list[tuple[int, int, int, int]]:
    return [
        u
        for u in product((0, 1), repeat=4)
        if (u[0] * u[1] + u[2] * u[3]) % 2 == 1
    ]


def affine_masks(points: list[tuple[int, int, int, int]]) -> list[int]:
    masks: list[int] = []
    for coefficients in product((0, 1), repeat=5):
        mask = 0
        for index, u in enumerate(points):
            value = coefficients[0]
            value ^= sum(coefficients[i + 1] * u[i] for i in range(4)) % 2
            mask |= value << index
        masks.append(mask)
    return sorted(set(masks))


def main() -> None:
    points = core_points()
    affine = affine_masks(points)
    assert len(points) == 6
    assert len(affine) == 32

    # A product of two affine functions is the intersection of their masks.
    products = {left & right for left in affine for right in affine}
    missing = set(range(64)) - products
    assert missing == {63 ^ (1 << index) for index in range(6)}

    # The only missing one-product masks are complements of singletons.  The
    # full mask and every singleton are products, so two products suffice for
    # all 64 functions on the six-point core quadric.
    witnesses: dict[int, tuple[int, int, int, int]] = {}
    for left_1 in affine:
        for right_1 in affine:
            first = left_1 & right_1
            for left_2 in affine:
                for right_2 in affine:
                    target = first ^ (left_2 & right_2)
                    witnesses.setdefault(target, (left_1, right_1, left_2, right_2))
            if len(witnesses) == 64:
                break
        if len(witnesses) == 64:
            break
    assert set(witnesses) == set(range(64))

    # For a regular block Q1=x^T y, Q2=x^T C y with C and I+C invertible,
    # choose p2=r1=0.  Formula (35) becomes
    #
    #   P(u) = p1(u)^T (I+C)^(-T) r2(u).
    #
    # In dimension d>=2 set p1=(a1,a2,0,...) and
    # r2=(I+C)^T(b1,b2,0,...).  Then P=a1*b1+a2*b2, so each witness above
    # is a valid affine marked-vector construction for every such block.
    for target, (a_1, b_1, a_2, b_2) in witnesses.items():
        reconstructed = (a_1 & b_1) ^ (a_2 & b_2)
        assert reconstructed == target

    # Destructive negative control: one product does not realize a five-point
    # mask, so the second coordinate in the construction is essential.
    assert (63 ^ 1) not in products
    assert (63 ^ 1) in witnesses

    print("PASS: affine restriction code has 32 masks on the six-point core")
    print("PASS: one product gives 58 masks; the six missing masks are 5-subsets")
    print("PASS: two products give all 64 hit-block product-sign masks")
    print("PASS: five-point destructive control requires the second product")


if __name__ == "__main__":
    main()
