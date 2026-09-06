"""Frozen limitations + conformance + runtime_manifest fixtures stay aligned with regenerators."""

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
import runtime_manifest  # noqa: E402

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
    def test_all_fixtures_match_module_output(self):
        lim_fixture = json.loads((ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8"))
        conf_fixture = json.loads(
            (ROOT / "fixtures" / "conformance_report.json").read_text(encoding="utf-8")
        )
        man_fixture = json.loads(
            (ROOT / "fixtures" / "runtime_manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(lim_fixture, limitations.limitations())
        self.assertEqual(conf_fixture, conformance.run_conformance())
        self.assertEqual(man_fixture, runtime_manifest.manifest())

    def test_regenerate_all_rewrites_stable_fixtures(self):
        before_lim = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        before_conf = (ROOT / "fixtures" / "conformance_report.json").read_text(encoding="utf-8")
        before_man = (ROOT / "fixtures" / "runtime_manifest.json").read_text(encoding="utf-8")
        code = _load_main("regenerate_all_frozen_docs.py")()
        self.assertEqual(code, 0)
        after_lim = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        after_conf = (ROOT / "fixtures" / "conformance_report.json").read_text(encoding="utf-8")
        after_man = (ROOT / "fixtures" / "runtime_manifest.json").read_text(encoding="utf-8")
        self.assertEqual(after_lim, before_lim)
        self.assertEqual(after_conf, before_conf)
        self.assertEqual(after_man, before_man)
        self.assertEqual(json.loads(after_lim), limitations.limitations())
        self.assertEqual(json.loads(after_conf), conformance.run_conformance())
        self.assertEqual(json.loads(after_man), runtime_manifest.manifest())

    def test_regenerate_limitations_script_stable(self):
        before = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        code = _load_main("regenerate_limitations.py")()
        self.assertEqual(code, 0)
        after = (ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8")
        self.assertEqual(after, before)

    def test_regenerate_runtime_manifest_script_stable(self):
        before = (ROOT / "fixtures" / "runtime_manifest.json").read_text(encoding="utf-8")
        code = _load_main("regenerate_runtime_manifest.py")()
        self.assertEqual(code, 0)
        after = (ROOT / "fixtures" / "runtime_manifest.json").read_text(encoding="utf-8")
        self.assertEqual(after, before)

    def test_check_succeeds_when_fixtures_match(self):
        for script in (
            "regenerate_limitations.py",
            "regenerate_conformance_report.py",
            "regenerate_runtime_manifest.py",
            "regenerate_all_frozen_docs.py",
        ):
            with self.subTest(script=script):
                code = _load_main(script)(["--check"])
                self.assertEqual(code, 0)

    def test_check_fails_on_limitations_mismatch_without_write(self):
        path = ROOT / "fixtures" / "limitations.json"
        original = path.read_text(encoding="utf-8")
        try:
            path.write_text(original.replace('"LIMITATIONS"', '"TAMPERED"', 1), encoding="utf-8")
            mutated = path.read_text(encoding="utf-8")
            self.assertNotEqual(mutated, original)
            code = _load_main("regenerate_limitations.py")(["--check"])
            self.assertNotEqual(code, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), mutated)
            code_all = _load_main("regenerate_all_frozen_docs.py")(["--check"])
            self.assertNotEqual(code_all, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), mutated)
        finally:
            path.write_text(original, encoding="utf-8")

    def test_check_fails_on_conformance_mismatch_without_write(self):
        path = ROOT / "fixtures" / "conformance_report.json"
        original = path.read_text(encoding="utf-8")
        try:
            path.write_text(original.replace('"CONFORMANT"', '"TAMPERED"', 1), encoding="utf-8")
            mutated = path.read_text(encoding="utf-8")
            self.assertNotEqual(mutated, original)
            code = _load_main("regenerate_conformance_report.py")(["--check"])
            self.assertNotEqual(code, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), mutated)
            code_all = _load_main("regenerate_all_frozen_docs.py")(["--check"])
            self.assertNotEqual(code_all, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), mutated)
        finally:
            path.write_text(original, encoding="utf-8")

    def test_check_fails_on_runtime_manifest_mismatch_without_write(self):
        path = ROOT / "fixtures" / "runtime_manifest.json"
        original = path.read_text(encoding="utf-8")
        try:
            path.write_text(original.replace('"RUNTIME_MANIFEST"', '"TAMPERED"', 1), encoding="utf-8")
            mutated = path.read_text(encoding="utf-8")
            self.assertNotEqual(mutated, original)
            code = _load_main("regenerate_runtime_manifest.py")(["--check"])
            self.assertNotEqual(code, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), mutated)
            code_all = _load_main("regenerate_all_frozen_docs.py")(["--check"])
            self.assertNotEqual(code_all, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), mutated)
        finally:
            path.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
