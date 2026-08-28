# Exact finite verification

The mathematical proof establishes the all-parameter classification. These
three independent finite routes calibrate the formulas and boundary cases:

- `scan_rectangular_boxes.py` implements the Ding--Dong transfer recurrence,
  reproduces their $[4]\times[2]\times[3]$ polynomial, checks the bounded
  palindromicity map, and tests both near-leading coefficient formulas;
- `verify_next_to_leading.py` directly enumerates support complements and
  permitted single-cell increments, including a negative control that defeats
  the retracted preliminary support formula;
- `verify_lpp_frontier.py` uses a separate last-passage frontier dynamic
  program to test binary supports and the first ternary $d=3$ coefficient.

Requirements: Python 3 only; no third-party package is needed.

Run from the parent entry directory:

```powershell
python -X utf8 .\verification\scan_rectangular_boxes.py
python -X utf8 .\verification\verify_next_to_leading.py
python -X utf8 .\verification\verify_lpp_frontier.py
```

The commands must respectively report:

```text
calibration: PASS
near-extremal complement regression: PASS
frontier regression: PASS
```

These finite checks do not prove the classification for unbounded parameters.
The general result rests on the path-complementation, minimum-separator and
saturation arguments in the manuscript.
