"""Discovery probe for aggregate Walsh states of small quadratic atoms.

This program is not a proof of the all-dimensional spectrum.  It checks whether
the fixed five-variable slice construction from the previous case, followed by
all two-variable vectorial quadratic atoms under orthogonal direct sum, produces
the central aggregate states suggested by the n=6 and n=8 exact spectra.

The seven signature coordinates are ordered by the nonzero binary parameters
1,...,7.  In dimension 2m they are W_(a.F)(0)/2^m; in dimension 2m+1 they are
W_(a.F)(0)/2^(m+1).
"""

from __future__ import annotations

from functools import lru_cache


QuadraticTerms = list[tuple[int, int]]
Signature = tuple[int, int, int, int, int, int, int]


def pairs(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def polynomial_from_terms(n: int, terms: QuadraticTerms, affine: int = 0) -> int:
    """Encode constant, linear, then square-free quadratic coefficients."""
    value = affine
    positions = {pair: 1 + n + k for k, pair in enumerate(pairs(n))}
    for pair in terms:
        value ^= 1 << positions[tuple(sorted(pair))]
    return value


@lru_cache(maxsize=None)
def walsh_zero(n: int, polynomial: int) -> int:
    result = 0
    quadratic_pairs = pairs(n)
    for x in range(1 << n):
        bit = polynomial & 1
        for i in range(n):
            bit ^= ((polynomial >> (1 + i)) & 1) & ((x >> i) & 1)
        for k, (i, j) in enumerate(quadratic_pairs):
            bit ^= (
                ((polynomial >> (1 + n + k)) & 1)
                & ((x >> i) & 1)
                & ((x >> j) & 1)
            )
        result += -1 if bit else 1
    return result


def signature(n: int, components: tuple[int, int, int]) -> Signature:
    denominator = 1 << ((n + 1) // 2)
    values = []
    for parameter in range(1, 8):
        polynomial = 0
        for component in range(3):
            if (parameter >> component) & 1:
                polynomial ^= components[component]
        values.append(walsh_zero(n, polynomial) // denominator)
    return tuple(values)  # type: ignore[return-value]


def components_independent_mod_constants(components: tuple[int, int, int]) -> bool:
    for parameter in range(1, 8):
        polynomial = 0
        for component in range(3):
            if (parameter >> component) & 1:
                polynomial ^= components[component]
        if polynomial >> 1 == 0:
            return False
    return True


def all_two_variable_signatures() -> set[Signature]:
    coefficient_dimension = 1 + 2 + 1
    normalized = [
        walsh_zero(2, polynomial) // 2
        for polynomial in range(1 << coefficient_dimension)
    ]
    result: set[Signature] = set()
    for first in range(1 << coefficient_dimension):
        for second in range(1 << coefficient_dimension):
            for third in range(1 << coefficient_dimension):
                result.add(
                    (
                        normalized[first],
                        normalized[second],
                        normalized[first ^ second],
                        normalized[third],
                        normalized[first ^ third],
                        normalized[second ^ third],
                        normalized[first ^ second ^ third],
                    )
                )
    return result


NET5: list[QuadraticTerms] = [
    [(0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
]


def five_variable_affine_representatives() -> dict[int, tuple[int, int, int]]:
    bases = [polynomial_from_terms(5, terms) for terms in NET5]
    representatives: dict[int, tuple[int, int, int]] = {}
    for first in range(1 << 6):
        for second in range(1 << 6):
            for third in range(1 << 6):
                affine = (first, second, third)
                components = tuple(bases[i] ^ affine[i] for i in range(3))
                aggregate = sum(signature(5, components))
                support = 28 - aggregate
                representatives.setdefault(support, affine)
    return representatives


def sliced_component(terms: QuadraticTerms, first_affine: int, second_affine: int) -> int:
    """Return A(x)+t(A(x)+B(x)) on x0,...,x4,t=x5."""
    result = polynomial_from_terms(6, terms, first_affine)
    difference = first_affine ^ second_affine
    if difference & 1:
        result ^= 1 << (1 + 5)
    positions = {pair: 1 + 6 + k for k, pair in enumerate(pairs(6))}
    for i in range(5):
        if (difference >> (1 + i)) & 1:
            result ^= 1 << positions[(i, 5)]
    return result


def six_variable_slice_states() -> set[Signature]:
    representatives = five_variable_affine_representatives()
    result: set[Signature] = set()
    for first in representatives.values():
        for second in representatives.values():
            components = tuple(
                sliced_component(NET5[i], first[i], second[i]) for i in range(3)
            )
            if components_independent_mod_constants(components):
                result.add(signature(6, components))
    return result


def exceptional_six_variable_states() -> set[Signature]:
    """The sharp d3 state and the half-support state, lifted to six variables."""
    minimum_components = (
        polynomial_from_terms(6, [(0, 1)]),
        polynomial_from_terms(6, [(0, 2)]),
        polynomial_from_terms(6, [(0, 3)]),
    )
    half_components = (
        1 << (1 + 0),
        polynomial_from_terms(6, [(0, 1)]),
        polynomial_from_terms(6, [(0, 2)]),
    )
    assert components_independent_mod_constants(minimum_components)
    assert components_independent_mod_constants(half_components)
    return {signature(6, minimum_components), signature(6, half_components)}


def direct_sum(states: set[Signature], atoms: set[Signature]) -> set[Signature]:
    return {
        tuple(left * right for left, right in zip(state, atom))  # type: ignore[misc]
        for state in states
        for atom in atoms
    }


def main() -> None:
    representatives = five_variable_affine_representatives()
    expected_orbit = {17, *range(19, 33)}
    assert set(representatives) == expected_orbit

    atoms2 = all_two_variable_signatures()
    assert len(atoms2) == 330

    states6 = six_variable_slice_states() | exceptional_six_variable_states()
    aggregates6 = {sum(state) for state in states6}
    expected_slice_aggregates6 = {22, *range(-8, 21)}
    assert expected_slice_aggregates6 <= aggregates6

    states8 = direct_sum(states6, atoms2)
    aggregates8 = {sum(state) for state in states8}
    exact_aggregates8 = {
        -16,
        *range(-14, 30),
        30,
        32,
        34,
        36,
        38,
        40,
        44,
        48,
        56,
    }

    assert not (exact_aggregates8 - aggregates8)
    assert not (aggregates8 - exact_aggregates8)

    states10 = direct_sum(states8, atoms2)
    aggregates10 = {sum(state) for state in states10}
    predicted10 = (
        {2 * aggregate for aggregate in exact_aggregates8}
        | set(range(-27, 54, 2))
    )
    residual10 = predicted10 - aggregates10
    assert residual10 == {-27, 51, 53}
    assert not (aggregates10 - predicted10)

    print(f"five-variable representatives: {len(representatives)}")
    print(f"two-variable atom signatures: {len(atoms2)}")
    print(f"six-variable slice signatures: {len(states6)}")
    print(f"six-variable aggregate K: {sorted(aggregates6)}")
    print(f"eight-variable direct-sum signatures: {len(states8)}")
    print(f"eight-variable aggregate K: {sorted(aggregates8)}")
    print(
        "exact K_4 missed by this restricted atom library:",
        sorted(exact_aggregates8 - aggregates8),
    )
    print(
        "extra K beyond the exact K_4 spectrum (negative control):",
        sorted(aggregates8 - exact_aggregates8),
    )
    print(f"ten-variable direct-sum signatures: {len(states10)}")
    print(f"ten-variable aggregate K: {sorted(aggregates10)}")
    print("three residual K values in the proposed K_5 layer:", sorted(residual10))

    # Destructive control: a single damaged NET5 term must change the orbit.
    damaged = [terms.copy() for terms in NET5]
    damaged[0].pop()
    original = NET5[0]
    try:
        NET5[0] = damaged[0]
        assert set(five_variable_affine_representatives()) != expected_orbit
    finally:
        NET5[0] = original


if __name__ == "__main__":
    main()
