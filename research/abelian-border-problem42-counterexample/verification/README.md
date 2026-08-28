# Exact finite verification

The mathematical proof establishes the infinite sparse construction. The
bundled program checks its finite certificates and a bounded positive control:

- the nearest-neighbor 28-periodic height skeleton;
- the full parity-compatible palette at all 28 center residues;
- one replacement walk for each of the 28 target residues;
- the four-of-five contamination bound;
- an 80-interval finite sparse prefix of length 18,033.

Requirements: Python 3 only; no third-party package is needed.

Run from the parent entry directory:

```powershell
python -X utf8 .\verification\verify_sparse_palette_counterexample.py
```

The first seven output lines must be:

```text
period=28
full_palette_centers=28
replacement_targets=28
five_pair_contamination_bound=PASS
finite_sparse_intervals=80
finite_sparse_prefix_length=18033
finite_sparse_full_local_palette=PASS
```

Finite verification does not replace the proof that the infinite sparse set
has the required separation, density and arithmetic-progression properties.
