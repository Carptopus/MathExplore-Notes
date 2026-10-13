"""Constant-ledger checks for the S43 complex-Cauchy derivative bound."""

from __future__ import annotations

import math

import mpmath as mp


def main() -> None:
    iv = mp.iv
    iv.dps = 100
    a = iv.sqrt(3) / 64

    # epsilon*||zeta|| <= 1/128 + a/256 < 1/120.
    assert (iv.mpf(1) / 128 + a / 256).b < (iv.mpf(1) / 120).a

    # Complex q ledger: R_zeta^2 coefficient and absolute constant.
    r2_coefficient = (
        iv.mpf(2) / 120
        + iv.mpf(3) / (4 * 120**2)
        + iv.mpf(5) / (6 * 256**2)
        + iv.mpf(1) / 120**3
        + iv.mpf(5) / (3 * 120**4)
    )
    constant = (
        iv.mpf(10) / 256**2
        + iv.mpf(13) / (9 * iv.sqrt(3) * 120**3)
        + iv.mpf(41) / (36 * 120**4)
    )
    assert r2_coefficient.b < (iv.mpf(1) / 50).a
    assert constant.b < (iv.mpf(1) / 1000).a

    # The loss in the real Gaussian exponent, including the Young step for
    # 2*a*R/50, fits inside the advertised 1/25 constant.
    exponent_constant = a + a * a / 2 + iv.mpf(1) / 1000
    exponent_constant += a * a / 50 + (a / 25) ** 2 / (4 * iv.mpf("0.01"))
    exponent_constant += iv.mpf(1) / 1000
    assert exponent_constant.b < (iv.mpf(1) / 25).a

    bell_prefactor = iv.mpf(13) / 30 * 73**5
    complex_prefactor = iv.exp(iv.mpf(1) / 25) * (1 + a) ** 30 * (
        7 + bell_prefactor
    )
    assert complex_prefactor.b < iv.mpf("4e9").a

    cauchy_prefactor = iv.mpf("4e9") * math.factorial(4) * 64**4
    assert cauchy_prefactor.b < iv.mpf("2e18").a

    decay = iv.mpf(94) / 100
    integral = 4 * iv.pi * 2**67 * (
        iv.mpf("0.5") * decay ** (-iv.mpf(3) / 2) * iv.gamma(iv.mpf(3) / 2)
        + iv.mpf("0.5") * decay ** (-iv.mpf(71) / 2) * iv.gamma(iv.mpf(71) / 2)
    )
    b_low = iv.mpf("3.2e19") * iv.sqrt(integral)
    assert integral.b < iv.mpf("1.452e61").a
    assert b_low.b < iv.mpf("1.220e50").a

    print("PASS complex-polydisc scale and q ledger")
    print("PASS Gaussian exponent and Bell prefactor ledger")
    print("PASS four-derivative Cauchy prefactor")
    print(f"PASS outward interval low-frequency L2 constant B_low in {b_low}")


if __name__ == "__main__":
    main()
