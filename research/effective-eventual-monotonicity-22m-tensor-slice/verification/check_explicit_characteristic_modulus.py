"""Exact algebra checks for explicit global bounds on the increment CF.

The inequalities themselves are proved by the case split recorded in S34.
This script freezes the polynomial identities and checks destructive samples.
"""

from __future__ import annotations

import math
import random

import sympy as sp


def main() -> None:
    a, b, c = sp.symbols("a b c", real=True)
    aa, bb, cc = a * a, b * b, c * c
    k = bb + cc / 2
    d1 = 1 - aa / 3 + bb + cc / 2 - 2 * sp.I * a / sp.sqrt(3)
    d2 = 1 + cc / 2 + 2 * sp.I * a / sp.sqrt(3)
    product = sp.expand(d1 * d2)

    expected_real = 1 + aa + bb + cc + bb * cc / 2 + cc**2 / 4 - aa * cc / 6
    expected_imag = 2 * a / sp.sqrt(3) * (bb - aa / 3)
    assert sp.simplify(sp.re(product) - expected_real) == 0
    assert sp.simplify(sp.im(product) - expected_imag) == 0

    d1_modulus_squared = sp.expand_complex(d1 * sp.conjugate(d1))
    expected_d1 = (1 + k - aa / 3) ** 2 + 4 * aa / 3
    assert sp.simplify(d1_modulus_squared - expected_d1) == 0

    d2_modulus_squared = sp.expand_complex(d2 * sp.conjugate(d2))
    expected_d2 = (1 + cc / 2) ** 2 + 4 * aa / 3
    assert sp.simplify(d2_modulus_squared - expected_d2) == 0

    rng = random.Random(3401)
    for _ in range(20_000):
        values = [rng.uniform(-8.0, 8.0) for _ in range(3)]
        radius_squared = sum(value * value for value in values)
        if radius_squared == 0.0:
            continue
        av, bv, cv = values
        d1v = 1 - av * av / 3 + bv * bv + cv * cv / 2 - 2j * av / math.sqrt(3)
        d2v = 1 + cv * cv / 2 + 2j * av / math.sqrt(3)
        modulus = abs(d1v * d2v)
        if radius_squared <= 1.0:
            assert modulus >= 1.0 + 23.0 * radius_squared / 24.0 - 2.0e-14
        else:
            assert modulus * modulus >= 1.0 + radius_squared / 2.0 - 2.0e-12

    print("PASS exact real/imaginary product identities")
    print("PASS exact individual determinant modulus identities")
    print("PASS destructive samples satisfy the S34 two-regime bounds")


if __name__ == "__main__":
    main()
