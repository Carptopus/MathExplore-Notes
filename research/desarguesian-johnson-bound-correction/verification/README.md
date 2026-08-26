# Verification

This directory contains a compact exact certificate of 18 pairwise disjoint
Desarguesian $3$-spreads in $V(6,2)$.

## Environment and command

The checker uses only Python 3.11 or newer and the standard library. From the
entry directory, run:

```powershell
python -X utf8 verification\check_desarguesian_certificate.py
```

The program reconstructs the $\mathbb F_{64}/\mathbb F_8$ field-reduction
spread, applies the 18 stored invertible $\mathbb F_2$-linear maps, and checks
spread validity, distinctness, and pairwise disjointness. It also rejects a
singular-map control and a duplicate-spread control.

## Evidence boundary

The certificate proves only $D(6,3,2)\geq18>10$. The manuscript's
all-parameter correction is a separate symbolic comparison and does not
follow from the finite computation. Passing the checker does not replace
external mathematical review.

The code is licensed under MIT; the fixed JSON certificate is dedicated under
CC0 1.0.
