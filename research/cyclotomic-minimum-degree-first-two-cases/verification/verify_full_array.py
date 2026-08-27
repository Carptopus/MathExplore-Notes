"""Exact full-array verifier independent of the marginal-evaluation implementation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


N = 46189
PRIMES = (11, 13, 17, 19)
BOUNDARY = 41990
POLYGON_SUPPORT = tuple(range(0, BOUNDARY + 1, N // PRIMES[0]))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def basis_matrix(prime: int) -> np.ndarray:
    matrix = np.zeros((prime, prime - 1), dtype=np.int64)
    matrix[0, :] = -1
    matrix[1:, :] = np.eye(prime - 1, dtype=np.int64)
    return matrix


def expand_certificate(coordinates: np.ndarray) -> np.ndarray:
    bases = tuple(basis_matrix(prime) for prime in PRIMES)
    return np.einsum(
        "ai,bj,ck,dl,ijkl->abcd",
        bases[0],
        bases[1],
        bases[2],
        bases[3],
        coordinates,
        optimize=True,
        dtype=np.int64,
    )


def exponent_coordinates(index: int) -> tuple[int, int, int, int]:
    return tuple(
        (index * pow(N // prime, -1, prime)) % prime
        for prime in PRIMES
    )  # type: ignore[return-value]


def verify(certificate_path: Path, metadata_path: Path, mode: str) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if int(metadata["n"]) != N or tuple(metadata["primes"]) != PRIMES:
        raise AssertionError("metadata is not anchored to n=46189")
    if file_sha256(certificate_path) != metadata["certificate_sha256"]:
        raise AssertionError("certificate SHA-256 mismatch")
    coordinates = np.load(certificate_path, allow_pickle=False)["certificate"]
    expected_shape = tuple(prime - 1 for prime in PRIMES)
    if coordinates.dtype != np.int64 or coordinates.size != int(np.prod(expected_shape)):
        raise AssertionError((coordinates.dtype, coordinates.shape, expected_shape))
    coordinates = coordinates.reshape(expected_shape)
    full_array = expand_certificate(coordinates)
    if full_array.shape != PRIMES:
        raise AssertionError(full_array.shape)

    fiber_max_abs = []
    for axis in range(len(PRIMES)):
        sums = full_array.sum(axis=axis, dtype=np.int64)
        fiber_max_abs.append(int(np.max(np.abs(sums))))
    if any(fiber_max_abs):
        raise AssertionError(("nonzero fiber sum", fiber_max_abs))

    limit = 41989 if mode == "minimum" else BOUNDARY
    values = np.fromiter(
        (int(full_array[exponent_coordinates(index)]) for index in range(limit + 1)),
        dtype=np.int64,
        count=limit + 1,
    )
    result: dict[str, object] = {
        "result": "PASS",
        "mode": mode,
        "n": N,
        "certificate_sha256": metadata["certificate_sha256"],
        "full_array_shape": full_array.shape,
        "fiber_sum_abs_max_by_axis": fiber_max_abs,
    }
    if mode == "minimum":
        if np.any(values >= 0):
            raise AssertionError((int(values.max()), int(np.count_nonzero(values >= 0))))
        result.update(
            {
                "checked_positions": int(values.size),
                "functional_min": int(values.min()),
                "functional_max": int(values.max()),
                "nonnegative_count": int(np.count_nonzero(values >= 0)),
            }
        )
        return result

    polygon_values = values[np.asarray(POLYGON_SUPPORT, dtype=np.int64)]
    outside_mask = np.ones(values.size, dtype=bool)
    outside_mask[np.asarray(POLYGON_SUPPORT, dtype=np.int64)] = False
    outside_values = values[outside_mask]
    if np.any(polygon_values != 0) or np.any(outside_values >= 0):
        raise AssertionError(
            (
                polygon_values.tolist(),
                int(outside_values.max()),
                int(np.count_nonzero(outside_values >= 0)),
            )
        )
    result.update(
        {
            "checked_positions": int(values.size),
            "polygon_values": polygon_values.tolist(),
            "outside_functional_min": int(outside_values.min()),
            "outside_functional_max": int(outside_values.max()),
            "outside_nonnegative_count": int(np.count_nonzero(outside_values >= 0)),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--mode", choices=("minimum", "boundary"), required=True)
    args = parser.parse_args()
    print(verify(args.certificate, args.metadata, args.mode))


if __name__ == "__main__":
    main()
