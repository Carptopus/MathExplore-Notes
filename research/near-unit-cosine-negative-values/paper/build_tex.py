"""Deterministic, hash-gated typesetting of the frozen Markdown manuscript."""
import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'manuscript.md'
EXPECTED = 'CA08ED2E7A386DE14C12140817FF5A067EE74F4B27ED066AA196531FCE61CE43'
PREAMBLE = r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=26mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,microtype,amsmath,amssymb}
\usepackage[colorlinks=true,urlcolor=blue!60!black]{hyperref}
\usepackage{xcolor}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.45em}
\setlength{\emergencystretch}{3em}
\urlstyle{same}
\hypersetup{pdfauthor={Carptopus},pdftitle={Uniform polynomial negative values for trigonometric sums with near-unit coefficients}}
\begin{document}
'''

def prose(s):
    # Protect all original math and URLs before escaping prose.
    parts = re.split(r'(\\\(.*?\\\)|https?://\S+|`[^`]+`)', s)
    out = []
    for p in parts:
        if p.startswith(r'\('):
            out.append(p)
        elif p.startswith('https://'):
            out.append(r'\url{' + p + '}')
        elif p.startswith('`'):
            code = p[1:-1]
            if re.fullmatch(r'[A-F0-9]{64}', code):
                out.append(r'\texttt{' + r'\allowbreak{}'.join(code) + '}')
            else:
                out.append(r'\nolinkurl{' + code + '}')
        else:
            p = p.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_').replace('#', r'\#')
            p = p.replace('^', r'\textasciicircum{}').replace('“', '``').replace('”', "''")
            p = re.sub(r'\*\*(.+?)\*\*', lambda m: r'\textbf{' + m[1] + '}', p)
            p = re.sub(r'\*([^*]+)\*', lambda m: r'\emph{' + m[1] + '}', p)
            out.append(p)
    return ''.join(out)

def main():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest().upper() == EXPECTED, 'frozen source hash mismatch'
    lines = raw.decode('utf-8').splitlines()
    out = [PREAMBLE]
    display = False
    for line in lines:
        if line.strip() in (r'\[', r'\]'):
            display = not display
            out.append(line)
        elif display:
            out.append(line)
        elif line.startswith('# '):
            out.append(r'\title{' + prose(line[2:]) + r'}\author{}\date{}\maketitle')
        elif line.startswith('## '):
            out.append(r'\section*{' + prose(line[3:]) + '}')
            if line == '## References':
                out.append(r'\small\raggedright\setlength{\parskip}{0.3em}')
        else:
            out.append(prose(line))
    assert not display
    out.append(r'\end{document}')
    tex = '\n'.join(out) + '\n'
    # Exact equality of the ordered inline and display math payloads is a conversion guard.
    pattern = r'\\\(.*?\\\)|\\\[.*?\\\]'
    assert re.findall(pattern, raw.decode('utf-8'), re.S) == re.findall(pattern, tex, re.S)
    (HERE / 'main.tex').write_text(tex, encoding='utf-8', newline='\n')
    print('Frozen hash and ordered math-payload identity: PASS')

if __name__ == '__main__':
    main()
