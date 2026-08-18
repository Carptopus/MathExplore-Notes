"""Independent prime-field audit of the D2 character-count formula."""

from __future__ import annotations

import json
import math
from pathlib import Path


PRIMES = (7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83)


def chi(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    result = pow(value, (prime - 1) // 2, prime)
    if result == 1:
        return 1
    if result == prime - 1:
        return -1
    raise AssertionError("Euler criterion failed")


def direct_count(alpha: int, prime: int) -> int:
    return sum(
        chi(ratio, prime) == 1
        and chi(1 + alpha * ratio, prime) == 1
        and chi(ratio + alpha, prime) == 1
        for ratio in range(prime)
    )


def cubic_sum(alpha: int, prime: int) -> int:
    return sum(
        chi(ratio * (1 + alpha * ratio) * (ratio + alpha), prime)
        for ratio in range(prime)
    )


def main() -> None:
    records = []
    for prime in PRIMES:
        alphas = [
            alpha
            for alpha in range(prime)
            if chi(alpha, prime) == -1 and chi(1 + alpha, prime) == -1
        ]
        if len(alphas) != (prime - 3) // 4:
            raise AssertionError("the alpha count formula failed")

        alpha_records = []
        for alpha in alphas:
            trace_sum = cubic_sum(alpha, prime)
            predicted_numerator = (
                prime - 3 + trace_sum - 4 * chi(alpha - 1, prime)
            )
            if predicted_numerator % 8:
                raise AssertionError("the D2 numerator is not divisible by eight")
            predicted = predicted_numerator // 8
            observed = direct_count(alpha, prime)
            if predicted != observed:
                raise AssertionError("the fixed-alpha count formula failed")
            if abs(trace_sum) > 2 * math.sqrt(prime) + 1e-12:
                raise AssertionError("the cubic character sum violates Hasse")
            alpha_records.append(
                {
                    "alpha": alpha,
                    "T_alpha": trace_sum,
                    "chi_alpha_minus_one": chi(alpha - 1, prime),
                    "C_alpha": observed,
                }
            )

        total = sum(record["C_alpha"] for record in alpha_records)
        empirical_closed_form = (
            prime * prime - 6 * prime + 1 - 8 * chi(2, prime)
        ) // 32
        if total != empirical_closed_form:
            raise AssertionError("the registered empirical total-count formula failed")
        records.append(
            {
                "q": prime,
                "alpha_count": len(alphas),
                "admissible_pair_count": total,
                "minimum_C_alpha": min((row["C_alpha"] for row in alpha_records), default=0),
                "hasse_lower_bound": (prime - 7 - 2 * math.sqrt(prime)) / 8,
                "alpha_records": alpha_records,
            }
        )

    output = {
        "experiment_id": "HSF-SWITCH-0002-D2-CHARACTER-COUNT",
        "checks": {
            "alpha_count_formula": True,
            "fixed_alpha_formula_D2_1": True,
            "hasse_bound_on_frozen_primes": True,
            "empirical_total_count_formula_on_frozen_primes": True,
        },
        "records": records,
        "claim_boundary": (
            "The script verifies D2.1 on frozen prime fields. The displayed total "
            "pair-count closed form is still empirical and is not used in the Hasse "
            "existence proof. Prime-power and literature audits remain open."
        ),
    }
    output_path = Path(__file__).resolve().parent / "results" / "general-paley-switch-character-count.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output["checks"], ensure_ascii=False, indent=2))
    print(json.dumps([{key: row[key] for key in row if key != "alpha_records"} for row in records], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
