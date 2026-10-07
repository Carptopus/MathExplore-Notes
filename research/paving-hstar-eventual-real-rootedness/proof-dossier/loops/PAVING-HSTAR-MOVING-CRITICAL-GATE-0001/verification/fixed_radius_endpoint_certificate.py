"""固定半径负轴端点的有理上界；单端点通过不代表全半轴证明。"""

import argparse
import json
import math
import re
import time
from fractions import Fraction as F


BITS = 40
SCALE = 1 << BITS
MAX_CELLS = 8192
MAX_SECONDS = 45


def down(value):
    return F(value.numerator * SCALE // value.denominator, SCALE)


def up(value):
    return F(-((-value.numerator * SCALE) // value.denominator), SCALE)


def atan_bounds(inverse, terms):
    value = sum((F((-1) ** k, (2 * k + 1) * inverse ** (2 * k + 1))
                 for k in range(terms)), F(0))
    next_term = F((-1) ** terms, (2 * terms + 1) * inverse ** (2 * terms + 1))
    return min(value, value + next_term), max(value, value + next_term)


def pi_bounds():
    alo, ahi = atan_bounds(5, 24)
    blo, bhi = atan_bounds(239, 8)
    return down(16 * alo - 4 * bhi), up(16 * ahi - 4 * blo)


def cos_bounds(theta):
    # theta<=pi的交错余项从第二项以后单调；这里截断到索引17、18。
    term = F(1)
    total = term
    lower = None
    for k in range(1, 19):
        term *= -theta * theta / ((2 * k - 1) * (2 * k))
        total += term
        if k == 17:
            lower = total
    return max(F(-1), down(lower)), min(F(1), up(total))


def sqrt_lower(value):
    if value <= 0:
        raise ValueError("分母平方必须严格正")
    scaled = value.numerator * SCALE * SCALE // value.denominator
    result = F(math.isqrt(scaled), SCALE)
    if result <= 0 or result * result > value:
        raise ValueError("平方根下界无效")
    return result


def positive_exp_lower(value):
    term = F(1)
    total = term
    for k in range(1, 25):
        term *= value / k
        total += term
    return total


E_LOWER = positive_exp_lower(F(1))


def exp_upper(value):
    value = up(value)
    if value <= -32:
        # e>2；这里是故意宽松但严格的正上界，不丢掉远弧。
        return F(1, 1 << 32)
    if value < 0:
        magnitude = -value
        integer = magnitude.numerator // magnitude.denominator
        remainder = magnitude - integer
        return up(1 / (E_LOWER ** integer * positive_exp_lower(remainder)))
    if value > 1:
        raise ValueError("正指数超过本认证器的固定范围1；须调整分段/半径")
    partial = positive_exp_lower(value)
    first_tail = value ** 25 / math.factorial(25)
    return up(partial + first_tail / (1 - value / 26))


def kernel_max(radius, lo, hi):
    vertex = -1 / (2 * radius ** 3)
    candidates = [lo, hi]
    if lo <= vertex <= hi:
        candidates.append(vertex)
    return max(-F(2, 3) * x / radius - radius ** 2 * (2 * x * x - 1) / 3 - F(1, 2)
               for x in candidates)


def denominator_min(radius, lo, hi):
    candidates = [lo, hi]
    for critical in (F(-1, 2), F(1, 2)):
        if lo <= critical <= hi:
            candidates.append(critical)
    return min((1 - radius ** 3) ** 2 + 2 * radius ** 3 * (1 - x) * (2 * x + 1) ** 2
               for x in candidates)


def certify(endpoint, radius, cells):
    started = time.monotonic()
    if not (type(endpoint) is int and type(cells) is int
            and isinstance(radius, F) and 0 <= endpoint <= 10 ** 6
            and 0 < radius < 1 and radius.numerator <= 10 ** 6
            and radius.denominator <= 10 ** 6 and 8 <= cells <= MAX_CELLS):
        raise ValueError("超出冻结规模门：T整数0..10^6，有理R分子分母<=10^6，8<=cells<=8192")
    plo, phi = pi_bounds()
    nodes = []
    for k in range(cells + 1):
        if time.monotonic() - started > MAX_SECONDS:
            raise TimeoutError("端点认证超时；不得自动扩大规模重试")
        if k == 0:
            nodes.append((F(1), F(1)))
        elif k == cells:
            nodes.append((F(-1), F(-1)))
        else:
            lower, _ = cos_bounds(up(phi * k / cells))
            _, upper = cos_bounds(down(plo * k / cells))
            nodes.append((lower, upper))
    accumulator = 0
    for k in range(cells):
        if time.monotonic() - started > MAX_SECONDS:
            raise TimeoutError("端点认证超时；不得自动扩大规模重试")
        lo, hi = nodes[k + 1][0], nodes[k][1]
        height = kernel_max(radius, lo, hi)
        divisor = sqrt_lower(denominator_min(radius, lo, hi))
        term = up(exp_upper(endpoint * height) / divisor)
        accumulator += term.numerator * (SCALE // term.denominator)
    # 对称积分的pi与每格宽pi/N消掉；累加始终向上舍入。
    q_upper = 3 * radius ** 3 * F(accumulator, SCALE * cells)
    d_lower = 2 - exp_upper(-F(3, 2) * endpoint)
    passed = q_upper < d_lower
    return {
        "status": "CERTIFIED_ENDPOINT" if passed else "NOT_CERTIFIED",
        "T": endpoint,
        "R": str(radius),
        "cells": cells,
        "fixed_point_bits": BITS,
        "q_upper": str(q_upper),
        "d_lower": str(d_lower),
        "ratio_upper": str(q_upper / d_lower),
        "seconds": round(time.monotonic() - started, 6),
        "scope": "仅固定R、给定T的完整积分上界；非连续区间/全根性证明",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, required=True)
    parser.add_argument("--radius", required=True)
    parser.add_argument("--cells", type=int, default=256)
    args = parser.parse_args()
    if re.fullmatch(r"[0-9]{1,7}(?:/[0-9]{1,7})?", args.radius) is None:
        parser.error("半径仅接受有限长度的非负整数或分子/分母，不接受科学记数法")
    result = certify(args.T, F(args.radius), args.cells)
    print(json.dumps(result, ensure_ascii=False))
    if result["status"] != "CERTIFIED_ENDPOINT":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
