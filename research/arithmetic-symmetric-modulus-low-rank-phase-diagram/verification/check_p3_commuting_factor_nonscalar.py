"""Formula guards for MATH-DIR-0114/S10."""

from __future__ import annotations

import numpy as np


TOL = 5.0e-9


def random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    unitary, triangular = np.linalg.qr(raw)
    phases = np.diag(triangular)
    return unitary @ np.diag(np.exp(-1j * np.angle(phases)))


def random_contraction(rng: np.random.Generator) -> np.ndarray:
    return (
        random_unitary(rng)
        @ np.diag(rng.random(2))
        @ random_unitary(rng).conj().T
    )


def trace_formulas(
    sigma: np.ndarray, c: np.ndarray, k: np.ndarray
) -> tuple[float, float]:
    q = sigma**2 / c
    x = np.abs(k) ** 2
    numerator = 2.0 * float(np.sum(sigma**3))
    denominator = float(np.sum(c**3 + q**3))
    for i in range(2):
        for j in range(2):
            numerator += (
                3.0 * sigma[i] * sigma[j] * (sigma[i] + sigma[j]) * x[i, j]
            )
            denominator += 3.0 * (
                c[i] ** 2 * q[j] + c[i] * q[j] ** 2
            ) * x[i, j]
    return numerator, denominator


def direct_traces(
    sigma: np.ndarray, c: np.ndarray, k: np.ndarray
) -> tuple[float, float]:
    s = np.diag(sigma).astype(complex)
    c_matrix = np.diag(c).astype(complex)
    q_matrix = s @ np.linalg.inv(c_matrix) @ s
    u = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0], [0.0, 0.0]])
    defect = np.linalg.eigh(np.eye(2) - k.conj().T @ k)
    root = (defect[1] * np.sqrt(np.maximum(defect[0], 0.0))) @ defect[1].conj().T
    v = np.vstack([k, root])
    numerator_matrix = u @ s @ u.conj().T + v @ s @ v.conj().T
    denominator_matrix = u @ c_matrix @ u.conj().T + v @ q_matrix @ v.conj().T
    return float(np.trace(np.linalg.matrix_power(numerator_matrix, 3)).real), float(
        np.trace(np.linalg.matrix_power(denominator_matrix, 3)).real
    )


def check_random_commuting_data() -> None:
    rng = np.random.default_rng(20261015)
    for _ in range(4000):
        sigma = np.exp(rng.uniform(-2.5, 2.5, size=2))
        c = np.exp(rng.uniform(-2.5, 2.5, size=2))
        k = random_contraction(rng)
        expected = trace_formulas(sigma, c, k)
        actual = direct_traces(sigma, c, k)
        if max(abs(expected[i] - actual[i]) for i in range(2)) > 3.0e-5:
            raise AssertionError("non-scalar cubic trace expansion failed")
        if actual[1] + TOL < 0.8 * actual[0]:
            raise AssertionError("commuting-factor p=3 inequality failed")


def check_matching_vertices() -> None:
    vertices = [np.zeros((2, 2), dtype=complex)]
    for i in range(2):
        for j in range(2):
            vertex = np.zeros((2, 2), dtype=complex)
            vertex[i, j] = 1.0
            vertices.append(vertex)
    vertices.extend(
        [np.eye(2), np.array([[0.0, 1.0], [1.0, 0.0]])]
    )
    for ratio in np.geomspace(0.03, 30.0, 31):
        sigma = np.array([1.0, ratio])
        for first in np.geomspace(0.05, 20.0, 25):
            for second in np.geomspace(0.05, 20.0, 25):
                c = np.array([first, second])
                for vertex in vertices:
                    numerator, denominator = trace_formulas(sigma, c, vertex)
                    if denominator + TOL < 0.8 * numerator:
                        raise AssertionError("non-scalar matching vertex failed")


def check_weighted_chain_identity() -> None:
    for ratio in np.geomspace(0.03, 30.0, 81):
        numerator = 2.0 * (1.0 + ratio**3) + 3.0 * ratio * (1.0 + ratio)
        chain_numerator = (1.0 + ratio) ** 3 + 1.0 + ratio**3
        if abs(numerator - chain_numerator) > TOL:
            raise AssertionError("weighted-chain numerator identity failed")


def destructive_control() -> None:
    sigma = np.array([1.0, 1.0])
    c = np.array([2.0 ** (-1.0 / 3.0), 2.0 ** (1.0 / 3.0)])
    k = np.array([[0.0, 1.0], [0.0, 0.0]])
    numerator, denominator = trace_formulas(sigma, c, k)
    if denominator >= 0.81 * numerator:
        raise AssertionError("destructive control did not reject the wrong constant")


def main() -> None:
    check_random_commuting_data()
    check_matching_vertices()
    check_weighted_chain_identity()
    destructive_control()
    print("MATH-DIR-0114 S10 p=3 commuting-factor guards: VERIFIED")


if __name__ == "__main__":
    main()
