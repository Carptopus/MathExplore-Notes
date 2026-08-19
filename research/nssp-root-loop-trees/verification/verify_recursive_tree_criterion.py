# AI-assisted generation and review: OpenAI Codex. Responsible maintainer: Carptopus.
"""Falsification calibration for the recursive rooted-tree nSSP criterion.

The candidate criterion says that a bidirected tree matrix with one nonzero
root loop has the nSSP exactly when, at every vertex, the characteristic
polynomials of its child subtrees are pairwise coprime.

Modular full rank proves full rank over Q/R for the displayed integer matrix.
Modular rank loss is only a counterexample candidate, so targeted negative
controls are also checked by exact Fraction elimination.
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


def multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return trim(result)


def product(polys: list[list[Fraction]]) -> list[Fraction]:
    result = [Fraction(1)]
    for poly in polys:
        result = multiply(result, poly)
    return result


def divide_with_remainder(
    dividend: list[Fraction], divisor: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    remainder = trim(dividend[:])
    divisor = trim(divisor[:])
    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and remainder != [Fraction(0)]:
        degree = len(remainder) - len(divisor)
        factor = remainder[-1] / divisor[-1]
        quotient[degree] += factor
        for index, coefficient in enumerate(divisor):
            remainder[index + degree] -= factor * coefficient
        trim(remainder)
    return trim(quotient), trim(remainder)


def gcd(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    left, right = trim(left[:]), trim(right[:])
    while right != [Fraction(0)]:
        _, remainder = divide_with_remainder(left, right)
        left, right = right, remainder
    if left == [Fraction(0)]:
        return left
    return scale(left, Fraction(1, 1) / left[-1])


def children_from_parent(parent: tuple[int, ...]) -> list[list[int]]:
    children = [[] for _ in range(len(parent) + 1)]
    for child, parent_vertex in enumerate(parent, start=1):
        children[parent_vertex].append(child)
    return children


def rooted_subtree_polynomials(
    parent: tuple[int, ...], edge_products: tuple[int, ...]
) -> tuple[list[list[Fraction]], list[list[Fraction]], list[list[int]]]:
    """Return F_v, Q_v and children, with coefficients low to high."""
    children = children_from_parent(parent)
    count = len(children)
    subtree = [[Fraction(0)] for _ in range(count)]
    deleted_root = [[Fraction(0)] for _ in range(count)]
    for vertex in range(count - 1, -1, -1):
        child_polys = [subtree[child] for child in children[vertex]]
        deleted_root[vertex] = product(child_polys)
        current = [Fraction(0)] + deleted_root[vertex]
        for child in children[vertex]:
            siblings = [
                subtree[other]
                for other in children[vertex]
                if other != child
            ]
            term = multiply(deleted_root[child], product(siblings))
            beta = Fraction(edge_products[child - 1])
            current = add(current, scale(term, -beta))
        subtree[vertex] = trim(current)
    return subtree, deleted_root, children


def recursive_coprime_status(
    subtree: list[list[Fraction]], children: list[list[int]]
) -> tuple[bool, list[dict[str, object]]]:
    violations: list[dict[str, object]] = []
    for vertex, child_vertices in enumerate(children):
        for left_index in range(len(child_vertices)):
            for right_index in range(left_index + 1, len(child_vertices)):
                left = child_vertices[left_index]
                right = child_vertices[right_index]
                common = gcd(subtree[left], subtree[right])
                if len(common) > 1:
                    violations.append({
                        "vertex": vertex,
                        "children": [left, right],
                        "gcd_low_to_high": [str(value) for value in common],
                    })
    return not violations, violations


def build_matrix(
    parent: tuple[int, ...],
    forward: tuple[int, ...],
    backward: tuple[int, ...],
) -> list[list[int]]:
    count = len(parent) + 1
    matrix = [[0] * count for _ in range(count)]
    matrix[0][0] = 1
    for child, parent_vertex in enumerate(parent, start=1):
        matrix[parent_vertex][child] = forward[child - 1]
        matrix[child][parent_vertex] = backward[child - 1]
    return matrix


def matrix_multiply(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    rows = len(left)
    middle = len(right)
    columns = len(right[0]) if right else 0
    return [
        [
            sum(
                (left[row][index] * right[index][column] for index in range(middle)),
                Fraction(0),
            )
            for column in range(columns)
        ]
        for row in range(rows)
    ]


def characteristic_polynomial(matrix: list[list[int]]) -> list[Fraction]:
    """Independent Newton-trace characteristic polynomial, low to high."""
    size = len(matrix)
    if size == 0:
        return [Fraction(1)]
    base = [[Fraction(value) for value in row] for row in matrix]
    power = [[Fraction(int(row == column)) for column in range(size)] for row in range(size)]
    coefficients_high = [Fraction(1)]
    traces = [Fraction(0)]
    for exponent in range(1, size + 1):
        power = matrix_multiply(power, base)
        traces.append(sum((power[index][index] for index in range(size)), Fraction(0)))
        coefficient = -sum(
            (
                coefficients_high[exponent - index] * traces[index]
                for index in range(1, exponent + 1)
            ),
            Fraction(0),
        ) / exponent
        coefficients_high.append(coefficient)
    return trim(list(reversed(coefficients_high)))


def subtree_vertex_sets(children: list[list[int]]) -> list[list[int]]:
    result = [[] for _ in children]
    for vertex in range(len(children) - 1, -1, -1):
        vertices = [vertex]
        for child in children[vertex]:
            vertices.extend(result[child])
        result[vertex] = vertices
    return result


def induced_matrix(matrix: list[list[int]], vertices: list[int]) -> list[list[int]]:
    return [[matrix[row][column] for column in vertices] for row in vertices]


def verification_matrix(matrix: list[list[int]]) -> list[list[int]]:
    count = len(matrix)
    variables = [
        (row, column)
        for row in range(count)
        for column in range(count)
        if matrix[row][column] == 0
    ]
    equations: list[list[int]] = []
    for row in range(count):
        for column in range(count):
            equation: list[int] = []
            for variable_row, variable_column in variables:
                coefficient = (
                    matrix[row][variable_column]
                    if column == variable_row
                    else 0
                )
                if row == variable_column:
                    coefficient -= matrix[variable_row][column]
                equation.append(coefficient)
            equations.append(equation)
    return equations


def rank_mod_prime(matrix: list[list[int]], prime: int = PRIME) -> int:
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]),
            None,
        )
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
                (work[row][index] - factor * work[rank][index]) % prime
                for index in range(columns)
            ]
        rank += 1
        if rank == columns:
            break
    return rank


def rank_over_q(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]),
            None,
        )
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
                work[row][index] - factor * work[rank][index]
                for index in range(columns)
            ]
        rank += 1
        if rank == columns:
            break
    return rank


def nonzero(rng: random.Random) -> int:
    return rng.choice((-3, -2, -1, 1, 2, 3))


def evaluate(
    label: str,
    parent: tuple[int, ...],
    forward: tuple[int, ...],
    backward: tuple[int, ...],
    exact: bool = False,
) -> dict[str, object]:
    edge_products = tuple(
        forward[index] * backward[index] for index in range(len(parent))
    )
    subtree, _, children = rooted_subtree_polynomials(parent, edge_products)
    recursive_coprime, violations = recursive_coprime_status(subtree, children)
    matrix = build_matrix(parent, forward, backward)
    verification = verification_matrix(matrix)
    columns = (len(matrix) - 1) ** 2
    rank = rank_mod_prime(verification)
    direct_match = None
    if exact:
        direct_matrix = [row[:] for row in matrix]
        direct_matrix[0][0] = 0
        vertex_sets = subtree_vertex_sets(children)
        direct_match = all(
            characteristic_polynomial(
                induced_matrix(direct_matrix, vertex_sets[vertex])
            )
            == subtree[vertex]
            for vertex in range(len(matrix))
        )
    return {
        "label": label,
        "parent": parent,
        "edge_products": edge_products,
        "recursive_coprime": recursive_coprime,
        "violations": violations,
        "root_polynomial_low_to_high": [
            str(value) for value in subtree[0]
        ],
        "verification_rank_mod_prime": rank,
        "verification_columns": columns,
        "nssp_full_mod_prime": rank == columns,
        "positive_modular_rank_loss_candidate": recursive_coprime and rank < columns,
        "negative_modular_full_rank_counterexample": (
            not recursive_coprime and rank == columns
        ),
        "exact_rank_over_q": rank_over_q(verification) if exact else None,
        "independent_subtree_polynomials_match": direct_match,
    }


def targeted_cases() -> list[
    tuple[str, tuple[int, ...], tuple[int, ...], tuple[int, ...]]
]:
    return [
        (
            "nested_leaf_collision",
            (0, 1, 1),
            (1, 1, 1),
            (2, 3, -2),
        ),
        (
            "nested_coprime_positive",
            (0, 1, 1, 3),
            (1, 1, 1, 1),
            (2, -3, 2, -2),
        ),
        (
            "two_branch_vertices_positive",
            (0, 1, 1, 3, 3, 5),
            (1, 1, 1, 1, 1, 1),
            (2, -3, 2, -1, 3, -2),
        ),
        (
            "nested_shared_nonzero_factor",
            (0, 1, 2, 1, 4),
            (1, 1, 1, 1, 1),
            (2, 3, 2, -3, 2),
        ),
        (
            "single_subtree_repeated_complex_roots",
            (0, 1, 1, 3, 4, 5),
            (1, 1, 1, 1, 1, 1),
            (-2, 3, -1, 1, -4, 1),
        ),
        (
            "same_products_new_direction_split",
            (0, 1, 1, 3, 4, 5),
            (-1, -1, -1, -1, 2, -1),
            (2, -3, 1, -1, -2, -1),
        ),
    ]


def parent_tuples(vertices: int):
    ranges = [range(child) for child in range(1, vertices)]
    yield from itertools.product(*ranges)


def run(max_vertices: int, samples: int) -> dict[str, object]:
    rng = random.Random(20260819)
    targeted = [evaluate(*case, exact=True) for case in targeted_cases()]
    total = 0
    recursively_coprime = 0
    recursively_coprime_full = 0
    noncoprime = 0
    noncoprime_full = 0
    positive_candidates: list[dict[str, object]] = []
    negative_counterexamples: list[dict[str, object]] = []
    shape_counts: dict[str, int] = {}

    for vertices in range(2, max_vertices + 1):
        shapes = 0
        for parent in parent_tuples(vertices):
            shapes += 1
            for sample in range(samples):
                forward = tuple(nonzero(rng) for _ in parent)
                backward = tuple(nonzero(rng) for _ in parent)
                case = evaluate(
                    f"n{vertices}_shape{shapes}_sample{sample}",
                    parent,
                    forward,
                    backward,
                )
                total += 1
                if case["recursive_coprime"]:
                    recursively_coprime += 1
                    recursively_coprime_full += int(case["nssp_full_mod_prime"])
                else:
                    noncoprime += 1
                    noncoprime_full += int(case["nssp_full_mod_prime"])
                if case["positive_modular_rank_loss_candidate"]:
                    positive_candidates.append(case)
                if case["negative_modular_full_rank_counterexample"]:
                    negative_counterexamples.append(case)
        shape_counts[str(vertices)] = shapes

    return {
        "prime": PRIME,
        "max_vertices": max_vertices,
        "samples_per_parent_tuple": samples,
        "parent_tuple_counts": shape_counts,
        "total_random_cases": total,
        "recursive_coprime": recursively_coprime,
        "recursive_coprime_full_mod_prime": recursively_coprime_full,
        "noncoprime": noncoprime,
        "noncoprime_full_mod_prime": noncoprime_full,
        "positive_modular_rank_loss_candidate_count": len(positive_candidates),
        "first_positive_candidate": (
            positive_candidates[0] if positive_candidates else None
        ),
        "negative_modular_full_rank_counterexample_count": len(
            negative_counterexamples
        ),
        "first_negative_counterexample": (
            negative_counterexamples[0] if negative_counterexamples else None
        ),
        "targeted": targeted,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-vertices", type=int, default=7)
    parser.add_argument("--samples", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(run(args.max_vertices, args.samples), indent=2))


if __name__ == "__main__":
    main()
