# Near-minimal Ehrhart data on the primitive-triangle boundary of denominator-two polygons

## Manuscript

- [Read or download the PDF](ehrhart-denominator2-primitive-boundary.pdf)
- [BibTeX citation](CITATION.bib)
- [LaTeX source](ehrhart-denominator2-primitive-boundary.tex)
- [Verification material](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (22 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let $P\subset\mathbb R^2$ be a convex polygon of denominator two with

$$
b(P)=0,\qquad b(2P)=3,
$$

and set $N=i(P)$ and $I=i(2P)$. The paper proves the necessary congruence

$$
2I+1\equiv4N\pm1\pmod8
$$

and determines the near-minimal boundary as follows:

- for $N\ge4$, the values with $I\le3N-3$ are exactly $2N-1$, $2N$, and,
  when $N\equiv2$ or $3\pmod4$, $3N-3$;
- the small cases are $(N,I)=(2,3),(3,5),(3,6)$ in this region;
- $I=3N-2$ occurs exactly at $(N,I)=(10,28)$;
- an explicit infinite family has $N=4k+5$ and $I=3N-1$, proving that the
  preceding exclusion is one lattice point sharp on an infinite subfamily.

The result is a sharp near-boundary classification, not a classification of
all denominator-two Ehrhart data.

## Proof and evidence

The proof combines parity in primitive lattice triangles, internal-hull
stability, outer-hull geometry for hollow width-one polygons, and a bounded
exhaustive check after a theoretical reduction to $3\le N\le10$. The supplied
programs independently check the parity identities, explicit constructions,
the bounded branch, and destructive controls. The general theorem rests on the
written proof; bounded computation is used only where the manuscript says so.

## Prior-work boundary

Earlier work supplies the denominator-two Ehrhart framework, the known linear
region, primitive-triangle normal forms, parity-color tools, hollow-polygon
classification, Scott bounds, and outer-hull theory. The candidate new
contribution is their synthesis into the stated mod-$8$ obstruction and sharp
near-minimal boundary classification. Absolute priority remains qualified
pending broader public and expert review.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively for
AI-assisted literature search, proof exploration, verification, adversarial
auditing, and manuscript preparation. The paper contains the complete
disclosure and responsibility statement.

## Keywords

Ehrhart theory; rational polygon; half-integral polygon; denominator two;
lattice polygon; primitive lattice triangle; parity; internal hull; outer hull;
lattice width; discrete geometry; computational geometry.
