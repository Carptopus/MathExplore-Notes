#!/usr/bin/env python3
"""Exact reduction of the general unequal-angle MI-14 constant certificate.

The normalized rank-two core is written as

    X = [[Sigma D W*, Sigma sqrt(I-D^2)], [0, 0]],

with arbitrary ``W in U(2)``.  The five paired commutator roots are recovered
from exact power traces.  Instead of constructing all ten pair-sum
coefficients, this script uses the staircase-Schur identity

    product_{i<j}(x_i+x_j)
      = -e1^2 e4^2 - e1 e2^2 e5 + e1 e2 e3 e4
        + 2 e1 e4 e5 + e2 e3 e5 - e3^2 e4 - e5^2

for ``x_i=3/2-mu_i`` to obtain only ``B0=R(3)``.  Singular-value and
principal-angle label symmetries are reduced modulo two quadratic relations.
The output is discovery material until a sign certificate for B0 is found.
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import sympy as sp


def build_general_power_sums() -> tuple[list[sp.Expr], tuple[sp.Symbol, ...]]:
    p, q, c, d, s, t, x, y, phase = sp.symbols(
        "p q c d s t x y phase", nonzero=True
    )
    product, imbalance = sp.symbols("product imbalance", real=True)
    principal_product, complement_product = sp.symbols(
        "principal_product complement_product", real=True
    )
    principal_difference, mixing, phase_cosine = sp.symbols(
        "principal_difference mixing phase_cosine", real=True
    )
    phase_square = sp.symbols("phase_square", real=True)

    singular_first = (1 + imbalance) / 2
    singular_second = (1 - imbalance) / 2
    principal_sum = 1 + principal_product**2 - complement_product**2
    principal_first = (principal_sum + principal_difference) / 2
    principal_second = (principal_sum - principal_difference) / 2
    complement_first = 1 - principal_first
    complement_second = 1 - principal_second
    difference_square = sp.expand(
        (1 - (principal_product + complement_product) ** 2)
        * (1 - (principal_product - complement_product) ** 2)
    )

    unitary = sp.Matrix([[phase * x, y], [-y, x / phase]])
    sigma = sp.diag(p, q)
    principal = sp.diag(c, d)
    complement = sp.diag(s, t)
    matrix = sp.zeros(4)
    matrix[:2, :2] = sigma * principal * unitary.T.subs(phase, 1 / phase)
    matrix[:2, 2:] = sigma * complement
    operator = sp.kronecker_product(sp.eye(4), matrix) - sp.kronecker_product(
        matrix.T, sp.eye(4)
    )
    matrix_bar = matrix.subs(phase, 1 / phase)
    operator_adjoint = sp.kronecker_product(
        sp.eye(4), matrix_bar.T
    ) - sp.kronecker_product(matrix_bar, sp.eye(4))
    gram = operator_adjoint * operator
    base_variables = (p, q, c, d, s, t, x, y)

    def reduce_relations(expression: sp.Expr) -> sp.Expr:
        reduced = sp.rem(
            sp.Poly(sp.expand(expression), imbalance),
            sp.Poly(imbalance**2 - 1 + 4 * product**2, imbalance),
        ).as_expr()
        reduced = sp.rem(
            sp.Poly(sp.expand(reduced), principal_difference),
            sp.Poly(principal_difference**2 - difference_square, principal_difference),
        ).as_expr()
        return sp.expand(reduced)

    def paired_power(
        first_exp: int,
        second_exp: int,
        first_square: sp.Expr,
        second_square: sp.Expr,
        cross_product: sp.Expr,
    ) -> sp.Expr:
        if first_exp % 2 != second_exp % 2:
            raise RuntimeError(
                f"unpaired exponents {first_exp}, {second_exp}"
            )
        if first_exp % 2:
            return (
                cross_product
                * first_square ** ((first_exp - 1) // 2)
                * second_square ** ((second_exp - 1) // 2)
            )
        return first_square ** (first_exp // 2) * second_square ** (
            second_exp // 2
        )

    def reduce_trace(expression: sp.Expr) -> sp.Expr:
        phase_groups: dict[int, sp.Expr] = {}
        for term in sp.Add.make_args(sp.expand(expression)):
            powers = term.as_powers_dict()
            exponents = tuple(int(powers.get(variable, 0)) for variable in base_variables)
            phase_exponent = int(powers.get(phase, 0))
            coefficient = term
            for variable, exponent in zip(base_variables, exponents):
                coefficient /= variable**exponent
            coefficient /= phase**phase_exponent
            p_exp, q_exp, c_exp, d_exp, s_exp, t_exp, x_exp, y_exp = exponents
            if x_exp % 2 or y_exp % 2:
                raise RuntimeError(f"unexpected mixing parity: {exponents}")
            reduced = (
                coefficient
                * paired_power(
                    p_exp,
                    q_exp,
                    singular_first,
                    singular_second,
                    product,
                )
                * paired_power(
                    c_exp,
                    d_exp,
                    principal_first,
                    principal_second,
                    principal_product,
                )
                * paired_power(
                    s_exp,
                    t_exp,
                    complement_first,
                    complement_second,
                    complement_product,
                )
                * mixing ** (x_exp // 2)
                * (1 - mixing) ** (y_exp // 2)
            )
            phase_groups[phase_exponent] = phase_groups.get(phase_exponent, 0) + reduced

        result = sp.expand(phase_groups.get(0, 0))
        maximum_phase = max(abs(exponent) for exponent in phase_groups)
        for exponent in range(1, maximum_phase + 1):
            positive = sp.expand(phase_groups.get(exponent, 0))
            negative = sp.expand(phase_groups.get(-exponent, 0))
            if sp.simplify(positive - negative) != 0:
                raise RuntimeError(f"phase Laurent coefficients differ at {exponent}")
            result += 2 * positive * sp.chebyshevt(exponent, phase_cosine)

        phase_reduced = 0
        for (exponent,), coefficient in sp.Poly(
            sp.expand(result), phase_cosine
        ).terms():
            if exponent % 2:
                raise RuntimeError("unexpected odd phase-cosine power")
            phase_reduced += coefficient * phase_square ** (exponent // 2)
        return reduce_relations(phase_reduced)

    powers: list[sp.Expr] = []
    gram_power = sp.eye(16)
    for _ in range(5):
        gram_power = gram_power * gram
        powers.append(reduce_trace(sp.trace(gram_power) / 2))
    return powers, (
        product,
        imbalance,
        principal_product,
        complement_product,
        principal_difference,
        mixing,
        phase_square,
    )


def constant_pair_gap(
    power_sums: list[sp.Expr], variables: tuple[sp.Symbol, ...]
) -> sp.Expr:
    product, imbalance, principal_product, complement_product, principal_difference, _, _ = variables
    difference_square = sp.expand(
        (1 - (principal_product + complement_product) ** 2)
        * (1 - (principal_product - complement_product) ** 2)
    )

    def reduce_relations(expression: sp.Expr) -> sp.Expr:
        reduced = sp.rem(
            sp.Poly(sp.expand(expression), imbalance),
            sp.Poly(imbalance**2 - 1 + 4 * product**2, imbalance),
        ).as_expr()
        reduced = sp.rem(
            sp.Poly(sp.expand(reduced), principal_difference),
            sp.Poly(principal_difference**2 - difference_square, principal_difference),
        ).as_expr()
        return sp.expand(reduced)

    root_elementary = [sp.Integer(1)]
    for degree in range(1, 6):
        value = sum(
            (-1) ** (index - 1)
            * root_elementary[degree - index]
            * power_sums[index - 1]
            for index in range(1, degree + 1)
        ) / degree
        root_elementary.append(reduce_relations(value))

    half_three = sp.Rational(3, 2)
    shifted_elementary = [sp.Integer(1)]
    for degree in range(1, 6):
        value = sum(
            (-1) ** index
            * sp.binomial(5 - index, degree - index)
            * half_three ** (degree - index)
            * root_elementary[index]
            for index in range(degree + 1)
        )
        shifted_elementary.append(reduce_relations(value))
    e1, e2, e3, e4, e5 = shifted_elementary[1:]
    value = (
        -e1**2 * e4**2
        - e1 * e2**2 * e5
        + e1 * e2 * e3 * e4
        + 2 * e1 * e4 * e5
        + e2 * e3 * e5
        - e3**2 * e4
        - e5**2
    )
    return reduce_relations(value)


def numeric_error(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...], seed: int = 20261018
) -> float:
    function = sp.lambdify(variables, expression, "numpy")
    rng = np.random.default_rng(seed)
    largest_error = 0.0
    for _ in range(20):
        singular_square = rng.uniform(0.5, 0.999)
        p, q = np.sqrt(singular_square), np.sqrt(1 - singular_square)
        c, d = sorted(rng.uniform(0.01, 0.99, size=2), reverse=True)
        angle = rng.uniform(0.01, np.pi / 2 - 0.01)
        phase = rng.uniform(0.0, np.pi)
        cosine, sine = np.cos(angle), np.sin(angle)
        unitary = np.array(
            [
                [np.exp(1j * phase) * cosine, sine],
                [-sine, np.exp(-1j * phase) * cosine],
            ]
        )
        sigma = np.diag([p, q])
        principal = np.diag([c, d])
        complement = np.diag(np.sqrt(1 - np.array([c, d]) ** 2))
        matrix = np.block(
            [
                [sigma @ principal @ unitary.conj().T, sigma @ complement],
                [np.zeros((2, 2)), np.zeros((2, 2))],
            ]
        )
        operator = np.kron(np.eye(4), matrix) - np.kron(matrix.T, np.eye(4))
        eigenvalues = np.linalg.eigvalsh(operator.conj().T @ operator)[::-1]
        roots = eigenvalues[:10:2]
        direct = np.prod(
            [3 - roots[first] - roots[second] for first in range(5) for second in range(first + 1, 5)]
        )
        arguments = (
            p * q,
            p * p - q * q,
            c * d,
            np.sqrt((1 - c * c) * (1 - d * d)),
            c * c - d * d,
            cosine * cosine,
            np.cos(phase) ** 2,
        )
        predicted = float(function(*arguments))
        largest_error = max(largest_error, abs(float(direct) - predicted))
    return largest_error


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("powers", "b0"), default="b0")
    args = parser.parse_args()
    powers, variables = build_general_power_sums()
    if args.stage == "powers":
        print(
            json.dumps(
                {
                    "result": "PASS",
                    "power_sum_term_counts": [len(sp.Add.make_args(item)) for item in powers],
                },
                indent=2,
            )
        )
        return
    expression = constant_pair_gap(powers, variables)
    error = numeric_error(expression, variables)
    product, imbalance, principal_product, complement_product, principal_difference, mixing, phase_square = variables
    odd_coefficient = sp.Poly(expression, imbalance, principal_difference).coeff_monomial(
        imbalance * principal_difference
    )
    forbidden_terms = [
        monomial
        for monomial, _ in sp.Poly(expression, imbalance, principal_difference).terms()
        if monomial not in ((0, 0), (1, 1))
    ]
    common_factors = []
    for variable in (product, principal_product, complement_product, mixing, phase_square):
        if odd_coefficient != 0 and sp.rem(
            sp.Poly(odd_coefficient, variable), sp.Poly(variable, variable)
        ).as_expr() == 0:
            common_factors.append(str(variable))
    payload = {
        "result": "PASS" if error <= 2.0e-7 and not forbidden_terms else "FAIL",
        "numeric_max_error": error,
        "term_count": len(sp.Add.make_args(expression)),
        "degrees": {
            str(variable): sp.Poly(expression, *variables).degree(variable)
            for variable in variables
        },
        "joint_swap_normal_form": "B0 = even_part + imbalance*principal_difference*odd_part",
        "forbidden_label_terms": forbidden_terms,
        "odd_part_term_count": len(sp.Add.make_args(odd_coefficient)),
        "odd_part_common_coordinate_factors": common_factors,
    }
    print(json.dumps(payload, indent=2))
    if payload["result"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
