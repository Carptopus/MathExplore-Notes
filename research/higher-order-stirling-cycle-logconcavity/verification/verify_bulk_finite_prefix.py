"""Certified finite-prefix check for the unresolved compact bulk.

The exact normalized coefficients

    c(k,d) = 5^k [z^d] f_5(z)^k

satisfy the positive recurrence

    (d+5k)c(k,d) = (d-1+5k)c(k,d-1) + 5k c(k-1,d),
    c(k,0)=1.

This verifier checks the original strict inequality for

    2 <= k <= 1000,   k/2 < d < 12k.

It uses 40-significant-digit decimal arithmetic.  This is a certificate,
not an unqualified floating-point scan: every recurrence node has at most
4(k+d) rounded operations on any dependency path.  With unit roundoff
u=5*10^-40, the worst possible relative distortion in the final comparison
is below 10^-30.  The script requires every computed relative slack to be
larger than 10^-25 and also rejects overflow, underflow, subnormal values,
clamping, or invalid decimal operations.
"""

from __future__ import annotations

from decimal import (
    Clamped,
    Context,
    Decimal,
    DivisionByZero,
    InvalidOperation,
    Overflow,
    ROUND_HALF_EVEN,
    Subnormal,
    Underflow,
    getcontext,
    setcontext,
)


PRECISION = 40
MAX_K = 1000
MAX_D = 12 * MAX_K
UNIT_ROUNDOFF = Decimal(5).scaleb(-PRECISION)
REQUIRED_SLACK = Decimal("1e-25")


def configure_decimal() -> None:
    setcontext(
        Context(
            prec=PRECISION,
            rounding=ROUND_HALF_EVEN,
            Emin=-999999,
            Emax=999999,
        )
    )
    getcontext().clear_flags()


def verify_error_budget() -> None:
    # A recurrence path has at most k+d nodes and four relevant roundings
    # per node (two multiplications, positive addition, division).  Four
    # coefficient occurrences enter the final ratio; twenty extra operations
    # safely cover its integer factors and comparison quotient.
    path_roundings = 4 * (MAX_K + MAX_D + 2)
    distortion_exponent = 4 * path_roundings + 20

    # For 0<u<1/2, (1+u)/(1-u) < 1+4u.  Bernoulli plus a geometric
    # remainder gives (1+4u)^L < 1+8Lu whenever 4Lu<1/2.
    assert 4 * distortion_exponent * UNIT_ROUNDOFF < Decimal("0.5")
    distortion_bound = 8 * distortion_exponent * UNIT_ROUNDOFF
    assert distortion_bound < Decimal("1e-30")
    assert REQUIRED_SLACK > distortion_bound
    print("PASS: decimal roundoff budget is below 1e-30")


def comparison_slack(
    center: Decimal,
    lower: Decimal,
    upper: Decimal,
    k: int,
    d: int,
) -> Decimal:
    total = 5 * k + d

    # ratio/target - 1, evaluated by a positive cross-product:
    #
    # c(k,d)^2 / (c(k-1,d+1)c(k+1,d-1))
    #   >= k/(k+1) * product_{i=1}^4 (N+i)/(N-i+1).
    left = center * center * Decimal(k + 1)
    for value in range(total - 3, total + 1):
        left *= Decimal(value)
    right = lower * upper * Decimal(k)
    for value in range(total + 1, total + 5):
        right *= Decimal(value)
    return left / right - Decimal(1)


def verify_prefix() -> None:
    zero = Decimal(0)
    one = Decimal(1)
    previous = [zero] * (MAX_D + 1)
    previous[0] = one
    previous_previous: list[Decimal] | None = None

    minimum = Decimal("Infinity")
    minimizer: tuple[int, int] | None = None
    checks = 0

    for row in range(1, MAX_K + 2):
        current = [zero] * (MAX_D + 1)
        current[0] = one
        five_row = Decimal(5 * row)
        for excess in range(1, MAX_D + 1):
            current[excess] = (
                Decimal(excess - 1 + 5 * row) * current[excess - 1]
                + five_row * previous[excess]
            ) / Decimal(excess + 5 * row)

        center_row = row - 1
        if previous_previous is not None and center_row >= 2:
            for excess in range(center_row // 2 + 1, 12 * center_row):
                slack = comparison_slack(
                    previous[excess],
                    previous_previous[excess + 1],
                    current[excess - 1],
                    center_row,
                    excess,
                )
                assert slack > REQUIRED_SLACK
                checks += 1
                if slack < minimum:
                    minimum = slack
                    minimizer = (center_row, excess)

        previous_previous, previous = previous, current

    forbidden = (Overflow, Underflow, Subnormal, Clamped, InvalidOperation,
                 DivisionByZero)
    assert not any(getcontext().flags[signal] for signal in forbidden)
    assert minimizer is not None
    print(
        "PASS: certified compact-bulk prefix",
        f"checks={checks}",
        f"minimum_slack={minimum}",
        f"at={minimizer}",
    )


if __name__ == "__main__":
    configure_decimal()
    verify_error_budget()
    verify_prefix()
