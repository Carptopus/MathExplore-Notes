"""Symbolic certificate for the first-order compact-bulk margin.

The analytic proof uses a uniform lattice Edgeworth expansion.  This
script checks the algebraic cancellations in the anti-diagonal ratio and
the first-order expansion of the factorial weight.  It does not claim an
effective finite threshold.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    e, mu, variance = sp.symbols("e mu variance", positive=True)
    common, skew = sp.symbols("common skew", real=True)
    a = mu + 1

    # k=1/e.  For m=k+r and bounded displacement s, the logarithm of the
    # local lattice probability has the uniform first-order form
    #
    # -log(m)/2 + (common + skew*s - s^2/(2 variance))/m + O(k^-2).
    #
    # The unspecified common and skew corrections cancel from the
    # anti-diagonal ratio at order 1/k.
    def log_local(r: int, displacement: sp.Expr) -> sp.Expr:
        m = 1 / e + r
        return (
            -sp.log(m) / 2
            + (common + skew * displacement - displacement**2 / (2 * variance))
            / m
        )

    log_probability_ratio = sp.series(
        2 * log_local(0, 0)
        - log_local(-1, a)
        - log_local(1, -a),
        e,
        0,
        3,
    ).removeO()
    first_probability_coefficient = sp.expand(log_probability_ratio).coeff(e, 1)
    assert sp.simplify(first_probability_coefficient - a**2 / variance) == 0

    # The exact external weight T, with N=(mu+5)k, has logarithm
    # (-1 + 16/(mu+5))/k + O(k^-2).
    total_scaled = mu + 5
    target_weight = 1 / (1 + e)
    for i in range(1, 5):
        target_weight *= (total_scaled + i * e) / (
            total_scaled - (i - 1) * e
        )
    log_target = sp.series(sp.log(target_weight), e, 0, 3).removeO()
    first_target_coefficient = sp.expand(log_target).coeff(e, 1)
    expected_target = -1 + 16 / (mu + 5)
    assert sp.simplify(first_target_coefficient - expected_target) == 0

    margin = sp.factor(first_probability_coefficient - first_target_coefficient)
    expected_margin = (mu + 1) ** 2 / variance + 1 - 16 / (mu + 5)
    assert sp.simplify(margin - expected_margin) == 0

    # For 0<mu<11, positivity is precisely the strict saddle-curvature
    # inequality already certified in verify_saddle_curvature.py:
    # variance*(11-mu) < (mu+1)^2*(mu+5).
    reduced = sp.factor(
        margin * variance * (mu + 5)
        - ((mu + 1) ** 2 * (mu + 5) - variance * (11 - mu))
    )
    assert reduced == 0

    print("PASS: common and skew Edgeworth terms cancel at order 1/k")
    print("PASS: compact-bulk first-order margin equals the certified curvature margin")


if __name__ == "__main__":
    main()
