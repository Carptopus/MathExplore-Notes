"""Symbolically check the split-prime eigenline boundary in Section 4."""

from __future__ import annotations

import json

import sympy as sp


s = sp.symbols("s")


def reduce_s(expression: sp.Expr) -> sp.Expr:
    return sp.rem(sp.Poly(sp.expand(expression), s), sp.Poly(s**2 + 1, s)).as_expr()


lines = {
    "i": ((1, 0), (0, 1)),
    "-i": ((0, 1), (1, 0)),
    "j": ((1, s), (1, -s)),
    "-j": ((1, -s), (1, s)),
    "k": ((1, 1), (1, -1)),
    "-k": ((1, -1), (1, 1)),
}
opposite = {"i": "-i", "-i": "i", "j": "-j", "-j": "j", "k": "-k", "-k": "k"}


def determinant(first: tuple[sp.Expr, sp.Expr], second: tuple[sp.Expr, sp.Expr]) -> sp.Expr:
    return reduce_s(first[0] * second[1] - first[1] * second[0])


rows = []
for left, (left_plus, _) in lines.items():
    for right, (_, right_minus) in lines.items():
        value = determinant(left_plus, right_minus)
        is_zero = value == 0
        if is_zero != (right == opposite[left]):
            raise AssertionError((left, right, value))
        if not is_zero:
            norm = reduce_s(value * value.xreplace({s: -s}))
            if norm not in (1, 2, 4):
                raise AssertionError((left, right, value, norm))
        rows.append({"left_plus": left, "right_minus": right, "determinant": str(value)})

print(
    json.dumps(
        {
            "status": "PASS_SPLIT_EIGENLINE_BOUNDARY",
            "ordered_pairs": len(rows),
            "zero_pairs": sum(row["determinant"] == "0" for row in rows),
            "boundary": "zero exactly for the six antipodal ordered pairs",
            "rows": rows,
        },
        indent=2,
    )
)
