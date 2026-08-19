# AI-assisted generation and review: OpenAI Codex. Responsible maintainer: Carptopus.
"""Cross-check spectral separation against exact nSSP verification ranks."""

from __future__ import annotations

from fractions import Fraction

from verify_nssp_weighted_paths import (
    rank_mod_prime,
    verification_matrix,
    weighted_path,
)


def trim(poly: list[Fraction]) -> list[Fraction]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def subtract(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    size = max(len(left), len(right))
    return trim(
        [
            (left[i] if i < len(left) else 0)
            - (right[i] if i < len(right) else 0)
            for i in range(size)
        ]
    )


def remainder(dividend: list[Fraction], divisor: list[Fraction]) -> list[Fraction]:
    work = dividend[:]
    divisor = trim(divisor[:])
    while len(work) >= len(divisor) and any(work):
        shift = len(work) - len(divisor)
        scale = work[-1] / divisor[-1]
        term = [Fraction(0)] * shift + [scale * value for value in divisor]
        work = subtract(work, term)
    return trim(work)


def gcd(left: list[int], right: list[int]) -> list[Fraction]:
    a = [Fraction(value) for value in left]
    b = [Fraction(value) for value in right]
    while any(b):
        a, b = b, remainder(a, b)
    lead = a[-1]
    return [value / lead for value in a]


def zero_diagonal_path_polynomial(edge_weights: list[int]) -> list[int]:
    """Characteristic polynomial, coefficients in ascending degree order."""
    previous = [1]
    current = [0, 1]
    for weight in edge_weights:
        x_current = [0] + current
        square_previous = [-(weight * weight) * value for value in previous]
        size = max(len(x_current), len(square_previous))
        following = [
            (x_current[i] if i < len(x_current) else 0)
            + (square_previous[i] if i < len(square_previous) else 0)
            for i in range(size)
        ]
        previous, current = current, following
    return current


def arms_are_coprime(n: int, loop: int) -> bool:
    left_size = loop - 1
    right_size = n - loop
    left = (
        [1]
        if left_size == 0
        else zero_diagonal_path_polynomial(list(range(1, loop - 1)))
    )
    right = (
        [1]
        if right_size == 0
        else zero_diagonal_path_polynomial(list(range(loop + 1, n)))
    )
    return len(gcd(left, right)) == 1


def main() -> None:
    checked = 0
    for n in range(2, 16):
        for loop in range(1, n + 1):
            matrix = weighted_path(n, loop)
            verification = verification_matrix(matrix)
            has_full_rank_mod_p = (
                rank_mod_prime(verification) == len(verification[0])
            )
            separated = arms_are_coprime(n, loop)
            expected = n % 2 == 0 or loop % 2 == 1
            if separated != expected or has_full_rank_mod_p != expected:
                raise AssertionError(
                    f"n={n}, loop={loop}: coprime={separated}, "
                    f"full_rank_mod_p={has_full_rank_mod_p}, "
                    f"expected={expected}"
                )
            checked += 1
    print(
        f"PASS: {checked} cases; arm coprimality, mod-p rank calibration, "
        "and the parity classification agree for 2<=n<=15"
    )


if __name__ == "__main__":
    main()
