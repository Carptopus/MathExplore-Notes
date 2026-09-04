# Real-rooted h-star polynomials of rank-two matroids with parallel classes of size at most three

This directory contains an internally audited manuscript proving a new infinite structural case
of real-rootedness for Ehrhart `h*`-polynomials of matroid base polytopes.

- [PDF manuscript](rank-two-matroid-hstar-size-three.pdf)
- [LaTeX source](rank-two-matroid-hstar-size-three.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22305179](https://doi.org/10.5281/zenodo.22305179)
- Concept DOI: [10.5281/zenodo.22305178](https://doi.org/10.5281/zenodo.22305178)
- [Verification program](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Public version: v0.1-beta (4 September 2026)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/rank-two-matroid-hstar-size-three)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified public Beta; external mathematical review pending.

## Main result

Let `M` be a rank-two matroid. If every nonloop parallel class of `M` has size at most three,
then the Ehrhart polynomial `h*(P(M),x)` of its base polytope has only real zeros. Consequently,
its coefficient sequence is log-concave and unimodal.

The proof is computer-assisted only at the finite boundary: an exact Sturm certificate settles
the remaining `n=9` estimate, and exact checks cover all 31 connected small partitions and six
disconnected types. Every larger ground set is covered by one uniform analytic estimate.

## Prior-work boundary

Ferroni, Jochemko and Schroeter proved the corresponding result for rank-two sparse paving
matroids, which after loop deletion have parallel classes of size at most two. The candidate
contribution here advances that structural bound from two to three, including all connected and
disconnected boundary cases. It does not claim real-rootedness for arbitrary rank-two matroids or
for all matroid base polytopes.

The manuscript also records the Laguerre scaling condition and the additional uniformity
obligations that would be needed to extend this method to a general fixed parallel-class bound.

## Reproduction

The verifier requires Python 3 and SymPy 1.14. From the repository root, run:

```powershell
pwsh -NoProfile -File .\research\rank-two-matroid-hstar-size-three\verification\run_all.ps1
```

The manuscript PDF is built from `rank-two-matroid-hstar-size-three.tex` with Tectonic and a
fixed source-date epoch:

```powershell
$env:SOURCE_DATE_EPOCH = '1788547200'
tectonic .\research\rank-two-matroid-hstar-size-three\rank-two-matroid-hstar-size-three.tex
```

The runner executes the verifier in ordinary and optimized (`-O`) modes and requires both outputs
to match the frozen result. These computations validate the symbolic certificate and finite
boundary; the uniform theorem for all larger ground sets is proved analytically in the manuscript.

## AI-assisted research disclosure

Carptopus is the responsible author and takes responsibility for the claims, proofs, source use,
and released artifacts. OpenAI Codex was used for AI-assisted literature organization, proof
development and stress testing, exact verification, adversarial auditing, and manuscript
preparation. The manuscript contains the complete disclosure and responsibility statement.

## Keywords

Matroid base polytopes; Ehrhart h-star polynomials; real-rootedness; rank-two matroids; parallel
classes; log-concavity; Sturm sequences; reproducible mathematics; AI-assisted mathematics.
