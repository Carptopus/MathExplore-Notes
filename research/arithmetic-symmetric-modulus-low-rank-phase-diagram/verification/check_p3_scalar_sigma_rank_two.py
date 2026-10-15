"""Formula guards for MATH-DIR-0114/S9."""

from __future__ import annotations

import numpy as np


TOL = 4.0e-9


def random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    unitary, triangular = np.linalg.qr(raw)
    phases = np.diag(triangular)
    return unitary @ np.diag(np.exp(-1j * np.angle(phases)))


def random_contraction(rng: np.random.Generator) -> np.ndarray:
    left = random_unitary(rng)
    right = random_unitary(rng)
    singular = rng.random(2)
    return left @ np.diag(singular) @ right.conj().T


def formulas(h: np.ndarray, k: np.ndarray) -> tuple[float, float]:
    x = np.abs(k) ** 2
    numerator = 4.0 + 6.0 * float(x.sum())
    base = float(np.sum(h**3 + h**-3))
    coefficients = np.empty((2, 2), dtype=float)
    for i in range(2):
        for j in range(2):
            coefficients[i, j] = 3.0 * (
                h[i] ** 2 / h[j] + h[i] / h[j] ** 2
            )
    denominator = base + float(np.sum(coefficients * x))
    return numerator, denominator


def direct_traces(h: np.ndarray, k: np.ndarray) -> tuple[float, float]:
    identity = np.eye(2, dtype=complex)
    b = np.block([[identity, k], [k.conj().T, identity]])
    weight = np.diag(np.r_[h, 1.0 / h]).astype(complex)
    return float(np.trace(np.linalg.matrix_power(b, 3)).real), float(
        np.trace(np.linalg.matrix_power(b @ weight, 3)).real
    )


def check_trace_expansion_and_random_inequality() -> None:
    rng = np.random.default_rng(20261015)
    for _ in range(4000):
        h = np.exp(rng.uniform(-2.5, 2.5, size=2))
        k = random_contraction(rng)
        expected = formulas(h, k)
        actual = direct_traces(h, k)
        if max(abs(expected[i] - actual[i]) for i in range(2)) > 2.0e-6:
            raise AssertionError("cubic trace expansion failed")
        if actual[1] + TOL < 0.8 * actual[0]:
            raise AssertionError("p=3 scalar-Sigma inequality failed")


def check_matching_vertices() -> None:
    vertices = [np.zeros((2, 2), dtype=complex)]
    for i in range(2):
        for j in range(2):
            vertex = np.zeros((2, 2), dtype=complex)
            vertex[i, j] = 1.0
            vertices.append(vertex)
    vertices.extend(
        [
            np.eye(2, dtype=complex),
            np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex),
        ]
    )
    for t in np.linspace(-4.0, 4.0, 81):
        for u in np.linspace(-4.0, 4.0, 81):
            h = np.exp(np.array([t, u]))
            for vertex in vertices:
                numerator, denominator = formulas(h, vertex)
                if denominator + TOL < 0.8 * numerator:
                    raise AssertionError("matching-vertex inequality failed")


def check_nilpotent_equality() -> None:
    h = np.array([2.0 ** (-1.0 / 3.0), 2.0 ** (1.0 / 3.0)])
    k = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    numerator, denominator = formulas(h, k)
    if abs(numerator - 10.0) > TOL or abs(denominator - 8.0) > TOL:
        raise AssertionError("nilpotent equality failed")


def destructive_control() -> None:
    h = np.array([2.0 ** (-1.0 / 3.0), 2.0 ** (1.0 / 3.0)])
    k = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    numerator, denominator = formulas(h, k)
    if denominator >= 0.81 * numerator:
        raise AssertionError("destructive control did not reject the wrong constant")


def main() -> None:
    check_trace_expansion_and_random_inequality()
    check_matching_vertices()
    check_nilpotent_equality()
    destructive_control()
    print("MATH-DIR-0114 S9 p=3 scalar-Sigma rank-two guards: VERIFIED")


if __name__ == "__main__":
    main()
