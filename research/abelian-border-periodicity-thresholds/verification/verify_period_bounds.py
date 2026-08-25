"""Exact corollary checks for eventual period bounds in the threshold graphs."""

from __future__ import annotations

import importlib.util
import json
from math import gcd
from pathlib import Path

import networkx as nx


VERIFICATION_DIR = Path(__file__).resolve().parent
PROBE_PATH = VERIFICATION_DIR / "probe_finite_type_cores.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("abelian_border_probe", PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PROBE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


probe = load_probe()


def canonical_rotation(word: str) -> str:
    return min(word[index:] + word[:index] for index in range(len(word)))


def cycle_label(graph: nx.DiGraph, component: set[str]) -> str:
    state = min(component)
    start = state
    labels: list[str] = []
    for _ in range(len(component)):
        internal = [
            (target, data["weight"])
            for _, target, data in graph.out_edges(state, data=True)
            if target in component
        ]
        assert len(internal) == 1
        state, weight = internal[0]
        labels.append(str(weight))
    assert state == start
    return "".join(labels)


def least_ordinary_period(word: str) -> int:
    return next(
        period
        for period in range(1, len(word) + 1)
        if all(
            word[index] == word[(index + period) % len(word)]
            for index in range(len(word))
        )
    )


def least_abelian_period(word: str) -> tuple[int, int, int]:
    size = len(word)
    for period in range(1, size + 1):
        orbit = size // gcd(size, period)
        for start in range(size):
            weights = {
                sum(
                    int(word[(start + block * period + offset) % size])
                    for offset in range(period)
                )
                for block in range(orbit)
            }
            if len(weights) == 1:
                return period, start, next(iter(weights))
    raise AssertionError("ordinary cycle period must always be an Abelian period")


def nonbranching_cycles(threshold: int, window: int):
    _, graph = probe.build_graph(threshold, window)
    for component_tuple in nx.strongly_connected_components(graph):
        component = set(component_tuple)
        internal_edges = sum(
            1 for _, target in graph.out_edges(component) if target in component
        )
        if (len(component) > 1 or internal_edges > 0) and internal_edges == len(
            component
        ):
            yield cycle_label(graph, component)


def main() -> None:
    cycles14 = list(nonbranching_cycles(14, 36))
    ordinary_rows = [
        (least_ordinary_period(word), canonical_rotation(word)) for word in cycles14
    ]
    max_ordinary = max(period for period, _ in ordinary_rows)
    ordinary_witness = min(word for period, word in ordinary_rows if period == max_ordinary)
    assert len(cycles14) == 1377
    assert max_ordinary == 13
    assert ordinary_witness == "0000000000001"
    sharp_ordinary_witness = "1000000000000"
    assert canonical_rotation(sharp_ordinary_witness) == ordinary_witness
    assert least_ordinary_period(sharp_ordinary_witness) == 13

    cycles15 = list(nonbranching_cycles(15, 30))
    abelian_rows = [
        (least_abelian_period(word), canonical_rotation(word)) for word in cycles15
    ]
    max_abelian = max(period[0] for period, _ in abelian_rows)
    abelian_witness = min(
        word for period, word in abelian_rows if period[0] == max_abelian
    )
    assert len(cycles15) == 2536
    assert max_abelian == 14
    assert abelian_witness == "00000000000001"
    sharp_abelian_witness = "10000000000000"
    assert canonical_rotation(sharp_abelian_witness) == abelian_witness
    assert least_abelian_period(sharp_abelian_witness)[0] == 14

    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "threshold14": {
                    "nonbranching_cycles": len(cycles14),
                    "maximum_least_ordinary_period": max_ordinary,
                    "canonical_witness": ordinary_witness,
                },
                "threshold15": {
                    "nonbranching_cycles": len(cycles15),
                    "maximum_least_abelian_period": max_abelian,
                    "canonical_witness": abelian_witness,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
