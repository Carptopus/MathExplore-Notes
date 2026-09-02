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

## Evidence boundary

`check_basis_obstruction.py` reconstructs the basis triples of `F_2^3`, verifies their Fano-line
complement, checks the host's weak chromatic number, exercises complete-three-graph and Fano-plane
homomorphism controls, and exhaustively checks the two six-vertex non-homomorphism obstructions and
the 3-colourability of every vertex link.

These are finite destructive checks. The general homomorphism obstruction, the exact limiting
density, and the parametric statement for arbitrary finite `r`-graphs are proved symbolically in
the manuscript.
