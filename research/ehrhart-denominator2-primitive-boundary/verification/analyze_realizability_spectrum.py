from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from math import gcd


def missing_color_count(d: int, p_residue: int) -> int:
    """Count odd--odd interior points in the normalized primitive triangle."""
    total = 0
    for y in range(1, d, 2):
        residue = (p_residue * y) % d
        if residue % 2 == 0 and residue > y:
            total += 1
    return total


def missing_color_points(d: int, p_residue: int) -> list[tuple[int, int]]:
    """Return the odd--odd points counted by missing_color_count."""
    p_even = p_residue if p_residue % 2 == 0 else p_residue + d
    points = []
    for y in range(1, d, 2):
        quotient, residue = divmod(p_even * y, d)
        if residue % 2 == 0 and residue > y:
            points.append((quotient + 1, y))
    return points


def points_are_collinear(points: list[tuple[int, int]]) -> bool:
    if len(points) <= 2:
        return True
    (x0, y0), (x1, y1) = points[:2]
    return all((x - x0) * (y1 - y0) == (y - y0) * (x1 - x0) for x, y in points[2:])


def anharmonic_orbit(d: int, p: int) -> set[int]:
    """S3 orbit induced by permuting the three vertices of T(D,p)."""
    values = set()
    frontier = {p % d}
    while frontier:
        value = frontier.pop()
        if value in values:
            continue
        values.add(value)
        inverse = pow(value, -1, d)
        frontier.update({(1 - value) % d, inverse})
    return values


def admissible_parameters(d: int) -> list[int]:
    return [p for p in range(d) if gcd(p, d) == gcd(p - 1, d) == 1]


def realized_spectrum(d: int) -> dict[int, list[int]]:
    spectrum: dict[int, list[int]] = defaultdict(list)
    for p in admissible_parameters(d):
        spectrum[missing_color_count(d, p)].append(p)
    return dict(sorted(spectrum.items()))


def predicted_positive_counts(d: int) -> list[int]:
    """Counts allowed by the HHK linear bounds plus the mod-8 obstruction."""
    interior = (d - 1) // 2
    predicted = []
    for n in range(1, interior + 1):
        if 2 * n - 1 > interior:
            continue
        if interior > 6 * n + 4:
            continue
        if interior % 4 not in {(2 * n) % 4, (2 * n - 1) % 4}:
            continue
        predicted.append(n)
    return predicted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-d", type=int, default=401)
    parser.add_argument("--show-first", type=int, default=30)
    parser.add_argument("--defect-two", action="store_true")
    parser.add_argument("--collinear", action="store_true")
    args = parser.parse_args()

    if args.max_d < 1:
        raise SystemExit("--max-d must be positive")

    rows = []
    first_missing = None
    first_exact = None
    gap_counter: Counter[int] = Counter()
    for d in range(1, args.max_d + 1, 2):
        spectrum = realized_spectrum(d)
        actual = sorted(n for n in spectrum if n > 0)
        predicted = predicted_positive_counts(d)
        missing = sorted(set(predicted) - set(actual))
        unexpected = sorted(set(actual) - set(predicted))
        rows.append((d, (d - 1) // 2, len(admissible_parameters(d)), actual, predicted, missing, unexpected))
        for n in missing:
            gap_counter[n] += 1
        if missing and first_missing is None:
            first_missing = rows[-1]
        if not missing and predicted and first_exact is None:
            first_exact = rows[-1]

    print("D I |U_D| actual predicted missing unexpected")
    for row in rows[: args.show_first]:
        print(row)

    mismatch_rows = [row for row in rows if row[5] or row[6]]
    print(f"SUMMARY odd_D={len(rows)} mismatch_D={len(mismatch_rows)}")
    print(f"FIRST_MISSING={first_missing}")
    print(f"FIRST_EXACT_NONEMPTY={first_exact}")
    print(f"MOST_COMMON_MISSING_N={gap_counter.most_common(20)}")

    if mismatch_rows:
        print("FIRST_MISMATCH_ROWS")
        for row in mismatch_rows[:20]:
            print(row)

    if args.defect_two:
        hits = []
        for d, interior, _, actual, _, _, _ in rows:
            target = (d + 1) // 4 - 2
            if target in actual:
                witnesses = realized_spectrum(d)[target]
                hits.append((d, interior, target, witnesses))
        print(f"DEFECT_TWO_HITS={hits}")

    if args.collinear:
        print("COLLINEAR_MISSING_COLOR_CLASSES")
        for d, _, _, _, _, _, _ in rows:
            classes = []
            seen = set()
            for p in admissible_parameters(d):
                if p in seen:
                    continue
                orbit = anharmonic_orbit(d, p)
                seen.update(orbit)
                points = missing_color_points(d, p)
                if points_are_collinear(points):
                    classes.append((p, len(points), points, sorted(orbit)))
            if classes:
                print((d, classes))


if __name__ == "__main__":
    main()
