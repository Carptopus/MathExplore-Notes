# Destructive verification suite

The symbolic proof in the manuscript establishes the all-orders theorem. This
program provides bounded destructive checks of the sector identity, sign
pattern, arithmetic reductions, exact divisibility, and two deliberate
mutations. Finite checks do not establish the all-orders quantifier.

Requirements:

- Python 3;
- `mpmath`;
- `sympy`.

Run from the parent entry directory:

```powershell
python -X utf8 .\verification\verify_full_n_sector_certificate.py
```

The suite checks all orders through `n=1000` at its main numerical boundary,
performs exact algebraic checks through `n=180`, and verifies both negative
controls. The final JSON object must report `"result": "PASS"`.
