# Verification

The two standard-library Python programs check the finite-field coefficient calculations used by
the manuscript:

- `verify_bar_segre_value_polynomial.py` reconstructs the value-set polynomial for
  $m=5,7,9,11$ and checks $(c_1,c_2,c_3)=(0,0,1)$;
- `verify_glynn_cycle_cover_arithmetic.py` checks the zero-weight formulas, cycle-cover parity,
  Kummer valuations, coefficient gaps, and initial finite value-set polynomials.

`finite_field.py` supplies the shared polynomial-basis arithmetic used by both checkers.

Run both ordinary and optimized executions from the repository root:

```powershell
pwsh -NoProfile -File .\research\o-monomial-affine-stabilizers\verification\run_all.ps1
```

Use `-Python <path>` to select a particular Python 3 interpreter. The runner rejects any output
that differs from the frozen results. Each verifier also contains a destructive control.
