# An unbounded gap between minimum degree and the minor-connectivity ceiling

This directory contains a manuscript proving an exact minor-connectivity ceiling for every
independent blow-up of the 12-vertex Mader graph.

- [Read or download the PDF](unbounded-minor-connectivity-gap.pdf)
- [LaTeX source](unbounded-minor-connectivity-gap.tex)
- [BibTeX citation](CITATION.bib)
- [Verification package](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Public version: v0.1-beta (3 September 2026)
- DOI: [10.5281/zenodo.22281553](https://doi.org/10.5281/zenodo.22281553)
- Concept DOI: [10.5281/zenodo.22281552](https://doi.org/10.5281/zenodo.22281552)
- Public repository: [MathExplore-Notes](https://github.com/Carptopus/MathExplore-Notes/tree/master/research/unbounded-minor-connectivity-gap)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)

## Main result

Let $M_{12}$ be Mader's 12-vertex graph and let $M_{12}[\overline K_t]$ denote its independent
$t$-fold blow-up. For every integer $t\ge2$, the manuscript proves

$$
\kappa^*(M_{12}[\overline K_t])=\left\lfloor\frac{9t}{2}\right\rfloor,
\qquad
\delta(M_{12}[\overline K_t])=5t.
$$

Consequently,

$$
\delta(M_{12}[\overline K_t])-\kappa^*(M_{12}[\overline K_t])
=\left\lceil\frac t2\right\rceil,
$$

so the gap between minimum degree and the largest connectivity of a minor is unbounded. The family
also gives infinitely many counterexamples to Barát's conjectured bound
$\kappa^*(G)\ge\delta(G)-1$.

The lower bound comes from an explicit uniform minor model. The upper bound localizes every
hypothetical highly connected minor to a torso, classifies its three branch-set quotient factors,
and closes the remaining cases by an anticomplete-shores formula.

Status: internally verified public Beta v0.1. The complete proof and manuscript have passed
zero-trust audits, and the PDF and bounded verification package have passed artifact checks.
External mathematical review remains pending.

## Reproduction

The finite checker requires Python 3 and NetworkX 3.6.1. From PowerShell:

```powershell
cd verification
.\run_all.ps1 -Python python
```

The runner executes two destructive controls, reconstructs the explicit models for
$t=2,\ldots,8$, compares the structural connectivity calculation with NetworkX, and requires exact
agreement with the frozen output. These bounded checks validate the construction and its
implementation; the universal upper bound is proved theoretically.

## Scope

The theorem concerns independent blow-ups of the specific graph $M_{12}$. It disproves the proposed
universal additive-one bound by an unbounded family, but it does not classify $\kappa^*(G)$ for
arbitrary graphs. No claim of absolute priority over unindexed work is made.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure.
