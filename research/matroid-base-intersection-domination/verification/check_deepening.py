"""固定功能验证：独立全子集/全图基准对照完整算法输出，含破坏性控制。"""

from itertools import combinations
import json
from pathlib import Path
import time

from laminar_solver import Laminar, normalize, resource_gate

MAX_SMALL_N = 8
MAX_GRAPH_BASES = 12
MAX_FIXTURES = 96
MAX_FAMILIES = 250000


def rank_and_partition(n, constraints):
    # 独立基准仅看集合不等式；不调用树秩、DP或解析式。
    independent = []
    for mask in range(1 << n):
        independent.append(all(sum(bool(mask & (1 << e)) for e in elements) <= cap
                               for elements, cap in constraints))
    rank = [0] * (1 << n)
    chi = [0] + [n + 1] * ((1 << n) - 1)
    for mask in range(1, 1 << n):
        if mask % 64 == 0:
            resource_gate()
        rank[mask] = mask.bit_count() if independent[mask] else max(
            rank[mask ^ (1 << e)] for e in range(n) if mask & (1 << e))
        anchor = mask & -mask
        sub = mask
        while sub:
            if sub & anchor and independent[sub]:
                chi[mask] = min(chi[mask], 1 + chi[mask ^ sub])
            sub = (sub - 1) & mask
    return independent, rank, chi


def cocircuits(n, rank):
    full, R = (1 << n) - 1, rank[-1]
    return [full ^ H for H in range(1 << n) if rank[H] == R - 1 and all(
        rank[H | (1 << e)] == R for e in range(n) if not H & (1 << e))]


def graph_components(selected):
    unseen = set(range(len(selected)))
    answer = 0
    while unseen:
        answer += 1
        todo = [unseen.pop()]
        while todo:
            i = todo.pop()
            neighbors = {j for j in unseen if selected[i] & selected[j]}
            unseen -= neighbors
            todo.extend(neighbors)
    return answer


def graph_frontier(bases, stats):
    answer = {}
    for mask in range(1, 1 << len(bases)):
        stats['families'] += 1
        if stats['families'] > MAX_FAMILIES:
            raise ValueError('固定基族比较超过250000硬门，不扩大或重试')
        selected = [b for i, b in enumerate(bases) if mask & (1 << i)]
        if all(any(base == b or base & b for b in selected) for base in bases):
            c = graph_components(selected)
            for k in range(c, len(bases) + 1):
                answer[k] = min(answer.get(k, len(bases) + 1), len(selected))
    return answer


def rows(n, R, extra=()):
    return [(list(range(n)), R)] + [(list(elements), cap) for elements, cap in extra]


def fixtures():
    result = []
    for n in (4, 5, 6):
        for R in range(2, n):
            result.append((n, rows(n, R)))
    for R in (2, 3, 4, 5):
        for a in (1, 2, 3):
            for b in (1, 2):
                result.append((6, rows(6, R, [(range(3), a), (range(3, 6), b)])))
    for R in (2, 3, 4, 5):
        for outer in (2, 3, 4):
            for inner in (1, 2):
                result.append((7, rows(7, R, [(range(5), outer), (range(3), inner)])))
    return result


