"""Fail-closed certificate for the candidate counterexample M*(K6).

No optimizer is used.  The six local rotations are frozen explicitly.  The
checker reconstructs their global adjacency relation, enumerates all 31 bonds
of K6, and verifies that every bond induces one cycle.  It also constructs a
binary representation of M*(K6) and checks the matroid 3-connectivity
inequality on every relevant ground-set bipartition.
"""

from __future__ import annotations

from itertools import combinations


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}

# A reversible cyclic order of the five edges incident with each K6 vertex,
# recorded by their other endpoints.
ROTATIONS = {
    0: (1, 3, 5, 2, 4),
    1: (0, 3, 2, 5, 4),
    2: (0, 4, 3, 1, 5),
    3: (0, 1, 2, 4, 5),
    4: (0, 1, 5, 3, 2),
    5: (0, 2, 1, 4, 3),
}


def require(condition: bool, message: object) -> None:
    """Raise an unconditional verification error, including under python -O."""
    if not condition:
        raise RuntimeError(message)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def adjacency_certificate() -> set[tuple[tuple[int, int], tuple[int, int]]]:
    selected = set()
    for vertex, rotation in ROTATIONS.items():
        require(
            set(rotation) == set(VERTICES) - {vertex},
            ("invalid rotation", vertex, rotation),
        )
        for index, left in enumerate(rotation):
            right = rotation[(index + 1) % len(rotation)]
            selected.add(tuple(sorted((edge(vertex, left), edge(vertex, right)))))
    require(len(selected) == 30, ("wrong adjacency count", len(selected)))
    return selected


def canonical_bonds() -> list[tuple[int, frozenset[tuple[int, int]]]]:
    output = []
    full = (1 << len(VERTICES)) - 1
    for mask in range(1, full):
        complement = full ^ mask
        if mask > complement:
            continue
        side = {vertex for vertex in VERTICES if mask & (1 << vertex)}
        cut = frozenset(
            edge(u, v) for u, v in EDGES if (u in side) != (v in side)
        )
        output.append((mask, cut))
    require(len(output) == 31, ("wrong bond count", len(output)))
    return output


def induced_cycle(
    bond: frozenset[tuple[int, int]],
    selected: set[tuple[tuple[int, int], tuple[int, int]]],
) -> tuple[tuple[int, int], ...]:
    neighbors = {element: [] for element in bond}
    for left, right in selected:
        if left in bond and right in bond:
            neighbors[left].append(right)
            neighbors[right].append(left)
    require(
        all(len(values) == 2 for values in neighbors.values()),
        ("bond is not 2-regular", bond, neighbors),
    )

    start = min(bond)
    previous = None
    current = start
    order = []
    while True:
        order.append(current)
        choices = sorted(neighbors[current])
        following = choices[0] if choices[0] != previous else choices[1]
        previous, current = current, following
        if current == start:
            break
        require(current not in order, ("premature cycle closure", bond, order))
    require(
        len(order) == len(bond),
        ("bond restriction is disconnected", bond, order),
    )
    return tuple(order)


def gf2_rank(columns: list[int]) -> int:
    basis: dict[int, int] = {}
    for column in columns:
        value = column
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def cographic_columns() -> list[int]:
    """Represent M*(K6) by a basis of the binary cycle space of K6."""
    tree = {edge(0, vertex) for vertex in range(1, 6)}
    cotree = [item for item in EDGES if item not in tree]
    require(len(cotree) == 10, ("wrong cycle-space dimension", len(cotree)))
    rows = []
    for u, v in cotree:
        cycle = {edge(u, v), edge(0, u), edge(0, v)}
        row = sum(1 << EDGE_INDEX[item] for item in cycle)
        rows.append(row)
    columns = []
    for column_index in range(len(EDGES)):
        value = sum(
            (1 << row_index)
            for row_index, row in enumerate(rows)
            if row & (1 << column_index)
        )
        columns.append(value)
    require(gf2_rank(columns) == 10, "cographic representation lost rank")
    return columns


def verify_three_connectivity() -> None:
    columns = cographic_columns()
    full_rank = gf2_rank(columns)
    ground_size = len(columns)
    for mask in range(1 << ground_size):
        size = mask.bit_count()
        if size < 2 or ground_size - size < 2:
            continue
        if size * 2 > ground_size:
            continue
        left = [columns[index] for index in range(ground_size) if mask & (1 << index)]
        right = [columns[index] for index in range(ground_size) if not mask & (1 << index)]
        connectivity = gf2_rank(left) + gf2_rank(right) - full_rank
        require(connectivity >= 2, ("2-separation", mask, size, connectivity))


def main() -> None:
    selected = adjacency_certificate()
    size_distribution: dict[int, int] = {}
    cycles = []
    for mask, bond in canonical_bonds():
        cycle = induced_cycle(bond, selected)
        size_distribution[len(bond)] = size_distribution.get(len(bond), 0) + 1
        cycles.append((mask, cycle))
    require(
        size_distribution == {5: 6, 8: 15, 9: 10},
        ("wrong bond-size distribution", size_distribution),
    )

    # Every frozen adjacency is essential already on one of the 31 bonds.
    for removed in selected:
        damaged = selected - {removed}
        require(
            any(
                not all(
                    sum(
                        1
                        for pair in damaged
                        if element in pair and pair[0] in bond and pair[1] in bond
                    )
                    == 2
                    for element in bond
                )
                for _, bond in canonical_bonds()
            ),
            ("nonessential frozen adjacency", removed),
        )

    verify_three_connectivity()

    # K6 is nonplanar already by the simple-planar edge bound 15 > 3*6-6.
    require(
        len(EDGES) == 15 and 15 > 3 * len(VERTICES) - 6,
        "K6 planar edge-bound check failed",
    )

    print("PASS: frozen adjacency relation has 30 pairs")
    print("PASS: all 31 K6 bonds induce one cycle")
    print(f"PASS: bond-size distribution {size_distribution}")
    print("PASS: binary representation satisfies every 3-connectivity cut")
    print("PASS: K6 violates the simple-planar edge bound")
    print("CANDIDATE: M*(K6) is a 3-connected regular non-graphic orderable matroid")


if __name__ == "__main__":
    main()
