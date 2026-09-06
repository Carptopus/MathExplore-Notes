"""Bounded regression from the original h* formula, not a general proof.

Avoid the gamma-to-cross transformation when constructing the target. Compare
its centered monic Ehrhart polynomial with the proposed path recurrence, and
require a last-edge perturbation to fail in every case.
"""

from __future__ import annotations

import sympy as sp

import check_k4n_jacobi as k4
import check_k5n_jacobi as k5


CASES = ((4, 4), (4, 5), (4, 8), (5, 5), (5, 6), (5, 9))
x, y, t = sp.symbols("x y t")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def original_target(m: int, n: int) -> sp.Poly:
    require((m, n) in CASES, "Only the frozen small regression cases are allowed")
    d = m + n - 1
    hstar = sp.Poly(
        sum(
            sp.binomial(2*j, j) * sp.binomial(m-1, j)
            * sp.binomial(n-1, j) * t**j * (1+t)**(d-2*j)
            for j in range(min(m-1, n-1)+1)
        ), t, domain=sp.QQ,
    )
    ehrhart = sum(
        hstar.nth(a) * sp.prod(x+d-a-k for k in range(d)) / sp.factorial(d)
        for a in range(d+1)
    )
    centered = sp.Poly(sp.expand(ehrhart).subs(x, -sp.Rational(1, 2)+sp.I*y).expand(), y)
    return sp.Poly(centered.monic().as_expr(), y, domain=sp.QQ)


def path_polynomial(n: int, tail: list[sp.Expr]) -> sp.Poly:
    # Determinant recurrence uses squared off-diagonal entries directly.
    previous, current = sp.Poly(1, y), sp.Poly(y, y)
    for weight in [sp.Rational(j*j, 4) for j in range(1, n)] + tail:
        previous, current = current, sp.Poly(
            y*current.as_expr()-weight*previous.as_expr(), y, domain=sp.QQ
        )
    return current


def main() -> None:
    for m, n in CASES:
        if m == 4:
            tail = [w.subs(k4.n, n) for w in (k4.alpha, k4.beta_tail, k4.gamma)]
        else:
            tail = [w.subs(k5.n, n) for w in k5.tail_weights]
        target = original_target(m, n)
        require(path_polynomial(n, tail) == target, f"Original-object mismatch: {(m,n)}")
        broken = tail[:-1] + [tail[-1]+1]
        require(path_polynomial(n, broken) != target, f"Perturbation undetected: {(m,n)}")
    print("PASS: 6 original h*-to-Ehrhart comparisons and 6 last-edge negative controls; finite regression only")


if __name__ == "__main__":
    main()
