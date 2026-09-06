#!/usr/bin/env python3
"""Rebuild fixtures/limitations.json from limitations.limitations().

Deterministic freeze (no timestamps). Do not hand-edit the fixture.
Run from repository root:

  python address/reference-runtime-v0.1/tools/regenerate_limitations.py

Or from this package directory:

  python tools/regenerate_limitations.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import limitations  # noqa: E402

FIXTURES = ROOT / "fixtures"
OUT = FIXTURES / "limitations.json"


def main() -> int:
    doc = limitations.limitations()
    OUT.write_text(
        json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    try:
        display = OUT.relative_to(Path.cwd())
    except ValueError:
        display = OUT
    print(f"wrote {display}")
    print(f"status={doc.get('status')} keys={len(doc)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
