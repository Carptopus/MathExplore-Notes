"""Verify one concrete application of the dense-anchor extension lemma."""

from __future__ import annotations

import json
from pathlib import Path

from probe_q3_weak_saturation import closure_wide, cube_masks_wide


HERE = Path(__file__).parent


def main() -> None:
    old = json.loads((HERE / "results" / "exact-first-cube-n8.json").read_text(encoding="utf-8"))
    block = json.loads(
        (HERE / "results" / "q3-k11-k7-anchor-certificate.json").read_text(
            encoding="utf-8"
        )
    )
    old_edges = [tuple(edge) for edge in old["witness"]]

    # Block vertices 0,...,6 are old anchors.  Its vertices 7,...,10 become
    # new host vertices 8,...,11.
    mapping = {**{i: i for i in range(7)}, **{i: i + 1 for i in range(7, 11)}}
    paid_block_edges = [
        tuple(sorted((mapping[u], mapping[v])))
        for u, v in block["initial_edges"]
        if u >= 7 or v >= 7
    ]
    initial_edges = sorted(set(old_edges + paid_block_edges))
    assert len(paid_block_edges) == 7
    assert len(initial_edges) == 22

    n = 12
    edges, cubes = cube_masks_wide(n)
    edge_index = {edge: i for i, edge in enumerate(edges)}
    mask = sum(1 << edge_index[edge] for edge in initial_edges)
    full = (1 << len(edges)) - 1
    closed = closure_wide(mask, cubes, full)
    result = {
        "old_order": 8,
        "new_order": 12,
        "old_seed_edges": len(old_edges),
        "paid_block_edges": len(paid_block_edges),
        "initial_edges": len(initial_edges),
        "closed_edges": closed.bit_count(),
        "complete_graph_edges": len(edges),
        "verified": closed == full,
        "initial_edge_list": initial_edges,
    }
    assert result["verified"]
    output = HERE / "results" / "dense-anchor-extension-k8-to-k12.json"
    output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({k: v for k, v in result.items() if k != "initial_edge_list"}))


if __name__ == "__main__":
    main()
