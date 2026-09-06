"""小规模内存正负控；直接枚举原图 cyclic flats，不代替一般证明。"""

from itertools import combinations
import json


def require(test, message):
    if not test:
        raise ValueError(message)


def partition(n, edges):
    parent = list(range(n))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        a, b = root(u), root(v)
        parent[b] = a
    groups = {}
    for u in range(n):
        groups.setdefault(root(u), []).append(u)
    return tuple(sorted(tuple(group) for group in groups.values()))


def rank(p):
    return sum(len(block) - 1 for block in p)


def contained(p, q):
    return all(any(set(block) <= set(other) for other in q) for block in p)


def support(n, vertices):
    vertices = sorted(vertices)
    return partition(n, [(vertices[0], v) for v in vertices[1:]]) if vertices else partition(n, [])


def join(n, p, q):
    edges = []
    for block in p + q:
        edges.extend((block[0], v) for v in block[1:])
    return partition(n, edges)


def cyclic_flats(n, edges):
    require(n <= 10 and len(edges) <= 14, '有限控制规模越界')
    require(all(u != v for u, v in edges), '本控制不接受 loop')
    data = {}
    for mask in range(1 << len(edges)):
        selected = [e for j, e in enumerate(edges) if mask & (1 << j)]
        p = partition(n, selected)
        closure = [e for e in edges if contained(support(n, e), p)]
        if len(closure) != len(selected):
            continue
        r = rank(p)
        if any(rank(partition(n, selected[:j] + selected[j + 1:])) < r for j in range(len(selected))):
            continue
        require(p not in data or data[p] == len(selected), '同一 flat 空间权重冲突')
        data[p] = len(selected)
    return data


def minimal_cycles(data):
    nonzero = [p for p in data if rank(p)]
    return [p for p in nonzero if not any(q != p and contained(q, p) for q in nonzero)]


def active_vertices(p):
    blocks = [set(b) for b in p if len(b) > 1]
    require(len(blocks) == 1, '当前最小循环或侧不是单连通支撑')
    return blocks[0]


def reconstruct_side(n, global_data, side, all_sides, port, simple_data=None):
    old = {p: w for p, w in global_data.items() if contained(p, side)}
    generators = list(old)
    path_data = global_data if simple_data is None else simple_data
    cross = [q for q in minimal_cycles(path_data) if not any(contained(q, u) for u in all_sides)]
    require(bool(cross), '跨侧循环缺失')
    side_vertices = active_vertices(side)
    for q in cross:
        generators.append(support(n, active_vertices(q) & side_vertices))
    spaces = {partition(n, [])}
    for generator in generators:
        spaces |= {join(n, x, generator) for x in tuple(spaces)}
        require(len(spaces) <= 4096, '生成空间硬门越界')
    result = {}
    for x in spaces:
        nu = max(w - rank(f) for f, w in old.items() if contained(f, x))
        result[x] = rank(x) + nu + int(contained(port, x))
    return result, cross


def run_case(name, n, edges, blocks, ports, bare_count):
    require(len(edges) == len(set(tuple(sorted(e)) for e in edges)), '输入正控必须简单')
    data = cyclic_flats(n, edges)
    sides = [support(n, vertices) for vertices in blocks]
    require(all(u in data for u in sides), '侧不是原图 cyclic flat')
    require(len(edges) - sum(data[u] for u in sides) == bare_count, '裸边数不匹配')
    counts = []
    for side, port_vertices in zip(sides, ports):
        side_edges = [e for e in edges if contained(support(n, e), side)]
        port = support(n, port_vertices)
        predicted, cross = reconstruct_side(n, data, side, sides, port)
        direct = cyclic_flats(n, side_edges + [port_vertices])
        require(predicted == direct, f'{name}: 补边全部空间/权重不相等')
        damaged = dict(predicted)
        damaged[side] += 1
        require(damaged != direct, f'{name}: 权重破坏负控未拒绝')
        counts.append(len(direct))
    if bare_count:
        common = set.intersection(*(active_vertices(q) for q in cross))
        require(len(common) - 1 == bare_count + len(sides) - 1, 'P 维数错误')
        for side, port_vertices in zip(sides, ports):
            require(common & active_vertices(side) == set(port_vertices), 'P 端口交不正确')
    return {'case': name, 'cyclic_flat_count': len(data), 'augmented_side_counts': counts,
            'all_spaces_and_weights_equal': True, 'damaged_weight_rejected': True}


def parallel_control():
    n = 5
    base = list(combinations([0, 1, 2], 2)) + list(combinations([2, 3, 4], 2)) + [(0, 3)]
    # 同时加重侧内端口边与裸骨架边。原多重数据不能直接用最小循环恢复路径。
    edges = base + [(0, 2), (0, 3)]
    simple_data = cyclic_flats(n, base)
    full_data = cyclic_flats(n, edges)
    sides = [support(n, [0, 1, 2]), support(n, [2, 3, 4])]
    for side, port_vertices in zip(sides, [(0, 2), (2, 3)]):
        port = support(n, port_vertices)
        predicted, _ = reconstruct_side(n, full_data, side, sides, port, simple_data)
        direct_edges = [e for e in edges if contained(support(n, e), side)] + [port_vertices]
        direct = cyclic_flats(n, direct_edges)
        require(predicted == direct, '多重侧回装不等于直接补边')
    rejected = False
    try:
        wrong, _ = reconstruct_side(n, full_data, sides[1], sides, support(n, [2, 3]))
        expected = cyclic_flats(n, [e for e in edges if contained(support(n, e), sides[1])] + [(2, 3)])
        rejected = wrong != expected
    except ValueError:
        rejected = True
    require(rejected, '混用多重数据最小循环的错误入口未被拒绝')
    return {'case': 'parallel_marks_inside_and_on_bare_edge',
            'full_weighted_sides_equal_direct': True,
            'unsimplified_minimal_cycle_shortcut_rejected': True}


def main():
    triangle = lambda vs: list(combinations(vs, 2))
    cases = []
    # S11：三块，端口本来邻接；补边形成真实平行类。
    cases.append(run_case('cycle_of_three_triangles', 6,
        triangle([0, 1, 3]) + triangle([1, 2, 4]) + triangle([2, 0, 5]),
        [{0, 1, 3}, {1, 2, 4}, {2, 0, 5}], [(0, 1), (1, 2), (2, 0)], 0))
    # S12：两块加一条裸边，是无限方向轨道机制的最小型控制。
    cases.append(run_case('two_triangles_one_bare_edge', 5,
        triangle([0, 1, 2]) + triangle([2, 3, 4]) + [(0, 3)],
        [{0, 1, 2}, {2, 3, 4}], [(0, 2), (2, 3)], 1))
    # S12：一块加裸路径，覆盖商空间非零和 k=1 边界。
    cases.append(run_case('triangle_bare_path_length_two', 4,
        triangle([0, 1, 2]) + [(0, 3), (3, 1)],
        [{0, 1, 2}], [(0, 1)], 2))
    # 端口不邻接：两个四循环沿循环骨架连接，检验真正补非边。
    left = [(0, 1), (1, 2), (2, 3), (3, 0)]
    right = [(2, 4), (4, 5), (5, 6), (6, 2)]
    cases.append(run_case('two_squares_bare_path_length_two', 8,
        left + right + [(0, 7), (7, 5)],
        [{0, 1, 2, 3}, {2, 4, 5, 6}], [(0, 2), (2, 5)], 2))
    cases.append(parallel_control())
    print(json.dumps({'scope': 'finite exact controls, not a general proof', 'results': cases}, indent=2))


if __name__ == '__main__':
    main()
