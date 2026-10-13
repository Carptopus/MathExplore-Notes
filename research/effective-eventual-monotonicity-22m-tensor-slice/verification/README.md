# Verification package

This directory contains the ten frozen Python sources supporting the
computer-assisted parts of the manuscript: nine executable checks and their
shared exact Edgeworth generator.

## Environment

The audited local run used:

- CPython 3.13.11, 64-bit Windows build;
- `mpmath==1.3.0`;
- `numpy==2.5.2`;
- `scipy==1.17.0`;
- `sympy==1.14.0`.

Install the pinned Python dependencies in an isolated environment, then run:

```powershell
python -B verification\run_all.py
```

from the paper directory.  The scripts run serially.  No network access or
external data is required.  The expected terminal condition is:

```text
PASS: all frozen verification scripts completed
```

`check_chi_field_random_walk_reduction.py` includes numerical calibration
output for `I_1,I_2`; that output is explicitly not part of the proof.  The
strict coefficient and threshold comparisons use outward `mpmath.iv`
endpoints.  Random samples in several scripts are fixed-seed destructive or
regression controls, not substitutes for the analytic continuous-domain
lemmas in `../supplement/`.

`MANIFEST.sha256` freezes every verification source, this README, the pinned
requirements, and the six analytic ledgers.

