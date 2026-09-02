# Verification package

This directory contains the exact regression checks supporting the explicit quadratic-net
families and the finite rank/sign reductions used in the manuscript.

## Requirements

- Python 3.11 or a compatible recent Python 3 release;
- PowerShell 7 for the combined entry point;
- no third-party Python packages.

Run from this directory:

```powershell
.\run_all.ps1 -Python python
```

The released checks cover:

- direct Walsh-transform verification of the infinite odd-dimensional witness family;
- the six stable offsets and their affine masks;
- the even- and odd-dimensional outer reductions throughout the calibrated local band;
- destructive controls that alter the base quadratic net.

## Evidence boundary

The scripts verify the explicit signatures and exhaust the finite dyadic rank/sign models used to
calibrate the proof. They do not replace the scalar and vector maximal-Pfaffian arguments in the
manuscript, and they are not an independent computation of the complete third support spectrum.
