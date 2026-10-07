from __future__ import annotations

import hashlib
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAIN_SOURCE = ROOT / "manuscript.md"
SUPPLEMENT_SOURCE = ROOT / "supplement.md"
MAIN_TARGET = HERE / "main.tex"
SUPPLEMENT_TARGET = HERE / "supplement.tex"
CJK_LABEL = HERE / "audit-packet-cjk.png"
MAIN_SHA256 = "A309E2E1E102B223A208B11CFE713F739EBD8B43EFEB9FD05571F827507F7ABC"
SUPPLEMENT_SHA256 = "0F0BEC99F0F7D78C4980F7D88F32ABCDF5A58E48EE82F8DDA8513C281CD898BF"


COMMON_PACKAGES = r"""\usepackage[a4paper,margin=25mm]{geometry}
\usepackage{microtype}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{graphicx}
\usepackage{needspace}
\usepackage{xcolor}
\usepackage{xurl}
\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=blue!55!black,urlcolor=blue!65!black]{hyperref}
\usepackage{fancyhdr}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{proposition}[theorem]{Proposition}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0.44em}
\setlength{\emergencystretch}{5em}
\setlength{\headheight}{14pt}
\urlstyle{same}
"""


MAIN_PREAMBLE = r"""% Generated deterministically from the frozen Markdown source.
% Responsible author: Carptopus.
\documentclass[11pt]{article}
""" + COMMON_PACKAGES + r"""
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Carptopus}
\fancyhead[R]{Endpoint permanent gates and cycle forests}
\fancyfoot[C]{\thepage}

\title{Endpoint permanent gates and cycle-forest families\\
for the Lih--Wang chord inequality}
\author{Carptopus}
\date{7 October 2026}

\hypersetup{
  pdftitle={Endpoint permanent gates and cycle-forest families for the Lih--Wang chord inequality},
  pdfauthor={Carptopus},
  pdfsubject={Sufficient endpoint criteria and cycle-forest families for the Lih--Wang chord inequality},
  pdfkeywords={permanent, doubly stochastic matrix, row-stochastic matrix, rook polynomial, cycle forest, Bernstein certificate}
}

\begin{document}
\maketitle
\begin{center}
\fcolorbox{black!35}{black!4}{\parbox{0.88\textwidth}{\centering\small
Internal technical draft; not peer reviewed.}}
\end{center}
"""


