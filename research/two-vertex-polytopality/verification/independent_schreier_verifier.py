"""独立 rank-4 构造重建与交条件验证器。

本文件不导入 torus_rank4_probe。大群成员判定使用 SymPy 的确定性
Schreier--Sims；只有预先确认群阶不超过硬上限的小群才允许显式枚举。
"""

from __future__ import annotations

from collections import deque
from sympy.combinatorics import Permutation, PermutationGroup


N = 8
Flag = tuple[int, int, int, int]  # face x, face y, corner, boundary-edge index


def all_flags() -> list[Flag]:
    return [
        (x, y, corner, edge)
        for x in range(N)
        for y in range(N)
        for corner in range(4)
        for edge in ((corner - 1) % 4, corner)
    ]


FLAGS = all_flags()
INDEX = {flag: i for i, flag in enumerate(FLAGS)}
DEGREE = len(FLAGS)
IDENTITY = tuple(range(DEGREE))
MAX_EXPLICIT_GROUP_ORDER = 4_096


def adjacent(flag: Flag, color: int) -> Flag:
    x, y, corner, edge = flag
    if color == 0:
        other = (edge + 1) % 4 if corner == edge else edge
        return x, y, other, edge
    if color == 1:
        other_edge = corner if edge == (corner - 1) % 4 else (corner - 1) % 4
        return x, y, corner, other_edge
    if color != 2:
        raise ValueError(color)
    transitions = {
        (0, 0): (0, -1, 3, 2),
        (0, 1): (0, -1, 2, 2),
        (1, 1): (1, 0, 0, 3),
        (1, 2): (1, 0, 3, 3),
        (2, 2): (0, 1, 1, 0),
        (2, 3): (0, 1, 0, 0),
        (3, 3): (-1, 0, 2, 1),
        (3, 0): (-1, 0, 1, 1),
    }
    dx, dy, new_corner, new_edge = transitions[edge, corner]
    return (x + dx) % N, (y + dy) % N, new_corner, new_edge


R = tuple(tuple(INDEX[adjacent(flag, color)] for flag in FLAGS) for color in range(3))


def multiply(*permutations: tuple[int, ...]) -> tuple[int, ...]:
    """Right action: apply permutations from left to right."""
    value = IDENTITY
    for permutation in permutations:
        value = tuple(permutation[value[i]] for i in range(DEGREE))
    return value


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * DEGREE
    for i, image in enumerate(permutation):
        result[image] = i
    return tuple(result)


