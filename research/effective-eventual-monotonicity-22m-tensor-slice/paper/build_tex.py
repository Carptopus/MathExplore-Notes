from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript.md"
TARGET = Path(__file__).resolve().parent / "main.tex"
SOURCE_SHA256 = "6C3147DC9B976721C1706B1A380A6EC0D4E12F943CCC762CD28DF2E2D849E260"

PREAMBLE = r"""% Deterministically converted from the hash-pinned frozen manuscript.
% Responsible human author: Carptopus.
\documentclass[11pt]{article}
\usepackage[a4paper,margin=25mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,microtype}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{needspace,xcolor,xurl,fancyhdr}
\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=blue!55!black,urlcolor=blue!65!black]{hyperref}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Carptopus}
\fancyhead[R]{Effective eventual monotonicity}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.42em}
\setlength{\emergencystretch}{4em}
\urlstyle{same}
\allowdisplaybreaks[1]
"""

DISCLOSURE = (
    "Carptopus is the sole author and is responsible for the mathematical claims, "
    "source attribution, revisions, and any public version of this manuscript. "
    "OpenAI Codex was used as an AI-assisted research and writing tool for literature "
    "organization, proof exploration, exact and interval verification, adversarial "
    "auditing, artifact generation, and manuscript drafting. Codex is not an author "
    "or responsible author."
)

EXPECTED_STATEMENTS = [
    ("Theorem", "1.1"),
    ("Proposition", "2.1"),
    ("Theorem", "2.2"),
    ("Lemma", "4.1"),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "–": "--",
        "—": "---",
        "ţ": r"\c{t}",
    }
    return "".join(replacements.get(character, character) for character in text)


TOKEN_RE = re.compile(
    r"(\$[^$\n]+\$|<https?://[^>]+>|`[^`]+`|\*[^*]+\*|\[[1-6](?:,[^\]]+)?\])"
)


def inline(text: str, citations: bool = True) -> str:
    output: list[str] = []
    for token in TOKEN_RE.split(text):
        if not token:
            continue
        if token.startswith("$") and token.endswith("$"):
            output.append(token)
        elif token.startswith("<http") and token.endswith(">"):
            output.append(r"\url{" + token[1:-1] + "}")
        elif token.startswith("`") and token.endswith("`"):
            output.append(r"\texttt{" + escape(token[1:-1]) + "}")
        elif token.startswith("*") and token.endswith("*"):
            output.append(r"\emph{" + escape(token[1:-1]) + "}")
        elif citations and re.fullmatch(r"\[[1-6](?:,[^\]]+)?\]", token):
            first = re.match(r"\[(\d)", token)
            assert first is not None
            output.append(r"\hyperlink{ref" + first.group(1) + "}{" + escape(token) + "}")
        else:
            output.append(escape(token))
    return "".join(output)


def source_math_inventory(source: str) -> list[str]:
    displays = re.findall(r"^\$\$\s*\n(.*?)\n\$\$\s*$", source, re.M | re.S)
    without_displays = re.sub(r"^\$\$\s*\n.*?\n\$\$\s*$", "", source, flags=re.M | re.S)
    inline_math = re.findall(r"\$([^$\n]+)\$", without_displays)
    inventory: list[tuple[int, str]] = []
    for match in re.finditer(r"^\$\$\s*\n(.*?)\n\$\$\s*$", source, re.M | re.S):
        inventory.append((match.start(), match.group(1)))
    for match in re.finditer(r"\$([^$\n]+)\$", without_displays):
        inventory.append((match.start(), match.group(1)))
    # The two scans above use different coordinate strings, so ordering is checked
    # independently below by the converter. Counts and literal content are the gate.
    return displays + inline_math


