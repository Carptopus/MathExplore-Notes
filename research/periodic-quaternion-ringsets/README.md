# Periodic infinite ringsets in the Lipschitz quaternions

## Manuscript

- [Read or download the PDF](periodic-quaternion-ringsets.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22069614](https://doi.org/10.5281/zenodo.22069614)
- [LaTeX source](periodic-quaternion-ringsets.tex)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (23 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let $\mathbf L=\mathbb Z[\mathbf i,\mathbf j,\mathbf k]$ be the ring of
Lipschitz quaternions. Given a prescribed odd squarefree period $m$ and a
periodic word $w:\mathbb Z\to\{\mathbf i,\mathbf j\}$, define

$$
S_w=\{a+w(a):a\in\mathbb Z\}\subset\mathbf L.
$$

The manuscript proves that $S_w$ is a ringset if and only if $w$ is
nonconstant and, for every prime $p\mid m$ with $p\equiv3\pmod4$, the
restriction of $w$ to every residue class modulo $p$ is nonconstant.
Consequently, when every prime divisor of $m$ is congruent to $1$ modulo $4$,
every nonconstant binary word of period $m$ produces an infinite ringset.

## Proof structure

- At split prime powers, rank-one idempotents in
  $\mathbf L/p^e\mathbf L\cong M_2(\mathbb Z/p^e\mathbb Z)$ force the relevant
  residue image to be core.
- At primes congruent to $3$ modulo $4$, a Frobenius real-part extractor gives
  an explicit obstruction whenever a residue fibre contains only one letter.
- Periodic congruence orbits translate the local conditions into conditions on
  the word, and the Chinese remainder theorem closes the local-global step.

## Scope and prior-work boundary

The residue-null-ideal criterion, finite quaternion ringset theory, finite
core-set classifications, and the previously known sufficient congruence
pairing mechanism are prior work. The candidate contribution is the exact
local-global criterion above for this prescribed-period infinite binary
family, together with the split-prime-power and obstruction arguments needed
for necessity and sufficiency. No directly covering public theorem was found
in the literature search completed on 23 August 2026; absolute priority
remains qualified pending broader public and expert review.

Finite calculations were used only for exploration and boundary calibration.
The theorem is established by the written proof and does not depend on a
finite search or software certificate.

## AI-assisted research disclosure

Carptopus is the author and bears full responsibility for the manuscript.
OpenAI Codex was used as an AI-assisted research, verification, and writing
tool. The paper contains the complete disclosure.

## Keywords

Integer-valued polynomial; Lipschitz quaternion; noncommutative algebra;
ringset; null ideal; periodic word; local-global principle; matrix ring;
Chinese remainder theorem.
