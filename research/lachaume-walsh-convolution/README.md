# A Walsh-convolution proof of two conjectures of Lachaume

This directory contains an internally audited short manuscript identifying Lachaume's derivative
sum with a rescaled Walsh symmetric additive convolution. The classical Walsh root-location
theorem then settles Lachaume's Conjectures 4 and 5 in every degree.

- [PDF manuscript](lachaume-walsh-convolution.pdf)
- [LaTeX source](lachaume-walsh-convolution.tex)
- [BibTeX citation](CITATION.bib)
- [Verification program](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Public version: v0.1-beta (4 September 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified public Beta; external mathematical review pending.

## Main result

For complex polynomials `P,Q` of degree at most `p`, define

$$
\mathcal D_p(P,Q)(x)=\sum_{k=0}^{p}P^{(k)}(x)Q^{(p-k)}(x).
$$

The manuscript proves the exact identity

$$
\mathcal D_p(P,Q)(x)=p!\,(P\boxplus_pQ)(2x),
$$

where `boxplus_p` is the classical Walsh symmetric additive convolution. Consequently, when `P`
and `Q` have degree `p`, every zero of the derivative sum belongs to the convex hull of all input
zeros; in particular, real-rooted inputs produce a real-rooted output. Through Lachaume's stated
equivalences, this proves Conjectures 4 and 5 and the corresponding semi-symmetric hyperbolicity
statement.

## Prior-work boundary

The Walsh convolution and its root-location theorem are classical. Lachaume's 2018
Lovelock-gravity paper already invokes Walsh's theorem for the related implication from a
real-rooted diagonal restriction to concavity. The candidate contribution here is limited to the
explicit derivative-convolution identity with its exact scaling, its application to Conjectures 4
and 5, and the complex convex-hull deduction. It does not claim Lachaume's Conjectures 1 or 3.

## Reproduction

The verifier requires Python 3 and SymPy 1.14. From the repository root, run:

```powershell
pwsh -NoProfile -File .\research\lachaume-walsh-convolution\verification\run_all.ps1
```

The manuscript PDF is built from `lachaume-walsh-convolution.tex` with Tectonic and the frozen
source-date epoch:

```powershell
$env:SOURCE_DATE_EPOCH = '1788480000'
tectonic .\research\lachaume-walsh-convolution\lachaume-walsh-convolution.tex
```

The runner executes the verifier in ordinary and optimized (`-O`) modes and requires both outputs
to match the frozen result. The symbolic checks cover generic degrees 1 through 8, a telescoping
certificate, an apolar identity, and a destructive control. They supplement rather than replace
the general proof.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for literature
organization, proof development and stress testing, exact verification, adversarial auditing, and
manuscript preparation. The manuscript contains the complete disclosure and responsibility
statement.

## Keywords

Walsh convolution; symmetric additive convolution; real-rooted polynomials; root location;
hyperbolic polynomials; semi-symmetric polynomials; polynomial convolutions; reproducible
mathematics; AI-assisted mathematics.
