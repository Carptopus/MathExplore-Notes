"""Finite reconstruction of the bar-Segre value-set polynomial.

The proof is symbolic and appears in the manuscript.  This script only checks its
three leading coefficient claims over several exact finite fields.
"""

from __future__ import annotations

from finite_field import BinaryField


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def multiply(left: list[int], right: list[int], field: BinaryField) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if b:
                result[i + j] ^= field.multiply(a, b)
    return result


def root_polynomial(roots: set[int], field: BinaryField) -> list[int]:
    factors = [[root, 1] for root in roots]
    while len(factors) > 1:
        next_level = []
        for index in range(0, len(factors), 2):
            if index + 1 == len(factors):
                next_level.append(factors[index])
            else:
                next_level.append(
                    multiply(factors[index], factors[index + 1], field)
                )
        factors = next_level
    return factors[0]


def check_negative_control() -> None:
    """Confirm that the excluded m=3 boundary has nontrivial affine symmetry."""
    degree = 3
    field = BinaryField(degree)
    q = field.order
    image = {field.power(x, q - 6) ^ x for x in range(q)}
    stabilizer = [
        (u, v)
        for u in range(1, q)
        for v in range(q)
        if {field.multiply(u, y) ^ v for y in image} == image
    ]
    require((1, 0) in stabilizer, "negative control lost the identity")
    require(
        len(stabilizer) > 1,
        "negative control failed to detect the nontrivial m=3 stabilizer",
    )


def main() -> None:
    for degree in (5, 7, 9, 11):
        field = BinaryField(degree)
        q = field.order
        exponent = q - 6
        image = {field.power(x, exponent) ^ x for x in range(q)}
        require(len(image) == q // 2, f"m={degree}: image is not two-to-one")
        polynomial = root_polynomial(image, field)
        k = q // 2
        require(len(polynomial) == k + 1, f"m={degree}: wrong polynomial degree")
        require(polynomial[k] == 1, f"m={degree}: polynomial is not monic")
        require(polynomial[k - 1] == 0, f"m={degree}: c1 is nonzero")
        require(polynomial[k - 2] == 0, f"m={degree}: c2 is nonzero")
        require(polynomial[k - 3] == 1, f"m={degree}: c3 is not one")
        require(
            all(coefficient in (0, 1) for coefficient in polynomial),
            f"m={degree}: coefficient escaped the prime field",
        )
        print(f"m={degree}: degree={k}, (c1,c2,c3)=(0,0,1)")
    check_negative_control()
    print("NEGATIVE_CONTROL_PASS: excluded m=3 has a nontrivial affine stabilizer")
    print("PASS: exact finite reconstructions agree with the symbolic lemma")


if __name__ == "__main__":
    main()
