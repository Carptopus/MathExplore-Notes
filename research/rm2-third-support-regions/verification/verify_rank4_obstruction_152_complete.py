"""Exact rank-four six-slice obstruction for n=12 and Z=152.

The proof has three finite layers:

1. enumerate all canonical alternating-pencil block decompositions of an
   eight-dimensional radical;
2. apply a sign-free arithmetic over-approximation, leaving 27 decompositions
   in seven component-symmetric structural families;
3. use the exact K0, K1, D1 and D2 six-point transfer masks to reject every
   surviving family.

All longer singular, degenerate, and nondegenerate regular blocks are removed
by layer 2, rather than assumed absent.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product


TARGET_CORRECTION = -928  # 4*152 - 6*2^8
FULL = 63


def core_points() -> list[tuple[int, int, int, int]]:
    return [
        u
        for u in product((0, 1), repeat=4)
        if (u[0] * u[1] + u[2] * u[3]) % 2 == 1
    ]


def affine_zero_masks() -> set[int]:
    points = core_points()
    result: set[int] = set()
    for coefficients in product((0, 1), repeat=5):
        mask = 0
        for index, u in enumerate(points):
            value = coefficients[0]
            value ^= sum(coefficients[i + 1] * u[i] for i in range(4)) % 2
            mask |= (1 ^ value) << index
        result.add(mask)
    return result


AFFINE = affine_zero_masks()
PRODUCT_MASKS = {left & right for left in AFFINE for right in AFFINE}


def signed_sums(magnitude: int, count: int) -> set[int]:
    return {magnitude * (2 * positive - count) for positive in range(count + 1)}


def arithmetic_profile_possible(exponents: tuple[int, int, int]) -> bool:
    # Every global nonzero mask is an intersection of affine masks, so its size
    # is 0,1,2,3,4, or 6, never 5.  Ignore every remaining sign correlation.
    for counts in product((0, 1, 2, 3, 4, 6), repeat=3):
        choices = [
            signed_sums(1 << exponent, count)
            for exponent, count in zip(exponents, counts)
        ]
        if any(
            first + second + third == TARGET_CORRECTION
            for first in choices[0]
            for second in choices[1]
            for third in choices[2]
        ):
            return True
    return False


def canonical_blocks() -> list[tuple[str, int, tuple[int, int, int]]]:
    blocks: list[tuple[str, int, tuple[int, int, int]]] = [
        ("K0", 1, (1, 1, 1))
    ]
    for k in range(1, 4):
        blocks.append((f"K{k}", 2 * k + 1, (k + 1, k + 1, k + 1)))
    for k in range(1, 5):
        for singular_component in range(3):
            exponents = [k, k, k]
            exponents[singular_component] += 1
            blocks.append(
                (f"D{k}@{singular_component}", 2 * k, tuple(exponents))
            )
    for d in range(2, 5):
        blocks.append((f"R{d}", 2 * d, (d, d, d)))
    return blocks


def candidate_decompositions() -> list[tuple[tuple[int, int, int], tuple[str, ...]]]:
    blocks = canonical_blocks()
    result: list[tuple[tuple[int, int, int], tuple[str, ...]]] = []

    def recurse(
        remaining: int,
        first_index: int,
        exponents: tuple[int, int, int],
        path: tuple[str, ...],
    ) -> None:
        if remaining == 0:
            if arithmetic_profile_possible(exponents):
                result.append((exponents, path))
            return
        for index in range(first_index, len(blocks)):
            name, dimension, contribution = blocks[index]
            if dimension > remaining:
                continue
            recurse(
                remaining - dimension,
                index,
                tuple(exponents[i] + contribution[i] for i in range(3)),
                (*path, name),
            )

    recurse(8, 0, (0, 0, 0), ())
    return result


def local_corrections(
    active: int, magnitudes: tuple[int, int, int], product_sign: int | None
) -> set[int]:
    indices = [index for index in range(3) if active & (1 << index)]
    result: set[int] = set()
    for signs in product((-1, 1), repeat=len(indices)):
        if len(indices) == 3 and product_sign is not None:
            if signs[0] * signs[1] * signs[2] != product_sign:
                continue
        result.add(
            sum(signs[position] * magnitudes[index] for position, index in enumerate(indices))
        )
    return result


def active_histogram(masks: tuple[int, int, int]) -> tuple[int, ...]:
    counts = [0] * 8
    for point in range(6):
        active = sum(((mask >> point) & 1) << index for index, mask in enumerate(masks))
        counts[active] += 1
    return tuple(counts)


def good_histograms(
    exponents: tuple[int, int, int], product_sign: int | None
) -> set[tuple[int, ...]]:
    magnitudes = tuple(1 << exponent for exponent in exponents)
    local = [local_corrections(active, magnitudes, product_sign) for active in range(8)]
    result: set[tuple[int, ...]] = set()

    def recurse(
        active: int, remaining: int, counts: tuple[int, ...], sums: set[int]
    ) -> None:
        if active == 7:
            for _ in range(remaining):
                sums = {left + right for left in sums for right in local[active]}
            if TARGET_CORRECTION in sums:
                result.add((*counts, remaining))
            return
        for count in range(remaining + 1):
            next_sums = sums
            for _ in range(count):
                next_sums = {
                    left + right for left in next_sums for right in local[active]
                }
            recurse(active + 1, remaining - count, (*counts, count), next_sums)

    recurse(0, 6, (), {0})
    return result


def exact_sigma_works(exponents: tuple[int, int, int], negative_mask: int) -> bool:
    magnitudes = tuple(1 << exponent for exponent in exponents)
    sums = {0}
    for point in range(6):
        product_sign = -1 if negative_mask & (1 << point) else 1
        choices = local_corrections(7, magnitudes, product_sign)
        sums = {left + right for left in sums for right in choices}
    return TARGET_CORRECTION in sums


def k0_states() -> set[tuple[int, int, int]]:
    # If the two affine coefficients are a,b, the three nonzero masks are
    # Z(a), Z(b), Z(a+b).  On truth masks, Z(a+b) is the complement of XOR.
    return {
        (first, second, (~(first ^ second)) & FULL)
        for first in AFFINE
        for second in AFFINE
    }


def verify_surviving_families() -> None:
    positive_448 = good_histograms((4, 4, 8), 1)
    assert not any(
        active_histogram((FULL, FULL, high)) in positive_448
        for high in PRODUCT_MASKS
    )

    positive_457 = good_histograms((4, 5, 7), 1)
    assert not any(
        active_histogram((FULL, middle, high)) in positive_457
        for middle in PRODUCT_MASKS
        for high in PRODUCT_MASKS
    )

    # D1+D1+D2 at the same pencil point.  Arithmetic with arbitrary product
    # signs works only when all three masks are full; then the target requires
    # exactly a five-point negative mask.  D2 length two realizes every
    # product mask and precisely excludes those six masks.
    arbitrary_447 = good_histograms((4, 4, 7), None)
    hits_447 = [
        high
        for high in PRODUCT_MASKS
        if active_histogram((FULL, FULL, high)) in arbitrary_447
    ]
    assert hits_447 == [FULL]
    required_sigma_447 = {
        mask for mask in range(64) if exact_sigma_works((4, 4, 7), mask)
    }
    assert required_sigma_447 == {FULL ^ (1 << index) for index in range(6)}
    assert required_sigma_447.isdisjoint(PRODUCT_MASKS)

    k0 = k0_states()
    k00 = {
        tuple(first[index] & second[index] for index in range(3))
        for first in k0
        for second in k0
    }
    assert len(k0) == 1024
    assert len(k00) == 14017

    positive_558 = good_histograms((5, 5, 8), 1)
    assert not any(
        active_histogram((base[0], base[1], base[2] & high)) in positive_558
        for base in k00
        for high in PRODUCT_MASKS
    )

    positive_567 = good_histograms((5, 6, 7), 1)
    restricted_products = {
        mask: {mask & candidate for candidate in PRODUCT_MASKS}
        for mask in range(64)
    }
    assert not any(
        active_histogram((base[0], middle, high)) in positive_567
        for base in k00
        for middle in restricted_products[base[1]]
        for high in restricted_products[base[2]]
    )

    # K0+K0+D1+D2.  D2 makes the product sign arbitrary whenever the global
    # common mask is proper.  If the common mask is full, its length-two sign
    # set is again PRODUCT_MASKS.
    arbitrary_557 = good_histograms((5, 5, 7), None)
    for base in k00:
        for high in restricted_products[base[2]]:
            masks = (base[0], base[1], high)
            common = masks[0] & masks[1] & masks[2]
            if common != FULL:
                assert active_histogram(masks) not in arbitrary_557
    assert not any(exact_sigma_works((5, 5, 7), mask) for mask in PRODUCT_MASKS)

    # K0+K1+D1+D1.  K1 contributes three independent affine masks; the two
    # D1 blocks add one more product mask to the high component.  Product sign
    # stays positive.
    positive_557 = good_histograms((5, 5, 7), 1)
    restricted_affine = {
        mask: {mask & candidate for candidate in AFFINE} for mask in range(64)
    }
    assert not any(
        active_histogram((low_1, low_2, high)) in positive_557
        for base in k0
        for low_1 in restricted_affine[base[0]]
        for low_2 in restricted_affine[base[1]]
        for high in restricted_products[base[2]]
    )


def main() -> None:
    assert len(AFFINE) == 32
    assert len(PRODUCT_MASKS) == 58
    assert set(range(64)) - PRODUCT_MASKS == {
        FULL ^ (1 << index) for index in range(6)
    }

    candidates = candidate_decompositions()
    assert len(candidates) == 27
    profile_counts = Counter(tuple(sorted(exponents)) for exponents, _ in candidates)
    assert profile_counts == Counter(
        {
            (4, 4, 7): 3,
            (4, 4, 8): 3,
            (4, 5, 7): 6,
            (5, 5, 7): 6,
            (5, 5, 8): 3,
            (5, 6, 7): 6,
        }
    )

    path_kinds: defaultdict[str, int] = defaultdict(int)
    for _, path in candidates:
        names = Counter(name.split("@")[0] for name in path)
        if names == Counter({"D1": 4}):
            path_kinds["four_D1"] += 1
        elif names == Counter({"D1": 2, "D2": 1}):
            path_kinds["two_D1_one_D2"] += 1
        elif names == Counter({"K0": 2, "D1": 3}):
            path_kinds["two_K0_three_D1"] += 1
        elif names == Counter({"K0": 2, "D1": 1, "D2": 1}):
            path_kinds["two_K0_D1_D2"] += 1
        elif names == Counter({"K0": 1, "K1": 1, "D1": 2}):
            path_kinds["K0_K1_two_D1"] += 1
        else:
            raise AssertionError(f"unexpected surviving path: {path}")
    assert sum(path_kinds.values()) == 27

    verify_surviving_families()

    print("PASS: all canonical block decompositions of radical dimension 8 enumerated")
    print("PASS: arithmetic gate leaves exactly 27 paths in six exponent profiles")
    print("PASS: exact K0/K1/D1/D2 mask transfers reject every surviving path")
    print("CONCLUSION: no rank-four six-slice representation has n=12 and Z=152")


if __name__ == "__main__":
    main()
