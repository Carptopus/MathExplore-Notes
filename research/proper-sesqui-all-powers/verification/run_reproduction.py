"""Offline one-entry reproduction for the public verification materials."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DATA = ROOT / "data"
RESULTS = ROOT / "results"


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script: str, arguments: list[str]) -> dict[str, object]:
    command = [sys.executable, str(SRC / script), *arguments]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed: {script} {' '.join(arguments)}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return {
        "script": f"src/{script}",
        "arguments": arguments,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout.strip()[-500:],
        "stderr_tail": completed.stderr.strip()[-500:],
    }


def scan_private_paths(paths: list[Path]) -> None:
    forbidden = [
        "D:" + "\\Codes\\",
        "E:" + "\\Documents\\",
        "Z:" + "\\TEMP\\",
        "C:" + "\\Users\\",
        "Admin" + "istrator",
    ]
    text_suffixes = {".md", ".py", ".json", ".txt"}
    for path in paths:
        if path.suffix.lower() not in text_suffixes:
            continue
        text = path.read_text(encoding="utf-8")
        normalized = text.replace("/", "\\").lower()
        while "\\\\" in normalized:
            normalized = normalized.replace("\\\\", "\\")
        for fragment in forbidden:
            if fragment.lower() in normalized:
                raise AssertionError(
                    f"private path fragment {fragment!r} found in {relative(path)}"
                )


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    generated = {
        "inverse_pair": RESULTS / "inverse-pair-independent.json",
        "subiaco_bridge": RESULTS / "subiaco-bridge.json",
        "cubic_sum": RESULTS / "subiaco-cubic-sum.json",
        "zero_anchor": RESULTS / "zero-anchor-resultants.json",
        "curve_normal_form": RESULTS / "zero-anchor-curve-normal-form.json",
        "parameter_curve": RESULTS / "parameter-curve.json",
        "finite_basis": RESULTS / "finite-basis.json",
        "bad_incidence": RESULTS / "bad-incidence-geometry.json",
        "proof_redteam": RESULTS / "proof-chain-independent.json",
        "independent_resultants": RESULTS / "zero-anchor-resultants-independent.json",
    }

    commands = [
        (
            "verify_parameter_regression.py",
            [relative(DATA / "parameter-regression-t4-t5.json")],
        ),
        ("verify_subiaco_symbolic_identities.py", []),
        (
            "verify_inverse_pair_hsf_family.py",
            [
                "--input",
                relative(DATA / "inverse-pair-direct-family.json"),
                "--output",
                relative(generated["inverse_pair"]),
            ],
        ),
        (
            "verify_subiaco_bridge_reductions.py",
            ["--dimensions", "4", "6", "8", "--output", relative(generated["subiaco_bridge"])],
        ),
        (
            "verify_subiaco_cubic_image_sum.py",
            ["--output", relative(generated["cubic_sum"])],
        ),
        (
            "verify_zero_anchor_multiplier_resultants.py",
            ["--output", relative(generated["zero_anchor"])],
        ),
        (
            "verify_e0513_zero_anchor_curve_normal_form.py",
            ["--output", relative(generated["curve_normal_form"])],
        ),
        (
            "verify_e0514_parameter_curve_and_linearization.py",
            ["--output", relative(generated["parameter_curve"])],
        ),
        (
            "construct_e0516_zero_anchor_finite_basis.py",
            ["--output", relative(generated["finite_basis"])],
        ),
        (
            "verify_e0516_bad_incidence_geometry.py",
            [relative(generated["finite_basis"]), "--output", relative(generated["bad_incidence"])],
        ),
        (
            "verify_e0517_e0516_proof_chain_independent.py",
            [relative(generated["finite_basis"]), "--output", relative(generated["proof_redteam"])],
        ),
        (
            "verify_e0521_zero_anchor_resultants_independent.py",
            ["--output", relative(generated["independent_resultants"])],
        ),
    ]
    runs = [run(script, arguments) for script, arguments in commands]

    artifacts: dict[str, object] = {}
    for name, path in generated.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        status = str(payload.get("status", ""))
        if "PASS" not in status:
            raise AssertionError(f"unexpected status for {name}: {status}")
        artifacts[name] = {
            "path": relative(path),
            "sha256": sha256(path),
            "status": status,
        }

    source_files = [
        ROOT / "README.md",
        ROOT / "LICENSE-DOCS-CC-BY-4.0.md",
        ROOT / "LICENSE-CODE-MIT.txt",
        ROOT / "LICENSE-DATA-CC0.md",
        ROOT / "run_reproduction.py",
        *sorted(SRC.glob("*.py")),
        *sorted(DATA.glob("*.json")),
        *generated.values(),
    ]
    missing = [str(path) for path in source_files if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"verification files missing: {missing}")
    scan_private_paths(source_files)

    manifest = {
        "title": "Proper transposed sesqui arrays at all Sylvester--Hadamard powers",
        "release": "v0.3-beta",
        "author": "Carptopus",
        "contact": "carptopus@163.com",
        "mathematical_status": "INTERNAL_CANDIDATE_EXTERNAL_REVIEW_PENDING",
        "licenses": {
            "documentation": "CC BY 4.0",
            "python_code": "MIT",
            "json_data_certificates_and_manifests": "CC0 1.0",
        },
        "files": [
            {
                "path": relative(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in source_files
        ],
        "status": "PASS_PUBLIC_VERIFICATION_MANIFEST_NO_PRIVATE_PATHS",
    }
    manifest_path = ROOT / "MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    result = {
        "title": manifest["title"],
        "release": manifest["release"],
        "python": sys.version,
        "commands": runs,
        "artifacts": artifacts,
        "manifest": {
            "path": relative(manifest_path),
            "sha256": sha256(manifest_path),
            "file_count": len(source_files),
        },
        "release_gate": {
            "internal_reproduction": True,
            "private_path_scan": True,
            "human_author_selected": True,
            "author": "Carptopus",
            "licenses_selected": True,
            "external_review_complete": False,
            "ai_assisted_disclosure": True,
        },
        "status": "PASS_PUBLIC_REPRODUCTION_EXTERNAL_REVIEW_PENDING",
    }
    result_path = RESULTS / "reproduction.json"
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
