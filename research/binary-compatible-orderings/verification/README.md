# Exact verification

The two formal programs certify the exhaustive four-dimensional base lemma:

- `classify_n4.py` uses hyperplane-coordinate orbit prefixes;
- `verify_n4_independent.py` independently implements the finite-field
  operations and uses Fano line-position prefixes.

Both must return exactly four normalized solutions. They share the necessary
`GL(4,2)` normalization and prefix-search architecture; their agreement checks
the complete invariant implementation, not two unrelated search designs.

`probe_binary_compatible.py` is an optional discovery and calibration probe.
It is reproducible and included in the checksum gate, but it is not part of the
formal four-dimensional certificate.

From the repository root run:

~~~powershell
pwsh -NoProfile -File .\research\binary-compatible-orderings\verification\run_all.ps1
~~~

The general all-dimensional theorem is proved in the manuscript. These scripts
do not replace the initial-flag and unique-lift arguments.
