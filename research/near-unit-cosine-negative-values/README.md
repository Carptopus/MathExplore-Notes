# Uniform polynomial negative values for trigonometric sums with near-unit coefficients

Carptopus · v0.1-beta · First public date: 2026-10-23.

Version DOI: [10.5281/zenodo.23592006](https://doi.org/10.5281/zenodo.23592006).
Concept DOI: [10.5281/zenodo.23592005](https://doi.org/10.5281/zenodo.23592005).
The Zenodo supplement freezes the initial public package; citation/DOI navigation
and byte-preservation attributes were completed subsequently in Git.

[PDF](paper/main.pdf) · [Manuscript](manuscript.md) · [TeX](paper/main.tex) · [Citation](CITATION.bib) · [Checksums](SHA256SUMS)

For arbitrary distinct positive integer frequencies and complex coefficients satisfying
`|c_j - 1| <= 0.021`, the negative minimum of the real trigonometric sum has
a uniform lower bound `c n^(1/12)` for an absolute positive constant `c`.
A correlation argument gives `c n^(1/24)` when `0.99 <= |c_j| <= 1.01`,
with arbitrary independent phases. These are continuous coefficient perturbation results;
they do not settle the full square-root Chowla conjecture or establish optimal exponents.

Shankar's asymmetric-boundary count, Bedert's cubic Fourier framework, and standard
Fourier tools are prior work. The contribution connects directional selection with
low interior leakage. Exact unit-modulus arbitrary-phase bounds already follow from
known unweighted results (with the stronger exponent `1/10`); allowing arbitrary
phases alone is not claimed as new. See the manuscript references and attribution.

Project-internal independent proof and complete-manuscript audits passed, and all
five PDF pages were checked. These are internal checks, not formal peer review;
external mathematical review and global priority confirmation remain pending.
The announced 26 October 2026 Bedert–Sahasrabudhe IAS graph analogue has no precise
weighted theorem available in the checked sources. Its coverage of continuous
coefficients remains UNKNOWN, as disclosed in manuscript reference [BS]. No global-first claim is made.

## Reproduction and files

Python 3.10+ standard library suffices for [finite exact controls](verification/README.md).
From this entry directory run:

```sh
python -B verification/check_correlation_controls.py --output correlation-controls.local.json
```

Compare mathematical fields with `verification/results/correlation-controls.json`;
elapsed time and local paths may differ. Finite controls check identities and constants,
not the universal analytic proof or novelty. `paper/build_tex.py` regenerates TeX from
the hash-gated manuscript; compile `paper/main.tex` with a LaTeX installation providing
the packages in its preamble. `paper/check_pdf.py` requires PyMuPDF and Pillow for
PDF inspection (its historical Windows cache directory must exist or be adjusted).
The supplied PDF and TeX are frozen accepted artifacts.

The manuscript and documentation use CC BY 4.0; executable code uses MIT.
See [licenses](LICENSE.md) and [MIT text](verification/LICENSE-CODE-MIT.txt).
Third-party source PDFs and internal research history are excluded.
Carptopus is the sole human author and assumes authorial responsibility.
Codex assisted research, writing and checks; AI tools are not authors.
