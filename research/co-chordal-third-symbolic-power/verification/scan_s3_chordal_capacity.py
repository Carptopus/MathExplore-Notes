"""Small exact pressure test for the s=3 co-chordal symbolic-power boundary.

For a chordal graph H, construct all degree-five exponent vectors a such that
sum(a[v] for v in Q) <= 2 for every maximal clique Q of H.  These are the
degree-five generators obtained from I(G)^(3), where G is the complement of H.

The script tests two sufficient mechanisms only:

* the discrete-polymatroid symmetric exchange axiom;
* linear quotients for several deterministic monomial orders induced by one
  perfect-elimination ordering.

Failure of either test is NOT a counterexample to a linear resolution.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import networkx as nx


Exponent = tuple[int, ...]


def bounded_compositions(total: int, parts: int, cap: int = 2):
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(min(cap, total) + 1):
        for tail in bounded_compositions(total - first, parts - 1, cap):
            yield (first,) + tail


def maximal_cliques(graph: nx.Graph) -> list[tuple[int, ...]]:
    return [tuple(sorted(clique)) for clique in nx.find_cliques(graph)]


def generators(graph: nx.Graph) -> list[Exponent]:
    n = graph.number_of_nodes()
    cliques = maximal_cliques(graph)
    return [
        a
        for a in bounded_compositions(5, n)
        if all(sum(a[v] for v in clique) <= 2 for clique in cliques)
    ]


def exchange_witness(gens: list[Exponent]):
    gen_set = set(gens)
    for a in gens:
        for b in gens:
            for i, (ai, bi) in enumerate(zip(a, b)):
                if ai <= bi:
                    continue
                repaired = False
                for j, (aj, bj) in enumerate(zip(a, b)):
                    if aj >= bj:
                        continue
                    candidate = list(a)
                    candidate[i] -= 1
                    candidate[j] += 1
                    if tuple(candidate) in gen_set:
                        repaired = True
                        break
                if not repaired:
                    return {"a": a, "b": b, "i": i}
    return None


def divides(a: Exponent, b: Exponent) -> bool:
    return all(x <= y for x, y in zip(a, b))


def quotient_ratio(u: Exponent, v: Exponent) -> Exponent:
    return tuple(max(ui - vi, 0) for ui, vi in zip(u, v))


def minimal_monomials(items: list[Exponent]) -> list[Exponent]:
    unique = sorted(set(items), key=lambda a: (sum(a), a))
    result: list[Exponent] = []
    for item in unique:
        if not any(divides(old, item) for old in result):
            result.append(item)
    return result


def linear_quotient_failure(ordered: list[Exponent]):
    for index, current in enumerate(ordered[1:], start=1):
        ratios = [quotient_ratio(previous, current) for previous in ordered[:index]]
        minimal = minimal_monomials(ratios)
        if any(sum(item) != 1 for item in minimal):
            return {
                "index": index,
                "current": current,
                "minimal_colon_generators": minimal,
            }
    return None


def componentwise_max(a: Exponent, b: Exponent) -> Exponent:
    return tuple(max(x, y) for x, y in zip(a, b))


def strictly_divides(a: Exponent, b: Exponent) -> bool:
    return divides(a, b) and a != b


def nonlinear_first_syzygy_witness(gens: list[Exponent]):
    """Return an exact lcm-lattice H_0 witness, if one exists.

    For each pair-lcm m, the vertices of the crosscut complex are the minimal
    generators dividing m.  Two vertices are connected by an edge exactly when
    their lcm is strictly below m.  If this graph is disconnected, reduced H_0
    is nonzero and beta_(1,m)(I) is nonzero.  Degree(m)>6 is then a nonlinear
    first syzygy for this degree-five ideal.
    """
    candidate_lcms = {
        componentwise_max(gens[i], gens[j])
        for i in range(len(gens))
        for j in range(i + 1, len(gens))
        if sum(componentwise_max(gens[i], gens[j])) > 6
    }
    for multidegree in sorted(candidate_lcms, key=lambda a: (sum(a), a)):
        atoms = [g for g in gens if divides(g, multidegree)]
        if len(atoms) < 2:
            continue
        seen = {0}
        frontier = [0]
        while frontier:
            i = frontier.pop()
            for j in range(len(atoms)):
                if j in seen:
                    continue
                if strictly_divides(componentwise_max(atoms[i], atoms[j]), multidegree):
                    seen.add(j)
                    frontier.append(j)
        if len(seen) != len(atoms):
            components = []
            unseen = set(range(len(atoms)))
            while unseen:
                start = min(unseen)
                component = {start}
                queue = [start]
                unseen.remove(start)
                while queue:
                    i = queue.pop()
                    neighbours = [
                        j
                        for j in list(unseen)
                        if strictly_divides(
                            componentwise_max(atoms[i], atoms[j]), multidegree
                        )
                    ]
                    for j in neighbours:
                        unseen.remove(j)
                        component.add(j)
                        queue.append(j)
                components.append([atoms[i] for i in sorted(component)])
            return {
                "multidegree": multidegree,
                "total_degree": sum(multidegree),
                "components": components,
            }
    return None


def simplicial_elimination_order(graph: nx.Graph) -> list[int]:
    remaining = set(graph.nodes)
    order: list[int] = []
    while remaining:
        for vertex in sorted(remaining):
            neighbours = set(graph.neighbors(vertex)) & remaining
            if all(graph.has_edge(u, v) for u, v in itertools.combinations(neighbours, 2)):
                order.append(vertex)
                remaining.remove(vertex)
                break
        else:  # pragma: no cover - guarded by nx.is_chordal
            raise ValueError("graph is not chordal")
    return order


def reordered_key(a: Exponent, variable_order: list[int], reverse_variables: bool):
    sequence = list(reversed(variable_order)) if reverse_variables else variable_order
    return tuple(a[v] for v in sequence)


def candidate_orders(gens: list[Exponent], peo: list[int]):
    for reverse_variables in (False, True):
        for reverse_tuple in (False, True):
            for descending in (False, True):
                def key(a, rv=reverse_variables, rt=reverse_tuple):
                    values = reordered_key(a, peo, rv)
                    return tuple(reversed(values)) if rt else values

                name = (
                    f"{'rev-' if reverse_variables else ''}peo-"
                    f"{'revlex' if reverse_tuple else 'lex'}-"
                    f"{'desc' if descending else 'asc'}"
                )
                yield name, sorted(gens, key=key, reverse=descending)


def graph_record(graph: nx.Graph, atlas_index: int):
    peo = simplicial_elimination_order(graph)
    gens = generators(graph)
    exchange_failure = exchange_witness(gens)
    quotient_results = {}
    for name, ordered in candidate_orders(gens, peo):
        quotient_results[name] = linear_quotient_failure(ordered)
    return {
        "atlas_index": atlas_index,
        "n": graph.number_of_nodes(),
        "m": graph.number_of_edges(),
        "graph6": nx.to_graph6_bytes(graph, header=False).decode("ascii").strip(),
        "maximal_cliques": maximal_cliques(graph),
        "peo": peo,
        "generator_count": len(gens),
        "exchange_failure": exchange_failure,
        "linear_quotient_orders": quotient_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    tested = 0
    polymatroid_failure_count = 0
    polymatroid_failures = []
    no_candidate_lq_count = 0
    no_candidate_lq = []
    no_candidate_lq_indices = []
    nonlinear_first_syzygy_count = 0
    nonlinear_first_syzygies = []
    first_order_success = {}

    for atlas_index, graph in enumerate(nx.graph_atlas_g()):
        n = graph.number_of_nodes()
        if n < 3 or n > args.max_n or not nx.is_chordal(graph):
            continue
        record = graph_record(graph, atlas_index)
        tested += 1
        if record["exchange_failure"] is not None:
            polymatroid_failure_count += 1
            if len(polymatroid_failures) < 3:
                polymatroid_failures.append(record)
        successful_orders = [
            name
            for name, failure in record["linear_quotient_orders"].items()
            if failure is None
        ]
        if not successful_orders:
            no_candidate_lq_count += 1
            no_candidate_lq_indices.append(record["atlas_index"])
            witness = nonlinear_first_syzygy_witness(generators(graph))
            if witness is not None:
                nonlinear_first_syzygy_count += 1
                if len(nonlinear_first_syzygies) < 3:
                    nonlinear_first_syzygies.append({**record, "witness": witness})
            if len(no_candidate_lq) < 3:
                no_candidate_lq.append(record)
        elif successful_orders:
            first_order_success[successful_orders[0]] = (
                first_order_success.get(successful_orders[0], 0) + 1
            )

    result = {
        "scope": {
            "source": "NetworkX graph_atlas_g nonisomorphic graphs",
            "max_n": args.max_n,
            "objects": "all chordal atlas graphs on 3..max_n vertices",
            "claim_boundary": "tests sufficient mechanisms only; not linear-resolution equivalence",
        },
        "tested_chordal_graphs": tested,
        "polymatroid_failure_count": polymatroid_failure_count,
        "first_polymatroid_failures": polymatroid_failures,
        "no_tested_linear_quotient_order_count": no_candidate_lq_count,
        "no_tested_linear_quotient_order_atlas_indices": no_candidate_lq_indices,
        "first_no_tested_linear_quotient_order": no_candidate_lq,
        "nonlinear_first_syzygy_count": nonlinear_first_syzygy_count,
        "first_nonlinear_first_syzygies": nonlinear_first_syzygies,
        "first_successful_order_distribution": first_order_success,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