def main():
    start = time.monotonic()
    stats = {'laminar_fixtures': 0, 'T_m_comparisons': 0, 'constructed_families': 0,
             'graph_exact_fixtures': 0, 'families': 0, 'graph_value_comparisons': 0,
             'paving_fixtures': 0, 'paving_frontiers': 0, 'outside': 0, 'cycle': 0}
    nested_control = False
    input_fixtures = fixtures()
    if len(input_fixtures) > MAX_FIXTURES:
        raise ValueError('固定实例超过96硬门')
    for n, constraints in input_fixtures:
        if n > MAX_SMALL_N:
            raise ValueError('小对象基准超过8元素硬门')
        solver = Laminar(n, [{'elements': e, 'capacity': cap} for e, cap in constraints])
        independent, ranks, chi = rank_and_partition(n, constraints)
        R = ranks[-1]
        if R != solver.R:
            raise AssertionError('树真实秩与独立全子集秩不一致')
        circuits = cocircuits(n, ranks)
        for m in range(1, n + 1):
            expected = min((C.bit_count() for C in circuits if chi[C] <= m), default=None)
            actual, C = solver.frontier(m)
            if expected != actual or (C is not None and (C not in circuits or chi[C] > m)):
                raise AssertionError(('T_m不一致', n, constraints, m, expected, actual))
            stats['T_m_comparisons'] += 1
            broken, _ = solver.frontier(m, destructive_drop_nested=True)
            nested_control |= broken != expected
        bases = [mask for mask in range(1 << n) if mask.bit_count() == R and independent[mask]]
        direct = graph_frontier(bases, stats) if len(bases) <= MAX_GRAPH_BASES else None
        stats['graph_exact_fixtures'] += int(direct is not None)
        for k in range(1, n + 1):
            result = solver.solve(k)
            selected = result['bases']
            if len(set(selected)) != len(selected) or any(b not in bases for b in selected) \
                    or not all(any(base & b for b in selected) for base in bases) \
                    or graph_components(selected) > k:
                raise AssertionError('输出互异性、基合法性、原图支配或分量条件失败')
            expected = min(max(chi[C], (C.bit_count() - k + R - 2) // (R - 1)) for C in circuits)
            if result['gamma_ck'] != expected:
                raise AssertionError('输出与独立余圈分划不一致')
            if direct is not None:
                if direct[min(k, len(bases))] != len(selected):
                    raise AssertionError('输出与原基交图全部族穷举不一致')
                stats['graph_value_comparisons'] += 1
            stats['constructed_families'] += 1
            for key in ('outside', 'cycle'):
                stats[key] += result['normalization'][key]
        stats['laminar_fixtures'] += 1

    # 独立paving对象：长直线、交叉线、Fano，以及秩四稀疏paving。
    paving = [(6, rows(6, 3, [(range(4), 2)])),
              (6, rows(6, 3, [([0, 1, 2], 2), ([2, 3, 4], 2)])),
              (7, rows(7, 3, [(line, 2) for line in (
                  (0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
                  (1, 4, 6), (2, 3, 6), (2, 4, 5))])),
              (8, rows(8, 4, [([0, 1, 2, 3], 3), ([4, 5, 6, 7], 3), ([0, 1, 4, 5], 3)])),
              (8, rows(8, 4, [([0, 1, 2, 3], 3), ([4, 5, 6, 7], 3)]))]
    wrong_all_max_control = False
    for n, constraints in paving:
        independent, ranks, chi = rank_and_partition(n, constraints)
        R = ranks[-1]
        # 检验拟阵增广公理，不能仅由任意集合约束假定为拟阵。
        sets = [mask for mask, good in enumerate(independent) if good]
        for I in sets:
            for J in sets:
                if I.bit_count() < J.bit_count() and not any(
                        independent[I | (1 << e)] for e in range(n) if (J & ~I) & (1 << e)):
                    raise AssertionError('paving固定输入不满足拟阵公理')
        if any(not independent[mask] for mask in range(1 << n) if mask.bit_count() < R):
            raise AssertionError('固定输入不是paving')
        circuits = cocircuits(n, ranks)
        q = min(chi[C] for C in circuits)
        s = min(C.bit_count() for C in circuits)
        if min(C.bit_count() for C in circuits if chi[C] == q) != s:
            raise AssertionError('paving T_q=s失败')
        wrong_all_max_control |= q == 1 and any(C.bit_count() == s and chi[C] > q for C in circuits)
        for m in range(q, n + 1):
            if min(C.bit_count() for C in circuits if chi[C] <= m) != s:
                raise AssertionError('paving前沿不是常值')
            stats['paving_frontiers'] += 1
        stats['paving_fixtures'] += 1

    # 错误的“全层级输入只检查根”以及“q=1所有最短余圈均独立”必须被识别。
    if not nested_control or not wrong_all_max_control:
        raise AssertionError('指定破坏性控制未命中')
    try:
        Laminar(5, [{'elements': [0, 1, 2], 'capacity': 2},
                    {'elements': [2, 3, 4], 'capacity': 2}])
    except ValueError:
        crossing_rejected = True
    else:
        raise AssertionError('交叉约束被错误接受为laminar')

    # 明确的覆盖族正控：两个分量，源分量含关联圈，目标等于并集，迫使B分支。
    cycle_matroid = Laminar(5, [{'elements': list(range(5)), 'capacity': 2}])
    repaired, cycle_counts = normalize([3, 6, 5, 24], 31, cycle_matroid)
    if cycle_counts != {'outside': 0, 'cycle': 1} or graph_components(repaired) != 1:
        raise AssertionError('固定关联圈覆盖正控未触发B')
    stats['cycle'] += cycle_counts['cycle']

    # 32点实例只调用完整输出算法，不枚举全部基或基族。
    # 其最优下界来自S3一般证明，本控制独立核输出覆盖及容量，不能冒充全图穷举。
    with open(Path(__file__).with_name('simple_rank4_q5.json'), encoding='utf-8') as handle:
        large_fixture = json.load(handle)
    large_solver = Laminar(large_fixture['n'], large_fixture['constraints'])
    large = large_solver.solve(large_fixture['k'])
    large_union = 0
    for base in large['bases']:
        large_union |= base
        if base.bit_count() != 4 or any(
                sum(bool(base & (1 << e)) for e in row['elements']) > row['capacity']
                for row in large_fixture['constraints']):
            raise AssertionError('32点输出容量不合法')
    C = sum(1 << e for e in range(15, 32))
    if large['gamma_ck'] != 6 or len(set(large['bases'])) != 6 \
            or C & ~large_union or graph_components(large['bases']) != 1:
        raise AssertionError('32点锐损失输出控制失败')
    peak = resource_gate()
    print(json.dumps({'status': 'VERIFIED', 'stats': stats,
                      'controls': {'drop_nested_caught': nested_control,
                                   'all_shortest_q1_independent_caught': wrong_all_max_control,
                                   'crossing_input_rejected': crossing_rejected,
                                   'forced_cycle_branch': cycle_counts,
                                   'simple_rank4_q5_output': {'bases': 6, 'components': 1,
                                                             'full_graph_enumeration': False}},
                      'elapsed_seconds': time.monotonic() - start,
                      'peak_working_set_bytes': peak,
                      'scope': '固定实例；大于12基不穷举基族；paving检验前沿而非全部基族'},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
