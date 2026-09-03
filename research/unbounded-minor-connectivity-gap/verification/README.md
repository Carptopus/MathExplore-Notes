# Verification

`verify_general_lower_model.py` independently reconstructs the labelled graph $M_{12}$, its
independent blow-up, the explicit branch-set model, and the full quotient used for the lower bound
in Theorem 1. It checks the complement-component calculation against NetworkX vertex connectivity
for $t=2,\ldots,8$.

Requirements:

- Python 3;
- NetworkX 3.6.1;
- PowerShell 7 for the exact-output runner.

From this directory:

```powershell
.\run_all.ps1 -Python python
```

Alternatively, run the Python verifier directly:

```powershell
python verify_general_lower_model.py
```

The PowerShell runner also requires exact agreement with
`results/general-lower-model-t2-t8.txt`. The Python verifier first runs two destructive controls
and must reject a disconnected branch set and overlapping branch sets.

The finite checks validate the implementation and sample instances; they are not used to infer the
universal theorem.
