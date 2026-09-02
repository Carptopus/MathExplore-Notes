from __future__ import annotations

from fractions import Fraction
from math import factorial


def harmonic_segment(start: int, stop: int) -> Fraction:
    return sum((Fraction(1, value) for value in range(start, stop + 1)), Fraction())


def main() -> None:
    # Direct exact check of the finite prefix left by the analytic estimate.
    for n in range(3, 25):
        s2 = harmonic_segment(5, n + 3)
        s3 = sum(
            (
                Fraction(1, right) * harmonic_segment(5, right - 5)
                for right in range(10, n + 8)
            ),
            Fraction(),
        )
        c1 = factorial(n + 3)
        c2 = factorial(n + 7) * s2
        c3 = factorial(n + 11) * s3
        assert c2 * c2 > c1 * c3, n

    # Rational certificate used at x=n+4>=29.  We use sqrt(2)>7/5 and
    # log(29/5)>7/4; the latter follows from the Taylor upper bound below.
    coefficient = Fraction(7, 5) - Fraction(33, 29) ** 2
    assert coefficient * Fraction(7, 4) > Fraction(33, 29) ** 2 * Fraction(4, 29)

    x = Fraction(7, 4)
    partial = sum((x**j / factorial(j) for j in range(4)), Fraction())
    exponential_upper_bound = partial + (x**4 / factorial(4)) / (1 - x / 5)
    assert exponential_upper_bound < Fraction(29, 5)

    print("PASS: exact finite prefix for the k=2 strip")
    print("PASS: rational large-n certificate for every n>=25")


if __name__ == "__main__":
    main()
