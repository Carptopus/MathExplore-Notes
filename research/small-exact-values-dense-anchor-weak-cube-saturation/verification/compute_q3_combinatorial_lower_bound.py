"""Compute the Terekhov--Zhukovskii g* lower bound for Q_3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# e_i = min_{|S|=i} |E(Q3) \ E(Q3-S)| - 1, for i=1,...,7.
E_COSTS = (0, 2, 4, 6, 7, 9, 10, 11)


def g_star(limit: int) -> list[int]:
    values = [0] + [10**9] * limit
    for total in range(1, limit + 1):
        values[total] = min(
            values[total - part] + E_COSTS[part]
            for part in range(1, min(7, total) + 1)
        )
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=50)
    args = parser.parse_args()
    values = g_star(args.max_n - 8)
    remainder_costs = [0, 2, 4, 6, 7, 9, 10]
    periodic = all(
        values[t] == 11 * (t // 7) + remainder_costs[t % 7]
        for t in range(len(values))
    )
    assert periodic
    result = {
        "pattern": "Q3",
        "e_i_for_i_1_to_7": list(E_COSTS[1:]),
        "formula": "if n-8 = 7q+r, lower bound = 11+11q+h[r]",
        "h": remainder_costs,
        "verified_through_n": args.max_n,
        "periodic_formula_verified": periodic,
        "values": {str(n): 11 + values[n - 8] for n in range(8, args.max_n + 1)},
    }
    output = Path(__file__).parent / "results" / "q3-combinatorial-lower-bound.json"
    output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({k: v for k, v in result.items() if k != "values"}))


if __name__ == "__main__":
    main()
