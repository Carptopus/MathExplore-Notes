"""Independent exact verifier for the n=46189 boundary uniqueness certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def crt_coordinates(index: int, n: int, primes: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        (index * pow(n // prime, -1, prime)) % prime
        for prime in primes
    )


def build_marginals(certificate: np.ndarray) -> dict[int, np.ndarray | np.int64]:
    dimension = certificate.ndim
    marginals: dict[int, np.ndarray | np.int64] = {}
    for nonzero_mask in range(1 << dimension):
        zero_axes = tuple(
            axis for axis in range(dimension)
            if not nonzero_mask & (1 << axis)
        )
        marginals[nonzero_mask] = (
            certificate.sum(axis=zero_axes, dtype=np.int64)
            if zero_axes
            else certificate
        )
    return marginals


def evaluate(
    coordinates: tuple[int, ...],
    marginals: dict[int, np.ndarray | np.int64],
) -> int:
    nonzero_mask = sum(
        (1 << axis)
        for axis, coordinate in enumerate(coordinates)
        if coordinate != 0
    )
    marginal = marginals[nonzero_mask]
    lookup = tuple(coordinate - 1 for coordinate in coordinates if coordinate != 0)
    value = int(marginal[lookup]) if lookup else int(marginal)
    return -value if (len(coordinates) - nonzero_mask.bit_count()) % 2 else value


def verify(certificate_path: Path, metadata_path: Path) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    n = int(metadata["n"])
    primes = tuple(int(value) for value in metadata["primes"])
    boundary = int(metadata["boundary"])
    polygon_support = tuple(int(value) for value in metadata["polygon_support"])
    if metadata.get("schema") != "cyclotomic-boundary-uniqueness-certificate-v1":
        raise AssertionError("unexpected metadata schema")
    if n != 46189 or primes != (11, 13, 17, 19) or boundary != 41990:
        raise AssertionError((n, primes, boundary))
    if boundary != (primes[0] - 1) * n // primes[0]:
        raise AssertionError("boundary formula mismatch")
    if np.prod(primes, dtype=np.int64) != n or len(set(primes)) != len(primes):
        raise AssertionError("metadata factorization is invalid")
    expected_support = tuple(range(0, boundary + 1, n // primes[0]))
    if polygon_support != expected_support:
        raise AssertionError((polygon_support, expected_support))
    if file_sha256(certificate_path) != metadata["certificate_sha256"]:
        raise AssertionError("certificate SHA-256 mismatch")

    certificate = np.load(certificate_path, allow_pickle=False)["certificate"]
    expected_shape = tuple(prime - 1 for prime in primes)
    if certificate.dtype != np.int64 or certificate.size != int(np.prod(expected_shape)):
        raise AssertionError((certificate.dtype, certificate.shape, expected_shape))
    certificate = certificate.reshape(expected_shape)
    marginals = build_marginals(certificate)

    polygon_set = set(polygon_support)
    outside_max = None
    outside_min = None
    outside_max_index = None
    polygon_values: list[int] = []
    nonnegative_outside_count = 0
    for index in range(boundary + 1):
        value = evaluate(crt_coordinates(index, n, primes), marginals)
        if index in polygon_set:
            polygon_values.append(value)
            continue
        if outside_max is None or value > outside_max:
            outside_max = value
            outside_max_index = index
        if outside_min is None or value < outside_min:
            outside_min = value
        if value >= 0:
            nonnegative_outside_count += 1

    if any(value != 0 for value in polygon_values):
        raise AssertionError(("polygon values", polygon_values))
    if outside_max is None or outside_max > -1 or nonnegative_outside_count:
        raise AssertionError((outside_max, outside_max_index, nonnegative_outside_count))
    return {
        "result": "PASS",
        "n": n,
        "primes": primes,
        "boundary": boundary,
        "polygon_support": polygon_support,
        "certificate_shape": certificate.shape,
        "certificate_sha256": metadata["certificate_sha256"],
        "polygon_values": polygon_values,
        "outside_functional_min": outside_min,
        "outside_functional_max": outside_max,
        "outside_functional_max_index": outside_max_index,
        "outside_nonnegative_count": nonnegative_outside_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    print(verify(args.certificate, args.metadata))


if __name__ == "__main__":
    main()
