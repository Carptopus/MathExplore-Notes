"""All-parameter algebraic certificates for w_1 > 0, not the full CL summit.

The positive-coefficient tests below retain r,q,i,j as formal variables. They
are not finite parameter sampling. The reduction to these rational functions
and the coverage of all index cases are stated in Section 5 of the manuscript.
"""

from functools import cache

import sympy as sp

from probe_uniform_tail_weights import recover_tail_weights


r, q, i, j = sp.symbols("r q i j")
I, J, U, Q = sp.symbols("I J U Q")
n, d = r + q, 2 * r + q
A = n**2 * (n + 1)**2
D = d * (d - 1) * r
C = ((2 * n + 1) * (r - 1)**2
     + (q + 1) * (q + 2) * (r + 2 * r**3 / ((2 * r - 1) * q)))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ratio(k):
    k = sp.sympify(k)
    return (2*k + 1)*(r - k)**2 / ((k + 1)*(2*r - 2*k - 1)*(d - 1 - k))


def h(k):
    return 1 - ratio(k)


def v(k):
    k = sp.sympify(k)
    return 1 - 2*(k + 1)/(2*k + 1)*ratio(k)


@cache
def kernel():
    return sp.factor(A + q*d*((D*v(i) - C)*h(j) + (D*v(j) - C)*h(i))/2
                     - q**2*d**2*h(i)*h(j))


def first_block(order):
    terms = [sp.Integer(1)]
    for k in range(order):
        terms.append(terms[-1] * ratio(k))
    s = sum(terms)
    hh = sum(term*h(k) for k, term in enumerate(terms))
    vv = sum(term*v(k) for k, term in enumerate(terms))
    return sp.factor(A*s*s + q*d*(D*vv - C*s)*hh - q*q*d*d*hh*hh)


def check_positive_coefficients(poly):
    require(poly.domain == sp.QQ, "certificate must use exact rational coefficients")
    require(poly.TC() > 0, "certificate needs a strictly positive constant")
    require(all(coefficient > 0 for coefficient in poly.coeffs()),
            "nonpositive nonzero coefficient in certificate")


def certificate(label, expression, substitutions, variables):
    numerator, denominator = sp.fraction(sp.factor(expression))
    require(not expression.atoms(sp.Float), "inexact input to symbolic certificate")
    polynomials = []
    for piece in (numerator, denominator):
        translated = piece.subs(substitutions, simultaneous=True)
        polynomials.append(sp.Poly(sp.expand(translated), *variables, domain=sp.QQ))
    for poly in polynomials:
        check_positive_coefficients(poly)
    print(f"CERTIFICATE {label}: numerator {len(polynomials[0].terms())} terms, "
          f"degree {polynomials[0].total_degree()}; "
          f"denominator {len(polynomials[1].terms())} terms; all positive.", flush=True)


def all_parameter_certificates():
    K = kernel()
    # Symmetry reduces the domain to 0 <= i <= j <= r. Only (0,0) is exempt.
    certificate("i=0,1<=j<r", K.subs(i, 0),
                {j: J+1, r: J+U+2, q: Q+1}, (J, U, Q))
    certificate("1<=i<=j<r", K,
                {i: I+1, j: I+J+1, r: I+J+U+2, q: Q+1}, (I, J, U, Q))
    # Endpoint ratio R_r is exactly zero. Substitute before translation.
    endpoint = sp.factor(K.subs(j, r))
    certificate("i=0,j=r", endpoint.subs(i, 0),
                {r: U+2, q: Q+1}, (U, Q))
    certificate("1<=i<j=r", endpoint,
                {i: I+1, r: I+U+2, q: Q+1}, (I, U, Q))
    certificate("i=j=r", endpoint.subs(i, r),
                {r: U+2, q: Q+1}, (U, Q))
    block = first_block(2)
    certificate("0..2 block,r>=3", block,
                {r: U+3, q: Q+1}, (U, Q))
    low = 2*(9*q + 32)*(2*q*q + 17*q + 32)/(9*(q + 2)*(q + 3))
    require(sp.cancel(block.subs(r, 2) - low) == 0, "r=2 boundary identity failed")
    certificate("r=2 full block", low, {q: Q+1}, (Q,))


def independent_regression():
    def central(k):
        return sp.binomial(2*k, k) / sp.Integer(4)**k

    K = kernel()
    checked = 0
    for rv, qv in ((2, 1), (2, 9), (3, 1), (3, 5), (4, 2), (5, 5), (7, 1)):
        nv, dv = rv+qv, 2*rv+qv
        t = [central(k)*central(rv-k)/central(rv)
             * sp.binomial(rv, k)/sp.binomial(dv-1, k) for k in range(rv+1)]
        s = sum(t)
        u = 1 - sum(t[k]/(2*k-1) for k in range(1, rv+1))
        substitutions = {r: rv, q: qv}
        hv = [h(k).subs(substitutions) for k in range(rv+1)]
        vv = [v(k).subs(substitutions) for k in range(rv+1)]
        require(sum(t[k]*hv[k] for k in range(rv+1)) == 1,
                "mass telescoping failed")
        require(sum(t[k]*vv[k] for k in range(rv+1)) == u,
                "U telescoping failed")
        expected = (A*s*s + q*d*(D*u - C*s) - q*q*d*d).subs(substitutions)
        specialized = K.subs(substitutions)
        observed = sum(t[a]*t[b]*specialized.subs({i: a, j: b})
                       for a in range(rv+1) for b in range(rv+1))
        require(observed == expected, "kernel double-sum identity failed")
        recovered = recover_tail_weights(rv+1, nv)[1]
        require(observed/(4*s*(nv*nv*s - qv*dv)) == recovered,
                "kernel-to-Euclid comparison failed")
        checked += 1
    # A pointwise-positive-kernel claim would be false without the small block.
    require(K.subs({r: 5, q: 5, i: 0, j: 0}) < 0,
            "negative kernel control failed")
    require(first_block(1).subs({r: 10, q: 100}) < 0,
            "insufficient first block control failed")
    try:
        check_positive_coefficients(sp.Poly(U - 1, U, domain=sp.QQ))
    except RuntimeError:
        pass
    else:
        raise RuntimeError("coefficient checker accepted destructive control")
    print(f"PASS: {checked} independent Euclid comparisons and negative controls.", flush=True)


if __name__ == "__main__":
    all_parameter_certificates()
    independent_regression()
    print("PASS: positive-kernel certificates for all r>=2,q>=1. "
          "Only w_1 is certified; this is not the full CL conjecture.", flush=True)
