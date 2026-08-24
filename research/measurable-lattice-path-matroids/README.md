# Minorizing measures and truncations of measurable lattice-path matroids

## Manuscript

- [Read or download the PDF](measurable-lattice-path-matroids.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22079095](https://doi.org/10.5281/zenodo.22079095)
- [LaTeX source](measurable-lattice-path-matroids.tex)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (24 August 2026)
- License: [CC BY 4.0](LICENSE.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let a measurable lattice-path matroid be specified by a closed set
$K\subseteq[0,1]$ and lower and upper cumulative paths $a\leq b$. The
manuscript determines both of its minorizing-measure relaxations exactly.

The basic minorizing measures are precisely the weak-star compact path corridor

$$
\mathsf{bmm}(M_K(a,b))
=\{f\lambda:0\leq f\leq1,\ F_f(1)=R,\ a(t)\leq F_f(t)\leq b(t)\ (t\in K)\}.
$$

All minorizing measures are precisely the interval relaxation

$$
\mathsf{mm}(M_K(a,b))
=\{f\lambda:0\leq f\leq1,\ F_f(t)-F_f(s)\leq b(t)-a(s)\ (s\leq t,\ s,t\in K)\}.
$$

Consequently, every real truncation is obtained by intersecting the interval
relaxation with one total-mass equation. For the full-rank basic corridor, the
paper also gives the exact contact-set criterion for extreme points and proves
that every such extreme point is weak-star exposed.

## Scope and prior-work boundary

Finite lattice-path and positroid polytopes provide the finite-dimensional
analogue. General measurable-matroid foundations, weak-star density, and
classical continuous-control purification results are treated as prior tools.
The candidate contribution is the exact atomless corridor and interval
descriptions for arbitrary closed time sets, together with all real truncation
slices and the contact-set exposed-point theorem.

No directly covering public theorem was found in the bounded literature search
completed on 24 August 2026. Absolute priority remains qualified pending wider
public and expert review.

## AI-assisted research disclosure

Carptopus is the author and bears full responsibility for the manuscript.
OpenAI Codex was used as an AI-assisted research, verification, and writing
tool. The paper contains the complete disclosure.

## Keywords

Measurable matroid; lattice-path matroid; minorizing measure; basic minorizing
measure; weak-star topology; interval relaxation; real truncation; extreme
point; exposed point; continuous linear programming; purification.
