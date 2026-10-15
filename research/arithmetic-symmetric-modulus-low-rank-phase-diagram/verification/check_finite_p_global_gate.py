"""Symbolic and destructive guard for the S7 finite-p global gate.

This checks the algebraic identities used in the proof and searches the
three-parameter necessary gate for counterexamples to the balanced-frontier
claim.  It is a regression/falsification guard, not a substitute for the
written proof or its independent audit.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp


def psi(h: float, x: float, q: float) -> float:
    breakpoint = 2.0 * (1.0 - x * x)
    if q <= breakpoint:
        return 1.0 - h * h + q * q / (4.0 * (1.0 - x * x))
    return q - h * h + x * x


def minimized_l_expression(h: float, x: float, q: float) -> float:
    lower = 1.0 - h * h
    stationary = q / 2.0 - h * h + x * x
    ell = max(lower, stationary)
    return ell + q * q / (4.0 * (ell + h * h - x * x))


def first_gate_contact(h: float, x: float, u: float) -> float:
    """First positive tau satisfying S7 (7), using its exact branches."""
    a = max(h - x * u, 0.0)
    one_minus_u_sq = 1.0 - u * u
    if a == 0.0:
        return 2.0 * math.sqrt((1.0 - h * h) / one_minus_u_sq)

    breakpoint_tau = 2.0 * (1.0 - x * x) / a
    quadratic_coefficient = (
        one_minus_u_sq - a * a / (1.0 - x * x)
    ) / 4.0
    if quadratic_coefficient > 0.0:
        quadratic_root = math.sqrt((1.0 - h * h) / quadratic_coefficient)
        if quadratic_root <= breakpoint_tau * (1.0 + 2.0e-12):
            return quadratic_root

    # At a genuinely linear first contact, the branch entrance is infeasible,
    # so the first feasible point is the larger root of the upward quadratic.
    return 2.0 * (a + abs(x - h * u)) / one_minus_u_sq


def balanced_contact(r: float, u: float) -> float:
    if r * (3.0 - u) <= 1.0 + u:
        return 2.0 * (1.0 - r) / math.sqrt(
            (1.0 - u) * (1.0 + u - 2.0 * r)
        )
    return 4.0 * math.sqrt(r) / (1.0 + u)


def symbolic_checks() -> None:
    h, x, u, r, z = sp.symbols("h x u r z", positive=True, real=True)

    discriminant = (h - x * u) ** 2 - (1 - u**2) * (h**2 - x**2)
    assert sp.factor(discriminant - (x - h * u) ** 2) == 0

    numerator = 1 - z + r**2
    denominator = 1 - z - u**2 + 2 * r * u
    derivative = sp.diff(numerator / denominator, z)
    assert sp.factor(derivative - (r - u) ** 2 / denominator**2) == 0

    cross = (1 - h**2) * (1 + u - 2 * h * x) - (1 - h * x) ** 2 * (1 + u)
    at_boundary = sp.factor(cross.subs(u, h / x))
    expected = -h**2 * (x - h) * (x**2 - 1) / x
    assert sp.factor(at_boundary - expected) == 0
    expected_derivative = -h * (h * (x**2 + 1) - 2 * x)
    assert sp.factor(sp.diff(cross, u) - expected_derivative) == 0

    # Linear-entry factorization and the comparisons that close the region
    # where the balanced point itself first contacts the quadratic branch.
    entry = (1 - u**2) * (1 - x**2) ** 2 - (h - x * u) ** 2 * (
        2 - h**2 - x**2
    )
    t1_hx = 1 + h * x - u * (1 - h * x)
    t2_hx = 1 - h * x + u * (1 + h * x)
    z_hx = h**2 + x**2
    assert sp.factor(entry - (z_hx - t1_hx) * (z_hx - t2_hx)) == 0

    t1 = 1 + r - u * (1 - r)
    t2 = 1 - r + u * (1 + r)
    balance_margin = 1 + u - r * (3 - u)
    common = 1 + u - 2 * r
    z_a = (1 - r) ** 2 * (1 + u) ** 2 / ((1 - u) * common) - 2 * r
    z_b = 2 * r + (1 - r) ** 2 * (1 - u) / common
    assert sp.factor(
        t2 - z_a - (r - u) * (1 + u) * balance_margin / ((1 - u) * common)
    ) == 0
    assert sp.factor(
        t1 - z_b - (1 - r) * (u - r) * (1 - u) / common
    ) == 0
    assert sp.factor(
        r / u
        - (1 - r) ** 2 / ((1 - u) * common)
        - (r - u) * (1 - r * (2 - u)) / (u * (1 - u) * common)
    ) == 0
    assert sp.factor(t1 - r * (u + 1 / u) - (u - r) * (1 - u) / u) == 0


def elimination_checks() -> None:
    for p in (1.05, 1.5, 2.0, 3.0, 10.0, 50.0):
        for y in np.linspace(1.0e-5, 1.0 - 1.0e-5, 101):
            y_p = y**p
            common = 1.0 + 2.0 * y - y_p
            r = (1.0 - y_p) / common
            d = 2.0 / math.sqrt(common * (1.0 + y_p))
            e = y * d

            assert abs(2.0 * r * y - (1.0 - r) * (1.0 - y_p)) < 2.0e-12

            direct = (
                ((1.0 + r) ** p + (1.0 - r) ** p) ** (1.0 / p)
                / (d**p + e**p) ** (1.0 / p)
            )
            formula = (
                ((1.0 + y - y_p) ** p + y_p) ** (1.0 / p)
                * (1.0 + y_p) ** (0.5 - 1.0 / p)
                / math.sqrt(common)
            )
            assert abs(direct - formula) < 3.0e-12


def pareto_mapping_checks() -> None:
    rng = np.random.default_rng(20261014)
    for _ in range(10_000):
        r = float(rng.uniform(1.0e-5, 1.0 - 1.0e-5))
        u = float(rng.uniform(1.0e-5, 1.0 - 1.0e-5))
        tau = balanced_contact(r, u)

        if r * (3.0 - u) <= 1.0 + u:
            t_sq = (1.0 - u) / (1.0 + u - 2.0 * r)
            t = math.sqrt(t_sq)
            d = 1.0 / t + r * t
            e = (1.0 - r) * t
            assert t <= 1.0 / math.sqrt(r) * (1.0 + 2.0e-12)
        else:
            d = 2.0 * math.sqrt(r)
            e = tau - d
            assert e >= (1.0 - r) / math.sqrt(r) * (1.0 - 2.0e-12)

        assert abs(d + e - tau) < 2.0e-10
        assert abs((d - e) / (d + e) - u) < 2.0e-10


def destructive_search() -> None:
    rng = np.random.default_rng(27182818)
    smallest_gap = math.inf
    witness: tuple[float, float, float, float] | None = None

    for _ in range(100_000):
        r = float(rng.uniform(1.0e-7, 1.0 - 1.0e-7))
        # Every h,x in (0,1) with hx=r is represented by h in (r,1).
        log_h = rng.uniform(math.log(r), 0.0)
        h = math.exp(float(log_h))
        x = r / h
        u = float(rng.uniform(0.0, 1.0 - 1.0e-8))

        contact = first_gate_contact(h, x, u)
        balanced = balanced_contact(r, u)
        gap = contact - balanced
        if gap < smallest_gap:
            smallest_gap = gap
            witness = (h, x, u, gap)
        assert gap >= -2.0e-8, witness

        # Check the returned contact satisfies the piecewise gate, while a
        # slightly earlier point does not unless roundoff is at a branch seam.
        lhs = contact * contact * (1.0 - u * u) / 4.0
        rhs = psi(h, x, contact * max(h - x * u, 0.0))
        assert lhs + 2.0e-8 >= rhs
        earlier = contact * (1.0 - 1.0e-6)
        lhs_earlier = earlier * earlier * (1.0 - u * u) / 4.0
        rhs_earlier = psi(h, x, earlier * max(h - x * u, 0.0))
        assert lhs_earlier <= rhs_earlier + 2.0e-7

    assert witness is not None
    print(
        "smallest random balanced-frontier gap: "
        f"{smallest_gap:.3e} at h={witness[0]:.8f}, "
        f"x={witness[1]:.8f}, u={witness[2]:.8f}"
    )


def elimination_minimization_checks() -> None:
    rng = np.random.default_rng(31415926)
    for _ in range(10_000):
        h = float(rng.uniform(1.0e-5, 1.0 - 1.0e-5))
        x = float(rng.uniform(1.0e-5, 1.0 - 1.0e-5))
        q = float(rng.uniform(0.0, 8.0))
        assert abs(minimized_l_expression(h, x, q) - psi(h, x, q)) < 2.0e-12


def main() -> None:
    symbolic_checks()
    elimination_minimization_checks()
    pareto_mapping_checks()
    elimination_checks()
    destructive_search()
    print("PASS: finite-p global gate symbolic identities and destructive search")


if __name__ == "__main__":
    main()
