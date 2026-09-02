from __future__ import annotations

from math import comb, factorial
from fractions import Fraction


def row(r: int, n_max: int):
    """Yield exact rows C_r(n,k), starting with n=0."""
    previous = [1]
    yield previous
    for n in range(1, n_max + 1):
        current = [0] * (n + 1)
        for k in range(n + 1):
            value = 0
            linear = n + (r - 1) * k - 1
            if k < len(previous):
                value += linear * previous[k]
            if k > 0:
                value += (
                    factorial(r - 1)
                    * comb(linear, r - 1)
                    * previous[k - 1]
                )
            current[k] = value
        previous = current
        yield current


def first_failure(r: int, n_max: int):
    for n, values in enumerate(row(r, n_max)):
        for k in range(1, n):
            defect = values[k] * values[k] - values[k - 1] * values[k + 1]
            if defect < 0:
                return n, k, values[k - 1 : k + 2], defect
    return None


def minimum_normalized_margin(r: int, n_max: int):
    best = None
    for n, values in enumerate(row(r, n_max)):
        for k in range(1, n):
            if values[k] == 0:
                continue
            left = values[k] * values[k]
            right = values[k - 1] * values[k + 1]
            if right == 0:
                continue
            # Store the exact ratio left/right; compare by cross multiplication.
            candidate = (left, right, n, k)
            if best is None or left * best[1] < best[0] * right:
                best = candidate
    return best


def direct_composition_value(r: int, n: int, k: int) -> int:
    """Independent coefficient formula, avoiding the triangular recurrence."""
    if k == 0:
        return int(n == 0)
    excess = n - k
    if excess < 0:
        return 0
    coefficients = [Fraction(1, r + degree) for degree in range(excess + 1)]
    polynomial = [Fraction(1)]
    for _ in range(k):
        updated = [Fraction(0)] * (min(excess, len(polynomial) - 1 + excess) + 1)
        for i, left in enumerate(polynomial):
            for j, right in enumerate(coefficients[: excess - i + 1]):
                if i + j <= excess:
                    updated[i + j] += left * right
        polynomial = updated
    size = n + (r - 1) * k
    value = Fraction(factorial(size), factorial(k)) * polynomial[excess]
    assert value.denominator == 1
    return value.numerator


def main() -> None:
    # Cross-check the recurrence against the independent coefficient formula
    # C_r(n,k)=N!/k! [z^(n-k)](sum_{j>=0} z^j/(r+j))^k.
    for r in range(2, 8):
        for n, values in enumerate(row(r, 9)):
            for k, value in enumerate(values):
                assert value == direct_composition_value(r, n, k)
    print("PASS: recurrence agrees with the independent composition formula")

    for r in range(2, 13):
        failure = first_failure(r, 250)
        margin = minimum_normalized_margin(r, 250)
        if margin is None:
            margin_text = "n/a"
        else:
            margin_text = f"{margin[0] / margin[1]:.12g} at (n,k)=({margin[2]},{margin[3]})"
        print(f"r={r}: first_failure={failure}; min_ratio={margin_text}")

    # Regression certificate for the symbolic all-r argument recorded in S2.
    # The finite checks below do not themselves prove global monotonicity:
    # S2 proves it by expanding denominator-minus-numerator of R(r+1)/R(r)
    # after r=s+1 and observing that every coefficient is positive.
    shifted_coefficients = (11, 143, 718, 1742, 2047, 947, 20)
    assert all(coefficient > 0 for coefficient in shifted_coefficients)

    def middle_ratio(r: int) -> Fraction:
        return Fraction(
            6 * r * factorial(2 * r + 1) ** 2,
            (r + 1) ** 2 * factorial(3 * r) * factorial(r + 1),
        )

    assert middle_ratio(5) == Fraction(55, 39) > 1
    assert middle_ratio(6) == Fraction(5148, 5831) < 1
    for r in range(1, 50):
        assert middle_ratio(r + 1) < middle_ratio(r)
    print("PASS: the n=3 middle inequality holds exactly for 2 <= r <= 5")

    # For r=3, Sagan's criterion applies to c_k=L and d_k=L(L-1),
    # with L=n+2k-1.  The mixed slack is exactly 8(L-1).
    for n in range(1, 100):
        for k in range(1, n):
            L = n + 2 * k - 1
            c_minus, c, c_plus = L - 2, L, L + 2
            d_minus = (L - 2) * (L - 3)
            d = L * (L - 1)
            d_plus = (L + 2) * (L + 1)
            slack = 2 * d * c - (d_minus * c_plus + d_plus * c_minus)
            assert slack == 8 * (L - 1) >= 0
    print("PASS: Sagan mixed-coefficient slack for r=3 is 8(L-1)")


if __name__ == "__main__":
    main()
