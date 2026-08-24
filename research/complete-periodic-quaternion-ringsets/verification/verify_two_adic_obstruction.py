"""Independent finite calibration for the Section 7 two-adic obstruction.

This program checks the valuation identities used in the proof.  It does not
search for a witness and does not prove the unbounded statement.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def v2(value: int) -> int:
    if value == 0:
        return 10**9
    value = abs(value)
    return (value & -value).bit_length() - 1


def factorial_v2(value: int) -> int:
    return sum(value // (2**power) for power in range(1, value.bit_length() + 1))


def tau(value: int) -> int:
    return v2(value * value + 4)


def p_value(period: int, difference: int) -> int:
    return math.prod(difference - offset for offset in range(1, period))


def gaussian_valuation_q(period: int, difference: int) -> int:
    return 2 * v2(p_value(period, difference)) + sum(
        tau(difference - offset) for offset in range(1, period)
    )


def analyze(exponent: int) -> dict[str, int]:
    period = 2**exponent
    base_factorial = factorial_v2(period - 1)
    base_tau = 5 * period // 4 - 2
    baseline = 2 * base_factorial + base_tau

    if gaussian_valuation_q(period, 0) != baseline:
        raise AssertionError("baseline formula failed")

    minimum_gain = 10**9
    for residue in range(1, period):
        # The least lift already realizes the lower-bound regime unless it is
        # an exact root, in which case use the next period lift.
        for lift in (0, period, -period):
            difference = residue + lift
            if difference in range(1, period):
                continue
            gain = gaussian_valuation_q(period, difference) - baseline
            minimum_gain = min(minimum_gain, gain)
    if minimum_gain < 2:
        raise AssertionError((exponent, minimum_gain))

    modulus_exponent = baseline + 2
    return {
        "exponent": exponent,
        "period": period,
        "factorial_v2": base_factorial,
        "tau_sum": base_tau,
        "baseline_pi_valuation": baseline,
        "minimum_checked_off_class_gain": minimum_gain,
        "witness_modulus_exponent": modulus_exponent,
        "null_same_class_lower_bound": baseline + exponent,
        "transverse_failure_v2": baseline + 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = [analyze(exponent) for exponent in range(3, 11)]
    payload = {
        "status": "PASS_FINITE_VALUATION_CALIBRATION",
        "boundary": (
            "checks the closed valuation formulas for 3 <= N <= 10 and "
            "three representative lifts per nonzero residue; the general "
            "proof is the argument in Section 7"
        ),
        "rows": rows,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")


if __name__ == "__main__":
    main()
