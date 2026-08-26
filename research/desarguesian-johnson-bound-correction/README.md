# On a claimed upper bound for partial Desarguesian parallelisms

## Manuscript

- [Read or download the PDF](desarguesian-johnson-bound-correction.pdf)
- [LaTeX source](desarguesian-johnson-bound-correction.tex)
- [BibTeX citation](CITATION.bib)
- DOI: pending Zenodo publication
- [Verification code and certificate](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (26 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Certificate-data dedication: [CC0 1.0](verification/LICENSE-DATA-CC0.md)
- Status: internally verified correction note; external mathematical review pending.

## Main result

Let $D(n,t,q)$ denote the largest number of pairwise disjoint Desarguesian
$t$-spreads in $V(n,q)$. For every prime power $q$, odd prime $t\geq3$, and
$z\geq2$, with $n=zt$, the note proves

$$
D(n,t,q)>
\frac{q^t-1}{q^n-1}
\left[\begin{matrix}n-1\\t-1\end{matrix}\right]_q
>
\frac{q^{n-1}-1}{q^{t-1}-1}.
$$

The first strict inequality is the Zhang--Zhou orbit lower bound; the second
is an elementary uniform comparison. Their combination contradicts the upper
bound claimed in Johnson's 2010 paper and repeated in the corresponding book
chapter throughout the nontrivial odd-prime parameter range.

## Scope and prior-work boundary

Earlier work on $PG(5,2)$ already implies a complete finite counterexample of
size $155>10$, so this note does not claim the first counterexample. Johnson's
book also records the relevant common-subplane disjointness issue as
unresolved, so the note does not claim the first identification of that proof
obligation. The retained contribution is the uniform all-parameter
comparison, a definition-compatibility argument, an explanation of why the
unsupported step is fatal, and a compact independently checkable witness.

The note does not propose a best corrected replacement for the failed bound,
and no claim of external expert confirmation, peer review, or absolute global
priority is made.

## Reproduction

The checker uses only the Python standard library. From this directory, run:

```powershell
python -X utf8 verification\check_desarguesian_certificate.py
```

It reconstructs 18 pairwise disjoint $GL(6,2)$-images of a Desarguesian
$3$-spread, proving the finite witness $D(6,3,2)\geq18>10$. It also runs a
singular-map negative control and a duplicate-spread negative control. The
general theorem is a symbolic comparison and does not depend on enumeration.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
tool for literature triage, symbolic checks, proof stress-testing,
verification-code review, and manuscript preparation. The paper contains the
complete disclosure and responsibility statement.

## Keywords

Desarguesian spread; partial parallelism; finite geometry; field reduction;
Cayley graph; Gaussian binomial coefficient; translation net; correction
note; computer-assisted mathematics.
