# Acyclic component hypotheses for total cut complexes of disconnected graphs

## Manuscript

- [Read or download the PDF](total-cut-low-components.pdf)
- [BibTeX citation](CITATION.bib)
- Concept DOI: [10.5281/zenodo.22045539](https://doi.org/10.5281/zenodo.22045539)
- Previous v0.2-beta: [10.5281/zenodo.22059068](https://doi.org/10.5281/zenodo.22059068)
- [LaTeX source](total-cut-low-components.tex)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.3-beta (28 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Let $G=G_1\sqcup\cdots\sqcup G_k$ be a finite simple graph with $k$ nonempty
connected components and $n$ vertices. For $d\geq2$, let $\Delta_d^t(G)$ be
the total $d$-cut complex. If $k\geq d$ and, for every component $G_i$ and
every $2\leq r\leq d$, the complex $\Delta_r^t(G_i)$ is void or
integer-acyclic, then

$$
\Delta_d^t(G)\simeq
\bigvee_{\binom{k-1}{d-1}} S^{n-d-1}.
$$

The theorem covers the complete component range $k\geq d$. It subsumes the
previous v0.2-beta result for the three low-component layers and answers
Question 30 of Carnero Bravo for the component class stated above by removing
the component clique-complex simple-connectivity condition.

## Proof structure

- An acyclic composition diagram and its homology-colimit spectral sequence
  compute the integral homology in every component range.
- For $k\geq d+1$, direct combinatorial connectivity arguments upgrade the
  homology calculation to the asserted homotopy type.
- For the boundary layer $k=d$, a weak-composition cover has contractible
  nonbaseline blocks and connected intersections; successive van Kampen
  arguments close the fundamental group.
- The graph $C_4\sqcup K_1$ at $d=2$ supplies a negative control showing that
  component acyclicity cannot simply be omitted.

## Scope and prior-work boundary

This version is a successor to *The Low-Component Cases for Total Cut
Complexes of Disconnected Graphs*. It uses the composition-poset and
homotopy-colimit framework of Carnero Bravo, while replacing objectwise
contractibility by integral acyclicity and supplying new connectivity
arguments under the weaker hypotheses.

The paper does not classify arbitrary disconnected graphs, determine the
simple-homotopy type, or remove every component acyclicity hypothesis. The
weakening from contractible to integer-acyclic is formal until a graph-domain
strictness witness is known. Absolute priority remains qualified pending
broader public and expert review.

This is a theoretical proof. Finite computation was used only for exploratory
falsification and is not part of the proof.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted
research, verification, and writing tool. The manuscript contains the full
disclosure and responsibility statement.

## Keywords

Total cut complex; bounded-independence complex; disconnected graph;
simplicial complex; Alexander duality; homotopy colimit; van Kampen theorem;
wedge of spheres; graph complex; algebraic topology.
