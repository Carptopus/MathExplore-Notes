"""转移候选的固定原对象控制；不承担一般证明及新颖性。"""

import argparse
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def binary_rank(values):
    pivots = {}
    for value in values:
        while value:
            key = value.bit_length() - 1
            if key in pivots:
                value ^= pivots[key]
            else:
                pivots[key] = value
                break
    return len(pivots)


def values(rank, ground):
    total_rank = rank(ground)
    bases, t02 = 0, 0
    for mask in range(1 << len(ground)):
        chosen = tuple(ground[i] for i in range(len(ground)) if mask & (1 << i))
        selected_rank = rank(chosen)
        t02 += (-1) ** (total_rank - selected_rank)
        bases += int(len(chosen) == selected_rank == total_rank)
    return t02, bases


def check(name, size, rank, flat, k, accepted):
    require(size <= 14, "固定原子集规模硬门14元")
    ground = tuple(range(size))
    flat = set(flat)
    outside = tuple(i for i in ground if i not in flat)
    total_rank = rank(ground)
    flat_rank = rank(flat)
    require(all(rank((i,)) == 1 for i in ground), "原对象有圈元")
    require(all(rank(tuple(j for j in ground if j != i)) == total_rank for i in ground),
            "原对象有余圈元")
    require(all(rank((*flat, i)) > flat_rank for i in outside), "指定F不是平坦")
    large = set()
    for i in flat:
        mates = {j for j in ground if rank((i, j)) == 1}
        if len(mates) >= k:
            large.update(mates)
    spans = rank(large) == flat_rank
    c = total_rank - flat_rank
    s = len(outside) - c
    tq, bq = values(lambda subset: rank((*flat, *subset)) - flat_rank, outside)
    tm, bm = values(rank, ground)
    hypotheses = spans and tq >= bq and 2 * (2 ** k - 1 - k) >= s
    require(hypotheses == accepted, f"{name}:前提控制不符")
    if accepted:
        require(tm >= bm, f"{name}:候选传递结论失败")
        if tq > bq:
            require(tm > bm, f"{name}:商严格性未传递")
    return {"name": name, "size": size, "h": flat_rank, "c": c, "s": s,
            "k": k, "quotient_T02": tq, "quotient_bases": bq,
            "T02": tm, "bases": bm, "hypotheses": hypotheses,
            "subsets": (1 << size) + (1 << len(outside))}


def vector_case(name, columns, flat, k):
    return check(name, len(columns),
                 lambda subset: binary_rank(columns[i] for i in subset), flat, k, True)


def theta_case(c, multiplicity, k, accepted):
    edges = [(0, 1)] * multiplicity
    for i in range(c):
        edges.extend(((0, i + 2), (i + 2, 1)))

    def rank(subset):
        parents = list(range(c + 2))

        def root(i):
            while parents[i] != i:
                i = parents[i]
            return i

        score = 0
        for i in subset:
            a, b = map(root, edges[i])
            if a != b:
                parents[a] = b
                score += 1
        return score

    return check(f"theta_c{c}_multiplicity{multiplicity}", len(edges), rank,
                 range(multiplicity), k, accepted)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "不覆盖既有控制证据")
    rows = [
        vector_case("independent_support", (1, 1, 1, 2, 2, 2, 4, 5, 6, 7), range(6), 3),
        vector_case("internal_singleton", (1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7), range(7), 3),
        vector_case("dependent_support", (1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7), range(9), 3),
        vector_case("internal_small_class", (1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7), range(8), 3),
        vector_case("equality_parallel_pair", (1, 1), range(2), 2),
        theta_case(4, 3, 3, True),
        theta_case(4, 2, 2, False),
    ]
    packet = {"scope": "seven fixed original-vector/graph controls, not a general proof",
              "cases": rows, "subsets_checked": sum(row["subsets"] for row in rows)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(packet, ensure_ascii=False))


if __name__ == "__main__":
    main()
