"""Exact finite certificates for the sparse full-palette construction.

This verifies the periodic palette and constructs one replacement closed walk
for every target residue.  It does not replace the infinite sparse-set proof.
"""

from __future__ import annotations

from dataclasses import dataclass


PERIOD_WORD = tuple(map(int, "0101010101232323210123232321"))
PERIOD = len(PERIOD_WORD)


@dataclass(frozen=True)
class Replacement:
    target_residue: int
    start_residue: int
    relative_target: int
    word: tuple[int, ...]


def closed_walks(start: int, length: int):
    def visit(word: tuple[int, ...]):
        if len(word) == length:
            if abs(word[-1] - start) == 1:
                yield word
            return
        for height in (word[-1] - 1, word[-1] + 1):
            if 0 <= height <= 3:
                yield from visit(word + (height,))

    yield from visit((start,))


def verify_period_word() -> None:
    assert PERIOD == 28
    assert set(PERIOD_WORD) == {0, 1, 2, 3}
    assert all(
        abs(PERIOD_WORD[(index + 1) % PERIOD] - PERIOD_WORD[index]) == 1
        for index in range(PERIOD)
    )


def palette(center: int) -> set[int]:
    return {
        PERIOD_WORD[index] + PERIOD_WORD[(center - index) % PERIOD]
        for index in range(PERIOD)
    }


def verify_full_palette() -> dict[int, list[int]]:
    certificate: dict[int, list[int]] = {}
    for center in range(PERIOD):
        expected = {0, 2, 4, 6} if center % 2 == 0 else {1, 3, 5}
        assert palette(center) == expected
        certificate[center] = sorted(expected)
    return certificate


def find_replacements() -> dict[int, Replacement]:
    replacements: dict[int, Replacement] = {}
    for start_residue in range(PERIOD):
        base = tuple(
            PERIOD_WORD[(start_residue + offset) % PERIOD]
            for offset in range(PERIOD)
        )
        for word in closed_walks(base[0], PERIOD):
            for relative_target in range(1, PERIOD):
                target = (start_residue + relative_target) % PERIOD
                if target in replacements or word[relative_target] == base[relative_target]:
                    continue
                replacements[target] = Replacement(
                    target_residue=target,
                    start_residue=start_residue,
                    relative_target=relative_target,
                    word=word,
                )
        if len(replacements) == PERIOD:
            break
    assert set(replacements) == set(range(PERIOD))
    return replacements


def verify_replacements(replacements: dict[int, Replacement]) -> None:
    for target, replacement in replacements.items():
        word = replacement.word
        start = replacement.start_residue
        relative = replacement.relative_target
        assert len(word) == PERIOD
        assert word[0] == PERIOD_WORD[start]
        assert abs(word[-1] - word[0]) == 1
        assert all(abs(word[index + 1] - word[index]) == 1 for index in range(PERIOD - 1))
        assert (start + relative) % PERIOD == target
        assert word[relative] != PERIOD_WORD[target]


def verify_five_pair_bound() -> None:
    # A closed interval of diameter PERIOD meets at most two points of either
    # endpoint progression, hence contaminates at most four of five pairs.
    # Work in doubled coordinates so integer and half-integer centers are
    # covered together.  The nearest pair has endpoint offset |u| <= PERIOD;
    # shifting the pair index changes each endpoint by 2*PERIOD.  A defect
    # interval has doubled diameter 2*PERIOD.
    for nearest_offset in range(-PERIOD, PERIOD + 1):
        left = [nearest_offset + 2 * k * PERIOD for k in range(-2, 3)]
        right = [-nearest_offset - 2 * k * PERIOD for k in range(-2, 3)]
        for interval_start in range(-8 * PERIOD, 8 * PERIOD + 1):
            interval = range(interval_start, interval_start + 2 * PERIOD + 1)
            interval_set = set(interval)
            contaminated = {
                k for k in range(5)
                if left[k] in interval_set or right[k] in interval_set
            }
            assert len(contaminated) <= 4


def arithmetic_progressions():
    level = 1
    while True:
        for start in range(level):
            for step in range(1, level + 1):
                yield start, step
        level += 1


def construct_finite_prefix(
    replacements: dict[int, Replacement], stages: int = 80
) -> tuple[list[int], list[tuple[int, int, int]]]:
    intervals: list[tuple[int, int, int]] = []
    previous_end = -1
    for stage, (progression_start, progression_step) in zip(
        range(1, stages + 1), arithmetic_progressions()
    ):
        target = progression_start
        while True:
            replacement = replacements[target % PERIOD]
            interval_start = target - replacement.relative_target
            required_gap = max(6 * PERIOD + 1, stage * 3)
            if interval_start > previous_end + required_gap:
                break
            target += progression_step
        interval_end = interval_start + PERIOD
        intervals.append((interval_start, interval_end, target))
        previous_end = interval_end

    length = intervals[-1][1] + 4 * PERIOD + 1
    path = [PERIOD_WORD[index % PERIOD] for index in range(length)]
    for interval_start, _, target in intervals:
        replacement = replacements[target % PERIOD]
        for offset, height in enumerate(replacement.word):
            path[interval_start + offset] = height
        assert path[target] != PERIOD_WORD[target % PERIOD]

    return path, intervals


def verify_finite_prefix(
    path: list[int], intervals: list[tuple[int, int, int]]
) -> None:
    assert all(abs(path[index + 1] - path[index]) == 1 for index in range(len(path) - 1))
    assert all(
        right_start - left_end > 6 * PERIOD
        for (_, left_end, _), (right_start, _, _) in zip(intervals, intervals[1:])
    )

    threshold = 5 * PERIOD + 1
    for center in range(threshold, 2 * len(path) - threshold):
        local = {
            path[left] + path[center - left]
            for left in range(max(0, (center - threshold + 1) // 2), min(len(path), center + 1))
            if 0 <= center - left < len(path)
            and abs(2 * left - center) < threshold
        }
        expected = {0, 2, 4, 6} if center % 2 == 0 else {1, 3, 5}
        assert local == expected, (center, local, expected)


def main() -> None:
    verify_period_word()
    palettes = verify_full_palette()
    replacements = find_replacements()
    verify_replacements(replacements)
    verify_five_pair_bound()
    path, intervals = construct_finite_prefix(replacements)
    verify_finite_prefix(path, intervals)
    print("period=28")
    print("full_palette_centers=28")
    print("replacement_targets=28")
    print("five_pair_contamination_bound=PASS")
    print(f"finite_sparse_intervals={len(intervals)}")
    print(f"finite_sparse_prefix_length={len(path)}")
    print("finite_sparse_full_local_palette=PASS")
    for target in range(PERIOD):
        item = replacements[target]
        print(
            f"target={target:02d} start={item.start_residue:02d} "
            f"relative={item.relative_target:02d} "
            f"word={''.join(map(str, item.word))}"
        )
    assert len(palettes) == PERIOD


if __name__ == "__main__":
    main()
