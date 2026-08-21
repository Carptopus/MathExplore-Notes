# The low-component cases for total cut complexes of disconnected graphs

## Manuscript

- [Read or download the PDF](total-cut-low-components.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22045540](https://doi.org/10.5281/zenodo.22045540)
- [LaTeX source](total-cut-low-components.tex)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (20 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let $G=G_1\sqcup\cdots\sqcup G_k$ be a graph with $k$ nonempty connected
components and $n$ vertices. For $d\geq2$, let $\Delta_d^t(G)$ be its total
$d$-cut complex. Under the component hypotheses stated in the manuscript, the
paper proves the three previously unresolved cases $k=d,d+1,d+2$ and obtains

$$
\Delta_d^t(G)\simeq
\bigvee_{\binom{k-1}{d-1}} S^{n-d-1}.
$$

Together with the previously known high-component range, this completes the
formula for every $d\geq2$ and $k\geq d$ under the stated hypotheses.

## Proof structure

- For $k=d+2$, a complete one-skeleton and a fixed-component triangular fan
  establish simple connectivity.
- For $k=d+1$, the proof separates the two boundary cases and fills the
  fundamental cycles of a spanning star by explicit triangular disks.
- For $k=d$, a cover by joins indexed by weak compositions isolates the
  all-ones sphere and retracts the remaining union onto its intersection with
  that sphere.
- An independent argument supplies the $d=2$, $k\geq5$ high-component case
  needed for the all-parameter conclusion as stated.

## Scope and prior-work boundary

Carnero Bravo's work establishes the high-component theorem for $d\geq3$ and
asks whether the same homotopy formula holds in the three low-component cases.
The candidate new contribution is the affirmative solution of those three
cases, plus the independent $d=2$ completion needed to state the combined
range uniformly. Definitions, Alexander-duality machinery, and the cited
high-component results remain prior work. Absolute priority remains qualified
pending broader public and expert review.

This is a theoretical proof. No finite computation or software output is used
to establish the theorem.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively as an
AI-assisted research, verification, and writing tool and is not an author. The
paper contains the complete disclosure and responsibility statement.

## Keywords

Total cut complex; bounded-independence complex; disconnected graph;
simplicial complex; Alexander duality; polyhedral join; nerve lemma; wedge of
spheres; graph complex; algebraic topology.
