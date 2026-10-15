from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pymupdf as fitz
from PIL import Image, ImageChops, ImageDraw


PAPER = Path(__file__).resolve().parent
SOURCE = PAPER.parent / "manuscript.md"
TEX = PAPER / "main.tex"
PDF = PAPER / "main.pdf"
AUDIT = PAPER / "audit"
RENDERED = AUDIT / "rendered-pages"
REPORT = AUDIT / "pdf-audit.json"
EXPECTED_SOURCE_SHA256 = "A7B55C458A30CAD0B8DF11BDF643788113F8C6D35FE046067E2499DF38245B2B"

EXPECTED_TEXT_MARKERS = [
    "Sharp Schatten constants for the arithmetic symmetric modulus",
    "Theorem 1.1",
    "Corollary 1.2",
    "Theorem 1.3",
    "Theorem 1.4",
    "Theorem 1.5",
    "Proposition 2.1",
    "Lemma 3.1",
    "Proposition 4.1",
    "Lemma 6.1",
    "Proposition 7.1",
    "Lemma 8.1",
    "AI-assisted research and writing",
    "Jean-Christophe Bourin",
    "Teng Zhang",
    "Mohamed Amine Aouichaoui",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    source_hash = sha256(SOURCE)
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(
            f"frozen source hash mismatch: expected {EXPECTED_SOURCE_SHA256}, got {source_hash}"
        )
    if not TEX.is_file() or not PDF.is_file():
        raise RuntimeError("main.tex and main.pdf must exist before the PDF audit")

    RENDERED.mkdir(parents=True, exist_ok=True)
    for stale in list(RENDERED.glob("page-*.png")) + list(RENDERED.glob("contact-*.png")):
        stale.unlink()

    document = fitz.open(PDF)
    if document.is_encrypted:
        raise RuntimeError("PDF is encrypted")

    pages: list[dict[str, object]] = []
    images: list[Image.Image] = []
    extracted_parts: list[str] = []
    replacement_characters = 0
    invalid_links = 0
    out_of_bounds_blocks = 0
    tight_render_margins = 0

    for index, page in enumerate(document):
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        image_path = RENDERED / f"page-{index + 1:02d}.png"
        pixmap.save(image_path)
        image = Image.open(image_path).convert("RGB")
        images.append(image.copy())

        text = page.get_text("text")
        extracted_parts.append(text)
        replacement_characters += text.count("\ufffd")
        bounds = page.rect
        blocks = page.get_text("blocks")
        bad_blocks = [
            [round(value, 3) for value in block[:4]]
            for block in blocks
            if block[0] < -1
            or block[1] < -1
            or block[2] > bounds.width + 1
            or block[3] > bounds.height + 1
        ]
        out_of_bounds_blocks += len(bad_blocks)

        links = page.get_links()
        bad_links = []
        for link in links:
            target_page = link.get("page", -1)
            uri = link.get("uri")
            if target_page >= len(document) or (target_page < -1 and not uri):
                bad_links.append(
                    {"kind": link.get("kind"), "page": target_page, "uri": uri}
                )
        invalid_links += len(bad_links)

        white = Image.new("RGB", image.size, "white")
        content_box = ImageChops.difference(image, white).getbbox()
        margins = None
        if content_box:
            margins = [
                content_box[0],
                content_box[1],
                image.width - content_box[2],
                image.height - content_box[3],
            ]
            if min(margins) < 12:
                tight_render_margins += 1

        pages.append(
            {
                "page": index + 1,
                "pixels": list(image.size),
                "text_characters": len(text),
                "text_blocks": len(blocks),
                "bad_blocks": bad_blocks,
                "links": len(links),
                "bad_links": bad_links,
                "content_box": list(content_box) if content_box else None,
                "render_margins_pixels": margins,
                "render": str(image_path.relative_to(PAPER)).replace("\\", "/"),
            }
        )

    thumbnail_width = 320
    for start in range(0, len(images), 4):
        group = images[start : start + 4]
        thumbs: list[Image.Image] = []
        for offset, image in enumerate(group):
            height = round(image.height * thumbnail_width / image.width)
            thumb = image.resize((thumbnail_width, height))
            canvas = Image.new("RGB", (thumbnail_width + 20, height + 44), "white")
            canvas.paste(thumb, (10, 34))
            ImageDraw.Draw(canvas).text(
                (10, 8), f"Page {start + offset + 1}", fill="black"
            )
            thumbs.append(canvas)
        sheet = Image.new(
            "RGB",
            (sum(item.width for item in thumbs), max(item.height for item in thumbs)),
            "#d0d0d0",
        )
        x = 0
        for item in thumbs:
            sheet.paste(item, (x, 0))
            x += item.width
        sheet.save(RENDERED / f"contact-{start // 4 + 1:02d}.png")

    extracted = normalized("\n".join(extracted_parts))
    missing_text_markers = [marker for marker in EXPECTED_TEXT_MARKERS if marker not in extracted]
    equation_tags = sorted(
        set(re.findall(r"\\tag\{(\d+\.\d+)\}", SOURCE.read_text(encoding="utf-8"))),
        key=lambda item: tuple(int(part) for part in item.split(".")),
    )
    missing_equation_tags = [tag for tag in equation_tags if f"({tag})" not in extracted]
    unresolved_reference_tokens = extracted.count("??")
    blank_pages = [page["page"] for page in pages if page["content_box"] is None]
    metadata = document.metadata
    document.close()

    failures = []
    if replacement_characters:
        failures.append("replacement characters found in extracted text")
    if out_of_bounds_blocks:
        failures.append("text blocks extend beyond page boundaries")
    if invalid_links:
        failures.append("invalid PDF links found")
    if tight_render_margins:
        failures.append("rendered content touches the page boundary")
    if blank_pages:
        failures.append("blank rendered pages found")
    if missing_text_markers:
        failures.append("expected manuscript text markers are missing")
    if missing_equation_tags:
        failures.append("expected equation tags are missing")
    if unresolved_reference_tokens:
        failures.append("unresolved reference tokens found")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "source": str(SOURCE),
        "source_sha256": source_hash,
        "tex": str(TEX),
        "tex_sha256": sha256(TEX),
        "pdf": str(PDF),
        "pdf_sha256": sha256(PDF),
        "page_count": len(pages),
        "metadata": metadata,
        "checks": {
            "rendered_all_pages": len(images) == len(pages),
            "replacement_characters": replacement_characters,
            "out_of_bounds_blocks": out_of_bounds_blocks,
            "invalid_links": invalid_links,
            "tight_render_margins": tight_render_margins,
            "blank_pages": blank_pages,
            "missing_text_markers": missing_text_markers,
            "equation_tags_expected": len(equation_tags),
            "missing_equation_tags": missing_equation_tags,
            "unresolved_reference_tokens": unresolved_reference_tokens,
            "total_links": sum(int(page["links"]) for page in pages),
        },
        "failures": failures,
        "pages": pages,
    }
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        raise RuntimeError("PDF audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
