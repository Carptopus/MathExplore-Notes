# Artifact check

Status: DONE

Case: MERINO-WELSH-PARALLEL-SUPPORT-UPGRADE-0001

Frozen source SHA256: `11DE5F36F58138091B033578A0780E72E8F620BB9E32BCB7B6135899B65D991F`.

## Build and scope

Frozen manuscript unchanged. Only paper/ and tmp/merino-transfer-artifacts/ were written by task scripts.
Literal numbered headings retained; bibliography generated from the seven frozen source entries. TeX typography maps dashes and the date middle dot without changing wording. Public preprint v0.1-beta; external mathematical review and formal peer review pending.

Commands executed from `D:\Codes\MyProjects\MathExplore`:

```powershell
& 'D:/Codes/MyProjects/MathExplore/.venv/Scripts/python.exe' 'research/Parallel-Support-Transfer-Merino-Welsh/paper/build_tex.py'
& 'D:/DevTools/Codex/resources/tectonic/tectonic.exe' --keep-logs --keep-intermediates 'research/Parallel-Support-Transfer-Merino-Welsh/paper/main.tex'
& 'D:/Codes/MyProjects/MathExplore/.venv/Scripts/python.exe' -B 'research/Parallel-Support-Transfer-Merino-Welsh/paper/check_artifacts.py' --visual-reviewed-pages 1,2,3,4,5,6,7,8,9,10
```

## Checks

- 10 A4 pages rendered at 1.5x with project PyMuPDF; every PNG verified using Pillow.
- PASS: full-page renders inspected; no clipping, garbled glyphs or formula overflow
- Visual inventory: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
- 319 inline/display mathematics expressions exactly preserved in sequence in TeX; equation tags 1-19 preserved and found in PDF extraction.
- 200 nonmath prose fragments of at least 20 normalized characters matched PDF extraction; missing: 0. Whitespace, wrap-hyphens, ligatures and typographic apostrophes normalized. This is auxiliary evidence, not a mathematical audit.
- All theorem conditions, empty-quotient clause, strictness limits, marked-flat intersection text and references retained.
- All seven reference URLs matched embedded PDF URI links; citation hyperlinks inspected structurally.
- Page numbers 1-10 present; no text block outside page bounds; no final missing-character or overfull/underfull warning.

- Page 1: title, author, date separator, preprint status and abstract checked
- Page 2: all three theorem headings, hypotheses and strictness clauses checked
- Pages 3-4: equations 3-8 and marked-flat intersection clause checked
- Pages 5-8: proof continuation, equations 9-18 and sparse-paving conditions checked
- Pages 9-10: equation 19, limitations, disclosure and all seven bibliography entries checked

## Warnings and limits

Fontconfig default-config notice; compiler used bundled Latin Modern successfully. Initial Unicode dash/middle-dot mapping was repaired in converter; final PDF has the intended glyphs. Tectonic fetched its normal ts1-lmr12.tfm cache asset; no runtime was installed.

- Package inputenc Warning: inputenc package ignored with utf8 based engines.
- Package rerunfilecheck Warning: File `main.out' has changed.

Not performed: independent mathematics/novelty audits, network validation of referenced URLs, publishing. Main thread separately verifies the old dependency DOI. DONE means only artifact completion, not proof approval or release authorization.

## File SHA256 inventory

- `build_tex.py`: `47A162F35FF7505AE41CB914B5B3798E5B294083DD69F1766D4E36F774C7B655`
- `check_artifacts.py`: `E2D7EC72CD61EEA82EACDDB88C56FFF49DB52D8D7201A8D7A9C12236915500AD`
- `main.aux`: `ED86DED460D70025B8A3C74F287D24CA2D5840AE5DD193C9FB659EF9666FED06`
- `main.log`: `1BCA01A1423D80A8E3F6B1479D160562D7608641B6438372743963756B7210C1`
- `main.pdf`: `88757059A7058472F4550752C810D45789919752012FD59D69738878517828EF`
- `main.tex`: `E48594F19738A78430F5B9782D66139059346497461A044D6C5C9D10A20DEF32`

Render paths, hashes, page bounds and PDF links are recorded in ARTIFACT-CHECK.json. Render PNGs and extracted text are temporary/rebuildable; no unviewed pages remain.
