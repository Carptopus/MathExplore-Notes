"""Small-order falsification probe for wsat(K_n, Q_3).

This script searches for sparse percolating edge sets.  It is discovery and
regression evidence only; it does not prove optimality.
"""

from __future__ import annotations

import argparse
import itertools
import random

import numpy as np


BASE_EDGES = tuple(
    (x, x ^ bit)
    for x in range(8)
    for bit in (1, 2, 4)
    if x < (x ^ bit)
)


def labelled_cube_patterns() -> tuple[int, ...]:
    patterns: set[int] = set()
    base_pairs = list(itertools.combinations(range(8), 2))
    edge_index = {edge: i for i, edge in enumerate(base_pairs)}
    for permutation in itertools.permutations(range(8)):
        mask = 0
        for x, y in BASE_EDGES:
            edge = tuple(sorted((permutation[x], permutation[y])))
            mask |= 1 << edge_index[edge]
        patterns.add(mask)
    assert len(patterns) == 840
    return tuple(sorted(patterns))


PATTERNS = labelled_cube_patterns()


def cube_masks(n: int) -> tuple[list[tuple[int, int]], np.ndarray]:
    if not 8 <= n <= 11:
        raise ValueError("the one-word mask builder supports 8 <= n <= 11")
    edges = list(itertools.combinations(range(n), 2))
    edge_index = {edge: i for i, edge in enumerate(edges)}
    base_pairs = list(itertools.combinations(range(8), 2))
    masks: list[int] = []
    for vertices in itertools.combinations(range(n), 8):
        for pattern in PATTERNS:
            mask = 0
            for i, (x, y) in enumerate(base_pairs):
                if pattern >> i & 1:
                    mask |= 1 << edge_index[(vertices[x], vertices[y])]
            masks.append(mask)
    return edges, np.asarray(masks, dtype=np.uint64)


def cube_masks_wide(n: int) -> tuple[list[tuple[int, int]], tuple[np.ndarray, np.ndarray]]:
    if not 12 <= n <= 16:
        raise ValueError("the two-word mask builder supports 12 <= n <= 16")
    edges = list(itertools.combinations(range(n), 2))
    edge_index = {edge: i for i, edge in enumerate(edges)}
    base_pairs = list(itertools.combinations(range(8), 2))
    lows: list[int] = []
    highs: list[int] = []
    for vertices in itertools.combinations(range(n), 8):
        for pattern in PATTERNS:
            low = 0
            high = 0
            for i, (x, y) in enumerate(base_pairs):
                if pattern >> i & 1:
                    edge = edge_index[(vertices[x], vertices[y])]
                    if edge < 64:
                        low |= 1 << edge
                    else:
                        high |= 1 << (edge - 64)
            lows.append(low)
            highs.append(high)
    return edges, (np.asarray(lows, dtype=np.uint64), np.asarray(highs, dtype=np.uint64))


def closure(mask: int, cubes: np.ndarray, full: int) -> int:
    current = np.uint64(mask)
    full64 = np.uint64(full)
    while current != full64:
        missing = cubes & ~current
        singleton = (missing != 0) & ((missing & (missing - np.uint64(1))) == 0)
        if not np.any(singleton):
            break
        add = np.bitwise_or.reduce(missing[singleton])
        updated = current | add
        if updated == current:
            break
        current = updated
    return int(current)


def closure_wide(mask: int, cubes: tuple[np.ndarray, np.ndarray], full: int) -> int:
    low_mask = (1 << 64) - 1
    current_low = np.uint64(mask & low_mask)
    current_high = np.uint64(mask >> 64)
    full_low = np.uint64(full & low_mask)
    full_high = np.uint64(full >> 64)
    cube_low, cube_high = cubes
    while current_low != full_low or current_high != full_high:
        missing_low = cube_low & ~current_low
        missing_high = cube_high & ~current_high
        low_singleton = (
            (missing_high == 0)
            & (missing_low != 0)
            & ((missing_low & (missing_low - np.uint64(1))) == 0)
        )
        high_singleton = (
            (missing_low == 0)
            & (missing_high != 0)
            & ((missing_high & (missing_high - np.uint64(1))) == 0)
        )
        if not np.any(low_singleton) and not np.any(high_singleton):
            break
        add_low = np.bitwise_or.reduce(missing_low[low_singleton], initial=np.uint64(0))
        add_high = np.bitwise_or.reduce(missing_high[high_singleton], initial=np.uint64(0))
        updated_low = current_low | add_low
        updated_high = current_high | add_high
        if updated_low == current_low and updated_high == current_high:
            break
        current_low = updated_low
        current_high = updated_high
    return int(current_low) | (int(current_high) << 64)


def greedy_search(n: int, repetitions: int, seed: int) -> tuple[int, list[tuple[int, int]]]:
    if n <= 11:
        edges, cubes = cube_masks(n)
        close = closure
    else:
        edges, cubes = cube_masks_wide(n)
        close = closure_wide
    full = (1 << len(edges)) - 1
    best = full
    rng = random.Random(seed)
    order = list(range(len(edges)))
    for _ in range(repetitions):
        current = full
        changed = True
        while changed:
            changed = False
            rng.shuffle(order)
            for i in order:
                candidate = current ^ (1 << i)
                if current >> i & 1 and close(candidate, cubes, full) == full:
                    current = candidate
                    changed = True
        if current.bit_count() < best.bit_count():
            best = current
    witness = [edge for i, edge in enumerate(edges) if best >> i & 1]
    assert close(best, cubes, full) == full
    return best.bit_count(), witness


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--repetitions", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260831)
    args = parser.parse_args()
    value, witness = greedy_search(args.n, args.repetitions, args.seed)
    print({"n": args.n, "best": value, "candidate_2n_minus_1": 2 * args.n - 1, "edges": witness})


if __name__ == "__main__":
    main()
