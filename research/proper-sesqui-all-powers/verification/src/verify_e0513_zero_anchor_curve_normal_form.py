"""Exact symbolic verification of the E0513 zero-anchor curve normal form."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


Monomial = tuple[int, ...]
Polynomial = frozenset[Monomial]


def add(*values: Polynomial) -> Polynomial:
    result: set[Monomial] = set()
    for value in values:
        result.symmetric_difference_update(value)
    return frozenset(result)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: set[Monomial] = set()
    for left_term in left:
        for right_term in right:
            term = tuple(a + b for a, b in zip(left_term, right_term))
            if term in result:
                result.remove(term)
            else:
                result.add(term)
    return frozenset(result)


def power(value: Polynomial, exponent: int) -> Polynomial:
    if not value:
        return value
    one = frozenset({tuple(0 for _ in next(iter(value)))})
    result = one
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        remaining >>= 1
    return result


def variable(count: int, index: int) -> Polynomial:
    term = [0] * count
    term[index] = 1
    return frozenset({tuple(term)})


def one(count: int) -> Polynomial:
    return frozenset({tuple(0 for _ in range(count))})


def monomial(*exponents: int) -> Polynomial:
    return frozenset({tuple(exponents)})


def substitute_a_t_into_h_w(value: Polynomial) -> Polynomial:
    """Substitute a=h^2 and t=hw into a polynomial in (a,t)."""

    result: set[Monomial] = set()
    for a_degree, t_degree in value:
        term = (2 * a_degree + t_degree, t_degree)
        if term in result:
            result.remove(term)
        else:
            result.add(term)
    return frozenset(result)


def substitute_a_p_into_h_w(value: Polynomial) -> Polynomial:
    """Substitute a=h^2 and p=hw into a polynomial in (a,p)."""

    return substitute_a_t_into_h_w(value)


def polynomial_payload(value: Polynomial, variables: Iterable[str]) -> dict[str, object]:
    names = list(variables)
    terms = [list(term) for term in sorted(value)]
    encoded = json.dumps(terms, separators=(",", ":")).encode("ascii")
    return {
        "variables": names,
        "term_count": len(terms),
        "terms": terms,
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # First derive the zero-anchor numerator directly from the published
    # Subiaco formula.  Variables are (h,w), c=h^2, x=cw^2.
    h = variable(2, 0)
    w = variable(2, 1)
    one_hw = one(2)
    c = power(h, 2)
    x = multiply(c, power(w, 2))
    u = add(one_hw, c, power(c, 2))
    denominator = add(power(x, 2), multiply(c, x), one_hw)
    numerator_f = add(
        multiply(power(c, 2), add(power(x, 4), x)),
        multiply(multiply(power(c, 2), u), add(power(x, 3), power(x, 2))),
    )
    square_root_x = multiply(h, w)
    direct_numerator_b = add(
        numerator_f,
        multiply(add(square_root_x, multiply(u, x)), power(denominator, 2)),
    )

    k_h_w = add(
        one_hw,
        multiply(add(h, power(h, 3)), w),
        multiply(add(power(h, 7), power(h, 9), power(h, 11)), power(w, 3)),
        multiply(power(h, 8), power(w, 4)),
        multiply(power(h, 11), power(w, 7)),
        multiply(power(h, 8), power(w, 8)),
        multiply(add(power(h, 9), power(h, 11), power(h, 13)), power(w, 9)),
    )
    expected_direct_numerator = multiply(multiply(h, w), k_h_w)
    if direct_numerator_b != expected_direct_numerator:
        raise AssertionError("direct Subiaco numerator does not equal hw*K_h(w)")

    # The dimension-free variables are a=h^2 and t=hr.
    a = variable(2, 0)
    t = variable(2, 1)
    one_at = one(2)
    u_a = add(one_at, a, power(a, 2))
    k_a_t = add(
        one_at,
        multiply(add(one_at, a), t),
        multiply(multiply(power(a, 2), u_a), power(t, 3)),
        multiply(power(a, 2), power(t, 4)),
        multiply(power(a, 2), power(t, 7)),
        power(t, 8),
        multiply(u_a, power(t, 9)),
    )
    if substitute_a_t_into_h_w(k_a_t) != k_h_w:
        raise AssertionError("K(a,t) does not specialize to K_h(w)")

    # For a generic image preimage write x=cw^2 and p=hw.  Then
    # B_c(x)=p*K(a,p)/(p^8+a^2*p^4+1).
    p = variable(2, 1)
    normalized_denominator = add(
        power(p, 8), multiply(power(a, 2), power(p, 4)), one_at
    )
    denominator_square_root = add(
        power(p, 4), multiply(a, power(p, 2)), one_at
    )
    if normalized_denominator != power(denominator_square_root, 2):
        raise AssertionError("D(a,p) is not the claimed characteristic-two square")
    if substitute_a_p_into_h_w(normalized_denominator) != power(denominator, 2):
        raise AssertionError("normalized denominator mismatch")

    # Repeat K with p in place of t.  The representation uses the same second
    # coordinate, so it is literally the same sparse polynomial.
    k_a_p = k_a_t
    normalized_numerator = multiply(p, k_a_p)
    if substitute_a_p_into_h_w(normalized_numerator) != direct_numerator_b:
        raise AssertionError("normalized image numerator mismatch")

    # Variables are now (a,t,p).  The cross intercept is
    # s=(1+a+a^2)t^2.  Membership s in B_c(F) is equivalent to L=0.
    a3 = variable(3, 0)
    t3 = variable(3, 1)
    p3 = variable(3, 2)
    one_atp = one(3)
    u3 = add(one_atp, a3, power(a3, 2))
    k_a_p3 = add(
        one_atp,
        multiply(add(one_atp, a3), p3),
        multiply(multiply(power(a3, 2), u3), power(p3, 3)),
        multiply(power(a3, 2), power(p3, 4)),
        multiply(power(a3, 2), power(p3, 7)),
        power(p3, 8),
        multiply(u3, power(p3, 9)),
    )
    denominator3 = add(
        power(p3, 8), multiply(power(a3, 2), power(p3, 4)), one_atp
    )
    special_intercept = multiply(u3, power(t3, 2))
    membership_curve = add(
        multiply(p3, k_a_p3),
        multiply(special_intercept, denominator3),
    )

    result = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0513-ZERO-ANCHOR-CURVE-NORMAL-FORM",
        "finite_field_samples_used": False,
        "direct_subiaco_numerator_identity": True,
        "dimension_free_change_of_variables": True,
        "denominator_square_identity": True,
        "denominator_nonzero_reason": (
            "D(a,p)=(p^4+a*p^2+1)^2; a zero would give "
            "y^2+y=a^-2 for y=p^2/a, contradicting "
            "Tr(a^-2)=Tr(a^-1)=1 for admissible a"
        ),
        "image_membership_cross_multiplication": True,
        "K_a_t": polynomial_payload(k_a_t, ("a", "t")),
        "D_a_p": polynomial_payload(normalized_denominator, ("a", "p")),
        "L_a_t_p": polynomial_payload(membership_curve, ("a", "t", "p")),
        "exact_equivalence": (
            "For admissible a and the unique t with K(a,t)=0, the zero-anchor "
            "cross intercept is external iff L(a,t,p)=0 has no field root p; "
            "the denominator is nonzero for every field element p."
        ),
        "remaining_general_target": (
            "prove that every even extension field contains an admissible "
            "a whose associated L-polynomial is root-free"
        ),
        "status": "PASS_EXACT_CURVE_NORMAL_FORM",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
