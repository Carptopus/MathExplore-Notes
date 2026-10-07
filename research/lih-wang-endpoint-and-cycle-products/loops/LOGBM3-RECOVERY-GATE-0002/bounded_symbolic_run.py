"""本案例纯符号命令的进程树资源门；只打印结果，不写日志文件。"""
import argparse
import subprocess
import sys
import threading
import time
import ctypes as ct
from ctypes import wintypes as wt
import os


class BasicLimits(ct.Structure):
    _fields_ = [('process_time', ct.c_longlong), ('job_time', ct.c_longlong),
                ('flags', wt.DWORD), ('min_working', ct.c_size_t),
                ('max_working', ct.c_size_t), ('active_limit', wt.DWORD),
                ('affinity', ct.c_size_t), ('priority', wt.DWORD), ('scheduling', wt.DWORD)]


class ExtendedLimits(ct.Structure):
    _fields_ = [('basic', BasicLimits), ('io', ct.c_ulonglong*6),
                ('process_memory', ct.c_size_t), ('job_memory', ct.c_size_t),
                ('peak_process', ct.c_size_t), ('peak_job', ct.c_size_t)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seconds', type=int, default=180)
    parser.add_argument('--mib', type=int, default=512)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    assert args.command and 0 < args.seconds <= 180 and 0 < args.mib <= 512
    assert os.name == 'nt', '本资源门使用 Windows Job Object'
    kernel = ct.WinDLL('kernel32', use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ct.c_void_p, wt.LPCWSTR]
    kernel.CreateJobObjectW.restype = wt.HANDLE
    kernel.SetInformationJobObject.argtypes = [wt.HANDLE, ct.c_int, ct.c_void_p, wt.DWORD]
    kernel.QueryInformationJobObject.argtypes = [wt.HANDLE, ct.c_int, ct.c_void_p, wt.DWORD, ct.c_void_p]
    kernel.AssignProcessToJobObject.argtypes = [wt.HANDLE, wt.HANDLE]
    kernel.TerminateJobObject.argtypes = [wt.HANDLE, wt.UINT]
    kernel.CloseHandle.argtypes = [wt.HANDLE]
    job = kernel.CreateJobObjectW(None, None)
    if not job:
        raise ct.WinError(ct.get_last_error())
    limits = ExtendedLimits()
    limits.basic.flags = 0x200 | 0x2000  # 整个进程树内存硬门；关闭句柄终止残余子进程。
    limits.job_memory = args.mib*1024**2
    if not kernel.SetInformationJobObject(job, 9, ct.byref(limits), ct.sizeof(limits)):
        raise ct.WinError(ct.get_last_error())
    proc = subprocess.Popen([sys.executable, '-B', '-u', '-X', 'utf8', *args.command],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding='utf-8')
    if not kernel.AssignProcessToJobObject(job, wt.HANDLE(proc._handle)):
        error = ct.get_last_error()
        proc.kill()
        proc.wait()
        kernel.CloseHandle(job)
        raise ct.WinError(error)
    output, overflow = [], []

    def read():
        count = 0
        for line in proc.stdout:
            count += len(line)
            if count > 200000:
                overflow.append(True)
            else:
                output.append(line)

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    started, peak = time.monotonic(), 0
    reason = None
    while proc.poll() is None:
        info = ExtendedLimits()
        if not kernel.QueryInformationJobObject(job, 9, ct.byref(info), ct.sizeof(info), None):
            reason = 'JOB_QUERY'
        peak = max(peak, info.peak_job)
        if peak > args.mib*1024**2:
            reason = 'MEMORY'
        elif time.monotonic()-started > args.seconds:
            reason = 'TIME'
        elif overflow:
            reason = 'OUTPUT'
        if reason:
            kernel.TerminateJobObject(job, 2)
            break
        time.sleep(0.05)
    code = proc.wait(timeout=10)
    reader.join(timeout=10)
    info = ExtendedLimits()
    kernel.QueryInformationJobObject(job, 9, ct.byref(info), ct.sizeof(info), None)
    peak = max(peak, info.peak_job)
    kernel.CloseHandle(job)
    print(''.join(output), end='')
    print('RESOURCE_SUMMARY', {'exit': code, 'seconds': round(time.monotonic()-started, 3),
                              'tree_private_peak': peak, 'gate': reason}, flush=True)
    sys.exit(2 if reason else code)


if __name__ == '__main__':
    main()
