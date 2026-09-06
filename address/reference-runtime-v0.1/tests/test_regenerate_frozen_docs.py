"""Frozen limitations + conformance fixtures stay aligned with regenerators."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import conformance  # noqa: E402
import limitations  # noqa: E402

TOOLS = ROOT / "tools"


def _load_main(script_name: str):
    path = TOOLS / script_name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main


class RegenerateFrozenDocsTests(unittest.TestCase):
    def test_both_fixtures_match_module_output(self):
        lim_fixture = json.loads((ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8"))
        conf_fixture = json.loads(
            (ROOT / "fixtures" / "conformance_report.json").read_text(encoding="utf-8")
        )
        self.assertEqual(lim_fixture, limitations.limitations())
        self.assertEqual(conf_fixture, conformance.run_conformance())

    def test_regenerate_all_rewrites_stable_fixtures(self):
        before_lim = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        before_conf = (ROOT / "fixtures" / "conformance_report.json").read_text(encoding="utf-8")
        code = _load_main("regenerate_all_frozen_docs.py")()
        self.assertEqual(code, 0)
        after_lim = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        after_conf = (ROOT / "fixtures" / "conformance_report.json").read_text(encoding="utf-8")
        self.assertEqual(after_lim, before_lim)
        self.assertEqual(after_conf, before_conf)
        self.assertEqual(json.loads(after_lim), limitations.limitations())
        self.assertEqual(json.loads(after_conf), conformance.run_conformance())

    def test_regenerate_limitations_script_stable(self):
        before = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        code = _load_main("regenerate_limitations.py")()
        self.assertEqual(code, 0)
        after = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
