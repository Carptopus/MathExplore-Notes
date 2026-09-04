# Verification

`verify_corank_one_parallel_support.py` checks the finite and algebraic interfaces used by the
manuscript:

- the exact basis-activity formula for parallel extensions;
- all binary simple matroids of ranks two and three;
- strictness throughout the corank-one class;
- varied parallel-class multiplicities and uniform nonbinary samples;
- the spanning-singleton, inside-hyperplane, and outside-hyperplane deletion--contraction cases;
- equality cases, destructive controls, and two rank-$(r-2)$ counterexamples.

Requirements: Python 3.10 or later and PowerShell 7. No third-party Python packages are required.

From the repository root:

```powershell
pwsh -NoProfile -File .\research\parallel-support-rank-merino-welsh\verification\run_all.ps1
```

Alternatively, from this directory:

```powershell
python -B verify_corank_one_parallel_support.py
python -B -O verify_corank_one_parallel_support.py
```

The runner requires ordinary and optimized execution to match the frozen output in
`results/verification-output.txt`. This ensures that correctness checks do not disappear when
Python assertions are disabled.

The computations validate the implementation and selected proof interfaces. The universal
theorem is proved in the manuscript rather than inferred from finite enumeration.
