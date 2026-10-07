"""独立小规模穷举连接代价；固定实例，不接受扩大规模参数。"""

from itertools import combinations, product
import json
from math import ceil
from resource_guard import gate


def component_counts(edges):
    count = len(edges)
    if count > 12:
        raise ValueError('固定控制最多12条超边')
    adjacency = [sum(1 << j for j, other in enumerate(edges)
                     if j != i and edge & other)
                 for i, edge in enumerate(edges)]
    values = [0] * (1 << count)
    for mask in range(1, 1 << count):
        if mask % 64 == 0:
            gate()
        unseen = mask
        components = 0
        while unseen:
            components += 1
            frontier = unseen & -unseen
            unseen ^= frontier
            while frontier:
                next_frontier = 0
                for i in range(count):
                    if frontier & (1 << i):
                        next_frontier |= adjacency[i]
                frontier = next_frontier & unseen
                unseen ^= frontier
        values[mask] = components
    return values


def exact_extension_costs(edges, components, k):
    count = len(edges)
    costs = [0 if value <= k else count + 1 for value in components]
    # 从超集向子集传播，枚举所有添加方案，不使用候选解析公式。
    for mask in range((1 << count) - 1, 0, -1):
        if mask % 64 == 0:
            gate()
        for i in range(count):
            if not mask & (1 << i):
                costs[mask] = min(costs[mask], 1 + costs[mask | (1 << i)])
    return costs


def bitset(elements):
    return sum(1 << item for item in elements)


def graphic_bases():
    graph = [(0, 1), (1, 2), (2, 0), (2, 3), (0, 3)]
    bases = []
    for selected in combinations(range(5), 3):
        reached = {0}
        for _ in range(4):
            for i in selected:
                u, v = graph[i]
                if u in reached or v in reached:
                    reached.update((u, v))
        if len(reached) == 4:
            bases.append(bitset(selected))
    return bases


def uniform_and_extremals():
    # 3<=N<=5，r=2；小实例用所有集合族检验谱和关联图判据。
    cases = []
    for n in (3, 4, 5):
        rank = 2
        edges = [bitset(pair) for pair in combinations(range(n), rank)]
        components = component_counts(edges)
        q, s = divmod(n, rank)
        a = rank - s - 1
        minimum = []
        for mask in range(1, 1 << len(edges)):
            union = 0
            for i, edge in enumerate(edges):
                if mask & (1 << i):
                    union |= edge
            dominates = union.bit_count() >= n - rank + 1
            size = mask.bit_count()
            if size == q and dominates:
                minimum.append(mask)
            for k in range(1, len(edges) + 1):
                optimum = max(q, ceil((n - rank + 1 - k) / (rank - 1)))
                if size == optimum and optimum > q:
                    beta = size * (rank - 1) + components[mask] - union.bit_count()
                    slack = size * (rank - 1) + k - (n - rank + 1)
                    criterion = components[mask] <= k and beta + k - components[mask] <= slack
                    actual = dominates and components[mask] <= k
                    if criterion != actual:
                        raise ValueError('关联图达界判据不符')
        possible = sorted({components[mask] for mask in minimum})
        if possible != list(range(max(1, q - a), q + 1)):
            raise ValueError('最小支配集分量谱不符')
        cases.append({'N': n, 'r': rank, 'minimum_component_spectrum': possible})
    return cases


def main():
    uniform = [bitset(triple) for triple in combinations(range(5), 3)]
    partition = [bitset((i, 3 + j)) for i, j in product(range(3), repeat=2)]
    # F_2^2的三个非零方向，每个两份；任意两个不同方向独立。
    vectors = [(1, 0), (1, 0), (0, 1), (0, 1), (1, 1), (1, 1)]
    vector_bases = [bitset((i, j)) for i, j in combinations(range(6), 2)
                    if vectors[i][0] * vectors[j][1] - vectors[i][1] * vectors[j][0] != 0]
    rows = []
    for name, rank, edges in [('U3_5', 3, uniform),
                              ('partition_3_3', 2, partition),
                              ('binary_rank2_double_directions', 2, vector_bases),
                              ('graphic_diamond', 3, graphic_bases())]:
        components = component_counts(edges)
        checks = 0
        for k in range(1, len(edges) + 1):
            actual = exact_extension_costs(edges, components, k)
            for mask in range(1, 1 << len(edges)):
                expected = max(0, ceil((components[mask] - k) / (rank - 1)))
                if actual[mask] != expected:
                    raise ValueError(f'{name}:连接律不符 mask={mask}, k={k}')
                checks += 1
        rows.append({'case': name, 'bases': len(edges), 'checks': checks, 'result': 'PASS'})
    path = [bitset((i, i + 1)) for i in range(6)]
    components = component_counts(path)
    chosen = (1 << 1) | (1 << 4)
    negative_cost = exact_extension_costs(path, components, 1)[chosen]
    if negative_cost != 2 or components[chosen] != 2:
        raise ValueError('P6负控不符')
    print(json.dumps({'fixed_controls': rows,
                      'uniform_extremals': uniform_and_extremals(),
                      'nonmatroid_negative': {'P6_cost': negative_cost, 'formula_if_misapplied': 1}},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
