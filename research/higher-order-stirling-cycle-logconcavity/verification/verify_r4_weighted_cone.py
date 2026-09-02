from __future__ import annotations

from fractions import Fraction
from math import factorial

import sympy as sp

from probe_stirling_logconcavity import row


def main() -> None:
    n, k, rho = sp.symbols("n k rho", positive=True)
    p = 3

    def a(j):
        return (n + p * j - 1) / (n + p * j)

    def b(j):
        return j / (n + p * j)

    def weight(nn, j):
        size = nn + p * j
        return j / (j + 1) * sp.prod(
            (size + i) / (size - p + i) for i in range(1, p + 1)
        )

    worst_defect = (a(k) * rho + b(k)) ** 2 - weight(n, k) * rho * (
        a(k - 1) + b(k - 1) / (weight(n - 1, k - 1) * rho)
    ) * (a(k + 1) * rho / weight(n - 1, k) + b(k + 1))

    numerator, denominator = sp.cancel(worst_defect).as_numer_denom()
    polynomial = sp.Poly(numerator, rho)
    leading = sp.factor(polynomial.coeff_monomial(rho**2))
    discriminant = sp.factor(sp.discriminant(polynomial.as_expr(), rho))
    size = n + 3 * k

    expected_denominator = size**2 * (size - 3) ** 2 * (size - 2) ** 2 * (size - 1) ** 2
    expected_leading = 9 * (size - 3) ** 2 * (size - 2) ** 2 * (size - 1) ** 2
    expected_discriminant = (
        -972
        * k**2
        * (size - 4) ** 2
        * (size - 3) ** 2
        * (size - 2) ** 3
        * (size - 1) ** 2
        * (size + 2)
    )

    assert sp.factor(denominator - expected_denominator) == 0
    assert sp.factor(leading - expected_leading) == 0
    assert sp.factor(discriminant - expected_discriminant) == 0
    print("PASS: r=4 weighted-cone denominator, leading coefficient, and discriminant")

    # Finite destructive check of the exact weighted inequality.  This is not
    # used as the general proof; it catches indexing or normalization drift.
    p_integer = 3
    for row_index, values in enumerate(row(4, 40)):
        normalized = [
            Fraction(values[j] * factorial(j), factorial(row_index + p_integer * j))
            for j in range(row_index + 1)
        ]
        for j in range(1, row_index):
            size_j = row_index + p_integer * j
            weight_j = Fraction(j, j + 1)
            for i in range(1, p_integer + 1):
                weight_j *= Fraction(size_j + i, size_j - p_integer + i)
            assert normalized[j] ** 2 >= weight_j * normalized[j - 1] * normalized[j + 1]
    print("PASS: exact r=4 weighted inequalities through n=40")


if __name__ == "__main__":
    main()
