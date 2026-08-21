# Proper transposed sesqui arrays at all Sylvester--Hadamard powers

## Manuscript

- [Read or download the PDF](proper-sesqui-all-powers.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22045289](https://doi.org/10.5281/zenodo.22045289)
- [LaTeX source](proper-sesqui-all-powers.tex)
- [Verification code and certificates](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.2-beta (19 August 2026)
- Manuscript license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Verification licenses: documentation [CC BY 4.0](verification/LICENSE-DOCS-CC-BY-4.0.md),
  Python code [MIT](verification/LICENSE-CODE-MIT.txt), and JSON certificates/results [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified candidate proof; public mathematical review pending.

Version v0.2-beta makes two explanatory corrections identified by a
post-publication internal audit: it states the complement step in the Second
Multiplier Theorem argument and adds the closest known Youden
deletion--exchange framework to the prior-work boundary. The theorem,
construction, verification programs, and certificates are unchanged; the
verification package therefore remains the frozen v0.1-beta package.

## Main result

For every power of two $t=2^k$, $k\ge 2$, the manuscript constructs a proper transposed sesqui array

$$
SA^{\mathsf T}(4t-2,t,-,t-1,t:(2t-1)\times 2t).
$$

The columns use the classical Sylvester--Hadamard trace design. The contribution is a compatible ordering that makes the array proper: row--row concurrence is nonconstant while the required column--column and row--column concurrences remain constant.

## Proof outline

- A general two-fibre ordering theorem reduces the construction to a two-to-one finite-field map.
- Odd field dimensions use an explicit inverse-pair family.
- Even dimensions use a Subiaco map and reduce the zero-fibre condition to two fixed algebraic curves.
- Geometric irreducibility, Artin--Schreier trace covers, and a Hasse--Weil estimate handle all sufficiently large even dimensions.
- Exact polynomial-gcd certificates cover the fifteen remaining even dimensions, and an explicit array handles $t=4$.

## Scope of the claim

The Sylvester--Hadamard column skeleton and same-parameter unordered or triple-array constructions are prior work. The candidate new result is the proper ordered construction, with nonconstant row concurrence, for every power of two in the stated family. Priority remains qualified until broader public and expert review.

## Reproduction

The verification programs use Python 3.11 or newer and only the standard
library. From the verification directory, run:

```powershell
python -X utf8 run_reproduction.py
```

The frozen public run completed all twelve verification commands with status
`PASS_PUBLIC_REPRODUCTION_EXTERNAL_REVIEW_PENDING`. This confirms reproduction
of the distributed exact calculations; it does not replace independent review
of the mathematical proof or the priority claim.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively as an
AI-assisted research, verification, and writing tool and is not an author. The
paper contains the complete disclosure and responsibility statement.

## Keywords

Transposed sesqui array; proper sesqui array; row-column design; combinatorial design; Sylvester--Hadamard design; finite field; two-to-one map; o-polynomial; Subiaco hyperoval; algebraic curve; Artin--Schreier cover; Hasse--Weil bound; computer-assisted proof.
