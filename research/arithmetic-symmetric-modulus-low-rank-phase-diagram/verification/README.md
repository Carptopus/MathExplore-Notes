# Verification controls

These scripts are regression, identity and destructive controls for formulas
used by the manuscript. They are not substitutes for the general proofs.

- `check_finite_p_*`, `check_frobenius_candidate.py`,
  `check_complex_frobenius_closure.py` and `check_real_frobenius_upper.py`
  cover the two-dimensional frontier and Frobenius specialization.
- `check_rank_two_all_dimensions_frobenius.py` and
  `check_schatten_nilpotent_family.py` cover the arbitrary-dimensional
  rank-at-most-two Frobenius theorem and its nilpotent calibration.
- the remaining five scripts cover the four-dimensional Gram reduction,
  subquadratic separation, weighted-chain transition and the two cubic strata.

Run all checks from this directory with Python 3.11 or later:

```powershell
python -m pip install -r requirements.txt
python run_all.py
```

The accepted project environment used NumPy 2.5.2 and SymPy 1.14.0. Individual
scripts use fixed random seeds where sampling is present. Successful finite
sampling is only a regression signal and never a general proof claim.
