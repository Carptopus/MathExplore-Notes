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

`verify_counterexample.py` reconstructs the bipartite Hasse graph, checks connectivity and a
perfect matching, compares the displayed polynomial formula against exhaustive independent-set
enumeration, independently scans all `2^18` subsets for `a=7,c=2`, checks the defect `-72`, and
tests `a=1,...,6` as negative controls and `a=7,...,40` as positive controls.

These are finite destructive checks. The Peck property, the closed formula, and the obstruction for
every `a >= 7` are proved parametrically in the manuscript.
