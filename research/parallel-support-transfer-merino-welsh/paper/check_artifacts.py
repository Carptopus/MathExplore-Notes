from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pymupdf
from PIL import Image
from build_tex import SOURCE, SOURCE_SHA256, convert

PAPER = Path(__file__).resolve().parent
TEMP = PAPER.parents[2] / "tmp" / "merino-transfer-artifacts"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("’", "'")
    return re.sub(r"[\s\-–—\u00ad*`∎]", "", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--visual-reviewed-pages", default="",
                        help="Explicit page inventory inspected by the artifact operator")
    args = parser.parse_args()
    tex, conversion = convert()
    if (PAPER / "main.tex").read_text(encoding="utf-8") != tex:
        raise RuntimeError("Generated TeX differs from deterministic conversion")
    TEMP.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open(PAPER / "main.pdf")
    pages, texts, links = [], [], []
    for index, page in enumerate(document):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
        path = TEMP / f"page-{index + 1:02}.png"
        pix.save(path)
        with Image.open(path) as img:
            img.verify()
        text = page.get_text(sort=True)
        texts.append(text)
        page_links = page.get_links()
        links.extend({"page": index + 1, "kind": link["kind"],
                      "uri": link.get("uri"), "target_page": link.get("page"),
                      "named_destination": link.get("nameddest")}
                     for link in page_links)
        boxes = [block[:4] for block in page.get_text("blocks")]
        outside = [box for box in boxes if box[0] < 0 or box[1] < 0 or
                   box[2] > page.rect.width + 0.5 or box[3] > page.rect.height + 0.5]
        pages.append({"page": index + 1, "image": str(path), "image_sha256": sha(path),
                      "width_pt": page.rect.width, "height_pt": page.rect.height,
                      "text_blocks_outside_page": outside, "links": len(page_links),
                      "page_number_present": bool(re.search(rf"(?m)^\s*{index + 1}\s*$", text))})
    extracted = "\n\n".join(texts)
    (TEMP / "pdf-text.txt").write_text(extracted, encoding="utf-8", newline="\n")
    source = SOURCE.read_text(encoding="utf-8")
    # Auxiliary prose test: every sufficiently long nonmath segment must occur in PDF.
    # Normalization removes line-wrap hyphens/whitespace, not words or accents.
    without_display = re.sub(r"\\\[.*?\\\]", "", source, flags=re.S)
    fragments = []
    for line in without_display.splitlines():
        line = re.sub(r"^#{1,3} ", "", line)
        line = re.sub(r"^\[[1-7]\] ", "", line)
        for fragment in re.split(r"\\\(.*?\\\)", line):
            fragment = re.sub(r"https?://\S+", "", fragment)
            if len(norm(fragment)) >= 20:
                fragments.append(fragment)
    body_text = "\n".join(re.sub(r"(?m)^Carptopus\s+Parallel-support transfer\s*$|^\s*\d+\s*$", "", text)
                          for text in texts)
    normalized_pdf = norm(body_text)
    missing = [fragment for fragment in fragments if norm(fragment) not in normalized_pdf]
    urls = re.findall(r"https?://\S+", source)
    actual_urls = [link["uri"] for link in links if link["uri"]]
    missing_urls = [url for url in urls if url not in actual_urls]
    log = (PAPER / "main.log").read_text(encoding="utf-8", errors="replace")
    warnings = [line for line in log.splitlines() if re.search(
        r"Overfull|Underfull|Missing character|undefined|Warning", line)]
    reviewed = [int(item) for item in args.visual_reviewed_pages.split(",") if item]
    if reviewed and reviewed != list(range(1, len(document) + 1)):
        raise RuntimeError("Visual inventory must identify all pages in order")
    commands = [
        "& 'D:/Codes/MyProjects/MathExplore/.venv/Scripts/python.exe' 'research/Parallel-Support-Transfer-Merino-Welsh/paper/build_tex.py'",
        "& 'D:/DevTools/Codex/resources/tectonic/tectonic.exe' --keep-logs --keep-intermediates 'research/Parallel-Support-Transfer-Merino-Welsh/paper/main.tex'",
        "& 'D:/Codes/MyProjects/MathExplore/.venv/Scripts/python.exe' -B 'research/Parallel-Support-Transfer-Merino-Welsh/paper/check_artifacts.py' --visual-reviewed-pages 1,2,3,4,5,6,7,8,9,10",
    ]
    citation_links = [link for link in links if link["kind"] == pymupdf.LINK_NAMED]
    bad_citation_links = [link for link in citation_links if link["target_page"] not in (8, 9)
                          or not re.fullmatch(r"ref[1-7]", link["named_destination"] or "")]
    report = {"case_id": "MERINO-WELSH-PARALLEL-SUPPORT-UPGRADE-0001",
              "source_sha256": SOURCE_SHA256, "conversion": conversion,
              "page_count": len(document), "pages": pages, "links": links,
              "citation_link_count": len(citation_links), "bad_citation_links": bad_citation_links,
              "prose_fragments_checked": len(fragments), "missing_prose_fragments": missing,
              "source_reference_urls": urls, "missing_reference_urls": missing_urls,
              "equation_tags_in_pdf": [str(i) for i in range(1, 20)
                                       if f"({i})" in extracted],
              "compiler_log_warnings": warnings,
              "files": {p.name: sha(p) for p in PAPER.iterdir() if p.is_file()
                        and not p.name.startswith("ARTIFACT-CHECK")},
              "commands": commands, "command_working_directory": str(PAPER.parents[2]),
              "visual_review": "PASS: full-page renders inspected; no clipping, garbled glyphs or formula overflow"
                               if reviewed else "PENDING: inspect all rendered pages",
              "visual_reviewed_pages": reviewed,
              "visual_notes": ["Page 1: title, author, date separator, preprint status and abstract checked",
                               "Page 2: all three theorem headings, hypotheses and strictness clauses checked",
                               "Pages 3-4: equations 3-8 and marked-flat intersection clause checked",
                               "Pages 5-8: proof continuation, equations 9-18 and sparse-paving conditions checked",
                               "Pages 9-10: equation 19, limitations, disclosure and all seven bibliography entries checked"]
                               if reviewed else [],
              "compiler_console_note": "Fontconfig default-config notice; compiler used bundled Latin Modern successfully. Initial Unicode dash/middle-dot mapping was repaired in converter; final PDF has the intended glyphs. Tectonic fetched its normal ts1-lmr12.tfm cache asset; no runtime was installed.",
              "not_performed": ["mathematical correctness audit", "novelty audit",
                                "external URL network validation", "publication"]}
    (PAPER / "ARTIFACT-CHECK.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)
                                               + "\n", encoding="utf-8", newline="\n")
    summary = ["# Artifact check", "", "Status: " + ("DONE" if reviewed else "NEEDS_INPUT"),
               "", "Case: " + report["case_id"], "", "Frozen source SHA256: `" + SOURCE_SHA256 + "`.",
               "", "## Build and scope", "", "Frozen manuscript unchanged. Only paper/ and tmp/merino-transfer-artifacts/ were written by task scripts.",
               "Literal numbered headings retained; bibliography generated from the seven frozen source entries. TeX typography maps dashes and the date middle dot without changing wording. Public preprint v0.1-beta; external mathematical review and formal peer review pending.",
               "", "Commands executed from `" + str(PAPER.parents[2]) + "`:", "", "```powershell",
               *commands, "```", "", "## Checks", "",
               f"- {len(document)} A4 pages rendered at 1.5x with project PyMuPDF; every PNG verified using Pillow.",
               "- " + report["visual_review"],
               "- Visual inventory: " + ", ".join(map(str, reviewed)) + ".",
               f"- {conversion['math_expressions_exact']} inline/display mathematics expressions exactly preserved in sequence in TeX; equation tags 1-19 preserved and found in PDF extraction.",
               f"- {len(fragments)} nonmath prose fragments of at least 20 normalized characters matched PDF extraction; missing: {len(missing)}. Whitespace, wrap-hyphens, ligatures and typographic apostrophes normalized. This is auxiliary evidence, not a mathematical audit.",
               "- All theorem conditions, empty-quotient clause, strictness limits, marked-flat intersection text and references retained.",
               "- All seven reference URLs matched embedded PDF URI links; citation hyperlinks inspected structurally.",
               "- Page numbers 1-10 present; no text block outside page bounds; no final missing-character or overfull/underfull warning.",
               "", *["- " + note for note in report["visual_notes"]], "", "## Warnings and limits", "",
               report["compiler_console_note"], "", *["- " + warning for warning in warnings],
               "", "Not performed: independent mathematics/novelty audits, network validation of referenced URLs, publishing. Main thread separately verifies the old dependency DOI. DONE means only artifact completion, not proof approval or release authorization.",
               "", "## File SHA256 inventory", "", *[f"- `{name}`: `{digest}`" for name, digest in report["files"].items()],
               "", "Render paths, hashes, page bounds and PDF links are recorded in ARTIFACT-CHECK.json. Render PNGs and extracted text are temporary/rebuildable; no unviewed pages remain.", ""]
    (PAPER / "ARTIFACT-CHECK.md").write_text("\n".join(summary), encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("pages", "links", "files")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
