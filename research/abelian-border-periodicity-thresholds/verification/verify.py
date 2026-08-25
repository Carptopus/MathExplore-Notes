"""Fail-closed verification for the first Abelian-border threshold layer."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import platform
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


def direct_abelian_bordered(word: str) -> bool:
    return any(
        word[:border].count("1") == word[-border:].count("1")
        for border in range(1, len(word))
    )


def brute_allowed(threshold: int, window: int) -> set[str]:
    result: set[str] = set()
    for bits in itertools.product("01", repeat=window):
        word = "".join(bits)
        if all(
            direct_abelian_bordered(word[start : start + length])
            for length in range(threshold, window + 1)
            for start in range(window - length + 1)
        ):
            result.add(word)
    return result


def graph_rows(threshold: int, window: int, phase_limit: int | None = None):
    words, graph = probe.build_graph(threshold, window)
    cyclic = 0
    maximum_states = 0
    branching: list[dict[str, object]] = []
    for component_tuple in nx.strongly_connected_components(graph):
        component = set(component_tuple)
        internal_edges = sum(
            1 for _, target in graph.out_edges(component) if target in component
        )
        if len(component) == 1 and internal_edges == 0:
            continue
        cyclic += 1
        maximum_states = max(maximum_states, len(component))
        if internal_edges <= len(component):
            continue
        if phase_limit is None:
            raise AssertionError("branching component without a phase check")
        phase = probe.closed_uniform_phase_cover(graph, component, phase_limit)
        witnesses = phase["witnesses"]
        best = max(witnesses, key=lambda row: (row[2], -row[0]), default=(0, 0, 0))
        branching.append(
            {
                "states": len(component),
                "internal_edges": internal_edges,
                "covered_states": phase["covered_states"],
                "uncovered_acyclic": phase["uncovered_acyclic"],
                "witness_period": best[0],
                "witness_weight": best[1],
                "witness_states": best[2],
            }
        )
    branching.sort(key=lambda row: tuple(row.values()))
    return {
        "threshold": threshold,
        "window": window,
        "allowed_words": len(words),
        "graph_nodes": graph.number_of_nodes(),
        "graph_edges": graph.number_of_edges(),
        "cyclic_components": cyclic,
        "maximum_cyclic_states": maximum_states,
        "branching_components": branching,
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    # The optimized half-length test must agree with the definition using every
    # nonempty proper prefix and suffix, including overlapping borders.
    checked_words = 0
    for length in range(1, 17):
        for bits in itertools.product("01", repeat=length):
            word = "".join(bits)
            assert probe.abelian_bordered(word) == direct_abelian_bordered(word)
            checked_words += 1

    # Small exhaustive controls independently enumerate all binary words.
    controls = []
    for threshold, window in ((3, 6), (4, 8), (5, 10)):
        expected = brute_allowed(threshold, window)
        actual = set(probe.allowed_words(threshold, window))
        assert actual == expected
        controls.append(
            {"threshold": threshold, "window": window, "allowed_words": len(actual)}
        )

    threshold14 = graph_rows(14, 36)
    assert threshold14 == {
        "threshold": 14,
        "window": 36,
        "allowed_words": 38450,
        "graph_nodes": 38544,
        "graph_edges": 38450,
        "cyclic_components": 1377,
        "maximum_cyclic_states": 13,
        "branching_components": [],
    }

    threshold15 = graph_rows(15, 30, phase_limit=24)
    assert threshold15["allowed_words"] == 199420
    assert threshold15["graph_nodes"] == 217280
    assert threshold15["graph_edges"] == 199420
    assert threshold15["cyclic_components"] == 2540
    assert threshold15["branching_components"] == [
        {
            "states": 40,
            "internal_edges": 42,
            "covered_states": 29,
            "uncovered_acyclic": True,
            "witness_period": 4,
            "witness_weight": 2,
            "witness_states": 29,
        },
        {
            "states": 40,
            "internal_edges": 42,
            "covered_states": 29,
            "uncovered_acyclic": True,
            "witness_period": 4,
            "witness_weight": 2,
            "witness_states": 29,
        },
        {
            "states": 60,
            "internal_edges": 62,
            "covered_states": 54,
            "uncovered_acyclic": True,
            "witness_period": 14,
            "witness_weight": 7,
            "witness_states": 54,
        },
        {
            "states": 60,
            "internal_edges": 62,
            "covered_states": 54,
            "uncovered_acyclic": True,
            "witness_period": 14,
            "witness_weight": 7,
            "witness_states": 54,
        },
    ]

    files = [
        PROBE_PATH,
        VERIFICATION_DIR / "verify_threshold14.cpp",
        VERIFICATION_DIR / "verify_threshold15.cpp",
        VERIFICATION_DIR / "verify_period_bounds.py",
        Path(__file__).resolve(),
    ]
    result = {
        "status": "VERIFIED",
        "environment": {
            "python": platform.python_version(),
            "networkx": nx.__version__,
        },
        "controls": {
            "definition_words_checked": checked_words,
            "small_graphs": controls,
        },
        "threshold14": threshold14,
        "threshold15": threshold15,
        "sha256": {path.name: sha256(path) for path in files},
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
