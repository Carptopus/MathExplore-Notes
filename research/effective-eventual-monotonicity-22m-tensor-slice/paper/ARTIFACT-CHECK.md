# Artifact check

Status: **PASS**

This is a conversion, compilation, rendering, and content-fidelity result only.
It is not an independent mathematics or novelty audit, external peer review,
release authorization, or publication operation.

## Frozen input and outputs

- Frozen source: `../manuscript.md`
- Frozen source SHA-256:
  `6C3147DC9B976721C1706B1A380A6EC0D4E12F943CCC762CD28DF2E2D849E260`
- Generated TeX SHA-256:
  `D14C864C044745904B934068BB6D984E366D7859BB29DE1756A5D7838CE3A1BE`
- Final PDF SHA-256:
  `447215DD0050175ECD583EBCD95AF9E0E1C639170C4689F6F53A91CE08F470E8`
- PDF: 9 A4 pages (595.28 by 841.89 points)
- Compiler: bundled Tectonic `0.17.0+20260731`, invoked through the
  `latex-compile` 0.2.7 `compile_latex.py` entry point
- Rendering/check environment: project `.venv`, PyMuPDF 1.28.2 and Pillow
  12.3.0

Carptopus is the sole author. The PDF states only that the internal proof
audit passed and that external peer review has not been completed. It also
contains the required AI-assisted research and writing disclosure, names
Codex as an assisting tool, and explicitly states that Codex is not an author
or responsible author.

## Reproduction commands

Run from `D:\Codes\MyProjects\MathExplore` in PowerShell:

```powershell
& '.venv/Scripts/python.exe' -X utf8 'research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/build_tex.py'
$env:SOURCE_DATE_EPOCH='1791936000'
$env:FORCE_SOURCE_DATE='1'
& '.venv/Scripts/python.exe' -X utf8 'E:/Documents/Codex/codex-home/plugins/cache/openai-bundled/latex/0.2.7/scripts/compile_latex.py' 'D:/Codes/MyProjects/MathExplore/research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/main.tex' --output-directory 'D:/Codes/MyProjects/MathExplore/research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/build' --json
Copy-Item -LiteralPath 'research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/build/main.pdf' -Destination 'research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/main.pdf' -Force
& '.venv/Scripts/python.exe' -X utf8 'research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/check_artifacts.py'
```

The successful compile returned exit code 0 and produced all intermediate
build output under `paper/build/`. No tool or package was installed.

## Conversion and content-fidelity checks

- The source hash gate matched before each TeX generation.
- All 52 display-math bodies and 98 inline-math expressions were retained in
  source order. All 42 explicit equation tags, from (2.1) through (6.3), were
  inventoried in order.
- The exact statement sequence was retained: Theorem 1.1, Proposition 2.1,
  Theorem 2.2, and Lemma 4.1. Both explicit proof headings and their terminal
  squares were retained; Section 6 remains the proof of the main theorem.
- The section/subsection hierarchy, all six reference entries, all URLs, and
  the numbered three-item certificate list were retained. No Markdown heading,
  fence, URL-angle-bracket, or inline-code marker leaked into `main.tex`.
- The frozen source places `\tag{4.4}` and `\tag{5.9}` inside `aligned`, which
  amsmath rejects. The converter mechanically moves only those two tags to the
  end of their corresponding `aligned` display in TeX. Formula bodies,
  symbols, thresholds, and claims are unchanged; the frozen Markdown was not
  modified.
- Extracted PDF text was checked for the title, Carptopus, status, Theorems
  1.1 and 2.2, the `3 x 10^103 + 3` and `3 x 10^103` thresholds, the explicit
  smaller-range limitation, all references, and the AI disclosure. PDF text
  uses ordinary extraction conventions for superscripts and ligatures.
- The PDF contains all six reference URI links, the author email link, and six
  working named-destination links from in-text citations to the bibliography.
  Link structure was checked locally; network reachability was not tested.

## Full-page rendering and visual review

Every page was rendered at 1.8x (1072 by 1516 pixels) with PyMuPDF, verified
as a readable PNG with Pillow, and then individually viewed at original render
resolution. There are no unviewed pages.

- Page 1: title, author/email, date, audit-status box, abstract threshold, and
  Introduction checked; no clipping or title collision.
- Page 2: Theorem 1.1 threshold/conclusion and smaller-range limitation,
  Section 2, Proposition 2.1, and equations (2.1)--(2.4) checked.
- Page 3: proof continuation, equations (2.5)--(2.9), Theorem 2.2, and the
  opening of Section 3 checked.
- Page 4: equations (3.3)--(4.4), including the long polynomial and relocated
  (4.4) tag, checked for complete symbols and right-margin clearance.
- Page 5: Lemma 4.1, equations (4.5)--(4.7), proof close, Section 5, and
  equations (5.1)--(5.3) checked. The long `H(t)` display is intact.
- Page 6: low-frequency bounds (5.4)--(5.11), including the long (5.6)
  display and relocated (5.9) tag, checked.
- Page 7: equations (5.12)--(6.1), subsection transition, and Section 6 heading
  checked; no orphan heading or broken display.
- Page 8: inequalities (6.2)--(6.3), terminal proof square, all three
  certificate items, and the full `1 <= r < 3 x 10^103` limitation checked.
- Page 9: author-responsibility/AI disclosure and all six bibliography entries
  and URLs checked. The remaining lower-page whitespace is normal final-page
  space, not an empty page.

Automated geometry checks found no text block outside any page media box, no
blank page, no Unicode replacement character, and no missing page number.
All 24 used font programs are embedded. Visual inspection found no cropping,
formula overflow, mojibake, missing glyph, formula break, or isolated title.

## Reproducibility and warnings

Two consecutive converter runs produced the same TeX SHA-256. Two consecutive
0.2.7 compile-script runs with `SOURCE_DATE_EPOCH=1791936000` and
`FORCE_SOURCE_DATE=1` produced the same PDF SHA-256. Thus both the TeX and the
current PDF build were reproducible in this environment.

The compiler emitted a benign Fontconfig default-configuration notice and an
`inputenc`-ignored warning under the UTF-8 XeTeX engine. The first pass also
requested a normal rerun for PDF outlines; Tectonic reran automatically. The
successful final pass contained no TeX error, overfull/underfull box warning,
missing-glyph warning, or unresolved-reference warning.

## Machine evidence and file hashes

Detailed page bounds, render hashes, link inventory, embedded-font data, and
text checks are in `artifact-check.json`; extracted text and page PNGs are in
`paper/build/`.

- `build_tex.py`:
  `AF06FA6E7BAAAB3EDB8C2DF04644B59C0987EC6EDD4BDFC55640C2F612769A56`
- `check_artifacts.py`:
  `7B6C0F6F2EB81499F6A48CB2494CD2451EDC55C94BBB51F2C21F6F22D7724BAC`
- `README.md`:
  `DA2A8E263F38D62E29C63E6597F9537F36DCD2F6F1006933F040D454BDE2F1D3`
- `artifact-check.json`:
  `532A1CD340BA98AB48E5B6999E2FCFE369C4912FA25AAEA4F2FF68244F5C4831`

## Remaining boundary

No issue remains within the requested artifact-build scope. The build did not
rerun or reinterpret the mathematical verification package, audit proof
correctness or novelty, test external URL availability, commit to Git, upload,
publish, or alter project research state. PASS means only that this frozen
manuscript was faithfully converted, compiled, and mechanically/visually
checked as described above.
