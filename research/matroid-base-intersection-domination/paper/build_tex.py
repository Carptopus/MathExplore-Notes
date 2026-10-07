from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

if not __debug__:
    raise RuntimeError('Optimized Python (-O/-OO) is forbidden: conversion fidelity assertions must remain enabled')

# Mechanical Markdown conversion only; all mathematical display interiors are literal.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'manuscript.md'
PAPER = Path(__file__).resolve().parent
SOURCE_SHA256 = 'C1B38B8A70E3C98546A691F959CE28E65C14EB586F6F06825C88861BDB9BD5D2'
MAPPING_SHA256 = '6D1198B8BC43B0469E5E05BC66810E2BC9AFFFEA730ECDB8370A38661D5DC0A7'
MAPPING_DATA = (PAPER / 'inline-notation.json').read_bytes()
if hashlib.sha256(MAPPING_DATA).hexdigest().upper() != MAPPING_SHA256:
    raise RuntimeError('Frozen notation mapping hash mismatch')
MAPPING = json.loads(MAPPING_DATA)['literal_to_tex']
PATTERNS = [re.escape(s) if s in ('>=', '<=') else r"(?<![A-Za-z0-9_'’])" + re.escape(s) + r"(?![A-Za-z0-9_'’])"
            for s in sorted(MAPPING, key=lambda s: (-len(s), s))]
NOTATION_PATTERN = re.compile('|'.join(PATTERNS))
REPLACEMENTS = []
PROSE_ROUNDTRIPS = []
PREAMBLE = r'''% Hash-pinned mechanical conversion; see conversion-check.json.
\documentclass[11pt]{article}
\usepackage[a4paper,margin=27mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,microtype,amsmath,amssymb,mathtools,needspace,xcolor}
\usepackage[colorlinks=true,linkcolor=blue!55!black,urlcolor=blue!65!black]{hyperref}
\usepackage{xurl,fancyhdr}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{Carptopus}\fancyhead[R]{Matroid base-intersection domination}
\fancyfoot[C]{\thepage}\setlength{\headheight}{14pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.44em}
\setlength{\emergencystretch}{4em}\urlstyle{same}
'''


def escape(s):
    table = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
             '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
             '^': r'\textasciicircum{}', '∎': r'\hfill\ensuremath{\square}',
             '−': r'\ensuremath{-}', '²': r'\textsuperscript{2}',
             '·': r'\textperiodcentered{}', '–': '--', '—': '---',
             'é': r"\'{e}", 'ő': r'\H{o}'}
    return ''.join(table.get(c, c) for c in s)


def mapped_text(s, line):
    if line is None:
        return escape(s)
    emitted, inverse, selected = [], [], []
    pos = 0
    for match in NOTATION_PATTERN.finditer(s):
        literal = match[0]
        prefix = s[pos:match.start()]
        tex = r'\(' + MAPPING[literal] + r'\)'
        emitted.extend([escape(prefix), tex])
        inverse.extend([prefix, literal])
        selected.append((literal, MAPPING[literal]))
        REPLACEMENTS.append({'source_line': line, 'source_literal': literal, 'replacement_tex': MAPPING[literal],
                             'emitted_tex': tex, 'chunk_start': match.start(), 'chunk_end': match.end()})
        pos = match.end()
    emitted.append(escape(s[pos:]))
    inverse.append(s[pos:])
    # Independent source reconstruction from the selected match spans and literals.
    assert ''.join(inverse) == s, 'Inline mapping inverse lost source text'
    emitted_chunk = ''.join(emitted)
    actual_math = re.findall(r'\\\((.*?)\\\)', emitted_chunk)
    assert actual_math == [tex for literal, tex in selected], 'Emitted math differs from frozen mapping'
    inverse_iter = iter(selected)
    reconstructed_escaped = re.sub(r'\\\((.*?)\\\)', lambda match: escape(next(inverse_iter)[0]), emitted_chunk)
    assert reconstructed_escaped == escape(s), 'Inverse of emitted TeX does not equal literal escaped source'
    PROSE_ROUNDTRIPS.append({'source_line': line, 'source_chunk': s, 'reconstructed_chunk': ''.join(inverse),
                            'emitted_chunk': emitted_chunk, 'inverse_emitted_tex_exact': True})
    return emitted_chunk


