# Paper artifact build

This directory contains a deterministic TeX conversion of the frozen
`../manuscript.md` and its compiled PDF. Carptopus is the sole author. The
artifact includes an accurate AI-assisted research and writing disclosure.
Artifact generation does not constitute mathematical review or publication.

The converter refuses to run unless the frozen source has SHA-256
`6C3147DC9B976721C1706B1A380A6EC0D4E12F943CCC762CD28DF2E2D849E260`.

From the repository root in PowerShell:

```powershell
& '.venv/Scripts/python.exe' -X utf8 'research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/build_tex.py'
& '.venv/Scripts/python.exe' -X utf8 'E:/Documents/Codex/codex-home/plugins/cache/openai-bundled/latex/0.2.7/scripts/compile_latex.py' 'D:/Codes/MyProjects/MathExplore/research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/main.tex' --output-directory 'D:/Codes/MyProjects/MathExplore/research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/build' --json
Copy-Item -LiteralPath 'research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/build/main.pdf' -Destination 'research/Effective-Eventual-Monotonicity-Tensor-Approximation/paper/main.pdf' -Force
```

The build directory is intentionally confined to `paper/build/`. See
`ARTIFACT-CHECK.md` for the exact compiler result, hashes, full-page rendering
inspection, text/link/font checks, and reproducibility scope of the current
artifact.
