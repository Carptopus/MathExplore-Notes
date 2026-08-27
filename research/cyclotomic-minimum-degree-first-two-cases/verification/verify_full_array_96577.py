"""Exact full-array verifier for n=96577, separate from marginal evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


N = 96577
PRIMES = (13, 17, 19, 23)
BOUNDARY = 89148
POLYGON_SUPPORT = tuple(range(0, BOUNDARY + 1, N // PRIMES[0]))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def basis(prime: int) -> np.ndarray:
    result = np.zeros((prime, prime - 1), dtype=np.int64)
    result[0] = -1
    result[1:] = np.eye(prime - 1, dtype=np.int64)
    return result


def coordinates(index: int) -> tuple[int, int, int, int]:
    return tuple(
        index * pow(N // prime, -1, prime) % prime
        for prime in PRIMES
    )  # type: ignore[return-value]


def verify(certificate_path: Path, metadata_path: Path) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if (
        int(metadata["n"]) != N
        or tuple(metadata["primes"]) != PRIMES
        or int(metadata["boundary"]) != BOUNDARY
        or tuple(metadata["polygon_support"]) != POLYGON_SUPPORT
    ):
        raise AssertionError("metadata is not anchored to n=96577")
    if sha256(certificate_path) != metadata["certificate_sha256"]:
        raise AssertionError("certificate SHA-256 mismatch")
    coefficient_array = np.load(certificate_path, allow_pickle=False)["certificate"]
    expected_shape = tuple(prime - 1 for prime in PRIMES)
    if coefficient_array.dtype != np.int64 or coefficient_array.size != int(np.prod(expected_shape)):
        raise AssertionError((coefficient_array.dtype, coefficient_array.shape))
    coefficient_array = coefficient_array.reshape(expected_shape)
    bases = tuple(basis(prime) for prime in PRIMES)
    full = np.einsum(
        "ai,bj,ck,dl,ijkl->abcd",
        bases[0],
        bases[1],
        bases[2],
        bases[3],
        coefficient_array,
        optimize=True,
        dtype=np.int64,
    )
    fiber_max = [
        int(np.max(np.abs(full.sum(axis=axis, dtype=np.int64))))
        for axis in range(4)
    ]
    if any(fiber_max):
        raise AssertionError(("fiber sums", fiber_max))
    values = np.fromiter(
        (int(full[coordinates(index)]) for index in range(BOUNDARY + 1)),
        dtype=np.int64,
        count=BOUNDARY + 1,
    )
    polygon = values[np.asarray(POLYGON_SUPPORT, dtype=np.int64)]
    outside_mask = np.ones(values.size, dtype=bool)
    outside_mask[np.asarray(POLYGON_SUPPORT, dtype=np.int64)] = False
    outside = values[outside_mask]
    if np.any(polygon != 0) or np.any(outside >= 0):
        raise AssertionError((polygon.tolist(), int(outside.max())))
    return {
        "result": "PASS",
        "n": N,
        "certificate_sha256": metadata["certificate_sha256"],
        "full_array_shape": full.shape,
        "fiber_sum_abs_max_by_axis": fiber_max,
        "checked_positions": int(values.size),
        "polygon_values": polygon.tolist(),
        "outside_functional_min": int(outside.min()),
        "outside_functional_max": int(outside.max()),
        "outside_nonnegative_count": int(np.count_nonzero(outside >= 0)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    print(verify(args.certificate, args.metadata))


if __name__ == "__main__":
    main()
