# Every two-vertex premaniplex is the symmetry type graph of a finite abstract polytope

This directory contains the manuscript and exact rank-four verification for the theorem that every
connected two-vertex premaniplex of rank at least three is the full symmetry type graph of a finite
abstract polytope.

- [Read or download the PDF](two-vertex-polytopality.pdf)
- [LaTeX source](two-vertex-polytopality.tex)
- [BibTeX citation](CITATION.bib)
- [Verification package](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Public version: v0.1-beta (3 September 2026)
- DOI: [10.5281/zenodo.22274310](https://doi.org/10.5281/zenodo.22274310)
- Concept DOI: [10.5281/zenodo.22274309](https://doi.org/10.5281/zenodo.22274309)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/two-vertex-polytopality)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

## Main result

For every rank `r>=3`, each of the `2^r-1` connected two-vertex premaniplexes is realized as the
full symmetry type graph of a finite abstract polytope. The proof treats every set of internal link
colors simultaneously and establishes the remaining path-intersection identity. Two exceptional
rank-four base types are supplied by exact finite constructions.

The result upgrades the known realization of all two-vertex types by finite maniplexes to realization
by finite abstract polytopes. It also completes the cases left outside the previously known special
link-set constructions.

Status: internally verified public Beta v0.1. The proof and full manuscript have passed independent
zero-trust audits, and the PDF and bounded verification package have passed artifact checks. External
mathematical review remains pending.

## Reproduction

The rank-four verification requires Python 3, SymPy 1.14, and PowerShell 7. From PowerShell:

```powershell
cd verification
.\run_all.ps1 -Python python
```

The runner executes the two implementations serially, enforces a per-run process-tree memory limit
and timeout, and reports peak private memory. See [verification/README.md](verification/README.md)
for the exact scope and independence boundary.

## Scope

This is a complete realization theorem for connected two-vertex premaniplexes. It does not classify
polytopes with more symmetry-type vertices, and it does not claim external peer review or absolute
priority over unindexed work.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
