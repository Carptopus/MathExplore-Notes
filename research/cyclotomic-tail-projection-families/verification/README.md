# Exact condition checker

The checker uses only the Python standard library. Run from this entry
directory with PowerShell:

```powershell
python -X utf8 .\verification\verify_general_tail_condition.py --primes 37 41 43 47 53
```

The example must report:

```text
"tail_condition_strict": true
"outside_steinberger_condition": true
"result": "PASS"
```

The program uses integer and rational arithmetic to evaluate the condition in
Theorem 1.1 and Steinberger's reciprocal condition. It accepts only strictly
increasing distinct odd primes and requires at least four total factors.

This program calibrates the explicit condition. The infinite-family theorem
depends on the symbolic proof in the manuscript, not on finite computation.
