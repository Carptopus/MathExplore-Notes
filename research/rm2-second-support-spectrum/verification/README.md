# Verification material

These programs accompany the manuscript *Attainable Second Support Weights of
Binary Second-Order Reed--Muller Codes*.

They require Python 3.11 or newer, use only the standard library, and do not
require network access or a computer algebra system. From the entry directory,
run:

```powershell
python -X utf8 verification/verify_second_support_spectrum.py
python -X utf8 verification/verify_explicit_walsh_atoms.py
python -X utf8 verification/verify_normal_form_obligations.py
python -X utf8 verification/probe_walsh_atom_semigroup.py
```

The programs have deliberately different roles:

- `verify_second_support_spectrum.py` exhaustively enumerates the exact spectra
  for `n=1,...,4`.
- `verify_explicit_walsh_atoms.py` evaluates the displayed low-dimensional
  quadratic atoms directly on all inputs.
- `verify_normal_form_obligations.py` tests the deterministic rank-lowering map
  and the bounded parity, budget, sign, and carry obligations used by the
  normal-form proof.
- `probe_walsh_atom_semigroup.py` calibrates the finite-atom model and its two
  destructive controls. It is a discovery/calibration probe, not independent
  proof evidence. It imports the helper
  `probe_recursive_slice_construction.py`, which is included only as that
  dependency.

The all-dimension theorem rests on the symbolic manuscript proof. Successful
bounded runs must not be interpreted as a proof for arbitrary dimension.

The executable files in this directory are licensed under the
[MIT License](LICENSE-CODE-MIT.txt).
