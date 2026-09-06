"""Content-addressed package manifest helper for Address reference runtime v0.1.

Builds a deterministic, content-addressed digest of frozen reference runtime
source files. Platform-independent (LF normalized).

The generated package_digest (sha256:<64 hex>) can be quoted by
Address.lineage.runtime_sha to reference this exact runtime implementation.
Lineage runtime_sha remains optional (null is allowed) and is never forced on
all Addresses.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "address-runtime-manifest-v1"
STATUS = "RUNTIME_MANIFEST"

# Frozen reference runtime python source files in deterministic sort order.
FROZEN_FILES: tuple[str, ...] = (
    "address_cli.py",
    "address_runtime.py",
    "audit_log.py",
    "conformance.py",
    "decision_log.py",
    "evidence_contract.py",
    "limitations.py",
    "protocol_claim_gate.py",
    "replay_verifier.py",
    "resolution_gate.py",
    "response_contract.py",
    "runtime_manifest.py",
)

REQUIRED_KEYS = {"schema_version", "status", "package_digest", "files"}
REQUIRED_FILE_KEYS = {"path", "sha256", "bytes"}


def _package_root(root: Path | None = None) -> Path:
    return root if root is not None else Path(__file__).resolve().parent


def file_entry(relpath: str, root: Path | None = None) -> dict[str, Any]:
    """Compute deterministic entry for a frozen file with LF normalization."""
    base = _package_root(root)
    target = base / relpath
    # Normalize CRLF to LF so sha256 and bytes are identical across Windows and Linux.
    normalized = target.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    hex_digest = hashlib.sha256(normalized).hexdigest()
    return {
        "bytes": len(normalized),
        "path": relpath,
        "sha256": f"sha256:{hex_digest}",
    }


def package_digest(root: Path | None = None) -> str:
    """Return content-addressed digest (sha256:<hex>) of the frozen files manifest."""
    base = _package_root(root)
    files = [file_entry(name, base) for name in FROZEN_FILES]
    payload = {
        "files": files,
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
    }
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def manifest(root: Path | None = None) -> dict[str, Any]:
    """Build the full content-addressed runtime manifest document."""
    base = _package_root(root)
    files = [file_entry(name, base) for name in FROZEN_FILES]
    digest = package_digest(base)
    return {
        "files": files,
        "package_digest": digest,
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
    }


# Alias
build_manifest = manifest


def verify_manifest(doc: Any, root: Path | None = None) -> list[str]:
    """Verify runtime manifest document against expected shape and on-disk files."""
    if not isinstance(doc, dict):
        return ["runtime manifest must be an object"]
    missing = REQUIRED_KEYS - set(doc)
    if missing:
        return ["missing required fields: " + ", ".join(sorted(missing))]
    if doc.get("schema_version") != SCHEMA_VERSION:
        return [f"unsupported runtime manifest schema_version: {doc.get('schema_version')}"]
    if doc.get("status") != STATUS:
        return [f"status must be {STATUS}"]
    files = doc.get("files")
    if not isinstance(files, list):
        return ["files must be a list"]
    for idx, entry in enumerate(files):
        if not isinstance(entry, dict) or set(entry) != REQUIRED_FILE_KEYS:
            return [f"files[{idx}] must contain exactly path, sha256, bytes"]
        if not isinstance(entry.get("path"), str) or not isinstance(entry.get("sha256"), str) or not isinstance(entry.get("bytes"), int):
            return [f"files[{idx}] has invalid field types"]
    expected = manifest(root)
    if doc.get("package_digest") != expected["package_digest"]:
        return ["package_digest does not match current runtime files digest"]
    if doc.get("files") != expected["files"]:
        return ["files entries do not match current runtime files"]
    return []


def main(argv: list[str] | None = None) -> int:
    doc = manifest()
    print(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
