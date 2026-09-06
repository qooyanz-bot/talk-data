#!/usr/bin/env python3
"""Rebuild frozen limitations + conformance fixtures via their regenerators.

Calls regenerate_limitations then regenerate_conformance_report.
Does not touch contract goldens (use regenerate_contract_goldens.py).
Run from repository root:

  python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py

Or from this package directory:

  python tools/regenerate_all_frozen_docs.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def _load_main(script_name: str):
    path = TOOLS / script_name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main


def main() -> int:
    for name in (
        "regenerate_limitations.py",
        "regenerate_conformance_report.py",
    ):
        code = _load_main(name)()
        if code:
            return int(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
