# Tail-projection certificates for cyclotomic minimum-degree polynomials beyond the reciprocal condition

## Manuscript

- [Read or download the PDF](cyclotomic-tail-projection-families.pdf)
- [LaTeX source](cyclotomic-tail-projection-families.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22127365](https://doi.org/10.5281/zenodo.22127365)
- Concept DOI: [10.5281/zenodo.22127364](https://doi.org/10.5281/zenodo.22127364)
- [Condition checker](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (27 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Let `n=p*q_1*...*q_k` be odd and squarefree, where
`p<q_1<...<q_k` and `k>=3`, and put `P=q_1*...*q_k`. The manuscript gives an
explicit divisor-residue quantity `B_k`. It proves that `B_k<P` implies:

- the minimum degree of a nonzero polynomial in `R_{>=0}[x]` divisible by
  the `n`-th cyclotomic polynomial is `(p-1)P`;
- equality occurs only for positive scalar multiples of the regular `p`-gon
  polynomial `1+x^P+...+x^((p-1)P)`.

For every fixed `k>=3`, the condition holds for all sufficiently large prime
tuples contained in a short multiplicative interval. These tuples fail
Steinberger's earlier reciprocal sufficient condition. The theorem therefore
gives infinitely many new cases for every fixed number of at least four
distinct prime factors.

## Proof mechanism

The proof starts from the Chinese-remainder tensor description of the
cyclotomic coefficient space. It projects an alternating divisor expansion
onto the final interval of `P-1` exponents, proves strict negativity there by
exact residue-class counts, and then applies an explicit zero-marginal anchor
correction that cancels the regular polygon support. The resulting integer
functional separates every lower-degree nonnegative multiple and forces the
equality case.

## Scope and relation to the companion entry

This theorem gives a general sufficient condition and infinite prime families.
It does not prove Steinberger's full conjecture and does not claim that the
condition is necessary. It is complementary to the earlier
[fixed-parameter certificate paper](../cyclotomic-minimum-degree-first-two-cases/README.md),
which proves the first two parameters outside Steinberger's theorem by dense
exact certificates. Neither result subsumes the other.

A targeted search completed on 27 August 2026 found no public paper, preprint,
author update, or indexed computational archive directly covering this
divisor-residue condition or the resulting infinite families. This is the
recorded search boundary, not an absolute worldwide priority claim.

## Reproduction

The checker uses only the Python standard library. From this entry directory:

```powershell
python -X utf8 .\verification\verify_general_tail_condition.py --primes 37 41 43 47 53
```

The example must report `"tail_condition_strict": true`,
`"outside_steinberger_condition": true`, and `"result": "PASS"`.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature discovery, computational exploration, proof organization,
stress testing, verification-code review, adversarial auditing, and manuscript
preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Cyclotomic polynomials; nonnegative coefficients; minimum degree; separation
certificates; Chinese remainder theorem; tensor projections; prime tuples;
infinite families; computer-assisted proof; AI-assisted mathematics.
