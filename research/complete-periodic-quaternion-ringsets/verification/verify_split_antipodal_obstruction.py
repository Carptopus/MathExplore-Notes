"""Finite calibration for the split-prime antipodal-fibre obstruction.

This checks valuation and 2x2 matrix identities for sample split primes.  It
does not replace the general proof in Lemma 5.2.
"""

from __future__ import annotations

import json
from math import factorial
from pathlib import Path


def vp(value: int, prime: int) -> int:
    if value == 0:
        return 10**9
    value = abs(value)
    total = 0
    while value % prime == 0:
        value //= prime
        total += 1
    return total


def matmul(a: tuple[int, ...], b: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    return (
        (a[0] * b[0] + a[1] * b[2]) % modulus,
        (a[0] * b[1] + a[1] * b[3]) % modulus,
        (a[2] * b[0] + a[3] * b[2]) % modulus,
        (a[2] * b[1] + a[3] * b[3]) % modulus,
    )


def product_at(t: int, modulus_class: int) -> int:
    value = 1
    for r in range(1, modulus_class):
        value *= t - r
    return value


def check_case(prime: int, nu: int) -> dict[str, int | bool]:
    m = prime**nu
    v = vp(factorial(m - 1), prime)
    k = v + 1
    modulus = prime**k

    # In an eigenbasis: E=E11, A=E22, B=E21, hence ABE=E21.
    e = (1, 0, 0, 0)
    a = (0, 0, 0, 1)
    b = (0, 0, 1, 0)
    abe = matmul(matmul(a, b, modulus), e, modulus)

    base_v = vp(product_at(0, m), prime)
    minimum_off_gain = 10**9
    for residue in range(1, m):
        # Three lifts exercise the class-wise valuation statement.
        for lift in (-2, -1, 0, 1, 2):
            value = product_at(residue + lift * m, m)
            minimum_off_gain = min(minimum_off_gain, vp(value, prime) - v)

    return {
        "prime": prime,
        "nu": nu,
        "M": m,
        "V": v,
        "K": k,
        "K_ge_nu": k >= nu,
        "base_valuation_exact": base_v == v,
        "minimum_off_gain": minimum_off_gain,
        "off_vanishes_mod_pK": minimum_off_gain >= 1,
        "ABE_nonzero_mod_p": any(entry % prime for entry in abe),
        "witness_survives": any((pow(prime, v, modulus) * entry) % modulus for entry in abe),
    }


def main() -> None:
    cases = [check_case(p, nu) for p in (5, 13, 17) for nu in (1, 2)]
    assert all(case["K_ge_nu"] for case in cases)
    assert all(case["base_valuation_exact"] for case in cases)
    assert all(case["off_vanishes_mod_pK"] for case in cases)
    assert all(case["ABE_nonzero_mod_p"] for case in cases)
    assert all(case["witness_survives"] for case in cases)

    payload = {"status": "PASS", "scope": "finite calibration only", "cases": cases}
    output = Path(__file__).with_name("results") / "split-antipodal-obstruction.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
