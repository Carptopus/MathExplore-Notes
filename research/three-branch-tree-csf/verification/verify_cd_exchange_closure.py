"""Exact cross-layout controls for the S13 C/D exchange closure."""

from __future__ import annotations

import argparse
import importlib.util
from collections import defaultdict
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
S12_CONTROL = HERE / "verify_scalar_profile_merge.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coefficient(polynomial, degree):
    return polynomial[degree] if degree < len(polynomial) else 0


def threshold(arms, level):
    return sum(length >= level for length in arms)


def layout(description):
    alpha, beta, left, middle, right = description
    return alpha, beta, 1 + sum(left), 1 + sum(middle), 1 + sum(right)


def is_cd_pair(s12, first, second):
    alpha, beta, a, b, c = layout(first)
    alpha2, beta2, a2, b2, c2 = layout(second)
    left = (a, b, c, alpha, beta)
    right = (a2, b2, c2, alpha2, beta2)
    return s12.is_allowed_exchange(left, right) or s12.is_allowed_exchange(
        right, left
    )


def polynomial_add(*polynomials):
    size = max(map(len, polynomials))
    result = [0] * size
    for polynomial in polynomials:
        for index, value in enumerate(polynomial):
            result[index] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def polynomial_negate(polynomial):
    return tuple(-value for value in polynomial)


def polynomial_multiply(*polynomials):
    result = (1,)
    for polynomial in polynomials:
        product = [0] * (len(result) + len(polynomial) - 1)
        for first_index, first_value in enumerate(result):
            for second_index, second_value in enumerate(polynomial):
                product[first_index + second_index] += first_value * second_value
        result = tuple(product)
    return result


def polynomial_shift(polynomial, amount):
    return (0,) * amount + polynomial


def arm(length):
    return (0,) + (1,) * length


def arm_sum(arms):
    return polynomial_add(*(arm(length) for length in arms))


def all_zero(polynomial):
    return all(value == 0 for value in polynomial)


