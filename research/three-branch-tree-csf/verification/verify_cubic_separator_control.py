"""Exact positive/negative control for the c=d cubic separator route."""

from __future__ import annotations

import importlib.util
from collections import deque
from pathlib import Path


PROBE_PATH = Path(__file__).resolve().parent / "probe_three_branch_cut_profiles.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("three_branch_probe", PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PROBE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def path_profile(adjacency):
    counts = [0] * len(adjacency)
    for start in range(len(adjacency)):
        distances = [-1] * len(adjacency)
        distances[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour, _ in adjacency[current]:
                if distances[neighbour] < 0:
                    distances[neighbour] = distances[current] + 1
                    queue.append(neighbour)
        for finish in range(start + 1, len(adjacency)):
            counts[distances[finish]] += 1
    return tuple(counts)


def main() -> None:
    probe = load_probe()
    first = (1, 1, (1, 1), (3, 1), (2, 2, 2, 1))
    second = (1, 1, (1, 1), (2, 1, 1), (3, 2, 2))

    first_adjacency, _ = probe.tree(first)
    second_adjacency, _ = probe.tree(second)
    assert len(first_adjacency) == len(second_adjacency) == 16
    assert first != second
    assert first[0] + first[1] == second[0] + second[1]
    assert sorted(first[2] + first[3] + first[4]) == sorted(
        second[2] + second[3] + second[4]
    )
    assert path_profile(first_adjacency) == path_profile(second_adjacency)

    first_profile = probe.cut_profile(first, 3)
    second_profile = probe.cut_profile(second, 3)
    assert first_profile[0] == second_profile[0]
    assert first_profile[1] == second_profile[1]
    assert first_profile[2] != second_profile[2]

    first_three = dict(first_profile[2])
    second_three = dict(second_profile[2])
    witness = (5, 5, 3, 3)
    assert first_three.get(witness, 0) == 0
    assert second_three.get(witness, 0) == 1
    print(
        "PASS order=16 one_cut_equal=true two_cut_equal=true "
        "three_cut_witness=(5,5,3,3):0!=1"
    )


if __name__ == "__main__":
    main()
