# Exact verification

`verify_middle_runner_counterexample.py` uses exact rational arithmetic to
check the finite evidence accompanying the manuscript.

It verifies:

- the explicit counterexample at offset `1/4`;
- the positive control at offset `0`;
- invariance under integer translation of an initial position; and
- the closed median formula at 775 rational representatives in `[0,1]` with
  denominator at most 50.

## Run

Python 3.9 or newer is sufficient; there are no third-party dependencies.

```powershell
python -X utf8 verification\verify_middle_runner_counterexample.py
```

Expected final lines:

```text
closed-form offsets checked: 775
PASS
```

The finite checks are supplementary evidence and regression tests. The claim
for all real offsets is proved in the manuscript by exact piecewise
integration.