def closure(
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
    result = {IDENTITY}
    queue = deque([IDENTITY])
    while queue:
        value = queue.popleft()
        for generator in generators:
            nxt = multiply(value, generator)
            if nxt not in result:
                result.add(nxt)
                queue.append(nxt)
                if len(result) > limit:
                    raise RuntimeError(f"closure exceeded {limit}")
    assert len(result) == exact_order
    return result


def color_flags(link_colors_below_top: frozenset[int]) -> tuple[int, ...]:
    colors = [-1] * DEGREE
    colors[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for color, generator in enumerate(R):
            j = generator[i]
            expected = colors[i] ^ (color in link_colors_below_top)
            if colors[j] == -1:
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
    return multiply(*(R[color] for color in ETA_WORDS[link_colors - {3}]))


def reflect_in_face(flag: Flag, horizontal_base: bool) -> Flag:
    x, y, corner, edge = flag
    if horizontal_base:
        corner_map = (1, 0, 3, 2)
    else:
        corner_map = (3, 2, 1, 0)
    new_corner = corner_map[corner]
    endpoints = {corner_map[edge], corner_map[(edge + 1) % 4]}
    new_edge = next(j for j in range(4) if {j, (j + 1) % 4} == endpoints)
    return x, y, new_corner, new_edge


def tilde_rho0(link_colors: frozenset[int]) -> tuple[int, ...]:
    colors = color_flags(link_colors - {3})
    e = eta(link_colors)
    base_face = FLAGS[0][:2]
    forced: dict[tuple[int, int], bool] = {}

    def force_orientation(face: tuple[int, int], horizontal: bool) -> None:
        prior = forced.get(face)
        if prior is not None:
            # Opposite square edges induce the same reflection orientation.
            assert prior == horizontal
        else:
            forced[face] = horizontal

    base_eta_image = FLAGS[e[0]]
    force_orientation(base_eta_image[:2], base_eta_image[3] in {0, 2})
    for i, flag in enumerate(FLAGS):
        if flag[:2] != base_face or colors[i] != 1:
            continue
        image = FLAGS[e[i]]
        horizontal = image[3] in {0, 2}
        force_orientation(image[:2], horizontal)
    permutation = tuple(
        INDEX[reflect_in_face(flag, forced.get(flag[:2], True))]
        for flag in FLAGS
    )
    fixing = multiply(permutation, R[0])
    assert fixing[e[0]] == e[0]
    for i, flag in enumerate(FLAGS):
        if flag[:2] == base_face and colors[i] == 0:
            required = multiply(R[0], e, R[0])[i]
            assert fixing[required] == required
    return permutation


def dart_voltages(link_colors: frozenset[int], top: tuple[int, ...]):
    result: dict[tuple[int, int], tuple[int, ...]] = {}
    for start in (0, 1):
        for color in range(4):
            if color == 0:
                result[start, color] = IDENTITY
            elif color == 3:
                result[start, color] = top
            elif color in link_colors:
                result[start, color] = (
                    multiply(R[0], R[color])
                    if start == 0
                    else multiply(R[color], R[0])
                )
            else:
                result[start, color] = (
                    R[color]
                    if start == 0
                    else multiply(R[0], R[color], R[0])
                )
    return result


def voltage_generators(
    link_colors: frozenset[int],
    allowed: set[int],
    top: tuple[int, ...],
    start_vertex: int,
) -> tuple[list[tuple[int, ...]], tuple[int, ...] | None]:
    darts = dart_voltages(link_colors, top)
    links = sorted(allowed & link_colors)
    tree_color = links[0] if links else None
    tree = darts[start_vertex, tree_color] if tree_color is not None else None
    generators: list[tuple[int, ...]] = []
    for color in sorted(allowed):
        if color not in link_colors:
            generators.append(darts[start_vertex, color])
            if tree is not None:
                generators.append(
                    multiply(inverse(tree), darts[1 - start_vertex, color], tree)
                )
        elif color != tree_color:
            assert tree is not None
            generators.append(multiply(inverse(tree), darts[start_vertex, color]))
    return generators, tree


def verify_case(link_colors: frozenset[int]) -> list[tuple[int, int, int, int, int]]:
    e = eta(link_colors)
    colors = color_flags(link_colors - {3})
    assert multiply(e, e) == IDENTITY
    assert all(colors[e[i]] == colors[i] for i in range(DEGREE))
    for x in range(N):
        for y in range(N):
            assert len({
                FLAGS[e[i]][:2]
                for i, flag in enumerate(FLAGS)
                if flag[:2] == (x, y)
            }) == 8
    t = tilde_rho0(link_colors)
    top = multiply(t, R[0])
    assert multiply(top, top) == IDENTITY
    darts = dart_voltages(link_colors, top)
    assert all(
        colors[permutation[i]] == colors[i]
        for permutation in darts.values()
        for i in range(DEGREE)
    )
    assert all(
        darts[start, color] != IDENTITY
        and multiply(darts[start, color], darts[start, color]) == IDENTITY
        for start in (0, 1)
        for color in range(4)
        if color not in link_colors
    )
    assert all(
        len({darts[start, color] for color in link_colors}) == len(link_colors)
        for start in (0, 1)
    )
    for start in (0, 1):
        for left in range(4):
            for right in range(left + 2, 4):
                endpoint = start
                value = IDENTITY
                for color in (left, right, left, right):
                    value = multiply(darts[endpoint, color], value)
                    endpoint ^= color in link_colors
                assert endpoint == start and value == IDENTITY
    rows = []
    for start in (0, 1):
        for k in range(1, 4):
            upper_generators, upper_tree = voltage_generators(
                link_colors, set(range(k, 4)), top, start
            )
            upper_sympy = PermutationGroup(
                [Permutation(list(generator)) for generator in upper_generators]
            )
            upper_order = int(upper_sympy.order())
            assert upper_order > 0
            if upper_order > MAX_EXPLICIT_GROUP_ORDER:

                def upper_contains(value: tuple[int, ...]) -> bool:
                    return upper_sympy.contains(Permutation(list(value)), strict=True)

            else:
                upper_elements = closure(
                    upper_generators,
                    limit=MAX_EXPLICIT_GROUP_ORDER,
                )
                assert len(upper_elements) == upper_order

                def upper_contains(value: tuple[int, ...]) -> bool:
                    return value in upper_elements
            for m in range(3):
                lower_generators, lower_tree = voltage_generators(
                    link_colors, set(range(m + 1)), top, start
                )
                middle_generators, middle_tree = voltage_generators(
                    link_colors, set(range(k, m + 1)) if k <= m else set(), top, start
                )
                lower = closure(lower_generators)
                middle = closure(middle_generators)
                closed_intersection = {
                    x for x in lower
                    if upper_contains(x)
                }
                assert closed_intersection == middle
                lower_open = (
                    {multiply(lower_tree, x) for x in lower}
                    if lower_tree is not None
                    else set()
                )
                if upper_tree is None:
                    open_intersection = set()
                else:
                    open_intersection = {
                        x for x in lower_open
                        if upper_contains(multiply(inverse(upper_tree), x))
                    }
                middle_open = (
                    {multiply(middle_tree, x) for x in middle}
                    if middle_tree is not None
                    else set()
                )
                assert open_intersection == middle_open
                rows.append(
                    (k, m, start, len(closed_intersection), len(open_intersection))
                )
    return rows


def main() -> None:
    assert len(closure(list(R))) == 512
    for links in (frozenset({0, 3}), frozenset({0, 1, 3}), frozenset({0, 2, 3})):
        print(f"verifying_links={sorted(links)}", flush=True)
        print(
            f"links={sorted(links)} eta_word={''.join(map(str, ETA_WORDS[links - {3}]))} "
            f"rows={verify_case(links)}",
            flush=True,
        )
    print("independent_schreier_verifier=PASS", flush=True)


if __name__ == "__main__":
    main()
