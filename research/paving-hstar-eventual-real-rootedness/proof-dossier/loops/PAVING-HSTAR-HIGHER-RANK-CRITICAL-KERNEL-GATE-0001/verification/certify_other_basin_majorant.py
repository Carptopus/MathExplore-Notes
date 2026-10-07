"""S88其他好盆地一维主控的连续有理上界；失败不反证原H。"""

from fractions import Fraction as F
from pathlib import Path
import ctypes
from ctypes import wintypes
import hashlib
import importlib.util
import json
import sys
import time


if len(sys.argv) != 1:
    raise SystemExit("固定连续证书不接受参数")
START = time.monotonic()
DEPENDENCY = Path(__file__).resolve().parents[2] / "PAVING-HSTAR-MOVING-CRITICAL-GATE-0001" / "verification" / "fixed_radius_endpoint_certificate.py"
DEPENDENCY_HASH = "650ED1CDB8AD6089E8A7294411B7C1EBEC768F05D40DB55431D026046D8EE669"
if hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest().upper() != DEPENDENCY_HASH:
    raise RuntimeError("冻结有理库哈希不符")
spec = importlib.util.spec_from_file_location("frozen_basin_bounds", DEPENDENCY)
bounds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bounds)

MAX_SECONDS = 120
MAX_EVALS = 256
MAX_DEPTH = 20
MAX_RSS = 256 * 1024**2
NODES = 256
K = F(2, 9)
PLO, PHI = bounds.pi_bounds()
PEAK_RSS = 0
EVALS = 0


class MemoryCounters(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
        (name, ctypes.c_size_t) for name in (
            "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
            "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
            "PagefileUsage", "PeakPagefileUsage", "PrivateUsage",
        )
    ]


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
psapi = ctypes.WinDLL("psapi", use_last_error=True)
kernel32.GetCurrentProcess.argtypes = []
kernel32.GetCurrentProcess.restype = wintypes.HANDLE
psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(MemoryCounters), wintypes.DWORD]
psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
PROCESS = kernel32.GetCurrentProcess()


def guard():
    global PEAK_RSS
    data = MemoryCounters()
    data.cb = ctypes.sizeof(data)
    if not psapi.GetProcessMemoryInfo(PROCESS, ctypes.byref(data), data.cb):
        raise ctypes.WinError(ctypes.get_last_error())
    PEAK_RSS = max(PEAK_RSS, data.PeakWorkingSetSize)
    if data.PeakWorkingSetSize > MAX_RSS or time.monotonic() - START > MAX_SECONDS:
        raise RuntimeError("连续证书资源越门；禁止扩大或自动重试")


