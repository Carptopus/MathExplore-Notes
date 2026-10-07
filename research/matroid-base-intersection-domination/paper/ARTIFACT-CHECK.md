# Artifact check — matroid base-intersection domination

Status: DONE for this artifact task only, with the final main-thread-frozen inline-notation map applied. This is not mathematical/novelty audit, external review, publication authorization, or project acceptance.

Frozen manuscript SHA256: `C1B38B8A70E3C98546A691F959CE28E65C14EB586F6F06825C88861BDB9BD5D2`.

Frozen `inline-notation.json` SHA256: `6D1198B8BC43B0469E5E05BC66810E2BC9AFFFEA730ECDB8370A38661D5DC0A7`.

Exported `main.pdf`: 14 A4 pages, SHA256 `768FD904FB2DEC51DDA73E0D7FCFD28AB4E0FC2D337957BC477173A77805A4CA`.

Standalone `main.tex`: SHA256 `AB89DB4BA0BC2415E02CA8FD125961CDA5D7883CFAD70B43CDE23A85DA64DE05`.

## Build and evidence

Run from `D:\Codes\MyProjects\MathExplore` using the existing project interpreter and installed compiler:

```powershell
& '.venv/Scripts/python.exe' 'research/Matroid-Base-Intersection-Domination/paper/build_tex.py'
& 'D:/DevTools/Codex/resources/tectonic/tectonic.exe' --keep-logs --keep-intermediates 'research/Matroid-Base-Intersection-Domination/paper/main.tex'
& '.venv/Scripts/python.exe' 'research/Matroid-Base-Intersection-Domination/paper/build_tex.py' --check-only
& '.venv/Scripts/python.exe' 'research/Matroid-Base-Intersection-Domination/paper/check_pdf.py'
```

`build_tex.py` rejects source and mapping hash drift. TeX regeneration is byte-identical. `conversion-check.json` records every source line and corresponding output: all 431 lines covered, all 25 display interiors retained literally (newline normalization only), all 12 equation tags, 25 headings, 17 reference labels and 14 embedded URLs matched. No theorem numbering, reference inventories or review-status prose were inherited from the mechanics template. The source and notation map were not edited by the builder.

The frozen map is applied once, longest literal first, only in prose/bullets/headings, with identifier boundaries including straight and curly apostrophes. Operators `>=`/`<=` are the explicit boundary exception. Title/author/date, display interiors, bibliography, URLs, citation labels and code spans are excluded. Bare `a`/`A` are absent from the final map. No unlisted token is inferred. All 717 replacements retain source literal, exact TeX and source line. For all 404 prose chunks, emitted inline TeX is checked against the frozen map and inverted back to exactly `escape(source_chunk)`; the inverse result is recorded. This exact check, not PDF normalization, is the primary inline-math fidelity evidence. The last four parent-frozen literal additions (`a_0b_1`, `a_1b_i`, `a_0a_1`, `n_l`) are applied; `rg -F '\_' main.tex` reports zero matches (rg exit 1 means no match), confirmed by a guarded zero-match check.

Both public build/check scripts explicitly reject optimized Python `-O`/`-OO`. Actual checks: normal `build_tex.py --check-only` exit 0; `-O build_tex.py --check-only` exit 1; `-O check_pdf.py` exit 1, each with the intended RuntimeError.

`pdf-check.json` contains extraction/layout/font/link evidence. Of 134 prose/bullet/reference source lines checked, 122 match normalized PDF extraction; 12 mathematical paragraphs do not match the linearized text. These differences remain explicit, not suppressed: source lines 40 (p2), 165 (p5), 178 (p6), 235 (p7), 295 (p9), 319/321 (p10), 327/329/341/343 (p11), 376 (p12). Each was visually compared against source/frozen mapping. The visible gamma superscript/subscript order, binomial two-row typography, summation operators and other mapped inline notation are intact. Individual explanation/page/check evidence is in `ARTIFACT-CHECK.json`. This is not a claim of token-equivalent PDF mathematical extraction.

Normalization transliterates only the provided Greek table and ignores punctuation/whitespace/accents; it remains auxiliary. Literal display equality and emitted-TeX inverse equality are the primary content evidence. All 14 external URI targets match, including the parenthesized Akkari DOI; all 32 internal citation annotations resolve. Online URL reachability was not checked.

## Full-page inspection

PyMuPDF 1.28.2 and Pillow 12.3.0 from `.venv` rendered/verified all 14 pages at 1.5x (approximately 108 dpi). Every full-page PNG of PDF `2898F7BE77DDB11342536F42A1B93AE1BA9ECB995BF08F8EDFC456014601C25E` was opened with `view_image`. Intermediate PDF `E5FFD0DF60D047ED6A0BD851A14E377BF10D8D16D09AB850C0A7FD29EB9C1637` changed only p10/p11, both opened and inspected again; other 12 hashes were identical. The final four literal additions change only p7/p11 relative to that intermediate PDF; both final pages were opened and inspected again. The other 12 final PNG file hashes are exactly equal to already-inspected intermediate pixels. No unseen pages. This explicit two-step equality chain preserves full-page visual evidence without unnecessarily viewing identical pixels again. Current and preceding render hashes, paths and provenance are in `ARTIFACT-CHECK.json` / `pdf-check.json`. Auxiliary extraction is `tmp/kneser-unified-artifacts/pdf-text.txt`.

All pages have readable text, aligned formulas/tags, complete page numbers and intact margins. No cropping, formula overflow, garbled text or overlapping content was observed. All 21 fonts are embedded. Unicode minus, superscript 2, middle dot, en dash, proof square, accented names and mapped Greek notation are visible. Only explicitly mapped source notation is converted to inline math; remaining source notation stays literal. No mathematical content beyond the frozen mapping was inferred or rewritten.

The former orphan section 9 heading is fixed: it now accompanies subsection 9.1 on page 11. Appendix B's first bullet is wholly on page 13. There are no remaining overfull/underfull-box or missing-glyph warnings, and no material unresolved layout issue was observed. The compiler emitted a Fontconfig default-config warning, but embedded-font and rendered-glyph checks passed. Ordinary paragraph/proof page continuations remain normal pagination.

## UI and scope limitations

`open_in_codex` returned queued for the parent task `01a11730-d4bd-7bc1-a68b-29add8a8dea5`. The subagent's `compile_latex_document` request had not returned diagnostics at closeout. The main thread reports its separate native request timed out during initial format/package downloading, not on a source diagnostic. Native preview compilation remains unconfirmed. Native preview is not used as proof of PDF export; the installed Tectonic export and actual rendered PDF are the completed acceptance basis for the original contract.

This task did not inspect mathematical correctness, novelty, verification-code results or external peer-review status, and did not modify those materials. No dependencies were installed, no research state changed, and no commits/uploads/publication occurred. Deterministic TeX reproduction is verified; identical PDF bytes across compiler versions/runs are not promised.

`ARTIFACT-CHECK.json` holds the machine-readable receipt, page inventory, check scope and hashes of build/evidence files. `finalize_check.py` is an internal receipt helper, not a required public reproduction dependency: it records already-completed visual inspection only for this exact PDF hash and must not be reused to certify changed pixels. The parent-owned paper README is preserved.
