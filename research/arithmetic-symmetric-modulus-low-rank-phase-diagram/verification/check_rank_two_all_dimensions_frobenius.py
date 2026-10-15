"""Regression checks for the dimension-free rank-at-most-two theorem in S36."""

from __future__ import annotations

import math

import numpy as np


ALPHA = 3.0 * math.sqrt(2.0) / 4.0
CONSTANT = math.sqrt(ALPHA)


def random_isometry(rng: np.random.Generator, rows: int) -> np.ndarray:
    raw = rng.normal(size=(rows, 2)) + 1j * rng.normal(size=(rows, 2))
    q, _ = np.linalg.qr(raw)
    return q[:, :2]


def random_positive(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    return raw @ raw.conj().T + 0.4 * np.eye(2)


def symmetric_modulus(matrix: np.ndarray) -> np.ndarray:
    left_values, left_vectors = np.linalg.eigh(matrix @ matrix.conj().T)
    right_values, right_vectors = np.linalg.eigh(matrix.conj().T @ matrix)
    left = (left_vectors * np.sqrt(np.maximum(left_values, 0.0))) @ left_vectors.conj().T
    right = (right_vectors * np.sqrt(np.maximum(right_values, 0.0))) @ right_vectors.conj().T
    return (left + right) / 2.0


rng = np.random.default_rng(20261015)
largest_ratio = 0.0
largest_reduction_error = 0.0
for dimension in range(3, 10):
    for _ in range(1200):
        u = random_isometry(rng, dimension)
        v = random_isometry(rng, dimension)
        singular = np.diag(np.exp(rng.uniform(-1.5, 1.5, size=2)))
        c = random_positive(rng)
        inverse_c = np.linalg.inv(c)
        t = u @ singular @ v.conj().T
        p = u @ c @ u.conj().T
        q = v @ singular @ inverse_c @ singular @ v.conj().T
        denominator = (p + q) / 2.0
        ratio = np.linalg.norm(symmetric_modulus(t), "fro") / np.linalg.norm(denominator, "fro")
        largest_ratio = max(largest_ratio, ratio)
        if ratio > CONSTANT + 4e-10:
            raise AssertionError("dimension-free rank-two bound failed")

        k = u.conj().T @ v
        a = float(np.trace(singular @ singular).real)
        z = float(np.trace(singular @ k @ singular @ k.conj().T).real)
        first = float(np.trace(c @ c).real)
        d = singular @ inverse_c @ singular
        second = float(np.trace(d @ d).real)
        cross = float(np.trace(c @ k @ d @ k.conj().T).real)
        reduced_numerator = math.sqrt((a + z) / 2.0)
        reduced_denominator = math.sqrt((first + second + 2.0 * cross) / 4.0)
        reduction_error = abs(ratio - reduced_numerator / reduced_denominator)
        largest_reduction_error = max(largest_reduction_error, reduction_error)
        if reduction_error > 2e-7:
            raise AssertionError("ambient-to-contraction reduction failed")

# Exact S1 equality family at r=sqrt(2)-1, reconstructed from its Gram matrix.
parameter = math.sqrt(2.0) - 1.0
b = 1.0 - 2.0 * parameter
gram = np.array(
    [
        [1.0, parameter, -b, -parameter],
        [parameter, 1.0, parameter, b],
        [-b, parameter, 1.0, -parameter],
        [-parameter, b, -parameter, 1.0],
    ]
)
values, vectors = np.linalg.eigh(gram)
coordinates = (vectors[:, values > 1e-10] * np.sqrt(values[values > 1e-10])).T
u1, v1, u2, v2 = (coordinates[:, index] for index in range(4))
a1 = np.outer(u1, v1)
a2 = np.outer(u2, v2)
numerator = np.linalg.norm(symmetric_modulus(a1 + a2), "fro")
denominator = np.linalg.norm(symmetric_modulus(a1) + symmetric_modulus(a2), "fro")
equality_ratio = numerator / denominator
if abs(equality_ratio - CONSTANT) > 5e-8:
    raise AssertionError("three-dimensional equality control failed")
if equality_ratio <= CONSTANT - 1e-5:
    raise AssertionError("lowered-constant destructive control failed")

print("PASS: dimension-free rank-at-most-two Frobenius theorem")
print(f"largest random ratio = {largest_ratio:.12f}")
print(f"largest ambient reduction error = {largest_reduction_error:.3e}")
print(f"sharp equality ratio = {equality_ratio:.12f}")
