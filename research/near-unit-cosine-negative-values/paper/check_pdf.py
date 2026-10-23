"""Render every page with project PyMuPDF/Pillow and preserve QA evidence."""
import json
from pathlib import Path
import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
CACHE = Path('Z:/TEMP/MathExplore/MATH-DIR-0147-writing')
doc = fitz.open(HERE / 'main.pdf')
rows = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    img.save(CACHE / f'page-{i+1}.png')
    text = page.get_text()
    (CACHE / f'page-{i+1}.txt').write_text(text, encoding='utf-8')
    bad = [list(b[:4]) for b in page.get_text('blocks') if not page.rect.contains(fitz.Rect(b[:4]))]
    rows.append({'page': i+1, 'outside_page_blocks': bad, 'replacement_character': '\ufffd' in text,
                 'links': len(page.get_links()), 'page_number_present': str(i+1) in text.splitlines()[-2:]})
(CACHE / 'pdf-check.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
print(json.dumps(rows, indent=2))
