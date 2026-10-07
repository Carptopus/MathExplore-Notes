"""公开固定检查的独立资源门：不加载发现探针或数学构造代码。"""

import ctypes
from ctypes import wintypes
import sys
import time

if sys.platform != 'win32':
    raise RuntimeError('本复现实现需要 Windows；数学定理不依赖 Windows')

START = time.monotonic()
TIME_LIMIT = 45
MEMORY_LIMIT = 256 * 1024 * 1024


class Counters(ctypes.Structure):
    _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
        (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
        'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage',
        'PagefileUsage', 'PeakPagefileUsage')]


KERNEL = ctypes.WinDLL('kernel32', use_last_error=True)
KERNEL.GetCurrentProcess.restype = wintypes.HANDLE
PSAPI = ctypes.WinDLL('psapi', use_last_error=True)
PSAPI.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]


def gate():
    if time.monotonic() - START > TIME_LIMIT:
        raise TimeoutError('固定复核超过45秒，停止且不自动重试')
    info = Counters()
    info.cb = ctypes.sizeof(info)
    if not PSAPI.GetProcessMemoryInfo(KERNEL.GetCurrentProcess(), ctypes.byref(info), info.cb):
        raise OSError(ctypes.get_last_error(), '无法核验进程内存，停止')
    if max(info.WorkingSetSize, info.PagefileUsage) > MEMORY_LIMIT:
        raise MemoryError('固定复核超过256MiB，停止且不自动重试')
    return info.PeakWorkingSetSize
