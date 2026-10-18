#!/usr/bin/env python3
"""Exact and numerical controls for the rank-one MI-14 B0 factor.

For a Frobenius-normalized rank-one matrix X, the five paired roots of T_X
are 2-|tr X|^2, 1, 1, 0, 0.  Hence the pair-sum constant gate is

    B0 = product_{i<j} (3-mu_i-mu_j)
       = 48*tau^2*(1+tau)^2,

where tau=|tr X|^2.  The symbolic identity is the proof; random matrix checks
and exact zero/positive controls guard the implementation and normalization.
"""

from __future__ import annotations

import json

import numpy as np
import sympy as sp


def symbolic_identity() -> sp.Expr:
    tau = sp.symbols("tau", nonnegative=True)
    roots = (2 - tau, 1, 1, 0, 0)
    product = sp.prod(
        3 - roots[first] - roots[second]
        for first in range(5)
        for second in range(first + 1, 5)
    )
    return sp.factor(product - 48 * tau**2 * (1 + tau) ** 2)


def spectral_b0(matrix: np.ndarray) -> tuple[float, float]:
    size = matrix.shape[0]
    commutator = np.kron(np.eye(size), matrix) - np.kron(matrix.T, np.eye(size))
    eigenvalues = np.linalg.eigvalsh(commutator.conj().T @ commutator)
    positive = np.sort(eigenvalues[eigenvalues > 1e-9])[::-1]
    if len(positive) != 6:
        raise RuntimeError(f"expected six positive eigenvalues, got {len(positive)}")
    paired = positive.reshape(3, 2).mean(axis=1)
    roots = np.concatenate((paired, np.zeros(2)))
    b0 = np.prod(
        [
            3.0 - roots[first] - roots[second]
            for first in range(5)
            for second in range(first + 1, 5)
        ]
    )
    tau = abs(np.trace(matrix)) ** 2
    expected = 48.0 * tau**2 * (1.0 + tau) ** 2
    return float(b0), float(expected)


def normalized_rank_one(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    left = left / np.linalg.norm(left)
    right = right / np.linalg.norm(right)
    return np.outer(left, right.conj())


def main() -> None:
    identity_remainder = symbolic_identity()
    rng = np.random.default_rng(12829)
    maximum_error = 0.0
    for _ in range(32):
        left = rng.normal(size=4) + 1j * rng.normal(size=4)
        right = rng.normal(size=4) + 1j * rng.normal(size=4)
        b0, expected = spectral_b0(normalized_rank_one(left, right))
        maximum_error = max(maximum_error, abs(b0 - expected))

    zero_matrix = np.zeros((4, 4), dtype=complex)
    zero_matrix[0, 1] = 1.0
    zero_b0, zero_expected = spectral_b0(zero_matrix)

    positive_matrix = np.zeros((4, 4), dtype=complex)
    positive_matrix[0, 0] = 1.0
    positive_b0, positive_expected = spectral_b0(positive_matrix)

    passed = (
        identity_remainder == 0
        and maximum_error <= 2e-9
        and abs(zero_b0) <= 2e-9
        and abs(zero_expected) <= 2e-9
        and abs(positive_b0 - 192.0) <= 2e-9
        and abs(positive_expected - 192.0) <= 2e-9
    )
    print(
        json.dumps(
            {
                "result": "PASS" if passed else "FAIL",
                "symbolic_remainder": str(identity_remainder),
                "formula": "B0=48*tau^2*(1+tau)^2, tau=|tr(X)|^2",
                "random_rank_one_max_error": maximum_error,
                "trace_zero_control": {
                    "B0": zero_b0,
                    "expected": zero_expected,
                },
                "trace_one_control": {
                    "B0": positive_b0,
                    "expected": positive_expected,
                },
                "proof_boundary": (
                    "The symbolic paired-root product proves the factorization "
                    "once the rank-one spectrum is supplied by S8. Numerical "
                    "checks only guard normalization and implementation."
                ),
            },
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
