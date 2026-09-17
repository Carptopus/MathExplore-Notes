"""Exact bounded control for the S4 first-event dichotomy."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
S1_CONTROL = HERE / "verify_minimal_endpoint_extraction.py"


def load_control():
    spec = importlib.util.spec_from_file_location("s1_control", S1_CONTROL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {S1_CONTROL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def spider_expansion(control, arms: tuple[int, ...]):
    adjacency = [[]]
    edges = []
    for length in arms:
        previous = 0
        for _ in range(length):
            current = len(adjacency)
            adjacency.append([])
            edge_index = len(edges)
            edges.append((previous, current))
            adjacency[previous].append((current, edge_index))
            adjacency[current].append((previous, edge_index))
            previous = current
    return control.power_sum_expansion(adjacency, range(len(edges)))


def path_expansion(control, vertices: int):
    if vertices == 0:
        return {(): 1}
    return spider_expansion(control, (vertices - 1,))


def multiply(left, right):
    result = {}
    for left_part, left_coefficient in left.items():
        for right_part, right_coefficient in right.items():
            part = tuple(sorted(left_part + right_part, reverse=True))
            result[part] = (
                result.get(part, 0)
                + left_coefficient * right_coefficient
            )
    return {part: value for part, value in result.items() if value}


def pruning_product(control, arms: tuple[int, ...], degree: int):
    polynomial = [{(): 1}] + [{} for _ in range(degree)]
    paths = [path_expansion(control, size) for size in range(degree + 1)]
    for length in arms:
        following = [{} for _ in range(degree + 1)]
        for first in range(degree + 1):
            for second in range(min(length, degree - first) + 1):
                control.add_scaled(
                    following[first + second],
                    multiply(polynomial[first], paths[second]),
                    1,
                )
        polynomial = following
    return polynomial


def normalized_derivative(control, alternating, order):
    result = control.derivative(alternating, order)
    sign = (-1) ** (order - 1)
    return {part: sign * value for part, value in result.items()}


def subtract(control, left, right):
    result = dict(left)
    control.add_scaled(result, right, -1)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=13)
    args = parser.parse_args()

    control = load_control()
    probe = control.load_probe()
    checked = 0
    seamless_checked = 0
    path_root_checked = 0

    for order in range(8, args.max_order + 1):
        for description in probe.descriptions(order):
            alpha, beta, left, middle, right = description
            left_order = 1 + sum(left)
            right_order = 1 + sum(right)
            if left_order >= right_order:
                continue

            adjacency, edges = probe.tree(description)
            trunk_length = alpha + beta
            alternating = control.power_sum_expansion(
                adjacency,
                range(len(edges)),
                range(trunk_length),
            )
            first_order = min(left_order + alpha, right_order)
            pruning = pruning_product(
                control,
                middle + right,
                first_order - left_order,
            )

            for complement_order in range(left_order, first_order + 1):
                prediction = {}
                for extension in range(
                    complement_order - left_order + 1
                ):
                    arms = left if extension == 0 else left + (extension,)
                    control.add_scaled(
                        prediction,
                        multiply(
                            spider_expansion(control, arms),
                            pruning[
                                complement_order - left_order - extension
                            ],
                        ),
                        1,
                    )
                actual = normalized_derivative(
                    control,
                    alternating,
                    order - complement_order,
                )
                difference = subtract(control, actual, prediction)
                if complement_order < first_order:
                    expected = {}
                else:
                    extended_left = spider_expansion(
                        control, left + (alpha,)
                    )
                    right_expansion = spider_expansion(control, right)
                    if right_order < left_order + alpha:
                        expected = right_expansion
                    elif left_order + alpha < right_order:
                        expected = {
                            part: -value
                            for part, value in extended_left.items()
                        }
                    else:
                        expected = subtract(
                            control, right_expansion, extended_left
                        )
                if difference != expected:
                    raise AssertionError(
                        (description, complement_order, difference, expected)
                    )

            seamless = (
                right_order == left_order + alpha
                and tuple(sorted(right, reverse=True))
                == tuple(sorted(left + (alpha,), reverse=True))
            )
            if seamless:
                complement_order = right_order + 1
                pruning = pruning_product(
                    control,
                    middle + right,
                    complement_order - left_order,
                )
                prediction = {}
                for extension in range(
                    complement_order - left_order + 1
                ):
                    arms = left if extension == 0 else left + (extension,)
                    control.add_scaled(
                        prediction,
                        multiply(
                            spider_expansion(control, arms),
                            pruning[
                                complement_order - left_order - extension
                            ],
                        ),
                        1,
                    )
                actual = normalized_derivative(
                    control,
                    alternating,
                    order - complement_order,
                )
                difference = subtract(control, actual, prediction)

                expected = {}
                control.add_scaled(
                    expected,
                    spider_expansion(control, left + (alpha + 1,)),
                    -1,
                )
                control.add_scaled(
                    expected,
                    multiply({(1,): 1}, spider_expansion(control, right)),
                    -1,
                )
                if beta >= 2:
                    control.add_scaled(
                        expected,
                        spider_expansion(control, right + (1,)),
                        1,
                    )
                middle_order = 1 + sum(middle)
                if middle_order == 2:
                    left_middle = control.component_vertices(
                        adjacency, alpha, 0
                    )
                    control.add_scaled(
                        expected,
                        control.induced_expansion(adjacency, left_middle),
                        1,
                    )
                if difference != expected or not difference:
                    raise AssertionError(
                        ("seamless", description, difference, expected)
                    )
                seamless_checked += 1

            if (
                len(left) == 2
                and alpha >= 2
                and right_order >= left_order + 2
            ):
                complement_order = left_order + 1
                actual = normalized_derivative(
                    control,
                    alternating,
                    order - complement_order,
                )
                expected = spider_expansion(control, left + (1,))
                remaining_twig_count = len(middle) + len(right)
                control.add_scaled(
                    expected,
                    multiply(
                        {(1,): remaining_twig_count},
                        spider_expansion(control, left),
                    ),
                    1,
                )
                if actual != expected:
                    raise AssertionError(
                        ("path-root", description, actual, expected)
                    )
                path_root_checked += 1
            checked += 1
        print(f"n={order}: PASS")
    print(
        f"PASS checked_descriptions={checked} "
        f"seamless_descriptions={seamless_checked} "
        f"path_root_descriptions={path_root_checked}"
    )


if __name__ == "__main__":
    main()
