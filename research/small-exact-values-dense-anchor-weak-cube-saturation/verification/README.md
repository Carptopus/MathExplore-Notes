# Verification package

This directory reproduces the finite computations supporting the manuscript.

## Requirements

- Python 3.13 or a compatible recent Python 3 release;
- NumPy 2.5;
- NetworkX 3.6.

The released checks were run with Python 3.13.11, NumPy 2.5.2, and NetworkX 3.6.1.

## Full reproduction

From this directory in PowerShell:

```powershell
.\run_all.ps1 -Python python
```

This reruns the structural audit, the complete normalized enumerations for orders 8, 9, and 10,
the upper-witness checks, certificate construction and independent NetworkX replay, and the two
bound calculations. The order-10 enumeration is the slowest step.

To audit the released result files and certificates without rerunning the exhaustive enumeration:

```powershell
.\run_all.ps1 -Python python -SkipExactEnumeration
```

## Evidence boundary

- `exact_first_cube_enumeration.py` performs the normalized exhaustive searches.
- `audit_normalisation_and_connectivity.py` independently checks the graph facts used by the
  normalization and the order-10 biconnectivity filter.
- `audit_activation_certificate.py` independently replays the four released activation
  certificates with NetworkX.
- `verify_dense_anchor_extension.py` reads the released 28-edge certificate rather than a search
  log and checks the concrete extension from order 8 to order 12.
- The seven-period lower-bound script is a finite cross-check of a prior theorem; it is not a new
  proof of that theorem.

The discovery searches are intentionally omitted. Solver timeouts and unsuccessful searches are
not mathematical evidence.
