"""Check the explicit K4/K6 examples; this does not prove the infinite classifications."""

import itertools
import json


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def pair(a, b):
    return tuple(sorted((a, b)))


def is_cycle(vertices, adjacencies):
    vertices = set(vertices)
    if len(vertices) < 3:
        return False
    neighbors = {v: set() for v in vertices}
    for a, b in adjacencies:
        if a not in vertices or b not in vertices or a == b:
            return False
        neighbors[a].add(b)
        neighbors[b].add(a)
    if any(len(nbrs) != 2 for nbrs in neighbors.values()):
        return False
    seen = set()
    pending = [next(iter(vertices))]
    while pending:
        v = pending.pop()
        if v not in seen:
            seen.add(v)
            pending.extend(neighbors[v] - seen)
    return seen == vertices


def all_bonds(n):
    # In a complete graph every nonempty proper vertex set is a bond side.
    # Fix vertex zero in the side to count complementary descriptions once.
    edges = list(itertools.combinations(range(n), 2))
    for mask in range(1, 1 << n, 2):
        if mask == (1 << n) - 1:
            continue
        yield {e for e in edges if ((mask >> e[0]) & 1) != ((mask >> e[1]) & 1)}


def check_bond_cycles(n, adjacency):
    count = 0
    for bond in all_bonds(n):
        induced = {a for a in adjacency if a[0] in bond and a[1] in bond}
        require(is_cycle(bond, induced), f"K{n}: bond is not a single cycle: {sorted(bond)}")
        count += 1
    require(count == (1 << (n - 1)) - 1, "Incomplete bond enumeration")
    return count


def check_complex(n, faces):
    require(n in (4, 6), "Only the fixed K4/K6 examples are supported")
    require(all(len(f) == 3 and len(set(f)) == 3 for f in faces), "Malformed face")
    require(all(isinstance(v, int) and 0 <= v < n for f in faces for v in f), "Invalid vertex")
    normalized = [tuple(sorted(f)) for f in faces]
    require(len(set(normalized)) == len(normalized), "Duplicate face")
    edges = set(itertools.combinations(range(n), 2))
    incidence = {e: 0 for e in edges}
    adjacency = set()
    for f in normalized:
        face_edges = list(itertools.combinations(f, 2))
        for e in face_edges:
            incidence[e] += 1
        adjacency.update(pair(a, b) for a, b in itertools.combinations(face_edges, 2))
    require(all(value == 2 for value in incidence.values()), "Edge-face incidence is not two")
    for v in range(n):
        link_edges = {tuple(x for x in f if x != v) for f in normalized if v in f}
        require(is_cycle(set(range(n)) - {v}, link_edges), f"Link at {v} is not a cycle")
    count = check_bond_cycles(n, adjacency)
    return {"n": n, "faces": len(faces), "edges": len(edges),
            "euler_characteristic": n - len(edges) + len(faces),
            "bonds_checked": count, "adjacency_count": len(adjacency)}, adjacency


def expect_rejection(call):
    try:
        call()
    except InvalidCertificate:
        return
    raise RuntimeError("Negative control incorrectly accepted")


def main():
    examples = {
        4: list(itertools.combinations(range(4), 3)),
        6: [tuple(map(int, f)) for f in
            "013 014 024 025 035 123 125 145 234 345".split()],
    }
    output = {"scope": "finite positive examples only", "examples": []}
    # Sanity checks target degree-only validation and disconnected false positives.
    require(is_cycle(range(3), {(0, 1), (1, 2), (0, 2)}), "Triangle positive control")
    require(not is_cycle(range(6), {(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)}),
            "Disconnected two-regular negative control")
    for n, faces in examples.items():
        result, adjacency = check_complex(n, faces)
        for i in range(len(faces)):
            expect_rejection(lambda i=i: check_complex(n, faces[:i] + faces[i + 1:]))
        expect_rejection(lambda: check_complex(n, faces + [faces[0]]))
        for a in adjacency:
            expect_rejection(lambda a=a: check_bond_cycles(n, adjacency - {a}))
        nonadjacent = set(itertools.combinations(sorted(itertools.combinations(range(n), 2)), 2)) - adjacency
        for a in nonadjacent:
            expect_rejection(lambda a=a: check_bond_cycles(n, adjacency | {a}))
        result["negative_controls"] = {
            "face_deletions_rejected": len(faces), "duplicate_face_rejected": 1,
            "adjacency_deletions_rejected": len(adjacency),
            "adjacency_insertions_rejected": len(nonadjacent),
        }
        output["examples"].append(result)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
