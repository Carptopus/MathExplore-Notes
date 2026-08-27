"""Independent exact verifier for the n=46189 Farkas certificate.

This verifier does not import the discovery LP or its sparse-matrix builder.  It
reconstructs CRT coordinates directly and evaluates the tensor-difference functional
through exact int64 marginals.
"""

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
    coordinates = []
    for prime in primes:
        step = n // prime
        inverse = pow(step, -1, prime)
        coordinates.append((index * inverse) % prime)
    return tuple(coordinates)


def build_marginals(certificate: np.ndarray) -> dict[int, np.ndarray | np.int64]:
    dimension = certificate.ndim
    marginals: dict[int, np.ndarray | np.int64] = {}
    for nonzero_mask in range(1 << dimension):
        zero_axes = tuple(axis for axis in range(dimension) if not nonzero_mask & (1 << axis))
        marginal = certificate.sum(axis=zero_axes, dtype=np.int64) if zero_axes else certificate
        marginals[nonzero_mask] = marginal
    return marginals


def evaluate(
    coordinates: tuple[int, ...],
    marginals: dict[int, np.ndarray | np.int64],
) -> int:
    nonzero_mask = sum((1 << axis) for axis, value in enumerate(coordinates) if value != 0)
    marginal = marginals[nonzero_mask]
    lookup = tuple(value - 1 for value in coordinates if value != 0)
    value = int(marginal[lookup]) if lookup else int(marginal)
    zero_count = len(coordinates) - nonzero_mask.bit_count()
    return -value if zero_count % 2 else value


def verify(certificate_path: Path, metadata_path: Path) -> dict[str, object]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    n = int(metadata["n"])
    primes = tuple(int(value) for value in metadata["primes"])
    max_degree = int(metadata["max_degree"])
    if metadata.get("schema") != "cyclotomic-mindeg-farkas-certificate-v1":
        raise AssertionError("unexpected metadata schema")
    if n != 46189 or primes != (11, 13, 17, 19) or max_degree != 41989:
        raise AssertionError((n, primes, max_degree))
    if np.prod(primes, dtype=np.int64) != n or len(set(primes)) != len(primes):
        raise AssertionError("metadata factorization is invalid")
    if file_sha256(certificate_path) != metadata["certificate_sha256"]:
        raise AssertionError("certificate SHA-256 mismatch")

    certificate = np.load(certificate_path, allow_pickle=False)["certificate"]
    expected_shape = tuple(prime - 1 for prime in primes)
    if certificate.dtype != np.int64 or certificate.size != int(np.prod(expected_shape)):
        raise AssertionError((certificate.dtype, certificate.shape, expected_shape))
    certificate = certificate.reshape(expected_shape)

    marginals = build_marginals(certificate)
    maximum = None
    minimum = None
    maximum_index = None
    nonnegative_count = 0
    for index in range(max_degree + 1):
        value = evaluate(crt_coordinates(index, n, primes), marginals)
        if maximum is None or value > maximum:
            maximum = value
            maximum_index = index
        if minimum is None or value < minimum:
            minimum = value
        if value >= 0:
            nonnegative_count += 1

    if maximum is None or maximum > -1 or nonnegative_count:
        raise AssertionError((maximum, maximum_index, nonnegative_count))
    return {
        "result": "PASS",
        "n": n,
        "primes": primes,
        "max_degree": max_degree,
        "certificate_shape": certificate.shape,
        "certificate_sha256": metadata["certificate_sha256"],
        "functional_min": minimum,
        "functional_max": maximum,
        "functional_max_index": maximum_index,
        "nonnegative_count": nonnegative_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    print(verify(args.certificate, args.metadata))


if __name__ == "__main__":
    main()
