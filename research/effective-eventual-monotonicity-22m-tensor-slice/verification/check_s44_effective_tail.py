"""Exact constant ledger for the S44 effective eventual-monotonicity tail."""

from __future__ import annotations

from pathlib import Path
import sys

import mpmath as mp
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))

from derive_edgeworth_coefficient import (  # noqa: E402
    W0,
    W1,
    W2,
    exact_edgeworth_polynomials,
)


def even_moment(power: int) -> sp.Integer:
    assert power % 2 == 0
    return sp.factorial2(power - 1) if power else sp.Integer(1)


def second_coefficient_bound() -> sp.Rational:
    _, second = exact_edgeworth_polynomials()
    variables = (W0, W1, W2)
    total = sp.Integer(0)
    poly = sp.Poly(second, *variables)
    assert poly.total_degree() == 12
    assert len(poly.terms()) == 51
    for powers, coefficient in poly.terms():
        assert all(power % 2 == 0 for power in powers)
        radial = sp.Integer(0)
        for selected in range(3):
            moment = sp.Integer(1)
            for index, power in enumerate(powers):
                moment *= even_moment(power + (2 if index == selected else 0))
            radial += moment
        total += 3 * abs(coefficient) * radial
    return sp.factor(total)


def main() -> None:
    iv = mp.iv
    iv.dps = 100
    r0 = iv.mpf(2) ** 128
    log_r = iv.log(r0)
    cutoff = r0 ** (iv.mpf(1) / 16)
    decay = iv.mpf(23) / 47

    log_medium = (
        iv.log(iv.mpf("1e30"))
        + 6 * log_r
        + iv.mpf("0.5")
        * (
            iv.log(4 * iv.pi)
            + 80 * iv.log(2)
            - iv.log(decay)
            + 81 * iv.log(cutoff)
            - decay * cutoff**2
        )
    )
    log_high = (
        iv.log(iv.mpf("1e30"))
        + 6 * log_r
        + iv.mpf("0.5")
        * (
            iv.log(4 * iv.pi)
            + iv.mpf(3) / 2 * log_r
            + (-r0 / 2 + 43) * iv.log(iv.mpf(3) / 2)
            + 123 * iv.log(2)
            - iv.log(3)
        )
    )
    target = -iv.mpf(5) / 2 * log_r
    assert log_medium.b < target.a
    assert log_high.b < target.a

    # Derivatives with respect to t=log(r) of log(bound/r^(-5/2)).
    medium_derivative = (
        iv.mpf("8.5")
        + iv.mpf(81) / 32
        - decay / 16 * r0 ** (iv.mpf(1) / 8)
    )
    high_derivative = iv.mpf(37) / 4 - iv.log(iv.mpf(3) / 2) * r0 / 4
    assert medium_derivative.b < iv.mpf(0).a
    assert high_derivative.b < iv.mpf(0).a

    d_bound = second_coefficient_bound()
    assert d_bound == sp.Rational(540373, 144)

    b_total = iv.mpf("1.221e50")
    plancherel = 3 * iv.sqrt(5) / (8 * iv.sqrt(iv.pi))
    k_bound = plancherel * b_total
    assert k_bound.b < iv.mpf("5.78e49").a
    c_lower = iv.mpf("0.0853526992029")
    d_threshold = 12 * (iv.mpf(540373) / 144) / c_lower
    error_threshold = (8 * iv.mpf("5.78e49") / c_lower) ** 2
    assert d_threshold.b < iv.mpf("5.28e5").a
    assert error_threshold.b < iv.mpf("2.94e103").a
    assert r0.b < iv.mpf("3e103").a
    assert error_threshold.b < iv.mpf("3e103").a

    print("PASS medium/high L2 bounds at r=2^128 and monotone thereafter")
    print(f"PASS exact second-coefficient bound |D| <= {d_bound}")
    print(f"PASS outward interval weighted remainder K in {k_bound}")
    print(f"PASS outward interval strict-monotonicity threshold in {error_threshold}")


if __name__ == "__main__":
    main()
