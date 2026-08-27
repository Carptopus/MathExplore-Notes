"""Check the divisor-residue condition in the accompanying manuscript."""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
import math


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1 if divisor == 2 else 2
    return True


def condition(primes: tuple[int, ...]) -> dict[str, object]:
    if len(primes) < 4:
        raise AssertionError("at least four distinct prime factors are required")
    if tuple(sorted(primes)) != primes or len(set(primes)) != len(primes):
        raise AssertionError("the prime factors must be distinct and increasing")
    if any(prime % 2 == 0 or not is_prime(prime) for prime in primes):
        raise AssertionError("all factors must be odd primes")

    p = primes[0]
    others = primes[1:]
    k = len(others)
    product = math.prod(others)
    negative_sign_bound = 0
    positive_sign_bound = 0
    proper_divisor_sum = 0
    terms: list[dict[str, object]] = []

    for size in range(k):
        for selected in combinations(others, size):
            divisor = math.prod(selected)
            complementary_product = product // divisor
            residue = complementary_product % p
            if residue == 0:
                raise AssertionError("a complementary product is divisible by p")
            sign = -1 if (k - size) % 2 else 1
            contribution = divisor * (residue if sign < 0 else p)
            if sign < 0:
                negative_sign_bound += contribution
            else:
                positive_sign_bound += contribution
            proper_divisor_sum += divisor
            terms.append(
                {
                    "divisor": divisor,
                    "complementary_product": complementary_product,
                    "complement_size": k - size,
                    "sign": sign,
                    "residue_mod_p": residue,
                    "upper_bound_contribution": contribution,
                }
            )

    anchor_bound = Fraction(p * proper_divisor_sum, others[0] - 1)
    total_bound = Fraction(
        negative_sign_bound + positive_sign_bound
    ) + anchor_bound
    reciprocal_sum = sum((Fraction(1, prime) for prime in others), Fraction())
    return {
        "n": math.prod(primes),
        "primes": list(primes),
        "nonminimal_prime_count": k,
        "tail_product": product,
        "negative_sign_residue_bound": negative_sign_bound,
        "positive_sign_p_bound": positive_sign_bound,
        "proper_divisor_sum": proper_divisor_sum,
        "anchor_bound": str(anchor_bound),
        "total_bound": str(total_bound),
        "bound_over_tail_product": str(total_bound / product),
        "tail_condition_strict": total_bound < product,
        "steinberger_reciprocal_condition": Fraction(2, p) > reciprocal_sum,
        "outside_steinberger_condition": Fraction(2, p) <= reciprocal_sum,
        "terms": terms,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primes", type=int, nargs="+", required=True)
    arguments = parser.parse_args()
    result = condition(tuple(arguments.primes))
    result["result"] = (
        "PASS" if result["tail_condition_strict"] else "HYPOTHESIS_NOT_SATISFIED"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
