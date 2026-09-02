from __future__ import annotations

import sympy as sp


MAX_COEFFICIENT = 40
MAX_EXCESS_CALIBRATION = 32


def reciprocal_renewal_coefficients(limit: int) -> list[sp.Rational]:
    """Return c_m from C(z)=1-1/(5 f_5(z)) using the exact ODE recurrence."""
    coefficients = [sp.Rational(0)] * (limit + 1)
    coefficients[1] = sp.Rational(5, 6)
    for m in range(2, limit + 1):
        convolution = sum(
            coefficients[i] * coefficients[m - i] for i in range(1, m)
        )
        coefficients[m] = sp.cancel(
            ((m - 6) * coefficients[m - 1] + 5 * convolution) / (m + 5)
        )
    return coefficients


def normalized_coefficient_polynomials(max_excess: int):
    """Return P_d(k)=5^k [z^d] f_5(z)^k."""
    k, z = sp.symbols("k z")
    positive_part = sp.Poly(
        sum(sp.Rational(5, j + 5) * z**j for j in range(1, max_excess + 2)),
        z,
    )
    powers = [sp.Poly(1, z)]
    for _ in range(max_excess + 1):
        powers.append(powers[-1] * positive_part)

    choose = []
    for m in range(max_excess + 2):
        falling = sp.prod(k - j for j in range(m)) if m else sp.Integer(1)
        choose.append(sp.expand(falling / sp.factorial(m)))

    polynomials = []
    for d in range(max_excess + 2):
        polynomials.append(
            sp.expand(
                sum(
                    choose[m] * powers[m].coeff_monomial(z**d)
                    for m in range(d + 1)
                )
            )
        )
    return k, polynomials


def main() -> None:
    z = sp.symbols("z")
    coefficients = reciprocal_renewal_coefficients(MAX_COEFFICIENT)

    assert coefficients[1:6] == [
        sp.Rational(5, 6),
        sp.Rational(5, 252),
        sp.Rational(5, 378),
        sp.Rational(605, 63504),
        sp.Rational(1381, 190512),
    ]
    assert all(coefficient > 0 for coefficient in coefficients[1:])

    # Cross-check the recurrence against the reciprocal power series itself.
    truncated_a = sum(
        sp.Rational(5, j + 5) * z**j for j in range(MAX_COEFFICIENT + 1)
    )
    reciprocal = sp.series(1 / truncated_a, z, 0, MAX_COEFFICIENT + 1).removeO()
    for m in range(1, MAX_COEFFICIENT + 1):
        assert sp.expand(reciprocal).coeff(z, m) == -coefficients[m]

    # Since A=5f_5=1/(1-C) and every coefficient of C is positive,
    # log A=-log(1-C)=sum_{ell>=1} C^ell/ell has positive coefficients.
    # At a fixed saddle z this is the Levy series of a compound Poisson
    # distribution, so every cumulant is positive.  The truncation below is
    # an independent algebraic control of the general coefficient argument.
    renewal = sum(coefficients[m] * z**m for m in range(1, MAX_COEFFICIENT + 1))
    levy_from_renewal = sp.series(
        -sp.log(1 - renewal), z, 0, MAX_COEFFICIENT + 1
    ).removeO().expand()
    levy_direct = sp.series(
        sp.log(truncated_a), z, 0, MAX_COEFFICIENT + 1
    ).removeO().expand()
    assert sp.expand(levy_from_renewal - levy_direct) == 0
    assert all(levy_direct.coeff(z, m) > 0 for m in range(1, MAX_COEFFICIENT + 1))

    # Discovery calibration only: this does not prove the all-d Turan inequality.
    k, polynomials = normalized_coefficient_polynomials(MAX_EXCESS_CALIBRATION)
    u = sp.symbols("u", nonnegative=True)
    for d in range(1, MAX_EXCESS_CALIBRATION + 1):
        total_size = 5 * k + d
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

    print("PASS: exact reciprocal-renewal recurrence and positive coefficients")
    print("PASS: positive Levy series gives a compound-Poisson saddle law")
    print(
        "PASS (calibration only): shifted defect coefficients are positive for "
        f"1 <= d <= {MAX_EXCESS_CALIBRATION}"
    )


if __name__ == "__main__":
    main()
