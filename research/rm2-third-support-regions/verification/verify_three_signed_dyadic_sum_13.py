"""Bounded destructive check for the three-term signed-dyadic lemma.

The proof in the research record is valuation-theoretic and covers arbitrary
negative exponents.  This script only guards the formula and the three stated
integer multisets against transcription drift.
"""

from fractions import Fraction
from itertools import combinations_with_replacement


def main() -> None:
    terms = {Fraction(0)}
    for exponent in range(-20, 6):
        value = Fraction(2) ** exponent
        terms.update((value, -value))

    solutions = {
        values
        for values in combinations_with_replacement(sorted(terms), 3)
        if sum(values) == 13
    }
    assert all(value.denominator == 1 for values in solutions for value in values)
    assert solutions == {
        (Fraction(-4), Fraction(1), Fraction(16)),
        (Fraction(-2), Fraction(-1), Fraction(16)),
        (Fraction(1), Fraction(4), Fraction(8)),
    }
    print("PASS: no fractional solution for exponents -20..5")
    print("SOLUTIONS: (-4,1,16), (-2,-1,16), (1,4,8)")


if __name__ == "__main__":
    main()
