"""Regression checks for the all-p nilpotent lower-bound curve."""

import math


def lower_power(p: float) -> float:
    return (2.0**p + 2.0) / 2.0 ** (p / 2.0 + 1.5)


def family_power(p: float, r: float) -> float:
    q = 2.0 * math.sqrt(r * (1.0 - r))
    return q**p * (1.0 + 2.0 ** (1.0 - p)) / (
        2.0 * (1.0 - r) ** p + (2.0 * r) ** p
    )


for exponent in (1.0, 1.25, 1.5, 2.0, 3.0, 5.0, 10.0, 50.0):
    t = 2.0 ** (1.0 / exponent - 1.0)
    r = t / (1.0 + t)
    actual = family_power(exponent, r)
    expected = lower_power(exponent)
    if not math.isclose(actual, expected, rel_tol=2e-13, abs_tol=2e-13):
        raise AssertionError((exponent, actual, expected))

    # The public Zhang v1 construction is the r=1/3 member of this family.
    zhang = family_power(exponent, 1.0 / 3.0)
    if exponent < 50.0 and not actual > zhang:
        raise AssertionError(("no strict finite-p improvement", exponent, actual, zhang))

if not math.isclose(lower_power(1.0), 1.0, rel_tol=0.0, abs_tol=1e-15):
    raise AssertionError("trace endpoint")
if not math.isclose(lower_power(2.0), 3.0 * math.sqrt(2.0) / 4.0, rel_tol=2e-15):
    raise AssertionError("Frobenius specialization")
if not math.isclose(lower_power(200.0) ** (1.0 / 200.0), math.sqrt(2.0), rel_tol=6e-3):
    raise AssertionError("operator endpoint limit")

print("PASS: all-p nilpotent lower curve")
print("L_2 =", math.sqrt(lower_power(2.0)))
print("L_10 =", lower_power(10.0) ** 0.1)
