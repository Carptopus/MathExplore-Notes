"""S22 固定紧域有理区间及 N<256 有限补集；不单独确认原全核定理。"""

import ctypes
import json
import time
from fractions import Fraction
from math import comb, factorial
from ctypes import wintypes

SCALE = 1 << 96
MAX_DEPTH = 24
MAX_LEAVES = 100000
MAX_SECONDS = 120
MAX_PRIVATE = 128 * 1024 * 1024
START = time.perf_counter()
PEAK_PRIVATE = 0


class MemoryCounters(ctypes.Structure):
    _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD),
                ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t),
                ('PrivateUsage', ctypes.c_size_t)]


def resource_check():
    global PEAK_PRIVATE
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi = ctypes.WinDLL('psapi', use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]
    counters = MemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
        raise RuntimeError('无法核验当前 Python worker 内存，不报告资源保护通过')
    PEAK_PRIVATE = max(PEAK_PRIVATE, counters.PrivateUsage)
    if counters.PrivateUsage > MAX_PRIVATE or time.perf_counter() - START > MAX_SECONDS:
        raise RuntimeError('资源门触发；停止且不得自动重试')


class I:
    """2^-96 格上的外向有理区间，每次运算均向外取整。"""
    def __init__(self, lo, hi=None):
        lo, hi = Fraction(lo), Fraction(lo if hi is None else hi)
        self.lo = lo.numerator * SCALE // lo.denominator
        self.hi = -((-hi.numerator * SCALE) // hi.denominator)

    @classmethod
    def ticks(cls, lo, hi):
        value = cls.__new__(cls)
        value.lo, value.hi = lo, hi
        assert lo <= hi
        return value

    def __add__(self, other):
        other = iv(other)
        return I.ticks(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I.ticks(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -iv(other)

    def __rsub__(self, other):
        return iv(other) - self

    def __mul__(self, other):
        other = iv(other)
        products = [self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi]
        return I.ticks(min(products) // SCALE, -((-max(products)) // SCALE))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = iv(other)
        assert other.lo > 0, '区间除数必须严格正'
        quotients = [(a * SCALE, b) for a in (self.lo, self.hi)
                     for b in (other.lo, other.hi)]
        return I.ticks(min(a // b for a, b in quotients),
                       max(-((-a) // b) for a, b in quotients))

    def __rtruediv__(self, other):
        return iv(other) / self


def iv(value):
    return value if isinstance(value, I) else I(value)


def prefix_lower(a, e):
    degree = min(20, (a.lo - e.hi) // (2 * e.hi))
    if degree < 1:
        return None
    v = e * e
    t = I(Fraction(4142135623730950, 10**16), Fraction(4142135623730951, 10**16))
    rho = I.ticks((4 / (1 + t + t * v / 2)).lo,
                  (4 / (1 + t + (t - 1) * v / 2)).hi)
    b = [I(1), -Fraction(1, 2) + Fraction(5, 4) * v + (1 - v) * rho / 8]
    for j in range(degree - 1):
        b.append(-Fraction(1, 2) * ((1 - Fraction(6*j + 11, 2) * v) * b[-1]
                       + (Fraction(1, 4) - Fraction(4*j + 5, 4) * v
                          + (j + 1) * Fraction(2*j + 3, 2) * v * v) * b[-2]))
    product, total = I(1), I(0)
    for j in range(degree + 1):
        if j:
            for r in (2*j - 1, 2*j):
                product = product * (a - r * e) / (1 - r * v)
        correction = 1 - Fraction(2*j + 1, 2*j + 2) * (a * e - (2*j + 1) * v) / (1 - (2*j + 1) * v)
        total += b[j] * product * correction / ((2*j + 1) * factorial(j))
    x = Fraction(3, 4) * Fraction(a.hi, SCALE)**2 / (1 - 2*Fraction(e.hi, SCALE)**2)**2
    if x >= degree + 2:
        return None
    tail = x**(degree + 1) / (factorial(degree + 1) * (2*degree + 3)) / (1 - x/(degree + 2))
    return total.lo - I(tail).hi


def interval_certificate():
    stack = [(Fraction(13, 20), Fraction(49, 16), Fraction(0), Fraction(1, 16), 0)]
    leaves, lowest, deepest, nodes = 0, SCALE, 0, 0
    while stack:
        al, ah, el, eh, depth = stack.pop()
        nodes += 1
        if nodes % 32 == 0:
            resource_check()
        lower = prefix_lower(I(al, ah), I(el, eh))
        if lower is not None and lower > SCALE // 2:
            leaves += 1
            lowest, deepest = min(lowest, lower), max(deepest, depth)
        else:
            if depth >= MAX_DEPTH or nodes >= 2 * MAX_LEAVES:
                raise RuntimeError('紧域有理证书未闭合；不能报告 PASS')
            if (ah - al) / Fraction(193, 80) >= (eh - el) / Fraction(1, 16):
                mid = (al + ah) / 2
                stack += [(al, mid, el, eh, depth + 1), (mid, ah, el, eh, depth + 1)]
            else:
                mid = (el + eh) / 2
                stack += [(al, ah, el, mid, depth + 1), (al, ah, mid, eh, depth + 1)]
        if leaves >= MAX_LEAVES:
            raise RuntimeError('叶盒硬门触发')
    return {'leaves': leaves, 'nodes': nodes, 'deepest': deepest,
            'minimum_lower': str(Fraction(lowest, SCALE)), 'precision_bits': 96}


def integer_row(n, end, d0_sign=1):
    assert 4 <= n <= 252 and n % 4 == 0 and 0 <= end <= n
    # 来自原中央二项式身份，均以 2^N 归一为整数。
    b = (-1)**(n // 4) * sum((-1)**m * comb(n, 2*m) * comb(2*m, m) * 2**(n - 2*m)
                             for m in range(n // 2 + 1))
    d0 = d0_sign * (-1)**(n // 4) * sum((-1)**(m + 1) * m * comb(n, 2*m) * comb(2*m, m) * 2**(n - 2*m)
                                        for m in range(1, n // 2 + 1))
    initial = (2**(3*n // 2) - b) // 2
    assert 2 * initial == 2**(3*n // 2) - b
    w = [d0, (n - 2)*d0]
    numerator = (4*n - 10)*d0 + n*(n - 1)*b
    assert numerator % 8 == 0
    w.append(comb(n - 2, 2)*d0 - numerator // 8)
    for j in range(2, min(end - 1, n - 2)):
        numerator = -((8*j*j - (4*n + 2)*j + 2*n - 4)*w[j]
                      + (9*j*j - (10*n + 5)*j + 2*n*n + 4*n)*w[j - 1]
                      + 2*(n - j)*(n + 1 - j)*w[j - 2])
        denominator = 2*(j + 1)*(j - 1)
        assert numerator % denominator == 0
        w.append(numerator // denominator)
    w += [0] * max(0, end - len(w))
    f = [initial]
    for l in range(end):
        numerator = (n - l)*f[-1] + w[l]
        assert numerator % (l + 1) == 0
        f.append(numerator // (l + 1))
    return initial, f


def original_controls():
    # 原二项尾展开；与 O_j 整数递推隔离，只在 N=4,8 用作正控。
    for n in (4, 8):
        c = [Fraction(0) for _ in range(n + 1)]
        for m in range(1, n // 2 + 1):
            for red in range(m + 1, 2*m + 1):
                scalar = Fraction((-1)**(n // 4 + m)*comb(n, 2*m)*comb(2*m, red), 2**(2*m))
                for u in range(red + 1):
                    for v in range(2*m - red + 1):
                        c[u + v] += scalar*(-1)**u*comb(red, u)*comb(2*m - red, v)
        initial, row = integer_row(n, n)
        for l in range(n + 1):
            original = sum(c[j]*Fraction(comb(l, j), comb(n, j)) for j in range(l + 1))
            assert Fraction(row[l], 2**n * comb(n, l)) == original
        altered = integer_row(n, 1, d0_sign=-1)[1]
        assert altered[1] != row[1], '反号初值的负控未被拒绝'
        assert Fraction(row[0], 2**n * comb(n, 0)) != -c[0], '整体反号负控未被拒绝'
    assert I(Fraction(1, 3)).lo <= SCALE // 3 and I(Fraction(1, 3)).hi == SCALE // 3 + 1
    assert (I(-2, 3) * I(-5, 7)).lo == -15*SCALE
    assert (I(-2, 3) * I(-5, 7)).hi == 21*SCALE
    assert (I(-1, 2) / I(2, 3)).lo <= -SCALE // 2
    assert (I(-1, 2) / I(2, 3)).hi >= SCALE


def finite_complement():
    count, smallest = 0, None
    for n in range(4, 256, 4):
        resource_check()
        end = (n + 2)//3 - 1
        initial, row = integer_row(n, end)
        for l in range(1, end + 1):
            right = (n - l)*initial*comb(n, l)
            gap = right - n*row[l]
            assert gap > 0, (n, l, gap)
            ratio = Fraction(gap, right)
            smallest = ratio if smallest is None else min(smallest, ratio)
            count += 1
    return {'pairs': count, 'smallest_relative_gap': str(smallest), 'max_n': 252}


def main():
    resource_check()
    original_controls()
    denominator = 10**16
    assert (denominator + 4142135623730950)**2 < 2*denominator**2
    assert (denominator + 4142135623730951)**2 > 2*denominator**2
    # Gaussian 角积分加强与尾阈值的独立有理控制。
    assert min(Fraction(1), Fraction(3, 4), Fraction(14, 27), Fraction(8, 27), Fraction(4, 81)) > 0
    assert sum(Fraction(7**j, factorial(j)) for j in range(8)) > 160
    assert sum(Fraction(27, 16)**j / factorial(j) for j in range(6)) > 5
    assert Fraction(1, 16) + Fraction(8, 9) < 1
    assert 4624*256 < 5000*255
    certificate = interval_certificate()
    finite = finite_complement()
    resource_check()
    print(json.dumps({'verdict': 'PASS', 'scope': 'S22 exact prefix box and N<256 complement only',
          'certificate': certificate, 'finite': finite,
          'controls': 'original full N4,N8 rows; initial and overall sign destructive controls; outward rational operations',
          'resource': {'elapsed_seconds': time.perf_counter() - START,
                       'sampled_peak_private_bytes': PEAK_PRIVATE,
                       'private_cap_bytes': MAX_PRIVATE, 'timeout_seconds': MAX_SECONDS,
                       'target': 'current Python worker; cooperative checks each 32 nodes and each N'},
          'not_proved_by_script_alone': 'phase rho enclosure, analytic tail, full coefficient gate and G stability require proof audit'},
          ensure_ascii=False))


if __name__ == '__main__':
    main()
