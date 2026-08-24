# The face lattice of the irreducible-Ferrers polytope is a product of triangles

## Manuscript

- [Read or download the PDF](ferrers-polytope-triangle-product.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: pending
- [LaTeX source](ferrers-polytope-triangle-product.tex)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (24 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

For every integer $d\geq3$, Beeloo-Sauerbier Couvée and Neri associate an
integral polytope $\mathfrak P_d$ with irreducible Ferrers diagrams. This note
proves their Conjecture 5.28:

$$
\mathfrak P_d\simeq_{\mathrm{comb}}(\Delta_2)^{d-2}.
$$

Thus the complete face lattice is that of a Cartesian product of $d-2$
triangles. In particular, $\mathfrak P_d$ is a simple polytope of dimension
$2(d-2)$ with $3(d-2)$ facets, and its face enumerator is

$$
(3+3t+t^2)^{d-2}.
$$

## Proof boundary

The original paper supplies the nonnegative affine-slice model and proves that
the vertices realize all one-positive-coordinate-per-block support patterns.
The new step is a block-support face-lattice lemma: for such an orthant slice,
every allowed coordinate-zero pattern is realized by a face. This recovers the
whole face lattice from the known vertex supports.

The result is combinatorial equivalence only. It does not assert affine or
unimodular equivalence, and it does not prove the Etzion--Silberstein conjecture
itself. The proof is theoretical and does not depend on finite computation.

## Prior-work and review status

The cited preprint introduced $\mathfrak P_d$, proved integrality, classified
its vertices, and verified the product-of-triangles face vector through
$d=7$. As of the public-source refresh on 24 August 2026, no direct public
proof of Conjecture 5.28 was located. Absolute priority remains qualified
pending broader database coverage and expert review.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively for
AI-assisted literature search, proof exploration, adversarial auditing, and
manuscript preparation. The paper contains the complete disclosure and
responsibility statement.

## Keywords

Ferrers diagram; Ferrers polytope; face lattice; product of triangles;
product of simplices; combinatorial equivalence; rank-metric codes;
Etzion--Silberstein conjecture; polyhedral combinatorics; coding theory.
