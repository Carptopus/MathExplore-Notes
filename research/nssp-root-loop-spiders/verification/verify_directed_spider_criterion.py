# AI-assisted generation and review: OpenAI Codex. Responsible maintainer: Carptopus.
"""Destructive calibration for arbitrary directed rooted-spider matrices.

All sampled matrices have a single nonzero root loop, zero diagonal elsewhere,
and two independently chosen nonzero integer weights on every tree edge.
The script compares full nSSP verification rank modulo a prime with exact
pairwise coprimality over Q of the directed arm characteristic polynomials.

A modular rank loss is only a counterexample candidate. A modular full rank
proves full rank over Q/R for that displayed integer matrix.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from fractions import Fraction


PRIME = 1_000_003


def trim(poly: list[Fraction]) -> list[Fraction]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    size = max(len(left), len(right))
    return trim([
        (left[i] if i < len(left) else Fraction(0))
        + (right[i] if i < len(right) else Fraction(0))
        for i in range(size)
    ])


def scale(poly: list[Fraction], value: Fraction) -> list[Fraction]:
    return trim([value * coefficient for coefficient in poly])


def divide_with_remainder(
    dividend: list[Fraction], divisor: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    remainder = trim(dividend[:])
    divisor = trim(divisor[:])
    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and remainder != [0]:
        degree = len(remainder) - len(divisor)
        factor = remainder[-1] / divisor[-1]
        quotient[degree] += factor
        for i, coefficient in enumerate(divisor):
            remainder[i + degree] -= factor * coefficient
        trim(remainder)
    return trim(quotient), trim(remainder)


def gcd(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    left, right = trim(left[:]), trim(right[:])
    while right != [0]:
        _, remainder = divide_with_remainder(left, right)
        left, right = right, remainder
    return scale(left, Fraction(1, 1) / left[-1]) if left != [0] else [Fraction(0)]


def path_polynomial(products: tuple[int, ...], vertices: int) -> list[Fraction]:
    if vertices == 0:
        return [Fraction(1)]
    previous = [Fraction(1)]
    current = [Fraction(0), Fraction(1)]
    for vertex in range(2, vertices + 1):
        beta = Fraction(products[vertex - 2])
        following = add([Fraction(0)] + current, scale(previous, -beta))
        previous, current = current, following
    return current


def arm_polynomials(
    lengths: tuple[int, ...],
    forward: tuple[tuple[int, ...], ...],
    backward: tuple[tuple[int, ...], ...],
) -> list[list[Fraction]]:
    result: list[list[Fraction]] = []
    for length, upper, lower in zip(lengths, forward, backward):
        internal_products = tuple(
            upper[i] * lower[i] for i in range(1, length)
        )
        result.append(path_polynomial(internal_products, length))
    return result


def pairwise_coprime(polys: list[list[Fraction]]) -> bool:
    return all(
        len(gcd(polys[i], polys[j])) == 1
        for i in range(len(polys))
        for j in range(i + 1, len(polys))
    )


def build_matrix(
    lengths: tuple[int, ...],
    forward: tuple[tuple[int, ...], ...],
    backward: tuple[tuple[int, ...], ...],
) -> list[list[int]]:
    n = 1 + sum(lengths)
    matrix = [[0] * n for _ in range(n)]
    matrix[0][0] = 1
    cursor = 1
    for length, upper, lower in zip(lengths, forward, backward):
        parent = 0
        for offset in range(length):
            child = cursor + offset
            matrix[parent][child] = upper[offset]
            matrix[child][parent] = lower[offset]
            parent = child
        cursor += length
    return matrix


def verification_matrix(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    variables = [(i, j) for i in range(n) for j in range(n) if matrix[i][j] == 0]
    result: list[list[int]] = []
    for row in range(n):
        for column in range(n):
            equation: list[int] = []
            for i, j in variables:
                coefficient = matrix[row][j] if column == i else 0
                if row == j:
                    coefficient -= matrix[i][column]
                equation.append(coefficient)
            result.append(equation)
    return result


def rank_mod_prime(matrix: list[list[int]], prime: int = PRIME) -> int:
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [value * inverse % prime for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (work[row][j] - factor * work[rank][j]) % prime
                for j in range(columns)
            ]
        rank += 1
        if rank == columns:
            break
    return rank


def rank_over_q(matrix: list[list[int]]) -> int:
    """Exact Fraction elimination, used only on the targeted controls."""
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][j] - factor * work[rank][j]
                for j in range(columns)
            ]
        rank += 1
        if rank == columns:
            break
    return rank


def nonzero(rng: random.Random) -> int:
    return rng.choice((-3, -2, -1, 1, 2, 3))


def directed_weights(
    lengths: tuple[int, ...], rng: random.Random
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    forward = tuple(tuple(nonzero(rng) for _ in range(length)) for length in lengths)
    backward = tuple(tuple(nonzero(rng) for _ in range(length)) for length in lengths)
    return forward, backward


def targeted_cases() -> list[tuple[str, tuple[int, ...], tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]]:
    # Products on the length-four arm are (1,-4,1), so its polynomial is
    # (x^2+1)^2. It is coprime to x^2-2 and x^2-3 despite the internal root.
    repeated = (
        "internal_repeated_complex_roots",
        (2, 2, 4),
        ((1, 1), (1, 1), (1, 1, 1, 1)),
        ((1, 2), (1, 3), (1, 1, -4, 1)),
    )
    collision = (
        "shared_nonzero_arm_factor",
        (2, 2, 4),
        ((1, 1), (1, 1), (1, 1, 1, 1)),
        ((1, 2), (1, 2), (1, 1, -4, 1)),
    )
    two_odd = (
        "shared_zero_factor",
        (1, 3, 4),
        ((2,), (1, 1, 1), (1, 1, 1, 1)),
        ((-3,), (1, 2, -1), (1, -1, 2, -2)),
    )
    repeated_same_products_new_split = (
        "internal_repeated_roots_same_products_new_split",
        (2, 2, 4),
        ((-1, 2), (-1, -3), (-1, -1, 2, -1)),
        ((-1, 1), (-1, -1), (-1, -1, -2, -1)),
    )
    shared_complex = (
        "shared_complex_arm_factor",
        (1, 2, 2),
        ((2,), (1, 1), (1, 1)),
        ((-3,), (1, -1), (1, -1)),
    )
    return [
        repeated,
        repeated_same_products_new_split,
        collision,
        shared_complex,
        two_odd,
    ]


def evaluate(
    label: str,
    lengths: tuple[int, ...],
    forward: tuple[tuple[int, ...], ...],
    backward: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    matrix = build_matrix(lengths, forward, backward)
    polys = arm_polynomials(lengths, forward, backward)
    coprime = pairwise_coprime(polys)
    verification = verification_matrix(matrix)
    rank = rank_mod_prime(verification)
    columns = (len(matrix) - 1) ** 2
    return {
        "label": label,
        "lengths": lengths,
        "forward": forward,
        "backward": backward,
        "arm_polynomials_low_to_high": [
            [str(value) for value in poly] for poly in polys
        ],
        "pairwise_coprime": coprime,
        "verification_rank": rank,
        "verification_columns": columns,
        "nssp_full_mod_prime": rank == columns,
        "positive_modular_rank_loss_candidate": coprime and rank < columns,
        "negative_modular_full_rank_counterexample": not coprime and rank == columns,
        "exact_rank_over_q": rank_over_q(verification)
        if label.startswith(("internal_", "shared_"))
        else None,
    }


def run(max_vertices: int, samples: int) -> dict[str, object]:
    rng = random.Random(20260819)
    cases = [evaluate(*case) for case in targeted_cases()]
    for arms in (3, 4):
        for lengths in itertools.product(range(1, max_vertices), repeat=arms):
            if tuple(sorted(lengths)) != lengths or 1 + sum(lengths) > max_vertices:
                continue
            for sample in range(samples):
                forward, backward = directed_weights(lengths, rng)
                cases.append(evaluate(f"random_{arms}_{sample}", lengths, forward, backward))
    coprime_cases = [case for case in cases if case["pairwise_coprime"]]
    noncoprime_cases = [case for case in cases if not case["pairwise_coprime"]]
    positive_rank_loss_candidates = [
        case for case in cases if case["positive_modular_rank_loss_candidate"]
    ]
    negative_full_rank_counterexamples = [
        case for case in cases if case["negative_modular_full_rank_counterexample"]
    ]
    return {
        "prime": PRIME,
        "max_vertices": max_vertices,
        "samples_per_shape": samples,
        "total": len(cases),
        "coprime": len(coprime_cases),
        "coprime_full": sum(bool(case["nssp_full_mod_prime"]) for case in coprime_cases),
        "noncoprime": len(noncoprime_cases),
        "noncoprime_full": sum(bool(case["nssp_full_mod_prime"]) for case in noncoprime_cases),
        "coprime_modular_rank_loss_candidate_count": len(positive_rank_loss_candidates),
        "first_coprime_modular_rank_loss_candidate": (
            positive_rank_loss_candidates[0] if positive_rank_loss_candidates else None
        ),
        "noncoprime_modular_full_rank_counterexample_count": (
            len(negative_full_rank_counterexamples)
        ),
        "first_noncoprime_modular_full_rank_counterexample": (
            negative_full_rank_counterexamples[0]
            if negative_full_rank_counterexamples
            else None
        ),
        "targeted": cases[:len(targeted_cases())],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-vertices", type=int, default=10)
    parser.add_argument("--samples", type=int, default=8)
    args = parser.parse_args()
    print(json.dumps(run(args.max_vertices, args.samples), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
