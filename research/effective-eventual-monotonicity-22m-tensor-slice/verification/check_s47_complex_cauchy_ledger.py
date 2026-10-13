"""Interval and symbolic ledger for the S47 complex-Cauchy supplement.

The proof of the parameter-uniform inequalities is written in S47.  This
script freezes the derivative formulas and checks every advertised numerical
margin with outward interval arithmetic.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp


def main() -> None:
    s0, s1, s2 = sp.symbols("s0 s1 s2")
    d1 = (1 - s0 / sp.sqrt(3)) ** 2 - s1**2 - s2**2 / 2
    d2 = 1 + 2 * s0 / sp.sqrt(3) - s2**2 / 2
    assert sp.simplify(sp.diff(d1, s0) + 2 * (1 - s0 / sp.sqrt(3)) / sp.sqrt(3)) == 0
    assert sp.simplify(sp.diff(d1, s1) + 2 * s1) == 0
    assert sp.simplify(sp.diff(d1, s2) + s2) == 0
    assert sp.simplify(sp.diff(d2, s0) - 2 / sp.sqrt(3)) == 0
    assert sp.diff(d2, s1) == 0
    assert sp.simplify(sp.diff(d2, s2) + s2) == 0

    iv = mp.iv
    iv.dps = 100
    one = iv.mpf(1)
    r0 = iv.mpf(2) ** 128

    # Middle-frequency coordinate derivative bounds on |s_j| <= 1+1/(64r).
    h = one / (64 * r0)
    middle_d1_gradient = 2 / iv.sqrt(3) * (1 + (1 + h) / iv.sqrt(3)) + 3 * (1 + h)
    middle_d2_gradient = 2 / iv.sqrt(3) + 1 + h
    assert middle_d1_gradient.b < iv.mpf(5).a
    assert middle_d2_gradient.b < iv.mpf(3).a
    middle_log_loss = (16 * r0 + 10) / (128 * r0)
    assert middle_log_loss.b < (one / 4).a

    middle_cauchy_constant = 16 * 24 * 64**4 * (
        iv.exp(one / 4) + iv.mpf("3e4")
    )
    assert middle_cauchy_constant.b < iv.mpf("1e30").a

    # For u>=1 and |s_j|<2u, the displayed affine majorants dominate the
    # exact gradient sums coefficientwise.
    assert (2 / iv.sqrt(3)).b < iv.mpf(2).a
    assert (iv.mpf(2) / 3 + 6).b < iv.mpf(8).a
    assert (2 / iv.sqrt(3)).b < iv.mpf(2).a
    high_log_loss = (10 + 8 / r0) / 8192
    assert high_log_loss.b < (one / 512).a

    high_cauchy_constant = 16 * 24 * 4096**4 * (
        iv.exp(one / 512) + iv.mpf("2e4") * iv.exp(one / 4096)
    )
    assert high_cauchy_constant.b < iv.mpf("1e30").a

    # Correct logarithmic derivative of the high-frequency L2 bound divided
    # by r^(-5/2): 6 + 3/4 + 5/2 = 37/4.
    high_relative_derivative = iv.mpf(37) / 4 - r0 * iv.log(iv.mpf(3) / 2) / 4
    assert high_relative_derivative.b < iv.mpf(0).a

    print("PASS exact d1,d2 derivative formulas")
    print("PASS middle-frequency nonvanishing and Cauchy constant ledger")
    print("PASS high-frequency nonvanishing and Cauchy constant ledger")
    print("PASS corrected high-frequency logarithmic derivative is negative")


if __name__ == "__main__":
    main()
