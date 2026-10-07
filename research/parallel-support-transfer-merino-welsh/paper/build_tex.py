from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

# Adapted mechanically from Merino-Welsh-Parallel-Support/paper/build_tex.py.
# Preserve source numbering and literal mathematics; never infer theorem boundaries.
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript.md"
TARGET = Path(__file__).resolve().parent / "main.tex"
SOURCE_SHA256 = "11DE5F36F58138091B033578A0780E72E8F620BB9E32BCB7B6135899B65D991F"
PREAMBLE = r"""% Deterministically converted from the hash-pinned manuscript.
\documentclass[11pt]{article}
\usepackage[a4paper,margin=27mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,microtype,amsmath,amssymb,mathtools,needspace,xcolor}
\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=blue!55!black,urlcolor=blue!65!black]{hyperref}
\usepackage{xurl,fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Carptopus}
\fancyhead[R]{Parallel-support transfer}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.44em}
\setlength{\emergencystretch}{4em}
\urlstyle{same}
"""


def escape(text: str) -> str:
    table = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
             "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
             "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
             "∎": r"\hfill\(\square\)", "–": "--", "—": "---",
             "·": r"\textperiodcentered{}"}
    return "".join(table.get(char, char) for char in text)


def prose(text: str, citations: bool = True) -> str:
    # URLs, emphasis, inline code and bracket citations are isolated before escaping.
    tokens = re.split(r"(https?://\S+|\*[^*]+\*|`[^`]+`|\[[1-7](?:, [^\]]+)?\])", text)
    output = []
    for token in tokens:
        if token.startswith(("https://", "http://")):
            output.append(r"\url{" + token + "}")
        elif token.startswith("*") and token.endswith("*"):
            output.append(r"\emph{" + escape(token[1:-1]) + "}")
        elif token.startswith("`") and token.endswith("`"):
            output.append(r"\texttt{" + escape(token[1:-1]) + "}")
        elif citations and re.fullmatch(r"\[[1-7](?:, [^\]]+)?\]", token):
            output.append(r"\hyperlink{ref" + token[1] + "}{" + escape(token) + "}")
        else:
            output.append(escape(token))
    return "".join(output)


def inline(text: str, citations: bool = True) -> str:
    return "".join(part if part.startswith(r"\(") else prose(part, citations)
                   for part in re.split(r"(\\\(.*?\\\))", text))


def convert() -> tuple[str, dict]:
    data = SOURCE.read_bytes()
    actual = hashlib.sha256(data).hexdigest().upper()
    if actual != SOURCE_SHA256:
        raise RuntimeError(f"Frozen source hash mismatch: {actual}")
    source = data.decode("utf-8")
    lines = source.splitlines()
    nonblank = [line for line in lines if line.strip()]
    title, author, date, status = nonblank[:4]
    if not title.startswith("# ") or author != "Carptopus":
        raise RuntimeError("Unexpected frozen title/author header")
    output = [PREAMBLE.rstrip(), r"\title{" + inline(title[2:]) + "}",
              r"\author{" + inline(author) + "}", r"\date{" + inline(date) + "}",
              r"\hypersetup{pdfauthor={Carptopus},pdftitle={" + escape(title[2:]) + "}}",
              r"\begin{document}", r"\maketitle", r"\begin{center}",
              inline(status), r"\end{center}", ""]
    started = abstract = display = bibliography = False
    refs, headings = [], []
    consumed = []
    for number, raw in enumerate(lines, 1):
        if raw == "## Abstract":
            started = abstract = True
            output.append(r"\begin{abstract}")
            consumed.append(number)
            continue
        if not started:
            continue
        consumed.append(number)
        if raw == r"\[":
            if display:
                raise RuntimeError(f"Nested display at line {number}")
            display = True
            output.append(raw)
            continue
        if display:
            output.append(raw)
            if raw == r"\]":
                display = False
            continue
        if raw.startswith("## "):
            if abstract:
                output.append(r"\end{abstract}")
                abstract = False
            heading = raw[3:]
            headings.append(heading)
            if heading == "References":
                bibliography = True
                output.extend([r"\begin{thebibliography}{9}", r"\small\raggedright"])
            else:
                output.append(r"\section*{" + inline(heading) + "}")
            continue
        if raw.startswith("### "):
            heading = raw[4:]
            headings.append(heading)
            output.extend([r"\Needspace{5\baselineskip}",
                           r"\subsection*{" + inline(heading) + "}"])
            continue
        if raw.startswith("#"):
            raise RuntimeError(f"Unhandled heading at line {number}: {raw}")
        if bibliography and raw.strip():
            match = re.fullmatch(r"\[([1-7])\] (.+)", raw)
            if not match:
                raise RuntimeError(f"Unhandled reference at line {number}")
            refs.append(int(match[1]))
            output.append(r"\bibitem{ref" + match[1] + "}" +
                          r"\hypertarget{ref" + match[1] + "}{}" + inline(match[2], False))
        else:
            output.append(inline(raw))
    if display or abstract or not bibliography or refs != list(range(1, 8)):
        raise RuntimeError("Incomplete document structure or reference inventory")
    output.extend([r"\end{thebibliography}", r"\end{document}", ""])
    tex = "\n".join(output)
    # Exact equality, in sequence, for every inline/display mathematical expression.
    math_pattern = r"\\\(.*?\\\)|\\\[.*?\\\]"
    source_math = re.findall(math_pattern, source, re.S)
    tex_math = re.findall(math_pattern, tex, re.S)
    # The proof-ending square is typography, not part of the mathematical source.
    tex_math = [item for item in tex_math if item != r"\(\square\)"]
    if source_math != tex_math:
        raise RuntimeError("Mathematical expression conversion changed source content")
    tags = re.findall(r"\\tag\{(\d+)\}", source)
    if tags != [str(i) for i in range(1, 20)]:
        raise RuntimeError(f"Unexpected equation tag sequence: {tags}")
    evidence = {"source_sha256": actual, "source_lines": len(lines),
                "converted_body_lines": len(consumed), "math_expressions_exact": len(source_math),
                "equation_tags": tags, "headings": headings, "references": refs,
                "status": status, "tex_sha256": hashlib.sha256(tex.encode()).hexdigest().upper()}
    return tex, evidence


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="Validate in memory; write no TeX/PDF")
    args = parser.parse_args()
    tex, evidence = convert()
    if not args.check_only:
        TARGET.write_text(tex, encoding="utf-8", newline="\n")
        evidence["target"] = str(TARGET)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
