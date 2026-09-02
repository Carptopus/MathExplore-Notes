# A complete log-concavity classification for higher-order Stirling cycle rows

## Manuscript

- [Read or download the PDF](higher-order-stirling-cycle-logconcavity.pdf)
- [LaTeX source](higher-order-stirling-cycle-logconcavity.tex)
- [BibTeX citation](CITATION.bib)
- DOI: pending publication deposit
- [Verification programs](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1-beta (2 September 2026)
- Manuscript and documentation license: [CC BY 4.0](LICENSE.md)
- Verification-code license: [MIT](verification/LICENSE-CODE-MIT.txt)
- Status: internally verified candidate proof; external mathematical review pending.

## Main result

Let \([N,k]_{\ge r}\) be the number of permutations of \(N\) elements having exactly
\(k\) cycles, every cycle of length at least \(r\), and set

$$
C_r(n,k)=[n+(r-1)k,k]_{\ge r}.
$$

The manuscript proves that every row \(C_r(n,\cdot)\) is log-concave for every \(n\)
if and only if

$$
1\le r\le5.
$$

The cases \(r=1,2\) were known. The manuscript proves the open layers \(r=3,4,5\)
and shows that every \(r\ge6\) already fails in the row \(n=3\). It also proves, for
every \(r\ge2\), that the normalized rows

$$
\frac{k!\,C_r(n,k)}{(n+(r-1)k)!}
$$

are log-concave.

## Proof and computational boundary

The \(r=3\) proof uses Sagan's inductive criterion. The \(r=4\) proof preserves a
weighted log-concavity cone after factorial normalization. The \(r=5\) proof combines
two exact parameter wedges, an exhaustive finite prefix of 5,754,989 inequalities, and
an effective fifth-order Fourier--Edgeworth estimate for the remaining infinite band.

The supplied programs reproduce the symbolic identities, exact rational certificates,
analytic constants, and finite-prefix computation. The finite computation is one part of
the proof and is not presented as a substitute for the analytic reduction.

## Scope and prior-work boundary

Deb and Sokal proved the \(r=2\) layer and explicitly left \(r=3,4,5\) as open cases.
The manuscript does not claim real-rootedness, total positivity, or Hankel-total positivity
for these rows, nor does it address other parts of their conjecture. The novelty review is
bounded by publicly accessible sources through 2 September 2026.

## Reproduction

Requirements: PowerShell 7, Python 3.13 or compatible, and SymPy 1.14.0. From the
repository root run:

~~~powershell
pwsh -NoProfile -File .\research\higher-order-stirling-cycle-logconcavity\verification\run_all.ps1
~~~

The fifth-order Bernstein certificate is the longest symbolic step and may require about
half an hour. The finite-prefix program visits 5,754,989 points.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used as an AI-assisted tool for
literature organization, proof development and stress testing, exact verification,
adversarial auditing, and manuscript preparation. The manuscript contains the complete
disclosure and responsibility statement.

## Keywords

Associated Stirling numbers; Stirling cycle numbers; log-concavity; recurrence
preservers; Fourier--Edgeworth estimates; computer-assisted proof; exact certificates;
AI-assisted mathematics.
