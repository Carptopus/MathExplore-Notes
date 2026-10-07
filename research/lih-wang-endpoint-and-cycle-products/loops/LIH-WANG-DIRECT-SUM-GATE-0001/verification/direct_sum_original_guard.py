"""完整小阶标量层与固定原直和矩阵控制，不认证全参数定理。"""

from collections import defaultdict
import ctypes
from ctypes import wintypes
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
from math import comb, factorial, prod
import os
from pathlib import Path
import threading
import time

START = time.monotonic()
STOP = threading.Event()
PEAK = 0


class Counters(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("faults", wintypes.DWORD)] + [
        (name, ctypes.c_size_t) for name in (
            "peak_working", "working", "peak_paged", "paged", "peak_nonpaged",
            "nonpaged", "pagefile", "peak_pagefile", "private")]


get_process = ctypes.WinDLL("kernel32", use_last_error=True).GetCurrentProcess
get_process.restype = wintypes.HANDLE
get_info = ctypes.WinDLL("psapi", use_last_error=True).GetProcessMemoryInfo
get_info.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
get_info.restype = wintypes.BOOL


def watchdog():
    if not STOP.wait(50):
        print("RESOURCE_TIMEOUT_50_SECONDS", flush=True)
        os._exit(3)


threading.Thread(target=watchdog, daemon=True).start()


def gate():
    global PEAK
    info = Counters()
    info.cb = ctypes.sizeof(info)
    if not get_info(get_process(), ctypes.byref(info), info.cb):
        raise ctypes.WinError(ctypes.get_last_error())
    PEAK = max(PEAK, info.peak_working, info.peak_pagefile, info.private)
    if PEAK > 128 * 1024 * 1024:
        raise MemoryError("128MiB资源门，不重试")


def occupancy_poly(occ):
    result = [F(1)]
    for value in occ:
        following = [F(0)] * (len(result) + 1)
        for k, coefficient in enumerate(result):
            following[k] += coefficient
            following[k + 1] += value * coefficient
        result = following
    return result


def gamma(poly, n, j):
    assert 4 <= n <= 7 and 0 <= j <= n and len(poly) == n + 1
    return sum(F(comb(j, k) * factorial(n - k), comb(n, k) * n ** (n - k))
               * poly[k] for k in range(j + 1)) / 2 ** j


def scalar_boundary():
    records = []
    for n in range(4, 8):
        bb = occupancy_poly([1] * n)
        f1 = occupancy_poly([2] + [1] * (n - 2) + [0])
        cn, p0 = F(factorial(n), n ** n), F(1, 2 ** (n - 2))
        env = [p0 * x + (1 - p0) * y for x, y in zip(bb, f1)]
        assert gamma(env, n, 0) == cn
        for j in range(1, n + 1):
            slope = F(j, 2 * n) - gamma(bb, n, j) + gamma(f1, n, j)
            margin = (1 - F(j, 2 * n)) * cn + F(j, 2 * n) * p0 - gamma(env, n, j)
            assert slope > 0 and margin > 0
            records.append(f'{n}:{j}:{slope}:{margin}')
        gate()
    assert len(records) == 22
    return hashlib.sha256('\n'.join(records).encode('ascii')).hexdigest()


def original_matrix(parts, fixed):
    n = fixed + sum(1 + sum(ell - 1 for ell in lengths) for lengths, _ in parts)
    assert 4 <= n <= 9 and len(parts) == 2
    aa = [[F(i == j) for j in range(n)] for i in range(n)]
    root, private, edges = 0, [], []
    for lengths, weights in parts:
        assert len(lengths) == len(weights) and sum(weights) <= 1
        following = root + 1
        for ell, weight in zip(lengths, weights):
            branch = list(range(following, following + ell - 1))
            cycle = [root, *branch]
            for i, row in enumerate(cycle):
                aa[row][row] -= weight
                aa[row][cycle[(i + 1) % ell]] += weight
            previous = root
            for vertex in branch:
                edges.append((previous, vertex, weight * (1 - weight)))
                previous = vertex
            private.extend(branch)
            following += ell - 1
        root = following
    assert all(sum(row) == 1 for row in aa)
    assert all(sum(aa[i][j] for i in range(n)) == 1 for j in range(n))
    return aa, private, edges


def rook_by_injective_partial_dp(aa):
    n, dp = len(aa), {0: F(1)}
    for row in aa:
        following = defaultdict(F)
        for mask, weight in dp.items():
            following[mask] += weight
            for col, value in enumerate(row):
                if value and not (mask >> col) & 1:
                    following[mask | (1 << col)] += weight * value
        dp = following
        gate()
    out = [F(0)] * (n + 1)
    for mask, weight in dp.items():
        out[mask.bit_count()] += weight
    return out


