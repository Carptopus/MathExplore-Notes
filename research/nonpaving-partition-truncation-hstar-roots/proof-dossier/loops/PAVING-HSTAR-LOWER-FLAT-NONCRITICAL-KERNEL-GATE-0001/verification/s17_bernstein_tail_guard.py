"""S17 的有限有理补集与连续多项式证书；不证明剩余全 l 不等式。"""

import json
from fractions import Fraction
from math import comb

import sympy as sp


def laurent_powers(limit):
    # P_r(z)=(2-z+z^-1)^r；整数递推，不枚举样本对象。
    powers = [{0: 1}]
    for r in range(limit):
        previous = powers[-1]
        powers.append({j: 2 * previous.get(j, 0) - previous.get(j - 1, 0)
                       + previous.get(j + 1, 0)
                       for j in range(-r - 1, r + 2)})
    return powers


def u_numerator(n, l, powers):
    r = n - l
    value = sum((-1) ** (j // 2) * sum(comb(l, s) * powers[r][j + s]
                for s in range(min(l, r - j) + 1))
                for j in range(2, r + 1, 2))
    return (-1) ** (n // 4) * value


def continuous_certificate(radius, a_power, b_power, ceiling):
    x, t = sp.symbols('x t')
    b = (radius - 1 / radius) / 2
    a = 2 + b * b - 2 * b * x - x * x
    b_poly = 1 + 1 / radius ** 2 + 2 * x / radius
    polynomial = sp.expand(ceiling - a ** a_power * b_poly ** b_power)
    values = []
    for i in range(16):
        left = -1 + sp.Rational(i, 8)
        q = sp.Poly(sp.expand(polynomial.subs(x, left + t / 8)), t)
        degree = q.degree()
        values.extend(sum(q.nth(j) * sp.binomial(l, j) / sp.binomial(degree, j)
                          for j in range(l + 1)) for l in range(degree + 1))
    assert min(values) > 0
    # 破坏性控制：翻转已认证多项式符号不能再得到全正证书。
    assert min(-v for v in values) < 0
    return str(min(values))


def main():
    # 数学有限补集的硬门：N=4k<160；不开放任意规模参数。
    max_n = 156
    powers = laurent_powers(max_n)
    controls = {(4, 0): Fraction(19, 16), (4, 1): Fraction(5, 8),
                (4, 2): Fraction(1, 4), (8, 5): Fraction(-1, 8),
                (8, 6): Fraction(-1, 4)}
    for (n, l), expected in controls.items():
        assert Fraction(u_numerator(n, l, powers), 2 ** (n - l)) == expected
    checked, smallest_relative_gap = 0, None
    for n in range(4, max_n + 1, 4):
        b_num = (-1) ** (n // 4) * powers[n][0]
        u0_twice_num = 2 ** (3 * n // 2) - b_num
        assert 0 < b_num < 2 ** (3 * n // 2)
        assert 4 * b_num < 2 * 2 ** (3 * n // 2)
        for l in range((n + 2) // 3, n - 1):
            r = n - l
            left = 2 * n * u_numerator(n, l, powers) * 2 ** l
            right = r * u0_twice_num
            gap = right - left
            assert gap >= 0, (n, l, gap)
            ratio = Fraction(gap, right)
            smallest_relative_gap = ratio if smallest_relative_gap is None else min(ratio, smallest_relative_gap)
            checked += 1
        # 末两项为准确零，不靠有限正控外推。
        assert u_numerator(n, n - 1, powers) == 0
        assert u_numerator(n, n, powers) == 0
    certificates = [continuous_certificate(sp.Rational(8, 5), 2, 1, 7),
                    continuous_certificate(sp.Rational(8, 5), 1, 3, 13),
                    continuous_certificate(sp.Integer(3), 1, 3, 8)]
    assert Fraction(7, 8) ** 26 < Fraction(3, 80)
    assert Fraction(13, 16) ** 20 < Fraction(3, 80)
    assert 160 * Fraction(8, 9) ** 80 < 1
    assert Fraction(41, 40) * Fraction(8, 9) ** 2 < 1
    print(json.dumps({'verdict': 'PASS', 'scope': 'N<160 and l>=ceil(N/3); three continuous certificates',
                      'finite_pairs': checked, 'smallest_relative_gap': str(smallest_relative_gap),
                      'continuous_minima': certificates,
                      'controls': 'five Laurent positive controls and three sign destructive controls',
                      'not_proved': 'all k, 3<=l<N/3'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
