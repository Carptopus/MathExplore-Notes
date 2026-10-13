"""Check the exact TR-16 reduction and calibrate its low-dimensional integral.

The numerical quadrature below is deliberately labelled calibration only.  It has no
directed-rounding or rigorous tail certificate and therefore is not a proof of I_2 <= 2 I_1.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp
from scipy.special import dawsn, erf, erfc, erfcx, gamma, roots_genlaguerre
from numpy.polynomial.legendre import leggauss


def check_exact_matrix_identity() -> None:
    a0, b0 = sp.symbols("a0 b0", real=True)
    a1, b1, y1, z1 = sp.symbols("a1 b1 y1 z1", real=True)
    a2, b2, y2, z2 = sp.symbols("a2 b2 y2 z2", real=True)
    eye = sp.eye(2)
    swap = sp.Matrix([[0, 1], [1, 0]])

    def outer(a: sp.Expr, b: sp.Expr) -> sp.Matrix:
        v = sp.Matrix([a, b])
        return v * v.T

    p = outer(a0, b0)
    k1 = outer(a1, b1) - y1**2 * eye + y1 * z1 * swap
    k2 = outer(a2, b2) - y2**2 * eye + y2 * z2 * swap

    direct_r2 = (
        outer(a0, b0)
        + outer(a1, b1)
        + outer(a2, b2)
        - (y1**2 + y2**2) * eye
        + (y1 * z1 + y2 * z2) * swap
    )
    assert sp.simplify(direct_r2 - (p + k1 + k2)) == sp.zeros(2)


def mean_abs_u_minus_chi_square(u: float, degrees: int) -> float:
    if degrees == 2:
        return u - 2.0 + 4.0 * math.exp(-u / 2.0)
    if degrees != 1:
        raise ValueError(degrees)
    root = math.sqrt(u)
    cdf = erf(math.sqrt(u / 2.0))
    phi = math.exp(-u / 2.0) / math.sqrt(2.0 * math.pi)
    return 1.0 - u + 2.0 * (u - 1.0) * cdf + 4.0 * root * phi


def integrated_q_t_kernel(u: float, p: np.ndarray, sine: float, q_degrees: int) -> np.ndarray:
    """E_{Q,T}|(u-p)(u-Q)-T(u-sine*sqrt(u*p))|.

    Here T~chi-square(2), while Q has one or two degrees of freedom.  The formula
    follows by integrating the absolute affine function of T and then the truncated
    Laplace transform of Q on either side of u.
    """

    d = u - p
    c = u - sine * np.sqrt(u * p)
    abs_d = np.abs(d)
    abs_c = np.abs(c)
    lam = np.divide(
        abs_d,
        2.0 * abs_c,
        out=np.full_like(p, np.inf, dtype=float),
        where=abs_c > 1.0e-14,
    )

    if q_degrees == 2:
        exp_u = math.exp(-u / 2.0)
        prob_lower = 1.0 - exp_u
        prob_upper = exp_u
        laplace_upper = exp_u / (1.0 + 2.0 * lam)
        denominator = 1.0 - 2.0 * lam
        near = np.abs(denominator) < 1.0e-7
        laplace_lower = np.empty_like(lam)
        laplace_lower[near] = (u / 2.0) * exp_u
        laplace_lower[~near] = (
            np.exp(-lam[~near] * u) - exp_u
        ) / denominator[~near]
    elif q_degrees == 1:
        prob_lower = erf(math.sqrt(u / 2.0))
        prob_upper = erfc(math.sqrt(u / 2.0))
        laplace_upper = (
            math.exp(-u / 2.0)
            * erfcx(np.sqrt((0.5 + lam) * u))
            / np.sqrt(1.0 + 2.0 * lam)
        )
        laplace_lower = np.empty_like(lam)
        below = lam < 0.5 - 1.0e-8
        above = lam > 0.5 + 1.0e-8
        middle = ~(below | above)
        laplace_lower[below] = (
            np.exp(-lam[below] * u)
            * erf(np.sqrt((0.5 - lam[below]) * u))
            / np.sqrt(1.0 - 2.0 * lam[below])
        )
        laplace_lower[middle] = math.sqrt(2.0 * u / math.pi) * math.exp(-u / 2.0)
        shifted = lam[above] - 0.5
        laplace_lower[above] = (
            2.0
            / math.sqrt(math.pi)
            * math.exp(-u / 2.0)
            * dawsn(np.sqrt(shifted * u))
            / np.sqrt(2.0 * lam[above] - 1.0)
        )
    else:
        raise ValueError(q_degrees)

    # A=d(u-Q), and A-cT crosses zero on Q<u exactly when d*c>0.
    crossing_lower = d * c > 0.0
    crossing_probability = np.where(crossing_lower, prob_lower, prob_upper)
    crossing_laplace = np.where(crossing_lower, laplace_lower, laplace_upper)
    kernel = (
        abs_d * mean_abs_u_minus_chi_square(u, q_degrees)
        + 2.0 * abs_c * (1.0 - 2.0 * crossing_probability)
        + 4.0 * abs_c * crossing_laplace
    )
    return np.where(
        abs_c < 1.0e-14,
        abs_d * mean_abs_u_minus_chi_square(u, q_degrees),
        kernel,
    )


def integrate_fixed_sine(order: int, sine: float, r: int) -> float:
    u_shape = r / 2.0
    p_shape = (r + 1) / 2.0
    q_degrees = r
    if r not in (1, 2):
        raise ValueError("This calibration implements only r=1,2.")

    u_nodes, u_weights = roots_genlaguerre(order, u_shape - 1.0)
    p_nodes, p_weights = roots_genlaguerre(order, p_shape - 1.0)
    u_nodes = 2.0 * u_nodes
    p_nodes = 2.0 * p_nodes
    u_weights = u_weights / gamma(u_shape)
    p_weights = p_weights / gamma(p_shape)

    total = 0.0
    for u, weight in zip(u_nodes, u_weights, strict=True):
        values = integrated_q_t_kernel(float(u), p_nodes, sine, q_degrees)
        total += float(weight) * float(np.dot(p_weights, values))
    return total


def integrate_i_r(order: int, angular_order: int, r: int) -> float:
    nodes, weights = leggauss(angular_order)
    # theta=pi(x+1), and dtheta/(2pi)=dx/2.
    total = 0.0
    for node, weight in zip(nodes, weights, strict=True):
        sine = math.sin(math.pi * (float(node) + 1.0))
        total += float(weight) * 0.5 * integrate_fixed_sine(order, sine, r)
    return total


def main() -> None:
    check_exact_matrix_identity()
    i1 = integrate_i_r(order=80, angular_order=96, r=1)
    i2 = integrate_i_r(order=80, angular_order=96, r=2)
    a223 = math.pi * i1 / 2.0
    a224 = math.pi * i2 / 4.0
    margin = 2.0 * i1 - i2

    assert 3.54 < i1 < 3.59
    assert 7.02 < i2 < 7.12
    assert margin > 0.03
    assert 5.55 < a223 < 5.66
    assert 5.50 < a224 < 5.61

    print("PASS: exact chi-field/random-walk matrix reduction")
    print(f"CALIBRATION ONLY: I1={i1:.12f}, I2={i2:.12f}, 2*I1-I2={margin:.12f}")
    print(f"CALIBRATION ONLY: a(2,2,3)={a223:.9f}, a(2,2,4)={a224:.9f}")
    print("NOT A PROOF: quadrature has no directed-rounding or rigorous tail certificate")


if __name__ == "__main__":
    main()
