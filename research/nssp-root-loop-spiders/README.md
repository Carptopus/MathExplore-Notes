# An exact nSSP criterion for root-loop spider matrices

## Manuscript

- [Read or download the PDF](nssp-root-loop-spiders.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22045528](https://doi.org/10.5281/zenodo.22045528)
- [LaTeX source](nssp-root-loop-spiders.tex)
- [Verification code](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (19 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- SHA-256 checksum-manifest license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let $T=S(\ell_1,\ldots,\ell_m)$ be a spider with $m\geq3$ arms. Consider a
real matrix $A$ whose nonzero off-diagonal positions are exactly both directed
entries on every edge of $T$. Its root diagonal entry is nonzero and every
other diagonal entry is zero. If $B_j$ is the arm matrix obtained by deleting
the root and

$$
P_j(x)=\det(xI-B_j),
$$

then the manuscript proves

$$
A\text{ has the nSSP}
\quad\Longleftrightarrow\quad
P_1,\ldots,P_m\text{ are pairwise coprime in }\mathbb R[x].
$$

Equivalently, $A$ fails the non-symmetric strong spectral property exactly
when two distinct arms share an eigenvalue over $\mathbb C$.

## Proof outline

- Diagonal similarity reduces the directed parameters to two-way edge products.
- A cyclic-root argument proves that pairwise-coprime arm polynomials make the full matrix nonderogatory.
- Parity separation and rooted continuant identities make the reduced characteristic-coefficient Jacobian injective.
- A common nonzero arm root gives an explicit real centralizer witness, including the nonreal-root case.
- A common zero root is handled separately through alternating zero modes on odd arms.

The result permits arbitrary non-symmetric real weights, negative edge
products, repeated roots within one arm, and nonreal shared-root witnesses.

## Scope of the claim

This is a fixed-matrix criterion, not a pattern-wide allowability
classification. The symmetric two-arm spectral-separation mechanism is already
public in the earlier [looped-double-path Beta](../nssp-looped-double-paths/README.md),
whose classification of arbitrary loop assignments remains an independent
result. The contribution claimed here is the extension to genuinely branching
root-loop spiders with arbitrary non-symmetric real weights.

The general nSSP/transversality framework, the characteristic-coefficient
Jacobian bridge, generalized-star inverse-eigenvalue methods, cyclic-matrix
facts, and continuant recurrences are prior tools. Global priority remains
qualified pending broader public and expert review.

## Reproduction

The verification program uses Python 3.11 or newer and only the standard
library. From this entry directory, run:

```powershell
python -X utf8 verification/verify_directed_spider_criterion.py --max-vertices 11 --samples 10
```

The expected summary reports 585 cases: 145 pairwise-coprime cases with full
modular verification rank, and 440 noncoprime cases with no modular-full-rank
counterexample. Five integrated destructive controls cover a repeated complex
root within one arm, a changed directed splitting with fixed edge products,
and shared nonzero, nonreal, and zero factors.

Modular full rank certifies full rank over the rationals and reals for the
displayed integer matrix. Modular rank loss is only a screen; the three
negative controls are also eliminated exactly over the rationals. These finite
checks calibrate the proof and do not replace its general argument or
independent review.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively as an
AI-assisted research, verification, and writing tool and is not an author. The
paper contains the complete disclosure and responsibility statement.

## Keywords

Non-symmetric strong spectral property; nSSP; inverse eigenvalue problem;
root-loop spider; spider matrix; generalized star; bidirected tree; tridiagonal
matrix; arm spectrum; pairwise coprime characteristic polynomials; spectral
separation; centralizer; Jacobian method; computer-assisted mathematics.
