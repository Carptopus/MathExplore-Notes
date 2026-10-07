# Parallel-support transfer and sparse paving quotients in a one-sided Merino–Welsh inequality

Author: Carptopus · Version v0.1-beta (7 October 2026)

Archived version: [10.5281/zenodo.23212705](https://doi.org/10.5281/zenodo.23212705). The Zenodo reproducibility ZIP preserves the initial public package at Git commit `2a6a12f2b681f1f73a8d832fb0c0b01fe77bbdb5`; subsequent DOI backfill changes only citation and index metadata, not the manuscript, PDF, TeX or verification files.

This manuscript combines a conditional transfer mechanism, an all-parameter sparse paving quotient application, and a complementary strict corank-two theorem. It does not resolve the full Merino–Welsh conjecture.

- [Manuscript](manuscript.md)
- [PDF](paper/main.pdf) and [LaTeX source](paper/main.tex)
- [Finite verification](verification/README.md)
- [BibTeX](CITATION.bib)
- [Checksums](SHA256SUMS.txt)

## Results and boundaries

For a finite loopless, coloopless matroid M, write b(M)=T_M(1,1).

1. If a flat F is spanned by parallel classes of size at least k>=2, its nonempty quotient Q satisfies T_Q(0,2)>=b(Q), and 2^k-1-k >= corank(Q)/girth(Q), then T_M(0,2)>=b(M). Strict quotient inequality transfers. Empty quotients are covered separately.
2. If the flat spanned by all nontrivial parallel classes has corank two, and its quotient has two disjoint bases, then T_M(0,2)>b(M).
3. If a parallel-spanned flat has a loopless, coloopless sparse paving quotient of rank c>=1 and size m>=2c, then T_M(0,2)>=b(M), without a bound on total rank or dependencies among parallel directions. Uniform quotients are included.

The third result does not cover every rank-two quotient in the second result. The paper cites the earlier [parallel-support corank-at-most-one preprint](https://doi.org/10.5281/zenodo.22296382), whose published version remains unchanged. Known quotient endpoints and standard recurrences are explicitly credited. A classical multitheta graph family calibrates the budget, not an optimal universal threshold.

Finite checks do not replace the proofs. These results do not cover all paving quotients or all two-base matroids. The prior-art comparison is bounded and is not a claim of global priority.

## Review and disclosure

The writing-preparation proof package and complete manuscript have passed independent project audits. The ten-page PDF has passed full-page rendering and conversion-fidelity checks. These checks are distinct from external mathematical review and formal peer review, which are pending.

AI tools assisted with research, checking, literature comparison, and writing. Carptopus is the responsible author.

Manuscript and documentation: [CC BY 4.0](LICENSE.md). Verification code: [MIT](verification/LICENSE-CODE-MIT.txt).

Keywords: matroid theory; Tutte polynomial; Merino–Welsh inequality; parallel support; sparse paving matroids; deletion–contraction; quotient girth.
