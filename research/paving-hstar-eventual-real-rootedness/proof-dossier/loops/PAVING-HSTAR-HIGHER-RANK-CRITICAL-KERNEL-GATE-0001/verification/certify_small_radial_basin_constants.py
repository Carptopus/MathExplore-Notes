"""S85 两个固定积分上界的有理证书；不是秩/参数抽样。"""

from fractions import Fraction as F
from math import isqrt
import json
import sys
import time
import ctypes
from ctypes import wintypes


if len(sys.argv) != 1:
    raise SystemExit("固定证书不接受参数")

START = time.monotonic()
class ProcessMemoryCounters(ctypes.Structure):
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
psapi.GetProcessMemoryInfo.argtypes = [
    wintypes.HANDLE, ctypes.POINTER(ProcessMemoryCounters), wintypes.DWORD,
]
psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
PROCESS = kernel32.GetCurrentProcess()
ROUND = 10**30
CELL_ROUND = 10**12
MAX_SECONDS = 60
MAX_RSS = 256 * 1024**2
PEAK_RSS = 0
EXP_CALLS = 0


def resource_guard():
    global PEAK_RSS
    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    if not psapi.GetProcessMemoryInfo(PROCESS, ctypes.byref(counters), counters.cb):
        raise ctypes.WinError(ctypes.get_last_error())
    rss = counters.WorkingSetSize
    PEAK_RSS = max(PEAK_RSS, rss)
    if rss > MAX_RSS or time.monotonic() - START > MAX_SECONDS:
        raise RuntimeError("S85固定证书超过内存或时间硬门，禁止自动重试")


def round_down(value, scale=ROUND):
    return F((value.numerator * scale) // value.denominator, scale)


def round_up(value, scale=ROUND):
    return F(-((-value.numerator * scale) // value.denominator), scale)


def exp_interval(value):
    """正项24阶加几何余项；负指数取倒数，平方时向外取整。"""
    global EXP_CALLS
    EXP_CALLS += 1
    if EXP_CALLS > 1600:
        raise RuntimeError("固定证书指数调用数越门")
    resource_guard()
    positive = abs(value)
    squares = 0
    while positive > 1:
        positive /= 2
        squares += 1
    term = total = F(1)
    for degree in range(1, 25):
        term *= positive / degree
        total += term
    next_term = term * positive / 25
    lower = round_down(total)
    upper = round_up(total + next_term / (1 - positive / 26))
    for _ in range(squares):
        lower = round_down(lower * lower)
        upper = round_up(upper * upper)
    if value < 0:
        return round_down(1 / upper), round_up(1 / lower)
    return lower, upper


def sqrt_lower(value):
    """12位十进有理下界；只用整数平方根，不用浮点sqrt。"""
    integer = isqrt((value.numerator * CELL_ROUND**2) // value.denominator)
    lower = F(integer, CELL_ROUND)
    assert lower > 0 and lower * lower <= value
    assert (lower + F(1, CELL_ROUND)) ** 2 > value
    return lower


def fixed_integral_upper(curvature, tilt):
    # [0,12]分成240个闭区间，每项取逐因子的有效上界。
    width = F(1, 20)
    total = F(0)
    for cell in range(240):
        left, right = cell * width, (cell + 1) * width
        gaussian = exp_interval(-curvature * left**2 / 2)[1]
        cosh = (exp_interval(tilt * right)[1] + exp_interval(-tilt * right)[1]) / 2
        denominator = sqrt_lower(F(2, 9) + F(979, 1000) * left**2)
        total += round_up(width * gaussian * cosh / denominator, CELL_ROUND)
    # z>=12：cosh(bz)<=exp(bz)，指数斜率<=-(12A-b)，分母>=.989*12。
    edge = F(12)
    assert curvature * edge > tilt
    assert F(989, 1000) ** 2 < F(979, 1000)
    tail = exp_interval(-curvature * edge**2 / 2 + tilt * edge)[1]
    tail /= F(989, 1000) * edge * (curvature * edge - tilt)
    return round_up(F(1118, 3141) * (total + tail), CELL_ROUND)


def require_upper(bound, target):
    if not bound < target:
        raise ValueError("证书无法支付指定严格上界")


leading = fixed_integral_upper(F(685, 1000), F(278, 1000))
other = fixed_integral_upper(F(339, 1000), F(410, 1000))
outer = F(500, 3) * exp_interval(-F(454, 9))[1]
require_upper(outer, F(1, 10**18))
require_upper(leading + outer, F(7, 10))
require_upper(other + outer, F(9, 10))

# 正控：指数零精确包住1、逆指数区间互相包容、平方根下界方向。
zero = exp_interval(F(0))
assert zero[0] == zero[1] == 1
ep, en = exp_interval(F(1, 2)), exp_interval(-F(1, 2))
assert ep[0] * en[0] <= 1 <= ep[1] * en[1]
assert sqrt_lower(F(4)) == 2

# 负控：破坏阈值必须被拒绝；不把拒绝当作真实积分的下界证明。
rejected = 0
for bound, bad_target in [(leading, F(3, 5)), (other, F(4, 5))]:
    try:
        require_upper(bound, bad_target)
    except ValueError:
        rejected += 1
assert rejected == 2
resource_guard()
print(json.dumps({
    "status": "VERIFIED_FIXED_S85_INTEGRAL_CONSTANTS_ONLY",
    "cells_per_integral": 240,
    "arithmetic": "Fraction / outward rational rounding / integer sqrt",
    "leading_upper": str(leading),
    "other_upper": str(other),
    "outer_upper": str(round_up(outer, 10**25)),
    "negative_controls_rejected": rejected,
    "exp_calls": EXP_CALLS,
    "elapsed_seconds": round(time.monotonic() - START, 3),
    "peak_rss_bytes": PEAK_RSS,
    "all_parameter_basin_proof": False,
}, ensure_ascii=False, indent=2))
