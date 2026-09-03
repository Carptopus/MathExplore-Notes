"""最低未覆盖秩的精确探针。

模型使用 Mochan 文中建议替代 M_3 的正则环面地图 {4,4}_{(8,0)}，
只检查给定电压构造的路径交条件，不把有限结果当作一般证明。
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import product

from sympy.combinatorics import Permutation, PermutationGroup


N = 8


@dataclass(frozen=True, order=True)
class Edge:
    kind: str
    x: int
    y: int


@dataclass(frozen=True, order=True)
class Flag:
    vertex: tuple[int, int]
    edge: Edge
    face: tuple[int, int]


def mod(a: int) -> int:
    return a % N


def edge_vertices(edge: Edge) -> tuple[tuple[int, int], tuple[int, int]]:
    if edge.kind == "h":
        return (edge.x, edge.y), (mod(edge.x + 1), edge.y)
    return (edge.x, edge.y), (edge.x, mod(edge.y + 1))


def edge_faces(edge: Edge) -> tuple[tuple[int, int], tuple[int, int]]:
    if edge.kind == "h":
        return (edge.x, edge.y), (edge.x, mod(edge.y - 1))
    return (edge.x, edge.y), (mod(edge.x - 1), edge.y)


def face_edges(face: tuple[int, int]) -> tuple[Edge, Edge, Edge, Edge]:
    x, y = face
    return (
        Edge("h", x, y),
        Edge("v", mod(x + 1), y),
        Edge("h", x, mod(y + 1)),
        Edge("v", x, y),
    )


def all_flags() -> list[Flag]:
    result: list[Flag] = []
    for face in product(range(N), repeat=2):
        for edge in face_edges(face):
            for vertex in edge_vertices(edge):
                result.append(Flag(vertex, edge, face))
    return sorted(result)


FLAGS = all_flags()
INDEX = {flag: i for i, flag in enumerate(FLAGS)}
IDENTITY = tuple(range(len(FLAGS)))
MAX_EXPLICIT_GROUP_ORDER = 4_096


def adjacency(flag: Flag, color: int) -> Flag:
    if color == 0:
        u, v = edge_vertices(flag.edge)
        return Flag(v if flag.vertex == u else u, flag.edge, flag.face)
    if color == 1:
        choices = [e for e in face_edges(flag.face) if flag.vertex in edge_vertices(e)]
        assert len(choices) == 2
        edge = choices[1] if choices[0] == flag.edge else choices[0]
        return Flag(flag.vertex, edge, flag.face)
    if color == 2:
        f, g = edge_faces(flag.edge)
        return Flag(flag.vertex, flag.edge, g if flag.face == f else f)
    raise ValueError(color)


R = tuple(tuple(INDEX[adjacency(flag, color)] for flag in FLAGS) for color in range(3))


def then(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Right action: apply left, then right."""
    return tuple(right[left[i]] for i in range(len(left)))


def word(*generators: tuple[int, ...]) -> tuple[int, ...]:
    value = IDENTITY
    for generator in generators:
        value = then(value, generator)
    return value


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for i, image in enumerate(permutation):
        result[image] = i
    return tuple(result)


def generate(
    generators: list[tuple[int, ...]],
    limit: int = MAX_EXPLICIT_GROUP_ORDER,
) -> set[tuple[int, ...]]:
    exact_order = int(
        PermutationGroup([Permutation(list(g)) for g in generators]).order()
    )
    if exact_order > limit:
        raise RuntimeError(
            f"refusing explicit closure of group of order {exact_order}; hard limit is {limit}"
        )
    seen = {IDENTITY}
    queue = deque([IDENTITY])
    while queue:
        value = queue.popleft()
        for generator in generators:
            nxt = then(value, generator)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
                if len(seen) > limit:
                    raise RuntimeError(f"group exceeded limit {limit}")
    assert len(seen) == exact_order
    return seen


