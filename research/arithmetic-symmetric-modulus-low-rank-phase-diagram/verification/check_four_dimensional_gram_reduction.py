"""Guard the exact four-dimensional Gram reduction in MATH-DIR-0114/S1."""

from __future__ import annotations

import numpy as np


TOL = 2e-7


def psd_sqrt(a: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh((a + a.conj().T) / 2)
    if vals.min() < -1e-11:
        raise AssertionError(f"matrix is not PSD: {vals.min()}")
    return (vecs * np.sqrt(np.maximum(vals, 0.0))) @ vecs.conj().T


def positive_matrix(rng: np.random.Generator, size: int) -> np.ndarray:
    z = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    return z @ z.conj().T + 0.35 * np.eye(size)


def schatten(a: np.ndarray, p: float) -> float:
    vals = np.linalg.eigvalsh((a + a.conj().T) / 2)
    vals = np.maximum(vals, 0.0)
    return float(np.sum(vals**p) ** (1.0 / p))


def assert_same_nonzero_spectrum(a: np.ndarray, b: np.ndarray) -> None:
    ea = np.linalg.eigvalsh((a + a.conj().T) / 2)
    eb = np.linalg.eigvalsh((b + b.conj().T) / 2)
    ea = np.sort(ea[ea > 1e-11])
    eb = np.sort(eb[eb > 1e-11])
    if ea.shape != eb.shape or np.max(np.abs(ea - eb), initial=0.0) > TOL:
        raise AssertionError((ea, eb))


def random_contraction(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    op = np.linalg.svd(z, compute_uv=False)[0]
    return z / (1.15 * op)


def check_random_reduction() -> None:
    rng = np.random.default_rng(20261015)
    for _ in range(240):
        sigma = positive_matrix(rng, 2)
        # Sigma is a positive singular-value matrix; diagonalizing it loses no generality.
        sigma = np.diag(np.linalg.eigvalsh(sigma))
        h = positive_matrix(rng, 2)
        k = random_contraction(rng)

        u = np.vstack((np.eye(2), np.zeros((2, 2))))
        defect = np.eye(2) - k.conj().T @ k
        v = np.vstack((k, psd_sqrt(defect)))
        if np.linalg.norm(u.conj().T @ v - k) > TOL:
            raise AssertionError("cross Gram realization failed")
        if np.linalg.norm(v.conj().T @ v - np.eye(2)) > TOL:
            raise AssertionError("V is not an isometry")

        sigma_half = psd_sqrt(sigma)
        c = sigma_half @ h @ sigma_half
        c_inv = np.linalg.inv(c)
        t = u @ sigma @ v.conj().T
        s_t = (psd_sqrt(t.conj().T @ t) + psd_sqrt(t @ t.conj().T)) / 2
        d_c = (u @ c @ u.conj().T + v @ sigma @ c_inv @ sigma @ v.conj().T) / 2

        l = sigma_half @ k @ sigma_half
        g = np.block([[sigma, l], [l.conj().T, sigma]]) / 2
        w = np.block(
            [[h, np.zeros((2, 2))], [np.zeros((2, 2)), np.linalg.inv(h)]]
        )
        w_half = psd_sqrt(w)
        weighted = w_half @ g @ w_half

        assert_same_nonzero_spectrum(s_t, g)
        assert_same_nonzero_spectrum(d_c, weighted)
        for p in (1.0, 1.2, 1.5, 2.0, 3.0, 8.0):
            if abs(schatten(s_t, p) - schatten(g, p)) > 3e-7:
                raise AssertionError("numerator norm reduction failed")
            if abs(schatten(d_c, p) - schatten(weighted, p)) > 3e-7:
                raise AssertionError("denominator norm reduction failed")

        extra = positive_matrix(rng, 4) / 20
        for p in (1.0, 1.5, 2.0, 4.0):
            if schatten(d_c + extra, p) + 1e-10 < schatten(d_c, p):
                raise AssertionError("positive-order Schatten monotonicity failed")


def check_nilpotent_equality() -> None:
    q = 1.37
    sigma = q * np.eye(2)
    k = np.array([[0.0, 0.0], [1.0, 0.0]])
    sigma_half = np.sqrt(q) * np.eye(2)
    l = sigma_half @ k @ sigma_half
    g = np.block([[sigma, l], [l.T, sigma]]) / 2
    expected_g = np.array([0.0, q / 2, q / 2, q])
    if np.max(np.abs(np.linalg.eigvalsh(g) - expected_g)) > TOL:
        raise AssertionError("nilpotent numerator spectrum mismatch")

    for p in (1.05, 1.2, 1.5, 2.0, 3.0, 8.0, 20.0):
        a = 2 ** ((p - 1) / (2 * p))
        h = np.diag([a, 1 / a])
        w = np.block(
            [[h, np.zeros((2, 2))], [np.zeros((2, 2)), np.linalg.inv(h)]]
        )
        weighted = psd_sqrt(w) @ g @ psd_sqrt(w)
        expected_d = np.array([0.0, q * a / 2, q * a / 2, q / a])
        if np.max(np.abs(np.linalg.eigvalsh(weighted) - expected_d)) > 2e-10:
            raise AssertionError("nilpotent denominator spectrum mismatch")
        ratio = schatten(g, p) / schatten(weighted, p)
        lower = ((2**p + 2) / (2 ** (p / 2 + 1.5))) ** (1 / p)
        if abs(ratio - lower) > 2e-10:
            raise AssertionError((p, ratio, lower))


if __name__ == "__main__":
    check_random_reduction()
    check_nilpotent_equality()
    print("VERIFIED: exact four-dimensional Gram reduction and nilpotent equality")
