"""固定小拟阵：由全部选基族直接核支配/覆盖前沿，不用候选式计算actual。"""

from itertools import combinations, product
import json
import time
from resource_guard import gate


MAX_BASES = 12
MAX_ELEMENTS = 7
TIME_LIMIT_SECONDS = 45
START = time.monotonic()


def deadline():
    gate()
    if time.monotonic() - START > TIME_LIMIT_SECONDS:
        raise TimeoutError('固定前沿验证超过45秒，停止且不重试')


def components(edges):
    unseen = set(range(len(edges)))
    groups = []
    while unseen:
        todo = [unseen.pop()]
        group = []
        while todo:
            i = todo.pop()
            group.append(i)
            neighbors = [j for j in unseen if edges[i] & edges[j]]
            unseen.difference_update(neighbors)
            todo.extend(neighbors)
        groups.append(group)
    return groups


def independent_partition_counts(bases, n):
    # 子集属于某条基即独立；独立分划DP仅用于解析式右端，不计算actual图最优值。
    independent = {0}
    for base in bases:
        sub = base
        while sub:
            independent.add(sub)
            sub = (sub - 1) & base
    chi = [0] + [n + 1] * ((1 << n) - 1)
    for mask in range(1, 1 << n):
        anchor = mask & -mask
        sub = mask
        while sub:
            if sub & anchor and sub in independent:
                chi[mask] = min(chi[mask], 1 + chi[mask ^ sub])
            sub = (sub - 1) & mask
    return chi


def normalize(selected, target, universe):
    """实施S3两种替换，以独立重算结果检查覆盖、互异及势能。"""
    rank = selected[0].bit_count()
    counts = {'outside': 0, 'cycle': 0}
    while len(components(selected)) > 1:
        deadline()
        before = list(selected)
        groups = components(before)
        union = 0
        for edge in before:
            union |= edge
        beta = len(before) * (rank - 1) + len(groups) - union.bit_count()
        if union & ~target:
            element = (union & ~target) & -(union & ~target)
            source = next(group for group in groups if any(before[i] & element for i in group))
            other = next(group for group in groups if group != source)
            reservoir = 0
            for i in other:
                reservoir |= before[i]
            for i in source:
                if before[i] & element:
                    remainder = before[i] ^ element
                    replacements = [remainder | (1 << f) for f in range(MAX_ELEMENTS)
                                    if reservoir & (1 << f) and remainder | (1 << f) in universe]
                    if not replacements:
                        raise AssertionError('生成分量无法提供合法替换元素')
                    selected[i] = replacements[0]
            expected_union = union ^ element
            counts['outside'] += 1
        elif beta:
            found = False
            for group in groups:
                if found:
                    break
                other = next(part for part in groups if part != group)
                reservoir = 0
                for i in other:
                    reservoir |= before[i]
                for i in group:
                    if found:
                        break
                    for f in range(MAX_ELEMENTS):
                        element = 1 << f
                        if not before[i] & element:
                            continue
                        if not any(before[j] & element for j in group if j != i):
                            continue
                        broken = [before[j] ^ element if j == i else before[j] for j in group]
                        if len(components(broken)) != 1:
                            continue
                        remainder = before[i] ^ element
                        replacements = [remainder | (1 << x) for x in range(MAX_ELEMENTS)
                                        if reservoir & (1 << x) and remainder | (1 << x) in universe]
                        if not replacements:
                            raise AssertionError('圈交换无法提供合法替换')
                        selected[i] = replacements[0]
                        found = True
                        break
            if not found:
                raise AssertionError('正圈秩未找到可消去关联边')
            expected_union = union
            counts['cycle'] += 1
        else:
            break
        new_union = 0
        for edge in selected:
            new_union |= edge
        if len(set(selected)) != len(before) or any(edge not in universe for edge in selected):
            raise AssertionError('替换违反基互异或基合法性')
        if new_union != expected_union or target & ~new_union:
            raise AssertionError('替换覆盖/并集变化不符')
        if len(components(selected)) != len(groups) - 1:
            raise AssertionError('替换未恰减一分量')
    expected = max(1, target.bit_count() - len(selected) * (rank - 1))
    if len(components(selected)) != expected:
        raise AssertionError('正规化未达到解析下界')
    return counts


