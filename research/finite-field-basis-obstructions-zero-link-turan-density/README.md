# Finite-field basis obstructions for zero link Turán density

## Manuscript

- [Read or download the PDF](finite-field-basis-obstructions-zero-link-turan-density.pdf)
- [LaTeX source](finite-field-basis-obstructions-zero-link-turan-density.tex)
- [BibTeX citation](CITATION.bib)
- [Verification program](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Public version: v0.1-beta (2 September 2026)
- DOI: [10.5281/zenodo.22253788](https://doi.org/10.5281/zenodo.22253788)
- Concept DOI: [10.5281/zenodo.22253787](https://doi.org/10.5281/zenodo.22253787)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/finite-field-basis-obstructions-zero-link-turan-density)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

Status: internally verified public Beta v0.1. The manuscript-level zero-trust audit and the PDF
artifact audit passed; external review remains pending.

## Main result

For an `r`-uniform hypergraph `H`, let `H_k` be its `k`-fold suspension and let
`pi_infty(H)` be the limiting Turán density of these suspensions. For a prime power `q` and
`m >= 0`, let `B_{q,m}(r)` be the `r`-graph of linearly independent `r`-sets in
`F_q^(r+m)`, with the zero vector isolated.

The manuscript proves that if there is no hypergraph homomorphism from `H` to `B_{q,m}(r)`, then

```text
pi_infty(H) >= product_{j=m+1}^infinity (1-q^(-j)) > 0.
```

Consequently, zero link Turán density forces a homomorphism into `B_{q,0}(r)` for every prime
power `q`.

The theorem is applied to a six-vertex three-graph `H_*` and its dual. Every vertex link in both
graphs is tripartite, but each graph has link Turán density at least
`product_{j>=1}(1-2^(-j))`, approximately `0.288788`. Thus tripartiteness of every vertex link is
not sufficient for zero link Turán density.

## Reproduction

The verification program uses the Python standard library only. It reconstructs the binary
three-dimensional basis hypergraph, checks positive and negative homomorphism controls, verifies
the two six-vertex obstructions, and independently checks that all their vertex links are
3-colourable.

```powershell
cd verification
.\run_all.ps1
```

## Scope

The manuscript does not classify all three-graphs of zero link Turán density. Finite-field
independent-set hosts and their density calculations are prior ingredients; the claimed
contribution is the arbitrary finite-hypergraph homomorphism formulation and the two six-vertex
examples passing every local tripartite-link test. The general formulation may be recognizable to
specialists as a folklore abstraction, so external priority confirmation remains pending.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
