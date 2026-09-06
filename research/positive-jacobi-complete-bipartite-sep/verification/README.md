# Exact verification

Requires Python 3.10+ and SymPy 1.14.0. From this directory, in your Python environment:

```text
python -m pip install -r requirements.txt
python run_checks.py
python -O run_checks.py
```

The runner performs four fixed checks serially and stops on the first failure or a 300-second per-process timeout. It does not install anything, contact the network, accept a parameter grid, or retry failed work. A timeout is not a mathematical conclusion. The fixed regressions use degree at most 15; symbolic certificate expansions have at most 1,346 numerator terms. No exhaustive parameter search is part of this package. The runner provides a wall-time limit, not an OS memory sandbox.

| Entry | What it establishes |
| --- | --- |
| `check_k4n_jacobi.py` | Symbolic rational-function identity and positive tail weights for the K4 family |
| `check_k5n_jacobi.py` | Symbolic rational-function identity and positive tail weights for the K5 family |
| `verify_second_tail_positive_kernel.py` | Seven exact positive-coefficient certificates covering Section 5; seven finite Euclidean comparisons and negative controls |
| `check_original_ehrhart.py` | Six direct h*-to-Ehrhart regressions, each with a perturbed-tail negative control |

`probe_uniform_tail_weights.py` is retained as an import name, not an exploration command. It exposes only the needed exact recovery routines, accepts the seven specified regression pairs, and contains no scan or executable main routine. Its arithmetic is unchanged from the internally reviewed helper; added guards reject unsupported inputs before computation. The K4/K5 and direct original-object check files are unchanged from the reviewed versions. The positive-kernel verifier only changes an internal document reference to Section 5 of the manuscript.

The general certificate is an exact polynomial-coefficient computation, not finite sampling. Its mathematical meaning still depends on the manuscript's reduction and complete partition of the parameter domain. The Euclidean and original-object comparisons are finite regressions only. Optimization mode does not disable the explicit validation checks.

Recorded outputs in `results/` report the actual tested environment and execution results. Source checksums are in the parent `SHA256SUMS.txt`. Python files are MIT licensed; generated outputs are CC0 1.0.
