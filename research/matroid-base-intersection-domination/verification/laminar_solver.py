"""显式容量树：求值、回溯余圈、构造互异最优基族；不是任意oracle求解器。"""

import argparse
import ctypes
from ctypes import wintypes
import json
import time


MAX_ELEMENTS = 64
MAX_NODES = 192
TIME_LIMIT = 45
MEMORY_LIMIT = 256 * 1024 * 1024
START = time.monotonic()


class Counters(ctypes.Structure):
    _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
        (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
        'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
        'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]


# DLL及结构类型只初始化一次；每次检查创建新ctypes类型会人为累积内存。
KERNEL = ctypes.WinDLL('kernel32', use_last_error=True)
KERNEL.GetCurrentProcess.restype = wintypes.HANDLE
PSAPI = ctypes.WinDLL('psapi', use_last_error=True)
PSAPI.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]


def resource_gate():
    if time.monotonic() - START > TIME_LIMIT:
        raise TimeoutError('容量树验证超过45秒，停止，不重试')
    info = Counters()
    info.cb = ctypes.sizeof(info)
    if not PSAPI.GetProcessMemoryInfo(KERNEL.GetCurrentProcess(), ctypes.byref(info), info.cb):
        raise OSError(ctypes.get_last_error(), '无法核进程内存，停止')
    if max(info.WorkingSetSize, info.PagefileUsage) > MEMORY_LIMIT:
        raise MemoryError('容量树验证超过256MiB内存门，停止，不重试')
    return info.PeakWorkingSetSize


class Laminar:
    def __init__(self, n, constraints):
        if not isinstance(n, int) or isinstance(n, bool) or not 2 <= n <= MAX_ELEMENTS:
            raise ValueError('显式元素数必须在2..64，本实现不接受压缩重数')
        self.n = n
        self.full = (1 << n) - 1
        caps = {self.full: n}
        for row in constraints:
            elements, cap = row['elements'], row['capacity']
            if not isinstance(cap, int) or isinstance(cap, bool) or cap < 0:
                raise ValueError('容量必须为非负整数')
            if len(set(elements)) != len(elements) or any(
                    not isinstance(e, int) or isinstance(e, bool) or not 0 <= e < n for e in elements):
                raise ValueError('元素列表重复或越界')
            mask = sum(1 << e for e in elements)
            if mask:
                caps[mask] = min(caps.get(mask, n), cap, mask.bit_count())
        # 本有限实现显式拒绝圈元素；证明允许先删圈，但不得静默重编号。
        if any(cap == 0 for cap in caps.values()):
            raise ValueError('本实现输入须无圈；请先显式删除圈并重编号')
        for i in range(n):
            caps[1 << i] = 1
        masks = sorted(caps, key=lambda x: (x.bit_count(), x))
        if len(masks) > MAX_NODES:
            raise ValueError('容量树节点超过192硬门')
        for a in masks:
            for b in masks:
                if a & b and a & b not in (a, b):
                    raise ValueError('容量约束交叉，不是laminar树')
        self.caps, self.masks = caps, masks
        self.children = {mask: [] for mask in masks}
        for mask in masks[:-1]:
            parent = min((a for a in masks if a != mask and mask & a == mask),
                         key=lambda a: a.bit_count())
            self.children[parent].append(mask)
        self.R = self.rank(self.full)
        if self.R < 2:
            raise ValueError('本实现只处理秩至少2')
        self.caps = {a: min(cap, self.R) for a, cap in caps.items()}
        self.caps[self.full] = self.R

    def rank(self, mask):
        values = {}
        for a in self.masks:
            values[a] = min(self.caps[a], sum(values[b] for b in self.children[a])) \
                if self.children[a] else int(bool(mask & a))
        return values[self.full]

    def independent(self, mask):
        return all((mask & a).bit_count() <= cap for a, cap in self.caps.items())

    def frontier(self, m, destructive_drop_nested=False):
        """只保留各局部秩的最大H；破坏开关仅供固定负控。"""
        tables = {}
        for a in self.masks:
            resource_gate()
            if not self.children[a]:
                candidates = {0: (0, 0), 1: (1, a)}
            else:
                candidates = {0: (0, 0)}
                for b in self.children[a]:
                    next_table = {}
                    for s, (size, chosen) in candidates.items():
                        for t, (child_size, child_chosen) in tables[b].items():
                            r = min(self.caps[a], s + t)
                            proposal = (size + child_size, chosen | child_chosen)
                            if proposal[0] > next_table.get(r, (-1, 0))[0]:
                                next_table[r] = proposal
                    candidates = next_table
            lower = a.bit_count() - m * self.caps[a]
            if destructive_drop_nested and a != self.full:
                lower = -1
            tables[a] = {r: value for r, value in candidates.items() if value[0] >= lower}
        feasible = [value for r, value in tables[self.full].items() if r < self.R]
        if not feasible:
            return None, None
        size, chosen = max(feasible)
        return self.n - size, self.full ^ chosen

    def bases_prefix(self, count):
        emitted = []
        def visit(i, chosen):
            resource_gate()
            if len(emitted) >= count:
                return
            remaining = self.full & ~((1 << i) - 1)
            if not self.independent(chosen) or self.rank(chosen | remaining) < self.R:
                return
            if chosen.bit_count() == self.R:
                emitted.append(chosen)
                return
            if i == self.n:
                return
            visit(i + 1, chosen | (1 << i))
            visit(i + 1, chosen)
        visit(0, 0)
        return emitted

    def extend(self, independent):
        for e in range(self.n):
            if independent.bit_count() == self.R:
                return independent
            proposal = independent | (1 << e)
            if self.independent(proposal):
                independent = proposal
        if independent.bit_count() != self.R:
            raise AssertionError('独立份无法扩基')
        return independent

    def leaf_order(self):
        def walk(a):
            if not self.children[a]:
                return [a.bit_length() - 1]
            return [e for child in self.children[a] for e in walk(child)]
        return walk(self.full)

    def solve(self, k):
        if not isinstance(k, int) or isinstance(k, bool) or k < 1:
            raise ValueError('k必须为正整数')
        lo, hi = 1, self.n
        while lo < hi:
            m = (lo + hi) // 2
            size, _ = self.frontier(m)
            if size is not None and size <= m * (self.R - 1) + k:
                hi = m
            else:
                lo = m + 1
        m = lo
        size, target = self.frontier(m)
        parts = [0] * m
        for i, e in enumerate(e for e in self.leaf_order() if target & (1 << e)):
            parts[i % m] |= 1 << e
        selected = list(dict.fromkeys(self.extend(part) for part in parts if part))
        for base in self.bases_prefix(2 * m):
            if len(selected) == m:
                break
            if base not in selected:
                selected.append(base)
        if len(selected) != m:
            raise AssertionError('未构造足够互异基')
        selected, counts = normalize(selected, target, self)
        return {'gamma_ck': m, 'cocircuit': target, 'T_m': size, 'bases': selected,
                'components': len(components(selected)), 'normalization': counts}


