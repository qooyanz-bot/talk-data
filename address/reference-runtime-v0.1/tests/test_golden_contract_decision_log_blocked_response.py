"""Freeze a saved public response with decision_log for --check-contract-only."""

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
import audit_log  # noqa: E402
import decision_log  # noqa: E402
import response_contract  # noqa: E402


class GoldenContractDecisionLogBlockedResponseTests(unittest.TestCase):
    def setUp(self):
        self.fixture_path = ROOT / "fixtures" / "golden_contract_decision_log_blocked_response.json"
        self.response = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        self.frozen_log = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json").read_text(encoding="utf-8")
        )

    def test_fixture_passes_response_contract_validate(self):
        self.assertEqual(response_contract.validate(self.response), [])
        self.assertEqual(self.response["resolution"]["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(self.response["resolution"]["value"])
        self.assertIsInstance(self.response["resolution"]["residual"], list)
        self.assertTrue(self.response["resolution"]["residual"])
        self.assertIsInstance(self.response["generated_audit"], dict)
        self.assertEqual(
            self.response["generated_audit"]["decision"],
            self.response["resolution"]["decision"],
        )
        self.assertEqual(self.response["protocol_claim"]["status"], "BLOCKED")
        self.assertIsNone(self.response["protocol_claim"]["value"])
        self.assertEqual(self.response["decision_log"], self.frozen_log)
        self.assertIsNone(self.response["decision_log"]["value"])
        self.assertEqual(self.response["decision_log"]["claim_status"], "BLOCKED")
        self.assertEqual(decision_log.verify(self.response["decision_log"]), [])

    def test_check_contract_only_cli_accepts_fixture(self):
        buf = StringIO()
        with redirect_stdout(buf):
            code = address_cli.main(["--check-contract-only", str(self.fixture_path)])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "CONTRACT_OK")
        self.assertEqual(payload["errors"], [])

    def test_fixture_fails_when_decision_log_id_tampered(self):
        broken = copy.deepcopy(self.response)
        broken["decision_log"]["decision_log_id"] = "decision_log:" + "0" * 64
        errors = response_contract.validate(broken)
        self.assertTrue(any("decision_log_id" in err for err in errors))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered_id.json"
            path.write_text(json.dumps(broken), encoding="utf-8")
            buf = StringIO()
            with redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "CONTRACT_INVALID")
            self.assertTrue(any("decision_log_id" in err for err in payload["errors"]))

    def test_fixture_fails_when_decision_log_value_filled(self):
        broken = copy.deepcopy(self.response)
        broken["decision_log"]["value"] = "invented"
        # Recompute content-address so the failure is specifically the public value=null rule.
        payload = dict(broken["decision_log"])
        payload.pop("decision_log_id", None)
        broken["decision_log"]["decision_log_id"] = (
            "decision_log:" + audit_log.content_digest(payload).removeprefix("sha256:")
        )
        errors = response_contract.validate(broken)
        self.assertIn("public decision_log value must be null", errors)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "filled_decision_log_value.json"
            path.write_text(json.dumps(broken), encoding="utf-8")
            buf = StringIO()
            with redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 1)
            payload_out = json.loads(buf.getvalue())
            self.assertEqual(payload_out["status"], "CONTRACT_INVALID")
            self.assertIn("public decision_log value must be null", payload_out["errors"])


if __name__ == "__main__":
    unittest.main()
