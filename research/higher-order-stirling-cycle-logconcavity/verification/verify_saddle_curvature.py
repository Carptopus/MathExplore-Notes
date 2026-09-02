from __future__ import annotations

import sympy as sp


def main() -> None:
    z, a, t = sp.symbols("z a t", positive=True)

    # After mu=a-5 and sigma^2=a(t-a+5), the r=5 curvature margin
    # divided by a has this exact linear form.
    reduced_margin = sp.expand(
        (a - 4) ** 2 - (16 - a) * (t - a + 5)
    )
    assert sp.simplify(
        reduced_margin - (a * (t + 13) - 16 * (t + 4))
    ) == 0

    rational_majorant = (13 - 12 * z) / (16 * (1 - z) * (4 - 3 * z))

    # f_5 is characterized by z f_5' + 5 f_5 = 1/(1-z).
    # The residual below proves that h=R-f_5 is positive by an
    # integrating-factor argument; it is a certificate, not a numerical test.
    residual = sp.factor(
        z * sp.diff(rational_majorant, z)
        + 5 * rational_majorant
        - 1 / (1 - z)
    )
    expected = (3 * z - 2) ** 2 / (
        16 * (1 - z) ** 2 * (4 - 3 * z) ** 2
    )
    assert sp.simplify(residual - expected) == 0
    assert sp.limit(rational_majorant, z, 0) - sp.Rational(1, 5) == sp.Rational(
        1, 320
    )

    print("PASS: exact r=5 saddle-curvature reduction")
    print("PASS: rational majorant residual is a nonnegative square")


if __name__ == "__main__":
    main()
