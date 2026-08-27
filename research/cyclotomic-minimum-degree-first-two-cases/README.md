# Exact certificates for the first two cases not covered by Steinberger's cyclotomic minimum-degree theorem

## Manuscript

- [Read or download the PDF](cyclotomic-minimum-degree-first-two-cases.pdf)
- [LaTeX source](cyclotomic-minimum-degree-first-two-cases.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22124096](https://doi.org/10.5281/zenodo.22124096)
- Concept DOI: [10.5281/zenodo.22124095](https://doi.org/10.5281/zenodo.22124095)
- [Exact certificates and verification](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (27 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Certificate-data license: [CC0 1.0](verification/results/LICENSE-DATA-CC0.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Steinberger conjectured that if `p` is the smallest prime divisor of `n`, the
lowest-degree nonzero polynomial with nonnegative coefficients divisible by
the `n`-th cyclotomic polynomial has degree `(p-1)n/p`, with the regular
`p`-gon as the unique monic minimizer. His general theorem leaves

```text
46189 = 11*13*17*19
96577 = 13*17*19*23
```

as the first two uncovered parameters. This manuscript proves the conjecture
for both:

- for `n=46189`, the minimum degree is `41990`, and the unique monic minimizer
  is `1+x^4199+...+x^(10*4199)`;
- for `n=96577`, the minimum degree is `89148`, and the unique monic minimizer
  is `1+x^7429+...+x^(12*7429)`.

The conclusions hold over nonnegative real coefficients. They are two exact
fixed-parameter results, not a proof of the general conjecture.

## Proof and verification

For each parameter, the proof provides an integer element of the orthogonal
complement of the cyclotomic CRT-array space. It vanishes on the regular
polygon support and is strictly negative at every other exponent through the
proposed boundary. This simultaneously proves the lower bound and forces
boundary uniqueness.

The retained certificates are checked in two independent ways: direct exact
evaluation through tensor marginals and explicit expansion of the full
multidimensional array with every coordinate fiber sum checked. A redundant
strict certificate independently verifies the lower-degree exclusion for
`n=46189`.

## Scope and prior-work boundary

The CRT-array space and separation criterion are due to Steinberger. This
entry contributes exact integer certificates and reproducible verification
for the first two values explicitly listed outside his theorem. It does not
settle the next listed value `215441`, all squarefree integers with four prime
factors, an infinite parameter family, or the general conjecture.

A targeted search completed on 27 August 2026 found no public paper, preprint,
author update, or indexed computational archive directly treating these two
certificates. This is the recorded search boundary, not an absolute worldwide
priority claim.

## Reproduction

Python 3 and NumPy are required. From this entry directory, follow the six
commands in [verification/README.md](verification/README.md). Every command
must finish with a `PASS` result.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature discovery, computational exploration, certificate
construction, proof stress testing, verification-code review, adversarial
auditing, and manuscript preparation. The manuscript contains the full
disclosure and responsibility statement.

## Keywords

Cyclotomic polynomials; nonnegative coefficients; minimum degree; exact
certificates; Chinese remainder theorem; tensor arrays; linear programming;
computer-assisted proof; AI-assisted mathematics.
