"""Offline one-entry reproduction for the Paley switching verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
ENTRY = ROOT.parent
RESULTS = ROOT / "results"


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path.relative_to(ENTRY)).replace("\\", "/")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed: {script}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return {
        "script": script,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout.strip()[-500:],
        "stderr_tail": completed.stderr.strip()[-500:],
    }


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_lf(path: Path) -> None:
    """Keep generated text consistent with the repository LF policy."""
    content = path.read_bytes()
    normalized = content.replace(b"\r\n", b"\n")
    if normalized != content:
        path.write_bytes(normalized)


def require_true_checks(payload: dict[str, object], label: str) -> str:
    checks = payload.get("checks")
    if not isinstance(checks, dict) or not checks or not all(checks.values()):
        raise AssertionError(f"failed checks in {label}: {checks}")
    return "PASS_ALL_CHECKS"


def validate_prime_fields(payload: dict[str, object]) -> str:
    records = payload.get("records")
    if not isinstance(records, list) or not records:
        raise AssertionError("prime-field records are missing")
    for record in records:
        if record.get("all_pair_identities_passed") is not True:
            raise AssertionError(f"prime-field identity failure: {record}")
        q = int(record["q"])
        pair_count = int(record["admissible_pair_count"])
        if q == 7:
            if pair_count != 0 or record.get("array_audit") is not None:
                raise AssertionError("q=7 boundary did not remain empty")
        elif q >= 11:
            if pair_count <= 0 or not isinstance(record.get("array_audit"), dict):
                raise AssertionError(f"missing witness or array audit for q={q}")
    return "PASS_FROZEN_PRIME_FIELDS"


def validate_gf27(payload: dict[str, object]) -> str:
    if payload.get("field") != "GF(3)[z]/(z^3+2z+1)":
        raise AssertionError("unexpected GF(27) model")
    if int(payload.get("alpha_count", 0)) <= 0:
        raise AssertionError("GF(27) has no admissible alpha")
    if int(payload.get("admissible_pair_count", 0)) <= 0:
        raise AssertionError("GF(27) has no admissible switch")
    audit = payload.get("array_audit")
    if not isinstance(audit, dict):
        raise AssertionError("GF(27) complete-array audit is missing")
    expected = {"v": 54, "r": 27, "c": 28, "e": 14, "cc": 13, "rc": 14}
    if audit.get("parameters") != expected:
        raise AssertionError(f"unexpected GF(27) parameters: {audit.get('parameters')}")
    spectrum = audit.get("rr_spectrum")
    if not isinstance(spectrum, dict) or len(spectrum) <= 1:
        raise AssertionError("GF(27) row concurrence is not proper")
    return "PASS_GF27_COMPLETE_ARRAY"


def scan_private_paths(paths: list[Path]) -> None:
    forbidden = [
        "D:" + "\\Codes\\",
        "E:" + "\\Documents\\",
        "Z:" + "\\TEMP\\",
        "C:" + "\\Users\\",
        "Admin" + "istrator",
    ]
    text_suffixes = {".md", ".py", ".json", ".txt", ".tex"}
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
    scripts = [
        "verify_general_paley_switch_symbolic.py",
        "verify_general_paley_switch_character_count.py",
        "verify_general_paley_switch_prime_fields.py",
        "verify_general_paley_switch_gf27_independent.py",
        "audit_general_paley_switch_generic_fields.py",
        "audit_q11_youden_certificate_independent.py",
    ]
    runs = [run(script) for script in scripts]

    generated = {
        "symbolic": RESULTS / "general-paley-switch-symbolic.json",
        "character_count": RESULTS / "general-paley-switch-character-count.json",
        "prime_fields": RESULTS / "general-paley-switch-primes.json",
        "gf27": RESULTS / "general-paley-switch-gf27.json",
        "generic_fields": RESULTS / "audit-paley-switch-generic-fields.json",
        "q11_youden": RESULTS / "audit-paley-switch-q11-youden-independent.json",
    }
    missing = [str(path) for path in generated.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"generated verification files missing: {missing}")
    for path in generated.values():
        normalize_lf(path)

    payloads = {name: load_json(path) for name, path in generated.items()}
    statuses = {
        "symbolic": require_true_checks(payloads["symbolic"], "symbolic"),
        "character_count": require_true_checks(payloads["character_count"], "character_count"),
        "prime_fields": validate_prime_fields(payloads["prime_fields"]),
        "gf27": validate_gf27(payloads["gf27"]),
        "generic_fields": require_true_checks(payloads["generic_fields"], "generic_fields"),
        "q11_youden": require_true_checks(payloads["q11_youden"], "q11_youden"),
    }
    artifacts = {
        name: {
            "path": relative(path),
            "sha256": sha256(path),
            "status": statuses[name],
        }
        for name, path in generated.items()
    }

    static_data = [
        RESULTS / "audit-paley-switch-q11-youden-completion.json",
        RESULTS / "audit-paley-switch-q11-certificate.json",
    ]
    source_files = [
        ROOT / "README.md",
        ROOT / "LICENSE-DOCS-CC-BY-4.0.md",
        ROOT / "LICENSE-CODE-MIT.txt",
        ROOT / "LICENSE-DATA-CC0.md",
        ROOT / "run_reproduction.py",
        *(ROOT / script for script in scripts),
        *static_data,
        *generated.values(),
    ]
    entry_text_files = [
        ENTRY / "README.md",
        ENTRY / "LICENSE.md",
        ENTRY / "paley-two-edge-switching.tex",
    ]
    missing = [str(path) for path in [*source_files, *entry_text_files] if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"distributed files missing: {missing}")
    scan_private_paths([*source_files, *entry_text_files])

    manifest = {
        "title": "Paley two-edge switching for proper transposed sesqui arrays",
        "release": "v0.3-beta",
        "author": "Carptopus",
        "contact": "carptopus@163.com",
        "mathematical_status": "INTERNAL_CANDIDATE_EXTERNAL_REVIEW_PENDING",
        "licenses": {
            "documentation": "CC BY 4.0",
            "python_code": "MIT",
            "json_results_and_manifests": "CC0 1.0",
        },
        "files": [
            {"path": relative(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
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
