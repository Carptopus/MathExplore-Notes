"""Independent bounded checks for the parallel-support theorem.

The checks cover the exact activity-block formula, the final inequality and
equality controls, representative deletion--contraction interfaces, and both
rank-(r-2) counterexamples. All failures are explicit, so ``python -O`` does
not disable any check. These finite computations do not prove the theorem.
"""

from __future__ import annotations

from itertools import combinations
from random import Random


def require(condition: bool, payload: object) -> None:
    if not condition:
        raise RuntimeError(payload)


def binary_rank(columns: tuple[int, ...] | list[int]) -> int:
    pivots: dict[int, int] = {}
    for value in columns:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in pivots:
                x ^= pivots[pivot]
            else:
                pivots[pivot] = x
                break
    return len(pivots)


def class_level_values(
    skeleton: tuple[int, ...], multiplicities: tuple[int, ...]
) -> tuple[int, int]:
    rank = binary_rank(skeleton)
    cyclic = 0
    bases = 0
    size = len(skeleton)
    for mask in range(1 << size):
        chosen = tuple(skeleton[i] for i in range(size) if mask >> i & 1)
        chosen_rank = binary_rank(chosen)
        weight_nonempty = 1
        weight_basis = 1
        for i in range(size):
            if mask >> i & 1:
                weight_nonempty *= 2 ** multiplicities[i] - 1
                weight_basis *= multiplicities[i]
        cyclic += (-1) ** (rank - chosen_rank) * weight_nonempty
        if chosen_rank == rank and len(chosen) == rank:
            bases += weight_basis
    return cyclic, bases


def uniform_class_level_values(
    rank: int, multiplicities: tuple[int, ...]
) -> tuple[int, int]:
    cyclic = 0
    bases = 0
    size = len(multiplicities)
    for mask in range(1 << size):
        chosen_count = mask.bit_count()
        chosen_rank = min(chosen_count, rank)
        weight_nonempty = 1
        weight_basis = 1
        for i, multiplicity in enumerate(multiplicities):
            if mask >> i & 1:
                weight_nonempty *= 2**multiplicity - 1
                weight_basis *= multiplicity
        cyclic += (-1) ** (rank - chosen_rank) * weight_nonempty
        if chosen_count == rank:
            bases += weight_basis
    return cyclic, bases


def coloopless_skeleton(skeleton: tuple[int, ...]) -> bool:
    rank = binary_rank(skeleton)
    return all(
        binary_rank(skeleton[:i] + skeleton[i + 1 :]) == rank
        for i in range(len(skeleton))
    )


