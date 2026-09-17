# Finite verification checks

These 17 `verify_*.py` scripts are exact, bounded regression and boundary checks developed alongside the proof. They check selected algebraic identities, event closures, exchange cases, path-separator formulas and degenerate boundaries used while developing the argument. `probe_three_branch_cut_profiles.py` is their shared finite-enumeration support module; the runner does not execute it as a separate check.

They do **not** prove the general theorem and are not substitutes for the mathematical proof in the manuscript. In particular, passing every script establishes only the finite claims encoded by the scripts.

## Run

Python 3 and PowerShell are required. No downloads or external solvers are used. From this directory:

```powershell
.\run_all.ps1
```

To select a particular Python interpreter:

```powershell
.\run_all.ps1 -Python 'C:\path\to\python.exe'
```

The runner executes the scripts serially and stops at the first nonzero exit code. The checked release result is recorded in [RESULTS.md](RESULTS.md).
