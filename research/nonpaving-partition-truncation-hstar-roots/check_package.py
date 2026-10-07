"""Read-only portable package-integrity guard; not a mathematical verifier."""
import hashlib
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def read_manifest(path):
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if len(line) < 67 or line[64:66] != "  ":
            raise RuntimeError("Malformed manifest: " + str(path))
        expected, name = line[:64].upper(), line[66:]
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or name in result:
            raise RuntimeError("Unsafe or duplicate path: " + name)
        if any(c not in "0123456789ABCDEF" for c in expected):
            raise RuntimeError("Invalid digest: " + name)
        result[name] = expected
    return result


def main():
    root = Path(__file__).resolve().parent
    entries = read_manifest(root / "SHA256SUMS.txt")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*")
              if p.is_file() and "__pycache__" not in p.parts}
    if actual != set(entries) | {"SHA256SUMS.txt"}:
        raise RuntimeError("Missing or extra package files: " + repr(actual ^ (set(entries) | {"SHA256SUMS.txt"})))
    for name, expected in entries.items():
        if digest(root / name) != expected:
            raise RuntimeError("SHA-256 mismatch: " + name)
    closure_root = root / "proof-dossier"
    manifests = list(closure_root.glob("loops/*PUBLICATION-PREP-0001/*.sha256"))
    if len(manifests) != 1:
        raise RuntimeError("Expected one frozen closure manifest")
    closure = read_manifest(manifests[0])
    expected_count = 216 if root.name == "paving-hstar-eventual-real-rootedness" else 37
    if len(closure) != expected_count:
        raise RuntimeError("Closure count mismatch")
    for name, expected in closure.items():
        if digest(closure_root / name) != expected:
            raise RuntimeError("Frozen dependency mismatch: " + name)
    actual_closure = {p.relative_to(closure_root).as_posix() for p in closure_root.rglob("*") if p.is_file()}
    if actual_closure != set(closure) | {manifests[0].relative_to(closure_root).as_posix()}:
        raise RuntimeError("Closure has missing or extra files")
    print(f"PASS: {len(entries)} package digests; exact {expected_count}-file proof closure")


if __name__ == "__main__":
    main()
