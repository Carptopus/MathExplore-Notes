from __future__ import annotations
import hashlib
import json
import re
import unicodedata
from pathlib import Path

if not __debug__:
    raise RuntimeError('Optimized Python (-O/-OO) is forbidden: PDF checks must remain enabled')

import pymupdf as fitz
from PIL import Image
import build_tex

PAPER = Path(__file__).resolve().parent
TMP = PAPER.parents[2] / 'tmp' / 'kneser-unified-artifacts'


def canon(s):
    for glyph, literal in json.loads(build_tex.MAPPING_DATA)['pdf_text_transliteration'].items():
        s = s.replace(glyph, literal)
    s = unicodedata.normalize('NFKD', s).lower()
    return ''.join(c for c in s if c.isalnum())


def main():
    _, conversion = build_tex.convert()
    assert hashlib.sha256((PAPER/'main.tex').read_bytes()).hexdigest().upper() == conversion['tex_sha256']
    TMP.mkdir(parents=True, exist_ok=True)
    prior = json.loads((PAPER/'pdf-check.json').read_text(encoding='utf-8')) if (PAPER/'pdf-check.json').exists() else {}
    doc = fitz.open(PAPER/'main.pdf')
    pages, fonts, uris, textparts, internal_links = [], {}, [], [], []
    for index, page in enumerate(doc):
        filename = TMP / f'page-{index+1:02d}.png'
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5), alpha=False).save(filename)
        with Image.open(filename) as im:
            im.verify()
        text = page.get_text(sort=True)
        textparts.append(text)
        links = page.get_links()
        uris.extend(x['uri'] for x in links if x.get('uri'))
        internal_links.extend({'page': x.get('page'), 'target': x.get('nameddest')} for x in links if not x.get('uri'))
        outside = []
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    rect = fitz.Rect(span['bbox'])
                    if not page.rect.contains(rect): outside.append({'text': span['text'], 'bbox': list(rect)})
        for font in page.get_fonts(full=True):
            xref = font[0]
            extracted = doc.extract_font(xref)
            fonts[str(xref)] = {'name': font[3], 'type': font[2], 'embedded_bytes': len(extracted[3])}
        pages.append({'page': index+1, 'render': str(filename), 'sha256': hashlib.sha256(filename.read_bytes()).hexdigest().upper(),
                      'page_size_points': list(page.rect), 'out_of_page_text_spans': outside,
                      'page_number_present': str(index+1) in [s.strip() for s in text.splitlines()], 'link_count': len(links),
                      'replacement_character_count': text.count('\ufffd')})
    text = '\n'.join(textparts)
    prior_pages = {p['page']: p for p in prior.get('pages', [])}
    for p in pages:
        old = prior_pages.get(p['page'], {})
        p['prior_render_sha256'] = old.get('sha256')
        p['prior_render_pixels_identical'] = p['sha256'] == old.get('sha256')
    (TMP/'pdf-text.txt').write_text(text, encoding='utf-8')
    # Headers/footers cannot break a paragraph comparison across page boundaries.
    body = '\n'.join(s for s in text.splitlines() if s.strip() not in ('Carptopus', 'Matroid base-intersection domination') and 'Matroid base-intersection domination' not in s and not re.fullmatch(r'\d+', s.strip()))
    normal = canon(body)
    failures, checked = [], []
    for record in conversion['line_coverage']:
        if record['kind'] not in ('prose', 'bullet', 'reference'): continue
        s = record['source']
        if not s.strip(): continue
        s = re.sub(r'\[([^\]]+)\]\((https?://\S+)\)', r'\1', s)
        if record['kind'] == 'reference': s = re.sub(r'^\[[A-Za-z0-9]+\] ', '', s)
        # Auxiliary normalization affects only the exact frozen literals, not unrelated words.
        for literal in sorted({x['source_literal'] for x in conversion['inline_replacements'] if x['source_line'] == record['line']}, key=len, reverse=True):
            if ' intersection ' in literal or ' union ' in literal or literal == 'negative infinity':
                s = s.replace(literal, literal.replace(' intersection ', ' ').replace(' union ', ' ').replace('negative infinity', '-infinity'))
        c = canon(s)
        if c not in normal: failures.append({'source_line': record['line'], 'source': s})
        checked.append(record['line'])
    missing_urls = sorted(set(conversion['embedded_urls'])-set(uris))
    extra_urls = sorted(set(uris)-set(conversion['embedded_urls']))
    log = (PAPER/'main.log').read_text(encoding='utf-8', errors='replace')
    result = {'source_sha256': conversion['source_sha256'], 'pdf_sha256': hashlib.sha256((PAPER/'main.pdf').read_bytes()).hexdigest().upper(),
              'prior_pdf_sha256': prior.get('pdf_sha256'),
              'page_count': len(pages), 'pages': pages, 'fonts': fonts,
              'all_fonts_embedded': all(x['embedded_bytes'] for x in fonts.values()),
              'prose_source_lines_checked': checked, 'prose_normalized_match_failures': failures,
              'url_set_match': not missing_urls and not extra_urls, 'missing_urls': missing_urls, 'extra_urls': extra_urls,
              'pdf_uri_annotations': uris, 'overfull_boxes': re.findall(r'Overfull[^\n]+', log),
              'internal_reference_links': internal_links,
              'internal_reference_targets_resolve': all(isinstance(x['page'], int) and 0 <= x['page'] < len(doc) and x['target'] in ['ref'+r for r in conversion['references']] for x in internal_links),
              'missing_glyph_warnings': re.findall(r'Missing character[^\n]+', log),
              'underfull_boxes': re.findall(r'Underfull[^\n]+', log),
              'visual_inspection': 'PENDING; render existence is not visual inspection',
              'limitations': ['PDF mathematical extraction is not token-equivalent to TeX; literal source/TeX displays plus rendered inspection are used.',
                              'Normalized prose matching ignores whitespace, punctuation and accents; exact line-wise conversion evidence remains primary.',
                              'No mathematics, novelty or external review audit; no online URL reachability check.']}
    (PAPER/'pdf-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('pages','fonts','prose_source_lines_checked','pdf_uri_annotations')},ensure_ascii=True,indent=2))


if __name__ == '__main__': main()
