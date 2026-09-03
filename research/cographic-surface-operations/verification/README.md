# Verification

These scripts provide exact finite checks for the examples and calibration
statements in the manuscript. They use only the Python standard library.

From this directory, run:

```powershell
.\run_all.ps1 -Python python
```

The four entry points are:

- `verify_rp2_stellar_family.py`: shared graph, bond, and face-adjacency
  implementation, together with projective-plane positive controls;
- `verify_nonorientable_triangle_sum_family.py`: constructs and checks the
  first five nonorientable genera;
- `check_vertex_split_nonclosure.py`: exhausts all 90 nontrivial single vertex
  splits of the labelled nine-vertex Klein-bottle base example;
- `probe_two_step_seam_persistence.py`: bounded diagnostic search with a hard
  limit of 500 candidates. It exits nonzero if a positive prime witness is
  found, so the aggregate runner cannot report `PASS` in that case.

The first three checks support finite statements in the manuscript. The
bounded two-step `NO_HIT` is explicitly not evidence for a general theorem.
All general results are proved in the manuscript independently of these
computations.
