"""Zero-trust finite-field audit for the general Paley switching theorem.

This implementation imports no HSF constructor or previous switching verifier.
It builds prime and extension fields from polynomial arithmetic, re-enumerates
the character conditions, checks the elliptic-curve point count identity, and
reconstructs complete arrays directly from the definition for selected fields.

Finite computations audit formulas and boundary handling; they do not replace
the Hasse proof for the infinite family or establish literature novelty.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from itertools import product
from pathlib import Path


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def divisible_by_monic(poly: tuple[int, ...], divisor: tuple[int, ...], p: int) -> bool:
    remainder = list(poly)
    degree = len(divisor) - 1
    for index in range(len(remainder) - 1, degree - 1, -1):
        coefficient = remainder[index] % p
        if coefficient == 0:
            continue
        shift = index - degree
        for offset, value in enumerate(divisor):
            remainder[shift + offset] = (
                remainder[shift + offset] - coefficient * value
            ) % p
    return all(value % p == 0 for value in remainder[:degree])


def first_irreducible_monic(p: int, degree: int) -> tuple[int, ...]:
    if degree == 1:
        return (0, 1)
    for lower in product(range(p), repeat=degree):
        if lower[0] == 0:
            continue
        candidate = tuple(lower) + (1,)
        reducible = False
        for factor_degree in range(1, degree // 2 + 1):
            for factor_lower in product(range(p), repeat=factor_degree):
                divisor = tuple(factor_lower) + (1,)
                if divisible_by_monic(candidate, divisor, p):
                    reducible = True
                    break
            if reducible:
                break
        if not reducible:
            return candidate
    raise RuntimeError(f"no irreducible polynomial found over GF({p}) degree {degree}")


@dataclass(frozen=True)
class FiniteField:
    p: int
    degree: int
    modulus: tuple[int, ...]

    @property
    def order(self) -> int:
        return self.p**self.degree

    def digits(self, value: int) -> list[int]:
        result = []
        for _ in range(self.degree):
            result.append(value % self.p)
            value //= self.p
        return result

    def encode(self, coefficients: list[int]) -> int:
        result = 0
        multiplier = 1
        for coefficient in coefficients[: self.degree]:
            result += (coefficient % self.p) * multiplier
            multiplier *= self.p
        return result

    def add(self, left: int, right: int) -> int:
        return self.encode(
            [a + b for a, b in zip(self.digits(left), self.digits(right))]
        )

    def neg(self, value: int) -> int:
        return self.encode([-coefficient for coefficient in self.digits(value)])

    def sub(self, left: int, right: int) -> int:
        return self.add(left, self.neg(right))

    def mul(self, left: int, right: int) -> int:
        a = self.digits(left)
        b = self.digits(right)
        coefficients = [0] * (2 * self.degree - 1)
        for i, left_coefficient in enumerate(a):
            for j, right_coefficient in enumerate(b):
                coefficients[i + j] = (
                    coefficients[i + j] + left_coefficient * right_coefficient
                ) % self.p
        for index in range(len(coefficients) - 1, self.degree - 1, -1):
            coefficient = coefficients[index] % self.p
            if coefficient == 0:
                continue
            shift = index - self.degree
            for offset in range(self.degree):
                coefficients[shift + offset] = (
                    coefficients[shift + offset]
                    - coefficient * self.modulus[offset]
                ) % self.p
            coefficients[index] = 0
        return self.encode(coefficients[: self.degree])

    def pow(self, value: int, exponent: int) -> int:
        result = 1
        base = value
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            exponent >>= 1
        return result

    def inv(self, value: int) -> int:
        if value == 0:
            raise ZeroDivisionError
        return self.pow(value, self.order - 2)

    def chi(self, value: int) -> int:
        if value == 0:
            return 0
        result = self.pow(value, (self.order - 1) // 2)
        if result == 1:
            return 1
        if result == self.neg(1):
            return -1
        raise AssertionError("Euler criterion did not return +/-1")

    def integer(self, value: int) -> int:
        result = 0
        for _ in range(value):
            result = self.add(result, 1)
        return result


def make_field(p: int, degree: int) -> FiniteField:
    return FiniteField(p, degree, first_irreducible_monic(p, degree))


def audit_field_axioms(field: FiniteField) -> None:
    q = field.order
    if field.mul(1, 1) != 1 or field.add(1, field.neg(1)) != 0:
        raise AssertionError("identity failure")
    for value in range(1, q):
        if field.mul(value, field.inv(value)) != 1:
            raise AssertionError("inverse failure")
    sample = sorted({0, 1, 2 % q, q // 3, q // 2, q - 1})
    for left in sample:
        for middle in sample:
            for right in sample:
                if field.mul(left, field.add(middle, right)) != field.add(
                    field.mul(left, middle), field.mul(left, right)
                ):
                    raise AssertionError("distributivity failure")


def alpha_set(field: FiniteField) -> list[int]:
    return [
        alpha
        for alpha in range(field.order)
        if field.chi(alpha) == -1 and field.chi(field.add(1, alpha)) == -1
    ]


def admissible_ratios(field: FiniteField, alpha: int) -> list[int]:
    return [
        ratio
        for ratio in range(field.order)
        if field.chi(ratio) == 1
        and field.chi(field.add(1, field.mul(alpha, ratio))) == 1
        and field.chi(field.add(ratio, alpha)) == 1
    ]


def cubic_sum(field: FiniteField, alpha: int) -> int:
    total = 0
    for ratio in range(field.order):
        value = field.mul(
            ratio,
            field.mul(
                field.add(1, field.mul(alpha, ratio)),
                field.add(ratio, alpha),
            ),
        )
        total += field.chi(value)
    return total


def switched_partner(field: FiniteField, alpha: int, ratio: int) -> list[int]:
    partner = [0] * field.order
    for value in range(1, field.order):
        if field.chi(value) == 1:
            other = field.mul(alpha, value)
            partner[value] = other
            partner[other] = value
    one_alpha = alpha
    ratio_alpha = field.mul(alpha, ratio)
    if partner[1] != one_alpha or partner[ratio] != ratio_alpha:
        raise AssertionError("baseline edges absent")
    partner[1] = ratio_alpha
    partner[ratio_alpha] = 1
    partner[ratio] = one_alpha
    partner[one_alpha] = ratio
    if any(partner[partner[value]] != value for value in range(field.order)):
        raise AssertionError("switched partner is not an involution")
    return partner


def field_sum(field: FiniteField, values: set[int]) -> int:
    result = 0
    for value in values:
        result = field.add(result, value)
    return result


def moment_defect(field: FiniteField, block: set[int]) -> int:
    first = field_sum(field, block)
    second = 0
    # Accumulate with multiplicity: a set of squares would merge +/- pairs.
    for value in block:
        second = field.add(second, field.mul(value, value))
    return field.sub(
        field.mul(field.integer(len(block)), second), field.mul(first, first)
    )


def audit_switch(field: FiniteField, alpha: int, ratio: int) -> dict[str, object]:
    partner = switched_partner(field, alpha, ratio)
    fibres: dict[int, list[int]] = {}
    for value in range(field.order):
        edge_sum = field.add(value, partner[value])
        fibres.setdefault(edge_sum, []).append(value)
    expected_sizes = [1] + [2] * ((field.order - 1) // 2)
    if sorted(map(len, fibres.values())) != expected_sizes or fibres.get(0) != [0]:
        raise AssertionError("wrong sum-fibre profile")
    for edge_sum, fibre in fibres.items():
        if edge_sum and sorted(field.chi(value) for value in fibre) != [-1, 1]:
            raise AssertionError("nonzero fibre does not cross square classes")

    block = set(fibres)
    defect = moment_defect(field, block)
    predicted = field.neg(
        field.mul(alpha, field.mul(field.sub(ratio, 1), field.sub(ratio, 1)))
    )
    if defect != predicted or defect == 0:
        raise AssertionError("moment defect mismatch")

    difference_counts = []
    for shift in range(1, field.order):
        difference_counts.append(
            sum(field.sub(left, right) == shift for left in block for right in block)
        )
    if len(set(difference_counts)) == 1:
        raise AssertionError("switched block remained a difference set")
    return {
        "alpha": alpha,
        "ratio": ratio,
        "block_size": len(block),
        "moment_defect": defect,
        "difference_multiplicities": sorted(set(difference_counts)),
        "partner": partner,
        "block": sorted(block),
    }


def audit_complete_array(
    field: FiniteField, alpha: int, ratio: int, corrupt_infinity: bool = False
) -> dict[str, object]:
    q = field.order
    partner = switched_partner(field, alpha, ratio)
    rows: list[list[tuple[int, int]]] = []
    for shift in range(q):
        row = []
        for column in range(q):
            base = field.sub(column, shift)
            symbol = field.add(field.add(base, partner[base]), shift)
            label = 0 if field.chi(partner[base]) == 1 else 1
            row.append((symbol, label))
        row.append((shift, 1 if corrupt_infinity and shift == 0 else 0))
        rows.append(row)
    if any(len(set(row)) != q + 1 for row in rows):
        raise AssertionError("row binary failure")
    columns = [[rows[row][column] for row in range(q)] for column in range(q + 1)]
    if any(len(set(column)) != q for column in columns):
        raise AssertionError("column binary failure")
    occurrences = Counter(symbol for row in rows for symbol in row)
    if len(occurrences) != 2 * q or set(occurrences.values()) != {(q + 1) // 2}:
        raise AssertionError("replication failure")
    row_supports = list(map(set, rows))
    column_supports = list(map(set, columns))
    cc = {
        len(column_supports[left] & column_supports[right])
        for left in range(q + 1)
        for right in range(left + 1, q + 1)
    }
    rc = {
        len(row_supports[row] & column_supports[column])
        for row in range(q)
        for column in range(q + 1)
    }
    rr = Counter(
        len(row_supports[left] & row_supports[right])
        for left in range(q)
        for right in range(left + 1, q)
    )
    if cc != {(q - 1) // 2} or rc != {(q + 1) // 2} or len(rr) < 2:
        raise AssertionError("intersection audit failure")
    return {
        "v": 2 * q,
        "rows": q,
        "columns": q + 1,
        "replication": (q + 1) // 2,
        "cc": next(iter(cc)),
        "rc": next(iter(rc)),
        "rr_spectrum": dict(sorted(rr.items())),
    }


def audit_case(p: int, degree: int, full_array: bool) -> dict[str, object]:
    field = make_field(p, degree)
    audit_field_axioms(field)
    q = field.order
    alphas = alpha_set(field)
    if len(alphas) != (q - 3) // 4:
        raise AssertionError("alpha-count formula failed")
    alpha_records = []
    pairs: list[tuple[int, int]] = []
    for alpha in alphas:
        ratios = admissible_ratios(field, alpha)
        total = cubic_sum(field, alpha)
        correction = field.chi(field.sub(alpha, 1))
        numerator = q - 3 + total - 4 * correction
        if numerator % 8 or len(ratios) != numerator // 8:
            raise AssertionError("fixed-alpha count formula failed")
        if total * total > 4 * q:
            raise AssertionError("Hasse bound failed")
        alpha_records.append(
            {"alpha": alpha, "T_alpha": total, "C_alpha": len(ratios)}
        )
        pairs.extend((alpha, ratio) for ratio in ratios)
    if q >= 19 and alphas and min(item["C_alpha"] for item in alpha_records) == 0:
        raise AssertionError("positive Hasse threshold failed")

    switch_audit = None
    array_audit = None
    mutation_detected = None
    if pairs:
        alpha, ratio = pairs[0]
        switch_audit = audit_switch(field, alpha, ratio)
        if full_array:
            array_audit = audit_complete_array(field, alpha, ratio)
            try:
                audit_complete_array(field, alpha, ratio, corrupt_infinity=True)
            except AssertionError:
                mutation_detected = True
            else:
                mutation_detected = False
                raise AssertionError("controlled infinity-label corruption was not detected")
    return {
        "field": f"GF({p}^{degree})",
        "q": q,
        "modulus_low_to_high": list(field.modulus),
        "alpha_count": len(alphas),
        "pair_count": len(pairs),
        "minimum_C_alpha": min(
            (item["C_alpha"] for item in alpha_records), default=None
        ),
        "alpha_records": alpha_records,
        "switch_audit": {
            key: value
            for key, value in (switch_audit or {}).items()
            if key not in {"partner", "block"}
        }
        if switch_audit
        else None,
        "array_audit": array_audit,
        "controlled_mutation_detected": mutation_detected,
    }


def main() -> int:
    cases = [
        (3, 1, False),
        (7, 1, False),
        (11, 1, True),
        (19, 1, True),
        (3, 3, True),
        (3, 5, True),
        (7, 3, False),
    ]
    records = [audit_case(*case) for case in cases]
    payload = {
        "experiment_id": "HSF-AUDIT-0003-E01-GENERIC-FIELDS",
        "implementation_boundary": (
            "No prior HSF or switching module is imported. Extension fields are "
            "constructed from independently searched irreducible polynomials."
        ),
        "records": records,
        "checks": {
            "alpha_count": True,
            "fixed_alpha_count": True,
            "elliptic_point_count_hasse": True,
            "switch_and_moment_defect": True,
            "complete_array_selected_fields": True,
            "controlled_mutation": True,
        },
        "claim_boundary": (
            "Finite-field regression attacks implementation and boundary errors. "
            "The infinite conclusion still requires the written Hasse proof."
        ),
    }
    output = Path(__file__).resolve().parent / "results" / "audit-paley-switch-generic-fields.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
