from __future__ import annotations

import sympy as sp


MAX_EXCESS = 18


def normalized_coefficient_polynomials(max_excess: int):
    """Return P_d(k)=5^k [z^d] f_5(z)^k for 0<=d<=max_excess+1."""
    k, z = sp.symbols("k z")
    truncation = sum(
        sp.Rational(5, j + 5) * z**j for j in range(max_excess + 2)
    )
    positive_part = truncation - 1
    powers = [sp.Integer(1)]
    for _ in range(max_excess + 1):
        powers.append(sp.expand(powers[-1] * positive_part))

    polynomials = []
    for d in range(max_excess + 2):
        coefficient = sum(
            sp.binomial(k, m) * powers[m].coeff(z, d) for m in range(d + 1)
        )
        polynomials.append(sp.factor(sp.combsimp(coefficient)))
    return k, polynomials


def main() -> None:
    k, polynomials = normalized_coefficient_polynomials(MAX_EXCESS)
    u = sp.symbols("u", nonnegative=True)

    for d in range(1, MAX_EXCESS + 1):
        total_size = 5 * k + d
        # After cancelling common positive factorial and power-of-five factors,
        # this is the numerator of
        # C_5(k+d,k)^2-C_5(k+d,k-1)C_5(k+d,k+1).
        defect = (
            (k + 1)
            * total_size
            * (total_size - 1)
            * (total_size - 2)
            * (total_size - 3)
            * polynomials[d] ** 2
            - k
            * (total_size + 1)
            * (total_size + 2)
            * (total_size + 3)
            * (total_size + 4)
            * polynomials[d + 1].subs(k, k - 1)
            * polynomials[d - 1].subs(k, k + 1)
        )
        numerator = sp.cancel(defect).as_numer_denom()[0]
        shifted = sp.Poly(sp.expand(numerator.subs(k, u + 1)), u)
        assert all(coefficient > 0 for coefficient in shifted.all_coeffs()), d

    print(
        "PASS: exact positive-coefficient certificates for all "
        f"1 <= n-k <= {MAX_EXCESS} and every k >= 1"
    )


if __name__ == "__main__":
    main()