def components(edges):
    unseen = set(range(len(edges)))
    groups = []
    while unseen:
        todo = [unseen.pop()]
        group = []
        while todo:
            i = todo.pop()
            group.append(i)
            neighbors = {j for j in unseen if edges[j] & edges[i]}
            unseen.difference_update(neighbors)
            todo.extend(neighbors)
        groups.append(group)
    return groups


def normalize(selected, target, matroid):
    counts = {'outside': 0, 'cycle': 0}
    while len(components(selected)) > 1:
        resource_gate()
        before = selected[:]
        groups = components(before)
        union = 0
        for base in before:
            union |= base
        outside = union & ~target
        beta = len(before) * (matroid.R - 1) + len(groups) - union.bit_count()
        if outside:
            e = outside & -outside
            source = next(g for g in groups if any(before[i] & e for i in g))
            other = next(g for g in groups if g != source)
            reservoir = 0
            for i in other:
                reservoir |= before[i]
            for i in source:
                if before[i] & e:
                    rest = before[i] ^ e
                    f = next(1 << j for j in range(matroid.n)
                             if reservoir & (1 << j) and matroid.independent(rest | (1 << j)))
                    selected[i] = rest | f
            counts['outside'] += 1
        elif beta:
            changed = False
            for source in groups:
                other = next(g for g in groups if g != source)
                reservoir = 0
                for i in other:
                    reservoir |= before[i]
                for i in source:
                    for j in range(matroid.n):
                        e = 1 << j
                        if not before[i] & e:
                            continue
                        broken = [before[t] ^ e if t == i else before[t] for t in source]
                        if len(components(broken)) != 1 or not any(
                                before[t] & e for t in source if t != i):
                            continue
                        rest = before[i] ^ e
                        f = next(1 << t for t in range(matroid.n)
                                 if reservoir & (1 << t) and matroid.independent(rest | (1 << t)))
                        selected[i] = rest | f
                        changed = True
                        counts['cycle'] += 1
                        break
                    if changed:
                        break
                if changed:
                    break
            if not changed:
                raise AssertionError('正圈秩找不到圈替换')
        else:
            break
        after_union = 0
        for base in selected:
            after_union |= base
        if len(set(selected)) != len(selected) or target & ~after_union \
                or len(components(selected)) != len(groups) - 1:
            raise AssertionError('正规化破坏互异、覆盖或单步分量下降')
    return selected, counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    with open(args.input, encoding='utf-8') as handle:
        fixture = json.load(handle)
    matroid = Laminar(fixture['n'], fixture['constraints'])
    result = matroid.solve(fixture['k'])
    result['peak_working_set_bytes'] = resource_gate()
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
