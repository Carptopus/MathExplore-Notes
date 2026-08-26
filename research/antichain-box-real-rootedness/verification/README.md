# Exact verification

The two programs independently calibrate the finite instances and algebraic
identities used by the manuscript. They are not replacements for the general
combinatorial and Jacobi-polynomial proofs.

## Environment

- Python 3.11 or newer
- SymPy 1.14.0

Install the declared dependency in an isolated environment and run:

```powershell
python -m pip install -r verification\requirements.txt
python -X utf8 verification\verify.py
python -X utf8 verification\verify_palindromicity.py
```

The original real-rootedness program prints seven `PASS` lines and a final
`BOUNDARY` line. Two checks are destructive controls: they confirm that an
incorrect off-diagonal index and a noncanonical inverse cut are rejected.

The palindromicity program prints a JSON object with `"status": "PASS"`. It
checks 30 Jacobi-identity parameters, 144 classification pairs, 20 strict
gamma cases, the exact signed value at `x=-1`, and square/gap-two destructive
controls.
