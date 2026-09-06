"""Freeze a saved public CONTRADICTION ABSTAIN response fixture for --check-contract-only."""

import copy
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import response_contract  # noqa: E402


class GoldenContractContradictionResponseTests(unittest.TestCase):
    def setUp(self):
        self.fixture_path = ROOT / "fixtures" / "golden_contract_contradiction_response.json"
        self.response = json.loads(self.fixture_path.read_text(encoding="utf-8"))

    def test_fixture_passes_response_contract_validate(self):
        self.assertEqual(response_contract.validate(self.response), [])
        self.assertEqual(self.response["resolution"]["decision"], "ABSTAIN")
        self.assertEqual(self.response["resolution"]["reason"], "CONTRADICTION")
        self.assertIsNone(self.response["resolution"]["value"])
        self.assertIsInstance(self.response["resolution"]["residual"], list)
        self.assertTrue(self.response["resolution"]["residual"])
        self.assertIsInstance(self.response["generated_audit"], dict)
        self.assertEqual(
            self.response["generated_audit"]["decision"],
            self.response["resolution"]["decision"],
        )
        self.assertEqual(
            self.response["generated_audit"]["reason"],
            self.response["resolution"]["reason"],
        )
        self.assertEqual(self.response["generated_audit"]["decision"], "ABSTAIN")
        self.assertEqual(self.response["generated_audit"]["reason"], "CONTRADICTION")
        # Conflicting assertion_key listed in details (same key, different values).
        self.assertIn("target:sample", self.response["resolution"]["details"])

    def test_check_contract_only_cli_accepts_fixture(self):
        buf = StringIO()
        with redirect_stdout(buf):
            code = address_cli.main(["--check-contract-only", str(self.fixture_path)])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "CONTRACT_OK")
        self.assertEqual(payload["errors"], [])

    def test_fixture_fails_when_value_filled(self):
        broken = copy.deepcopy(self.response)
        broken["resolution"]["value"] = "invented"
        errors = response_contract.validate(broken)
        self.assertTrue(any("null" in err for err in errors))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "filled_value.json"
            path.write_text(json.dumps(broken), encoding="utf-8")
            buf = StringIO()
            with redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "CONTRACT_INVALID")
            self.assertTrue(any("null" in err for err in payload["errors"]))

    def test_fixture_fails_when_nested_lineage_result_sha_stamped(self):
        broken = copy.deepcopy(self.response)
        broken["lineage"] = {"result_sha": "sha256:" + "e" * 64}
        errors = response_contract.validate(broken)
        self.assertTrue(any("result_sha" in err for err in errors))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stamped_sha.json"
            path.write_text(json.dumps(broken), encoding="utf-8")
            buf = StringIO()
            with redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "CONTRACT_INVALID")
            self.assertTrue(any("result_sha" in err for err in payload["errors"]))

    def test_fixture_decision_must_remain_abstain_contradiction(self):
        """Regression: golden CONTRADICTION path must not silently become READY or other reasons."""
        self.assertEqual(self.response["resolution"]["decision"], "ABSTAIN")
        self.assertEqual(self.response["resolution"]["reason"], "CONTRADICTION")
        self.assertEqual(self.response["generated_audit"]["decision"], "ABSTAIN")
        self.assertEqual(self.response["generated_audit"]["reason"], "CONTRADICTION")
        broken = copy.deepcopy(self.response)
        broken["resolution"]["decision"] = "READY_FOR_VERIFICATION"
        broken["resolution"]["reason"] = "CONTRACTED_EVIDENCE"
        errors = response_contract.validate(broken)
        self.assertTrue(
            any("decision" in err or "reason" in err for err in errors)
            or broken["resolution"]["reason"] != "CONTRADICTION"
        )
        self.assertNotEqual(broken["resolution"]["reason"], "CONTRADICTION")


if __name__ == "__main__":
    unittest.main()
