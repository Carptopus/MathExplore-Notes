"""Regression guard for the finite-p two-item family in S6.

This checks the stationarity parametrization and selected numerical values.
It does not prove that the family is globally sharp over all 2x2 matrices.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize_scalar


def stationary_point(p: float, r: float) -> tuple[float, float, float, float]:
    c = 1.0 - r
    y = brentq(lambda value: 2.0 * r * value - c * (1.0 - value**p), 0.0, 1.0)
    t_sq = 2.0 * y / (c * (1.0 + y**p))
    t = np.sqrt(t_sq)
    d = 1.0 / t + r * t
    e = c * t
    return y, t, d, e


def family_ratio(p: float, r: float) -> float:
    _, _, d, e = stationary_point(p, r)
    numerator = ((1.0 + r) ** p + (1.0 - r) ** p) ** (1.0 / p)
    denominator = (d**p + e**p) ** (1.0 / p)
    return numerator / denominator


def main() -> None:
    expected = {
        1.5: 1.006290719101,
        2.0: 1.017898490669,
        3.0: 1.042098941719,
        4.0: 1.062586305441,
        10.0: 1.123156010933,
    }
    for p, target in expected.items():
        outer = minimize_scalar(
            lambda value: -family_ratio(p, value),
            bounds=(1.0e-8, 1.0 - 1.0e-8),
            method="bounded",
            options={"xatol": 1.0e-13},
        )
        r = float(outer.x)
        ratio = -float(outer.fun)
        y, t, d, e = stationary_point(p, r)
        derivative = d ** (p - 1.0) * (r - 1.0 / t**2) + (1.0 - r) ** p * t ** (p - 1.0)
        assert 0.0 < y < 1.0
        assert t < 1.0 / np.sqrt(r)
        assert abs(e / d - y) < 2.0e-12
        assert abs(derivative) < 2.0e-10
        assert abs(ratio - target) < 2.0e-9
        print(f"p={p:g} r={r:.12f} C_family={ratio:.12f}")

    print("PASS: finite-p two-item stationarity and numerical regressions")


if __name__ == "__main__":
    main()