def flag_coloring(link_colors: frozenset[int]) -> tuple[int, ...]:
    """Two-color M_3 using the link colors below the new top rank."""
    colors = [-1] * len(FLAGS)
    colors[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for color, generator in enumerate(R):
            j = generator[i]
            expected = colors[i] ^ (color in link_colors)
            if colors[j] < 0:
                colors[j] = expected
                queue.append(j)
            else:
                assert colors[j] == expected
    return tuple(colors)


ETA_WORDS = {
    frozenset({0}): (2, 1, 0, 1, 2, 1, 0, 2, 1, 2),
    frozenset({0, 1}): (2, 1, 0, 1, 2, 1, 0, 2, 1, 2),
    frozenset({0, 2}): (2, 1, 0, 2, 1, 2),
}


def eta(link_colors: frozenset[int]) -> tuple[int, ...]:
    """A color-preserving separating involution for the required lower coloring."""
    colors_below_top = link_colors - {3}
    return word(*(R[color] for color in ETA_WORDS[colors_below_top]))


def facet_reflection(face: tuple[int, int], base_edge: Edge, flag: Flag) -> Flag:
    """The square reflection fixing base_edge setwise and swapping its endpoints."""
    assert flag.face == face and base_edge in face_edges(face)
    base_vertices = set(edge_vertices(base_edge))
    mapping: dict[tuple[int, int], tuple[int, int]] = {}
    u, v = edge_vertices(base_edge)
    mapping[u], mapping[v] = v, u
    other = [w for e in face_edges(face) for w in edge_vertices(e) if w not in base_vertices]
    other = sorted(set(other))
    assert len(other) == 2
    # Match the non-base vertices by adjacency to the swapped base endpoints.
    for w in other:
        adjacent_base = next(z for z in base_vertices if any(
            set(edge_vertices(e)) == {w, z} for e in face_edges(face)
        ))
        target_base = mapping[adjacent_base]
        mapping[w] = next(z for z in other if any(
            set(edge_vertices(e)) == {z, target_base} for e in face_edges(face)
        ))
    new_vertex = mapping[flag.vertex]
    old_ends = set(edge_vertices(flag.edge))
    new_ends = {mapping[z] for z in old_ends}
    new_edge = next(e for e in face_edges(face) if set(edge_vertices(e)) == new_ends)
    return Flag(new_vertex, new_edge, face)


def tilde_rho0(link_colors: frozenset[int]) -> tuple[int, ...]:
    colors = flag_coloring(link_colors - {3})
    e = eta(link_colors)
    base_face = FLAGS[0].face
    base_edges = {face: face_edges(face)[0] for face in product(range(N), repeat=2)}
    forced: dict[tuple[int, int], Edge] = {}

    def force_base_edge(face: tuple[int, int], edge: Edge) -> None:
        prior = forced.get(face)
        if prior is not None:
            # Opposite edges of a square induce the same facet reflection.
            facet_flags = [flag for flag in FLAGS if flag.face == face]
            assert all(
                facet_reflection(face, prior, flag) == facet_reflection(face, edge, flag)
                for flag in facet_flags
            )
            return
        forced[face] = edge

    # The 2019 construction first requires Phi_0 eta to be the base flag of
    # its facet.  At the level of the induced facet reflection only its edge
    # matters.
    base_eta_image = FLAGS[e[0]]
    force_base_edge(base_eta_image.face, base_eta_image.edge)

    # For every white Phi in the base facet, Phi r_0 eta r_0 is a required
    # base flag.  Its base edge is the edge of the black flag Phi r_0 eta.
    for i, flag in enumerate(FLAGS):
        if flag.face != base_face or colors[i] != 1:
            continue
        image = FLAGS[e[i]]
        force_base_edge(image.face, image.edge)
    base_edges.update(forced)
    permutation = tuple(
        INDEX[facet_reflection(flag.face, base_edges[flag.face], flag)] for flag in FLAGS
    )
    assert then(permutation, permutation) == IDENTITY
    for i in (0, 1):
        assert then(permutation, R[i]) == then(R[i], permutation)

    fixing = word(permutation, R[0])
    assert fixing[e[0]] == e[0]
    for i, flag in enumerate(FLAGS):
        if flag.face == base_face and colors[i] == 0:
            required = word(R[0], e, R[0])[i]
            assert fixing[required] == required
    return permutation


def voltage_darts(link_colors: frozenset[int], top: tuple[int, ...]):
    """Return dart voltage by (start_vertex, color). 0=a, 1=b."""
    result = {}
    for start in (0, 1):
        for color in range(4):
            if color == 0:
                result[start, color] = IDENTITY
            elif color == 3:
                result[start, color] = top
            elif color in link_colors:
                result[start, color] = word(R[0], R[color]) if start == 0 else word(R[color], R[0])
            else:
                result[start, color] = R[color] if start == 0 else word(R[0], R[color], R[0])
    return result


def path_voltage_sets(
    link_colors: frozenset[int],
    allowed: set[int],
    top: tuple[int, ...],
    limit: int = MAX_EXPLICIT_GROUP_ORDER,
    start_vertex: int = 0,
):
    """Enumerate all reachable (endpoint, voltage) pairs for a fixed start."""
    darts = voltage_darts(link_colors, top)
    seen = {(start_vertex, IDENTITY)}
    queue = deque([(start_vertex, IDENTITY)])
    while queue:
        vertex, value = queue.popleft()
        for color in allowed:
            nxt_vertex = vertex ^ (color in link_colors)
            # Path voltages multiply in reverse order: new dart voltage on the left.
            nxt_value = then(darts[vertex, color], value)
            item = (nxt_vertex, nxt_value)
            if item not in seen:
                seen.add(item)
                queue.append(item)
                if len(seen) > limit:
                    raise RuntimeError(f"voltage state set exceeded limit {limit}")
    return {endpoint: {value for end, value in seen if end == endpoint} for endpoint in (0, 1)}


def voltage_group(
    link_colors: frozenset[int],
    allowed: set[int],
    top: tuple[int, ...],
    start_vertex: int = 0,
) -> tuple[PermutationGroup, tuple[int, ...] | None]:
    """Closed voltages at a start vertex and a chosen tree voltage."""
    darts = voltage_darts(link_colors, top)
    links = sorted(allowed & link_colors)
    generators: list[tuple[int, ...]] = []
    if links:
        tree_color = links[0]
        tree_voltage = darts[start_vertex, tree_color]
        tree_inverse = inverse(tree_voltage)
    else:
        tree_color = None
        tree_voltage = None
        tree_inverse = None

    for color in sorted(allowed):
        if color not in link_colors:
            generators.append(darts[start_vertex, color])
            if tree_voltage is not None and tree_inverse is not None:
                generators.append(
                    word(tree_inverse, darts[1 - start_vertex, color], tree_voltage)
                )
        elif color != tree_color:
            assert tree_voltage is not None and tree_inverse is not None
            generators.append(
                word(tree_inverse, darts[start_vertex, color])
            )

    if not generators:
        generators = [IDENTITY]
    return (
        PermutationGroup([Permutation(list(g)) for g in generators]),
        tree_voltage,
    )


def group_elements(group: PermutationGroup) -> set[tuple[int, ...]]:
    order = int(group.order())
    if order > MAX_EXPLICIT_GROUP_ORDER:
        raise RuntimeError(
            f"refusing to enumerate group of order {order}; "
            f"hard limit is {MAX_EXPLICIT_GROUP_ORDER}"
        )
    elements = {
        tuple(permutation(i) for i in range(len(FLAGS)))
        for permutation in group.generate_schreier_sims()
    }
    assert len(elements) == order
    return elements


def in_group(value: tuple[int, ...], group: PermutationGroup) -> bool:
    return group.contains(Permutation(list(value)), strict=True)


def check_intersections(
    link_colors: frozenset[int],
    top: tuple[int, ...],
    *,
    emit: bool = True,
) -> bool:
    label = "-".join(map(str, sorted(link_colors)))
    passed = True
    # k=0 and m=3 are tautological.  Check every remaining k,m pair instead
    # of importing Theorem 6.4, whose recursive M_n hypothesis is unavailable
    # for the toroidal rank-3 replacement.
    for k in range(1, 4):
        for m in range(3):
            lower_allowed = set(range(0, m + 1))
            upper_allowed = set(range(k, 4))
            middle_allowed = set(range(k, m + 1)) if k <= m else set()
            for start in (0, 1):
                upper_group, upper_tree = voltage_group(
                    link_colors, upper_allowed, top, start
                )
                if emit and m == 0:
                    print(
                        f"links={label} k={k} start={start} "
                        f"upper_group_order={upper_group.order()}",
                        flush=True,
                    )
                lower_group, lower_tree = voltage_group(
                    link_colors, lower_allowed, top, start
                )
                middle_group, middle_tree = voltage_group(
                    link_colors, middle_allowed, top, start
                )
                lower_elements = group_elements(lower_group)
                middle_elements = group_elements(middle_group)

                # Independent finite-state traversal checks the spanning-tree generators.
                lower_direct = path_voltage_sets(
                    link_colors, lower_allowed, top, start_vertex=start
                )
                middle_direct = path_voltage_sets(
                    link_colors, middle_allowed, top, start_vertex=start
                )
                assert lower_direct[start] == lower_elements
                assert middle_direct[start] == middle_elements

                same_endpoint = start
                other_endpoint = 1 - start
                for endpoint in (same_endpoint, other_endpoint):
                    if endpoint == same_endpoint:
                        lhs = {value for value in lower_elements if in_group(value, upper_group)}
                        rhs = middle_elements
                    else:
                        if lower_tree is None:
                            lower_open: set[tuple[int, ...]] = set()
                        else:
                            lower_open = {word(lower_tree, value) for value in lower_elements}
                        assert lower_direct[other_endpoint] == lower_open
                        if upper_tree is None:
                            lhs = set()
                        else:
                            upper_tree_inverse = inverse(upper_tree)
                            lhs = {
                                value for value in lower_open
                                if in_group(word(upper_tree_inverse, value), upper_group)
                            }
                        if middle_tree is None:
                            rhs = set()
                        else:
                            rhs = {word(middle_tree, value) for value in middle_elements}
                        assert middle_direct[other_endpoint] == rhs
                    equal = lhs == rhs
                    passed &= equal
                    if emit:
                        print(
                            f"links={label} k={k} m={m} pair={start}->{endpoint} sizes="
                            f"{lower_group.order()},{upper_group.order()},{len(lhs)},{len(rhs)} "
                            f"equal={equal}",
                            flush=True,
                        )
    return passed


def check_maniplex_relations(link_colors: frozenset[int], top: tuple[int, ...]) -> None:
    darts = voltage_darts(link_colors, top)
    for start in (0, 1):
        for left in range(4):
            for right in range(left + 2, 4):
                endpoint = start
                value = IDENTITY
                for color in (left, right, left, right):
                    value = then(darts[endpoint, color], value)
                    endpoint ^= color in link_colors
                assert endpoint == start
                assert value == IDENTITY


def main() -> None:
    monodromy = generate(list(R))
    print(f"flags={len(FLAGS)} monodromy_order={len(monodromy)}", flush=True)
    for link_colors in (frozenset({0, 3}), frozenset({0, 1, 3}), frozenset({0, 2, 3})):
        label = "-".join(map(str, sorted(link_colors)))
        colors = flag_coloring(link_colors - {3})
        e = eta(link_colors)
        assert then(e, e) == IDENTITY
        assert all(colors[e[i]] == colors[i] for i in range(len(colors)))
        for face in product(range(N), repeat=2):
            assert len({FLAGS[e[i]].face for i, flag in enumerate(FLAGS) if flag.face == face}) == 8
        t = tilde_rho0(link_colors)
        y3 = word(t, R[0])
        print(
            f"links={label} eta_word={''.join(map(str, ETA_WORDS[link_colors - {3}]))} "
            f"eta_color_preserving=True top_involution={then(y3,y3)==IDENTITY}",
            flush=True,
        )
        darts = voltage_darts(link_colors, y3)
        for voltage in darts.values():
            assert all(colors[voltage[i]] == colors[i] for i in range(len(FLAGS)))
        semiedges_exact_involutions = all(
            darts[start, color] != IDENTITY
            and then(darts[start, color], darts[start, color]) == IDENTITY
            for start in (0, 1)
            for color in range(4)
            if color not in link_colors
        )
        parallel_link_voltages_distinct = all(
            len({darts[start, color] for color in link_colors}) == len(link_colors)
            for start in (0, 1)
        )
        assert semiedges_exact_involutions
        assert parallel_link_voltages_distinct
        print(
            f"links={label} semiedges_exact_involutions=True "
            f"parallel_link_voltages_distinct=True",
            flush=True,
        )
        check_maniplex_relations(link_colors, y3)
        assert check_intersections(link_colors, y3)

    # Destructive control: replacing the paper's top voltage by 1 must fail.
    negative_passed = check_intersections(frozenset({0, 3}), IDENTITY, emit=False)
    print(f"negative_control_wrong_top_voltage_passed={negative_passed}", flush=True)
    assert not negative_passed


if __name__ == "__main__":
    main()
