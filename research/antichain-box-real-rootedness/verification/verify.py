"""有限校准反链多项式、候选行列式和 Jacobi 变换。

这些检查只用于发现边界错误，不能代替一般证明。
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import comb

import sympy as sp


Array = tuple[tuple[int, ...], tuple[int, ...]]
NegativePair = tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]


def add_polynomials(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    size = max(len(left), len(right))
    values = [0] * size
    for index, value in enumerate(left):
        values[index] += value
    for index, value in enumerate(right):
        values[index] += value
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def subtract_polynomials(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    size = max(len(left), len(right))
    values = [0] * size
    for index, value in enumerate(left):
        values[index] += value
    for index, value in enumerate(right):
        values[index] -= value
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def multiply_polynomials(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    values = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            values[i + j] += left_value * right_value
    return tuple(values)


def antichain_polynomial(m: int, n: int) -> tuple[int, ...]:
    """用可比较图的独立集递归精确枚举 [2]x[m]x[n] 的反链。"""

    elements = [(a, b, c) for a in range(2) for b in range(m) for c in range(n)]
    comparable_masks: list[int] = []
    for left in elements:
        mask = 0
        for index, right in enumerate(elements):
            left_le_right = all(x <= y for x, y in zip(left, right))
            right_le_left = all(y <= x for x, y in zip(left, right))
            if left_le_right or right_le_left:
                mask |= 1 << index
        comparable_masks.append(mask)

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[int, ...]:
        if mask == 0:
            return (1,)
        candidates = [index for index in range(len(elements)) if mask & (1 << index)]
        pivot = max(candidates, key=lambda index: (mask & comparable_masks[index]).bit_count())
        without_pivot = recurse(mask & ~(1 << pivot))
        with_pivot = (0,) + recurse(mask & ~comparable_masks[pivot])
        return add_polynomials(without_pivot, with_pivot)

    return recurse((1 << len(elements)) - 1)


def determinant_polynomial(m: int, n: int) -> tuple[int, ...]:
    degree = min(m, n)
    diagonal = tuple(comb(m, j) * comb(n, j) for j in range(degree + 1))
    upper = tuple(
        0 if j == 0 else comb(m + 1, j + 1) * comb(n - 1, j - 1)
        for j in range(degree + 1)
    )
    lower = tuple(
        0 if j == 0 else comb(m - 1, j - 1) * comb(n + 1, j + 1)
        for j in range(degree + 1)
    )
    return subtract_polynomials(
        multiply_polynomials(diagonal, diagonal),
        multiply_polynomials(upper, lower),
    )


def altered_determinant_polynomial(m: int, n: int) -> tuple[int, ...]:
    """故意破坏上右指标，确认校准不是恒等式误写后仍会通过。"""

    degree = min(m, n)
    diagonal = tuple(comb(m, j) * comb(n, j) for j in range(degree + 1))
    upper = tuple(
        0 if j == 0 else comb(m + 1, j) * comb(n - 1, j - 1)
        for j in range(degree + 1)
    )
    lower = tuple(
        0 if j == 0 else comb(m - 1, j - 1) * comb(n + 1, j + 1)
        for j in range(degree + 1)
    )
    return subtract_polynomials(
        multiply_polynomials(diagonal, diagonal),
        multiply_polynomials(upper, lower),
    )


def increasing_arrays(m: int, n: int) -> list[Array]:
    values: list[Array] = [((), ())]
    for size in range(1, min(m, n) + 1):
        for top in combinations(range(1, m + 1), size):
            for bottom in combinations(range(1, n + 1), size):
                values.append((top, bottom))
    return values


def tail_switch(left: Array, right: Array) -> NegativePair | None:
    """按 Krattenthaler 交叉坐标最大的冲突执行换尾。"""

    left_top, left_bottom = left
    right_top = tuple(value + 1 for value in right[0])
    right_bottom = tuple(value - 1 for value in right[1])
    crossings = [
        (i, j)
        for i in range(1, len(left_top) + 1)
        for j in range(1, len(right_top) + 1)
        if left_top[i - 1] < right_top[j - 1]
        and right_bottom[j - 1] < left_bottom[i - 1]
    ]
    if not crossings:
        return None
    i, j = max(
        crossings,
        key=lambda crossing: (
            right_top[crossing[1] - 1],
            left_bottom[crossing[0] - 1],
        ),
    )
    return (
        left_top[:i] + right_top[j - 1 :],
        left_bottom[: i - 1] + right_bottom[j:],
        right_top[: j - 1] + left_top[i:],
        right_bottom[:j] + left_bottom[i - 1 :],
    )


def negative_pairs(m: int, n: int) -> list[NegativePair]:
    """枚举行长差分别为 +2 和 -2 的行列式负项数组。"""

    values: list[NegativePair] = []
    limit = min(m - 1, n - 1)
    for r in range(limit + 1):
        for x_top in combinations(range(1, m + 2), r + 2):
            for x_bottom in combinations(range(1, n), r):
                for s in range(limit + 1):
                    for y_top in combinations(range(2, m + 1), s):
                        for y_bottom in combinations(range(0, n + 1), s + 2):
                            values.append((x_top, x_bottom, y_top, y_bottom))
    return values


def admissible_inverse_cut(pair: NegativePair, i: int, j: int) -> bool:
    x_top, x_bottom, y_top, y_bottom = pair
    rows = (
        x_top[:i] + y_top[j - 1 :],
        x_bottom[: i - 1] + y_bottom[j:],
        y_top[: j - 1] + x_top[i:],
        y_bottom[:j] + x_bottom[i - 1 :],
    )
    return all(all(a < b for a, b in zip(row, row[1:])) for row in rows)


def inverse_tail_switch(pair: NegativePair) -> tuple[Array, Array]:
    """在右上角坐标最大的可拼接间隙处执行逆换尾。"""

    x_top, x_bottom, y_top, y_bottom = pair
    cuts = [
        (i, j)
        for i in range(1, len(x_top))
        for j in range(1, len(y_bottom))
        if admissible_inverse_cut(pair, i, j)
    ]
    assert cuts, pair
    i, j = max(cuts, key=lambda cut: (x_top[cut[0]], y_bottom[cut[1]]))
    left = (x_top[:i] + y_top[j - 1 :], x_bottom[: i - 1] + y_bottom[j:])
    translated_right = (
        y_top[: j - 1] + x_top[i:],
        y_bottom[:j] + x_bottom[i - 1 :],
    )
    right = (
        tuple(value - 1 for value in translated_right[0]),
        tuple(value + 1 for value in translated_right[1]),
    )
    return left, right


def inverse_tail_switch_at_cut(
    pair: NegativePair, i: int, j: int
) -> tuple[Array, Array]:
    """在指定可拼接间隙执行逆换尾，用于破坏性对照。"""

    assert admissible_inverse_cut(pair, i, j), (pair, i, j)
    x_top, x_bottom, y_top, y_bottom = pair
    left = (x_top[:i] + y_top[j - 1 :], x_bottom[: i - 1] + y_bottom[j:])
    translated_right = (
        y_top[: j - 1] + x_top[i:],
        y_bottom[:j] + x_bottom[i - 1 :],
    )
    right = (
        tuple(value - 1 for value in translated_right[0]),
        tuple(value + 1 for value in translated_right[1]),
    )
    return left, right


def verify_tail_switch_bijection() -> tuple[int, int]:
    checked_pairs = 0
    checked_negative_objects = 0
    destructive_control_triggered = False
    for m in range(1, 5):
        for n in range(1, 5):
            arrays = increasing_arrays(m, n)
            positive_objects = [
                (left, right)
                for left in arrays
                for right in arrays
                if tail_switch(left, right) is not None
            ]
            image_list = [tail_switch(left, right) for left, right in positive_objects]
            assert all(image is not None for image in image_list)
            images = set(image_list)
            negatives = set(negative_pairs(m, n))
            assert images == negatives, (m, n, len(images), len(negatives))
            assert len(image_list) == len(images), (m, n, "image collision")
            for left, right in positive_objects:
                image = tail_switch(left, right)
                assert image is not None
                assert inverse_tail_switch(image) == (left, right), (m, n, left, right)
            for pair in negatives:
                assert tail_switch(*inverse_tail_switch(pair)) == pair, (m, n, pair)

                # 故意在首个可拼接处逆换尾；它并不总能恢复原像。
                x_top, _, _, y_bottom = pair
                cuts = [
                    (i, j)
                    for i in range(1, len(x_top))
                    for j in range(1, len(y_bottom))
                    if admissible_inverse_cut(pair, i, j)
                ]
                first = min(cuts, key=lambda cut: (x_top[cut[0]], y_bottom[cut[1]]))
                chosen = max(cuts, key=lambda cut: (x_top[cut[0]], y_bottom[cut[1]]))
                if first != chosen and tail_switch(
                    *inverse_tail_switch_at_cut(pair, *first)
                ) != pair:
                    destructive_control_triggered = True
            checked_pairs += 1
            checked_negative_objects += len(negatives)
    assert destructive_control_triggered
    return checked_pairs, checked_negative_objects


def verify_jacobi_connections() -> None:
    t = sp.symbols("t")
    for m in range(1, 7):
        for d in range(0, 6):
            denominator = 2 * m + d + 1
            q_m = sp.jacobi(m, 1, d, t)
            q_previous = sp.jacobi(m - 1, 1, d, t)
            first = (
                sp.jacobi(m, 0, d, t)
                - sp.Rational(m + d + 1, denominator) * q_m
                + sp.Rational(m + d, denominator) * q_previous
            )
            second = (
                (t - 1) * sp.jacobi(m - 1, 2, d, t)
                - sp.Rational(2 * m, denominator) * q_m
                + sp.Rational(2 * (m + 1), denominator) * q_previous
            )
            assert sp.expand(first) == 0, (m, d, "first")
            assert sp.expand(second) == 0, (m, d, "second")


def verify_jacobi_factorization() -> None:
    x = sp.symbols("x")
    t = (1 + x) / (1 - x)
    for m in range(1, 6):
        for n in range(m, 7):
            d = n - m
            diagonal = sum(comb(m, j) * comb(n, j) * x**j for j in range(m + 1))
            hypergeometric = sum(
                sp.rf(1 - m, j) * sp.rf(1 - n, j) / (sp.rf(3, j) * sp.factorial(j)) * x**j
                for j in range(m)
            )
            diagonal_jacobi = (1 - x) ** m * sp.jacobi(m, 0, d, t)
            hypergeometric_jacobi = (
                (1 - x) ** (m - 1)
                * sp.jacobi(m - 1, 2, d, t)
                / comb(m + 1, 2)
            )
            assert sp.cancel(diagonal - diagonal_jacobi) == 0, (m, n, "diagonal")
            assert sp.cancel(hypergeometric - hypergeometric_jacobi) == 0, (
                m,
                n,
                "off-diagonal",
            )

            rho = sp.sqrt(sp.Rational(n * (n + 1), m * (m + 1)))
            factor_minus = sp.jacobi(m, 0, d, t) - (
                rho * (t - 1) * sp.jacobi(m - 1, 2, d, t) / 2
            )
            factor_plus = sp.jacobi(m, 0, d, t) + (
                rho * (t - 1) * sp.jacobi(m - 1, 2, d, t) / 2
            )
            determinant = sum(
                value * x**j for j, value in enumerate(determinant_polynomial(m, n))
            )
            assert sp.cancel(determinant - (1 - x) ** (2 * m) * factor_minus * factor_plus) == 0, (
                m,
                n,
                "factorization",
            )


def verify_real_roots() -> None:
    x = sp.symbols("x")
    for m in range(1, 8):
        for n in range(1, 8):
            coefficients = determinant_polynomial(m, n)
            polynomial = sp.Poly(sum(value * x**j for j, value in enumerate(coefficients)), x)
            roots = polynomial.nroots(maxsteps=200)
            assert all(abs(complex(root).imag) < 1e-9 for root in roots), (m, n, roots)
            assert all(complex(root).real < -1e-9 for root in roots), (m, n, roots)


def main() -> None:
    checked_pairs: list[tuple[int, int]] = []
    negative_control_triggered = False
    for m in range(1, 5):
        for n in range(1, 5):
            enumerated = antichain_polynomial(m, n)
            determinant = determinant_polynomial(m, n)
            assert enumerated == determinant, (m, n, enumerated, determinant)
            if altered_determinant_polynomial(m, n) != enumerated:
                negative_control_triggered = True
            checked_pairs.append((m, n))
    assert negative_control_triggered
    switch_pairs, switch_objects = verify_tail_switch_bijection()
    verify_jacobi_connections()
    verify_jacobi_factorization()
    verify_real_roots()
    print(f"PASS: exact antichain/determinant comparison for {len(checked_pairs)} pairs")
    print("PASS: destructive off-diagonal-index control triggered")
    print(
        "PASS: exhaustive tail-switch bijection and canonical inverse for "
        f"{switch_objects} negative objects across {switch_pairs} parameter pairs"
    )
    print("PASS: destructive noncanonical inverse-cut control triggered")
    print("PASS: Jacobi connection identities for 36 parameter pairs")
    print("PASS: exact Jacobi transforms and factorization for 20 parameter pairs")
    print("PASS: numerical negative-real-root calibration for 49 parameter pairs")
    print("BOUNDARY: finite calibration does not replace the general proof in A2/A3")


if __name__ == "__main__":
    main()
