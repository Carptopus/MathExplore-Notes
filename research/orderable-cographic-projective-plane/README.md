# Projective-plane triangulations yield orderable cographic matroids

## Manuscript

- [Read or download the PDF](orderable-cographic-projective-plane.pdf)
- [LaTeX source](orderable-cographic-projective-plane.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22165775](https://doi.org/10.5281/zenodo.22165775)
- Concept DOI: [10.5281/zenodo.22165774](https://doi.org/10.5281/zenodo.22165774)
- [Exact verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (30 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Certificate-data license: [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified candidate proof; external mathematical review pending.

## Main results

If `T` is any finite simplicial triangulation of the real projective plane and
`G` is its 1-skeleton, the manuscript proves that the cographic matroid
`M*(G)` is orderable. The global ordering is induced by face corners; an Euler
characteristic argument forces the induced adjacency on every bond to be a
single cycle.

Starting with the six-vertex triangulation whose 1-skeleton is `K6` and
repeatedly applying stellar subdivision gives infinitely many pairwise
nonisomorphic 3-connected, regular, binary, non-graphic, orderable matroids.
This family gives counterexamples to Crenshaw--Oxley Conjecture 4. The smallest
member is the explicit matroid `M*(K6)`.

## Proof and computational boundary

The general theorem and infinite family are proved topologically. The included
Python programs exactly reconstruct the `K6` cographic representation, all 31
bonds, the global adjacency certificate, the projective-plane face mechanism,
and finite stellar-subdivision positive controls. The finite checks do not
replace the general proof, and no timeout or failed search is used as
mathematical evidence.

## Scope and prior-work boundary

The result does not classify all orderable cographic matroids and does not
extend the projective-plane theorem to arbitrary closed surfaces. It does not
conflict with the known 4-connected regular theorem because every member has
an exact 3-separation. A directed search found no source directly covering
`M*(K6)` or the projective-plane construction; this is a documented search
boundary, not a worldwide-priority guarantee.

## Reproduction

Requirements: PowerShell 7 and Python 3.10 or newer. No third-party Python
package is required. From the repository root run:

```powershell
pwsh -NoProfile -File .\research\orderable-cographic-projective-plane\verification\run_all.ps1
```

The command must finish with
`PASS: all orderable-cographic projective-plane checks completed`.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature organization, proof development and stress testing, exact
verification, adversarial auditing, and manuscript preparation. The manuscript
contains the complete disclosure and responsibility statement.

## Keywords

Matroid theory; orderable matroids; cographic matroids; binary matroids;
regular matroids; graph embeddings; real projective plane; simplicial
triangulations; stellar subdivision; counterexamples; AI-assisted mathematics.