def sqrt_upper(value):
    import math
    root = math.isqrt(value.numerator * bounds.SCALE**2 // value.denominator)
    answer = F(root, bounds.SCALE)
    if answer * answer < value:
        answer += F(1, bounds.SCALE)
    assert answer * answer >= value
    return answer


def cosine(multiplier):
    # 每处使用的|multiplier|<=2；利用偶性和2pi周期只送[0,pi]到旧库。
    multiplier = abs(multiplier)
    if multiplier > 1:
        multiplier = 2 - multiplier
    if not 0 <= multiplier <= 1:
        raise ValueError("余弦角域越门")
    lower = bounds.cos_bounds(bounds.up(PHI * multiplier))[0]
    upper = bounds.cos_bounds(bounds.down(PLO * multiplier))[1]
    return lower, upper


CLOW = F(1, 2)
CQUARTER = cosine(F(3, 8))[0]
SQRT3_UPPER = sqrt_upper(F(3))


def sin_squared(multiplier):
    clo, chi = cosine(multiplier)
    return max(F(0), bounds.down((1 - chi) / 2)), bounds.up((1 - clo) / 2)


def left_loss_lower(s):
    if s == 0:
        return F(0)
    if s <= F(1, 3):
        sin_lower = bounds.sqrt_lower(sin_squared(2 * s)[0])
        # sin(t)-t<=0，因此sqrt(3)取上界、t取pi上界，得到损失下界。
        return max(F(0), bounds.down(K * (
            (1 - cosine(s)[1]) / 2
            + SQRT3_UPPER * (sin_lower - PHI * s) / 2
        )))
    if s == 1:
        return 2 * K
    if s <= F(3, 7):
        lam, alpha = (1 - 1 / (3 * s)) / 2, F(1, 3)
    else:
        lam = (1 - s) / (2 * (3 - s))
        alpha = 3 * lam
    ca = cosine(alpha)[0]
    return max(F(0), bounds.down(K * (
        (ca - cosine(alpha + (1 - lam) * s)[1]) / (1 - lam)
        + (ca - cosine(lam * s - alpha)[1]) / lam
    )))


def left_force_upper(s):
    sine = sqrt_upper(sin_squared(s)[1])
    if s <= F(1, 3):
        return bounds.up(cosine(F(1, 6) - s / 2)[1] * sine)
    return sine


def right_first_loss_lower(s):
    return max(F(0), bounds.down(K * (
        (CLOW - cosine(F(1, 3) + s / 9)[1]) * 9
        + (CLOW - cosine(F(8, 9) * s - F(1, 3))[1]) * F(9, 8)
    )))


UQUARTER = right_first_loss_lower(F(3, 8))
UPI = bounds.down(UQUARTER + K * (CQUARTER + 1))


def right_loss_lower(s):
    if s <= F(3, 8):
        return right_first_loss_lower(s)
    if s <= 1:
        return max(F(0), bounds.down(UQUARTER + K * (CQUARTER - cosine(s)[1])))
    return UPI


def make_cells():
    cells = []
    first = [F(index**2, NODES**2) for index in range(NODES + 1)]
    last = sorted(2 - item for item in first)
    left_nodes = sorted(set(first + [F(1, 3), F(3, 7)]))
    right_nodes = sorted(set(first + [F(3, 8)]))
    for kind, nodes in [("left", left_nodes), ("right_head", right_nodes), ("right_tail", last)]:
        for lo, hi in zip(nodes, nodes[1:]):
            guard()
            if kind == "left":
                loss = left_loss_lower(lo)
                force = left_force_upper(hi)
                denominator = sin_squared(lo)[0]
            elif kind == "right_head":
                loss, force = right_loss_lower(lo), sin_squared(hi)[1]
                denominator = sin_squared(lo)[0]
            else:
                loss, force = right_loss_lower(lo), sqrt_upper(sin_squared(lo)[1])
                denominator = sin_squared(hi)[0]
            cells.append((hi - lo, loss, force, denominator))
    assert len(cells) == 3 * NODES + 3
    return cells


CELLS = make_cells()


def box_upper(a, b):
    global EVALS
    EVALS += 1
    if EVALS > MAX_EVALS:
        raise RuntimeError("连续证书盒数越门，不扩规模")
    # sinh(a/2)的正项下界；整个y盒的分母和exp(-y/2)由左端控制。
    h = a / 2
    sinh_lower = h + h**3 / 6 + h**5 / 120
    tlo, thi = 1 / b, 1 / a
    accumulator = F(0)
    for width, loss, force, denominator in CELLS:
        guard()
        tilt = 2 * K * force
        if loss:
            vertex = tilt / (2 * loss)
            t = max(tlo, min(thi, vertex))
        else:
            t = thi
        exponent = K / 2 - loss * t * t + tilt * t
        if exponent > 1:
            return None
        divisor = bounds.sqrt_lower(sinh_lower**2 + denominator)
        accumulator += bounds.up(width * bounds.exp_upper(exponent) / divisor)
    # v=pi*s，积分微元的pi与原规范4pi准确相消。
    return bounds.up(bounds.exp_upper(-a / 2) * accumulator / 4)


def check_cover(rows):
    ordered = sorted(rows)
    cursor = F(1, 100)
    for a, b, upper in ordered:
        if a != cursor or not a < b or not upper < F(13, 10):
            raise ValueError("连续覆盖、正宽或严格上界失败")
        cursor = b
    if cursor != F(51, 100):
        raise ValueError("连续覆盖未到准确终点")


stack = [(F(1, 100), F(51, 100), 0)]
rows = []
while stack:
    a, b, depth = stack.pop()
    upper = box_upper(a, b)
    if upper is not None and upper < F(13, 10):
        rows.append((a, b, upper))
    else:
        if depth >= MAX_DEPTH:
            raise RuntimeError("固定细分深度未认证；不是真实H反例")
        middle = (a + b) / 2
        stack.extend([(a, middle, depth + 1), (middle, b, depth + 1)])
check_cover(rows)

# 正控解析零值；负控故意破坏完整覆盖与最终阈值，必须被拒绝。
assert left_loss_lower(F(0)) == right_first_loss_lower(F(0)) == 0
assert cosine(F(0))[0] <= 1 <= cosine(F(0))[1]
rejected = 0
for broken in [rows[:-1], [(F(1, 100), F(51, 100), F(13, 10))]]:
    try:
        check_cover(broken)
    except ValueError:
        rejected += 1
assert rejected == 2
payload = [[str(a), str(b), str(upper)] for a, b, upper in sorted(rows)]
guard()
print(json.dumps({
    "status": "CERTIFIED_CONTINUOUS_JOTHER_ONLY",
    "y_domain": ["1/100", "51/100"],
    "dependency_sha256": DEPENDENCY_HASH,
    "cells_per_box": len(CELLS),
    "box_evaluations": EVALS,
    "accepted_boxes": len(rows),
    "worst_upper": str(max(upper for _, _, upper in rows)),
    "coverage_sha256": hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest(),
    "negative_controls_rejected": rejected,
    "seconds": round(time.monotonic() - START, 3),
    "system_peak_working_set_bytes": PEAK_RSS,
    "resource_guard": "逐格与输出前协作式检查；非OS分配硬限",
    "scope": "仅S88其他好盆地一维主控连续积分；完整Q<P未付",
}, ensure_ascii=False, indent=2))
