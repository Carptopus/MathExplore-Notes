from __future__ import annotations

import sympy as sp


def main() -> None:
    n, k, p = sp.symbols("n k p", positive=True)

    def a(j):
        return (n + p * j - 1) / (n + p * j)

    def b(j):
        return j / (n + p * j)

    denominator = (k * p + n) ** 2 * (k * p + n - p) * (k * p + n + p)
    expected = {
        "a": p**2 * (2 * k * p + 2 * n - 1) / denominator,
        "b": n * (2 * k * p + n) / denominator,
        "mixed": 2 * p * (k * n * p + k * p + n**2) / denominator,
    }
    actual = {
        "a": a(k) ** 2 - a(k - 1) * a(k + 1),
        "b": b(k) ** 2 - b(k - 1) * b(k + 1),
        "mixed": 2 * a(k) * b(k) - a(k - 1) * b(k + 1) - a(k + 1) * b(k - 1),
    }
    for name in actual:
        assert sp.factor(actual[name] - expected[name]) == 0
    print("PASS: universal normalized Sagan coefficient identities")


if __name__ == "__main__":
    main()