def convert() -> tuple[str, dict[str, object]]:
    source_bytes = SOURCE.read_bytes()
    actual_hash = sha256_bytes(source_bytes)
    if actual_hash != SOURCE_SHA256:
        raise RuntimeError(
            f"Frozen source hash mismatch: expected {SOURCE_SHA256}, got {actual_hash}"
        )
    source = source_bytes.decode("utf-8")
    lines = source.splitlines()
    if lines[:8] != [
        "# Effective eventual monotonicity on the $(2,2,m)$ tensor slice",
        "",
        "Carptopus  ",
        "carptopus@163.com",
        "",
        "Draft date: 14 October 2026",
        "",
        "Status: manuscript candidate; proof audited internally; not peer reviewed",
    ]:
        raise RuntimeError("Unexpected frozen title, author, date, or status header")

    output = [
        PREAMBLE.rstrip(),
        r"\title{Effective eventual monotonicity on the $(2,2,m)$ tensor slice}",
        r"\author{Carptopus\\\href{mailto:carptopus@163.com}{carptopus@163.com}}",
        r"\date{14 October 2026}",
        r"\hypersetup{pdfauthor={Carptopus},pdftitle={Effective eventual monotonicity on the (2,2,m) tensor slice}}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{center}",
        r"\fcolorbox{black!35}{black!4}{\parbox{0.86\textwidth}{\centering\small Internal proof audit passed. External peer review has not been completed.}}",
        r"\end{center}",
        "",
    ]

    headings: list[str] = []
    statements: list[tuple[str, str]] = []
    references: list[int] = []
    display_math: list[str] = []
    # The title is the only inline-math expression before the Abstract body.
    inline_math: list[str] = ["(2,2,m)"]
    aligned_tag_rewrites: list[str] = []
    abstract_open = False
    statement_open: str | None = None
    proof_open = False
    list_open = False
    bibliography = False

    def close_statement() -> None:
        nonlocal statement_open
        if statement_open:
            output.extend([rf"\end{{{statement_open}}}", ""])
            statement_open = None

    def close_proof() -> None:
        nonlocal proof_open
        if proof_open:
            output.extend([r"\end{proof}", ""])
            proof_open = False

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            output.extend([r"\end{enumerate}", ""])
            list_open = False

    index = 8
    while index < len(lines):
        raw = lines[index]

        if raw == "## References":
            close_list()
            close_proof()
            close_statement()
            if abstract_open:
                output.extend([r"\end{abstract}", ""])
                abstract_open = False
            output.extend([
                r"\section*{AI-assisted research and writing disclosure}",
                inline(DISCLOSURE),
                "",
                r"\begin{thebibliography}{9}",
                r"\small\raggedright",
            ])
            headings.append("References")
            bibliography = True
            index += 1
            continue

        if bibliography:
            if not raw.strip():
                index += 1
                continue
            match = re.match(r"\[([1-6])\] (.+)", raw)
            if not match:
                raise RuntimeError(f"Unexpected bibliography line {index + 1}: {raw}")
            number = int(match.group(1))
            parts = [match.group(2).strip()]
            index += 1
            while index < len(lines) and lines[index].strip() and not re.match(r"\[[1-6]\] ", lines[index]):
                parts.append(lines[index].strip())
                index += 1
            references.append(number)
            output.extend([
                rf"\bibitem{{ref{number}}}\hypertarget{{ref{number}}}{{}}" + inline(" ".join(parts), False),
                "",
            ])
            continue

        if not raw.strip():
            index += 1
            continue

        if raw == "## Abstract":
            output.extend([r"\begin{abstract}", ""])
            abstract_open = True
            headings.append("Abstract")
            index += 1
            continue

        section_match = re.fullmatch(r"## (\d+)\. (.+)", raw)
        if section_match:
            close_list()
            close_proof()
            close_statement()
            if abstract_open:
                output.extend([r"\end{abstract}", ""])
                abstract_open = False
            output.extend([r"\section{" + inline(section_match.group(2)) + "}", ""])
            headings.append(raw[3:])
            index += 1
            continue

        subsection_match = re.fullmatch(r"### (\d+\.\d+)\. (.+)", raw)
        if subsection_match:
            close_list()
            close_proof()
            close_statement()
            output.extend([r"\subsection{" + inline(subsection_match.group(2)) + "}", ""])
            headings.append(raw[4:])
            index += 1
            continue

        statement_match = re.fullmatch(r"### (Theorem|Proposition|Lemma) (\d+\.\d+)", raw)
        if statement_match:
            close_list()
            close_proof()
            close_statement()
            kind, number = statement_match.groups()
            environment = kind.lower()
            output.extend([r"\Needspace{5\baselineskip}", rf"\begin{{{environment}}}"])
            statement_open = environment
            statements.append((kind, number))
            headings.append(raw[4:])
            index += 1
            continue

        if raw == "#### Proof":
            close_list()
            close_statement()
            close_proof()
            output.append(r"\begin{proof}")
            proof_open = True
            headings.append("Proof")
            index += 1
            continue

        if raw.startswith("#"):
            raise RuntimeError(f"Unhandled heading at line {index + 1}: {raw}")

        if raw == "$$":
            close_list()
            math_lines: list[str] = []
            index += 1
            while index < len(lines) and lines[index] != "$$":
                math_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise RuntimeError("Unclosed display mathematics")
            content = "\n".join(math_lines)
            display_math.append(content)
            rendered_content = re.sub(
                r"(?m)^(.*?)(\s*\\tag\{([^}]+)\})\s*\n(\\end\{aligned\})$",
                lambda match: (
                    match.group(1).rstrip()
                    + "\n"
                    + match.group(4)
                    + "                                      "
                    + match.group(2).strip()
                ),
                content,
            )
            if rendered_content != content:
                aligned_tag_rewrites.extend(re.findall(r"\\tag\{([^}]+)\}", content))
            output.extend([r"\[", rendered_content, r"\]", ""])
            index += 1
            continue

        list_match = re.match(r"(\d+)\. (.+)", raw)
        if list_match:
            if not list_open:
                output.append(r"\begin{enumerate}")
                list_open = True
            parts = [list_match.group(2).strip()]
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if not candidate.strip() or re.match(r"\d+\. ", candidate) or candidate.startswith("#") or candidate == "$$":
                    break
                parts.append(candidate.strip())
                index += 1
            paragraph = " ".join(parts)
            inline_math.extend(re.findall(r"\$([^$\n]+)\$", paragraph))
            output.append(r"\item " + inline(paragraph))
            continue

        close_list()
        paragraph_lines = [raw.strip()]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if (
                not candidate.strip()
                or candidate.startswith("#")
                or candidate == "$$"
                or re.match(r"\d+\. ", candidate)
                or (bibliography and re.match(r"\[[1-6]\] ", candidate))
            ):
                break
            paragraph_lines.append(candidate.strip())
            index += 1
        paragraph = " ".join(paragraph_lines)

        if statement_open == "theorem" and statements[-1] == ("Theorem", "1.1") and paragraph.startswith("The theorem leaves"):
            close_statement()

        proof_end = paragraph.endswith("∎")
        if proof_end:
            paragraph = paragraph[:-1].rstrip()
        inline_math.extend(re.findall(r"\$([^$\n]+)\$", paragraph))
        output.extend([inline(paragraph), ""])
        if proof_end:
            if proof_open:
                close_proof()
            else:
                # Section 6 is itself titled "Proof of the main theorem" in the
                # frozen source, so its terminal square is not inside a Markdown
                # #### Proof block.
                output.extend([r"\hfill$\square$", ""])

    close_list()
    close_proof()
    close_statement()
    if abstract_open:
        output.extend([r"\end{abstract}", ""])
    if references != list(range(1, 7)):
        raise RuntimeError(f"Unexpected reference sequence: {references}")
    if statements != EXPECTED_STATEMENTS:
        raise RuntimeError(f"Unexpected statement sequence: {statements}")
    if not bibliography:
        raise RuntimeError("References heading not found")
    output.extend([r"\end{thebibliography}", r"\end{document}", ""])
    tex = "\n".join(output)

    source_displays = re.findall(r"^\$\$\s*\n(.*?)\n\$\$\s*$", source, re.M | re.S)
    source_without_displays = re.sub(r"^\$\$\s*\n.*?\n\$\$\s*$", "", source, flags=re.M | re.S)
    source_inlines = re.findall(r"\$([^$\n]+)\$", source_without_displays)
    if display_math != source_displays:
        raise RuntimeError("Display mathematics changed or reordered")
    if inline_math != source_inlines:
        raise RuntimeError("Inline mathematics changed or reordered")
    tags = re.findall(r"\\tag\{(\d+\.\d+)\}", source)
    if tags != [
        "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9",
        "3.1", "3.2", "3.3", "3.4", "3.5", "4.1", "4.2", "4.3", "4.4",
        "4.5", "4.6", "4.7", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6",
        "5.7", "5.8", "5.9", "5.10", "5.11", "5.12", "5.13", "5.14",
        "5.15", "5.16", "5.17", "5.18", "6.1", "6.2", "6.3",
    ]:
        raise RuntimeError(f"Unexpected equation tag sequence: {tags}")
    if aligned_tag_rewrites != ["4.4", "5.9"]:
        raise RuntimeError(f"Unexpected aligned-tag layout rewrites: {aligned_tag_rewrites}")
    markdown_markers = re.findall(r"(?m)^(?:#{1,4} |\$\$|```)|(?<!\\)`|<https?://", tex)
    if markdown_markers:
        raise RuntimeError(f"Markdown leakage detected: {markdown_markers[:5]}")

    evidence: dict[str, object] = {
        "source_sha256": actual_hash,
        "source_lines": len(lines),
        "display_math_exact": len(display_math),
        "inline_math_exact": len(inline_math),
        "equation_tags": tags,
        "aligned_tag_layout_rewrites": aligned_tag_rewrites,
        "statements": [f"{kind} {number}" for kind, number in statements],
        "headings": headings,
        "references": references,
        "status_text": "Internal proof audit passed. External peer review has not been completed.",
        "tex_sha256": sha256_bytes(tex.encode("utf-8")),
    }
    return tex, evidence


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="Validate conversion without writing main.tex")
    args = parser.parse_args()
    tex, evidence = convert()
    if not args.check_only:
        TARGET.write_text(tex, encoding="utf-8", newline="\n")
        evidence["target"] = str(TARGET)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
