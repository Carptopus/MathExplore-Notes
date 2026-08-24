# Verification materials

These programs are finite calibration and destructive tests for formulas used
in the manuscript. They do not prove the arbitrary-period classification.

Requirements:

- Python 3.10 or newer;
- SymPy for `verify_split_eigenlines.py`.

From this directory, run the fixed entry point:

```powershell
python run_all.py
```

The command runs three checks and rewrites the deterministic JSON files in
`results/`:

- `verify_two_adic_obstruction.py`: the closed $2$-adic valuation formulas for
  $3\leq N\leq10$;
- `verify_split_eigenlines.py`: all 36 ordered eigenline pairs, with exactly six
  antipodal degeneracies;
- `verify_split_antipodal_obstruction.py`: sample split primes
  $p=5,13,17$ and exponents $1,2$.

Python files are MIT-licensed; JSON results are CC0 1.0. See the entry-level
`LICENSE.md`.
