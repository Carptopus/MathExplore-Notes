"""Build and verify a sequential Q_3 activation certificate for a small seed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from probe_q3_weak_saturation import cube_masks, cube_masks_wide


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--n", type=int)
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    if isinstance(source, list):
        if args.n is None:
            raise ValueError("--n is required when the input contains several witnesses")
        source = next(item for item in source if int(item["n"]) == args.n)
    n = int(source["n"])
    witness = source.get("witness") or source.get("witness_if_complete")
    if witness is None:
        raise ValueError("input does not contain a complete witness")

    if n <= 11:
        edges, cube_array = cube_masks(n)
        cubes = [int(mask) for mask in cube_array]
    else:
        edges, (cube_low, cube_high) = cube_masks_wide(n)
        cubes = [
            int(low) | (int(high) << 64)
            for low, high in zip(cube_low, cube_high, strict=True)
        ]
    edge_index = {edge: i for i, edge in enumerate(edges)}
    current = sum(1 << edge_index[tuple(sorted(edge))] for edge in witness)
    full = (1 << len(edges)) - 1
    steps: list[dict[str, object]] = []

    while current != full:
        chosen_cube = None
        chosen_missing = None
        for cube in cubes:
            missing = cube & ~current
            if missing and missing & (missing - 1) == 0:
                chosen_cube = cube
                chosen_missing = missing.bit_length() - 1
                break
        if chosen_cube is None or chosen_missing is None:
            raise AssertionError("certificate construction got stuck")
        cube_edges = [edges[i] for i in range(len(edges)) if chosen_cube >> i & 1]
        steps.append(
            {
                "step": len(steps) + 1,
                "added_edge": edges[chosen_missing],
                "cube_edges_after_addition": cube_edges,
            }
        )
        current |= 1 << chosen_missing

    replay = sum(1 << edge_index[tuple(sorted(edge))] for edge in witness)
    for item in steps:
        cube = sum(
            1 << edge_index[tuple(sorted(edge))]
            for edge in item["cube_edges_after_addition"]
        )
        added = edge_index[tuple(item["added_edge"])]
        assert cube & ~replay == 1 << added
        replay |= 1 << added
    assert replay == full

    result = {
        "n": n,
        "initial_edge_count": len(witness),
        "initial_edges": witness,
        "activation_step_count": len(steps),
        "steps": steps,
        "verified": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({k: v for k, v in result.items() if k not in {"initial_edges", "steps"}}))


if __name__ == "__main__":
    main()
