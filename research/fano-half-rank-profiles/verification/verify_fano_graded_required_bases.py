"""Check that the frozen 812-base list equals the current conductor output."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from verify_fano_graded_conductor import main as build_conductor


def main() -> None:
    target = Path(__file__).resolve().parent / "results" / "required_sharp_bases.tsv"
    payload = target.read_bytes()
    frozen = {
        tuple(map(int, line.split()))
        for line in payload.decode("ascii").splitlines()
        if line.strip()
    }
    current = build_conductor()
    assert len(frozen) == 812
    assert frozen == current
    print(
        f"required_bases={len(frozen)} sha256={sha256(payload).hexdigest()}"
    )
    print("PASS: frozen required sharp bases equal the conductor output")


if __name__ == "__main__":
    main()
