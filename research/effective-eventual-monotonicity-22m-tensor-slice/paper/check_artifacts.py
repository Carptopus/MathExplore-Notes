from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pymupdf as fitz
from PIL import Image


PAPER = Path(__file__).resolve().parent
PDF = PAPER / "main.pdf"
RENDER_DIR = PAPER / "build" / "rendered-pages"
TEXT_PATH = PAPER / "build" / "pdf-text.txt"
JSON_PATH = PAPER / "artifact-check.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    if not PDF.is_file():
        raise RuntimeError(f"Missing final PDF: {PDF}")
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    document = fitz.open(PDF)
    pages: list[dict[str, object]] = []
    all_text: list[str] = []
    all_uris: list[str] = []
    all_fonts: dict[int, dict[str, object]] = {}

    for page_index, page in enumerate(document):
        page_number = page_index + 1
        text = page.get_text("text")
        all_text.append(text)
        blocks = page.get_text("blocks")
        outside = []
        for block in blocks:
            x0, y0, x1, y1, block_text = block[:5]
            if block_text.strip() and (
                x0 < -0.5
                or y0 < -0.5
                or x1 > page.rect.width + 0.5
                or y1 > page.rect.height + 0.5
            ):
                outside.append([x0, y0, x1, y1, block_text[:80]])

        links = page.get_links()
        uris = [link["uri"] for link in links if link.get("uri")]
        all_uris.extend(uris)
        internal_links = sum(1 for link in links if not link.get("uri") and (link.get("page", -1) >= 0 or link.get("nameddest")))

        for font in page.get_fonts(full=True):
            xref = int(font[0])
            if xref not in all_fonts:
                extracted = document.extract_font(xref)
                all_fonts[xref] = {
                    "xref": xref,
                    "extension": font[1],
                    "type": font[2],
                    "base_font": font[3],
                    "name": font[4],
                    "encoding": font[5],
                    "embedded_bytes": len(extracted[3]) if extracted and extracted[3] else 0,
                }

        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False)
        render_path = RENDER_DIR / f"page-{page_number:02d}.png"
        pixmap.save(render_path)
        with Image.open(render_path) as image:
            image.verify()
        with Image.open(render_path) as image:
            width, height = image.size
            extrema = image.convert("L").getextrema()

        pages.append(
            {
                "page": page_number,
                "mediabox": [page.rect.x0, page.rect.y0, page.rect.x1, page.rect.y1],
                "text_characters": len(text),
                "replacement_characters": text.count("\ufffd"),
                "outside_text_blocks": outside,
                "uri_links": uris,
                "internal_links": internal_links,
                "render": str(render_path.relative_to(PAPER)),
                "render_sha256": sha256(render_path),
                "render_pixels": [width, height],
                "grayscale_extrema": list(extrema),
            }
        )

    joined_text = "\n\f\n".join(all_text)
    TEXT_PATH.write_text(joined_text, encoding="utf-8", newline="\n")
    normalized_text = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", joined_text))
    expected_uris = [
        "mailto:carptopus@163.com",
        "https://doi.org/10.1080/03081087.2016.1164660",
        "https://doi.org/10.30757/ALEA.v22-29",
        "https://doi.org/10.1007/s10208-014-9194-z",
        "https://doi.org/10.1016/j.aim.2012.05.006",
        "https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/tensor-computations/TR-16",
        "https://github.com/openai/math",
    ]
    required_text = [
        "Effective eventual monotonicity on the (2, 2, m) tensor slice",
        "Carptopus",
        "Internal proof audit passed. External peer review has not been completed.",
        "Theorem 1.1",
        "Theorem 2.2",
        "3 × 10103 + 3",
        "3 × 10103",
        "it says nothing about the comparison",
        "1 ≤r < 3 × 10103",
        "References",
        "Draisma and E. Horobe",
        "OpenProblemsInNLA",
        "AI-assisted research and writing disclosure",
        "Carptopus is the sole author",
        "Codex is not an author or responsible author.",
    ]
    missing_text = [needle for needle in required_text if needle not in normalized_text]
    missing_uris = [uri for uri in expected_uris if uri not in all_uris]
    embedded_failures = [font for font in all_fonts.values() if not font["embedded_bytes"]]
    failures = {
        "missing_required_text": missing_text,
        "missing_expected_uris": missing_uris,
        "missing_internal_citation_links": [] if sum(page["internal_links"] for page in pages) >= 6 else ["expected at least six"],
        "pages_with_replacement_characters": [
            page["page"] for page in pages if page["replacement_characters"]
        ],
        "pages_with_outside_text_blocks": [
            page["page"] for page in pages if page["outside_text_blocks"]
        ],
        "blank_pages": [page["page"] for page in pages if page["text_characters"] < 20],
        "fonts_without_embedded_program": embedded_failures,
    }
    passed = all(not value for value in failures.values())
    evidence = {
        "status": "PASS" if passed else "REVISE",
        "pdf_sha256": sha256(PDF),
        "page_count": len(document),
        "page_size_points": [document[0].rect.width, document[0].rect.height],
        "pymupdf_version": fitz.VersionBind,
        "pillow_version": Image.__version__,
        "pages": pages,
        "fonts": sorted(all_fonts.values(), key=lambda item: int(item["xref"])),
        "uri_inventory": sorted(set(all_uris)),
        "text_sha256": sha256(TEXT_PATH),
        "failures": failures,
    }
    JSON_PATH.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
