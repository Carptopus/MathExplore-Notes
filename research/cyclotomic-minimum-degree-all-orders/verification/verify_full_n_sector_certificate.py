"""Destructively test the all-orders sector-certificate proof.

The theorem is symbolic.  This script performs bounded high-precision and
exact-algebra checks across all parameter categories, together with two
deliberate negative controls.  Finite checks are not used to justify the
all-orders quantifier.
"""

from __future__ import annotations

import json
import math
from collections import Counter

import mpmath as mp
import sympy as sp


MAX_SIGN_N = 1000
MAX_ALL_ANCHOR_N = 300
MAX_ALGEBRA_N = 180
PRECISION = 90


def smallest_prime_factor(n: int) -> int:
    for candidate in range(2, math.isqrt(n) + 1):
        if n % candidate == 0:
            return candidate
    return n


def category(n: int) -> str:
    factors = sp.factorint(n)
    if len(factors) == 1 and next(iter(factors.values())) == 1:
        return "prime"
    if len(factors) == 1:
        return "prime_power"
    if any(exponent > 1 for exponent in factors.values()):
        return "mixed_nonsquarefree"
    return "mixed_squarefree"


def kernel(p: int, theta: mp.mpf) -> mp.mpf:
    alpha = mp.pi / p
    return mp.fsum(
        mp.sin(k * alpha) * mp.cos(k * theta) for k in range(1, p)
    )


def kernel_closed(p: int, theta: mp.mpf) -> mp.mpf:
    alpha = mp.pi / p
    return (
        mp.sin(alpha)
        * (1 + mp.cos(p * theta))
        / (2 * (mp.cos(theta) - mp.cos(alpha)))
    )


def verify_signs_and_arithmetic(n: int) -> dict[str, object]:
    p = smallest_prime_factor(n)
    P = n // p
    d = (p - 1) * P
    alpha = mp.pi / p
    tolerance = mp.mpf("1e-65")
    anchors = {h * P for h in range(p)}

    if any(math.gcd(k, n) != 1 for k in range(1, p)):
        raise AssertionError(("nonprimitive low frequency", n, p))

    if n <= MAX_ALL_ANCHOR_N:
        checked_anchors = sorted(anchors)
        all_anchors_checked = True
    else:
        checked_anchors = sorted({0, min(1, p - 1) * P, (p - 1) * P})
        all_anchors_checked = False

    maximum_anchor = mp.mpf(0)
    for j in checked_anchors:
        value = kernel(p, 2 * mp.pi * j / n + alpha)
        maximum_anchor = max(maximum_anchor, abs(value))
    if maximum_anchor >= tolerance:
        raise AssertionError(("anchor mismatch", n, maximum_anchor))

    maximum_prefix: mp.mpf | None = None
    minimum_tail: mp.mpf | None = None
    for j in range(n):
        if j in anchors:
            continue
        value = kernel_closed(p, 2 * mp.pi * j / n + alpha)
        if j < d:
            maximum_prefix = value if maximum_prefix is None else max(maximum_prefix, value)
        elif j > d:
            minimum_tail = value if minimum_tail is None else min(minimum_tail, value)

    if maximum_prefix is not None and maximum_prefix >= 0:
        raise AssertionError(("prefix sign", n, maximum_prefix))
    if minimum_tail is not None and minimum_tail <= 0:
        raise AssertionError(("tail sign", n, minimum_tail))

    unit_images = {a % p for a in range(1, n) if math.gcd(a, n) == 1}
    if unit_images != set(range(1, p)):
        raise AssertionError(("unit reduction not surjective", n, unit_images))

    return {
        "n": n,
        "p": p,
        "category": category(n),
        "anchor_checks": len(checked_anchors),
        "all_anchors_checked": all_anchors_checked,
        "maximum_anchor_error": mp.nstr(maximum_anchor, 8),
        "maximum_prefix": None if maximum_prefix is None else mp.nstr(maximum_prefix, 8),
        "minimum_tail": None if minimum_tail is None else mp.nstr(minimum_tail, 8),
    }


