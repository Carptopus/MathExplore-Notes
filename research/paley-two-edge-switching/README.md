# Paley two-edge switching for proper transposed sesqui arrays

## Manuscript

- [Read or download the PDF](paley-two-edge-switching.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22059004](https://doi.org/10.5281/zenodo.22059004)
- [LaTeX source](paley-two-edge-switching.tex)
- [Verification code and reproduced results](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.3-beta (22 August 2026)
- Manuscript license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Verification licenses: documentation [CC BY 4.0](verification/LICENSE-DOCS-CC-BY-4.0.md),
  Python code [MIT](verification/LICENSE-CODE-MIT.txt), and JSON results [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

For every odd prime power $q\equiv3\pmod4$, $q\geq11$, the manuscript
constructs a proper transposed sesqui array

$$
SA^{\mathsf T}\!\left(
2q,\frac{q+1}{2},-,\frac{q-1}{2},\frac{q+1}{2}:q\times(q+1)
\right).
$$

The construction starts from the classical Paley matching between nonzero
squares and nonsquares, crosses two matching edges, and orders the resulting
row blocks cell by cell. Five quadratic-character conditions preserve the
required column--column and row--column concurrences. A nonzero second-moment
defect forces row--row concurrence to be nonconstant, making the array proper.

## Proof outline

- Exact symbolic identities establish the two-edge switch and moment defect.
- A quadratic-character count gives the exact number of admissible switches.
- The count is controlled by a family of elliptic curves; the Hasse bound gives
  existence for every $q\geq19$.
- An explicit $q=11$ witness closes the remaining case.
- Independent prime-field, $GF(27)$, and generic finite-field programs audit
  the formulas, boundary behavior, and complete-array parameters.

## Scope of the claim

The Paley parameter set, the underlying column skeleton, same-parameter triple
arrays, quadratic-character methods, and the Hasse bound are prior work. The
candidate new contribution is the two-edge switching construction that yields
a proper ordered family for every odd prime power in the stated range. This
priority statement remains qualified pending broader public and expert review.

The general Youden deletion--exchange interface and proper examples obtained
from it are also prior work. The released $q=11$ array has a compatible
Youden completion. The retained candidate increment is therefore the uniform
Paley parameterization, its two-edge switch and character constraints, and
the all-$q$ existence proof, not the abstract switch or Youden interface.

## Reproduction

The verification programs use Python 3.11 or newer and only the standard
library. From the verification directory, run:

```powershell
python -X utf8 run_reproduction.py
```

The expected final status is
`PASS_PUBLIC_REPRODUCTION_EXTERNAL_REVIEW_PENDING`. A successful run reproduces
the distributed exact calculations, including an independent check of the
frozen $q=11$ Youden completion and deletion roundtrip; it does not replace
independent review of the mathematical proof or the priority claim.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively as an
AI-assisted research, verification, and writing tool and is not an author. The
paper contains the complete disclosure and responsibility statement.

## Keywords

Transposed sesqui array; proper sesqui array; row-column design; combinatorial
design; Paley design; finite field; quadratic character; edge switching;
elliptic curve; Hasse bound; computer-assisted mathematics.
