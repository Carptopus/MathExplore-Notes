# Paper build

`main.tex` is generated from the frozen `../manuscript.md` source. The converter
checks the frozen SHA-256 before writing TeX and performs markup conversion only.

From this directory, with the MathExplore project environment available:

```powershell
& 'D:\Codes\MyProjects\MathExplore\.venv\Scripts\python.exe' .\build_tex.py
& 'D:\Codes\MyProjects\MathExplore\.venv\Scripts\python.exe' `
  'E:\Documents\Codex\codex-home\plugins\cache\openai-bundled\latex\0.2.8\scripts\compile_latex.py' `
  .\main.tex --json
& 'D:\Codes\MyProjects\MathExplore\.venv\Scripts\python.exe' .\audit_pdf.py
```

The accepted build used bundled Tectonic `0.17.0+20260731`. It produced a
19-page A4 PDF. The full-page audit found all 101 equation tags and checked all
106 PDF links, with no missing tag, unresolved reference, invalid link, blank
page, replacement character, out-of-bounds text block or tight page-boundary
contact.

The PDF was additionally inspected through five contact sheets. No cropping,
formula overflow, garbling, broken page number or unreadable text was found.
See [ARTIFACT-CHECK.md](ARTIFACT-CHECK.md) for the accepted hashes and scope.
