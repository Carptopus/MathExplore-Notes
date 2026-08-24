"""Finite calibration for the candidate F7* partition-degree proof.

This script does not prove the group-slice normal form.  It independently checks
the multiplication order in the three propagated circuit identities, verifies
the resulting construction for elementary abelian 2-groups, and exhibits the
predicted failed circuit for groups having a non-involution.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product, permutations


CIRCUIT_HYPERPLANES = {
    frozenset(s)
    for s in (
        (0, 1, 2, 4),
        (0, 1, 3, 5),
        (0, 2, 3, 6),
        (0, 4, 5, 6),
        (1, 2, 5, 6),
        (1, 3, 4, 6),
        (2, 3, 4, 5),
    )
}


class Group:
    def __init__(self, name, elements, multiply, identity):
        self.name = name
        self.elements = tuple(elements)
        self.mul = multiply
        self.e = identity
        self.inverse = {}
        for x in self.elements:
            ys = [y for y in self.elements if self.mul(x, y) == self.e and self.mul(y, x) == self.e]
            assert len(ys) == 1
            self.inverse[x] = ys[0]

    def inv(self, x):
        return self.inverse[x]


def cyclic(n):
    return Group(f"C{n}", range(n), lambda x, y: (x + y) % n, 0)


def elementary_abelian_2(k):
    return Group(f"C2^{k}", range(1 << k), lambda x, y: x ^ y, 0)


def symmetric_3():
    elems = tuple(permutations(range(3)))

    def compose(p, q):
        return tuple(p[q[i]] for i in range(3))

    return Group("S3", elems, compose, (0, 1, 2))


def dihedral_8():
    """The order-eight group <r,s | r^4=s^2=e, srs=r^-1>."""
    elems = tuple(product(range(4), range(2)))

    def multiply(x, y):
        i, j = x
        k, ell = y
        return ((i + (-1 if j else 1) * k) % 4, (j + ell) % 2)

    return Group("D8", elems, multiply, (0, 0))


def canonical_slice_identities(group):
    """Check P,Q,R on the normalized a=a0 slice over their full domains."""
    for b, c, d in product(group.elements, repeat=3):
        f = group.mul(group.inv(b), c)
        g = group.mul(group.inv(b), d)
        h = group.mul(group.inv(c), d)

        p = group.mul(group.mul(group.inv(c), b), g)
        q = group.mul(group.mul(group.inv(f), group.inv(b)), d)
        r = group.mul(group.mul(f, group.inv(c)), d)
        assert p == h
        assert q == h
        assert r == g


def propagated_row(group, a, b, c, d):
    s = a
    f = group.mul(group.mul(group.inv(b), group.inv(s)), c)
    g = group.mul(group.mul(group.inv(b), s), d)
    h = group.mul(group.mul(group.inv(c), s), d)
    return (a, b, c, d, f, g, h)


def rank_f7_dual(subset):
    size = len(subset)
    if size <= 3:
        return size
    if size == 4 and frozenset(subset) in CIRCUIT_HYPERPLANES:
        return 3
    return 4


def verify_full_voa(group):
    rows = [propagated_row(group, *x) for x in product(group.elements, repeat=4)]
    n = len(group.elements)
    for size in range(8):
        for subset in combinations(range(7), size):
            counts = Counter(tuple(row[i] for i in subset) for row in rows)
            expected_blocks = n ** rank_f7_dual(subset)
            assert len(counts) == expected_blocks, (group.name, subset, len(counts), expected_blocks)
            expected_frequency = n ** (4 - rank_f7_dual(subset))
            assert set(counts.values()) == {expected_frequency}, (group.name, subset)


def first_failed_last_circuit(group):
    for a, b, c, d in product(group.elements, repeat=4):
        row = propagated_row(group, a, b, c, d)
        _, _, c0, d0, f, g, _ = row
        expected_g = group.mul(group.mul(f, group.inv(c0)), d0)
        if g != expected_g:
            return (a, b, c, d, f, g, expected_g)
    return None


def main():
    groups = [
        cyclic(2),
        elementary_abelian_2(2),
        elementary_abelian_2(3),
        cyclic(4),
        cyclic(6),
        symmetric_3(),
        dihedral_8(),
    ]
    for group in groups:
        canonical_slice_identities(group)
        involutions = [x for x in group.elements if group.mul(x, x) == group.e]
        exponent_two = len(involutions) == len(group.elements)
        if exponent_two:
            verify_full_voa(group)
            outcome = "FULL_F7STAR_VOA_PASS"
        else:
            witness = first_failed_last_circuit(group)
            assert witness is not None
            outcome = f"LAST_CIRCUIT_FAIL witness={witness!r}"
        print(
            f"{group.name}: order={len(group.elements)} "
            f"involutions={len(involutions)} exponent_two={exponent_two} {outcome}"
        )


if __name__ == "__main__":
    main()
