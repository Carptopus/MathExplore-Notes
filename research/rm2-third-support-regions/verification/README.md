# Verification package

This directory contains the exact finite certificates retained by the manuscript
*Exact regions and low-polar-rank recursion in the third support spectrum of
binary second-order Reed--Muller codes*.

## Run

From the MathExplore-Notes repository root:

```powershell
pwsh -NoProfile -File research/rm2-third-support-regions/verification/run_all.ps1
```

For a standalone copy, pass any Python 3.10 or newer interpreter:

```powershell
pwsh -NoProfile -File verification/run_all.ps1 -Python C:\Path\To\python.exe
```

No third-party Python package is required. Assertions must be enabled; the runner
refuses optimized Python.

## Certificate groups

- `verify_slice_orbits.py`: explicit polar-net affine orbits and slice sumsets
  used for the spectra through nine variables;
- `verify_rank_exclusions.py`: exhaustive seven-word weight and polar-rank
  patterns for the eight- and nine-variable exclusions, including destructive
  maximal-Pfaffian control;
- `verify_three_signed_dyadic_sum_13.py` and
  `verify_rank2_or_rank4_dichotomy_19_8.py`: bounded arithmetic regressions for
  the general signed-dyadic proofs;
- `verify_walsh_zero_low_rank_boundary.py`: a boundary family excluded from the
  nonzero-Walsh recursion;
- `verify_kdr_arbitrary_length_formulas.py`: exact checks of the arbitrary-length
  `K_k`, `D_k`, and `R_d` control-matrix identities; its fixed-seed regular
  matrices are regression samples, while generality comes from the manuscript's
  matrix factorization;
- `verify_hit_*_transfer.py`: affine mask and product-sign transfer families for
  the three canonical block types;
- `verify_rank2_full_core_recursion.py`,
  `verify_rank4_stratum_recursion.py`, and
  `verify_rank4_full_core_recursion.py`: finite state laws, relation kernels,
  terminal core outputs, and independence controls;
- `verify_rank4_obstruction_19_8_all_n.py`: the dimension-independent finite
  obstruction for the forbidden ray;
- `verify_rank4_obstruction_152_complete.py`: an independent twelve-variable
  calibration of the same obstruction.

## Proof boundary

The scripts verify finite orbit sets, arithmetic branches, transition laws, and
state-machine implementation. They do not prove the classical low-weight theorem,
the canonical decomposition of alternating pencils, or the arbitrary-length
symbolic identities. Those inputs and proofs are stated separately in the
manuscript. A script timeout or a missing witness is never interpreted as a
nonexistence proof.

## Licenses

- executable verification code: [MIT](LICENSE-CODE-MIT.txt);
- frozen certificate data, if distributed: [CC0 1.0](LICENSE-DATA-CC0.md).
