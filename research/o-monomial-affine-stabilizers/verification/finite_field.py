"""Minimal polynomial-basis arithmetic for GF(2^m)."""

from __future__ import annotations


def poly_degree(value: int) -> int:
    return value.bit_length() - 1


def poly_multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def poly_mod(value: int, modulus: int) -> int:
    modulus_degree = poly_degree(modulus)
    while poly_degree(value) >= modulus_degree:
        value ^= modulus << (poly_degree(value) - modulus_degree)
    return value


def poly_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, poly_mod(left, right)
    return left


def is_irreducible(modulus: int, degree: int) -> bool:
    x = 2
    power = x
    for _ in range(degree):
        power = poly_mod(poly_multiply(power, power), modulus)
    if power != x:
        return False

    remaining = degree
    prime_divisors: list[int] = []
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            prime_divisors.append(prime)
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        prime_divisors.append(remaining)

    for prime in prime_divisors:
        power = x
        for _ in range(degree // prime):
            power = poly_mod(poly_multiply(power, power), modulus)
        if poly_gcd(power ^ x, modulus) != 1:
            return False
    return True


def find_modulus(degree: int) -> int:
    for low_part in range(1, 1 << degree, 2):
        candidate = (1 << degree) | low_part
        if is_irreducible(candidate, degree):
            return candidate
    raise RuntimeError(f"No irreducible polynomial found for degree {degree}")


class BinaryField:
    def __init__(self, degree: int):
        self.degree = degree
        self.order = 1 << degree
        self.modulus = find_modulus(degree)

    def multiply(self, left: int, right: int) -> int:
        result = 0
        while right:
            if right & 1:
                result ^= left
            right >>= 1
            left <<= 1
            if left & self.order:
                left ^= self.modulus
        return result

    def power(self, value: int, exponent: int) -> int:
        result = 1
        while exponent:
            if exponent & 1:
                result = self.multiply(result, value)
            value = self.multiply(value, value)
            exponent >>= 1
        return result