def verify_algebra(n: int) -> dict[str, object]:
    p = smallest_prime_factor(n)
    P = n // p
    x = sp.symbols("x")
    phi = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    regular = sp.Poly(sum(x ** (h * P) for h in range(p)), x, domain=sp.ZZ)
    if sp.rem(regular, phi).as_expr() != 0:
        raise AssertionError(("regular polygon not divisible", n))

    coeffs = list(reversed(phi.all_coeffs()))
    alpha = mp.pi / p
    anchors = {h * P for h in range(p)}
    values = [
        mp.mpf(0)
        if j in anchors
        else kernel_closed(p, 2 * mp.pi * j / n + alpha)
        for j in range(n)
    ]
    maximum_residual = mp.mpf(0)
    for shift in range(n - phi.degree()):
        residual = mp.fsum(
            mp.mpf(int(coefficient)) * values[shift + index]
            for index, coefficient in enumerate(coeffs)
        )
        maximum_residual = max(maximum_residual, abs(residual))
    if maximum_residual >= mp.mpf("1e-60"):
        raise AssertionError(("orthogonality residual", n, maximum_residual))
    return {
        "n": n,
        "phi_degree": phi.degree(),
        "basis_shifts": n - phi.degree(),
        "maximum_orthogonality_residual": mp.nstr(maximum_residual, 8),
    }


def verify_negative_control() -> dict[str, object]:
    n = 72
    p = smallest_prime_factor(n)
    P = n // p
    wrong = [kernel(p, 2 * mp.pi * h * P / n) for h in range(p)]
    maximum = max(abs(value) for value in wrong)
    if maximum < mp.mpf("0.5"):
        raise AssertionError("removing pi/p did not break anchor zeros")
    return {
        "n": n,
        "mutation": "removed phase pi/p",
        "maximum_anchor_absolute_value": mp.nstr(maximum, 8),
        "result": "EXPECTED_FAILURE_CONFIRMED",
    }


def verify_wrong_prime_control() -> dict[str, object]:
    n = 30
    wrong_p = 3
    bad = [k for k in range(1, wrong_p) if math.gcd(k, n) != 1]
    if bad != [2]:
        raise AssertionError(("wrong-prime control failed", bad))
    return {
        "n": n,
        "wrong_prime": wrong_p,
        "nonprimitive_low_frequencies": bad,
        "result": "EXPECTED_FAILURE_CONFIRMED",
    }


def verify_direct_sum_closed_form() -> dict[str, object]:
    maximum = mp.mpf(0)
    checked = 0
    for p in (2, 3, 5, 11, 97, 997):
        alpha = mp.pi / p
        for numerator in (1, 7, 19, 43):
            theta = 2 * mp.pi * mp.mpf(numerator) / (6 * p + 1) + alpha / 3
            if abs(mp.cos(theta) - mp.cos(alpha)) < mp.mpf("1e-40"):
                continue
            maximum = max(maximum, abs(kernel(p, theta) - kernel_closed(p, theta)))
            checked += 1
    if maximum >= mp.mpf("1e-65"):
        raise AssertionError(("direct sum / closed form mismatch", maximum))
    return {
        "checked_angles": checked,
        "maximum_absolute_error": mp.nstr(maximum, 8),
        "result": "PASS",
    }


def main() -> None:
    mp.mp.dps = PRECISION
    sign_results = [verify_signs_and_arithmetic(n) for n in range(2, MAX_SIGN_N + 1)]
    algebra_results = [verify_algebra(n) for n in range(2, MAX_ALGEBRA_N + 1)]
    counts = Counter(item["category"] for item in sign_results)
    all_anchor_results = [item for item in sign_results if item["all_anchors_checked"]]
    print(
        json.dumps(
            {
                "schema": "steinberger-full-n-sector-certificate-v2",
                "checked_n_range": [2, MAX_SIGN_N],
                "category_counts": dict(sorted(counts.items())),
                "all_anchor_n_range": [2, MAX_ALL_ANCHOR_N],
                "all_anchor_checks": sum(item["anchor_checks"] for item in all_anchor_results),
                "selected_anchor_checks_above_range": sum(
                    item["anchor_checks"] for item in sign_results if not item["all_anchors_checked"]
                ),
                "algebra_n_range": [2, MAX_ALGEBRA_N],
                "algebra_basis_shift_checks": sum(item["basis_shifts"] for item in algebra_results),
                "representative_sign_results": [
                    sign_results[index - 2]
                    for index in (2, 3, 4, 6, 8, 12, 27, 30, 60, 72, 105, 120, 997)
                ],
                "negative_control": verify_negative_control(),
                "wrong_prime_control": verify_wrong_prime_control(),
                "direct_sum_closed_form": verify_direct_sum_closed_form(),
                "result": "PASS",
                "boundary": (
                    "Finite checks are destructive controls only. The all-orders theorem "
                    "comes from the exact sector identity, primitive-root evaluation, "
                    "and unit-group reduction lemma."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

