# Symbolic verification

`verify_identity.py` checks the derivative/Walsh identity for generic polynomials of degrees 1
through 8. It independently checks the telescoping certificate and the associated apolar pairing,
then verifies that deleting an endpoint term is detected by a destructive control.

Requirements:

- Python 3;
- SymPy 1.14, pinned in `requirements.txt`.

Run from PowerShell:

```powershell
.\run_all.ps1 -Python python
```

The runner executes both ordinary and optimized Python modes, checks their exit codes, compares
their outputs with each other, and compares both with `results/expected-output.txt`. The script
uses explicit exceptions rather than Python `assert`, so optimization cannot disable its gates.

These finite symbolic checks confirm implementations of identities used in the manuscript. The
general theorem also depends on the written proof and the cited Walsh root-location theorem.
