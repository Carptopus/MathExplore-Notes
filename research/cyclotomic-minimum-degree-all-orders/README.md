# The minimum degree of nonnegative multiples of cyclotomic polynomials

## Manuscript

- [Read or download the PDF](cyclotomic-minimum-degree-all-orders.pdf)
- [LaTeX source](cyclotomic-minimum-degree-all-orders.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22137382](https://doi.org/10.5281/zenodo.22137382)
- Concept DOI: [10.5281/zenodo.22137381](https://doi.org/10.5281/zenodo.22137381)
- [Destructive verification suite](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (28 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Let `n>1`, let `p` be the smallest prime divisor of `n`, and put `P=n/p`.
The manuscript proves that every nonzero polynomial in `R_{>=0}[x]` divisible
by the `n`-th cyclotomic polynomial has degree at least `(p-1)P`. Equality
holds exactly for the positive scalar multiples of

```text
1 + x^P + ... + x^((p-1)P).
```

This gives a uniform affirmative solution of Conjecture 1 in John P.
Steinberger's 2012 paper for every integer `n>1`, including even integers,
prime powers, nonsquarefree orders, and orders with arbitrarily many distinct
prime factors.

## Proof mechanism

The proof constructs an explicit low-frequency trigonometric separation
certificate. A closed-form sector kernel vanishes precisely at the regular
`p`-gon positions and has a strict sign at every other exponent below the
candidate degree. Evaluation at primitive `n`-th roots makes the certificate
orthogonal to all relevant cyclotomic multiples. A unit-group reduction then
proves rigidity in the equality case.

## Relation to the two preceding entries

The all-orders theorem strictly subsumes the mathematical conclusions of the
[two fixed-parameter certificates](../cyclotomic-minimum-degree-first-two-cases/README.md)
and the [tail-projection infinite families](../cyclotomic-tail-projection-families/README.md).
Those entries remain public records of different certificate mechanisms and
of the discovery path; they are not needed for the proof of the present
theorem.

A targeted public search completed on 28 August 2026 found no paper, preprint,
author update, or indexed archive directly covering the all-orders theorem or
this sector-certificate mechanism. This records the search boundary and is not
an absolute worldwide-priority claim.

## Reproduction

The symbolic proof carries the all-orders quantifier. The bundled program is a
bounded destructive test suite for the kernel identity, sign pattern,
arithmetic reductions, exact divisibility checks, and two deliberate negative
controls. It requires Python, `mpmath`, and `sympy`.

From this entry directory:

```powershell
python -X utf8 .\verification\verify_full_n_sector_certificate.py
```

The final JSON object must report `"result": "PASS"`.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for computational exploration, proof development and organization,
adversarial checking, literature search, verification, and manuscript
preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Cyclotomic polynomials; nonnegative coefficients; minimum degree; roots of
unity; trigonometric kernels; separation certificates; regular polygons;
computer-assisted verification; AI-assisted mathematics.
