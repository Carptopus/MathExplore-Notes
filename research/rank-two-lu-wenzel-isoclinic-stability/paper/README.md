# Build instructions

`main.tex` is the accepted source for `main.pdf`. Build it from this directory
with a current TeX Live installation:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The accepted public PDF has 11 pages. Rebuilding may change PDF container bytes
because of toolchain metadata; the hashes in `SHA256SUMS.txt` identify the fixed
public files.
