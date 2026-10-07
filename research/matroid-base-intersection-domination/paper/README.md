# Building the paper

`main.tex` is a standalone source; compile it with a LaTeX engine supporting the listed standard packages. The accepted PDF is `main.pdf`. The manuscript and the explicit inline-notation map are hash-pinned by `build_tex.py`.

From this directory, using Python 3.10 or newer:

```powershell
<path-to-python.exe> -B -X utf8 build_tex.py --check-only
```

Without `--check-only`, the converter regenerates `main.tex` and conversion evidence. It does not edit the manuscript, infer new mathematical notation, compile the PDF, or certify mathematical correctness. Keep `manuscript.md` in the parent directory and `inline-notation.json` next to the converter.

Example with an already available Tectonic executable:

```powershell
<path-to-tectonic.exe> --keep-logs --keep-intermediates main.tex
```

Optional PDF extraction and full-page rendering use PyMuPDF and Pillow:

```powershell
<path-to-python.exe> -B -X utf8 check_pdf.py
```

The check writes a machine report in this directory and rendered pages under the checkout's `tmp/kneser-unified-artifacts/`. Rendered pages must be visually inspected; running the script alone does not certify a new PDF. See `ARTIFACT-CHECK.md` for the accepted frozen version, exact checks and remaining limitations. Rebuilding with a different compiler may change PDF bytes; byte-identical TeX reproduction is checked, not universal PDF-byte reproducibility.

These build/check scripts fall under the code MIT license in `../verification/LICENSE-CODE-MIT.txt`; manuscript and artifact documentation use CC BY 4.0.
