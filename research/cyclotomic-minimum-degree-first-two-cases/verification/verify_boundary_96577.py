"""Independent exact marginal verifier for the n=96577 boundary certificate."""

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


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def crt_coordinates(index: int) -> tuple[int, int, int, int]:
    return tuple(
        (index * pow(N // prime, -1, prime)) % prime
        for prime in PRIMES
    )  # type: ignore[return-value]


def build_marginals(certificate: np.ndarray) -> dict[int, np.ndarray | np.int64]:
    marginals: dict[int, np.ndarray | np.int64] = {}
    for nonzero_mask in range(1 << len(PRIMES)):
        zero_axes = tuple(
            axis for axis in range(len(PRIMES))
            if not nonzero_mask & (1 << axis)
        )
        marginals[nonzero_mask] = (
            certificate.sum(axis=zero_axes, dtype=np.int64)
            if zero_axes
            else certificate
        )
    return marginals


def evaluate(
    coordinates: tuple[int, int, int, int],
    marginals: dict[int, np.ndarray | np.int64],
) -> int:
    nonzero_mask = sum(
        1 << axis
        for axis, coordinate in enumerate(coordinates)
        if coordinate != 0
    )
    marginal = marginals[nonzero_mask]
    lookup = tuple(coordinate - 1 for coordinate in coordinates if coordinate != 0)
    value = int(marginal[lookup]) if lookup else int(marginal)
    return -value if (len(PRIMES) - nonzero_mask.bit_count()) % 2 else value


def verify(certificate_path: Path, metadata_path: Path) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("schema") != "cyclotomic-boundary-uniqueness-certificate-v1":
        raise AssertionError("unexpected metadata schema")
    if (
        int(metadata["n"]) != N
        or tuple(int(value) for value in metadata["primes"]) != PRIMES
        or int(metadata["boundary"]) != BOUNDARY
        or tuple(int(value) for value in metadata["polygon_support"]) != POLYGON_SUPPORT
    ):
        raise AssertionError("metadata is not anchored to n=96577")
    if BOUNDARY != (PRIMES[0] - 1) * N // PRIMES[0]:
        raise AssertionError("boundary formula mismatch")
    if file_sha256(certificate_path) != metadata["certificate_sha256"]:
        raise AssertionError("certificate SHA-256 mismatch")

    certificate = np.load(certificate_path, allow_pickle=False)["certificate"]
    expected_shape = tuple(prime - 1 for prime in PRIMES)
    if certificate.dtype != np.int64 or certificate.size != int(np.prod(expected_shape)):
        raise AssertionError((certificate.dtype, certificate.shape, expected_shape))
    certificate = certificate.reshape(expected_shape)
    marginals = build_marginals(certificate)

    polygon_set = set(POLYGON_SUPPORT)
    polygon_values: list[int] = []
    outside_values: list[int] = []
    for index in range(BOUNDARY + 1):
        value = evaluate(crt_coordinates(index), marginals)
        (polygon_values if index in polygon_set else outside_values).append(value)
    outside = np.asarray(outside_values, dtype=np.int64)
    if any(polygon_values) or np.any(outside >= 0):
        raise AssertionError((polygon_values, int(outside.max())))
    return {
        "result": "PASS",
        "n": N,
        "primes": PRIMES,
        "boundary": BOUNDARY,
        "certificate_shape": certificate.shape,
        "certificate_sha256": metadata["certificate_sha256"],
        "polygon_values": polygon_values,
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
