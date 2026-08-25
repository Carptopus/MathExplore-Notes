"""Finite-window recurrent-core probe for the Abelian border problem.

For a threshold C and window N, generate every binary N-word whose factors of
length C through N are Abelian bordered.  The resulting de Bruijn graph is an
over-approximation to the infinite language.  Recurrent SCCs are inspected for
a uniform equal-Parikh block length.

This is a discovery/calibration script only: finite N cannot establish the
unbounded hypothesis.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache

import networkx as nx


@lru_cache(maxsize=None)
def abelian_bordered(word: str) -> bool:
    length = len(word)
    total = sum(letter == "1" for letter in word)
    left = 0
    right = 0
    for border in range(1, length // 2 + 1):
        left += word[border - 1] == "1"
        right += word[length - border] == "1"
        if left == right:
            return True
    return False


def valid_after_append(word: str, threshold: int) -> bool:
    return all(
        abelian_bordered(word[-length:])
        for length in range(threshold, len(word) + 1)
    )


def allowed_words(threshold: int, window: int) -> list[str]:
    level = [""]
    for _ in range(window):
        next_level: list[str] = []
        for word in level:
            for letter in "01":
                candidate = word + letter
                if len(candidate) < threshold or valid_after_append(candidate, threshold):
                    next_level.append(candidate)
        level = next_level
        if not level:
            break
    return level


def build_graph(threshold: int, window: int) -> tuple[list[str], nx.DiGraph]:
    words = allowed_words(threshold, window)
    graph = nx.DiGraph()
    for word in words:
        graph.add_edge(word[:-1], word[1:], weight=int(word[-1]))
    return words, graph


def uniform_block_weight(
    graph: nx.DiGraph, component: set[str], max_period: int
) -> tuple[int, int] | None:
    """Find ell such that every ell-edge path in the SCC has the same 1-count."""

    outgoing: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for source, target, data in graph.edges(data=True):
        if source in component and target in component:
            outgoing[source].append((target, data["weight"]))

    weights = {state: {0} for state in component}
    for period in range(1, max_period + 1):
        next_weights: dict[str, set[int]] = {}
        for state in component:
            values = {
                weight + suffix_weight
                for target, weight in outgoing[state]
                for suffix_weight in weights[target]
            }
            next_weights[state] = values
        weights = next_weights
        union = set().union(*weights.values())
        if len(union) == 1 and all(weights[state] for state in component):
            return period, next(iter(union))
    return None


def closed_uniform_phase_cover(
    graph: nx.DiGraph, component: set[str], max_period: int
) -> dict[str, object]:
    """Find states supporting pathwise equal-weight blocks under ell-step motion."""

    one_step = {
        state: [
            (target, data["weight"])
            for _, target, data in graph.out_edges(state, data=True)
            if target in component
        ]
        for state in component
    }
    transitions = {state: {(state, 0)} for state in component}
    covered: set[str] = set()
    witnesses: list[tuple[int, int, int]] = []

    for period in range(1, max_period + 1):
        transitions = {
            state: {
                (target, weight + edge_weight)
                for middle, weight in transitions[state]
                for target, edge_weight in one_step[middle]
            }
            for state in component
        }
        for block_weight in range(period + 1):
            good = {
                state
                for state in component
                if transitions[state]
                and all(weight == block_weight for _, weight in transitions[state])
            }
            changed = True
            while changed:
                reduced = {
                    state
                    for state in good
                    if all(target in good for target, _ in transitions[state])
                }
                changed = reduced != good
                good = reduced
            if good:
                covered.update(good)
                witnesses.append((period, block_weight, len(good)))

    return {
        "covered_states": len(covered),
        "component_states": len(component),
        "fully_covered": covered == component,
        "uncovered_acyclic": nx.is_directed_acyclic_graph(
            graph.subgraph(component - covered)
        ),
        "witnesses": witnesses,
    }


def inspect(threshold: int, window: int) -> dict[str, object]:
    words, graph = build_graph(threshold, window)

    recurrent = []
    for component_tuple in nx.strongly_connected_components(graph):
        component = set(component_tuple)
        if len(component) == 1:
            state = next(iter(component))
            if not graph.has_edge(state, state):
                continue
        internal_edges = sum(
            1 for source, target in graph.edges if source in component and target in component
        )
        branching = internal_edges > len(component)
        recurrent.append(
            {
                "states": len(component),
                "edges": internal_edges,
                "branching": branching,
                "uniform_block": uniform_block_weight(graph, component, 2 * threshold + 8),
            }
        )
    recurrent.sort(key=lambda item: (item["branching"], item["states"]), reverse=True)
    return {
        "threshold": threshold,
        "window": window,
        "allowed_words": len(words),
        "recurrent_components": len(recurrent),
        "components": recurrent,
    }


def main() -> None:
    for threshold in range(3, 19):
        result = inspect(threshold, max(18, 2 * threshold + 8))
        components = result.pop("components")
        branching = [component for component in components if component["branching"]]
        result["branching_components"] = len(branching)
        result["largest_component"] = max(
            components, key=lambda component: component["states"], default=None
        )
        result["branching_without_uniform_block"] = sum(
            component["uniform_block"] is None for component in branching
        )
        print(result)


if __name__ == "__main__":
    main()
