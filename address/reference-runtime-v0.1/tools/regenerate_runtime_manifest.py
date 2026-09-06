#!/usr/bin/env python3
"""Rebuild fixtures/runtime_manifest.json from runtime_manifest.manifest().

Deterministic freeze of the reference-runtime files and package_digest.
Run from repository root:

  python address/reference-runtime-v0.1/tools/regenerate_runtime_manifest.py
  python address/reference-runtime-v0.1/tools/regenerate_runtime_manifest.py --check

Or from this package directory:

  python tools/regenerate_runtime_manifest.py
  python tools/regenerate_runtime_manifest.py --check

--check: dry-run; exit 0 if fixture matches; non-zero if rewrite would change it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import runtime_manifest  # noqa: E402

FIXTURES = ROOT / "fixtures"
OUT = FIXTURES / "runtime_manifest.json"


def _display(path: Path) -> Path:
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


def _generated_text() -> str:
    doc = runtime_manifest.manifest()
    return json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rebuild fixtures/runtime_manifest.json from runtime_manifest.manifest()."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="dry-run: exit 0 if fixture matches; non-zero if rewrite would change it",
    )
    args = parser.parse_args([] if argv is None else argv)
    text = _generated_text()
    display = _display(OUT)
    if args.check:
        if not OUT.is_file():
            print(f"missing {display}", file=sys.stderr)
            return 1
        on_disk = OUT.read_text(encoding="utf-8")
        if on_disk == text:
            print(f"ok {display}")
            return 0
        print(f"drift {display}", file=sys.stderr)
        return 1
    OUT.write_text(text, encoding="utf-8")
    doc = json.loads(text)
    print(f"wrote {display}")
    print(
        f"status={doc.get('status')} files={len(doc.get('files', []))} digest={doc.get('package_digest')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
