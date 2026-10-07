"""四次核固定半径端点完整积分有理认证；单端点不代表连续全轴。"""

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import time
from fractions import Fraction as F


DEPENDENCY_HASH = "650ED1CDB8AD6089E8A7294411B7C1EBEC768F05D40DB55431D026046D8EE669"
DEPENDENCY = (Path(__file__).resolve().parents[2]
              / "PAVING-HSTAR-MOVING-CRITICAL-GATE-0001"
              / "verification" / "fixed_radius_endpoint_certificate.py")
if hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest().upper() != DEPENDENCY_HASH:
    raise RuntimeError("冻结有理运算依赖哈希不匹配，停止认证")
spec = importlib.util.spec_from_file_location("frozen_rational_bounds", DEPENDENCY)
bounds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bounds)

SCALE = bounds.SCALE
MAX_CELLS = 8192
MAX_SECONDS = 45


def sqrt_upper(value):
    if value < 0:
        raise ValueError("平方根输入不能负")
    scaled = value.numerator * SCALE * SCALE // value.denominator
    root = math.isqrt(scaled)
    answer = F(root, SCALE)
    if answer * answer < value:
        answer = F(root + 1, SCALE)
    if answer * answer < value:
        raise ValueError("平方根上界无效")
    return answer


def kernel_max(radius, lo, hi, c_lower):
    coefficient = F(3, 4) * (1 / radius + radius ** 3)
    values = [coefficient * u - radius ** 3 * u ** 3 - c_lower
              for u in (lo, hi)]
    peak_squared = (1 + radius ** -4) / 4
    peak_lo = bounds.sqrt_lower(peak_squared)
    peak_hi = sqrt_upper(peak_squared)
    if lo <= peak_hi and hi >= peak_lo:
        # 正驻点是三次核极大点；负驻点为极小点，不影响最大值。
        values.append(2 * radius ** 3 * peak_hi ** 3 - c_lower)
    return max(values)


def denominator_min(radius, lo, hi, c_lo, c_hi):
    constant = (1 - radius ** 4) ** 2
    values = [constant + 4 * radius ** 4 * (2 * u * u - 1) ** 2
              for u in (lo, hi)]
    if ((lo <= c_hi and hi >= c_lo)
            or (lo <= -c_lo and hi >= -c_hi)):
        # 两个真实极小点可能在格内时，采用准确的全局最小值。
        values.append(constant)
    return min(values)


def certify(endpoint, radius, cells):
    started = time.monotonic()
    if not (type(endpoint) is int and type(cells) is int
            and isinstance(radius, F) and 0 <= endpoint <= 10 ** 6
            and 0 < radius < 1 and radius.numerator <= 10 ** 6
            and radius.denominator <= 10 ** 6 and 8 <= cells <= MAX_CELLS):
        raise ValueError("超出冻结规模门：整数T=0..10^6，有理R分子分母<=10^6，8<=cells<=8192")
    plo, phi = bounds.pi_bounds()
    sqrt2_lo = bounds.sqrt_lower(F(2))
    sqrt2_hi = sqrt_upper(F(2))
    c_lo, c_hi = sqrt2_lo / 2, sqrt2_hi / 2
    nodes = []
    for k in range(cells + 1):
        if time.monotonic() - started > MAX_SECONDS:
            raise TimeoutError("端点认证超时，不得自动扩大规模重试")
        if k == 0:
            nodes.append((F(1), F(1)))
        elif k == cells:
            nodes.append((F(-1), F(-1)))
        else:
            lower, _ = bounds.cos_bounds(bounds.up(phi * k / cells))
            _, upper = bounds.cos_bounds(bounds.down(plo * k / cells))
            nodes.append((lower, upper))
    accumulator = 0
    for k in range(cells):
        if time.monotonic() - started > MAX_SECONDS:
            raise TimeoutError("端点认证超时，不得自动扩大规模重试")
        lo, hi = nodes[k + 1][0], nodes[k][1]
        height = kernel_max(radius, lo, hi, c_lo)
        divisor = bounds.sqrt_lower(denominator_min(radius, lo, hi, c_lo, c_hi))
        term = bounds.up(bounds.exp_upper(endpoint * height) / divisor)
        accumulator += term.numerator * (SCALE // term.denominator)
    # 完整角积分对称成2*[0,pi]；格宽pi/N与规范2pi严格相消。
    q_upper = 4 * radius ** 4 * F(accumulator, SCALE * cells)
    d_lower = 2 - 2 * bounds.exp_upper(-sqrt2_lo * endpoint)
    passed = d_lower > 0 and q_upper < d_lower
    return {
        "status": "CERTIFIED_ENDPOINT" if passed else "NOT_CERTIFIED",
        "T": endpoint, "R": str(radius), "cells": cells,
        "fixed_point_bits": bounds.BITS,
        "q_upper": str(q_upper), "d_lower": str(d_lower),
        "ratio_upper": str(q_upper / d_lower) if d_lower > 0 else None,
        "dependency_sha256": DEPENDENCY_HASH,
        "seconds": round(time.monotonic() - started, 6),
        "scope": "仅四次核固定R及T的完整积分有理上界，非连续区间或全根性",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--T", type=int, required=True)
    parser.add_argument("--radius", required=True)
    parser.add_argument("--cells", type=int, default=512)
    args = parser.parse_args()
    if re.fullmatch(r"[0-9]{1,7}(?:/[0-9]{1,7})?", args.radius) is None:
        parser.error("半径仅接受有限长度非负整数或分子/分母，不接受科学记数法")
    result = certify(args.T, F(args.radius), args.cells)
    print(json.dumps(result, ensure_ascii=False))
    if result["status"] != "CERTIFIED_ENDPOINT":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
