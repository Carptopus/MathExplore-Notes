# Exact finite controls

The accompanying analytic proof establishes the general theorems. This script checks only
finite identities and constants; it is not a computer-assisted exhaustive proof.

`check_correlation_controls.py` uses Python's standard library, including `fractions.Fraction`
for exact Gaussian rational arithmetic. Python 3.10 or later suffices. In the project environment,
run from the repository root:

```powershell
python -B verification/check_correlation_controls.py --output correlation-controls.local.json
```

For use outside this Windows workspace, replace the interpreter and output path explicitly.
The output is disposable; the archived reference result is in `results/correlation-controls.json`.
No network, third-party library, random seed, or external solver is needed.

The archived run covered 108 column/profile cases over four finite supports and three coefficient
profiles. Controls detect omission of conjugation, exercise nonzero auxiliary means, and show that
an unselected column need not have a bounded interior/boundary ratio. The script also checks the
leakage absorption constant and the final prefactor. All assertions passed. The recorded execution
time is historical and is not a performance or peak-memory guarantee; no new run is claimed here.

Both files were copied byte-for-byte from the frozen research evidence:

| File | SHA256 |
| --- | --- |
| `check_correlation_controls.py` | B956499BEF727482FF9486A570E3B3F9E4F03B166F952DE667A846A14CF7C996 |
| `results/correlation-controls.json` | BFA18A4A9C5100DBCEF60D891AC35354FC0B87651C19009B256BBE4B627FEB47 |

The reference JSON records its source-script hash. It certifies neither the universal quantifiers
of the theorem nor novelty, publication readiness, or process memory usage.
