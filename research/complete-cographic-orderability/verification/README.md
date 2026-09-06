# Explicit example checks

Requires Python 3.10 or newer; standard library only.

```text
python verify_examples.py
```

The checker verifies the tetrahedral K4 and the listed projective-plane K6 complex:

- distinct triangular faces, exactly two faces per edge, and cyclic vertex links;
- a single induced adjacency cycle on every bond (7 for K4, 31 for K6);
- rejection after deleting each face, duplicating a face, deleting each adjacency,
  or inserting each missing adjacency;
- rejection of a disconnected two-regular graph by the cycle predicate.

The accepted input sizes are fixed at 4 and 6. The script does not search for orderings,
test arbitrary parameters, or certify the infinite negative statements. Those rely on
the manuscript proofs. It uses explicit exceptions rather than removable Python assertions.

Code license: MIT. The mathematical examples are reproduced from the manuscript and its cited predecessor.
