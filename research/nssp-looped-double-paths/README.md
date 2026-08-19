# Spectral separation and the nSSP for looped double paths

## Manuscript

- [Read or download the PDF](nssp-looped-double-paths.pdf)
- [LaTeX source](nssp-looped-double-paths.tex)
- [Verification code](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (19 August 2026)
- Manuscript and documentation license: [Creative Commons Attribution 4.0 International](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; public mathematical review pending.

## Main result

Let $P_{n,L}$ be the double path on $[n]$, with a loop precisely at the
vertices in $L$. The manuscript proves the classification

$$
P_{n,L}\text{ allows the nSSP}
\quad\Longleftrightarrow\quad
L\ne\varnothing\text{ and }(n\text{ is even or }L\text{ contains an odd vertex}).
$$

The structural core is an exact spectral criterion for a real symmetric
irreducible tridiagonal matrix with one nonzero diagonal entry: it has the
non-symmetric strong spectral property exactly when the two zero-diagonal
Jacobi arms obtained by deleting the looped vertex have disjoint spectra.

## Proof outline

- A simple-spectrum centralizer reduction converts nSSP into a Jacobian condition.
- Parity separation and rooted continuants recover the left and right arms when their spectra are disjoint.
- A shared arm eigenvalue gives an explicit commuting spectral-projector obstruction.
- Rationally scaling one arm avoids every nonzero spectral collision unless parity forces a common zero.
- The Superpattern Lemma and the known odd-order obstruction complete the classification for arbitrary loop sets.

## Scope of the claim

The general nSSP/Jacobian bridge, Jacobi inverse-spectral methods, the
Superpattern Lemma, and several previously known loop assignments are prior
work. The candidate contribution is the single-loop spectral-separation
criterion together with the resulting complete allow/not-allow classification.
The global priority statement remains qualified pending broader public and
expert review.

## Reproduction

The three verification programs use Python 3.11 or newer and only the standard
library. From this entry directory, run:

```powershell
python -X utf8 verification/verify_nssp_weighted_paths.py --max-n 32
python -X utf8 verification/verify_nssp_spectral_separation.py
python -X utf8 verification/audit_nssp_spectral_jacobian.py
```

The expected summaries report 272 weighted single-loop positions, 119
spectral-separation cases, and 77 Jacobian/projector cases. These computations
calibrate the proof and expose boundary errors; they do not replace the general
mathematical argument or independent review.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively as an
AI-assisted research, verification, and writing tool and is not an author. The
paper contains the complete disclosure and responsibility statement.

## Keywords

Non-symmetric strong spectral property; nSSP; inverse eigenvalue problem;
graph pattern; looped double path; Jacobi matrix; tridiagonal matrix; spectral
separation; inverse spectral theory; computer-assisted mathematics.
