"""Regenerate the normalized list of sharp bases required by the conductor."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from verify_fano_graded_conductor import main as build_conductor


def main() -> None:
    bases = build_conductor()
    lines = [" ".join(map(str, profile)) for profile in sorted(bases)]
    payload = ("\n".join(lines) + "\n").encode("ascii")
    target = Path(__file__).resolve().parent / "results" / "required_sharp_bases.tsv"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    print(f"wrote={target.name} bases={len(lines)} sha256={sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
