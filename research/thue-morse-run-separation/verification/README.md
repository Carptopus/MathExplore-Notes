# Verification

## Requirements

- Python 3.10 or newer;
- PowerShell 7 for the one-command wrapper;
- no third-party Python packages.

## Run everything

```powershell
.\run_all.ps1
```

To select a particular interpreter:

```powershell
.\run_all.ps1 -Python 'C:\path\to\python.exe'
```

The wrapper preserves the released JSON files, reruns both programs, and requires the regenerated
results to match the released evidence byte for byte.

## Programs and evidence boundary

`verify_candidate.py` performs two independent readings of `d(n)`: descent in the variable-length
morphism and the canonical Jacobsthal tail rule. It checks their agreement through `100000`,
reproduces `N_2=7` and `N_3=14563`, checks the displayed witnesses for `2 <= q <= 12`, and includes
false-exponent negative controls. These checks do not prove general minimality.

`verify_scale_and_minimizer.py` independently implements the `H(V)` membership encoding. It checks
the morphic encoding through `100000`, tests both scale implications on all relevant `v <= 300000`,
and exhaustively recovers the weak and strong binary minimizers for `2 <= q <= 7`. These are finite
destructive tests; the parametric scale and minimizer arguments are proved in the manuscript.

Released results are stored in `results/`.
