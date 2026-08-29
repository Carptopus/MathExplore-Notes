"""Verify the rank-four obstruction on the full 19/8 ray.

For radical dimension m=n-4, the target is

    Z = 19 * 2^(m-5),  m >= 8.

After division by the common factor 2^(m-5), the arithmetic gate depends only
on the three half-ranks delta_i.  Rank triangle and the six-point mask sizes
leave seven unordered half-rank profiles.  Canonical pencil blocks then reduce
to nine bounded cores plus common-radical K0 blocks.  The K0 transfer semigroup
stabilizes after two blocks, so three exact checks (0, 1, at least 2 K0 blocks)
cover every m.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product


FULL = 63
COEFFICIENTS = (-6, -4, -3, -2, -1, 0, 1, 2, 3, 4, 6)


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


def arithmetic_half_rank_profiles() -> set[tuple[int, int, int]]:
    # If the least half-rank were at least three, the total absolute normalized
    # correction would be at most 3*6*2^(5-3)=72<116.  Rank triangle then bounds
    # every candidate by five once the least half-rank is 0, 1, or 2.  Enumerate
    # this finite over-approximation; COEFFICIENTS already ignores correlations
    # between the six slice signs.
    result: set[tuple[int, int, int]] = set()
    scale = 1 << 5
    for half_ranks in product(range(6), repeat=3):
        if any(
            half_ranks[index]
            > half_ranks[(index + 1) % 3] + half_ranks[(index + 2) % 3]
            for index in range(3)
        ):
            continue
        denominators = [1 << half_rank for half_rank in half_ranks]
        common = 1 << max(half_ranks)
        weights = [scale * common // denominator for denominator in denominators]
        target = -116 * common
        if any(
            first * weights[0] + second * weights[1] + third * weights[2] == target
            for first, second, third in product(COEFFICIENTS, repeat=3)
        ):
            result.add(half_ranks)
    return result


def add_vectors(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(left[index] + right[index] for index in range(3))


def bounded_core_paths(
    candidate_profiles: set[tuple[int, int, int]],
) -> set[tuple[str, ...]]:
    # A candidate profile has minimum at most one.  Consequently every
    # non-K0 canonical block with minimum contribution at least two is absent.
    # Only K1=(1,1,1), D1@j=(0,1,1), and D2@j=(1,2,2) can remain.
    blocks: list[tuple[str, tuple[int, int, int]]] = [("K1", (1, 1, 1))]
    for component in range(3):
        d1 = [1, 1, 1]
        d1[component] = 0
        blocks.append((f"D1@{component}", tuple(d1)))
    for component in range(3):
        d2 = [2, 2, 2]
        d2[component] = 1
        blocks.append((f"D2@{component}", tuple(d2)))

    result: set[tuple[str, ...]] = set()

    def recurse(
        first_index: int,
        total: tuple[int, int, int],
        path: tuple[str, ...],
    ) -> None:
        if total in candidate_profiles and path:
            result.add(path)
        if max(total) >= 5:
            return
        for index in range(first_index, len(blocks)):
            name, contribution = blocks[index]
            updated = add_vectors(total, contribution)
            if all(value <= 5 for value in updated):
                recurse(index, updated, (*path, name))

    recurse(0, (0, 0, 0), ())
    return result


def canonicalize_path(path: tuple[str, ...]) -> tuple[str, ...]:
    best: tuple[str, ...] | None = None
    for permutation in permutations(range(3)):
        renamed: list[str] = []
        for name in path:
            if "@" not in name:
                renamed.append(name)
                continue
            family, raw_component = name.split("@")
            renamed.append(f"{family}@{permutation[int(raw_component)]}")
        candidate = tuple(sorted(renamed))
        if best is None or candidate < best:
            best = candidate
    assert best is not None
    return best


CORE_TYPES = {
    ("D1@0", "D1@0", "D1@0"),
    ("D1@0", "D1@0", "D1@0", "D1@0"),
    ("D1@0", "D1@0", "D1@0", "D1@0", "D1@0"),
    ("D1@0", "D1@0", "D1@0", "D1@1"),
    ("D1@0", "D1@0", "D1@0", "K1"),
    ("D1@0", "D1@0", "D1@1"),
    ("D1@0", "D1@0", "D2@0"),
    ("D1@0", "D1@0", "K1"),
    ("D1@0", "D2@0"),
}


def k0_levels() -> list[set[tuple[int, int, int]]]:
    one = {
        (first, second, (~(first ^ second)) & FULL)
        for first in AFFINE
        for second in AFFINE
    }
    two = {
        tuple(first[index] & second[index] for index in range(3))
        for first in one
        for second in one
    }
    three = {
        tuple(first[index] & second[index] for index in range(3))
        for first in two
        for second in one
    }
    assert len(one) == 1024
    assert len(two) == 14017
    assert three == two
    return [{(FULL, FULL, FULL)}, one, two]


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
    core_dimension: int,
    exponents: tuple[int, int, int],
    product_sign: int | None,
) -> set[tuple[int, ...]]:
    target = -116 * (1 << (core_dimension - 5))
    magnitudes = tuple(1 << exponent for exponent in exponents)
    local = [local_corrections(active, magnitudes, product_sign) for active in range(8)]
    result: set[tuple[int, ...]] = set()

    def recurse(
        active: int, remaining: int, counts: tuple[int, ...], sums: set[int]
    ) -> None:
        if active == 7:
            for _ in range(remaining):
                sums = {left + right for left in sums for right in local[active]}
            if target in sums:
                result.add((*counts, remaining))
            return
        for count in range(remaining + 1):
            updated = sums
            for _ in range(count):
                updated = {left + right for left in updated for right in local[active]}
            recurse(active + 1, remaining - count, (*counts, count), updated)

    recurse(0, 6, (), {0})
    return result


def core_data(path: tuple[str, ...]) -> tuple[int, tuple[int, int, int], bool, list[bool]]:
    dimension = 0
    exponents = [0, 0, 0]
    has_k1 = False
    has_d = [False, False, False]
    for name in path:
        if name == "K1":
            dimension += 3
            exponents = [value + 2 for value in exponents]
            has_k1 = True
        else:
            family, raw_component = name.split("@")
            component = int(raw_component)
            k = int(family[1:])
            dimension += 2 * k
            for index in range(3):
                exponents[index] += k + (1 if index == component else 0)
            has_d[component] = True
    return dimension, tuple(exponents), has_k1, has_d


def exact_sigma_works(
    core_dimension: int, exponents: tuple[int, int, int], negative_mask: int
) -> bool:
    target = -116 * (1 << (core_dimension - 5))
    magnitudes = tuple(1 << exponent for exponent in exponents)
    sums = {0}
    for point in range(6):
        product_sign = -1 if negative_mask & (1 << point) else 1
        choices = local_corrections(7, magnitudes, product_sign)
        sums = {left + right for left in sums for right in choices}
    return target in sums


def reject_d_only_core(path: tuple[str, ...], levels: list[set[tuple[int, int, int]]]) -> None:
    dimension, exponents, _, has_d = core_data(path)
    d2_components = {
        int(name.split("@")[1]) for name in path if name.startswith("D2@")
    }
    assert len(d2_components) <= 1
    positive = good_histograms(dimension, exponents, 1)
    arbitrary = (
        good_histograms(dimension, exponents, None) if d2_components else set()
    )
    cache_product = {
        mask: {mask & candidate for candidate in PRODUCT_MASKS}
        for mask in range(64)
    }

    for k0_count, base_states in enumerate(levels):
        if dimension + k0_count < 8 and k0_count < 2:
            continue
        for base in base_states:
            choices = [
                cache_product[base[index]] if has_d[index] else {base[index]}
                for index in range(3)
            ]
            for masks in product(*choices):
                common = masks[0] & masks[1] & masks[2]
                histogram = active_histogram(masks)
                if not d2_components:
                    assert histogram not in positive
                elif common != FULL:
                    assert histogram not in arbitrary
                else:
                    assert not any(
                        exact_sigma_works(dimension, exponents, negative_mask)
                        for negative_mask in PRODUCT_MASKS
                    )


def reject_k1_cores() -> None:
    # K1+three D1 blocks: even the independent PRODUCT_MASKS^3
    # over-approximation has no target histogram.
    path_long = ("D1@0", "D1@0", "D1@0", "K1")
    dimension, exponents, _, _ = core_data(path_long)
    positive = good_histograms(dimension, exponents, 1)
    assert not any(
        active_histogram(masks) in positive
        for masks in product(PRODUCT_MASKS, repeat=3)
    )

    # K1+two D1 blocks: target arithmetic forces the D1 component to be full.
    # K0 full on that component forces the two K0 affine coefficients equal;
    # the remaining masks reduce to two affine masks.  The required pattern is
    # either union H/intersection one point or union five/intersection empty;
    # no pair of affine masks on H has either pattern.
    path_short = ("D1@0", "D1@0", "K1")
    dimension, exponents, _, _ = core_data(path_short)
    positive = good_histograms(dimension, exponents, 1)
    assert len(positive) == 12
    assert not any(
        ((first | second) == FULL and (first & second).bit_count() == 1)
        or ((first | second).bit_count() == 5 and (first & second) == 0)
        for first, second in product(AFFINE, repeat=2)
    )


def main() -> None:
    assert len(AFFINE) == 32
    assert len(PRODUCT_MASKS) == 58
    assert set(range(64)) - PRODUCT_MASKS == {
        FULL ^ (1 << index) for index in range(6)
    }

    profiles = arithmetic_half_rank_profiles()
    assert {tuple(sorted(profile)) for profile in profiles} == {
        (0, 3, 3),
        (0, 4, 4),
        (0, 5, 5),
        (1, 2, 3),
        (1, 3, 3),
        (1, 3, 4),
        (1, 4, 4),
    }
    assert len(profiles) == 27

    paths = bounded_core_paths(profiles)
    canonical_paths = {canonicalize_path(path) for path in paths}
    assert len(paths) == 33
    assert canonical_paths == CORE_TYPES

    levels = k0_levels()
    for path in sorted(CORE_TYPES):
        if "K1" in path:
            continue
        reject_d_only_core(path, levels)
    reject_k1_cores()

    print("PASS: arithmetic gate leaves seven unordered half-rank profiles")
    print("PASS: canonical pencils reduce to nine bounded cores plus K0 blocks")
    print("PASS: K0 six-point transfer stabilizes after two blocks")
    print("PASS: all nine cores rejected for 0, 1, and at least 2 K0 blocks")
    print("CONCLUSION: the rank-four branch cannot realize 19*2^(n-9) for any n>=12")


if __name__ == "__main__":
    main()
