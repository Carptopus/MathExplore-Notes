# Finite verification checks

Requires Python 3 with the standard library only. From this directory:

```sh
python run_all.py
```

The runner executes both checks serially in normal and optimized (`-O`) modes, with a 60-second timeout per process. A failed check or timeout returns a nonzero exit code. No downloads or external solvers are used.

- `verify_triangle_defect.py` checks the cyclic-flat defect formula on four fixed weighted triangles and tests the loss of information caused by forgetting multiplicities. Constant-potential and coarse-configuration controls are included.
- `verify_gluing_interfaces.py` checks five fixed cycle-skeleton examples, including bare paths and parallel multiplicities, against directly enumerated cyclic flats. Damaged-weight and unsimplified minimal-cycle negative controls are included.

These are bounded exact-arithmetic regressions, not a general proof certificate. They do not independently validate every interface lemma or the complete rank induction; in particular, they do not separately test every two-sided interface in Lemmas 5.1 and 5.2. The mathematical argument is in the manuscript.

The individual scripts have size guards. Their fixed examples are small; the cyclic-flat enumerator rejects more than 14 edges, and intermediate generated-space collections are capped. Both scripts use explicit failures rather than assertions that disappear under `-O`.
