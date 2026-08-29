"""Verify the Walsh-zero low-polar-rank family missed by the original B3 claim.

For n >= 5, set q=x0*x1 and
    f1=q+x2, f2=q+x3, f3=q+x4.
Every nonzero output combination has zero Walsh sum.  Odd combinations have
polar rank two and even combinations have polar rank zero, while the common
zero fibre has size 2^(n-3).  This is a boundary/negative-control certificate:
it shows why the nonzero-Walsh hypothesis cannot be omitted from the existing
rank-two/rank-four recursion theorem.
"""

from __future__ import annotations


def gf2_rank(rows: list[int], dimension: int) -> int:
    rows = rows[:]
    rank = 0
    for column in range(dimension):
        pivot = next(
            (index for index in range(rank, dimension) if (rows[index] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(dimension):
            if index != rank and ((rows[index] >> column) & 1):
                rows[index] ^= rows[rank]
        rank += 1
    return rank


def value(function_index: int, point: int) -> int:
    q = ((point >> 0) & 1) & ((point >> 1) & 1)
    linear_coordinate = 2 + function_index
    return q ^ ((point >> linear_coordinate) & 1)


def combination(mask: int, point: int) -> int:
    result = 0
    for function_index in range(3):
        if (mask >> function_index) & 1:
            result ^= value(function_index, point)
    return result


def polar_rank(mask: int, dimension: int) -> int:
    rows = [0] * dimension
    zero = combination(mask, 0)
    for i in range(dimension):
        for j in range(i + 1, dimension):
            entry = (
                combination(mask, 1 << i)
                ^ combination(mask, 1 << j)
                ^ combination(mask, (1 << i) | (1 << j))
                ^ zero
            )
            if entry:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
    return gf2_rank(rows, dimension)


def walsh_sum(mask: int, dimension: int) -> int:
    return sum(
        1 if combination(mask, point) == 0 else -1
        for point in range(1 << dimension)
    )


def common_zero_count(dimension: int) -> int:
    return sum(
        all(value(function_index, point) == 0 for function_index in range(3))
        for point in range(1 << dimension)
    )


def main() -> None:
    for dimension in range(5, 11):
        signatures = [
            (polar_rank(mask, dimension), walsh_sum(mask, dimension))
            for mask in range(1, 8)
        ]
        expected_ranks = [2 if mask.bit_count() % 2 else 0 for mask in range(1, 8)]
        assert [rank for rank, _ in signatures] == expected_ranks
        assert all(walsh == 0 for _, walsh in signatures)
        assert common_zero_count(dimension) == 1 << (dimension - 3)

        truth_vectors = {
            tuple(value(function_index, point) for point in range(1 << dimension))
            for function_index in range(3)
        }
        assert len(truth_vectors) == 3
        assert all(any(combination(mask, point) for point in range(1 << dimension)) for mask in range(1, 8))

    # Destructive control: deleting the radical linear term from f1 restores a
    # nonzero Walsh sum for q, so the all-zero conclusion is not vacuous.
    dimension = 5
    q_walsh = sum(
        1 if ((((point >> 0) & 1) & ((point >> 1) & 1)) == 0) else -1
        for point in range(1 << dimension)
    )
    assert q_walsh != 0

    print("PASS: Walsh-zero low-rank boundary family verified for n=5..10")
    print("FORMULA: ranks=(2,2,0,2,0,0,2), Walsh=(0,...,0), Z=2^(n-3)")


if __name__ == "__main__":
    main()
