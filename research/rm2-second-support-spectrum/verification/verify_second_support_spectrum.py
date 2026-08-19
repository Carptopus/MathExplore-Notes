"""Exact small-order support spectra of two-dimensional RM_2(2, n) subcodes."""

from __future__ import annotations

from itertools import combinations


def monomial_values(n: int) -> list[int]:
    """Return truth-table bitsets for 1, x_i, and x_i*x_j."""
    values: list[int] = []
    monomials = [()] + [(i,) for i in range(n)] + list(combinations(range(n), 2))
    for indices in monomials:
        word = 0
        for point in range(1 << n):
            value = 1
            for index in indices:
                value &= (point >> index) & 1
            word |= value << point
        values.append(word)
    return values


def rm2_words_bitset(n: int) -> list[int]:
    words = [0]
    for basis_word in monomial_values(n):
        words += [word ^ basis_word for word in words]
    return words


def evaluate_from_coefficients(n: int, coefficients: int) -> tuple[int, ...]:
    monomials = [()] + [(i,) for i in range(n)] + list(combinations(range(n), 2))
    truth_table = []
    for point in range(1 << n):
        value = 0
        for bit, indices in enumerate(monomials):
            if (coefficients >> bit) & 1:
                term = 1
                for index in indices:
                    term &= (point >> index) & 1
                value ^= term
        truth_table.append(value)
    return tuple(truth_table)


def spectrum_bitset(n: int) -> tuple[set[int], int, bool]:
    words = rm2_words_bitset(n)
    spectrum: set[int] = set()
    pair_count = 0
    broken_formula_detected = False
    for left_index in range(1, len(words)):
        left = words[left_index]
        for right_index in range(left_index + 1, len(words)):
            right = words[right_index]
            direct = (left | right).bit_count()
            by_three_weights = (
                left.bit_count() + right.bit_count() + (left ^ right).bit_count()
            ) // 2
            common_zeros = (1 << n) - direct
            if direct != by_three_weights:
                raise AssertionError((n, left_index, right_index, direct, by_three_weights))
            if common_zeros != ((~(left | right)) & ((1 << (1 << n)) - 1)).bit_count():
                raise AssertionError("common-zero route disagrees")
            if direct != (
                left.bit_count() + right.bit_count() + (left | right).bit_count()
            ) // 2:
                broken_formula_detected = True
            spectrum.add(direct)
            pair_count += 1
    return spectrum, pair_count, broken_formula_detected


def spectrum_truth_tables(n: int) -> set[int]:
    dimension = 1 + n + n * (n - 1) // 2
    tables = [evaluate_from_coefficients(n, value) for value in range(1 << dimension)]
    spectrum: set[int] = set()
    for left_index in range(1, len(tables)):
        left = tables[left_index]
        for right_index in range(left_index + 1, len(tables)):
            right = tables[right_index]
            support = sum(a or b for a, b in zip(left, right, strict=True))
            spectrum.add(support)
    return spectrum


def main() -> None:
    broken_formula_detected = False
    for n in range(1, 5):
        bitset_spectrum, pair_count, detected_here = spectrum_bitset(n)
        broken_formula_detected |= detected_here
        independent_spectrum = spectrum_truth_tables(n)
        if bitset_spectrum != independent_spectrum:
            raise AssertionError((n, bitset_spectrum, independent_spectrum))
        print(
            f"n={n}: unordered independent generating pairs={pair_count}, "
            f"support_weights={sorted(bitset_spectrum)}"
        )
    if not broken_formula_detected:
        raise AssertionError("negative control did not distinguish XOR from OR")
    print("PASS: exact two-dimensional support spectra for RM_2(2,n), n=1..4")


if __name__ == "__main__":
    main()
