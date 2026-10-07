# Reproduction and frozen-source boundary

Run `python -X utf8 check_package.py` from this entry directory with Python 3.13 (standard library only). This portable, read-only command verifies every distributed SHA-256 value and the exact 37-file dependency closure, rejecting missing or extra files. It checks packaging integrity, not mathematical correctness.

Accepted main PDF SHA-256: `FFF7AAA234A0D88E671F30A65CF54DDD4D84FD4430A0794AC70044A61AEE8E0A`.

`manuscript.md` and the supplied TeX/PDF are byte-frozen. The original 37-file closure and manifest are under `proof-dossier/`, preserving original repository-relative paths. Resolve manuscript references beginning `loops/` relative to `proof-dossier/`. The manifest is `loops/NONPAVING-HSTAR-PUBLICATION-PREP-0001/A1-证明依赖闭包.sha256` there. Selected dependencies retain historical workflow labels for hash identity; these are not review-status claims.

For the frozen finite checks, use Windows and non-optimized Python 3.13; never pass `-O`, because assertions are part of the checking contract. The S17 guard additionally requires SymPy (tested with 1.14.0). S22 uses `ctypes.WinDLL` and Windows process-memory monitoring; Linux support is not claimed. From `proof-dossier/`, run guards serially, honoring their built-in time/memory gates:

```powershell
python -X utf8 loops/PAVING-HSTAR-LOWER-FLAT-NONCRITICAL-KERNEL-GATE-0001/verification/s17_bernstein_tail_guard.py
python -X utf8 loops/PAVING-HSTAR-LOWER-FLAT-NONCRITICAL-KERNEL-GATE-0001/verification/s22_prefix_exact_guard.py
```

Their fixed finite scopes and previously accepted receipts are recorded in the adjacent S17G and S22G documents; they are not substitutes for the uniform analytic proof. Stop on failure; do not automatically retry or remove the resource guards.

Compile from `paper` using a standard installed LaTeX environment: run `pdflatex main.tex` twice (or Tectonic). Keep `manifest-cjk.png` beside `main.tex`: it renders the Chinese manifest filename, not a proof figure. Standard packages listed in the TeX are required. No machine-specific converter or private third-party PDF is needed. Regenerated PDF bytes may differ with the compiler version. No runtime is downloaded by this package.
