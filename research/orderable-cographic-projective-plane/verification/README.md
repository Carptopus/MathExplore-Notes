# Exact verification

The verification package contains three independent finite positive controls:

- `verify_k6_cographic_counterexample.py` reconstructs `M*(K6)`, all 31
  circuits, the 30-pair global adjacency relation, and 3-connectivity;
- `verify_k6_projective_plane_mechanism.py` checks the ten-face triangulation,
  its face automorphisms, the three bond orbits, and their cycle representatives;
- `verify_rp2_stellar_family.py` checks a finite chain of stellar subdivisions.

Run all checks from the repository root:

```powershell
pwsh -NoProfile -File .\research\orderable-cographic-projective-plane\verification\run_all.ps1
```

The scripts use only the Python standard library. They are finite calibration
and reproducibility checks; the projective-plane theorem and infinite family
are proved in the manuscript.

