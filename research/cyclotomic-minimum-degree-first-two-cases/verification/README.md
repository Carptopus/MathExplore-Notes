# Exact certificate verification

The three integer NPZ files are the proof objects used by the manuscript.
Their JSON files record the parameter, tensor shape, boundary, support,
extreme values, and expected SHA-256 checksum.

The marginal verifiers reconstruct CRT coordinates and evaluate the integer
functional without importing the discovery linear programs. The full-array
verifiers independently expand the complete arrays and check every fiber sum
in all four coordinate directions.

## Requirements

- Python 3.9 or newer;
- NumPy; the audited environment used NumPy 2.5.2.

Install the recorded dependency in an isolated environment if needed:

```powershell
python -m pip install -r verification\requirements.txt
```

## Run

From the entry directory:

```powershell
python verification\verify_certificate.py `
  --certificate verification\results\certificate-46189.npz `
  --metadata verification\results\certificate-46189.json

python verification\verify_boundary_uniqueness.py `
  --certificate verification\results\boundary-uniqueness-46189.npz `
  --metadata verification\results\boundary-uniqueness-46189.json

python verification\verify_full_array.py `
  --mode minimum `
  --certificate verification\results\certificate-46189.npz `
  --metadata verification\results\certificate-46189.json

python verification\verify_full_array.py `
  --mode boundary `
  --certificate verification\results\boundary-uniqueness-46189.npz `
  --metadata verification\results\boundary-uniqueness-46189.json

python verification\verify_boundary_96577.py `
  --certificate verification\results\boundary-uniqueness-96577.npz `
  --metadata verification\results\boundary-uniqueness-96577.json

python verification\verify_full_array_96577.py `
  --certificate verification\results\boundary-uniqueness-96577.npz `
  --metadata verification\results\boundary-uniqueness-96577.json
```

All six invocations must report `PASS`. The full-array routes must additionally
report zero maximum absolute fiber sums on all four axes.

The finite certificate checks support the exact proof in the manuscript. They
do not establish the conjecture for parameters other than `46189` and `96577`.
