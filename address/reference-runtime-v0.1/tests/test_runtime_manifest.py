"""Tests for runtime_manifest content-addressed package digest and CLI mode."""

from __future__ import annotations

import contextlib
import copy
import json
import re
import sys
import unittest
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402
import runtime_manifest  # noqa: E402


class RuntimeManifestTests(unittest.TestCase):
    def test_frozen_files_tuple_sorted_and_nonempty(self):
        self.assertIsInstance(runtime_manifest.FROZEN_FILES, tuple)
        self.assertTrue(len(runtime_manifest.FROZEN_FILES) > 0)
        self.assertEqual(
            list(runtime_manifest.FROZEN_FILES),
            sorted(runtime_manifest.FROZEN_FILES),
        )
        for name in runtime_manifest.FROZEN_FILES:
            path = ROOT / name
            self.assertTrue(path.is_file(), f"missing frozen file: {name}")

    def test_manifest_structure_and_types(self):
        doc = runtime_manifest.manifest()
        self.assertEqual(set(doc), runtime_manifest.REQUIRED_KEYS)
        self.assertEqual(doc["schema_version"], runtime_manifest.SCHEMA_VERSION)
        self.assertEqual(doc["status"], runtime_manifest.STATUS)
        self.assertTrue(re.fullmatch(r"sha256:[0-9a-f]{64}", doc["package_digest"]))
        self.assertIsInstance(doc["files"], list)
        self.assertEqual(len(doc["files"]), len(runtime_manifest.FROZEN_FILES))
        for idx, entry in enumerate(doc["files"]):
            with self.subTest(idx=idx, path=entry.get("path")):
                self.assertEqual(set(entry), runtime_manifest.REQUIRED_FILE_KEYS)
                self.assertIsInstance(entry["path"], str)
                self.assertTrue(re.fullmatch(r"sha256:[0-9a-f]{64}", entry["sha256"]))
                self.assertIsInstance(entry["bytes"], int)
                self.assertGreater(entry["bytes"], 0)

    def test_package_digest_is_deterministic(self):
        digest1 = runtime_manifest.package_digest()
        digest2 = runtime_manifest.package_digest()
        self.assertEqual(digest1, digest2)
        self.assertEqual(runtime_manifest.manifest()["package_digest"], digest1)

    def test_verify_manifest_accepts_valid_manifest(self):
        doc = runtime_manifest.manifest()
        errors = runtime_manifest.verify_manifest(doc)
        self.assertEqual(errors, [])

    def test_verify_manifest_detects_tamper(self):
        doc = runtime_manifest.manifest()
        tampered_digest = copy.deepcopy(doc)
        tampered_digest["package_digest"] = "sha256:" + "0" * 64
        self.assertTrue(any("package_digest" in e for e in runtime_manifest.verify_manifest(tampered_digest)))

        tampered_schema = copy.deepcopy(doc)
        tampered_schema["schema_version"] = "wrong-version"
        self.assertTrue(any("schema_version" in e for e in runtime_manifest.verify_manifest(tampered_schema)))

        tampered_status = copy.deepcopy(doc)
        tampered_status["status"] = "WRONG_STATUS"
        self.assertTrue(any("status" in e for e in runtime_manifest.verify_manifest(tampered_status)))

        tampered_files = copy.deepcopy(doc)
        tampered_files["files"][0]["bytes"] = 99999999
        self.assertTrue(any("files entries" in e for e in runtime_manifest.verify_manifest(tampered_files)))

    def test_cli_runtime_manifest_mode(self):
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main(["--runtime-manifest"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["schema_version"], runtime_manifest.SCHEMA_VERSION)
        self.assertEqual(payload["status"], runtime_manifest.STATUS)
        self.assertEqual(payload["package_digest"], runtime_manifest.package_digest())
        self.assertEqual(payload, runtime_manifest.manifest())

    def test_cli_runtime_manifest_rejects_conflicts(self):
        cases = [
            ["address.json", "evidence.json"],
            ["--limitations"],
            ["--conformance"],
            ["--check-contract-only", str(ROOT / "fixtures" / "golden_contract_ok_response.json")],
            ["--verify-decision-log", str(ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json")],
            ["--validate-protocol-manifest", str(ROOT / "fixtures" / "r6g_frozen_protocol_manifest.json")],
            ["--now", "2026-09-06T00:00:00Z"],
        ]
        for extra in cases:
            with self.subTest(extra=extra):
                buf = StringIO()
                with contextlib.redirect_stdout(buf):
                    code = address_cli.main(["--runtime-manifest", *extra])
                self.assertEqual(code, 2)
                payload = json.loads(buf.getvalue())
                self.assertEqual(payload["status"], "INVALID_INPUT")
                self.assertTrue(payload["errors"])

    def test_lineage_runtime_sha_compatibility(self):
        fixture_path = ROOT / "fixtures" / "valid_synthetic_address.json"
        address = json.loads(fixture_path.read_text(encoding="utf-8"))
        # Quote runtime_manifest.package_digest in lineage.runtime_sha
        digest = runtime_manifest.package_digest()
        address["lineage"]["runtime_sha"] = digest
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
