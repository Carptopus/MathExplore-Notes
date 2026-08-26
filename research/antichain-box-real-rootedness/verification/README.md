# Exact verification

The program `verify.py` independently calibrates the finite instances and
algebraic identities used by the manuscript. It is not a replacement for the
general combinatorial and Jacobi-polynomial proofs.

## Environment

- Python 3.11 or newer
- SymPy 1.14.0

Install the declared dependency in an isolated environment and run:

```powershell
python -m pip install -r verification\requirements.txt
python -X utf8 verification\verify.py
```

The expected output contains seven `PASS` lines and one final `BOUNDARY` line.
Two checks are destructive controls: they confirm that an incorrect
off-diagonal index and a noncanonical inverse cut are rejected.
