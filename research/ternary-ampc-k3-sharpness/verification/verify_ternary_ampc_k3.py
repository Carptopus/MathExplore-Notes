"""Exact finite-state certificate for the substitution

    0 -> 001, 1 -> 020, 2 -> 000.

For a sorted offset tuple C, ``language(C)`` computes the exact ordered letter
tuples seen along translates of the primitive fixed point.  The recursion uses
the three residue classes modulo 3.  Uniform recurrence lets us discard the
finite prefix introduced when the quotient offsets are normalized.

The proof certificate is the finite closure of 3-by-3 local language patches
under the nine base-3 digit transitions.  Unlike a bounded offset scan, this
closure covers every pair of nonnegative offsets.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from collections import Counter, deque
from itertools import combinations


SIGMA = {
    0: (0, 0, 1),
    1: (0, 2, 0),
    2: (0, 0, 0),
}

EXPECTED_PATCH_STATES = 938
EXPECTED_PATCH_TRANSITIONS = 8442
EXPECTED_DISTRIBUTION = {3: 3, 4: 246, 5: 223, 6: 285, 7: 181}
EXPECTED_CLOSURE_SHA256 = (
    "BBF0CBF7D6E5E23CCEECC71A59644AD4F5DA0D48A1A2A0A219BB292A127CDAAA"
)
EXPECTED_WITNESS = frozenset(
    {(0, 2, 1), (1, 0, 2), (1, 1, 1), (1, 2, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)}
)


def _seed_pair_factors() -> frozenset[tuple[int, int]]:
    word = (0,)
    previous: frozenset[tuple[int, int]] = frozenset()
    for _ in range(10):
        word = tuple(symbol for letter in word for symbol in SIGMA[letter])
        current = frozenset(zip(word, word[1:]))
        if current == previous:
            return current
        previous = current
    raise AssertionError("length-two factor set did not stabilize")


PAIR_FACTORS = _seed_pair_factors()
EXPECTED_PAIR_FACTORS = frozenset({(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)})
if PAIR_FACTORS != EXPECTED_PAIR_FACTORS:
    raise AssertionError(("unexpected length-two language", PAIR_FACTORS))


def normalize(offsets: tuple[int, ...]) -> tuple[int, ...]:
    base = min(offsets)
    return tuple(value - base for value in offsets)


@lru_cache(maxsize=None)
def language(offsets: tuple[int, ...]) -> frozenset[tuple[int, ...]]:
    """Return the exact ordered pattern language at ``offsets``.

    Repeated quotient offsets are allowed and are needed by the recursion.
    The public calls use strictly increasing offsets.
    """

    offsets = normalize(offsets)
    if max(offsets) == 0:
        return frozenset((letter,) * len(offsets) for letter in range(3))
    if max(offsets) == 1:
        return frozenset(
            tuple(pair[offset] for offset in offsets) for pair in PAIR_FACTORS
        )

    result: set[tuple[int, ...]] = set()
    for residue in range(3):
        quotients = tuple((residue + value) // 3 for value in offsets)
        digits = tuple((residue + value) % 3 for value in offsets)
        quotient_base = min(quotients)
        child_offsets = tuple(value - quotient_base for value in quotients)
        for child in language(child_offsets):
            result.add(
                tuple(SIGMA[letter][digit] for letter, digit in zip(child, digits))
            )
    return frozenset(result)


def parikh_language(a: int, b: int) -> frozenset[tuple[int, int, int]]:
    words = language((0, a, b))
    return frozenset(
        (word.count(0), word.count(1), word.count(2)) for word in words
    )


def fixed_prefix(iterations: int = 10) -> tuple[int, ...]:
    word = (0,)
    for _ in range(iterations):
        word = tuple(symbol for letter in word for symbol in SIGMA[letter])
    return word


def direct_prefix_language(
    word: tuple[int, ...], a: int, b: int
) -> frozenset[tuple[int, int, int]]:
    result: set[tuple[int, int, int]] = set()
    for start in range(len(word) - b):
        sample = (word[start], word[start + a], word[start + b])
        result.add((sample.count(0), sample.count(1), sample.count(2)))
    return frozenset(result)


RELATIVE_CELLS = tuple(
    (i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)
)
CENTER_INDEX = RELATIVE_CELLS.index((0, 0))


def local_patch(a: int, b: int) -> tuple[frozenset[tuple[int, ...]], ...]:
    """Nine neighboring ordered triple languages around ``(a,b)``."""

    return tuple(language((0, a + i, b + j)) for i, j in RELATIVE_CELLS)


def digit_transition(
    patch: tuple[frozenset[tuple[int, ...]], ...], digit_a: int, digit_b: int
) -> tuple[frozenset[tuple[int, ...]], ...]:
    """Compute ``K(3a+digit_a, 3b+digit_b)`` from ``K(a,b)``.

    For a target neighbor ``(i,j)`` and a translation residue ``t``, the two
    quotient offsets differ from ``(a,b)`` by values in ``{-1,0,1}``.  Hence
    the 3-by-3 patch contains every child language required by the recursion.
    """

    child_by_cell = dict(zip(RELATIVE_CELLS, patch))
    output: list[frozenset[tuple[int, ...]]] = []
    for i, j in RELATIVE_CELLS:
        words: set[tuple[int, ...]] = set()
        for residue in range(3):
            child_cell = (
                (residue + digit_a + i) // 3,
                (residue + digit_b + j) // 3,
            )
            output_digits = (
                residue,
                (residue + digit_a + i) % 3,
                (residue + digit_b + j) % 3,
            )
            for child in child_by_cell[child_cell]:
                words.add(
                    tuple(
                        SIGMA[letter][digit]
                        for letter, digit in zip(child, output_digits)
                    )
                )
        output.append(frozenset(words))
    return tuple(output)


def finite_patch_closure() -> tuple[
    set[tuple[frozenset[tuple[int, ...]], ...]], int
]:
    initial = local_patch(0, 0)
    states = {initial}
    queue = deque([initial])
    transition_count = 0
    while queue:
        current = queue.popleft()
        for digit_a in range(3):
            for digit_b in range(3):
                transition_count += 1
                target = digit_transition(current, digit_a, digit_b)
                if target not in states:
                    states.add(target)
                    queue.append(target)
    return states, transition_count


def parikh_set(words: frozenset[tuple[int, ...]]) -> frozenset[tuple[int, int, int]]:
    return frozenset(
        (word.count(0), word.count(1), word.count(2)) for word in words
    )


def canonical_patch(patch: tuple[frozenset[tuple[int, ...]], ...]) -> tuple:
    return tuple(tuple(sorted(language_cell)) for language_cell in patch)


def closure_sha256(
    states: set[tuple[frozenset[tuple[int, ...]], ...]]
) -> str:
    ordered = sorted(states, key=canonical_patch)
    state_id = {state: index for index, state in enumerate(ordered)}
    payload = {
        "states": [canonical_patch(state) for state in ordered],
        "transitions": [
            (state_id[state], digit_a, digit_b, state_id[digit_transition(state, digit_a, digit_b)])
            for state in ordered
            for digit_a in range(3)
            for digit_b in range(3)
        ],
    }
    encoded = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest().upper()


def main() -> None:
    prefix = fixed_prefix()

    # Cross-check the recursion against a long explicit prefix on a fixed box.
    for a, b in combinations(range(25), 2):
        if a == 0:
            continue
        exact = parikh_language(a, b)
        observed = direct_prefix_language(prefix, a, b)
        if exact != observed:
            raise AssertionError((a, b, exact, observed))

    states, transition_count = finite_patch_closure()
    distribution = Counter(
        len(parikh_set(state[CENTER_INDEX])) for state in states
    )
    maximum = max(distribution)
    digest = closure_sha256(states)
    if len(states) != EXPECTED_PATCH_STATES:
        raise AssertionError(("unexpected patch-state count", len(states)))
    if transition_count != EXPECTED_PATCH_TRANSITIONS:
        raise AssertionError(("unexpected transition count", transition_count))
    if dict(sorted(distribution.items())) != EXPECTED_DISTRIBUTION:
        raise AssertionError(("unexpected center-complexity distribution", distribution))
    if maximum != 7:
        raise AssertionError(("unexpected maximum center complexity", maximum))
    if digest != EXPECTED_CLOSURE_SHA256:
        raise AssertionError(("unexpected closure hash", digest))

    # Cross-check the digit automaton against direct recursive patches.
    initial = local_patch(0, 0)
    for a in range(100):
        for b in range(100):
            digits: list[tuple[int, int]] = []
            quotient_a, quotient_b = a, b
            while quotient_a or quotient_b:
                digits.append((quotient_a % 3, quotient_b % 3))
                quotient_a //= 3
                quotient_b //= 3
            state = initial
            for digit_a, digit_b in reversed(digits):
                state = digit_transition(state, digit_a, digit_b)
            if state != local_patch(a, b):
                raise AssertionError(("patch transition mismatch", a, b))

    witness = parikh_language(2, 9)
    if witness != EXPECTED_WITNESS:
        raise AssertionError(("sharp witness failed", witness))

    print("PAIR_FACTORS", sorted(PAIR_FACTORS))
    print("PATCH_STATES", len(states))
    print("PATCH_TRANSITIONS", transition_count)
    print("CLOSURE_SHA256", digest)
    print("CENTER_PARIKH_SIZE_DISTRIBUTION", dict(sorted(distribution.items())))
    print("MAX_CENTER_PARIKH_SIZE", maximum)
    print("SHARP_PATTERN", (0, 2, 9), sorted(witness))
    print("PASS: exact finite patch closure covers all base-3 offset pairs")


if __name__ == "__main__":
    main()
