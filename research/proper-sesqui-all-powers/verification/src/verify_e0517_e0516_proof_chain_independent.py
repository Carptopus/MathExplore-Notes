"""Independent red-team checks for the new algebraic core of E0516.

This file intentionally does not import the E0516 constructor, verifier, or
finite-field helpers.  It checks the polynomial identities, smooth closed
points, local simple-pole branch, degree/genus bookkeeping, point-count
arithmetic, threshold, and the declared finite-basis boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


Monomial = tuple[int, int, int]  # exponents of a, t, p
SparsePolynomial = set[Monomial]


def toggle(target: SparsePolynomial, monomial: Monomial) -> None:
    if monomial in target:
        target.remove(monomial)
    else:
        target.add(monomial)


def product(left: SparsePolynomial, right: SparsePolynomial) -> SparsePolynomial:
    result: SparsePolynomial = set()
    for x in left:
        for y in right:
            toggle(result, tuple(x[i] + y[i] for i in range(3)))
    return result


def derivative(value: SparsePolynomial, variable: int) -> SparsePolynomial:
    result: SparsePolynomial = set()
    for monomial in value:
        if monomial[variable] & 1:
            reduced = list(monomial)
            reduced[variable] -= 1
            toggle(result, tuple(reduced))
    return result


def k_polynomial() -> SparsePolynomial:
    # 1+(1+a)t+a^2(1+a+a^2)t^3+a^2t^4+a^2t^7+t^8+(1+a+a^2)t^9
    return {
        (0, 0, 0),
        (0, 1, 0),
        (1, 1, 0),
        (2, 3, 0),
        (3, 3, 0),
        (4, 3, 0),
        (2, 4, 0),
        (2, 7, 0),
        (0, 8, 0),
        (0, 9, 0),
        (1, 9, 0),
        (2, 9, 0),
    }


def l_polynomial() -> SparsePolynomial:
    # p K(a,p) + (1+a+a^2)t^2(p^8+a^2p^4+1)
    result: SparsePolynomial = set()
    for a_degree, t_degree, _ in k_polynomial():
        toggle(result, (a_degree, 0, t_degree + 1))
    u_value = {(0, 0, 0), (1, 0, 0), (2, 0, 0)}
    t_square = {(0, 2, 0)}
    d_value = {(0, 0, 8), (2, 0, 4), (0, 0, 0)}
    for monomial in product(product(u_value, t_square), d_value):
        toggle(result, monomial)
    return result


def gf2_degree(value: int) -> int:
    return value.bit_length() - 1


def gf2_remainder(dividend: int, divisor: int) -> int:
    while dividend and gf2_degree(dividend) >= gf2_degree(divisor):
        dividend ^= divisor << (gf2_degree(dividend) - gf2_degree(divisor))
    return dividend


def gf2_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, gf2_remainder(left, right)
    return left


def gf2_product_mod(left: int, right: int, modulus: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
    return gf2_remainder(result, modulus)


def gf2_power_mod(value: int, exponent: int, modulus: int) -> int:
    result = 1
    while exponent:
        if exponent & 1:
            result = gf2_product_mod(result, value, modulus)
        value = gf2_product_mod(value, value, modulus)
        exponent >>= 1
    return result


def irreducible_degree_ten(value: int) -> bool:
    x_value = 0b10
    if gf2_power_mod(x_value, 1 << 10, value) != x_value:
        return False
    return all(
        gf2_gcd(value, gf2_power_mod(x_value, 1 << degree, value) ^ x_value) == 1
        for degree in (2, 5)
    )


class SmallField:
    def __init__(self, degree: int, modulus: int) -> None:
        self.degree = degree
        self.modulus = modulus

    def multiply(self, left: int, right: int) -> int:
        return gf2_product_mod(left, right, self.modulus)

    def power(self, value: int, exponent: int) -> int:
        result = 1
        while exponent:
            if exponent & 1:
                result = self.multiply(result, value)
            value = self.multiply(value, value)
            exponent >>= 1
        return result


def evaluate(
    polynomial: SparsePolynomial,
    field: SmallField,
    a_value: int,
    t_value: int,
    p_value: int,
) -> int:
    result = 0
    for a_degree, t_degree, p_degree in polynomial:
        term = field.multiply(
            field.power(a_value, a_degree), field.power(t_value, t_degree)
        )
        term = field.multiply(term, field.power(p_value, p_degree))
        result ^= term
    return result


def specialize_to_p(polynomial: SparsePolynomial, a_value: int, t_value: int) -> int:
    result = 0
    for a_degree, t_degree, p_degree in polynomial:
        coefficient = (a_value**a_degree) * (t_value**t_degree)
        if coefficient & 1:
            result ^= 1 << p_degree
    return result


def translate_t_by_one(polynomial: SparsePolynomial) -> set[tuple[int, int]]:
    """Return K(a,1+s) as an F2 support in (a,s)."""
    result: set[tuple[int, int]] = set()
    for a_degree, t_degree, _ in polynomial:
        for s_degree in range(t_degree + 1):
            # Lucas in base two: binomial(t_degree,s_degree) is odd iff
            # every one-bit of s_degree occurs in t_degree.
            if s_degree & ~t_degree:
                continue
            term = (a_degree, s_degree)
            if term in result:
                result.remove(term)
            else:
                result.add(term)
    return result


def check_local_algebra() -> dict[str, object]:
    k_value = k_polynomial()
    l_value = l_polynomial()
    d_value = {(0, 0, 0), (2, 0, 4), (0, 0, 8)}
    if derivative(l_value, 2) != d_value:
        raise AssertionError("formal derivative dL/dp does not equal D(a,p)")
    f10 = specialize_to_p(l_value, 1, 1)
    expected_f10 = sum(1 << degree for degree in (0, 1, 5, 9, 10))
    if f10 != expected_f10 or not irreducible_degree_ten(f10):
        raise AssertionError("degree-ten specialization failed")

    # Q=(1,1) is smooth on C because K_t(Q)=1.
    field2 = SmallField(1, 0b11)
    k_at_q = evaluate(k_value, field2, 1, 1, 0)
    kt_at_q = evaluate(derivative(k_value, 1), field2, 1, 1, 0)
    if k_at_q != 0 or kt_at_q != 1:
        raise AssertionError("Q is not the asserted smooth base point")

    f10_derivative = sum(1 << (degree - 1) for degree in (1, 5, 9))
    if gf2_gcd(f10, f10_derivative) != 1:
        raise AssertionError("degree-ten closed point is not separable")

    field8 = SmallField(3, 0b1011)
    alpha = 0b010
    cubic_point = (alpha, alpha ^ 1, 1)
    if evaluate(k_value, field8, *cubic_point) != 0:
        raise AssertionError("cubic point misses K")
    if evaluate(l_value, field8, *cubic_point) != 0:
        raise AssertionError("cubic point misses L")
    gradient_k = tuple(
        evaluate(derivative(k_value, index), field8, *cubic_point)
        for index in range(3)
    )
    gradient_l = tuple(
        evaluate(derivative(l_value, index), field8, *cubic_point)
        for index in range(3)
    )
    # grad K has t-coordinate 1 and grad L has nonzero p-coordinate.
    if gradient_k[1] != 1 or gradient_l[2] == 0:
        raise AssertionError("cubic closed point is not a smooth intersection")

    translated = translate_t_by_one(k_value)
    minimum_degree = min(sum(term) for term in translated)
    initial_form = {term for term in translated if sum(term) == minimum_degree}
    if minimum_degree != 3 or initial_form != {(2, 1), (3, 0)}:
        raise AssertionError("unexpected local branch at a=0,t=1")

    l_zero_one = specialize_to_p(l_value, 0, 1)
    expected_l_zero_one = sum(1 << degree for degree in (0, 1, 2, 8, 9, 10))
    factorization = gf2_product_mod((1 << 8) ^ 1, 0b111, 1 << 32)
    if l_zero_one != expected_l_zero_one or factorization != l_zero_one:
        raise AssertionError("simple-pole specialization factorization failed")
    field4 = SmallField(2, 0b111)
    omega = 0b10
    lp_at_omega = evaluate(derivative(l_value, 2), field4, 0, 1, omega)
    if lp_at_omega == 0:
        raise AssertionError("omega branch is ramified")

    return {
        "K_total_degree": max(sum(term) for term in k_value),
        "L_total_degree": max(sum(term) for term in l_value),
        "Q_smooth": True,
        "degree_ten_specialization_irreducible": True,
        "degree_ten_closed_point_smooth": True,
        "cubic_closed_point": list(cubic_point),
        "cubic_gradients": [list(gradient_k), list(gradient_l)],
        "cubic_closed_point_smooth": True,
        "closed_point_degree_gcd": 1,
        "base_local_initial_form": "a^2(s+a)",
        "incidence_simple_lift_derivative": lp_at_omega,
        "inverse_a_pole_order_on_incidence_curve": 1,
        "dL_dp_equals_D": True,
        "L_degree_in_p_on_admissible_locus": 10,
    }


def check_counting_arithmetic() -> dict[str, object]:
    genus_c = (11 - 1) * (11 - 2) // 2
    degree_a_c = 9
    genus_yc = 2 * genus_c - 1 + degree_a_c
    degree_x = 11 * 12
    genus_x = (degree_x - 1) * (degree_x - 2) // 2
    degree_a_x = 10 * degree_a_c
    genus_yx = 2 * genus_x - 1 + degree_a_x
    boundary_c = degree_a_c + degree_a_c + 2 * degree_a_c
    boundary_x = 10 * boundary_c
    boundary_yx = 2 * boundary_x
    base_error = 2 * genus_c + genus_yc
    incidence_error = 2 * genus_x + genus_yx
    combined_error = base_error + incidence_error / 2
    # On the admissible open curve, #trace-one = #base - #AS-cover/2.
    # For the lower bound on A_q only the deleted base boundary is lost;
    # the cover is used with an upper Hasse--Weil bound and needs no second
    # boundary deduction.  For the upper bound on T_q, half of the deleted
    # cover boundary is added back.
    admissible_constant_loss = boundary_c
    bad_triple_constant_gain = boundary_yx // 2
    base_singular_points = genus_c
    base_total_delta = genus_c
    base_normalization_collision_loss = base_total_delta
    incidence_degree_over_base = 10
    incidence_rational_singular_points = incidence_degree_over_base * base_singular_points
    constant_loss = (
        admissible_constant_loss
        + base_normalization_collision_loss
        + (bad_triple_constant_gain + incidence_rational_singular_points) / 2
    )

    def four_times_lower_bound(degree: int) -> int:
        q_value = 1 << degree
        root_q = 1 << (degree // 2)
        return q_value + 1 - int(4 * combined_error) * root_q - int(4 * constant_loss)

    if four_times_lower_bound(32) >= 0:
        raise AssertionError("d=32 should not be closed by the conservative bound")
    if four_times_lower_bound(34) <= 0:
        raise AssertionError("d=34 should be closed by the conservative bound")
    previous = four_times_lower_bound(34)
    for degree in range(36, 130, 2):
        current = four_times_lower_bound(degree)
        if current <= 0 or current <= previous:
            raise AssertionError("the even-degree tail is not monotonically positive")
        previous = current

    return {
        "genus_C_upper": genus_c,
        "degree_a_on_C_upper": degree_a_c,
        "genus_trace_cover_C_upper": genus_yc,
        "degree_X_upper": degree_x,
        "genus_X_upper": genus_x,
        "degree_a_on_X_upper": degree_a_x,
        "genus_trace_cover_X_upper": genus_yx,
        "boundary_C_upper": boundary_c,
        "boundary_X_upper": boundary_x,
        "boundary_trace_cover_X_upper": boundary_yx,
        "admissible_error_coefficient": base_error,
        "bad_triple_error_coefficient": incidence_error,
        "admissible_constant_loss": admissible_constant_loss,
        "bad_triple_constant_gain": bad_triple_constant_gain,
        "base_singular_point_upper": base_singular_points,
        "base_total_delta_upper": base_total_delta,
        "base_normalization_collision_loss": base_normalization_collision_loss,
        "incidence_degree_over_base": incidence_degree_over_base,
        "incidence_rational_singular_point_upper": incidence_rational_singular_points,
        "good_parameter_error_coefficient": combined_error,
        "good_parameter_constant_loss": constant_loss,
        "good_parameter_lower_bound": "(q+1)/4 - 17262.5*sqrt(q) - 486",
        "four_times_lower_bound_d32": four_times_lower_bound(32),
        "four_times_lower_bound_d34": four_times_lower_bound(34),
        "trace_count_identity": "N_trace1(Z_open)=#Z_open-#Y_Z_open/2",
        "first_even_degree_closed_by_bound": 34,
        "tail_monotonicity_checked_through": 128,
    }


def check_finite_basis(source: Path) -> dict[str, object]:
    data = json.loads(source.read_text(encoding="utf-8"))
    expected = list(range(4, 34, 2))
    degrees = [int(item["degree"]) for item in data["witnesses"]]
    if data["basis_degrees"] != expected or degrees != expected:
        raise AssertionError("finite basis is not exactly the Weil-bound complement")
    maximum_trials = max(int(item["trials"]) for item in data["witnesses"])
    if data.get("maximum_parameter_trials") != maximum_trials:
        raise AssertionError("finite-basis search disclosure is inconsistent")
    if not data.get("parameter_search_used"):
        raise AssertionError("parameter search must be disclosed")
    if data.get("exhaustive_field_enumeration_used"):
        raise AssertionError("unexpected exhaustive field enumeration claim")
    return {
        "degrees": expected,
        "count": len(expected),
        "maximum_parameter_trials": maximum_trials,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "exact_complement_of_general_tail": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("finite_basis", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "research_id": "RESEARCH-HSF-0001",
        "experiment_id": "HSF-E0517-E0516-PROOF-CHAIN-REDTEAM",
        "independence": "standard-library-only; imports no E0516 or project algebra code",
        "local_algebra": check_local_algebra(),
        "counting_arithmetic": check_counting_arithmetic(),
        "finite_basis_boundary": check_finite_basis(args.finite_basis),
        "proof_logic_not_mechanically_decided": [
            "monic specialization over a DVR implies generic irreducibility",
            "coprime smooth closed-point degrees force exact constant field F_2",
            "simple odd pole excludes an Artin-Schreier coboundary after base change",
            "the universal genus-versus-projective-degree bound uses Castelnuovo's bound only through the weaker plane-form estimate",
            "normalization is an isomorphism over the smooth locus and the total branch-collision loss is bounded by the plane-curve delta sum",
            "on the admissible rational locus dL/dp=D(a,p) is nonzero, so singular incidence triples can lie only above singular base pairs",
        ],
        "status": "PASS_E0517_INDEPENDENT_ALGEBRA_AND_COUNTING_REDTEAM",
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
