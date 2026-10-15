from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript.md"
TARGET = Path(__file__).resolve().parent / "main.tex"
SOURCE_SHA256 = "A7B55C458A30CAD0B8DF11BDF643788113F8C6D35FE046067E2499DF38245B2B"


PREAMBLE = r"""% Generated deterministically from the frozen Markdown source.
% Responsible author: Carptopus.
\documentclass[11pt]{article}
\usepackage[a4paper,margin=25mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{xcolor}
\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=blue!55!black,urlcolor=blue!65!black]{hyperref}
\usepackage{xurl}
\usepackage{fancyhdr}
\usepackage{enumitem}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Carptopus}
\fancyhead[R]{Arithmetic symmetric modulus: phase diagram}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.42em}
\setlength{\emergencystretch}{5em}
\setlist{nosep,leftmargin=2em}
\urlstyle{same}

\title{Sharp Schatten constants for the arithmetic symmetric modulus:\\dimension two and rank-two strata}
\author{Carptopus\\\href{mailto:carptopus@163.com}{carptopus@163.com}}
\date{Public Beta preprint, version 0.1-beta, 15 October 2026}

\hypersetup{
  pdftitle={Sharp Schatten constants for the arithmetic symmetric modulus: dimension two and rank-two strata},
  pdfauthor={Carptopus},
  pdfsubject={Sharp Schatten constants and low-rank strata for the arithmetic symmetric modulus},
  pdfkeywords={operator symmetric modulus, Schatten norm, sharp triangle inequality, low-rank matrix inequality, phase diagram}
}

\begin{document}
\maketitle

\begin{center}
\fcolorbox{black!35}{black!4}{\parbox{0.88\textwidth}{\centering\small
Public Beta preprint, version 0.1-beta, 15 October 2026. The frozen theorem
package and the complete manuscript have passed separate internal project
reviews. External mathematical review and formal peer review have not been
completed.}}
\end{center}
"""


BIBLIOGRAPHY = r"""
\begin{thebibliography}{9}
\footnotesize
\raggedright

\bibitem{bourin-lee}
Jean-Christophe Bourin and Eun-Young Lee,
\emph{Triangle inequalities for the operator symmetric modulus},
arXiv:2602.19607v1, 23 February 2026;
\emph{Proceedings of the American Mathematical Society} (2026),
DOI 10.1090/proc/17861.
\url{https://doi.org/10.1090/proc/17861}

\bibitem{zhang}
Teng Zhang,
\emph{Operator symmetric moduli and sharp triangle inequalities},
arXiv:2603.01046v1, 1 March 2026; \emph{Journal of the London Mathematical Society}
\textbf{114}(2) (2026), e70672.
\url{https://doi.org/10.1112/jlms.70672}

\bibitem{mi09}
Open Problems in Numerical Linear Algebra, MI-09,
\emph{Arithmetic symmetric modulus: optimal constants for Schatten norms},
public problem record, accessed 14 October 2026.
\url{https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/matrix-inequalities-and-norms/MI-09}

\bibitem{horn}
Alfred Horn,
\emph{Doubly stochastic matrices and the diagonal of a rotation matrix},
\emph{American Journal of Mathematics} \textbf{76} (1954), 620--630.
\url{https://doi.org/10.2307/2372705}

\bibitem{xia-wang-sheu}
Yong Xia, Shu Wang, and Ruey-Lin Sheu,
\emph{S-lemma with equality and its applications},
\emph{Mathematical Programming} \textbf{156} (2016), 513--547.
\url{https://doi.org/10.1007/s10107-015-0907-0}

\bibitem{bourin-lee-hybrid}
Jean-Christophe Bourin and Eun-Young Lee,
\emph{Some hybrid matrix triangle inequalities},
arXiv:2606.29188v1, 28 June 2026.
\url{https://arxiv.org/abs/2606.29188}

\bibitem{aouichaoui-lee}
Mohamed Amine Aouichaoui and Eun-Young Lee,
\emph{Solutions to some open problems in matrix analysis},
arXiv:2609.20094v2, 21 September 2026.
\url{https://arxiv.org/abs/2609.20094}

\end{thebibliography}

\end{document}
"""


