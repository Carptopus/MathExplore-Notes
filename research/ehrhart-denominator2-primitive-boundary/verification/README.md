# Verification material

These programs accompany the manuscript *Near-Minimal Ehrhart Data on the
Primitive-Triangle Boundary of Denominator-Two Polygons*.

They require Python 3.11 or newer, use only the standard library, and require
no network access or computer algebra system. From the entry directory, run:

```powershell
python -X utf8 verification/verify_mod8_obstruction.py
python -X utf8 verification/verify_near_lower_gap.py
python -X utf8 verification/verify_next_boundary_reduction.py
python -X utf8 verification/verify_width_one_shell_gate.py
```

The programs have distinct roles:

- `verify_mod8_obstruction.py` checks the slice, fiber-symmetry, and direct
  geometry forms of the parity identity and includes two negative controls.
- `verify_near_lower_gap.py` checks the low-region classification, the two
  bottom construction families, the $3N-3$ family, and a destructive control.
- `verify_next_boundary_reduction.py` exhausts the theoretically reduced
  $I=3N-2$ branch and verifies the unique $(10,28)$ representative.
- `verify_width_one_shell_gate.py` calibrates the width-one exclusion and
  verifies the sharp infinite-family formula through the documented finite
  range. It imports the two included helper modules.
- `analyze_realizability_spectrum.py` is an included helper and optional
  exploratory entry point.

The all-parameter claims rest on the symbolic manuscript proof. Successful
bounded runs must not be interpreted as proofs outside their stated ranges.

The executable files in this directory are licensed under the
[MIT License](LICENSE-CODE-MIT.txt).
