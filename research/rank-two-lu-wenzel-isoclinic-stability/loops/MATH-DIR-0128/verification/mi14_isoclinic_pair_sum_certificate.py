#!/usr/bin/env python3
"""Exact Bernstein certificate search for the full isoclinic MI-14 family.

For C=tW with W in U(2), phase and diagonal gauges reduce W to
[[exp(i phi)x,y],[-y,exp(-i phi)x]].  The script reconstructs the polynomial
of the five paired positive commutator eigenvalues from exact power traces,
forms the degree-ten polynomial of their pair sums, shifts by 3, and converts
every coefficient to tensor Bernstein form on the unit parameter box.
"""

from __future__ import annotations

import argparse
import json
from math import comb

import numpy as np
import sympy as sp


def build_reduced_power_sums() -> tuple[list[sp.Expr], tuple[sp.Symbol, ...]]:
    p, q, t, s, x, y, phase = sp.symbols("p q t s x y phase", nonzero=True)
    a, radius, mixing, product, phase_cosine = sp.symbols(
        "a radius mixing product phase_cosine", real=True
    )
    phase_square = sp.symbols("phase_square", real=True)
    unitary = sp.Matrix(
        [[phase * x, y], [-y, x / phase]]
    )
    sigma = sp.diag(p, q)
    matrix = sp.zeros(4)
    matrix[:2, :2] = sigma * (t * unitary.T).subs(phase, 1 / phase)
    matrix[:2, 2:] = sigma * (s * sp.eye(2))
    operator = sp.kronecker_product(sp.eye(4), matrix) - sp.kronecker_product(
        matrix.T, sp.eye(4)
    )
    matrix_bar = matrix.subs(phase, 1 / phase)
    operator_adjoint = sp.kronecker_product(
        sp.eye(4), matrix_bar.T
    ) - sp.kronecker_product(matrix_bar, sp.eye(4))
    gram = operator_adjoint * operator
    base_variables = (p, q, s, t, x, y)

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
            p_exp, q_exp, s_exp, t_exp, x_exp, y_exp = exponents
            if p_exp % 2 != q_exp % 2 or any(
                exponent % 2 for exponent in (s_exp, t_exp, x_exp, y_exp)
            ):
                raise RuntimeError(f"unexpected monomial exponents: {exponents}")
            singular_part = (
                a ** (p_exp // 2) * (1 - a) ** (q_exp // 2)
                if p_exp % 2 == 0
                else product
                * a ** ((p_exp - 1) // 2)
                * (1 - a) ** ((q_exp - 1) // 2)
            )
            reduced = (
                coefficient
                * singular_part
                * (1 - radius) ** (s_exp // 2)
                * radius ** (t_exp // 2)
                * mixing ** (x_exp // 2)
                * (1 - mixing) ** (y_exp // 2)
            )
            phase_groups[phase_exponent] = (
                phase_groups.get(phase_exponent, 0) + reduced
            )

        result = sp.expand(phase_groups.get(0, 0))
        maximum_phase = max(abs(exponent) for exponent in phase_groups)
        for exponent in range(1, maximum_phase + 1):
            positive = sp.expand(phase_groups.get(exponent, 0))
            negative = sp.expand(phase_groups.get(-exponent, 0))
            if sp.simplify(positive - negative) != 0:
                raise RuntimeError(f"phase Laurent coefficients differ at {exponent}")
            result += 2 * positive * sp.chebyshevt(exponent, phase_cosine)

        product_reduced = 0
        for (exponent,), coefficient in sp.Poly(sp.expand(result), product).terms():
            product_reduced += coefficient * (a * (1 - a)) ** (exponent // 2) * (
                product if exponent % 2 else 1
            )
        singular_reduced = sp.rem(
            sp.Poly(sp.expand(product_reduced), a),
            sp.Poly(a**2 - a + product**2, a),
        ).as_expr()
        if sp.Poly(sp.expand(singular_reduced), a).degree() > 0:
            raise RuntimeError("unexpected dependence on the labeled singular value")

        phase_reduced = 0
        for (exponent,), coefficient in sp.Poly(
            sp.expand(singular_reduced), phase_cosine
        ).terms():
            if exponent % 2:
                raise RuntimeError("unexpected odd phase-cosine power")
            phase_reduced += coefficient * phase_square ** (exponent // 2)
        return sp.factor(phase_reduced)

    powers: list[sp.Expr] = []
    gram_power = sp.eye(16)
    for exponent in range(1, 6):
        gram_power = gram_power * gram
        powers.append(reduce_trace(sp.trace(gram_power) / 2))
    return powers, (product, radius, mixing, phase_square)


def pair_sum_shift_coefficients(power_sums: list[sp.Expr]) -> list[sp.Expr]:
    root_elementary = [sp.Integer(1)]
    for degree in range(1, 6):
        value = sum(
            (-1) ** (index - 1)
            * root_elementary[degree - index]
            * power_sums[index - 1]
            for index in range(1, degree + 1)
        ) / degree
        root_elementary.append(sp.expand(value))

    all_root_powers = [sp.Integer(5), *power_sums]
    for degree in range(6, 11):
        value = sum(
            (-1) ** (index - 1)
            * root_elementary[index]
            * all_root_powers[degree - index]
            for index in range(1, 6)
        )
        all_root_powers.append(sp.expand(value))

    pair_powers = [sp.Integer(10)]
    for degree in range(1, 11):
        ordered_sum = sum(
            sp.binomial(degree, index)
            * all_root_powers[index]
            * all_root_powers[degree - index]
            for index in range(degree + 1)
        )
        pair_powers.append(sp.expand((ordered_sum - 2**degree * all_root_powers[degree]) / 2))

    pair_elementary = [sp.Integer(1)]
    for degree in range(1, 11):
        value = sum(
            (-1) ** (index - 1)
            * pair_elementary[degree - index]
            * pair_powers[index]
            for index in range(1, degree + 1)
        ) / degree
        pair_elementary.append(sp.expand(value))

    variable, shift = sp.symbols("pair_variable shift")
    polynomial = sum(
        (-1) ** degree * pair_elementary[degree] * variable ** (10 - degree)
        for degree in range(11)
    )
    shifted = sp.Poly(sp.expand(polynomial.subs(variable, shift + 3)), shift)
    return [shifted.coeff_monomial(shift**degree) for degree in range(11)]


def bernstein_statistics(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> dict[str, object]:
    product, radius, mixing, phase_square = variables
    scaled_product = sp.symbols("scaled_product")
    polynomial = sp.Poly(
        sp.expand(expression.subs(product, scaled_product / 2)),
        scaled_product,
        radius,
        mixing,
        phase_square,
    )
    degrees = tuple(polynomial.degree(variable) for variable in polynomial.gens)
    power_coefficients = {
        indices: polynomial.coeff_monomial(
            sp.prod(variable**degree for variable, degree in zip(polynomial.gens, indices))
        )
        for indices in __import__("itertools").product(
            *(range(degree + 1) for degree in degrees)
        )
    }
    minimum: sp.Rational | sp.Integer | None = None
    negative_count = 0
    total = 0
    for target in __import__("itertools").product(
        *(range(degree + 1) for degree in degrees)
    ):
        value = 0
        for source in __import__("itertools").product(
            *(range(index + 1) for index in target)
        ):
            weight = sp.prod(
                sp.Rational(comb(target_index, source_index), comb(degree, source_index))
                for target_index, source_index, degree in zip(target, source, degrees)
            )
            value += power_coefficients[source] * weight
        value = sp.factor(value)
        minimum = value if minimum is None or value < minimum else minimum
        negative_count += int(bool(value < 0))
        total += 1
    return {
        "degrees": list(degrees),
        "minimum": str(minimum),
        "negative_count": negative_count,
        "coefficient_count": total,
    }


def numeric_power_sum_error(
    power_sums: list[sp.Expr], variables: tuple[sp.Symbol, ...], seed: int = 20261018
) -> float:
    functions = [sp.lambdify(variables, expression, "numpy") for expression in power_sums]
    rng = np.random.default_rng(seed)
    largest_error = 0.0
    for _ in range(20):
        q = rng.uniform(0.05, 0.7)
        p = np.sqrt(1.0 - q * q)
        t = rng.uniform(0.02, 0.98)
        x = rng.uniform(0.02, 0.98)
        y = np.sqrt(1.0 - x * x)
        phase = rng.uniform(0.0, np.pi)
        unitary = np.array(
            [
                [np.exp(1j * phase) * x, y],
                [-y, np.exp(-1j * phase) * x],
            ]
        )
        sigma = np.diag([p, q])
        matrix = np.block(
            [
                [t * sigma @ unitary.conj().T, np.sqrt(1.0 - t * t) * sigma],
                [np.zeros((2, 2)), np.zeros((2, 2))],
            ]
        )
        operator = np.kron(np.eye(4), matrix) - np.kron(matrix.T, np.eye(4))
        eigenvalues = np.linalg.eigvalsh(operator.conj().T @ operator)
        arguments = (p * q, t * t, x * x, np.cos(phase) ** 2)
        for exponent, function in enumerate(functions, start=1):
            direct = 0.5 * np.sum(eigenvalues**exponent)
            predicted = float(function(*arguments))
            largest_error = max(largest_error, abs(float(direct) - predicted))
    return largest_error


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-shift-degree", type=int, default=10)
    args = parser.parse_args()
    if args.max_shift_degree < 0 or args.max_shift_degree > 10:
        raise SystemExit("max-shift-degree must lie in [0, 10]")
    power_sums, variables = build_reduced_power_sums()
    power_sum_error = numeric_power_sum_error(power_sums, variables)
    coefficients = pair_sum_shift_coefficients(power_sums)
    statistics = {
        str(degree): bernstein_statistics(coefficients[degree], variables)
        for degree in range(args.max_shift_degree + 1)
    }
    passed = (
        power_sum_error <= 2.0e-8
        and all(item["negative_count"] == 0 for item in statistics.values())
    )
    print(
        json.dumps(
            {
                "checked_shift_degrees": list(range(args.max_shift_degree + 1)),
                "numeric_power_sum_max_error": power_sum_error,
                "statistics": statistics,
                "result": "PASS" if passed else "FAIL",
                "interpretation": (
                    "PASS means every checked coefficient of the pair-sum polynomial "
                    "after the shift w=3+z has nonnegative tensor Bernstein coefficients "
                    "on product in [0,1/2] and the other three parameters in [0,1]."
                ),
            },
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