CITATIONS = {
    "[1]": r"\cite{bourin-lee}",
    "[2]": r"\cite{zhang}",
    "[3]": r"\cite{mi09}",
    "[4]": r"\cite{horn}",
    "[5]": r"\cite{xia-wang-sheu}",
    "[6]": r"\cite{bourin-lee-hybrid}",
    "[7]": r"\cite{aouichaoui-lee}",
}

STATEMENTS = {
    ("Theorem", "1.1"): ("theorem", "thm:dimension-two"),
    ("Corollary", "1.2"): ("corollary", "cor:frobenius-two"),
    ("Theorem", "1.3"): ("theorem", "thm:rank-two-frobenius"),
    ("Theorem", "1.4"): ("theorem", "thm:subquadratic-separation"),
    ("Theorem", "1.5"): ("theorem", "thm:cubic-strata"),
    ("Proposition", "2.1"): ("proposition", "prop:balanced-block"),
    ("Lemma", "3.1"): ("lemma", "lem:spectral-gate"),
    ("Proposition", "4.1"): ("proposition", "prop:balanced-optimal"),
    ("Lemma", "6.1"): ("lemma", "lem:frobenius-outer"),
    ("Proposition", "7.1"): ("proposition", "prop:superquadratic-chain"),
    ("Lemma", "8.1"): ("lemma", "lem:cubic-single-edge"),
}

NAMED_REFERENCES = {
    f"{kind} {number}": rf"{kind}~\ref{{{label}}}"
    for (kind, number), (_, label) in STATEMENTS.items()
}


def replace_prose(text: str) -> str:
    for source in sorted(NAMED_REFERENCES, key=len, reverse=True):
        text = text.replace(source, NAMED_REFERENCES[source])
    for source, replacement in CITATIONS.items():
        text = text.replace(source, replacement)
    text = re.sub(
        r"\((\d+\.\d+)\)",
        lambda match: rf"\eqref{{eq:{match.group(1)}}}",
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", lambda match: rf"\textbf{{{match.group(1)}}}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda match: rf"\emph{{{match.group(1)}}}", text)
    return text


def inline(text: str) -> str:
    parts = re.split(r"(\$[^$]*\$)", text)
    for index in range(0, len(parts), 2):
        parts[index] = replace_prose(parts[index])
    return "".join(parts)


