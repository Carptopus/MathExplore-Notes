"""Verify the E0514 parameter curve and its Artin--Schreier linearization."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from verify_e0513_zero_anchor_curve_normal_form import (
    Polynomial,
    add,
    multiply,
    one,
    power,
    variable,
)
from verify_zero_anchor_multiplier_resultants import (
    is_irreducible,
    resultant,
    trace_inverse_square,
)


def payload(value: Polynomial, variables: tuple[str, ...]) -> dict[str, object]:
    terms = [list(term) for term in sorted(value)]
    encoded = json.dumps(terms, separators=(",", ":")).encode("ascii")
    return {
        "variables": list(variables),
        "term_count": len(terms),
        "degrees": [max(term[index] for term in terms) for index in range(len(variables))],
        "total_degree": max(sum(term) for term in terms),
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def substitute_t_plus_one(value: Polynomial) -> Polynomial:
    """Substitute t=1+s in a polynomial in (a,t)."""

    a = variable(2, 0)
    s = variable(2, 1)
    result: Polynomial = frozenset()
    for a_degree, t_degree in value:
        result = add(
            result,
            multiply(power(a, a_degree), power(add(one(2), s), t_degree)),
        )
    return result


def substitute_z(value: Polynomial) -> Polynomial:
    """Substitute z=a^2+a in a polynomial in (z,t)."""

    a = variable(2, 0)
    t = variable(2, 1)
    z_value = add(a, power(a, 2))
    result: Polynomial = frozenset()
    for z_degree, t_degree in value:
        result = add(
            result,
            multiply(power(z_value, z_degree), power(t, t_degree)),
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # K(a,t) from E0513.
    a = variable(2, 0)
    t = variable(2, 1)
    one_at = one(2)
    u = add(one_at, a, power(a, 2))
    k = add(
        one_at,
        multiply(add(one_at, a), t),
        multiply(multiply(power(a, 2), u), power(t, 3)),
        multiply(power(a, 2), power(t, 4)),
        multiply(power(a, 2), power(t, 7)),
        power(t, 8),
        multiply(u, power(t, 9)),
    )

    # The t-adic Newton polygon when K is regarded as a polynomial in a.
    valuations: dict[int, int] = {}
    for a_degree, t_degree in k:
        valuations[a_degree] = min(valuations.get(a_degree, sys.maxsize), t_degree)
    expected_valuations = {0: 0, 1: 1, 2: 3, 3: 3, 4: 3}
    if valuations != expected_valuations:
        raise AssertionError("unexpected t-adic coefficient valuations")
    if not all(4 * valuations[index] > 3 * index for index in (1, 2, 3)):
        raise AssertionError("Newton polygon has an unexpected lower point")

    # At (a,t)=(0,1), the lowest total-degree form is a^2(a+s).
    local = substitute_t_plus_one(k)
    minimum_total_degree = min(sum(term) for term in local)
    initial_form = frozenset(term for term in local if sum(term) == minimum_total_degree)
    expected_initial_form = frozenset({(2, 1), (3, 0)})
    if minimum_total_degree != 3 or initial_form != expected_initial_form:
        raise AssertionError("unexpected local initial form at (0,1)")

    # Write z=a^2+a.  Then K=A(z,t)+aB(z,t) is linear in a.
    z = variable(2, 0)
    tz = variable(2, 1)
    one_zt = one(2)

    def c0(x: Polynomial) -> Polynomial:
        return power(add(one_zt, x), 9)

    def c1(x: Polynomial) -> Polynomial:
        return add(x, power(x, 9))

    def c2(x: Polynomial) -> Polynomial:
        return add(power(x, 3), power(x, 4), power(x, 7), power(x, 9))

    a_part = add(
        c0(tz),
        multiply(z, c2(tz)),
        multiply(power(z, 2), power(tz, 3)),
    )
    b_part = add(
        tz,
        power(tz, 3),
        power(tz, 4),
        power(tz, 7),
        multiply(z, power(tz, 3)),
    )
    reconstructed_k = add(
        substitute_z(a_part),
        multiply(a, substitute_z(b_part)),
    )
    if reconstructed_k != k:
        raise AssertionError("K=A+aB linearization failed")

    r_curve = add(
        power(a_part, 2),
        multiply(a_part, b_part),
        multiply(z, power(b_part, 2)),
    )

    # A and B can vanish together only over the stated exceptional z-values.
    # The resultant implementation represents F_2[z] polynomials as bitsets.
    a_coefficients = [0] * 10
    for degree in (0, 1, 8, 9):
        a_coefficients[degree] ^= 1
    for degree in (3, 4, 7, 9):
        a_coefficients[degree] ^= 0b10
    a_coefficients[3] ^= 0b100
    b_coefficients = [0] * 8
    for degree in (1, 3, 4, 7):
        b_coefficients[degree] ^= 1
    b_coefficients[3] ^= 0b10
    common_zero_resultant = resultant(a_coefficients, b_coefficients)
    expected_resultant = (1 << 11) ^ (1 << 13) ^ (1 << 14)
    if common_zero_resultant != expected_resultant:
        raise AssertionError("Res_t(A,B) mismatch")

    # The degree-six polynomial obtained from z^3+z^2+1 after z=a^2+a.
    exceptional_a = add(
        power(add(a, power(a, 2)), 3),
        power(add(a, power(a, 2)), 2),
        one_at,
    )
    expected_exceptional_a = frozenset({(0, 0), (2, 0), (3, 0), (5, 0), (6, 0)})
    if exceptional_a != expected_exceptional_a:
        raise AssertionError("exceptional degree-six polynomial mismatch")
    exceptional_a_bits = sum(1 << exponent for exponent in (0, 2, 3, 5, 6))
    if not is_irreducible(exceptional_a_bits):
        raise AssertionError("exceptional degree-six polynomial is reducible")
    if trace_inverse_square(exceptional_a_bits) != 0:
        raise AssertionError("exceptional inverse trace is not zero")

    # Build the determinant form of the bad incidence equation in (z,t,p).
    z3 = variable(3, 0)
    t3 = variable(3, 1)
    p3 = variable(3, 2)
    one_ztp = one(3)

    def c0_3(x: Polynomial) -> Polynomial:
        return power(add(one_ztp, x), 9)

    def c2_3(x: Polynomial) -> Polynomial:
        return add(power(x, 3), power(x, 4), power(x, 7), power(x, 9))

    def a_form(x: Polynomial) -> Polynomial:
        return add(
            c0_3(x),
            multiply(z3, c2_3(x)),
            multiply(power(z3, 2), power(x, 3)),
        )

    def b_form(x: Polynomial) -> Polynomial:
        return add(
            x,
            power(x, 3),
            power(x, 4),
            power(x, 7),
            multiply(z3, power(x, 3)),
        )

    a_t = a_form(t3)
    b_t = b_form(t3)
    a_p = a_form(p3)
    b_p = b_form(p3)
    d_zero = add(one_ztp, power(p3, 8), multiply(z3, power(p3, 4)))
    l_a = add(
        multiply(p3, a_p),
        multiply(multiply(add(one_ztp, z3), power(t3, 2)), d_zero),
    )
    l_b = add(
        multiply(p3, b_p),
        multiply(
            multiply(add(one_ztp, z3), power(t3, 2)),
            power(p3, 4),
        ),
    )
    incidence = add(multiply(a_t, l_b), multiply(b_t, l_a))

    result = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0514-PARAMETER-CURVE-AND-LINEARIZATION",
        "finite_field_samples_used": False,
        "newton_polygon": {
            "coefficient_valuations": valuations,
            "single_edge": [[0, 0], [4, 3]],
            "coprime_edge_vector": True,
        },
        "local_branch": {
            "point": [0, 1],
            "initial_form": "a^2(a+s)",
            "simple_a_zero_branch": True,
        },
        "K_linearization": True,
        "A_B_common_zero_resultant_exponents": [11, 13, 14],
        "exceptional_a_polynomial_exponents": [0, 2, 3, 5, 6],
        "exceptional_a_polynomial_irreducible": True,
        "exceptional_inverse_trace": 0,
        "R_z_t": payload(r_curve, ("z", "t")),
        "H_z_t_p": payload(incidence, ("z", "t", "p")),
        "conclusion": (
            "K is geometrically irreducible; its trace Artin-Schreier cover "
            "is geometrically irreducible; and the bad-incidence condition "
            "reduces birationally to R(z,t)=H(z,t,p)=0 on the admissible open set."
        ),
        "remaining_general_target": (
            "prove geometric irreducibility and obtain a Weil bound for the "
            "bad-incidence curve R=H=0, or derive a stronger explicit trace criterion"
        ),
        "status": "PASS_GENERAL_PARAMETER_CURVE_REDUCTION",
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
