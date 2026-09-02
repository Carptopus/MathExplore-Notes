"""Verify the published small-order upper witnesses for wsat(K_n, Q_3)."""

from __future__ import annotations

import json
from pathlib import Path

from probe_q3_weak_saturation import closure, closure_wide, cube_masks, cube_masks_wide


WITNESSES = {
    10: [
        (0, 6), (0, 9), (1, 5), (1, 6), (1, 7), (1, 9), (2, 4), (2, 9),
        (3, 4), (3, 6), (3, 8), (3, 9), (4, 7), (5, 6), (5, 7), (6, 7),
        (7, 8), (8, 9),
    ],
    11: [
        (0, 6), (0, 9), (1, 5), (1, 6), (1, 7), (1, 9), (2, 4), (2, 9),
        (4, 7), (5, 6), (5, 7), (6, 7), (7, 8), (8, 9), (3, 10), (3, 4),
        (3, 6), (8, 10), (3, 9),
    ],
    12: [
        (0, 4), (0, 8), (0, 9), (0, 11), (1, 7), (1, 9), (2, 4), (2, 6),
        (2, 8), (3, 6), (3, 8), (4, 7), (4, 8), (4, 10), (5, 6), (5, 7),
        (5, 9), (5, 11), (7, 10), (8, 11), (10, 11),
    ],
    13: [
        (0, 7), (0, 11), (1, 5), (1, 12), (2, 3), (2, 9), (2, 12), (3, 4),
        (3, 9), (4, 10), (4, 11), (5, 8), (5, 10), (5, 11), (5, 12), (6, 8),
        (6, 9), (6, 11), (7, 8), (7, 10), (8, 9), (8, 12), (9, 10),
    ],
}


def verify(n: int, witness: list[tuple[int, int]]) -> dict[str, object]:
    if n <= 11:
        edges, cubes = cube_masks(n)
        close = closure
    else:
        edges, cubes = cube_masks_wide(n)
        close = closure_wide
    edge_index = {edge: i for i, edge in enumerate(edges)}
    mask = sum(1 << edge_index[tuple(sorted(edge))] for edge in witness)
    full = (1 << len(edges)) - 1
    closed = close(mask, cubes, full)
    return {
        "n": n,
        "initial_edges": len(witness),
        "closed_edges": closed.bit_count(),
        "complete_graph_edges": len(edges),
        "verified": closed == full,
        "witness": witness,
    }


def main() -> None:
    results = [verify(n, witness) for n, witness in sorted(WITNESSES.items())]
    assert all(result["verified"] for result in results)
    output = Path(__file__).parent / "results" / "small-order-upper-witnesses.json"
    output.write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps([{k: v for k, v in result.items() if k != "witness"} for result in results]))


if __name__ == "__main__":
    main()
