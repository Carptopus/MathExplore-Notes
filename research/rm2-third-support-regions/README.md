# Exact regions and low-polar-rank recursion in the third support spectrum of binary second-order Reed--Muller codes

## Manuscript

- [Read or download the PDF](rm2-third-support-regions.pdf)
- [LaTeX source](rm2-third-support-regions.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22165319](https://doi.org/10.5281/zenodo.22165319)
- Concept DOI: [10.5281/zenodo.22165318](https://doi.org/10.5281/zenodo.22165318)
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

Let $\mathcal S_n^{(3)}$ be the set of support sizes of three-dimensional
subcodes of the binary second-order Reed--Muller code $RM_2(2,n)$. The
manuscript proves:

- for every $n\ge4$, the minimum $7\cdot2^{n-4}$ is isolated and the next
  support is at least $2^{n-1}$;
- for every $n\ge7$, the largest nonfull support is
  $2^n-2^{n-6}$, and the bound is sharp;
- the exact sets $\mathcal S_n^{(3)}$ for $2\le n\le9$;
- for every $n\ge8$, an exact classification of the complete near-full
  interval with fewer than $2^{n-5}$ common zeros;
- a finite sound-and-complete constructive recursion whenever one nonzero
  output combination has nonzero zero-frequency Walsh coefficient and polar
  rank two or four;
- for every $n\ge12$, the infinite forbidden ray
  $493\cdot2^{n-9}\notin\mathcal S_n^{(3)}$.

## Proof and computational boundary

The general arguments use Reed--Muller weight restrictions, Warning's second
theorem, Fano-plane rank geometry, maximal Pfaffians, Walsh transforms, and the
canonical decomposition of alternating pencils. The verification package
checks the finite orbit sets, arithmetic branches, affine-mask and sign
transitions, relation kernels, terminal core outputs, and the finite obstruction
behind the forbidden ray. Arbitrary-length identities and dimension-independent
reductions are proved in the manuscript; no timeout or failed search is used as
nonexistence evidence.

## Scope and prior-work boundary

The paper does not determine the complete third support spectrum for every
dimension. Its finite recursion excludes Walsh-zero selected directions and
does not cover the layer in which every nonzero Walsh direction has polar rank
at least six. It does not count subcodes or classify quadratic nets up to
isomorphism.

The closest checked work treats the ordinary quadratic weight spectrum,
two-dimensional support positions, or higher spectra of $RM_q(2,2)$ with the
number of variables fixed and the field varying. The current search found no
direct source covering the retained theorems; this is a documented search
boundary, not a worldwide-priority guarantee.

## Reproduction

Requirements: PowerShell 7 and Python 3.10 or newer. No third-party Python
package is required. From the repository root run:

```powershell
pwsh -NoProfile -File .\research\rm2-third-support-regions\verification\run_all.ps1
```

The command must finish with
`PASS: all RM2 third-support-region checks completed`.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature organization, proof development and stress testing,
symbolic and finite verification, adversarial auditing, and manuscript
preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Reed--Muller codes; higher support spectra; quadratic Boolean functions; Walsh
transforms; alternating pencils; Fano plane; Pfaffians; Kronecker blocks;
computer-assisted proof; AI-assisted mathematics.
