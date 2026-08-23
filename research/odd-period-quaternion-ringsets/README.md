# Periodic two-letter ringsets in the Lipschitz quaternions: the general odd-period classification

## Manuscript

- [Read or download the PDF](odd-period-quaternion-ringsets.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: pending Zenodo publication
- [LaTeX source](odd-period-quaternion-ringsets.tex)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (24 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let $\mathbf L=\mathbb Z[\mathbf i,\mathbf j,\mathbf k]$ be the ring of
Lipschitz quaternions. Given an arbitrary prescribed odd period $m$ and a
periodic word $w:\mathbb Z\to\{\mathbf i,\mathbf j\}$, define

$$
S_w=\{a+w(a):a\in\mathbb Z\}\subset\mathbf L.
$$

The manuscript proves that $S_w$ is a ringset if and only if $w$ is
nonconstant and, for every prime $p\mid m$ with $p\equiv3\pmod4$, every
position class modulo $p^{v_p(m)}$ contains both letters.

This is a strict generalization of the preceding
[odd-squarefree-period classification](https://doi.org/10.5281/zenodo.22069614),
which is recovered when every $v_p(m)=1$.

## New mechanism

The new necessity argument treats repeated prime factors. If a highest
$p$-power position class is monochromatic, it constructs an explicit central
fixed-divisor polynomial that vanishes on the entire periodic image modulo a
higher power of $p$, while coefficientwise right multiplication by the other
quaternion letter fails at a selected point. Split prime powers, paired
fibres, periodic congruence orbits, and the Chinese remainder theorem close
the sufficiency direction.

The theorem is symbolic. Finite calculations were used only to discover and
calibrate the prime-power boundary; the general conclusion does not depend on
a finite search or software certificate.

## Scope and prior-work boundary

The residue-null-ideal criterion, finite quaternion ringset theory,
fixed-divisor methods, split and paired-fibre mechanisms, and the complete
odd-squarefree-period theorem are prior work. The candidate contribution is
the removal of squarefreeness, the exact highest-prime-power condition, and
the explicit higher-prime-power obstruction.

No directly covering public theorem was found in the literature search
completed on 23 August 2026. Absolute priority remains qualified pending
broader public and expert review.

## AI-assisted research disclosure

Carptopus is the author and bears full responsibility for the manuscript.
OpenAI Codex was used as an AI-assisted research, verification, and writing
tool. The paper contains the complete disclosure.

## Keywords

Integer-valued polynomial; Lipschitz quaternion; noncommutative algebra;
ringset; null ideal; periodic word; prime power; fixed divisor; local-global
principle; Chinese remainder theorem.
