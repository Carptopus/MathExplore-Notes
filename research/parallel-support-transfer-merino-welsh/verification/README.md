# Fixed original-object controls

Python 3.10 or later; standard library only. From this directory:

```powershell
python run_control_checks.py
python -O run_control_checks.py
```

Use the interpreter configured for your environment; MathExplore uses its project `.venv`.

The checker reconstructs exactly seven fixed binary-vector or graphic matroids, compares their subset-rank Tutte evaluations with `results/transfer_s2.json`, and checks that promoting the multitheta negative control to an accepted case fails. A deliberately altered result value must fail comparison as well. Guards use explicit exceptions and remain active under `-O`.

The input verifier enforces a 14-element hard limit. The seven cases inspect fewer than 100,000 subsets in total; there is no parameter expansion, solver, download, or persistent output. The runner fails if its measured runtime exceeds 60 seconds.

Positive cases cover independent and dependent parallel directions, an extra internal singleton, a small internal class, an equality pair, and an admissible multitheta graph. The negative graph has two parallel uv edges and four length-two paths: T_M(0,2)=62, b(M)=64.

These checks use the earlier conservative corank/2 budget, not the full girth improvement. They neither enumerate all matroids nor prove the general transfer, corank-two or sparse paving theorems. All general claims rely on the manuscript proofs.
