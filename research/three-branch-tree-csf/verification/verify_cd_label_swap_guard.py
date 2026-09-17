"""Exact guard for S19's one-sided C/D label-swap factorization."""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, combinations_with_replacement


Poly = tuple[int, ...]


def normalize(poly: list[int] | Poly) -> Poly:
    values = list(poly)
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(*polys: Poly) -> Poly:
    size = max((len(poly) for poly in polys), default=0)
    values = [0] * size
    for poly in polys:
        for index, coefficient in enumerate(poly):
            values[index] += coefficient
    return normalize(values)


def neg(poly: Poly) -> Poly:
    return tuple(-coefficient for coefficient in poly)


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, neg(right))


def mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return ()
    values = [0] * (len(left) + len(right) - 1)
    for i, left_coefficient in enumerate(left):
        for j, right_coefficient in enumerate(right):
            values[i + j] += left_coefficient * right_coefficient
    return normalize(values)


def monomial(power: int) -> Poly:
    return (0,) * power + (1,)


def h(length: int) -> Poly:
    return (0,) + (1,) * length


def path_remainder(
    a_poly: Poly,
    b_poly: Poly,
    c_poly: Poly,
    alpha: int,
    beta: int,
) -> Poly:
    z = monomial(alpha)
    w = monomial(beta)
    h_alpha = h(alpha)
    h_beta = h(beta)
    one = (1,)
    return add(
        mul(a_poly, add(h_alpha, mul(z, h_beta))),
        mul(b_poly, add(h_alpha, h_beta)),
        mul(c_poly, add(h_beta, mul(w, h_alpha))),
        mul(sub(z, one), mul(a_poly, b_poly)),
        mul(sub(mul(z, w), one), mul(a_poly, c_poly)),
        mul(sub(w, one), mul(b_poly, c_poly)),
    )


def build_tree(
    alpha: int,
    beta: int,
    arms_a: tuple[int, ...],
    arms_b: tuple[int, ...],
    arms_c: tuple[int, ...],
) -> dict[int, set[int]]:
    adjacency: dict[int, set[int]] = {}

    def add_vertex() -> int:
        vertex = len(adjacency)
        adjacency[vertex] = set()
        return vertex

    def add_edge(u: int, v: int) -> None:
        adjacency[u].add(v)
        adjacency[v].add(u)

    centers = [add_vertex()]
    previous = centers[0]
    for _ in range(alpha):
        current = add_vertex()
        add_edge(previous, current)
        previous = current
    centers.append(previous)
    for _ in range(beta):
        current = add_vertex()
        add_edge(previous, current)
        previous = current
    centers.append(previous)

    for center, arms in zip(centers, (arms_a, arms_b, arms_c), strict=True):
        for length in arms:
            previous = center
            for _ in range(length):
                current = add_vertex()
                add_edge(previous, current)
                previous = current
    return adjacency


def path_sequence(adjacency: dict[int, set[int]]) -> Counter[int]:
    result: Counter[int] = Counter()
    for start in adjacency:
        distances = {start: 0}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor not in distances:
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        for end, distance in distances.items():
            if start < end:
                result[distance] += 1
    return result


def edge_partitions(adjacency: dict[int, set[int]]) -> Counter[tuple[int, int]]:
    order = len(adjacency)
    result: Counter[tuple[int, int]] = Counter()
    for u in adjacency:
        for v in adjacency[u]:
            if u > v:
                continue
            seen = {u}
            stack = [u]
            while stack:
                current = stack.pop()
                for neighbor in adjacency[current]:
                    if (current == u and neighbor == v) or (current == v and neighbor == u):
                        continue
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            part = len(seen)
            result[tuple(sorted((part, order - part)))] += 1
    return result


def degree_sequence(adjacency: dict[int, set[int]]) -> tuple[int, ...]:
    return tuple(sorted(len(neighbors) for neighbors in adjacency.values()))


def main() -> None:
    tree = build_tree(1, 1, (2, 1, 1), (3,), (2, 2, 1, 1))
    tree_prime = build_tree(1, 1, (2, 1, 1), (1,), (3, 2, 2, 1))
    assert len(tree) == len(tree_prime) == 16
    assert degree_sequence(tree) == degree_sequence(tree_prime)
    assert edge_partitions(tree) == edge_partitions(tree_prime)
    assert Counter((2, 1, 1) + (3,) + (2, 2, 1, 1)) == Counter(
        (2, 1, 1) + (1,) + (3, 2, 2, 1)
    )
    paths = path_sequence(tree)
    paths_prime = path_sequence(tree_prime)
    assert paths[3] == 28 and paths_prime[3] == 30

    checked = 0
    for u0_size in (1, 2, 3):
        for u0 in combinations_with_replacement(range(1, 5), u0_size):
            h0 = add(*(h(length) for length in u0))
            for t, v in combinations(range(1, 7), 2):
                for t_value, v_value in ((t, v), (v, t)):
                    for alpha in range(1, 5):
                        for beta in range(1, 5):
                            w_length = t_value + alpha
                            a_poly = add(h0, h(t_value))
                            c_poly = add(h0, h(t_value), h(w_length))
                            c_prime_poly = add(h0, h(v_value), h(w_length))
                            difference = sub(
                                path_remainder(a_poly, h(v_value), c_poly, alpha, beta),
                                path_remainder(a_poly, h(t_value), c_prime_poly, alpha, beta),
                            )
                            expected = mul(
                                mul(
                                    sub(h(v_value), h(t_value)),
                                    sub((1,), monomial(beta)),
                                ),
                                mul(sub(monomial(alpha), (1,)), h0),
                            )
                            assert difference == expected
                            assert any(difference)
                            checked += 1

    print(
        "PASS verify_cd_label_swap_guard "
        "interface_order=16 distance3=28!=30 "
        f"factor_cases={checked}"
    )


if __name__ == "__main__":
    main()