def permanent_dp(aa):
    n, dp = len(aa), {0: F(1)}
    for row in aa:
        following = defaultdict(F)
        for mask, weight in dp.items():
            for col, value in enumerate(row):
                if value and not (mask >> col) & 1:
                    following[mask | (1 << col)] += weight * value
        dp = following
        gate()
    return dp.get((1 << n) - 1, F(0))


def forest_distribution(edges, allow_conflicts=False):
    assert len(edges) <= 7
    out = [F(0)] * (len(edges) + 1)
    for mask in range(1 << len(edges)):
        used, coefficient, count = set(), F(1), 0
        for j, (u, v, alpha) in enumerate(edges):
            if (mask >> j) & 1:
                if not allow_conflicts and (u in used or v in used):
                    coefficient = F(0)
                    break
                used.update((u, v))
                coefficient *= alpha
                count += 1
        for d in range(count + 1):
            out[d] += coefficient * comb(count, d) * (-1) ** (count - d)
    return out


def matrix_control(parts, fixed):
    aa, private, edges = original_matrix(parts, fixed)
    n = len(aa)
    choices = [[(j, x) for j, x in enumerate(row) if x] for row in aa]
    count = prod(map(len, choices))
    assert count <= 4096
    rr = [F(0)] * (n + 1)
    dd = [F(0)] * (len(edges) + 1)
    pp = F(0)
    for sample in product(*choices):
        occupancy = [0] * n
        for col, _ in sample:
            occupancy[col] += 1
        weight = prod(value for _, value in sample)
        for k, coefficient in enumerate(occupancy_poly(occupancy)):
            rr[k] += weight * coefficient
        dd[sum(occupancy[col] == 2 for col in private)] += weight
        if all(value == 1 for value in occupancy):
            pp += weight
    assert rr == rook_by_injective_partial_dp(aa)
    assert rr[-1] == pp == permanent_dp(aa)
    assert dd == forest_distribution(edges)
    assert dd[0] != pp  # 私有零碰撞不等于原永久端点，真正走原计数路径。
    conflict_control = forest_distribution(edges, True) != dd
    cn = F(factorial(n), n ** n)
    for u in (F(1, 4), F(1, 2)):
        interpolated = [[u * aa[i][j] + (1 - u) / n for j in range(n)] for i in range(n)]
        actual = permanent_dp(interpolated)
        expanded = sum(factorial(n - k) * rr[k] * u ** k * ((1 - u) / n) ** (n - k)
                       for k in range(n + 1))
        wrong = sum(factorial(n - k) * rr[k] * u ** k * ((1 - u) / (n - 1)) ** (n - k)
                    for k in range(n + 1))
        assert actual == expanded and actual != wrong
        assert actual <= (1 - u) * cn + u * pp
    gate()
    return {"n": n, "row_choices": count, "rook_and_permanent": "EXACT",
            "forest_distribution": "EXACT", "two_u_original_chord": "PASSED",
            "conflicting_edges_control": "REJECTED" if conflict_control else "NO_CONFLICT_AT_THIS_POINT"}


def load_old(name):
    path = Path(__file__).resolve().parents[3] / 'loops' / 'LIH-WANG-NONCUBICAL-FACES-0001' / 'verification' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    digest = scalar_boundary()
    # 原窗口证书未改域/公式；一次串行重生成，为新应用保存实测收据。
    load_old('coupled_small_mean_guard').main()
    gate()
    load_old('poisson_boundary_window_guard').main()
    gate()
    cases = [
        ([((2,), (F(1, 2),)), ((2,), (F(1, 2),))], 0),
        ([((2, 2), (F(1, 4), F(1, 3))), ((2, 2), (F(1, 5), F(1, 4)))], 0),
        ([((3, 3), (F(1, 4), F(1, 3))), ((2, 2), (F(1, 3), F(1, 6)))], 0),
        ([((2, 3), (F(1, 4), F(1, 2))), ((3,), (F(2, 5),))], 2),
        ([((2, 3), (F(1, 3), F(2, 3))), ((3,), (F(0),))], 0),
    ]
    receipts = [matrix_control(parts, fixed) for parts, fixed in cases]
    assert sum(item['conflicting_edges_control'] == 'REJECTED' for item in receipts) >= 2
    print(json.dumps({"scope": "22_COMPLETE_SCALAR_LAYERS_AND_5_FIXED_ORIGINAL_MATRICES",
                      "low_window_sha256": digest, "matrices": receipts,
                      "negative_controls": "FALSE_ZERO_COLLISION_ENDPOINT_AND_GLOBAL_NORMALIZATION_REJECTED",
                      "all_parameters": "NOT_CHECKED", "full_Lih_Wang": "NOT_CHECKED",
                      "seconds": time.monotonic() - START, "peak_bytes": PEAK}))
    STOP.set()


if __name__ == '__main__':
    main()
