"""495个完整端点阈值标量层及无限n锚点，不采样原矩阵。"""

from fractions import Fraction as F
import hashlib
import json
from math import comb, factorial
import time

import direct_sum_original_guard as limits


def gamma(poly, n, j):
    assert 2 <= n <= 32 and 0 <= j <= n and len(poly) == n + 1
    return sum(F(comb(j, k) * factorial(n - k), comb(n, k) * n ** (n - k)) * poly[k]
               for k in range(j + 1)) / 2 ** j


def layer_contract(n, p0):
    assert 2 <= n <= 31 and 0 <= p0 <= 1
    bb = limits.occupancy_poly([1] * n)
    f1 = limits.occupancy_poly([2] + [1] * (n - 2) + [0])
    cn = F(factorial(n), n ** n)
    env = [p0 * x + (1 - p0) * y for x, y in zip(bb, f1)]
    assert gamma(env, n, 0) == cn
    result = []
    for j in range(1, n + 1):
        slope = F(j, 2 * n) - gamma(bb, n, j) + gamma(f1, n, j)
        margin = (1 - F(j, 2 * n)) * cn + F(j, 2 * n) * p0 - gamma(env, n, j)
        result.append((j, slope, margin))
    limits.gate()
    return result


def accepts(rows):
    return all(slope > 0 and margin > 0 for _, slope, margin in rows)


def main():
    records = []
    for n in range(2, 32):
        rows = layer_contract(n, F(1, 2 ** (n - 2)))
        assert accepts(rows)
        records.extend(f'{n}:{j}:{slope}:{margin}' for j, slope, margin in rows)
    assert len(records) == 495
    # 真实删除端点假设后，必须经过相同层契约拒绝，而非只比较两个阈值。
    assert not accepts(layer_contract(4, F(0)))
    n = 32
    bb = limits.occupancy_poly([1] * n)
    f1 = limits.occupancy_poly([2] + [1] * (n - 2) + [0])
    phi_i, phi_f1 = gamma(bb, n, n), gamma(f1, n, n)
    zn, cn = F(1, 2 ** (n - 1)), F(factorial(n), n ** n)
    assert phi_f1 == zn - (phi_i - zn) / (n - 1)
    assert F(0) <= phi_f1 <= zn and phi_i < F(1, 1024)
    assert F(4, 3) ** 32 > 80
    assert F(22, 7) < 4  # C32<10的有理pi上界。
    assert cn / 2 - 2 * zn * phi_i > 0
    limits.gate()
    print(json.dumps({"scope": "COMPLETE_495_SCALAR_LAYERS_PLUS_N32_ANCHOR",
                      "layers": 495,
                      "certificate_sha256": hashlib.sha256('\n'.join(records).encode('ascii')).hexdigest(),
                      "drop_endpoint_hypothesis": "REJECTED_BY_SAME_LAYER_CONTRACT",
                      "infinite_n": "REQUIRES_ANALYTIC_PROOF_AUDIT",
                      "all_matrices": "NOT_CHECKED", "full_Lih_Wang": "NOT_CHECKED",
                      "seconds": time.monotonic() - limits.START, "peak_bytes": limits.PEAK}))
    limits.STOP.set()


if __name__ == '__main__':
    main()
