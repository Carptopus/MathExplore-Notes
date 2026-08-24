# Finite proof-identity calibration

This directory contains a finite destructive check of the recurrence identities used in the manuscript's marked-clique capacity theorem.

## Files

- `verify_marked_clique_recurrence.py`: enumerates the admissible marked-clique states and checks both split identities and the inclusion required by the exact sequence.
- `scan_s3_chordal_capacity.py`: shared exact-composition and chordal-graph utilities.
- `results/marked-clique-recurrence-atlas.json`: retained output for the default range.

## Reproduce

Requirements: Python 3 and NetworkX. The released result was reproduced with Python 3.13 and NetworkX 3.6.1.

Run from this directory:

```powershell
python .\verify_marked_clique_recurrence.py --max-n 6 --output .\recomputed.json
```

The expected summary is 21,023 checked states and zero failures. The recomputed JSON should be byte-identical to `results/marked-clique-recurrence-atlas.json`.

## Scope

This is a finite calibration of the proof identities, not a proof of the theorem. The general result is established by the argument in the manuscript.
