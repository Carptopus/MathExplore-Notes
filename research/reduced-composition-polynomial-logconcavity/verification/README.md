# Verification

The two programs exercise independent interfaces used by the manuscript.

`test_truncation_pencil.py` uses exact rational arithmetic to check the Ardila--Doker merge
recurrence, the endpoint-deletion identities, every adjacent refinement-column minor, and the
determinant identity relating those minors to log-concavity defects. Its default run exhausts all
nontrivial compositions of total size at most 13. A deliberately enlarged weight interval supplies
a negative control and must produce failures only outside the admissible interval.

`verify_composition_unimodality.py` independently reconstructs the coefficients, checks positivity,
unimodality and log-concavity, and compares selected coefficients with SciPy B-spline knot
insertions. It also corrupts two refinement columns and must reject both.

Requirements:

- Python 3.13 or compatible;
- NumPy 2.5.2;
- SciPy 1.17.0;
- PowerShell 7 for the combined runner.

From this directory:

```powershell
.\run_all.ps1 -Python python
```

Both programs exit nonzero if a required identity, shape condition, or destructive control fails.
The finite checks validate implementations and proof interfaces; the universal theorem is proved
in the manuscript rather than inferred from finite testing.
