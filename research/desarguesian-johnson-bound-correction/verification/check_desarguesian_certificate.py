"""Independently check the stored V(6,2) Desarguesian-spread certificate."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "desarguesian-v6q2-certificate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def multiply(a: int, b: int, modulus: int, dimension: int) -> int:
    value = 0
    while b:
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & (1 << dimension):
            a ^= modulus
    return value


def power(a: int, exponent: int, modulus: int, dimension: int) -> int:
    value = 1
    while exponent:
        if exponent & 1:
            value = multiply(value, a, modulus, dimension)
        a = multiply(a, a, modulus, dimension)
        exponent >>= 1
    return value


def linear_image(columns: tuple[int, ...], vector: int) -> int:
    value = 0
    for index, column in enumerate(columns):
        if vector >> index & 1:
            value ^= column
    return value


def is_invertible(columns: tuple[int, ...], dimension: int) -> bool:
    return len({linear_image(columns, vector) for vector in range(1 << dimension)}) == (
        1 << dimension
    )


def images_are_distinct(images: list[set[tuple[int, ...]]]) -> bool:
    return len({frozenset(image) for image in images}) == len(images)


def main() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(data["base_field_order"] == 2, "certificate is not over F_2")
    dimension = data["ambient_dimension"]
    spread_dimension = data["spread_subspace_dimension"]
    require(dimension == 6, "unexpected ambient dimension")
    require(spread_dimension == 3, "unexpected spread-subspace dimension")
    modulus = int(data["field_modulus_binary"], 2)
    alpha = 2

    powers = [power(alpha, i, modulus, dimension) for i in range(63)]
    require(
        len(set(powers)) == 63 and set(powers) == set(range(1, 64)),
        "field generator does not enumerate F_64^*",
    )

    beta_exponent = data["base_spread_subfield_generator_exponent"]
    subfield_units = {power(alpha, beta_exponent * j, modulus, dimension) for j in range(7)}
    require(len(subfield_units) == 7, "subfield unit group does not have order 7")
    base = {
        tuple(sorted(multiply(power(alpha, i, modulus, dimension), x, modulus, dimension) for x in subfield_units))
        for i in range(9)
    }
    require(len(base) == 9, "base spread does not contain nine subspaces")
    require(
        {x for subspace in base for x in subspace} == set(range(1, 64)),
        "base spread does not partition the nonzero vectors",
    )
    for subspace in base:
        vectors = set(subspace) | {0}
        require(len(vectors) == 8, "base member does not have vector dimension three")
        require(
            all(x ^ y in vectors for x in vectors for y in vectors),
            "base member is not closed under vector addition",
        )

    images = []
    for encoded_columns in data["linear_map_columns_hex"]:
        columns = tuple(int(value, 16) for value in encoded_columns)
        require(is_invertible(columns, dimension), "certificate contains a singular map")
        image = {
            tuple(sorted(linear_image(columns, vector) for vector in subspace))
            for subspace in base
        }
        require(len(image) == 9, "image does not contain nine subspaces")
        require(
            {x for subspace in image for x in subspace} == set(range(1, 64)),
            "image does not partition the nonzero vectors",
        )
        images.append(image)

    require(len(images) == 18, "certificate does not contain 18 images")
    require(images_are_distinct(images), "certificate contains duplicate spreads")

    for i, left in enumerate(images):
        for right in images[i + 1 :]:
            require(left.isdisjoint(right), "two certified spreads share a subspace")

    require(
        not is_invertible((0,) * dimension, dimension),
        "singular-map negative control was not rejected",
    )
    require(
        not images_are_distinct([*images, images[0]]),
        "duplicate-spread negative control was not rejected",
    )

    johnson_bound = (2 ** (dimension - 1) - 1) // (
        2 ** (spread_dimension - 1) - 1
    )
    require(johnson_bound == 10, "unexpected Johnson bound")

    print(f"PASS: certificate contains {len(images)} pairwise disjoint GL-images")
    print(
        "Each image is a Desarguesian "
        f"{spread_dimension}-spread of V({dimension},{data['base_field_order']})"
    )
    print(f"Published Johnson bound for these parameters is {johnson_bound}")
    print("Negative controls rejected a singular map and a duplicate spread")


if __name__ == "__main__":
    main()