def check_fixture(name, rank, n, bases, parallel_sizes=None):
    if len(bases) > MAX_BASES or n > MAX_ELEMENTS or len(set(bases)) != len(bases):
        raise ValueError('固定规模硬门或基互异失败')
    if any(base.bit_count() != rank for base in bases):
        raise ValueError('非等秩基输入')
    universe = set(bases)
    size = len(bases)
    full = (1 << n) - 1
    chi = independent_partition_counts(bases, n)
    # 所有最小击中基的元素集：直接有限地重建余圈。
    hits = [mask for mask in range(1, full + 1) if all(mask & base for base in bases)]
    cocircuits = [mask for mask in hits
                  if not any(other != mask and other & mask == other for other in hits)]
    cover_frontier = [[size + 1] * (size + 1) for _ in range(full + 1)]
    domination_frontier = [size + 1] * (size + 1)
    min_family_components = {}
    adjacency_closed = [sum(1 << j for j, other in enumerate(bases) if base & other)
                        for base in bases]
    normalization_steps = {'outside': 0, 'cycle': 0}
    for selected_mask in range(1, 1 << size):
        deadline()
        selected = [base for i, base in enumerate(bases) if selected_mask & (1 << i)]
        m = len(selected)
        c = len(components(selected))
        union = 0
        dominated_vertices = 0
        for i, base in enumerate(bases):
            if selected_mask & (1 << i):
                union |= base
                dominated_vertices |= adjacency_closed[i]
        dominates = dominated_vertices == (1 << size) - 1
        if dominates:
            for k in range(c, size + 1):
                domination_frontier[k] = min(domination_frontier[k], m)
            min_family_components.setdefault(m, set()).add(c)
        sub = union
        while sub:
            cover_frontier[sub][m] = min(cover_frontier[sub][m], c)
            sub = (sub - 1) & union
        # 每一原基族取两个固定、确实被覆盖的目标：全部并集和删最低点的并集。
        for target in {union, union ^ (union & -union)} - {0}:
            steps = normalize(list(selected), target, universe)
            for operation in steps:
                normalization_steps[operation] += steps[operation]
    checks = 0
    for target in range(1, full + 1):
        for m in range(1, size + 1):
            actual = cover_frontier[target][m]
            if actual <= size:
                predicted = max(1, target.bit_count() - m * (rank - 1))
                if actual != predicted or m < chi[target]:
                    raise AssertionError(f'{name}:固定覆盖前沿失配 C={target}, m={m}')
                checks += 1
    for k in range(1, size + 1):
        predicted = min(max(chi[c], -(-(c.bit_count() - k) // (rank - 1))) for c in cocircuits)
        if domination_frontier[k] != predicted:
            raise AssertionError(f'{name}:余圈优化失配 k={k}')
    q = domination_frontier[size]
    spectrum = sorted(min_family_components[q])
    if parallel_sizes is not None:
        sizes = sorted(parallel_sizes, reverse=True)
        t = sum(sizes) - sizes[0]
        expected_q = sizes[1] if len(sizes) == 2 else max((t + 1) // 2, sizes[1])
        expected_spectrum = list(range(1 if len(sizes) == 2 else t - q, q + 1))
        if q != expected_q or spectrum != expected_spectrum:
            raise AssertionError(f'{name}:秩二支配或全分量谱不符')
        for k in range(1, size + 1):
            expected = q if len(sizes) == 2 else max(q, t - k)
            if domination_frontier[k] != expected:
                raise AssertionError('秩二全k值不符')
    return {'fixture': name, 'rank': rank, 'elements': n, 'bases': size,
            'cover_frontier_comparisons': checks, 'gamma': q,
            'gamma_components': spectrum, 'gamma_c_k': domination_frontier[1:],
            'normalization_steps': normalization_steps, 'result': 'PASS'}


def rank_two(sizes):
    classes = [j for j, size in enumerate(sizes) for _ in range(size)]
    return [sum(1 << i for i in pair) for pair in combinations(range(len(classes)), 2)
            if classes[pair[0]] != classes[pair[1]]]


def main():
    rows = []
    for sizes in [(3, 3), (3, 2, 1), (2, 2, 2), (4, 1, 1), (1, 1, 1, 1, 1)]:
        rows.append(check_fixture(f'rank2_{sizes}', 2, sum(sizes), rank_two(sizes), sizes))
    partition = [sum(1 << i for i in triple) for triple in product(range(3), range(3, 5), range(5, 7))]
    rows.append(check_fixture('partition_rank3_3_2_2', 3, 7, partition))
    classes = [0, 0, 1, 1, 2, 3]
    bases = [sum(1 << i for i in triple) for triple in combinations(range(6), 3)
             if len({classes[i] for i in triple}) == 3]
    rows.append(check_fixture('parallel_U3_4', 3, 6, bases))
    if sum(row['normalization_steps']['cycle'] for row in rows) == 0:
        raise AssertionError('圈交换分支未被实际覆盖')
    if sum(row['normalization_steps']['outside'] for row in rows) == 0:
        raise AssertionError('非必需元素删除分支未被实际覆盖')
    print(json.dumps({'fixed_controls': rows, 'seconds': time.monotonic() - START,
                      'limits': {'max_bases': MAX_BASES, 'max_elements': MAX_ELEMENTS,
                                 'timeout_seconds': TIME_LIMIT_SECONDS}}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
