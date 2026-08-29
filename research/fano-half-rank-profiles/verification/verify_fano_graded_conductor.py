"""Exact conductor certificate for the fixed-dimension Fano rank profile.

The separately checked low layers certify which profiles of height at most six
have a sharp realization in dimension twice their height.  This program proves
that those finite bases, together with the scaled chamber rays, cover every
higher profile except the stated small exceptions and the infinite E_t family.
All cone, residue, and transition calculations use exact integer arithmetic.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations

import sympy as sp

from probe_fano_anchor_cone_hilbert_basis import LINES, RAYS, pulling, residues


Profile = tuple[int, ...]


def add(*profiles: Profile) -> Profile:
    return tuple(sum(values) for values in zip(*profiles))


def multiply(coefficient: int, profile: Profile) -> Profile:
    return tuple(coefficient * value for value in profile)


def cut_profiles() -> set[Profile]:
    return {
        tuple(0 if point in line else 1 for point in range(7))
        for line in LINES
    }


CUTS = cut_profiles()


def line_jumps() -> set[Profile]:
    return {
        tuple(2 if point in line else 1 for point in range(7))
        for line in LINES
    }


LINE_JUMPS = line_jumps()


def scaled_ray(ray: Profile) -> Profile:
    if ray == (1,) * 7:
        return multiply(3, ray)
    if (max(ray) == 1 and ray not in CUTS) or ray in LINE_JUMPS:
        return multiply(2, ray)
    return ray


def half_rank_four(mask: int) -> int:
    rows = [0] * 4
    edge = 0
    for left in range(4):
        for right in range(left + 1, 4):
            if (mask >> edge) & 1:
                rows[left] |= 1 << right
                rows[right] |= 1 << left
            edge += 1
    rank = 0
    for column in range(4):
        pivot = next(
            (row for row in range(rank, 4) if (rows[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(4):
            if row != rank and ((rows[row] >> column) & 1):
                rows[row] ^= rows[rank]
        rank += 1
    return rank // 2


def dimension_four_profiles() -> set[Profile]:
    ranks = tuple(half_rank_four(mask) for mask in range(64))
    return {
        (
            ranks[first], ranks[second], ranks[first ^ second], ranks[third],
            ranks[first ^ third], ranks[second ^ third],
            ranks[first ^ second ^ third],
        )
        for first in range(64)
        for second in range(64)
        for third in range(64)
    }


DIMENSION_FOUR = dimension_four_profiles()


def bounded_holes(bound: int) -> set[Profile]:
    result = set(LINE_JUMPS)
    for distinguished in range(7):
        singleton = tuple(2 if point == distinguished else 1 for point in range(7))
        cuts = tuple(cut for cut in CUTS if cut[distinguished] == 1)
        assert len(cuts) == 4
        for first in range(bound + 1):
            for second in range(bound + 1):
                for third in range(bound + 1):
                    for fourth in range(bound + 1):
                        profile = add(
                            singleton,
                            multiply(first, cuts[0]),
                            multiply(second, cuts[1]),
                            multiply(third, cuts[2]),
                            multiply(fourth, cuts[3]),
                        )
                        if max(profile) <= bound:
                            result.add(profile)
    return result


HOLES = bounded_holes(10)


def singleton_owners(profile: Profile) -> set[int]:
    owners = set()
    target = sp.Matrix(profile)
    for distinguished in range(7):
        singleton = sp.Matrix(tuple(2 if point == distinguished else 1 for point in range(7)))
        cuts = tuple(cut for cut in CUTS if cut[distinguished] == 1)
        matrix = sp.Matrix.hstack(*(sp.Matrix(cut) for cut in cuts))
        solutions = list(sp.linsolve((matrix, target - singleton)))
        if solutions and all(value.is_integer and value >= 0 for value in solutions[0]):
            owners.add(distinguished)
    return owners


def e_profile(triple: tuple[int, int, int], height: int) -> Profile:
    result = [1] * 7
    for point in triple:
        result[point - 1] = height
    result[(triple[0] ^ triple[1] ^ triple[2]) - 1] = height - 1
    return tuple(result)


NONCOLLINEAR_TRIPLES = tuple(
    triple for triple in combinations(range(1, 8), 3)
    if triple[0] ^ triple[1] ^ triple[2]
)


def e_witness(profile: Profile) -> tuple[int, int, int] | None:
    height = max(profile)
    if height < 3:
        return None
    return next(
        (triple for triple in NONCOLLINEAR_TRIPLES
         if e_profile(triple, height) == profile),
        None,
    )


def status(profile: Profile) -> str:
    if profile == (0,) * 7:
        return "zero"
    if profile in HOLES:
        return "hole"
    height = max(profile)
    if height == 1 and profile not in CUTS:
        return "small-one"
    if height == 2 and profile not in DIMENSION_FOUR:
        return "small-two"
    if e_witness(profile) is not None:
        return "E"
    return "sharp"


def simplex_matrix(simplex: tuple[int, ...]) -> tuple[sp.Matrix, tuple[Profile, ...]]:
    generators = tuple(scaled_ray(RAYS[index]) for index in simplex)
    return sp.Matrix.hstack(*(sp.Matrix(generator) for generator in generators)), generators


def main() -> set[Profile]:
    simplices = pulling(tuple(range(len(RAYS))))
    determinant_distribution: Counter[int] = Counter()
    residue_occurrences: Counter[str] = Counter()
    transition_counts: Counter[str] = Counter()
    required_sharp_bases: set[Profile] = set()
    residue_union: set[Profile] = set()

    for ray in RAYS:
        scaled = scaled_ray(ray)
        assert status(scaled) == "sharp", (ray, scaled, status(scaled))
        required_sharp_bases.add(scaled)

    for simplex in simplices:
        matrix, generators = simplex_matrix(simplex)
        determinant_distribution[abs(int(matrix.det()))] += 1
        simplex_residues = residues(matrix)
        residue_union.update(simplex_residues)
        for residue in simplex_residues:
            residue_status = status(residue)
            residue_occurrences[residue_status] += 1
            assert residue_status in {"zero", "sharp", "hole", "small-one", "small-two"}
            if residue_status == "sharp":
                required_sharp_bases.add(residue)
                continue
            if residue_status == "zero":
                continue

            if residue_status == "hole":
                owners = singleton_owners(residue)
                for generator in generators:
                    successor = add(residue, generator)
                    successor_status = status(successor)
                    if successor_status == "hole":
                        common = owners.intersection(singleton_owners(successor))
                        assert common
                        assert any(generator in CUTS and generator[owner] == 1 for owner in common)
                        transition_counts["hole-preserving"] += 1
                    else:
                        assert successor_status == "sharp", (residue, generator, successor_status)
                        required_sharp_bases.add(successor)
                        transition_counts["hole-resolving"] += 1
                continue

            if residue_status == "small-two":
                for generator in generators:
                    successor = add(residue, generator)
                    assert status(successor) == "sharp", (residue, generator, status(successor))
                    required_sharp_bases.add(successor)
                    transition_counts["small-two-resolving"] += 1
                continue

            special_generators = []
            for generator in generators:
                successor = add(residue, generator)
                successor_status = status(successor)
                if successor_status == "sharp":
                    required_sharp_bases.add(successor)
                    transition_counts["small-one-resolving"] += 1
                else:
                    assert successor_status == "small-two", (
                        residue, generator, successor_status,
                    )
                    special_generators.append(generator)
                    transition_counts["small-one-to-small-two"] += 1

            for special in special_generators:
                first_e = add(residue, multiply(2, special))
                triple = e_witness(first_e)
                assert triple is not None
                assert first_e == e_profile(triple, 3)
                assert special == add(e_profile(triple, 4), multiply(-1, first_e))
                for other in generators:
                    if other == special:
                        continue
                    mixed = add(residue, special, other)
                    assert status(mixed) == "sharp", (
                        residue, special, other, status(mixed),
                    )
                    required_sharp_bases.add(mixed)
                    transition_counts["E-ray-resolving"] += 1

    assert len(simplices) == 81
    assert determinant_distribution == Counter({16: 36, 8: 24, 24: 18, 48: 3})
    assert len(residue_union) == 226
    assert max(max(profile) for profile in residue_union) == 6
    assert max(max(profile) for profile in required_sharp_bases) <= 6

    print(
        f"simplices={len(simplices)} determinants={dict(sorted(determinant_distribution.items()))} "
        f"residue_union={len(residue_union)} required_sharp_bases={len(required_sharp_bases)}"
    )
    print("residue_occurrences=", dict(sorted(residue_occurrences.items())))
    print("transitions=", dict(sorted(transition_counts.items())))
    print(
        "PASS every chamber lattice point reduces to a height-at-most-six sharp base, "
        "a listed ungraded hole, a small height-one/two exception, or the E_t family"
    )
    return required_sharp_bases


if __name__ == "__main__":
    main()