def cubic_special_factor(first, second):
    """Verify (45)--(47) in the q=1,m=2 double degeneracy."""

    _, beta, left, middle, right = first
    _, beta2, left2, middle2, right2 = second
    assert beta == beta2
    assert len(middle) == len(middle2) == 1
    assert len(right) == len(right2) == 2
    if left == left2:
        return False

    t = sum(left)
    assert sum(left2) == t
    p = middle2[0]
    v = middle[0]
    assert tuple(sorted(left)) == tuple(sorted((p, t - p)))
    assert tuple(sorted(left2)) == tuple(sorted((v, t - v)))
    common = list(right)
    common.remove(t - v)
    assert len(common) == 1
    ell = common[0]
    assert ell == p + v + 1
    assert tuple(sorted(right2)) == tuple(sorted((t - p, ell)))

    # Build the numerator N from (47), treating P,V,T,w as monomials.
    one = (1,)
    x = (0, 1)
    P = polynomial_shift(one, p)
    V = polynomial_shift(one, v)
    T = polynomial_shift(one, t)
    w = polynomial_shift(one, beta)
    PV = polynomial_multiply(P, V)
    one_minus_x = polynomial_add(one, polynomial_negate(x))
    one_minus_pvx = polynomial_add(
        one, polynomial_negate(polynomial_multiply(PV, x))
    )
    one_minus_p = polynomial_add(one, polynomial_negate(P))
    one_minus_v = polynomial_add(one, polynomial_negate(V))
    one_minus_w = polynomial_add(one, polynomial_negate(w))
    numerator = polynomial_add(
        polynomial_multiply(
            polynomial_add(PV, polynomial_negate(T)),
            w,
            one_minus_x,
            one_minus_pvx,
        ),
        polynomial_multiply(
            T, one_minus_p, one_minus_v, x, one_minus_w
        ),
    )
    assert not all_zero(numerator)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=20)
    args = parser.parse_args()

    s12 = load_module("s12_control", S12_CONTROL)
    s11 = s12.load_module("s11_for_cd", s12.S11_CONTROL)
    s7 = s11.load_module("s7_for_cd", s11.S7_CONTROL)
    probe = s7.load_probe()

    buckets = defaultdict(list)
    descriptions = 0
    for order in range(8, args.max_order + 1):
        for raw in probe.descriptions(order):
            description = s11.orient_unique_minimum(raw)
            if description is None:
                continue
            alpha, beta, left, middle, right = description
            if alpha != 1 or len(left) != 2:
                continue
            a = 1 + sum(left)
            b = 1 + sum(middle)
            c = 1 + sum(right)
            degree_profile = tuple(
                sorted((len(left) + 1, len(middle) + 2, len(right) + 1))
            )
            key = (
                order,
                a,
                alpha + beta,
                tuple(sorted(left + middle + right, reverse=True)),
                degree_profile,
                s12.scalar_profile(a, b, c, alpha, beta),
            )
            buckets[key].append(description)
            descriptions += 1

    fixed_formula_pairs = 0
    position_formula_pairs = 0
    cubic_special_pairs = 0
    cd_pairs = 0
    signature_buckets = defaultdict(list)

    for key, values in buckets.items():
        for description in values:
            signature = (
                key,
                s11.path_remainder(s7, description),
                s11.three_leaf_formula(s7, description),
                s11.four_leaf_five_edge_formula(description, probe),
            )
            signature_buckets[signature].append(description)

        for first_index, first in enumerate(values):
            for second in values[first_index + 1 :]:
                if layout(first) == layout(second) or not is_cd_pair(
                    s12, first, second
                ):
                    continue
                cd_pairs += 1
                q, m = len(first[3]), len(first[4])
                q2, m2 = len(second[3]), len(second[4])
                w_difference = s7.add(
                    s11.path_remainder(s7, first),
                    s7.negate(s11.path_remainder(s7, second)),
                )
                j_difference = s7.add(
                    s11.three_leaf_formula(s7, first),
                    s7.negate(s11.three_leaf_formula(s7, second)),
                )

                if q == q2 and m == m2 and first[2] != second[2]:
                    levels = range(
                        2,
                        max(first[2] + first[3] + first[4] + second[2] + second[3] + second[4])
                        + 1,
                    )
                    level = next(
                        value
                        for value in levels
                        if any(
                            threshold(first[index], value)
                            != threshold(second[index], value)
                            for index in (2, 3, 4)
                        )
                    )
                    rho = threshold(first[2], level) - threshold(
                        second[2], level
                    )
                    sigma = threshold(first[3], level) - threshold(
                        second[3], level
                    )
                    expected_w = -(m - 2) * rho + (q - m + 1) * sigma
                    expected_j = (1 - comb(m, 2)) * rho + (
                        comb(q + 1, 2) - comb(m, 2)
                    ) * sigma
                    assert coefficient(w_difference, level + 1) == expected_w
                    assert coefficient(j_difference, level + 2) == expected_j
                    fixed_formula_pairs += 1
                    if q == 1 and m == 2:
                        cubic_special_pairs += cubic_special_factor(first, second)
                elif q2 == m - 1 and m2 == q + 1:
                    if coefficient(w_difference, 3) != 0:
                        continue
                    a2 = threshold(first[2], 2)
                    a2_prime = threshold(second[2], 2)
                    expected_j = (
                        (a2 - a2_prime) * (q - 1) * (m - 2) // 2
                        - (m - q - 1)
                    )
                    k_difference = s11.four_leaf_five_edge_formula(
                        first, probe
                    ) - s11.four_leaf_five_edge_formula(second, probe)
                    expected_k = (
                        (a2 - a2_prime)
                        * (m - 2)
                        * (m + q)
                        * (q - 1)
                        // 6
                        + (m + q) * (q - m + 1) // 2
                    )
                    assert coefficient(j_difference, 4) == expected_j
                    assert k_difference == expected_k
                    position_formula_pairs += 1

    collisions = []
    for values in signature_buckets.values():
        layouts = {layout(description) for description in values}
        if len(layouts) > 1:
            collisions.append(values)
    assert not collisions, collisions[:1]

    print(
        "PASS",
        f"descriptions={descriptions}",
        f"cd_pairs={cd_pairs}",
        f"fixed_formula_pairs={fixed_formula_pairs}",
        f"position_formula_pairs={position_formula_pairs}",
        f"cubic_special_pairs={cubic_special_pairs}",
        "cross_layout_collisions=0",
    )


if __name__ == "__main__":
    main()