def expanded_columns(
    skeleton: tuple[int, ...], multiplicities: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(
        column
        for column, multiplicity in zip(skeleton, multiplicities, strict=True)
        for _ in range(multiplicity)
    )


def subset_values_from_rank_table(rank_table: tuple[int, ...]) -> tuple[int, int]:
    size = (len(rank_table) - 1).bit_length()
    require(len(rank_table) == 1 << size, ("bad rank table", len(rank_table)))
    full_rank = rank_table[-1]
    cyclic = 0
    bases = 0
    for mask, subset_rank in enumerate(rank_table):
        cyclic += (-1) ** (full_rank - subset_rank)
        if mask.bit_count() == full_rank and subset_rank == full_rank:
            bases += 1
    return cyclic, bases


def column_rank_table(columns: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        binary_rank(tuple(columns[i] for i in range(len(columns)) if mask >> i & 1))
        for mask in range(1 << len(columns))
    )


def deletion_rank_table(columns: tuple[int, ...], element: int) -> tuple[int, ...]:
    return column_rank_table(columns[:element] + columns[element + 1 :])


def contraction_rank_table(columns: tuple[int, ...], element: int) -> tuple[int, ...]:
    remaining = tuple(i for i in range(len(columns)) if i != element)
    element_rank = binary_rank((columns[element],))
    table: list[int] = []
    for mask in range(1 << len(remaining)):
        chosen = [columns[element]]
        chosen.extend(
            columns[remaining[i]] for i in range(len(remaining)) if mask >> i & 1
        )
        table.append(binary_rank(chosen) - element_rank)
    return tuple(table)


def matroid_profile(rank_table: tuple[int, ...]) -> dict[str, int | bool]:
    size = (len(rank_table) - 1).bit_length()
    require(len(rank_table) == 1 << size, ("bad profile rank table", len(rank_table)))
    full_rank = rank_table[-1]
    full_mask = (1 << size) - 1
    loopless = all(rank_table[1 << i] == 1 for i in range(size))
    coloopless = all(
        rank_table[full_mask ^ (1 << i)] == full_rank for i in range(size)
    )
    parallel_support_mask = 0
    singleton_classes = 0
    unseen = set(range(size))
    while unseen:
        first = min(unseen)
        parallel_class = {
            other
            for other in unseen
            if rank_table[(1 << first) | (1 << other)] == 1
        }
        if len(parallel_class) >= 2:
            for element in parallel_class:
                parallel_support_mask |= 1 << element
        else:
            singleton_classes += 1
        unseen -= parallel_class
    return {
        "rank": full_rank,
        "loopless": loopless,
        "coloopless": coloopless,
        "parallel_support_rank": rank_table[parallel_support_mask],
        "singleton_classes": singleton_classes,
    }


def skeleton_activities(
    skeleton: tuple[int, ...], basis: tuple[int, ...]
) -> tuple[set[int], set[int]]:
    rank = len(basis)
    basis_set = set(basis)
    outside = tuple(i for i in range(len(skeleton)) if i not in basis_set)
    internal = {
        b
        for b in basis
        if not any(
            e < b
            and binary_rank(
                tuple(skeleton[i] for i in basis if i != b) + (skeleton[e],)
            )
            == rank
            for e in outside
        )
    }
    external = {
        e
        for e in outside
        if not any(
            b < e
            and binary_rank(
                tuple(skeleton[i] for i in basis if i != b) + (skeleton[e],)
            )
            == rank
            for b in basis
        )
    }
    return internal, external


def formula_block_value(
    skeleton: tuple[int, ...],
    multiplicities: tuple[int, ...],
    basis: tuple[int, ...],
) -> tuple[int, int]:
    internal, external = skeleton_activities(skeleton, basis)
    cyclic = 2 ** sum(multiplicities[e] for e in external)
    for e in basis:
        cyclic *= 2 ** multiplicities[e] - (2 if e in internal else 1)
    bases = 1
    for e in basis:
        bases *= multiplicities[e]
    return cyclic, bases


def explicit_activity_blocks(
    skeleton: tuple[int, ...], multiplicities: tuple[int, ...]
) -> dict[tuple[int, ...], tuple[int, int]]:
    columns = expanded_columns(skeleton, multiplicities)
    class_of: list[int] = []
    for class_index, multiplicity in enumerate(multiplicities):
        class_of.extend([class_index] * multiplicity)
    rank = binary_rank(columns)
    totals: dict[tuple[int, ...], list[int]] = {}
    for lifted_basis in combinations(range(len(columns)), rank):
        if binary_rank(tuple(columns[i] for i in lifted_basis)) != rank:
            continue
        basis_set = set(lifted_basis)
        outside = tuple(i for i in range(len(columns)) if i not in basis_set)
        internal = {
            b
            for b in lifted_basis
            if not any(
                e < b
                and binary_rank(
                    tuple(columns[i] for i in lifted_basis if i != b) + (columns[e],)
                )
                == rank
                for e in outside
            )
        }
        external = {
            e
            for e in outside
            if not any(
                b < e
                and binary_rank(
                    tuple(columns[i] for i in lifted_basis if i != b) + (columns[e],)
                )
                == rank
                for b in lifted_basis
            )
        }
        projected = tuple(sorted(class_of[i] for i in lifted_basis))
        block = totals.setdefault(projected, [0, 0])
        if not internal:
            block[0] += 2 ** len(external)
        block[1] += 1
    return {basis: (values[0], values[1]) for basis, values in totals.items()}


def activity_formula_checks() -> tuple[int, int]:
    checked_instances = 0
    checked_blocks = 0
    patterns = ((1, 2, 3), (2, 1, 2), (3, 2, 1), (2, 3, 2))
    for rank in (2, 3):
        universe = tuple(range(1, 1 << rank))
        for size in range(rank, min(rank + 2, len(universe)) + 1):
            for skeleton in combinations(universe, size):
                if binary_rank(skeleton) != rank:
                    continue
                for seed in patterns:
                    multiplicities = tuple(seed[i % len(seed)] for i in range(size))
                    actual = explicit_activity_blocks(skeleton, multiplicities)
                    for basis, value in actual.items():
                        expected = formula_block_value(skeleton, multiplicities, basis)
                        require(
                            value == expected,
                            ("activity formula", skeleton, multiplicities, basis, value, expected),
                        )
                        checked_blocks += 1
                    require(
                        tuple(map(sum, zip(*actual.values(), strict=True)))
                        == class_level_values(skeleton, multiplicities),
                        ("activity total", skeleton, multiplicities),
                    )
                    checked_instances += 1
    return checked_instances, checked_blocks


def exhaustive_small() -> tuple[int, int]:
    checked = 0
    strict_checked = 0
    for rank in (2, 3):
        universe = tuple(range(1, 1 << rank))
        for size in range(rank, len(universe) + 1):
            for skeleton in combinations(universe, size):
                if binary_rank(skeleton) != rank or not coloopless_skeleton(skeleton):
                    continue
                for support_mask in range(1 << size):
                    support = tuple(
                        skeleton[i] for i in range(size) if support_mask >> i & 1
                    )
                    support_rank = binary_rank(support)
                    if support_rank < rank - 1:
                        continue
                    multiplicities = tuple(
                        2 if support_mask >> i & 1 else 1 for i in range(size)
                    )
                    cyclic, bases = class_level_values(skeleton, multiplicities)
                    require(
                        cyclic >= bases,
                        ("theorem", rank, skeleton, multiplicities, cyclic, bases),
                    )
                    if support_rank == rank - 1:
                        require(
                            cyclic > bases,
                            ("corank-one strictness", skeleton, multiplicities, cyclic, bases),
                        )
                        strict_checked += 1
                    checked += 1
    return checked, strict_checked


def varied_multiplicity_samples() -> int:
    rng = Random(20260904)
    checked = 0
    for rank in (3, 4, 5):
        universe = tuple(range(1, 1 << rank))
        for _ in range(500):
            size = rng.randint(rank + 1, min(rank + 5, len(universe)))
            skeleton = tuple(sorted(rng.sample(universe, size)))
            if binary_rank(skeleton) != rank or not coloopless_skeleton(skeleton):
                continue
            multiplicities = tuple(rng.randint(1, 4) for _ in skeleton)
            support = tuple(
                element
                for element, multiplicity in zip(skeleton, multiplicities, strict=True)
                if multiplicity >= 2
            )
            support_rank = binary_rank(support)
            if support_rank < rank - 1:
                continue
            cyclic, bases = class_level_values(skeleton, multiplicities)
            require(
                cyclic >= bases,
                ("sample theorem", rank, skeleton, multiplicities, cyclic, bases),
            )
            if support_rank == rank - 1:
                require(
                    cyclic > bases,
                    ("sample strictness", rank, skeleton, multiplicities, cyclic, bases),
                )
            checked += 1
    return checked


def uniform_nonbinary_samples() -> int:
    rng = Random(20260905)
    checked = 0
    for rank in range(2, 6):
        for size in range(rank + 1, rank + 6):
            for _ in range(100):
                multiplicities = tuple(rng.randint(1, 4) for _ in range(size))
                if sum(value >= 2 for value in multiplicities) < rank - 1:
                    continue
                cyclic, bases = uniform_class_level_values(rank, multiplicities)
                require(cyclic >= bases, ("uniform", rank, multiplicities, cyclic, bases))
                checked += 1
    return checked


def deletion_contraction_checks() -> dict[str, int]:
    checked = 0
    examples = (
        ("spanning-singleton", (1, 2, 3), (2, 2, 1), 4, (2, 2, 1)),
        ("inside-hyperplane", (1, 2, 3, 4, 7), (2, 2, 1, 1, 1), 4, (2, 2, 1)),
        ("outside-hyperplane", (1, 2, 4, 5, 6), (2, 2, 1, 1, 1), 4, (2, 2, 2)),
    )
    branch_counts: dict[str, int] = {}
    for label, skeleton, multiplicities, element, support_ranks in examples:
        columns = expanded_columns(skeleton, multiplicities)
        require(
            columns[element] not in columns[:element] + columns[element + 1 :],
            ("chosen element is not singleton", skeleton, multiplicities, element),
        )
        whole_table = column_rank_table(columns)
        deletion_table = deletion_rank_table(columns, element)
        contraction_table = contraction_rank_table(columns, element)
        whole = subset_values_from_rank_table(whole_table)
        deletion = subset_values_from_rank_table(deletion_table)
        contraction = subset_values_from_rank_table(contraction_table)
        require(
            whole == tuple(a + b for a, b in zip(deletion, contraction, strict=True)),
            ("deletion-contraction", skeleton, multiplicities, whole, deletion, contraction),
        )
        profiles = tuple(
            matroid_profile(table)
            for table in (whole_table, deletion_table, contraction_table)
        )
        for name, profile in zip(("whole", "deletion", "contraction"), profiles, strict=True):
            require(profile["loopless"], (label, name, "loop", profile))
            require(profile["coloopless"], (label, name, "coloop", profile))
            require(
                profile["parallel_support_rank"] >= profile["rank"] - 1,
                (label, name, "support condition", profile),
            )
        old_support = {
            index
            for index, class_index in enumerate(
                class_index
                for class_index, multiplicity in enumerate(multiplicities)
                for _ in range(multiplicity)
            )
            if multiplicities[class_index] >= 2
        }
        remaining = tuple(i for i in range(len(columns)) if i != element)
        old_support_masks = (
            sum(1 << i for i in old_support),
            sum(1 << new for new, old in enumerate(remaining) if old in old_support),
            sum(1 << new for new, old in enumerate(remaining) if old in old_support),
        )
        old_support_ranks = tuple(
            table[mask]
            for table, mask in zip(
                (whole_table, deletion_table, contraction_table),
                old_support_masks,
                strict=True,
            )
        )
        require(
            old_support_ranks == support_ranks,
            (label, "unexpected old-support ranks", old_support_ranks, profiles),
        )
        require(
            profiles[1]["singleton_classes"] < profiles[0]["singleton_classes"],
            (label, "deletion did not reduce singleton classes", profiles),
        )
        if label == "inside-hyperplane":
            require(
                profiles[1]["parallel_support_rank"] == profiles[1]["rank"] - 1
                and profiles[2]["parallel_support_rank"] >= profiles[2]["rank"] - 1,
                (label, "wrong induction layers", profiles),
            )
        if label == "outside-hyperplane":
            require(
                profiles[1]["parallel_support_rank"] == profiles[1]["rank"] - 1
                and profiles[2]["parallel_support_rank"] == profiles[2]["rank"],
                (label, "wrong deletion/spanning layers", profiles),
            )
        checked += 1
        branch_counts[label] = branch_counts.get(label, 0) + 1
    require(checked == len(examples), ("missing induction branch", branch_counts))
    return branch_counts


def equality_controls() -> tuple[int, int]:
    positive = 0
    destructive = 0
    for rank in range(1, 6):
        skeleton = tuple(1 << i for i in range(rank))
        equality = class_level_values(skeleton, (2,) * rank)
        require(equality[0] == equality[1], ("equality control", rank, equality))
        positive += 1
        perturbed = class_level_values(skeleton, (3,) + (2,) * (rank - 1))
        require(
            perturbed[0] > perturbed[1],
            ("equality destructive control", rank, perturbed),
        )
        destructive += 1
    return positive, destructive


def connected_matroid(columns: tuple[int, ...]) -> bool:
    rank = binary_rank(columns)
    full_mask = (1 << len(columns)) - 1
    for mask in range(1, full_mask):
        left = tuple(columns[i] for i in range(len(columns)) if mask >> i & 1)
        right = tuple(columns[i] for i in range(len(columns)) if not (mask >> i & 1))
        if binary_rank(left) + binary_rank(right) == rank:
            return False
    return True


def counterexample_controls() -> dict[str, tuple[int, int]]:
    # U_{2,3} direct-summed with U_{1,2}; heavy support has rank 1=r-2.
    disconnected = class_level_values((1, 2, 3, 4), (1, 1, 1, 2))
    require(disconnected == (4, 6), ("disconnected counterexample", disconnected))

    # Binary columns [1,1,2,4,7] represent a four-cycle with one doubled edge.
    connected_columns = (1, 1, 2, 4, 7)
    connected = subset_values_from_rank_table(column_rank_table(connected_columns))
    require(connected == (6, 7), ("connected counterexample", connected))
    require(connected_matroid(connected_columns), "connected counterexample is disconnected")
    rank = binary_rank(connected_columns)
    has_series_pair = any(
        binary_rank(
            tuple(
                connected_columns[i]
                for i in range(len(connected_columns))
                if i not in pair
            )
        )
        < rank
        for pair in combinations(range(len(connected_columns)), 2)
    )
    require(has_series_pair, "connected counterexample unexpectedly cosimple")
    return {"disconnected": disconnected, "connected": connected}


def main() -> None:
    activity = activity_formula_checks()
    exact, strict = exhaustive_small()
    sampled = varied_multiplicity_samples()
    uniform = uniform_nonbinary_samples()
    interfaces = deletion_contraction_checks()
    equality = equality_controls()
    counterexamples = counterexample_controls()
    print(
        "PASS:",
        {
            "activity_formula_instances_and_blocks": activity,
            "exhaustive_binary_rank_2_3": exact,
            "corank_one_strictness_cases": strict,
            "varied_multiplicity_samples": sampled,
            "uniform_nonbinary_samples": uniform,
            "deletion_contraction_interfaces": interfaces,
            "equality_and_destructive_controls": equality,
            "rank_r_minus_2_counterexamples": counterexamples,
        },
    )


if __name__ == "__main__":
    main()
