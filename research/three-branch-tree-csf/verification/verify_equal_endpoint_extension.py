"""Bounded controls for the S8 equal-endpoint extension separator."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict


def partitions(total: int, ceiling: int | None = None, current=()):
    if total == 0:
        if len(current) >= 2:
            yield current
        return
    ceiling = min(total, ceiling or total)
    for part in range(ceiling, 0, -1):
        yield from partitions(total - part, part, current + (part,))


def spider_expansion(arms: tuple[int, ...], cache={}):
    arms = tuple(sorted(arms, reverse=True))
    if arms in cache:
        return cache[arms]
    order = 1 + sum(arms)
    edges = []
    next_vertex = 1
    for length in arms:
        previous = 0
        for _ in range(length):
            edges.append((previous, next_vertex))
            previous = next_vertex
            next_vertex += 1

    result = Counter()
    for mask in range(1 << len(edges)):
        parent = list(range(order))

        def find(vertex):
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        kept = 0
        for edge_index, (first, second) in enumerate(edges):
            if not (mask >> edge_index) & 1:
                continue
            kept += 1
            first_root = find(first)
            second_root = find(second)
            if first_root != second_root:
                parent[second_root] = first_root
        sizes = Counter(find(vertex) for vertex in range(order))
        partition = tuple(sorted(sizes.values(), reverse=True))
        result[partition] += (-1) ** kept
    cache[arms] = result
    return result


def add(first, second):
    result = Counter(first)
    result.update(second)
    return result


def signature(expansion):
    return tuple(sorted((key, value) for key, value in expansion.items() if value))


def no_singleton(expansion):
    return signature(
        Counter(
            {
                partition: coefficient
                for partition, coefficient in expansion.items()
                if 1 not in partition
            }
        )
    )


def folded_profile(arms):
    order = 1 + sum(arms)
    threshold = [sum(length >= index for length in arms) for index in range(order + 1)]
    return tuple(
        threshold[index]
        if 2 * index == order
        else threshold[index] + threshold[order - index]
        for index in range(2, order // 2 + 1)
    )


def combined_threshold(first, second):
    order = 1 + sum(first)
    return tuple(
        sum(length >= index for length in first + second)
        for index in range(1, order)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=13)
    parser.add_argument("--folded-max-order", type=int, default=40)
    args = parser.parse_args()

    # Any spider with at least three arms is fixed by its folded one-cut data.
    for order in range(4, args.folded_max_order + 1):
        buckets = defaultdict(list)
        for arms in partitions(order - 1):
            if len(arms) >= 3:
                buckets[folded_profile(arms)].append(arms)
        assert all(len(values) == 1 for values in buckets.values())

    pair_cases = 0
    path_exceptions = 0
    for order in range(3, args.max_order + 1):
        spiders = list(partitions(order - 1))

        # Two active endpoints: original sum plus projected one-step extensions
        # determine the rooted pair.
        both_buckets = defaultdict(list)
        for first_index, first in enumerate(spiders):
            for second in spiders[first_index:]:
                original = add(spider_expansion(first), spider_expansion(second))
                extended = add(
                    spider_expansion(tuple(sorted(first + (1,), reverse=True))),
                    spider_expansion(tuple(sorted(second + (1,), reverse=True))),
                )
                key = (signature(original), no_singleton(extended))
                both_buckets[key].append((first, second))
                pair_cases += 1
        assert all(len(values) == 1 for values in both_buckets.values())

        # One active endpoint: the only allowed ambiguity is the root split of
        # the inactive path.
        single_buckets = defaultdict(list)
        for active in spiders:
            projected = no_singleton(
                spider_expansion(tuple(sorted(active + (1,), reverse=True)))
            )
            for inactive in spiders:
                original = add(spider_expansion(active), spider_expansion(inactive))
                single_buckets[(signature(original), projected)].append(
                    (active, inactive)
                )
        for values in single_buckets.values():
            active_values = {active for active, _ in values}
            assert len(active_values) == 1
            inactive_values = {inactive for _, inactive in values}
            if len(inactive_values) > 1:
                assert all(len(inactive) == 2 for inactive in inactive_values)
                path_exceptions += 1

        # The threshold identity used in the two-active proof.
        for first_index, first in enumerate(spiders):
            for second in spiders[first_index:]:
                original_threshold = combined_threshold(first, second)
                extended_threshold = combined_threshold(
                    tuple(sorted(first + (1,), reverse=True)),
                    tuple(sorted(second + (1,), reverse=True)),
                )
                assert (
                    extended_threshold[1 : len(original_threshold)]
                    == original_threshold[1:]
                )

    print(
        "PASS "
        f"pair_cases={pair_cases} path_exception_buckets={path_exceptions} "
        f"folded_orders_through={args.folded_max_order}"
    )


if __name__ == "__main__":
    main()