def prose(s, refs, line=None):
    pattern = r'(\[[^\]]+\]\(https?://\S+\)|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[A-Za-z0-9]+(?:, [A-Za-z0-9]+)*\])'
    out = []
    for t in re.split(pattern, s):
        link = re.fullmatch(r'\[([^\]]+)\]\((https?://\S+)\)', t)
        if link:
            out.append(r'\href{' + link[2] + '}{' + escape(link[1]) + '}')
        elif t.startswith('**') and t.endswith('**'):
            out.append(r'\textbf{' + mapped_text(t[2:-2], line) + '}')
        elif t.startswith('*') and t.endswith('*'):
            out.append(r'\emph{' + mapped_text(t[1:-1], line) + '}')
        elif t.startswith('`') and t.endswith('`'):
            out.append(r'\texttt{' + escape(t[1:-1]) + '}')
        elif t.startswith('[') and t.endswith(']') and all(x in refs for x in t[1:-1].split(', ')):
            out.append('[' + ', '.join(r'\hyperlink{ref' + x + '}{' + escape(x) + '}' for x in t[1:-1].split(', ')) + ']')
        else:
            out.append(mapped_text(t, line))
    return ''.join(out)


def convert():
    REPLACEMENTS.clear()
    PROSE_ROUNDTRIPS.clear()
    data = SOURCE.read_bytes()
    actual = hashlib.sha256(data).hexdigest().upper()
    if actual != SOURCE_SHA256:
        raise RuntimeError('Frozen source hash mismatch: ' + actual)
    source = data.decode('utf-8')
    lines = source.splitlines()
    header = [(i, s) for i, s in enumerate(lines, 1) if s.strip()][:3]
    if not header[0][1].startswith('# ') or header[1][1] != 'Carptopus':
        raise RuntimeError('Unexpected title/author')
    title, author, date = [x[1] for x in header]
    refs = re.findall(r'^\[([A-Za-z0-9]+)\] ', source, re.M)
    if len(set(refs)) != len(refs):
        raise RuntimeError('Duplicate bibliography label')
    out = [PREAMBLE.rstrip(), r'\title{' + escape(title[2:]) + '}',
           r'\author{' + escape(author) + '}', r'\date{' + escape(date) + '}',
           r'\hypersetup{pdfauthor={Carptopus},pdftitle={' + escape(title[2:]) + '}}',
           r'\begin{document}', r'\maketitle']
    records = [{'line': i, 'kind': 'header', 'source': s} for i, s in header]
    display = abstract = bibliography = itemize = False
    headings, body_refs = [], []
    for i, s in enumerate(lines, 1):
        if i <= header[-1][0]:
            if not s.strip():
                records.append({'line': i, 'kind': 'blank', 'source': s})
            continue
        kind = 'prose'
        if s == '$$':
            display = not display
            emitted = r'\[' if display else r'\]'
            kind = 'display-delimiter'
        elif display:
            emitted, kind = s, 'display-interior'
        elif s.startswith('## ') or s.startswith('### '):
            if itemize:
                out.append(r'\end{itemize}'); itemize = False
            if abstract:
                out.append(r'\end{abstract}'); abstract = False
            if bibliography:
                out.append(r'\end{thebibliography}'); bibliography = False
            heading = s.split(' ', 1)[1]
            headings.append(heading)
            if heading == 'Abstract':
                emitted = r'\begin{abstract}'; abstract = True
            elif heading == 'References':
                emitted = r'\begin{thebibliography}{McG12}\small\raggedright'; bibliography = True
            else:
                next_nonblank = next((x for x in lines[i:] if x.strip()), '')
                reserve = 14 if s.startswith('## ') and next_nonblank.startswith('### ') else 8
                emitted = r'\Needspace{' + str(reserve) + r'\baselineskip}' + '\n' + (r'\subsection*{' if s.startswith('### ') else r'\section*{') + prose(heading, refs, i) + '}'
            kind = 'heading'
        elif bibliography and s.strip():
            m = re.fullmatch(r'\[([A-Za-z0-9]+)\] (.+)', s)
            if not m:
                raise RuntimeError(f'Unhandled reference line {i}')
            body_refs.append(m[1])
            emitted = r'\bibitem[' + m[1] + ']{ref' + m[1] + '}' + r'\hypertarget{ref' + m[1] + '}{}' + prose(m[2], [])
            kind = 'reference'
        elif s.startswith('- '):
            if not itemize:
                out.append(r'\begin{itemize}'); itemize = True
            emitted = r'\Needspace{4\baselineskip}\item ' + prose(s[2:], refs, i)
            kind = 'bullet'
        else:
            if itemize and s.strip():
                out.append(r'\end{itemize}'); itemize = False
            if s.startswith('#'):
                raise RuntimeError(f'Unhandled heading line {i}')
            emitted = prose(s, refs, i)
            if not s.strip(): kind = 'blank'
        out.append(f'% source-line {i}\n' + emitted)
        records.append({'line': i, 'kind': kind, 'source': s, 'tex': emitted})
    if display:
        raise RuntimeError('Unclosed display')
    for flag, close in ((itemize, 'itemize'), (abstract, 'abstract'), (bibliography, 'thebibliography')):
        if flag: out.append(r'\end{' + close + '}')
    out.extend([r'\end{document}', ''])
    tex = '\n'.join(out)
    # Strip only converter comments before comparing each literal display interior.
    clean_tex = re.sub(r'^% source-line \d+\n', '', tex, flags=re.M)
    sm = re.findall(r'\$\$(.*?)\$\$', source, re.S)
    tm = re.findall(r'\\\[(.*?)\\\]', clean_tex, re.S)
    assert sm == tm, 'Display content changed'
    assert sorted(x['line'] for x in records) == list(range(1, len(lines)+1)), 'Incomplete source line coverage'
    assert headings == re.findall(r'^#{2,3} (.+)$', source, re.M)
    assert refs == body_refs
    urls = re.findall(r'\]\((https?://\S+)\)', source)
    assert urls == re.findall(r'\\href\{([^}]+)\}', tex)
    assert re.findall(r'\\tag\{([^}]+)\}', source) == re.findall(r'\\tag\{([^}]+)\}', tex)
    evidence = {'source_sha256': actual, 'source_lines': len(lines), 'all_source_lines_covered': True,
                'inline_mapping_sha256': MAPPING_SHA256, 'inline_mapping_inventory': MAPPING,
                'inline_replacements': REPLACEMENTS.copy(), 'inverse_prose_chunks': PROSE_ROUNDTRIPS.copy(),
                'all_inline_mapping_inverses_exact': True,
                'display_interiors_byte_equal_after_newline_normalization': len(sm),
                'headings': headings, 'references': refs, 'embedded_urls': urls,
                'equation_tags': re.findall(r'\\tag\{([^}]+)\}', source),
                'tex_sha256': hashlib.sha256(tex.encode()).hexdigest().upper(), 'line_coverage': sorted(records, key=lambda x:x['line'])}
    return tex, evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    tex, evidence = convert()
    if args.check_only:
        assert (PAPER/'main.tex').read_bytes() == tex.encode(), 'TeX is not reproducible'
    else:
        (PAPER/'main.tex').write_text(tex, encoding='utf-8', newline='\n')
        (PAPER/'conversion-check.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k:v for k,v in evidence.items() if k not in ('line_coverage', 'inline_replacements', 'inverse_prose_chunks', 'inline_mapping_inventory')}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
