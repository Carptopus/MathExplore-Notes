"""Exact verification of a height-one Peck-poset counterexample family."""

from __future__ import annotations

from collections import deque
from itertools import combinations
from math import comb


def graph(a: int, c: int) -> list[int]:
    """Return adjacency bitmasks for L=A+W and R=B+C.

    |A|=|C|=a and |W|=|B|=c.  Edges are A--B complete,
    A--C by the identity matching, and W--(B union C) complete.
    """
    n = a + c
    rows: list[int] = []
    b_mask = (1 << c) - 1
    all_right = (1 << n) - 1
    for i in range(a):
        rows.append(b_mask | (1 << (c + i)))
    rows.extend([all_right] * c)
    return rows


def connected(rows: list[int]) -> bool:
    n = len(rows)
    seen = {0}
    queue = deque([0])
    while queue:
        v = queue.popleft()
        if v < n:
            neighbours = (n + j for j in range(n) if rows[v] >> j & 1)
        else:
            j = v - n
            neighbours = (i for i in range(n) if rows[i] >> j & 1)
        for w in neighbours:
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return len(seen) == 2 * n


def maximum_matching(rows: list[int]) -> int:
    n = len(rows)
    right_match = [-1] * n

    def augment(left: int, seen: set[int]) -> bool:
        for right in range(n):
            if rows[left] >> right & 1 and right not in seen:
                seen.add(right)
                if right_match[right] < 0 or augment(right_match[right], seen):
                    right_match[right] = left
                    return True
        return False

    return sum(augment(left, set()) for left in range(n))


def formula_polynomial(a: int, c: int) -> list[int]:
    b = a + c
    return [
        (2**i - 2) * comb(a, i) + 2 * comb(b, i)
        for i in range(b + 1)
    ]


def brute_polynomial(rows: list[int]) -> list[int]:
    n = len(rows)
    out = [0] * (n + 1)
    for left_mask in range(1 << n):
        forbidden = 0
        for left in range(n):
            if left_mask >> left & 1:
                forbidden |= rows[left]
        allowed = ((1 << n) - 1) ^ forbidden
        right_mask = allowed
        while True:
            out[left_mask.bit_count() + right_mask.bit_count()] += 1
            if right_mask == 0:
                break
            right_mask = (right_mask - 1) & allowed
    return out


def full_subset_polynomial(rows: list[int]) -> list[int]:
    """Inspect every one of the 2^(2n) vertex subsets independently."""
    n = len(rows)
    out = [0] * (n + 1)
    for subset in range(1 << (2 * n)):
        left_mask = subset & ((1 << n) - 1)
        right_mask = subset >> n
        independent = True
        for left in range(n):
            if left_mask >> left & 1 and rows[left] & right_mask:
                independent = False
                break
        if independent:
            out[subset.bit_count()] += 1
    return out


def log_concavity_failures(polynomial: list[int]) -> list[tuple[int, int]]:
    return [
        (i, polynomial[i] ** 2 - polynomial[i - 1] * polynomial[i + 1])
        for i in range(1, len(polynomial) - 1)
        if polynomial[i] ** 2 < polynomial[i - 1] * polynomial[i + 1]
    ]


def verify(a: int, c: int) -> tuple[list[int], list[tuple[int, int]]]:
    rows = graph(a, c)
    assert connected(rows)
    assert maximum_matching(rows) == a + c
    formula = formula_polynomial(a, c)
    brute = brute_polynomial(rows)
    assert formula == brute
    return formula, log_concavity_failures(formula)


def main() -> None:
    polynomial, failures = verify(7, 2)
    assert polynomial == [1, 18, 114, 378, 742, 882, 602, 198, 18, 2]
    assert failures == [(8, -72)]

    rows = graph(7, 2)
    assert full_subset_polynomial(rows) == polynomial

    # Boundary control inside the same two-parameter construction.
    for a in range(1, 7):
        _, previous_failures = verify(a, 2)
        assert previous_failures == []

    # The displayed top-coefficient obstruction persists for the infinite
    # subfamily c=2, a>=7.
    for a in range(7, 41):
        p = formula_polynomial(a, 2)
        assert p[a + 1] ** 2 < p[a] * p[a + 2]

    print("PASS: graph connected and has a perfect matching")
    print("PASS: closed formula equals exhaustive antichain enumeration")
    print("PASS: an independent scan inspected all 2^18 vertex subsets")
    print("PASS: a=7, c=2 has log-concavity defect -72 at index 8")
    print("PASS: every c=2 parameter 1 <= a <= 6 is a negative control")
    print("PASS: the same top-coefficient obstruction holds for 7 <= a <= 40")


if __name__ == "__main__":
    main()
