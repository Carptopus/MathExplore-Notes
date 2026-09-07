# Circuit orderability of cographic matroids of complete and complete bipartite graphs

This paper classifies consistent reversible circuit orderings for two complete graph families.

- [Paper (PDF)](complete-cographic-orderability.pdf)
- [LaTeX source](complete-cographic-orderability.tex)
- [BibTeX citation](CITATION.bib)
- Version DOI: [10.5281/zenodo.22597680](https://doi.org/10.5281/zenodo.22597680)
- Concept DOI: [10.5281/zenodo.22597679](https://doi.org/10.5281/zenodo.22597679)
- [Zenodo record](https://zenodo.org/records/22597680)
- [Example checks](verification/README.md)
- Author: Carptopus ([carptopus@163.com](mailto:carptopus@163.com))
- Version: v0.1-beta, 7 September 2026
- Paper and documentation: [CC BY 4.0](LICENSE.md); verification code: [MIT](verification/LICENSE-CODE-MIT.txt)

## Main results

1. For every integer `n >= 4`, the cographic matroid `M*(K_n)` is orderable exactly when `n = 4` or `n = 6`.
2. For all positive integers `r, s`, `M*(K_{r,s})` is orderable exactly when `min(r,s) <= 2`.

The complete-graph proof reconstructs a closed simplicial surface from any consistent ordering, then uses a mod-two face equation and a link-degree obstruction. The bipartite classification adds a direct obstruction for `K_{3,s}` to previously known cases. These are structural proofs, not extrapolations from finite enumeration.

## Relation to earlier work

The positive `K6` example was already established in [Projective-plane triangulations yield orderable cographic matroids](https://doi.org/10.5281/zenodo.22165775). [Triangle sums, peripheral cycles, and contractions for orderable cographic matroids](https://doi.org/10.5281/zenodo.22286132) supplies related construction and operation results. The present paper classifies arbitrary orderings on the two specified graph families; it does not replace those more general construction results or classify all cographic matroids.

Crenshaw–Oxley's four-connected regular theorem covers the cases `r,s >= 4`, and their `K5` and `K3,3` negative examples are explicitly credited. Their original paper and Crenshaw's 2023 dissertation are cited in the manuscript.

## Verification and status

Run `python verification/verify_examples.py` with Python 3.10 or newer. No third-party package is required. The checker verifies all 7 bonds of the tetrahedral `K4` and all 31 bonds of the given `K6` complex, with destructive negative controls. It does not prove the infinite exclusion statements.

Internally checked preprint; external mathematical review and formal peer review are pending. OpenAI Codex assisted with research, verification, and writing; Carptopus is responsible for the manuscript.
