# Exact rank-four verification

The two Python programs independently reconstruct the 512 flags of `{4,4}_{(8,0)}` using different
coordinate encodings and facet-reflection implementations. Both verify the required intersection
conditions for the two exceptional rank-four symmetry types. The second implementation does not
import the first.

Both implementations use SymPy 1.14 for deterministic Schreier--Sims membership in the largest
upper group. Their construction models are independent, but the underlying group-membership kernel
is shared. Every explicit closure is preceded by an exact group-order check and refuses groups of
order greater than 4096.

Run from PowerShell 7:

```powershell
.\run_all.ps1 -Python python
```

Optional safety parameters:

```powershell
.\run_all.ps1 -Python python -MemoryLimitMB 1024 -TimeoutSeconds 120
```

The runner executes serially, monitors the complete process tree, terminates it on a memory or time
limit breach, and reports peak private memory. A successful run ends with both scripts exiting zero;
the first reports `negative_control_wrong_top_voltage_passed=False`, and the second reports
`independent_schreier_verifier=PASS`.

The verification establishes the two finite rank-four base cases used by the manuscript. The general
all-rank theorem also depends on the written mathematical argument and cited source theorems.
