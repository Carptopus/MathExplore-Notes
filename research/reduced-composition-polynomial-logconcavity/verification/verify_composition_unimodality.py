"""Exact destructive checks for reduced composition-polynomial coefficients.

The proof candidate identifies the coefficient vector, up to a positive scalar,
with one column of a B-spline knot-refinement matrix.  These computations do not
replace the variation-diminishing proof; they check the coefficient formula and
search systematically for boundary failures in unimodality and log-concavity.
"""

from __future__ import annotations

import argparse
import math
import random
from collections.abc import Iterable, Sequence

import numpy as np
from scipy.interpolate import BSpline


def compositions(total: int) -> Iterable[tuple[int, ...]]:
    """Yield every composition of ``total`` exactly once."""

    if total == 1:
        yield (1,)
        return
    for mask in range(1 << (total - 1)):
        parts: list[int] = []
        previous = 0
        for cut in range(1, total):
            if mask & (1 << (cut - 1)):
                parts.append(cut - previous)
                previous = cut
        parts.append(total - previous)
        yield tuple(parts)


def scaled_coefficients(parts: Sequence[int]) -> list[int]:
    """Return a common positive integer scaling of Ardila--Doker's coefficients."""

    partial_sums = [0]
    for part in parts:
        partial_sums.append(partial_sums[-1] + part)

    length = len(parts)
    size = partial_sums[-1]
    barycentric_denominators = [
        math.prod(abs(other - knot) for other in partial_sums if other != knot)
        for knot in partial_sums
    ]
    common_denominator = math.lcm(*barycentric_denominators)

    coefficients: list[int] = []
    for index in range(size - length + 1):
        value = 0
        for knot_index, knot in enumerate(partial_sums):
            if knot <= index:
                value += (
                    (-1) ** knot_index
                    * (common_denominator // barycentric_denominators[knot_index])
                    * math.comb(length + index - knot - 1, length - 1)
                )
        coefficients.append(value)
    return coefficients


def is_unimodal(values: Sequence[int]) -> bool:
    cursor = 1
    while cursor < len(values) and values[cursor - 1] <= values[cursor]:
        cursor += 1
    while cursor < len(values) and values[cursor - 1] >= values[cursor]:
        cursor += 1
    return cursor == len(values)


def is_log_concave(values: Sequence[int]) -> bool:
    return all(
        values[index] * values[index]
        >= values[index - 1] * values[index + 1]
        for index in range(1, len(values) - 1)
    )


def random_composition(rng: random.Random, size: int, length: int) -> tuple[int, ...]:
    cuts = sorted(rng.sample(range(1, size), length - 1))
    previous = 0
    parts: list[int] = []
    for cut in [*cuts, size]:
        parts.append(cut - previous)
        previous = cut
    return tuple(parts)


def check(parts: Sequence[int]) -> tuple[bool, bool, bool]:
    coefficients = scaled_coefficients(parts)
    positive = all(value > 0 for value in coefficients)
    return positive, is_unimodal(coefficients), is_log_concave(coefficients)


def scipy_refinement_coefficients(parts: Sequence[int]) -> list[float]:
    """Independently obtain the relevant knot-refinement column with SciPy."""

    length = len(parts)
    degree = length - 1
    size = sum(parts)
    partial_sums = [0]
    for part in parts:
        partial_sums.append(partial_sums[-1] + part)

    left_extension = list(range(-length, 0))
    right_extension = list(range(size + 1, size + length + 1))
    coarse_knots = np.asarray(
        [*left_extension, *partial_sums, *right_extension], dtype=float
    )
    coefficients = np.zeros(len(coarse_knots) - degree - 1)
    coefficients[len(left_extension)] = 1.0
    spline = BSpline(coarse_knots, coefficients, degree, extrapolate=False)

    for knot in range(1, size):
        if knot not in partial_sums:
            spline = spline.insert_knot(knot)

    refined: list[float] = []
    for index in range(size - length + 1):
        local_knots = np.arange(index, index + length + 1, dtype=float)
        matches = [
            basis_index
            for basis_index in range(len(spline.c))
            if basis_index + length + 1 <= len(spline.t)
            and np.array_equal(
                spline.t[basis_index : basis_index + length + 1], local_knots
            )
        ]
        if len(matches) != 1:
            raise AssertionError(
                f"unit-grid basis index is not unique: parts={parts}, index={index}"
            )
        refined.append(float(spline.c[matches[0]]))
    return refined


def refinement_identity_holds(
    parts: Sequence[int], candidate: Sequence[int] | None = None
) -> bool:
    scaled = list(candidate) if candidate is not None else scaled_coefficients(parts)
    denominator_scale = max(scaled)
    # The exact vector and the refinement vector are each known only up to a
    # positive common scale here.  Normalize by their maxima before comparing.
    exact = np.asarray(scaled, dtype=float) / denominator_scale
    refined = np.asarray(scipy_refinement_coefficients(parts), dtype=float)
    refined /= refined.max()
    return bool(np.allclose(exact, refined, rtol=1e-12, atol=1e-12))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exhaustive-size", type=int, default=16)
    parser.add_argument("--random-samples", type=int, default=10_000)
    parser.add_argument("--max-random-size", type=int, default=300)
    parser.add_argument("--max-random-length", type=int, default=40)
    parser.add_argument("--refinement-samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=460046)
    args = parser.parse_args()

    counts = {
        "tested": 0,
        "positive_failures": 0,
        "unimodal_failures": 0,
        "log_concave_failures": 0,
        "refinement_identity_failures": 0,
    }
    unique_compositions: set[tuple[int, ...]] = set()
    unique_refinement_samples: set[tuple[int, ...]] = set()
    first_failure: tuple[tuple[int, ...], tuple[bool, bool, bool]] | None = None

    def record(parts: tuple[int, ...]) -> None:
        nonlocal first_failure
        result = check(parts)
        counts["tested"] += 1
        unique_compositions.add(parts)
        for key, passed in zip(
            ("positive_failures", "unimodal_failures", "log_concave_failures"),
            result,
            strict=True,
        ):
            if not passed:
                counts[key] += 1
        if first_failure is None and not all(result):
            first_failure = (parts, result)

    for size in range(1, args.max_exhaustive_size + 1):
        for parts in compositions(size):
            record(parts)

    rng = random.Random(args.seed)
    for _ in range(args.random_samples):
        size = rng.randint(2, args.max_random_size)
        length = rng.randint(1, min(args.max_random_length, size))
        record(random_composition(rng, size, length))

    for _ in range(args.refinement_samples):
        size = rng.randint(2, min(args.max_random_size, 80))
        length = rng.randint(1, min(args.max_random_length, size, 15))
        parts = random_composition(rng, size, length)
        unique_refinement_samples.add(parts)
        if not refinement_identity_holds(parts):
            counts["refinement_identity_failures"] += 1
            if first_failure is None:
                first_failure = (parts, (True, True, True))

    negative_controls = [
        ((2, 3), list(reversed(scaled_coefficients((2, 3))))),
        ((1, 4, 2), [0, *scaled_coefficients((1, 4, 2))[:-1]]),
    ]
    negative_controls_passed = sum(
        not refinement_identity_holds(parts, corrupted)
        for parts, corrupted in negative_controls
    )

    print(f"COMPOSITIONS_TESTED {counts['tested']}")
    print(f"UNIQUE_COMPOSITIONS_TESTED {len(unique_compositions)}")
    print(f"POSITIVE_FAILURES {counts['positive_failures']}")
    print(f"UNIMODAL_FAILURES {counts['unimodal_failures']}")
    print(f"LOG_CONCAVE_FAILURES {counts['log_concave_failures']}")
    print(f"REFINEMENT_IDENTITY_FAILURES {counts['refinement_identity_failures']}")
    print(f"UNIQUE_REFINEMENT_SAMPLES {len(unique_refinement_samples)}")
    print(f"NEGATIVE_CONTROLS_PASSED {negative_controls_passed}")
    if first_failure is not None:
        print(f"FIRST_FAILURE {first_failure}")
    if (
        counts["positive_failures"]
        or counts["unimodal_failures"]
        or counts["log_concave_failures"]
        or counts["refinement_identity_failures"]
        or negative_controls_passed != len(negative_controls)
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