SUPPLEMENT_PREAMBLE = r"""% Generated deterministically from the frozen Markdown source.
% Responsible author: Carptopus.
\documentclass[11pt]{article}
""" + COMMON_PACKAGES + r"""
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Carptopus}
\fancyhead[R]{Lih--Wang finite certificates}
\fancyfoot[C]{\thepage}

\title{Exact finite certificates for the Lih--Wang\\
endpoint and cycle-family results}
\author{Carptopus}
\date{7 October 2026}

\hypersetup{
  pdftitle={Exact finite certificates for the Lih--Wang endpoint and cycle-family results},
  pdfauthor={Carptopus},
  pdfsubject={Finite exact certificate supplement},
  pdfkeywords={permanent, exact arithmetic, Bernstein certificate, verification supplement}
}

\begin{document}
\maketitle
\begin{center}
\fcolorbox{black!35}{black!4}{\parbox{0.88\textwidth}{\centering\small
Internal supplement; not peer reviewed.}}
\end{center}

This supplement states exactly what each finite computation proves. It is part
of the proof package for the accompanying manuscript. No computation below is a
sample of matrices or parameter values standing in for an unproved continuous
claim.
"""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def escape_text(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    return "".join(replacements.get(char, char) for char in text)


def code_text(text: str) -> str:
    rendered = escape_text(text.replace("\\", "@@BACKSLASH@@"))
    rendered = rendered.replace("@@BACKSLASH@@", r"\textbackslash{}\allowbreak{}")
    rendered = rendered.replace(r"\_", r"\_\allowbreak{}")
    rendered = re.sub(r"([/.-])", lambda match: match.group(1) + r"\allowbreak{}", rendered)
    rendered = rendered.replace(" ", r"\ \allowbreak{}")
    return rendered


def inline(text: str) -> str:
    protected: dict[str, str] = {}

    def keep(value: str) -> str:
        marker = f"@@PROTECTED{len(protected)}@@"
        protected[marker] = value
        return marker

    text = text.replace(
        "A1-写作前审计包.md",
        keep(r"\texttt{A1-}\raisebox{-0.18em}{\includegraphics[height=1.0em]{audit-packet-cjk.png}}\texttt{.md}"),
    )
    text = re.sub(r"\\\((.*?)\\\)", lambda match: keep("$" + match.group(1) + "$"), text)
    text = re.sub(
        r"\[([^]]+)\]\(([^)]+)\)",
        lambda match: keep(
            r"\href{" + ("supplement.pdf" if match.group(2) == "supplement.md" else match.group(2))
            + "}{" + inline(match.group(1)) + "}"
        ),
        text,
    )
    text = re.sub(
        r"`([^`]+)`",
        lambda match: keep(r"\texttt{" + code_text(match.group(1)) + "}"),
        text,
    )
    pieces = re.split(r"(\*[^*]+\*)", text)
    rendered = "".join(
        r"\emph{" + escape_text(piece[1:-1]) + "}"
        if piece.startswith("*") and piece.endswith("*")
        else escape_text(piece)
        for piece in pieces
        if piece
    )
    for marker, value in protected.items():
        rendered = rendered.replace(marker, value)
    return rendered


def convert_main() -> str:
    if sha256(MAIN_SOURCE) != MAIN_SHA256:
        raise RuntimeError(f"frozen main hash mismatch: {sha256(MAIN_SOURCE)}")
    lines = MAIN_SOURCE.read_text(encoding="utf-8").splitlines()
    output = [MAIN_PREAMBLE.rstrip(), ""]
    started = False
    abstract_open = False
    statement_env: str | None = None
    proof_open = False
    list_env: str | None = None
    references = False
    statement_numbers: list[str] = []
    source_displays: list[str] = []

    early_boundaries = {
        ("theorem", "1.1"): "Here ",
        ("corollary", "1.2"): "We next turn to cycle-supported matrices.",
        ("theorem", "1.3"): "The theorem does not include incidence graphs",
    }
    active_statement: tuple[str, str] | None = None

    def close_list() -> None:
        nonlocal list_env
        if list_env:
            output.extend([rf"\end{{{list_env}}}", ""])
            list_env = None

    def close_statement() -> None:
        nonlocal statement_env, active_statement
        close_list()
        if statement_env:
            output.extend([rf"\end{{{statement_env}}}", ""])
            statement_env = None
            active_statement = None

    def close_proof() -> None:
        nonlocal proof_open
        close_list()
        if proof_open:
            output.extend([r"\end{proof}", ""])
            proof_open = False

    i = 0
    while i < len(lines):
        raw = lines[i]
        if raw == "## Abstract":
            started = True
            output.extend([r"\begin{abstract}", ""])
            abstract_open = True
            i += 1
            continue
        if not started:
            i += 1
            continue

        if raw.startswith(r"\["):
            close_list()
            block = [raw]
            while not block[-1].rstrip().endswith(r"\]"):
                i += 1
                if i >= len(lines):
                    raise RuntimeError("unterminated display math")
                block.append(lines[i])
            display = "\n".join(block)
            source_displays.append(display)
            output.extend(block)
            i += 1
            continue

        boundary = early_boundaries.get(active_statement)
        if boundary and raw.startswith(boundary):
            close_statement()

        section = re.match(r"## (\d+)\. (.+)", raw)
        if section:
            close_proof()
            close_statement()
            if abstract_open:
                output.extend([r"\end{abstract}", ""])
                abstract_open = False
            output.extend([rf"\section{{{inline(section.group(2))}}}", ""])
            references = False
            i += 1
            continue

        subsection = re.match(r"### (\d+\.\d+) (.+)", raw)
        if subsection:
            close_proof()
            close_statement()
            output.extend([rf"\subsection{{{inline(subsection.group(2))}}}", ""])
            i += 1
            continue

        if raw == "## References":
            close_proof()
            close_statement()
            output.extend([r"\section*{References}", r"\begin{enumerate}", ""])
            list_env = "enumerate"
            references = True
            i += 1
            continue

        if raw == "## AI-assisted research disclosure":
            close_proof()
            close_statement()
            close_list()
            references = False
            output.extend([r"\section*{AI-assisted research disclosure}", ""])
            i += 1
            continue

        statement = re.match(
            r"### (Theorem|Lemma|Corollary|Proposition) (\d+\.\d+)(?: \((.+)\))?$", raw
        )
        if statement:
            close_proof()
            close_statement()
            kind = statement.group(1).lower()
            number = statement.group(2)
            note = statement.group(3)
            statement_numbers.append(number)
            output.extend([r"\Needspace{0.18\textheight}", rf"\begin{{{kind}}}" + (f"[{inline(note)}]" if note else "")])
            statement_env = kind
            active_statement = (kind, number)
            i += 1
            continue

        if raw == "#### Proof":
            close_statement()
            close_proof()
            output.extend([r"\begin{proof}", ""])
            proof_open = True
            i += 1
            continue

        named_proof = re.match(r"### Proof of (.+)", raw)
        if named_proof:
            close_statement()
            close_proof()
            output.extend([rf"\begin{{proof}}[Proof of {inline(named_proof.group(1))}]", ""])
            proof_open = True
            i += 1
            continue

        if raw.startswith("## ") or raw.startswith("### ") or raw.startswith("#### "):
            raise RuntimeError(f"unhandled heading: {raw}")

        numbered = re.match(r"\d+\. (.+)", raw)
        bullet = re.match(r"- (.+)", raw)
        if numbered or bullet:
            wanted = "enumerate" if numbered else "itemize"
            if list_env != wanted:
                close_list()
                output.append(rf"\begin{{{wanted}}}")
                list_env = wanted
            item = numbered.group(1) if numbered else bullet.group(1)
            output.append(r"\item " + inline(item))
            i += 1
            continue
        if list_env and raw == "" and not references:
            close_list()
            i += 1
            continue

        proof_end = raw.rstrip().endswith(r"\(\square\)")
        content = raw.rstrip()
        if proof_end:
            content = content[: -len(r"\(\square\)")].rstrip()
        output.append(inline(content))
        if proof_end:
            if proof_open:
                close_proof()
            else:
                output.extend([r"\hfill$\square$", ""])
        i += 1

    close_proof()
    close_statement()
    close_list()
    if abstract_open:
        output.extend([r"\end{abstract}", ""])
    expected = ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "4.1", "4.2", "5.1"]
    if statement_numbers != expected:
        raise RuntimeError(f"unexpected statement sequence: {statement_numbers}")
    rendered = "\n".join(output + [r"\end{document}", ""])
    for display in source_displays:
        if display not in rendered:
            raise RuntimeError("display-math fidelity failure")
    source_tags = re.findall(r"\\tag\{([^}]+)\}", MAIN_SOURCE.read_text(encoding="utf-8"))
    target_tags = re.findall(r"\\tag\{([^}]+)\}", rendered)
    if source_tags != target_tags:
        raise RuntimeError("equation tag sequence changed")
    return rendered


