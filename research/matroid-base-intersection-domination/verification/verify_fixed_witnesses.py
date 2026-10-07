"""固定功能复核：与发现/构造的消元实现隔离，不证明无限量词。"""

import argparse
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
import resource_guard as resource

if not __debug__:
    raise RuntimeError('固定验证禁止 -O / -OO；这些选项会禁用断言检查')


def dimension(columns, width):
    # 按坐标行对列矩阵消元，与发现端逐列最高位字典实现分开。
    rows = [sum(((v >> bit) & 1) << i for i, v in enumerate(columns)) for bit in range(width)]
    answer = 0
    for col in range(len(columns)):
        found = next((j for j in range(answer, width) if (rows[j] >> col) & 1), None)
        if found is None:
            continue
        rows[answer], rows[found] = rows[found], rows[answer]
        for j in range(width):
            if j != answer and (rows[j] >> col) & 1:
                rows[j] ^= rows[answer]
        answer += 1
        if answer == width:
            break
    return answer


def dot(u, v):
    return (u & v).bit_count() % 2


def verify_binary(record):
    d, r, q = record['d'], record['rank'], record['q']
    assert d in (5, 8) and r == d + 2 and q == ((1 << (d - 1)) + d - 1) // d - 1
    columns = record['columns']
    assert len(columns) == len(set(columns)) and 0 not in columns
    assert all(0 < v < (1 << r) for v in columns) and len(columns) <= 533
    assert dimension(columns, r) == r
    minimum, connected = record['minimum_bases'], record['connected_bases']
    assert len(minimum) == q and len(connected) == q + 1
    for bases in (minimum, connected):
        assert len({tuple(sorted(b)) for b in bases}) == len(bases)
        assert all(len(b) == r and len(set(b)) == r and set(b) <= set(columns)
                   and dimension(b, r) == r for b in bases)
    c = {v for v in columns if dot(1, v)}
    assert len(c) == q * r and set().union(*map(set, minimum)) == c
    assert sum(map(len, minimum)) == len(c)
    w = 1 << d
    support_d = {v for v in columns if dot(w, v)}
    assert support_d <= set().union(*map(set, connected))
    assert all(record['shared_element'] in b for b in connected)
    assert dimension([v for v in columns if v not in c], r) == r - 1
    assert dimension([v for v in columns if v not in support_d], r) == r - 1
    ha = [v for v in columns if not v & 1 and not v & (1 << (d + 1))]
    hb = [v for v in columns if not v & 1 and not v & w]
    assert len(ha) == len(hb) == (1 << d) - 1
    cocircuits = 0
    for u in range(1, 1 << r):
        if u % 32 == 0:
            resource.gate()
        complement = [v for v in columns if not dot(u, v)]
        if dimension(complement, r) != r - 1:
            continue
        cocircuits += 1
        if u == 1:
            continue
        pieces = [[v for v in block if dot(u, v)] for block in (ha, hb)]
        assert any(len(piece) == (1 << (d - 1)) and dimension(piece, r) == d for piece in pieces)
    return {'d': d, 'rank': r, 'q': q, 'elements': len(columns), 'cocircuits_checked': cocircuits,
            'connected_size': q + 1, 'F_1': q + (q - 1 + r - 2) // (r - 1)}


def rejection(record, mutation):
    altered = copy.deepcopy(record)
    mutation(altered)
    try:
        verify_binary(altered)
    except AssertionError:
        return True
    raise AssertionError('破坏控制未被检出')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-write', action='store_true', help='只向stdout回报，供只读守卫运行')
    args = parser.parse_args()
    bundle = json.loads((HERE / 'results' / 'fixed_simple_binary.json').read_text(encoding='utf-8'))
    records = bundle['witnesses']
    assert [row['d'] for row in records] == [5, 8]
    positive = [verify_binary(row) for row in records]
    negatives = []
    for row in records:
        negatives.append({'d': row['d'], 'duplicate_matrix_column': rejection(
            row, lambda x: x['columns'].append(x['columns'][0]))})
        def destroy_basis(x):
            x['minimum_bases'][0][-1] = x['minimum_bases'][0][0]
        negatives.append({'d': row['d'], 'dependent_minimum_basis': rejection(row, destroy_basis)})
    output = {'status': 'PASS_FIXED_ONLY', 'positive': positive, 'negative_controls': negatives,
              'peak_bytes': resource.gate(), 'boundary': 'no full graph or all-family enumeration; no priority claim'}
    if not args.no_write:
        destination = HERE / 'results' / 'fixed_guard.json'
        destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    main()
