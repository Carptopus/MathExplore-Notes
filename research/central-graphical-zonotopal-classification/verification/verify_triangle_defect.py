"""小型精确控制：从割幂理想行空间计算长度，不调用循环亏损公式。"""

from fractions import Fraction
from math import comb


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(rows):
    rows = [[Fraction(x) for x in row] for row in rows]
    if not rows:
        return 0
    pivot = 0
    for col in range(len(rows[0])):
        found = next((i for i in range(pivot, len(rows)) if rows[i][col]), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        scale = rows[pivot][col]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for i in range(pivot + 1, len(rows)):
            scale = rows[i][col]
            if scale:
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def power(a, b, degree):
    return [comb(degree, i) * a**i * b ** (degree - i) for i in range(degree + 1)]


def ideal_rows(weights, degree):
    # 边顺序 01,12,02；x2=-x0-x1，全部真割按互补只剩三个单顶点割。
    p, q, r = weights
    generators = [(1, 0, p + r), (0, 1, p + q), (1, 1, q + r)]
    rows = []
    for a, b, exponent in generators:
        if exponent > degree:
            continue
        base = power(a, b, exponent)
        for shift in range(degree - exponent + 1):
            row = [0] * (degree + 1)
            row[shift : shift + exponent + 1] = base
            rows.append(row)
    return rows


def length(weights, potential):
    require(len(weights) == 3 and all(1 <= w <= 4 for w in weights), '仅允许本控制包小规模三角形')
    a, b, c = potential
    a, b = a - c, b - c
    result = 0
    for degree in range(1, 12):
        rows = ideal_rows(weights, degree)
        if rank(rows + [power(a, b, degree)]) == rank(rows):
            return result
        result = degree
    raise RuntimeError('预设次数门内未幂零，拒绝外推')


def main():
    cases = [((1, 1, 1), [1, 1, 1, 1]), ((2, 2, 2), [3, 3, 3, 4]),
             ((2, 2, 4), [5, 5, 3, 6]), ((2, 3, 3), [5, 4, 4, 6])]
    points = [(1, 1, 0), (1, 0, 0), (0, 1, 0), (1, 2, 0)]
    for weights, expected in cases:
        actual = [length(weights, point) for point in points]
        require(actual == expected, f'长度不符: {weights}: {actual}')
        require(length(weights, (1, 1, 1)) == 0, '常势必须为零')
        print({'multiplicities': weights, 'exact_lengths': actual})
    # 故意移植另一图的亏损预测，必须被实际商环乘法拒绝。
    require(length((2, 2, 4), (0, 1, 0)) != length((2, 3, 3), (0, 1, 0)),
            '负控未拒绝粗配置相同即代数相同')
    print('PASS: exact rational cut-ideal controls; not a general reconstruction proof')


if __name__ == '__main__':
    main()
