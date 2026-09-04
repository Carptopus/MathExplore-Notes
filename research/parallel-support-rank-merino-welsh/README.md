# Parallel-support rank and a one-sided Merino--Welsh inequality

This directory contains an internally audited manuscript proving a one-sided Merino--Welsh
inequality for a natural class of finite matroids controlled by their nontrivial parallel classes.

- [Read or download the PDF](parallel-support-rank-merino-welsh.pdf)
- [LaTeX source](parallel-support-rank-merino-welsh.tex)
- [BibTeX citation](CITATION.bib)
- Current version DOI: [10.5281/zenodo.22296382](https://doi.org/10.5281/zenodo.22296382)
- Concept DOI: [10.5281/zenodo.22296381](https://doi.org/10.5281/zenodo.22296381)
- [Verification program](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (4 September 2026)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/parallel-support-rank-merino-welsh)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified public Beta; external mathematical review pending.

## Main result

For a finite loopless, coloopless matroid $M$, let $P(M)$ be the union of its nontrivial parallel
classes. The manuscript proves

$$
r_M(P(M))\ge r(M)-1
\quad\Longrightarrow\quad
T_M(0,2)\ge T_M(1,1).
$$

The inequality is strict when $r_M(P(M))=r(M)-1$. Equality in the full stated class occurs exactly
for direct sums of copies of $U_{1,2}$. The dual statement holds for nontrivial series classes, and
the manuscript gives the corresponding graphic corollary.

The rank threshold is sharp without additional hypotheses: explicit disconnected and connected
counterexamples occur when $r_M(P(M))=r(M)-2$.

## Proof mechanism

The proof first derives an exact basis-activity formula for arbitrary parallel extensions. It then
uses deletion--contraction on singleton parallel classes. In the terminal two-element cocircuit
core, an explicit surplus matching based on $2^K\ge 1+K$ pays for every zero-contribution basis.

The result establishes a sharp sufficient condition for one side of the Merino--Welsh inequality.
It does not resolve the full Merino--Welsh conjecture or the two-disjoint-bases conjecture.

## Reproduction

The checker uses only the Python standard library. From the repository root, run:

```powershell
pwsh -NoProfile -File .\research\parallel-support-rank-merino-welsh\verification\run_all.ps1
```

The runner executes the verifier in ordinary and optimized (`-O`) modes and requires both outputs
to agree with the frozen result. The checks cover the activity formula, all binary simple matroids
of ranks two and three, corank-one strictness, varied multiplicities, three deletion--contraction
interfaces, equality and destructive controls, and two corank-two boundary counterexamples.

These finite checks test the implementation and proof interfaces; they do not replace the general
proof in the manuscript.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof exploration and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Matroid theory; Tutte polynomial; Merino--Welsh inequality; parallel classes; series classes;
deletion--contraction; basis activities; graphic matroids; exact verification; AI-assisted
mathematics.
