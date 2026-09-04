# Exact verification

`verify_a3_bound.py` checks the exact finite and symbolic interfaces used by the manuscript:

- derives the cubic correction polynomial from the general rank-two formula;
- reconstructs the two uniform-estimate Taylor certificates and checks their coefficient,
  discriminant, stationary-point, and endpoint claims;
- reconstructs the `n=9` polynomial, Sturm profile, and endpoint signs;
- includes a positive-root destructive control for the Sturm routine;
- checks all 31 connected small partitions by two exact root tests;
- derives and checks all six disconnected cases.

Requirements: Python 3.10 or later, PowerShell 7, and SymPy 1.14.

From the repository root:

```powershell
pwsh -NoProfile -File .\research\rank-two-matroid-hstar-size-three\verification\run_all.ps1
```

Alternatively, from this directory:

```powershell
python -B verify_a3_bound.py
python -B -O verify_a3_bound.py
```

The runner requires ordinary and optimized execution to match the frozen output in
`results/expected-output.txt`. The script uses explicit exceptions rather than Python assertions,
so optimization cannot disable its correctness gates.

The computations validate the exact finite boundary and the algebra used by the proof. They do
not replace the manuscript's analytic argument for all `n>=10`.

