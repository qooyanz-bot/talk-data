#!/usr/bin/env python3
"""Rebuild fixtures/conformance_report.json from run_conformance().

Deterministic freeze (no timestamps). Do not hand-edit the fixture.
Run from repository root:

  python address/reference-runtime-v0.1/tools/regenerate_conformance_report.py

Or from this package directory:

  python tools/regenerate_conformance_report.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import conformance  # noqa: E402

FIXTURES = ROOT / "fixtures"
OUT = FIXTURES / "conformance_report.json"


def main() -> int:
    report = conformance.run_conformance()
    OUT.write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    try:
        display = OUT.relative_to(Path.cwd())
    except ValueError:
        display = OUT
    print(f"wrote {display}")
    print(f"status={report.get('status')} checks={len(report.get('checks', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
