"""Exact checks for THUE-MORSE-RUN-SEPARATION-0001.

This script uses Python integers only.  It deliberately keeps two independent
ways to read d(n): descent in the variable-length morphism and the canonical
Jacobsthal tail rule.
"""

from __future__ import annotations

import json
from pathlib import Path


def jacobsthal(i: int) -> int:
    return (2**i - (-1) ** i) // 3


def canonical_word(n: int) -> str:
    if n == 0:
        return ""
    i = 2
    while jacobsthal(i) <= n:
        i += 1
    remainder = n
    bits: list[str] = []
    for position in range(i - 1, 0, -1):
        value = jacobsthal(position)
        if value <= remainder:
            bits.append("1")
            remainder -= value
        else:
            bits.append("0")
    assert remainder == 0
    word = "".join(bits)
    assert word.startswith("1")
    assert len(word) - len(word.rstrip("1")) in range(0, len(word) + 1, 2)
    return word


def jacobsthal_value(word: str) -> int:
    return sum(int(bit) * jacobsthal(i) for i, bit in enumerate(reversed(word), 1))


def alternating_sum(word: str) -> int:
    return sum(int(bit) * (-1) ** i for i, bit in enumerate(reversed(word), 1))


def tail_run_length(word: str) -> int:
    if not word:
        return 0
    return len(word) - len(word.rstrip(word[-1]))


def d_from_jacobsthal(n: int) -> int:
    if n == 0:
        return 1
    return 1 if tail_run_length(canonical_word(n)) % 2 == 0 else 2


def morphism_lengths_until(n: int) -> tuple[list[int], list[int]]:
    length_1 = [1]
    length_2 = [1]
    while length_1[-1] <= n:
        old_1, old_2 = length_1[-1], length_2[-1]
        length_1.append(2 * old_1 + old_2)
        length_2.append(2 * old_1 + 3 * old_2)
    return length_1, length_2


def d_from_morphism(n: int) -> int:
    length_1, length_2 = morphism_lengths_until(n)
    level = len(length_1) - 1
    symbol = 1
    while level:
        image = (1, 2, 1) if symbol == 1 else (1, 2, 2, 2, 1)
        for child in image:
            child_length = (length_1 if child == 1 else length_2)[level - 1]
            if n < child_length:
                symbol = child
                break
            n -= child_length
        level -= 1
    return symbol


def exponent(q: int) -> int:
    return 2 ** (q + 1) - 2 if q % 2 == 0 else 2 ** (q + 1) + 1


def candidate(q: int) -> int:
    return 2 ** exponent(q) // 9


def candidate_words(q: int) -> tuple[str, str]:
    if q % 2 == 0:
        return "10" * (2**q - 2) + "1" * q, "10" * 2**q + "0" * (q - 2)
    return "10" * 2**q + "0" * (q - 1), "10" * (2**q - 1) + "0100" + "1" * (q - 1)


def first_separation(q: int, limit: int) -> int | None:
    for n in range(1, limit + 1):
        if d_from_morphism(2 ** (q + 2) * n) != d_from_morphism(2**q * n):
            return n
    return None


def run_checks() -> dict[str, object]:
    for n in range(100_001):
        assert d_from_morphism(n) == d_from_jacobsthal(n)

    exact_small = {"2": first_separation(2, 7), "3": first_separation(3, 14_563)}
    assert exact_small == {"2": 7, "3": 14_563}

    rows: list[dict[str, object]] = []
    for q in range(2, 13):
        n = candidate(q)
        word, four_word = candidate_words(q)
        x = 2**q * n
        four_x = 4 * x
        assert jacobsthal_value(word) == x
        assert jacobsthal_value(four_word) == four_x
        assert canonical_word(x) == word
        assert canonical_word(four_x) == four_word
        left = d_from_morphism(x)
        right = d_from_morphism(four_x)
        assert left != right
        assert d_from_morphism(2**q * (n - 1)) == d_from_morphism(2 ** (q + 2) * (n - 1))
        rows.append(
            {
                "q": q,
                "E_q": exponent(q),
                "candidate_decimal": str(n),
                "candidate_bit_length": n.bit_length(),
                "d_at_2q_candidate": left,
                "d_at_2q_plus_2_candidate": right,
                "alternating_sum_word": alternating_sum(word),
                "alternating_sum_four_word": alternating_sum(four_word),
                "word_length": len(word),
                "four_word_length": len(four_word),
            }
        )

    false_exponent_rejections: list[dict[str, object]] = []
    for q in range(2, 9):
        correct = exponent(q)
        rejected = []
        for wrong in (correct - 1, correct + 1):
            n = 2**wrong // 9
            rejected.append(
                {
                    "exponent": wrong,
                    "separates": d_from_morphism(2**q * n) != d_from_morphism(2 ** (q + 2) * n),
                }
            )
        assert not any(item["separates"] for item in rejected)
        false_exponent_rejections.append({"q": q, "checks": rejected})

    return {
        "status": "PASS_FOR_STATED_FINITE_CHECKS",
        "scope_warning": "Candidate witnesses and q=2,3 minimality only; general minimality is not proved.",
        "morphism_vs_jacobsthal_checked_through": 100_000,
        "exact_small_first_separations": exact_small,
        "candidate_rows": rows,
        "destructive_false_exponent_checks": false_exponent_rejections,
    }


if __name__ == "__main__":
    result = run_checks()
    output = Path(__file__).with_name("results") / "candidate_checks.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
