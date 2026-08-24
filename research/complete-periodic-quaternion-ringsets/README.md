# Periodic ringsets in the Lipschitz quaternions: the complete six-letter classification

## Manuscript

- [Read or download the PDF](complete-periodic-quaternion-ringsets.pdf)
- [BibTeX citation](CITATION.bib)
- DOI: pending Zenodo publication
- [LaTeX source](complete-periodic-quaternion-ringsets.tex)
- [Verification materials](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (24 August 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Python verification license: [MIT](LICENSE.md)
- JSON result license: [CC0 1.0](LICENSE.md)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let

$$
\mathbf L=\mathbb Z[\mathbf i,\mathbf j,\mathbf k],
\qquad
U=\{\pm\mathbf i,\pm\mathbf j,\pm\mathbf k\},
$$

and let $w:\mathbb Z\to U$ be periodic with an arbitrary prescribed period
$m$. For

$$
S_w=\{a+w(a):a\in\mathbb Z\}\subseteq\mathbf L,
$$

the manuscript gives a complete necessary-and-sufficient criterion for
$S_w$ to be a ringset:

1. $w$ is nonconstant;
2. for every $p\mid m$ with $p=2$ or $p\equiv3\pmod4$, every position class
   modulo $p^{v_p(m)}$ contains at least two letters;
3. for every $p\mid m$ with $p\equiv1\pmod4$, no two position fibres separated
   by a square root of $-1$ are singleton antipodal fibres.

The theorem covers every period and the full six-letter alphabet. It strictly
contains both preceding quaternion-ringset classifications:

- [odd squarefree periods and two letters](https://doi.org/10.5281/zenodo.22069614);
- [arbitrary odd periods and two letters](https://doi.org/10.5281/zenodo.22070532).

## New mechanisms

The even-period boundary is controlled by an explicit ramified Gaussian
fixed-divisor obstruction at $2$. At split primes, a matrix-ring eigenline
analysis isolates the exact failure: two square-root-separated fibres are
singletons carrying opposite quaternion units. These local results combine
with the nonsplit prime-power obstruction and the Chinese remainder theorem
to give the global classification.

The proof is symbolic. The supplied programs only calibrate the $2$-adic
valuation formula, the 36 split eigenline pairs, and sample split-prime
obstructions; they do not replace the general proof.

## Scope and prior-work boundary

Finite quaternion ringset theory, null-ideal criteria, split matrix models,
fixed-divisor estimates, and the two preceding periodic classifications are
treated as prior tools. The candidate contribution is the ramified
$2$-adic obstruction, the exact split-prime antipodal obstruction, and their
assembly into the complete six-letter arbitrary-period classification.

No directly covering public theorem was found in the bounded literature
search completed on 24 August 2026. Absolute priority remains qualified
pending broader public and expert review.

## AI-assisted research disclosure

Carptopus is the author and bears full responsibility for the manuscript.
OpenAI Codex was used as an AI-assisted research, verification, and writing
tool. The paper contains the complete disclosure.

## Keywords

Integer-valued polynomial; Lipschitz quaternion; noncommutative algebra;
ringset; null ideal; periodic word; ramified prime; split prime; fixed divisor;
matrix ring; local-global principle; Chinese remainder theorem.
