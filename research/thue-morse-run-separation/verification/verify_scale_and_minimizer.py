"""Destructive finite checks for the scale lemma and binary minimizer.

These checks do not prove the parametric lemmas.  They are designed to catch
indexing errors, missing scale directions, sign mistakes, and false minimizers.
"""

from __future__ import annotations

import json
from pathlib import Path

from verify_candidate import d_from_morphism


def valuation_2(n: int) -> int:
    if n == 0:
        return 10**9
    result = 0
    while n % 2 == 0:
        result += 1
        n //= 2
    return result


def is_vile(n: int) -> bool:
    return valuation_2(n) % 2 == 0


def count_vile(x: int) -> int:
    total = 0
    sign = 1
    while x:
        total += sign * x
        x //= 2
        sign = -sign
    return total


def error(x: int) -> int:
    return 3 * count_vile(x) - 2 * x


def h_map(x: int) -> int:
    return 2 * x - count_vile(x)


def inverse_h_member(y: int) -> int | None:
    low, high = 0, y + 1
    while low < high:
        middle = (low + high) // 2
        if h_map(middle) < y:
            low = middle + 1
        else:
            high = middle
    return low if h_map(low) == y and is_vile(low) else None


def exact_d_is_two(y: int) -> bool:
    return inverse_h_member(y) is not None


def binary_minimizer(q: int, required_h_power: int, max_length: int) -> tuple[int, int, int]:
    threshold = 2**q
    modulus = 2**required_h_power
    # state = (alternating digit sum, residue, valuation of first 1); value = least integer
    states: dict[tuple[int, int, int], int] = {(0, 0, -1): 0}
    best: tuple[int, int, int] | None = None
    for position in range(max_length):
        next_states: dict[tuple[int, int, int], int] = {}
        for (digit_sum, residue, first_one), value in states.items():
            for bit in (0, 1):
                new_value = value + (bit << position)
                new_sum = digit_sum + (bit if position % 2 == 0 else -bit)
                new_residue = (residue + (bit << position)) % modulus if position < required_h_power else residue
                new_first = position if first_one == -1 and bit else first_one
                key = (new_sum, new_residue, new_first)
                if key not in next_states or new_value < next_states[key]:
                    next_states[key] = new_value
        states = next_states
        length = position + 1
        for (digit_sum, _, first_one), value in states.items():
            if value.bit_length() != length or first_one < 0 or first_one % 2:
                continue
            if abs(digit_sum) < threshold or h_map(value) % modulus:
                continue
            row = (value, digit_sum, first_one)
            if best is None or value < best[0]:
                best = row
        if best is not None and length >= best[0].bit_length():
            return best
    raise AssertionError("No minimizer found inside the certified length bound")


def run_checks() -> dict[str, object]:
    for k in range(1, 100_001):
        assert (d_from_morphism(k) == 2) == exact_d_is_two(k)

    scale_checked = 0
    for v in range(1, 300_001):
        if not is_vile(v):
            continue
        y = h_map(v)
        e = error(v)
        r = valuation_2(y)
        if r >= 1 and abs(e) < 2**r:
            assert exact_d_is_two(4 * y)
            scale_checked += 1
        if r >= 4 and abs(e) < 2 ** (r - 2):
            assert exact_d_is_two(y // 4)
            scale_checked += 1

    minimizers: list[dict[str, object]] = []
    for q in range(2, 8):
        m = 2**q
        core = (4**m - 1) // 3
        shift = q - 2 if q % 2 == 0 else q - 1
        expected = core << shift
        length_bound = expected.bit_length() + 2 * q + 12
        weak, weak_e, weak_v2 = binary_minimizer(q, q, length_bound)
        strong, strong_e, strong_v2 = binary_minimizer(q, q + 2, length_bound + 12)
        assert weak == expected
        if q % 2 == 0:
            assert strong == expected
        else:
            assert h_map(strong) // 4 > h_map(expected)
        minimizers.append(
            {
                "q": q,
                "weak_scale_matches_formula": weak == expected,
                "weak_e": weak_e,
                "weak_v2": weak_v2,
                "strong_scale_matches_formula_when_q_even": strong == expected if q % 2 == 0 else None,
                "strong_e": strong_e,
                "strong_v2": strong_v2,
                "odd_q_opposite_direction_is_later": h_map(strong) // 4 > h_map(expected) if q % 2 else None,
            }
        )

    return {
        "status": "PASS_FOR_STATED_FINITE_CHECKS",
        "scope_warning": "Finite destructive checks only; the parametric proof is in S2.",
        "morphism_vs_h_of_v_membership_checked_through": 100_000,
        "scale_lemma_v_checked_through": 300_000,
        "scale_implications_checked": scale_checked,
        "binary_minimizers": minimizers,
    }


if __name__ == "__main__":
    result = run_checks()
    output = Path(__file__).with_name("results") / "scale_and_minimizer_checks.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
