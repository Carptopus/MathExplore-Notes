"""Exact rational verification for the three-runner counterexample family."""

from fractions import Fraction


Q = Fraction


def exact_order_means(velocities, starts):
    """Return exact order-statistic means over one normalized common period."""
    starts = [start % 1 for start in starts]
    size = len(velocities)
    breakpoints = {Q(0), Q(1)}

    for velocity, start in zip(velocities, starts):
        bound = abs(velocity) + 2
        for integer in range(-bound, bound + 1):
            time = Q(integer - start, velocity)
            if 0 < time < 1:
                breakpoints.add(time)

    for left in range(size):
        for right in range(left + 1, size):
            delta_velocity = velocities[left] - velocities[right]
            if delta_velocity == 0:
                continue
            bound = abs(delta_velocity) + 2
            delta_start = starts[left] - starts[right]
            for integer in range(-bound, bound + 1):
                time = Q(integer - delta_start, delta_velocity)
                if 0 < time < 1:
                    breakpoints.add(time)

    ordered_breakpoints = sorted(breakpoints)
    integrals = [Q(0) for _ in range(size)]

    for lower, upper in zip(ordered_breakpoints, ordered_breakpoints[1:]):
        midpoint = (lower + upper) / 2
        affine_pieces = []
        for velocity, start in zip(velocities, starts):
            raw_value = start + velocity * midpoint
            floor_value = raw_value.numerator // raw_value.denominator
            affine_pieces.append((start - floor_value, velocity))

        affine_pieces.sort(key=lambda piece: piece[0] + piece[1] * midpoint)
        for rank, (intercept, slope) in enumerate(affine_pieces):
            integrals[rank] += (
                intercept * (upper - lower)
                + Q(slope, 2) * (upper * upper - lower * lower)
            )

    return integrals


def predicted_median(offset):
    """Closed form for velocities (1,2,3) and starts (0,0,offset)."""
    offset %= 1
    if offset <= Q(1, 2):
        return Q(1, 2) - Q(4, 9) * offset * (Q(1, 2) - offset)
    return Q(1, 2) + Q(4, 9) * (offset - Q(1, 2)) * (1 - offset)


def main():
    velocities = [1, 2, 3]

    counterexample = exact_order_means(
        velocities,
        [Q(0), Q(0), Q(1, 4)],
    )
    assert counterexample == [Q(161, 576), Q(17, 36), Q(431, 576)]
    assert counterexample[1] != Q(1, 2)
    assert counterexample[0] + counterexample[2] == Q(37, 36)

    equivalent_lift = exact_order_means(
        velocities,
        [Q(0), Q(0), Q(4001, 4)],
    )
    assert equivalent_lift == counterexample

    positive_control = exact_order_means(
        velocities,
        [Q(0), Q(0), Q(0)],
    )
    assert positive_control == [Q(7, 24), Q(1, 2), Q(17, 24)]
    assert positive_control[0] + positive_control[2] == Q(1)

    checked_offsets = set()
    for denominator in range(1, 51):
        for numerator in range(denominator + 1):
            offset = Q(numerator, denominator)
            if offset in checked_offsets:
                continue
            checked_offsets.add(offset)
            exact_median = exact_order_means(
                velocities,
                [Q(0), Q(0), offset],
            )[1]
            assert exact_median == predicted_median(offset)

    print("counterexample:", counterexample)
    print("positive control:", positive_control)
    print("closed-form offsets checked:", len(checked_offsets))
    print("PASS")


if __name__ == "__main__":
    main()