def convert() -> str:
    source_bytes = SOURCE.read_bytes()
    actual_hash = hashlib.sha256(source_bytes).hexdigest().upper()
    if actual_hash != SOURCE_SHA256:
        raise RuntimeError(
            f"frozen source hash mismatch: expected {SOURCE_SHA256}, got {actual_hash}"
        )

    output: list[str] = [PREAMBLE.rstrip(), ""]
    started = False
    abstract_open = False
    display_open = False
    list_env: str | None = None
    statement_env: str | None = None
    proof_open = False
    seen_statements: set[tuple[str, str]] = set()
    seen_equations: set[str] = set()

    def close_list() -> None:
        nonlocal list_env
        if list_env:
            output.extend([rf"\end{{{list_env}}}", ""])
            list_env = None

    def open_list(environment: str) -> None:
        nonlocal list_env
        if list_env != environment:
            close_list()
            output.append(rf"\begin{{{environment}}}")
            list_env = environment

    def close_statement() -> None:
        nonlocal statement_env
        close_list()
        if statement_env:
            output.extend([rf"\end{{{statement_env}}}", ""])
            statement_env = None

    def close_proof() -> None:
        nonlocal proof_open
        close_list()
        if proof_open:
            output.extend([r"\end{proof}", ""])
            proof_open = False

    def close_structures() -> None:
        close_proof()
        close_statement()

    for raw in source_bytes.decode("utf-8").splitlines():
        if raw == "## References":
            close_structures()
            if abstract_open:
                output.extend([r"\end{abstract}", ""])
                abstract_open = False
            break

        if raw == "## Abstract":
            started = True
            abstract_open = True
            output.extend([r"\begin{abstract}", ""])
            continue
        if not started:
            continue

        if raw.strip() == "$$":
            close_list()
            output.append(r"\]" if display_open else r"\[")
            display_open = not display_open
            continue

        if display_open:
            math_line = raw.strip()
            math_line = re.sub(
                r"\\tag\{(\d+\.\d+)\}",
                lambda match: rf"\tag{{{match.group(1)}}}\label{{eq:{match.group(1)}}}",
                math_line,
            )
            tag_match = re.search(r"\\tag\{(\d+\.\d+)\}", raw)
            if tag_match:
                seen_equations.add(tag_match.group(1))
            output.append(math_line)
            continue

        section_match = re.fullmatch(r"## (\d+)\. (.+)", raw)
        if section_match:
            close_structures()
            if abstract_open:
                output.extend([r"\end{abstract}", ""])
                abstract_open = False
            output.extend([rf"\section{{{inline(section_match.group(2))}}}", ""])
            continue

        if raw == "## AI-assisted research and writing":
            close_structures()
            output.extend([r"\section*{AI-assisted research and writing}", ""])
            continue

        statement_match = re.fullmatch(
            r"\*\*(Theorem|Corollary|Proposition|Lemma) (\d+\.\d+)\.\*\*(.*)", raw
        )
        if statement_match:
            close_structures()
            key = (statement_match.group(1), statement_match.group(2))
            if key not in STATEMENTS:
                raise RuntimeError(f"unexpected statement: {raw}")
            statement_env, label = STATEMENTS[key]
            seen_statements.add(key)
            output.extend([rf"\begin{{{statement_env}}}", rf"\label{{{label}}}"])
            remainder = statement_match.group(3).strip()
            if remainder:
                output.append(inline(remainder))
            continue

        proof_match = re.fullmatch(r"\*\*(Proof(?: of .+?)?)\.\*\*(.*)", raw)
        if proof_match:
            close_statement()
            close_proof()
            heading = proof_match.group(1)
            output.append(r"\begin{proof}" if heading == "Proof" else rf"\begin{{proof}}[{inline(heading)}]")
            proof_open = True
            remainder = proof_match.group(2).strip()
            if remainder:
                output.append(inline(remainder))
            continue

        if raw.startswith("## "):
            raise RuntimeError(f"unhandled heading: {raw}")

        numbered = re.match(r"\d+\. (.+)", raw)
        bullet = re.match(r"- (.+)", raw)
        if numbered:
            open_list("enumerate")
            output.append(rf"\item {inline(numbered.group(1))}")
            continue
        if bullet:
            open_list("itemize")
            output.append(rf"\item {inline(bullet.group(1))}")
            continue

        if list_env and re.match(r"^\s{2,}\S", raw):
            output.append(inline(raw.strip()))
            continue
        if list_env and raw.strip():
            close_list()

        proof_end = raw.rstrip().endswith("∎")
        content = raw.rstrip()
        if proof_end:
            content = content[:-1].rstrip()
        output.append(inline(content))
        if proof_end:
            if not proof_open:
                raise RuntimeError("proof terminator encountered outside a proof")
            close_proof()

    if display_open:
        raise RuntimeError("unclosed display math")
    close_structures()
    missing_statements = set(STATEMENTS) - seen_statements
    if missing_statements:
        raise RuntimeError(f"missing statement headings: {sorted(missing_statements)}")
    source_tags = set(re.findall(rb"\\tag\{(\d+\.\d+)\}", source_bytes))
    expected_tags = {tag.decode("ascii") for tag in source_tags}
    if seen_equations != expected_tags:
        raise RuntimeError(
            f"equation tag mismatch: expected {sorted(expected_tags)}, got {sorted(seen_equations)}"
        )
    output.extend([BIBLIOGRAPHY.strip(), ""])
    return "\n".join(output)


def main() -> None:
    TARGET.write_text(convert(), encoding="utf-8", newline="\n")
    print(TARGET)


if __name__ == "__main__":
    main()
