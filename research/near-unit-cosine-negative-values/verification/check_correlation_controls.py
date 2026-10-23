"""S7有限精确控制：Fourier符号、稀疏支持及破坏性对照；不认证一般定理。"""

import argparse
import hashlib
import json
import time
from fractions import Fraction as R
from pathlib import Path


# 高斯有理数，避免浮点误差掩盖共轭或调制符号错误。
ZERO = (R(0), R(0))
ONE = (R(1), R(0))
IMAG = (R(0), R(1))


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[0], -a[1]


def mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def conj(a):
    return a[0], -a[1]


def square_norm(a):
    return a[0] ** 2 + a[1] ** 2


def product(f, g):
    """函数点乘的Fourier系数，由有限离散卷积独立组装。"""
    out = {}
    for i, a in f.items():
        for j, b in g.items():
            out[i + j] = add(out.get(i + j, ZERO), mul(a, b))
    return out


def run_controls():
    started = time.monotonic()
    supports = ((1, 2), tuple(range(1, 9)), (1, 2, 4, 8), (2, 3, 5, 7, 10))
    profiles = (
        ((R(1), R(0)),),
        ((R(979, 1000), R(0)), (R(1021, 1000), R(0))),
        ((R(1), R(21, 1000)), (R(1), R(-21, 1000)), (R(1), R(0))),
    )
    count = 0
    saw_phase_sensitive_square = False
    saw_nonzero_auxiliary_mean = False
    saw_bad_unselected_column = False
    for positive in supports:
        a_set = set(positive) | {-m for m in positive}
        assert len(a_set) <= 32 and max(a_set) <= 32
        total = sum(m - t in a_set for m in a_set for t in a_set)
        columns = {}
        for t in a_set:
            boundary = {m for m in a_set if m - t in a_set and m + t not in a_set}
            inside = {m for m in a_set if m - t in a_set and m + t in a_set}
            columns[t] = boundary, inside
            saw_bad_unselected_column |= len(inside) > 4 * len(boundary)
        assert 3 * sum(len(b) for b, _ in columns.values()) >= total
        good = [(t, b, i) for t, (b, i) in columns.items() if len(i) <= 4 * len(b)]
        assert any(6 * len(a_set) * len(b) >= total for _, b, _ in good)
        for profile in profiles:
            weights = {}
            for j, m in enumerate(positive):
                weights[m] = profile[j % len(profile)]
                weights[-m] = conj(weights[m])
            assert all(square_norm(add(c, neg(ONE))) <= R(21, 1000) ** 2 for c in weights.values())
            for t, boundary, inside in good:
                if time.monotonic() - started > 30:
                    raise RuntimeError('有限控制超过30秒硬门')
                # h=F⋆J⋆D⋆D：系数逐项乘积；J,D另按调制移位构造。
                j_coeff = {m + t: c for m, c in weights.items()}
                d_coeff = {m + t: c for m, c in weights.items()}
                for m, c in weights.items():
                    d_coeff[m - t] = add(d_coeff.get(m - t, ZERO), neg(c))
                h_coeff = {
                    m: mul(mul(c, j_coeff.get(m, ZERO)), mul(d_coeff.get(m, ZERO), d_coeff.get(m, ZERO)))
                    for m, c in weights.items()
                }
                for m, value in h_coeff.items():
                    if m not in boundary | inside:
                        assert value == ZERO
                    if m in boundary:
                        assert square_norm(value) > R(91, 100) ** 2
                    if m in inside:
                        assert square_norm(value) < R(2, 1000) ** 2
                    # 正控：共轭反射后环面卷积确得模平方。
                    assert mul(value, conj(value)) == (square_norm(value), R(0))
                    # 破坏控：删去共轭通常就不再是模平方。
                    saw_phase_sensitive_square |= mul(value, value) != (square_norm(value), R(0))
                # 从函数乘法独立构造F±，检查辅助均值及共轭实性。
                plus = product(weights, {0: (R(2), R(0)), t: neg(IMAG), -t: IMAG})
                minus = product(weights, {0: (R(2), R(0)), t: IMAG, -t: neg(IMAG)})
                assert plus.get(0, ZERO) == (-2 * weights[t][1], R(0))
                assert minus.get(0, ZERO) == (2 * weights[t][1], R(0))
                saw_nonzero_auxiliary_mean |= plus.get(0, ZERO) != ZERO
                for f in (plus, minus):
                    assert all(f.get(-m, ZERO) == conj(c) for m, c in f.items())
                for m in set(plus) | set(minus):
                    z_p = add(mul((R(2), R(0)), weights.get(m, ZERO)), mul(IMAG, add(weights.get(m + t, ZERO), neg(weights.get(m - t, ZERO)))))
                    assert plus.get(m, ZERO) == z_p
                w = sum(square_norm(h_coeff.get(m, ZERO)) for m in boundary)
                e = sum(square_norm(c) for m, c in h_coeff.items() if m not in boundary)
                if w:
                    assert e <= 4 * (R(2, 1000) / R(91, 100)) ** 2 * w
                count += 1
    assert saw_phase_sensitive_square, '破坏控未击中：共轭省略'
    assert saw_nonzero_auxiliary_mean, '正控未覆盖：复辅助均值非零'
    assert saw_bad_unselected_column, '负控未覆盖：任意列不可假定内部/边界比有界'
    assert R(234, 10) * 4 * (R(2, 1000) / R(91, 100)) ** 2 == R(36, 79625)
    assert R(180 * 128 * 64 ** 2) / R(91, 100) ** 2 < 120000000
    return {
        'status': 'PASS', 'column_profile_checks': count,
        'controls': {'conjugate_omission_detected': True, 'nonzero_auxiliary_mean': True,
                     'unselected_bad_column_detected': True},
        'arithmetic': 'exact Gaussian rationals; no numerical integration',
        'scope': 'finite identities, support localization and constants only; not a proof or memory certification',
        'elapsed_seconds': round(time.monotonic() - started, 4),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