def convert_supplement() -> str:
    if sha256(SUPPLEMENT_SOURCE) != SUPPLEMENT_SHA256:
        raise RuntimeError(f"frozen supplement hash mismatch: {sha256(SUPPLEMENT_SOURCE)}")
    lines = SUPPLEMENT_SOURCE.read_text(encoding="utf-8").splitlines()
    output = [SUPPLEMENT_PREAMBLE.rstrip(), ""]
    started = False
    list_open = False
    i = 0
    while i < len(lines):
        raw = lines[i]
        if raw.startswith("## "):
            if list_open:
                output.extend([r"\end{itemize}", ""])
                list_open = False
            heading = re.sub(r"^## \d+\. ", "", raw)
            output.extend([rf"\section{{{inline(heading)}}}", ""])
            started = True
            i += 1
            continue
        if not started:
            i += 1
            continue
        bullet = re.match(r"- (.+)", raw)
        if bullet:
            if not list_open:
                output.append(r"\begin{itemize}")
                list_open = True
            output.append(r"\item " + inline(bullet.group(1)))
            i += 1
            continue
        if list_open and raw == "":
            output.extend([r"\end{itemize}", ""])
            list_open = False
            i += 1
            continue
        if raw.startswith("    ") or re.fullmatch(r"\s*[0-9A-Fa-f]{64}[.;]?", raw):
            output.append(r"\noindent{\scriptsize\ttfamily\raggedright\sloppy " + code_text(raw.strip()) + r"\par}")
        else:
            output.append(inline(raw))
        i += 1
    if list_open:
        output.extend([r"\end{itemize}", ""])
    return "\n".join(output + [r"\end{document}", ""])


def main() -> None:
    font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 42)
    label = "写作前审计包"
    left, top, right, bottom = font.getbbox(label)
    image = Image.new("RGBA", (right - left + 8, bottom - top + 8), (255, 255, 255, 0))
    ImageDraw.Draw(image).text((4 - left, 4 - top), label, font=font, fill=(0, 0, 0, 255))
    image.save(CJK_LABEL)
    MAIN_TARGET.write_text(convert_main(), encoding="utf-8", newline="\n")
    SUPPLEMENT_TARGET.write_text(convert_supplement(), encoding="utf-8", newline="\n")
    print(MAIN_TARGET)
    print(SUPPLEMENT_TARGET)


if __name__ == "__main__":
    main()
