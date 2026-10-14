# Effective eventual monotonicity on the `(2,2,m)` tensor slice

Author: Carptopus · Version 0.1-beta · 14 October 2026

Published preprint: [Version DOI](https://doi.org/10.5281/zenodo.23353313) · [Concept DOI](https://doi.org/10.5281/zenodo.23353312). The Zenodo archive preserves the first fixed public package at Git commit `12ba9e48fd64e6721588b4db4f1972b8af118674`; this repository additionally backfills the DOI in the README and BibTeX without changing the accepted manuscript, TeX, PDF, verification sources or analytic supplements.

- [Manuscript](manuscript.md)
- [PDF](paper/main.pdf) · [LaTeX source](paper/main.tex) · [BibTeX](CITATION.bib)
- [Verification instructions](verification/README.md) · [Analytic supplements](supplement/)
- [Artifact checks](paper/ARTIFACT-CHECK.md) · [Build instructions](paper/README.md) · [File hashes](SHA256SUMS.txt)

## Result and boundary

In the normalization of Draisma and Horobeţ, the manuscript proves

$$
a(2,2,m)<a(2,2,m-1)
\qquad\text{for every integer }m\ge 3\times10^{103}+3.
$$

This is an effective tail result for the `(2,2,m)` slice of Draisma--Horobeţ Conjecture 1.3. It does not resolve the full conjecture, the comparison at `m=4`, the `r=1` case, or the enormous finite prefix `1 <= r < 3*10^103`. No global-first claim is made.

The proof specializes the Kac--Rice representation to a normalized random walk in `2 x 2` symmetric matrices and combines an exact moment-generating function, a weighted Edgeworth expansion, certified positivity of its first even correction, and explicit Fourier remainder bounds. The supplied Python programs check symbolic identities, interval inequalities and explicit constants. Fixed-seed numerical samples are controls only; finite computation is not used as a substitute for the general analytic proof.

## Review status

This is a **Public Beta** preprint. The writing-preparation proof audit passed with confidence 0.96, bounded novelty review returned `PASS_BOUNDED`, and the final-manuscript review passed with confidence 0.97. These are internal project reviews, not external validation. The source-to-TeX conversion, reproducible PDF build and full-page artifact inspection passed separately. External mathematical review and formal peer review have not been completed.

Codex assisted with research, literature comparison, verification and writing. Carptopus is the sole author and bears sole responsibility for the content. Codex is not an author or responsible author.

Manuscript, documentation and analytic supplements: [CC BY 4.0](LICENSE.md). Verification code: [MIT](verification/LICENSE-CODE-MIT.txt).

Keywords: mathematics; tensor approximation; critical rank-one approximation; random matrices; Edgeworth expansion; effective asymptotics; Kac--Rice; computer-assisted proof; AI-assisted mathematics.
