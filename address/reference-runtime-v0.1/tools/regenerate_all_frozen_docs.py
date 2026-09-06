#!/usr/bin/env python3
"""Rebuild frozen limitations + conformance fixtures via their regenerators.

Calls regenerate_limitations then regenerate_conformance_report.
Does not touch contract goldens (use regenerate_contract_goldens.py).
Run from repository root:

  python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py
  python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py --check

Or from this package directory:

  python tools/regenerate_all_frozen_docs.py
  python tools/regenerate_all_frozen_docs.py --check

--check: dry-run via both regenerators; exit 0 if both fixtures match;
exit non-zero if any rewrite would change files (does not write).
"""

from __future__ import annotations

import argparse
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rebuild frozen limitations + conformance fixtures."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="dry-run: exit 0 if fixtures match; non-zero if rewrite would change them",
    )
    args = parser.parse_args([] if argv is None else argv)
    child_argv = ["--check"] if args.check else []
    for name in (
        "regenerate_limitations.py",
        "regenerate_conformance_report.py",
    ):
        code = _load_main(name)(child_argv)
        if code:
            return int(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
